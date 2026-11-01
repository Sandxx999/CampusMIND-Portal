import sqlite3
import psycopg2
from psycopg2.extras import execute_values
import json
from datetime import datetime, timezone

sqlite_path = 'backend/campusmind.db'
neon_url = 'postgresql://neondb_owner:npg_5bKD1NHQWPXF@ep-twilight-rice-azdm9om1-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require&hostaddr=13.251.213.89'

s_conn = sqlite3.connect(sqlite_path)
s_conn.row_factory = sqlite3.Row
s_cur = s_conn.cursor()

p_conn = psycopg2.connect(neon_url)
p_cur = p_conn.cursor()

# 1. Create students table in Neon if not exists
p_cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    enrollment_no VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    mobile_no VARCHAR(50) NOT NULL,
    branch VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    courses_enrolled TEXT NOT NULL,
    sgpa REAL NOT NULL,
    cgpa REAL NOT NULL,
    attendance_pct REAL NOT NULL,
    backlogs INTEGER NOT NULL,
    fee_status VARCHAR(50) NOT NULL
);
""")

# 2. Create okf_nodes and okf_edges in Neon if not exists
p_cur.execute("""
CREATE TABLE IF NOT EXISTS okf_nodes (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    properties JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS okf_edges (
    id VARCHAR(255) PRIMARY KEY,
    source_id VARCHAR(255) REFERENCES okf_nodes(id) ON DELETE CASCADE,
    target_id VARCHAR(255) REFERENCES okf_nodes(id) ON DELETE CASCADE,
    relation_type VARCHAR(100) NOT NULL,
    weight REAL DEFAULT 1.0,
    properties JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
""")
p_conn.commit()

tables_in_order = [
    # Reference tables
    'roles',
    'departments',
    'programs',
    'courses',
    'academic_terms',
    'announcements',
    'campus_events',
    'knowledge_documents',
    'system_tasks',
    'sso_provider_configs',
    
    # Core User & Profile tables
    'users',
    'student_profiles',
    'faculty_profiles',
    'admin_profiles',
    'students',
    
    # Academic & Log tables
    'course_offerings',
    'enrollments',
    'event_registrations',
    'attendance_records',
    'assessments',
    'assessment_grades',
    'academic_interventions',
    'student_action_plans',
    'notification_alerts',
    'query_logs',
    'query_feedback',
    'audit_events',
    
    # Graph tables
    'okf_nodes',
    'okf_edges',
    
    # Portal tables
    'portal_user_accounts',
    'portal_student_profiles',
    'portal_exam_results',
    'portal_schedule_slots',
    'portal_subject_resources',
    'portal_notice_board',
    'portal_student_skills',
    'portal_student_projects',
    'portal_student_certifications',
    'portal_student_experiences',
    'portal_student_achievements',
    'portal_student_activities',
    'portal_student_career_profiles',
    'portal_upcoming_tasks',
]

# Get existing tables in Postgres
p_cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
pg_tables = set(r[0] for r in p_cur.fetchall())

# For each table, copy data
for t in tables_in_order:
    if t not in pg_tables:
        print(f"Skipping {t}: not in Postgres")
        continue
    
    # Get column info from Postgres (name, data_type, is_nullable)
    p_cur.execute(f"""
        SELECT column_name, data_type, is_nullable 
        FROM information_schema.columns 
        WHERE table_schema = 'public' AND table_name = '{t}';
    """)
    pg_cols_info = {r[0]: (r[1], r[2]) for r in p_cur.fetchall()}
    
    # Get columns from SQLite
    try:
        s_cur.execute(f"PRAGMA table_info('{t}');")
        s_cols = [r['name'] for r in s_cur.fetchall()]
        if not s_cols:
            print(f"Skipping {t}: not in SQLite")
            continue
    except Exception as e:
        print(f"Could not read SQLite table {t}: {e}")
        continue
        
    common_cols = [c for c in s_cols if c in pg_cols_info]
    # Check if there are NOT NULL columns in PG not in SQLite (e.g. created_at)
    extra_not_null_cols = []
    for c, (dtype, nullable) in pg_cols_info.items():
        if c not in s_cols and nullable == 'NO':
            extra_not_null_cols.append((c, dtype))
            
    insert_cols = common_cols + [c for c, _ in extra_not_null_cols]
    
    s_cur.execute(f"SELECT * FROM \"{t}\";")
    rows = s_cur.fetchall()
    print(f"Table {t}: transferring {len(rows)} rows...")
    
    if not rows:
        continue
        
    now = datetime.now(timezone.utc)
    transformed_rows = []
    for r in rows:
        row_vals = []
        for c in common_cols:
            val = r[c]
            col_type, nullable = pg_cols_info[c]
            if val is None and nullable == 'NO':
                if 'timestamp' in col_type or 'date' in col_type:
                    val = now
                elif 'int' in col_type or 'float' in col_type or 'real' in col_type:
                    val = 0
                elif 'bool' in col_type:
                    val = False
                else:
                    val = ''
            elif col_type == 'boolean' and val is not None:
                val = bool(val)
            elif col_type == 'jsonb' and isinstance(val, str):
                try:
                    val = json.dumps(json.loads(val))
                except Exception:
                    pass
            elif ('timestamp' in col_type or 'date' in col_type) and isinstance(val, str):
                try:
                    val = datetime.fromisoformat(val)
                except Exception:
                    val = now
            row_vals.append(val)
            
        for c, dtype in extra_not_null_cols:
            if 'timestamp' in dtype or 'date' in dtype:
                row_vals.append(now)
            elif 'int' in dtype or 'real' in dtype:
                row_vals.append(0)
            elif 'bool' in dtype:
                row_vals.append(False)
            else:
                row_vals.append('')
                
        transformed_rows.append(tuple(row_vals))
        
    # Clear target table first
    p_cur.execute(f'TRUNCATE TABLE "{t}" CASCADE;')
    
    # Insert rows
    col_str = ', '.join([f'"{c}"' for c in insert_cols])
    val_placeholders = ', '.join(['%s'] * len(insert_cols))
    insert_sql = f'INSERT INTO "{t}" ({col_str}) VALUES ({val_placeholders})'
    
    p_cur.executemany(insert_sql, transformed_rows)
    p_conn.commit()

print("ALL DATA TRANSFERRED SUCCESSFULLY TO NEON POSTGRESQL!")
p_cur.close()
p_conn.close()
s_conn.close()
