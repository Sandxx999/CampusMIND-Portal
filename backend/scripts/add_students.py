import os
import sys
import json
import sqlite3
from passlib.context import CryptContext

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
seed_file = os.path.join(backend_dir, "data", "seed_data.json")
db_path = os.path.join(backend_dir, "campusmind.db")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
default_pw_hash = pwd_context.hash("password123")
sindhu_pw_hash = pwd_context.hash("sindhu123")
vaishnavi_pw_hash = pwd_context.hash("vaishnavi123")
satyajit_pw_hash = pwd_context.hash("satyajit123")

with open(seed_file, "r", encoding="utf-8") as f:
    data = json.load(f)

new_users = [
    {
        "id": "STU_2024_016",
        "role": "student",
        "email": "sindhu.viplav@campus.edu",
        "password_hash": default_pw_hash,
        "full_name": "Sindhu Viplav",
        "profile_photo_url": "https://ui-avatars.com/api/?name=Sindhu+Viplav",
        "department": "Artificial Intelligence"
    },
    {
        "id": "STU_2024_017",
        "role": "student",
        "email": "vaishnavi@campus.edu",
        "password_hash": default_pw_hash,
        "full_name": "Vaishnavi",
        "profile_photo_url": "https://ui-avatars.com/api/?name=Vaishnavi",
        "department": "Artificial Intelligence"
    },
    {
        "id": "STU_2024_018",
        "role": "student",
        "email": "satyajit@campus.edu",
        "password_hash": default_pw_hash,
        "full_name": "Satyajit",
        "profile_photo_url": "https://ui-avatars.com/api/?name=Satyajit",
        "department": "Artificial Intelligence"
    }
]

new_profiles = [
    {
        "student_id": "STU_2024_016",
        "roll_number": "24AI016",
        "program": "B.Tech Artificial Intelligence",
        "current_semester": 5,
        "batch_year": "2024-2028",
        "overall_attendance_pct": 93.5,
        "bio": "AI student researcher specializing in Natural Language Processing, Large Language Models, and Multimodal Intelligence systems.",
        "location": "Hyderabad",
        "academic_status": "Active",
        "links": json.dumps({"github": "https://github.com/sindhu-viplav", "linkedin": "https://linkedin.com/in/sindhu-viplav", "portfolio": "https://sindhuviplav.dev"})
    },
    {
        "student_id": "STU_2024_017",
        "roll_number": "24AI017",
        "program": "B.Tech Artificial Intelligence",
        "current_semester": 5,
        "batch_year": "2024-2028",
        "overall_attendance_pct": 91.0,
        "bio": "Aspiring AI engineer enthusiastic about Computer Vision, Edge AI, Autonomous Systems, and embedded neural networks.",
        "location": "Hyderabad",
        "academic_status": "Active",
        "links": json.dumps({"github": "https://github.com/vaishnavi-ai", "linkedin": "https://linkedin.com/in/vaishnavi-ai", "portfolio": "https://vaishnavi.dev"})
    },
    {
        "student_id": "STU_2024_018",
        "roll_number": "24AI018",
        "program": "B.Tech Artificial Intelligence",
        "current_semester": 5,
        "batch_year": "2024-2028",
        "overall_attendance_pct": 87.5,
        "bio": "Data science practitioner and AI full-stack developer dedicated to Big Data Analytics, Predictive Modeling, and Distributed ML systems.",
        "location": "Hyderabad",
        "academic_status": "Active",
        "links": json.dumps({"github": "https://github.com/satyajit-ds", "linkedin": "https://linkedin.com/in/satyajit-ds", "portfolio": "https://satyajit.dev"})
    }
]

new_exams = [
    # Sindhu
    {"student_id": "STU_2024_016", "exam_type": "Mid Term 1", "course_code": "AI301", "course_name": "Deep Learning", "marks_obtained": 39.0, "max_marks": 40.0, "grade": "A+", "status": "Pass"},
    {"student_id": "STU_2024_016", "exam_type": "Mid Term 1", "course_code": "CS201", "course_name": "Data Structures", "marks_obtained": 37.0, "max_marks": 40.0, "grade": "A+", "status": "Pass"},
    {"student_id": "STU_2024_016", "exam_type": "Mid Term 1", "course_code": "MATH202", "course_name": "Discrete Math", "marks_obtained": 36.0, "max_marks": 40.0, "grade": "A", "status": "Pass"},
    {"student_id": "STU_2024_016", "exam_type": "Mid Term 1", "course_code": "AI302", "course_name": "Knowledge Representation", "marks_obtained": 40.0, "max_marks": 40.0, "grade": "A+", "status": "Pass"},
    # Vaishnavi
    {"student_id": "STU_2024_017", "exam_type": "Mid Term 1", "course_code": "AI301", "course_name": "Deep Learning", "marks_obtained": 38.0, "max_marks": 40.0, "grade": "A+", "status": "Pass"},
    {"student_id": "STU_2024_017", "exam_type": "Mid Term 1", "course_code": "CS201", "course_name": "Data Structures", "marks_obtained": 36.0, "max_marks": 40.0, "grade": "A", "status": "Pass"},
    {"student_id": "STU_2024_017", "exam_type": "Mid Term 1", "course_code": "MATH202", "course_name": "Discrete Math", "marks_obtained": 35.0, "max_marks": 40.0, "grade": "A", "status": "Pass"},
    {"student_id": "STU_2024_017", "exam_type": "Mid Term 1", "course_code": "AI302", "course_name": "Knowledge Representation", "marks_obtained": 38.0, "max_marks": 40.0, "grade": "A+", "status": "Pass"},
    # Satyajit
    {"student_id": "STU_2024_018", "exam_type": "Mid Term 1", "course_code": "AI301", "course_name": "Deep Learning", "marks_obtained": 36.0, "max_marks": 40.0, "grade": "A", "status": "Pass"},
    {"student_id": "STU_2024_018", "exam_type": "Mid Term 1", "course_code": "CS201", "course_name": "Data Structures", "marks_obtained": 38.0, "max_marks": 40.0, "grade": "A+", "status": "Pass"},
    {"student_id": "STU_2024_018", "exam_type": "Mid Term 1", "course_code": "MATH202", "course_name": "Discrete Math", "marks_obtained": 37.0, "max_marks": 40.0, "grade": "A+", "status": "Pass"},
    {"student_id": "STU_2024_018", "exam_type": "Mid Term 1", "course_code": "AI302", "course_name": "Knowledge Representation", "marks_obtained": 36.0, "max_marks": 40.0, "grade": "A", "status": "Pass"}
]

new_skills = [
    # Sindhu
    {"student_id": "STU_2024_016", "name": "Python", "category": "Programming", "proficiency_pct": 94, "verified": True},
    {"student_id": "STU_2024_016", "name": "PyTorch", "category": "AI/ML", "proficiency_pct": 88, "verified": True},
    {"student_id": "STU_2024_016", "name": "NLP & LLMs", "category": "AI/ML", "proficiency_pct": 91, "verified": True},
    {"student_id": "STU_2024_016", "name": "Hugging Face", "category": "AI/ML", "proficiency_pct": 85, "verified": True},
    {"student_id": "STU_2024_016", "name": "FastAPI", "category": "Web", "proficiency_pct": 82, "verified": True},
    {"student_id": "STU_2024_016", "name": "LangChain", "category": "AI/ML", "proficiency_pct": 86, "verified": True},
    {"student_id": "STU_2024_016", "name": "React", "category": "Web", "proficiency_pct": 75, "verified": False},
    {"student_id": "STU_2024_016", "name": "Docker & MLOps", "category": "Tools", "proficiency_pct": 72, "verified": False},

    # Vaishnavi
    {"student_id": "STU_2024_017", "name": "Python", "category": "Programming", "proficiency_pct": 92, "verified": True},
    {"student_id": "STU_2024_017", "name": "OpenCV", "category": "AI/ML", "proficiency_pct": 89, "verified": True},
    {"student_id": "STU_2024_017", "name": "PyTorch", "category": "AI/ML", "proficiency_pct": 84, "verified": True},
    {"student_id": "STU_2024_017", "name": "YOLO & Object Detection", "category": "AI/ML", "proficiency_pct": 87, "verified": True},
    {"student_id": "STU_2024_017", "name": "TensorFlow Lite", "category": "AI/ML", "proficiency_pct": 78, "verified": True},
    {"student_id": "STU_2024_017", "name": "ROS2", "category": "Tools", "proficiency_pct": 72, "verified": False},
    {"student_id": "STU_2024_017", "name": "C++", "category": "Programming", "proficiency_pct": 80, "verified": True},
    {"student_id": "STU_2024_017", "name": "Docker", "category": "Tools", "proficiency_pct": 70, "verified": False},

    # Satyajit
    {"student_id": "STU_2024_018", "name": "Python", "category": "Programming", "proficiency_pct": 90, "verified": True},
    {"student_id": "STU_2024_018", "name": "SQL & PostgreSQL", "category": "Programming", "proficiency_pct": 88, "verified": True},
    {"student_id": "STU_2024_018", "name": "Apache Spark", "category": "Tools", "proficiency_pct": 80, "verified": True},
    {"student_id": "STU_2024_018", "name": "Machine Learning", "category": "AI/ML", "proficiency_pct": 85, "verified": True},
    {"student_id": "STU_2024_018", "name": "FastAPI", "category": "Web", "proficiency_pct": 86, "verified": True},
    {"student_id": "STU_2024_018", "name": "React", "category": "Web", "proficiency_pct": 76, "verified": False},
    {"student_id": "STU_2024_018", "name": "Scikit-Learn", "category": "AI/ML", "proficiency_pct": 88, "verified": True},
    {"student_id": "STU_2024_018", "name": "Kubernetes", "category": "Tools", "proficiency_pct": 68, "verified": False}
]

new_projects = [
    # Sindhu
    {
        "student_id": "STU_2024_016",
        "title": "NeuroLingua",
        "category": "AI / NLP",
        "description": "Multilingual Indic LLM Fine-Tuner for Academic Translation and cross-lingual comprehension.",
        "role": "Lead Researcher",
        "technologies": json.dumps(["Python", "PyTorch", "Hugging Face", "FastAPI"]),
        "status": "Active",
        "github_url": "https://github.com/sindhu-viplav/neurolingua",
        "live_demo_url": "https://neurolingua.demo.ai"
    },
    {
        "student_id": "STU_2024_016",
        "title": "DocuInsight AI",
        "category": "AI / Full Stack",
        "description": "Enterprise Document Question Answering using RAG and Vector Embeddings.",
        "role": "Full Stack Developer",
        "technologies": json.dumps(["LangChain", "ChromaDB", "FastAPI", "React"]),
        "status": "Completed",
        "github_url": "https://github.com/sindhu-viplav/docuinsight",
        "live_demo_url": ""
    },
    {
        "student_id": "STU_2024_016",
        "title": "AI Automated Code Reviewer",
        "category": "Dev Tools",
        "description": "Transformer-based AST static vulnerability detector and code improvement suggester.",
        "role": "Developer",
        "technologies": json.dumps(["Python", "Transformers", "GitHub Actions"]),
        "status": "Completed",
        "github_url": "https://github.com/sindhu-viplav/code-reviewer",
        "live_demo_url": ""
    },

    # Vaishnavi
    {
        "student_id": "STU_2024_017",
        "title": "VisionGuard",
        "category": "Computer Vision / Edge AI",
        "description": "Real-Time Campus Edge Surveillance & Anomaly Detection system with sub-15ms inference.",
        "role": "Lead Architect",
        "technologies": json.dumps(["Python", "OpenCV", "YOLOv8", "PyTorch", "FastAPI"]),
        "status": "Active",
        "github_url": "https://github.com/vaishnavi-ai/visionguard",
        "live_demo_url": "https://visionguard.demo.ai"
    },
    {
        "student_id": "STU_2024_017",
        "title": "Autonomous Drone Navigator",
        "category": "Robotics & AI",
        "description": "Visual SLAM and Obstacle Avoidance Simulation for indoor GPS-denied environments.",
        "role": "Developer",
        "technologies": json.dumps(["ROS2", "C++", "Python", "Gazebo"]),
        "status": "Completed",
        "github_url": "https://github.com/vaishnavi-ai/drone-slam",
        "live_demo_url": ""
    },
    {
        "student_id": "STU_2024_017",
        "title": "MediScan AI",
        "category": "Healthcare AI",
        "description": "Automated Dermatological Lesion Classifier using quantized MobileNet for mobile clinics.",
        "role": "Developer",
        "technologies": json.dumps(["TensorFlow Lite", "React", "Flask"]),
        "status": "Completed",
        "github_url": "https://github.com/vaishnavi-ai/mediscan",
        "live_demo_url": ""
    },

    # Satyajit
    {
        "student_id": "STU_2024_018",
        "title": "DataPulse",
        "category": "Big Data / AI",
        "description": "Distributed Streaming Predictive Analytics Engine processing millions of campus IoT events.",
        "role": "Lead Engineer",
        "technologies": json.dumps(["Apache Kafka", "Spark", "FastAPI", "React"]),
        "status": "Active",
        "github_url": "https://github.com/satyajit-ds/datapulse",
        "live_demo_url": "https://datapulse.demo.ai"
    },
    {
        "student_id": "STU_2024_018",
        "title": "Campus Transit Optimizer",
        "category": "Predictive Analytics",
        "description": "Real-Time Shuttle Dispatch Prediction Algorithm reducing passenger wait times by 28%.",
        "role": "Developer",
        "technologies": json.dumps(["Python", "XGBoost", "PostgreSQL", "PostGIS"]),
        "status": "Completed",
        "github_url": "https://github.com/satyajit-ds/transit-opt",
        "live_demo_url": ""
    },
    {
        "student_id": "STU_2024_018",
        "title": "Algorithmic Trading Backtester",
        "category": "FinTech",
        "description": "Quantitative Sentiment & Historical Price Analysis platform for algorithmic portfolio balancing.",
        "role": "Developer",
        "technologies": json.dumps(["Python", "Pandas", "FastAPI", "ChartJS"]),
        "status": "Completed",
        "github_url": "https://github.com/satyajit-ds/quant-backtest",
        "live_demo_url": ""
    }
]

new_certs = [
    # Sindhu
    {"student_id": "STU_2024_016", "name": "Natural Language Processing Specialization", "issuer": "DeepLearning.AI / Coursera", "issue_date": "2025-02-15", "credential_id": "NLP_DL_2025", "credential_url": "https://coursera.org", "skills": json.dumps(["NLP", "Transformers", "Deep Learning"])},
    {"student_id": "STU_2024_016", "name": "AWS Certified Machine Learning - Specialty", "issuer": "AWS", "issue_date": "2025-06-20", "credential_id": "AWS_MLS_789", "credential_url": "https://aws.amazon.com", "skills": json.dumps(["AWS", "Cloud ML"])},
    {"student_id": "STU_2024_016", "name": "Fundamentals of Deep Learning", "issuer": "NVIDIA Deep Learning Institute", "issue_date": "2025-09-10", "credential_id": "NV_DLI_442", "credential_url": "https://nvidia.com", "skills": json.dumps(["CUDA", "PyTorch"])},

    # Vaishnavi
    {"student_id": "STU_2024_017", "name": "OpenCV Computer Vision Specialist", "issuer": "OpenCV University", "issue_date": "2025-03-12", "credential_id": "OCV_CV_910", "credential_url": "https://opencv.org", "skills": json.dumps(["OpenCV", "Computer Vision"])},
    {"student_id": "STU_2024_017", "name": "Professional Machine Learning Engineer", "issuer": "Google Cloud", "issue_date": "2025-07-18", "credential_id": "GCP_ML_551", "credential_url": "https://cloud.google.com", "skills": json.dumps(["GCP", "Vertex AI", "MLOps"])},
    {"student_id": "STU_2024_017", "name": "TensorFlow Developer Professional Certificate", "issuer": "DeepLearning.AI / Coursera", "issue_date": "2025-09-05", "credential_id": "TF_DEV_882", "credential_url": "https://coursera.org", "skills": json.dumps(["TensorFlow", "Deep Learning"])},

    # Satyajit
    {"student_id": "STU_2024_018", "name": "Certified Associate Developer for Apache Spark", "issuer": "Databricks", "issue_date": "2025-04-10", "credential_id": "DB_SPARK_311", "credential_url": "https://databricks.com", "skills": json.dumps(["Apache Spark", "Big Data", "Python"])},
    {"student_id": "STU_2024_018", "name": "Azure Data Scientist Associate", "issuer": "Microsoft", "issue_date": "2025-08-14", "credential_id": "AZ_DS_100", "credential_url": "https://microsoft.com", "skills": json.dumps(["Azure", "Data Science", "MLOps"])},
    {"student_id": "STU_2024_018", "name": "IBM Data Science Professional Certificate", "issuer": "IBM / Coursera", "issue_date": "2025-10-02", "credential_id": "IBM_DS_774", "credential_url": "https://coursera.org", "skills": json.dumps(["Data Science", "Python", "SQL"])}
]

new_exp = [
    # Sindhu
    {"student_id": "STU_2024_016", "organization": "IndoGen AI Labs", "role": "AI Research Intern", "experience_type": "Internship", "start_date": "Jun 2026", "end_date": "Aug 2026", "responsibilities": "Designed and benchmarked parameter-efficient LoRA adapters for domain-specific LLM fine-tuning.", "technologies": json.dumps(["Python", "PyTorch", "LoRA", "Hugging Face"])},

    # Vaishnavi
    {"student_id": "STU_2024_017", "organization": "Apex Robotics Systems", "role": "Computer Vision Engineering Intern", "experience_type": "Internship", "start_date": "Jun 2026", "end_date": "Aug 2026", "responsibilities": "Deployed real-time inference pipelines on NVIDIA Jetson Orin edge nodes.", "technologies": json.dumps(["Python", "OpenCV", "TensorRT", "Jetson Orin"])},

    # Satyajit
    {"student_id": "STU_2024_018", "organization": "CognitiveScale Analytics", "role": "Data Science Intern", "experience_type": "Internship", "start_date": "Jun 2026", "end_date": "Aug 2026", "responsibilities": "Engineered distributed ETL pipelines and implemented customer churn prediction models.", "technologies": json.dumps(["Python", "Apache Spark", "Scikit-Learn", "PostgreSQL"])}
]

new_achieve = [
    # Sindhu
    {"student_id": "STU_2024_016", "title": "1st Place - Smart India AI Ideathon 2025", "category": "Competition", "date": "2025-11-15", "organization": "Ministry of Education"},
    {"student_id": "STU_2024_016", "title": "Dean's List for Academic Merit (Top 3% Cohort)", "category": "Academic", "date": "2026-05-20", "organization": "IcfaiTech"},

    # Vaishnavi
    {"student_id": "STU_2024_017", "title": "Winner - Inter-College Computer Vision Challenge 2025", "category": "Competition", "date": "2025-10-22", "organization": "IEEE Computer Society"},
    {"student_id": "STU_2024_017", "title": "Second Runner-up - Intel Edge AI Hackathon", "category": "Competition", "date": "2026-03-14", "organization": "Intel Innovators"},

    # Satyajit
    {"student_id": "STU_2024_018", "title": "1st Place - National Data Science League 2025", "category": "Competition", "date": "2025-12-05", "organization": "Analytics India Magazine"},
    {"student_id": "STU_2024_018", "title": "Best Technical Paper Presentation", "category": "Academic", "date": "2026-04-18", "organization": "IEEE Student Symposium"}
]

new_activities = [
    # Sindhu
    {"student_id": "STU_2024_016", "organization": "Women in AI & Tech Student Chapter", "role": "President", "description": "Organized campus-wide AI hackathons and technical mentorship workshops."},

    # Vaishnavi
    {"student_id": "STU_2024_017", "organization": "Robotics & Automation Club", "role": "Vice President", "description": "Mentored junior students in autonomous robotics and edge computing."},

    # Satyajit
    {"student_id": "STU_2024_018", "organization": "ACM Student Chapter", "role": "Treasurer", "description": "Managed chapter finances and organized competitive programming bootcamps."}
]

new_careers = [
    # Sindhu
    {"student_id": "STU_2024_016", "target_role": "NLP Research Engineer", "target_industry": "Generative AI / Research & Development", "career_interests": json.dumps(["LLM Alignment", "Multimodal Transformers", "Retrieval-Augmented Generation", "Agentic Workflows"]), "career_readiness_pct": 86},

    # Vaishnavi
    {"student_id": "STU_2024_017", "target_role": "Computer Vision Engineer", "target_industry": "Autonomous Mobility & Robotics", "career_interests": json.dumps(["Edge Inference", "Visual SLAM", "Autonomous Navigation", "Medical Image Analysis"]), "career_readiness_pct": 82},

    # Satyajit
    {"student_id": "STU_2024_018", "target_role": "Machine Learning / Data Platform Engineer", "target_industry": "FinTech / Enterprise Data Intelligence", "career_interests": json.dumps(["Distributed Computing", "MLOps", "Predictive Analytics", "Large-Scale Feature Stores"]), "career_readiness_pct": 80}
]

new_tasks = [
    # Sindhu
    {"student_id": "STU_2024_016", "title": "AI301 Deep Learning Research Term Paper", "course": "AI301", "due_date": "Oct 04", "priority": "urgent"},
    {"student_id": "STU_2024_016", "title": "NLP Transformer Attention Mechanism Assignment", "course": "AI302", "due_date": "Oct 07", "priority": "due_soon"},
    {"student_id": "STU_2024_016", "title": "Knowledge Graphs Mini-Project Presentation", "course": "AI302", "due_date": "Oct 11", "priority": "upcoming"},

    # Vaishnavi
    {"student_id": "STU_2024_017", "title": "Computer Vision Edge Inference Lab Submission", "course": "AI303", "due_date": "Oct 03", "priority": "urgent"},
    {"student_id": "STU_2024_017", "title": "Data Structures Tree Traversal Quiz", "course": "CS201", "due_date": "Oct 06", "priority": "due_soon"},
    {"student_id": "STU_2024_017", "title": "Deep Learning CNN Architecture Implementation", "course": "AI301", "due_date": "Oct 09", "priority": "upcoming"},

    # Satyajit
    {"student_id": "STU_2024_018", "title": "Machine Learning Model Performance Analysis", "course": "AI303", "due_date": "Oct 04", "priority": "urgent"},
    {"student_id": "STU_2024_018", "title": "Discrete Mathematics Graph Theory Assignment", "course": "MATH202", "due_date": "Oct 08", "priority": "due_soon"},
    {"student_id": "STU_2024_018", "title": "Database Query Optimization & Indexing Lab", "course": "CS201", "due_date": "Oct 12", "priority": "upcoming"}
]

# Update seed_data.json
def update_list(key, new_items, id_key="id"):
    existing = {item.get(id_key): item for item in data.get(key, [])}
    for item in new_items:
        existing[item.get(id_key)] = item
    data[key] = list(existing.values())

# Update users and profiles by their ID
for u in new_users:
    idx = next((i for i, x in enumerate(data.get("users", [])) if x["id"] == u["id"]), None)
    if idx is not None:
        data["users"][idx] = u
    else:
        data.setdefault("users", []).append(u)

for p in new_profiles:
    idx = next((i for i, x in enumerate(data.get("student_profiles", [])) if x["student_id"] == p["student_id"]), None)
    if idx is not None:
        data["student_profiles"][idx] = p
    else:
        data.setdefault("student_profiles", []).append(p)

for c in new_careers:
    idx = next((i for i, x in enumerate(data.get("career_profiles", [])) if x["student_id"] == c["student_id"]), None)
    if idx is not None:
        data["career_profiles"][idx] = c
    else:
        data.setdefault("career_profiles", []).append(c)

# For multiple-per-student items, filter out existing for these students and append
new_student_ids = {"STU_2024_016", "STU_2024_017", "STU_2024_018"}

data["exam_results"] = [x for x in data.get("exam_results", []) if x.get("student_id") not in new_student_ids] + new_exams
data["skills"] = [x for x in data.get("skills", []) if x.get("student_id") not in new_student_ids] + new_skills
data["projects"] = [x for x in data.get("projects", []) if x.get("student_id") not in new_student_ids] + new_projects
data["certifications"] = [x for x in data.get("certifications", []) if x.get("student_id") not in new_student_ids] + new_certs
data["experiences"] = [x for x in data.get("experiences", []) if x.get("student_id") not in new_student_ids] + new_exp
data["achievements"] = [x for x in data.get("achievements", []) if x.get("student_id") not in new_student_ids] + new_achieve
data["activities"] = [x for x in data.get("activities", []) if x.get("student_id") not in new_student_ids] + new_activities
data["upcoming_tasks"] = [x for x in data.get("upcoming_tasks", []) if x.get("student_id") not in new_student_ids] + new_tasks

with open(seed_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
print("Updated seed_data.json successfully!")

# Now directly seed SQLite campusmind.db
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. portal_user_accounts
for u in new_users:
    cur.execute("""
        INSERT INTO portal_user_accounts (id, role, email, password_hash, full_name, profile_photo_url, department, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ON CONFLICT(id) DO UPDATE SET
            role=excluded.role,
            email=excluded.email,
            password_hash=excluded.password_hash,
            full_name=excluded.full_name,
            profile_photo_url=excluded.profile_photo_url,
            department=excluded.department
    """, (u["id"], u["role"], u["email"], u["password_hash"], u["full_name"], u["profile_photo_url"], u["department"]))

# 2. portal_student_profiles
for p in new_profiles:
    cur.execute("""
        INSERT INTO portal_student_profiles (student_id, roll_number, program, current_semester, batch_year, overall_attendance_pct, bio, location, academic_status, links)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(student_id) DO UPDATE SET
            roll_number=excluded.roll_number,
            program=excluded.program,
            current_semester=excluded.current_semester,
            batch_year=excluded.batch_year,
            overall_attendance_pct=excluded.overall_attendance_pct,
            bio=excluded.bio,
            location=excluded.location,
            academic_status=excluded.academic_status,
            links=excluded.links
    """, (p["student_id"], p["roll_number"], p["program"], p["current_semester"], p["batch_year"], p["overall_attendance_pct"], p["bio"], p["location"], p["academic_status"], p["links"]))

# 3. Clean and insert multi-row tables for new students
for sid in new_student_ids:
    cur.execute("DELETE FROM portal_exam_results WHERE student_id = ?", (sid,))
    cur.execute("DELETE FROM portal_student_skills WHERE student_id = ?", (sid,))
    cur.execute("DELETE FROM portal_student_projects WHERE student_id = ?", (sid,))
    cur.execute("DELETE FROM portal_student_certifications WHERE student_id = ?", (sid,))
    cur.execute("DELETE FROM portal_student_experiences WHERE student_id = ?", (sid,))
    cur.execute("DELETE FROM portal_student_achievements WHERE student_id = ?", (sid,))
    cur.execute("DELETE FROM portal_student_activities WHERE student_id = ?", (sid,))
    cur.execute("DELETE FROM portal_student_career_profiles WHERE student_id = ?", (sid,))
    cur.execute("DELETE FROM portal_upcoming_tasks WHERE student_id = ?", (sid,))

for e in new_exams:
    cur.execute("""
        INSERT INTO portal_exam_results (student_id, exam_type, course_code, course_name, marks_obtained, max_marks, grade, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (e["student_id"], e["exam_type"], e["course_code"], e["course_name"], e["marks_obtained"], e["max_marks"], e["grade"], e["status"]))

for s in new_skills:
    cur.execute("""
        INSERT INTO portal_student_skills (student_id, name, category, proficiency_pct, verified)
        VALUES (?, ?, ?, ?, ?)
    """, (s["student_id"], s["name"], s["category"], s["proficiency_pct"], 1 if s["verified"] else 0))

for p in new_projects:
    cur.execute("""
        INSERT INTO portal_student_projects (student_id, title, category, description, role, technologies, status, github_url, live_demo_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (p["student_id"], p["title"], p["category"], p["description"], p["role"], p["technologies"], p["status"], p["github_url"], p["live_demo_url"]))

for c in new_certs:
    cur.execute("""
        INSERT INTO portal_student_certifications (student_id, name, issuer, issue_date, credential_id, credential_url, skills)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (c["student_id"], c["name"], c["issuer"], c["issue_date"], c["credential_id"], c["credential_url"], c["skills"]))

for exp in new_exp:
    cur.execute("""
        INSERT INTO portal_student_experiences (student_id, organization, role, experience_type, start_date, end_date, responsibilities, technologies)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (exp["student_id"], exp["organization"], exp["role"], exp["experience_type"], exp["start_date"], exp["end_date"], exp["responsibilities"], exp["technologies"]))

for a in new_achieve:
    cur.execute("""
        INSERT INTO portal_student_achievements (student_id, title, category, date, organization)
        VALUES (?, ?, ?, ?, ?)
    """, (a["student_id"], a["title"], a["category"], a["date"], a["organization"]))

for act in new_activities:
    cur.execute("""
        INSERT INTO portal_student_activities (student_id, organization, role, description)
        VALUES (?, ?, ?, ?)
    """, (act["student_id"], act["organization"], act["role"], act["description"]))

for cp in new_careers:
    cur.execute("""
        INSERT INTO portal_student_career_profiles (student_id, target_role, target_industry, career_interests, career_readiness_pct)
        VALUES (?, ?, ?, ?, ?)
    """, (cp["student_id"], cp["target_role"], cp["target_industry"], cp["career_interests"], cp["career_readiness_pct"]))

for t in new_tasks:
    cur.execute("""
        INSERT INTO portal_upcoming_tasks (student_id, title, course, due_date, priority)
        VALUES (?, ?, ?, ?, ?)
    """, (t["student_id"], t["title"], t["course"], t["due_date"], t["priority"]))

# 4. Also seed core 'students' table for AI Chatbot and StudentRepository grounding
student_table_records = [
    # Sandeep (in case missing from students table)
    ("24AI015", "Gadde Sandeep", "student.ai@campus.edu", "+91 9876543210", "Artificial Intelligence", 3, 5, "AI301: Deep Learning, CS201: Data Structures, MATH202: Discrete Math, AI302: Knowledge Representation, AI303: Applied Statistics", 9.6, 3.85, 88.5, 0, "Paid"),
    ("STU_2024_015", "Gadde Sandeep", "student.ai@campus.edu", "+91 9876543210", "Artificial Intelligence", 3, 5, "AI301: Deep Learning, CS201: Data Structures, MATH202: Discrete Math, AI302: Knowledge Representation, AI303: Applied Statistics", 9.6, 3.85, 88.5, 0, "Paid"),
    # Sindhu
    ("24AI016", "Sindhu Viplav", "sindhu.viplav@campus.edu", "+91 9876543221", "Artificial Intelligence", 3, 5, "AI301: Deep Learning, CS201: Data Structures, MATH202: Discrete Math, AI302: Knowledge Representation, AI303: Applied Statistics", 9.8, 3.92, 93.5, 0, "Paid"),
    ("STU_2024_016", "Sindhu Viplav", "sindhu.viplav@campus.edu", "+91 9876543221", "Artificial Intelligence", 3, 5, "AI301: Deep Learning, CS201: Data Structures, MATH202: Discrete Math, AI302: Knowledge Representation, AI303: Applied Statistics", 9.8, 3.92, 93.5, 0, "Paid"),
    # Vaishnavi
    ("24AI017", "Vaishnavi", "vaishnavi@campus.edu", "+91 9876543222", "Artificial Intelligence", 3, 5, "AI301: Deep Learning, CS201: Data Structures, MATH202: Discrete Math, AI302: Knowledge Representation, AI303: Applied Statistics", 9.7, 3.88, 91.0, 0, "Paid"),
    ("STU_2024_017", "Vaishnavi", "vaishnavi@campus.edu", "+91 9876543222", "Artificial Intelligence", 3, 5, "AI301: Deep Learning, CS201: Data Structures, MATH202: Discrete Math, AI302: Knowledge Representation, AI303: Applied Statistics", 9.7, 3.88, 91.0, 0, "Paid"),
    # Satyajit
    ("24AI018", "Satyajit", "satyajit@campus.edu", "+91 9876543223", "Artificial Intelligence", 3, 5, "AI301: Deep Learning, CS201: Data Structures, MATH202: Discrete Math, AI302: Knowledge Representation, AI303: Applied Statistics", 9.5, 3.82, 87.5, 0, "Paid"),
    ("STU_2024_018", "Satyajit", "satyajit@campus.edu", "+91 9876543223", "Artificial Intelligence", 3, 5, "AI301: Deep Learning, CS201: Data Structures, MATH202: Discrete Math, AI302: Knowledge Representation, AI303: Applied Statistics", 9.5, 3.82, 87.5, 0, "Paid")
]

for rec in student_table_records:
    cur.execute("""
        INSERT INTO students (enrollment_no, name, email, mobile_no, branch, year, semester, courses_enrolled, sgpa, cgpa, attendance_pct, backlogs, fee_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(enrollment_no) DO UPDATE SET
            name=excluded.name,
            email=excluded.email,
            mobile_no=excluded.mobile_no,
            branch=excluded.branch,
            year=excluded.year,
            semester=excluded.semester,
            courses_enrolled=excluded.courses_enrolled,
            sgpa=excluded.sgpa,
            cgpa=excluded.cgpa,
            attendance_pct=excluded.attendance_pct,
            backlogs=excluded.backlogs,
            fee_status=excluded.fee_status
    """, rec)

conn.commit()
conn.close()
print("All 3 new students seeded successfully into SQLite campusmind.db!")
