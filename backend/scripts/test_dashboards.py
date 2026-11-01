import requests

students = ["STU_2024_015", "STU_2024_016", "STU_2024_017", "STU_2024_018"]

for s in students:
    login_res = requests.post("http://127.0.0.1:8000/api/auth/login", json={"identifier": s, "password": "password123"}).json()
    token = login_res["access_token"]
    dash_res = requests.get("http://127.0.0.1:8000/api/portal/student/me/dashboard", headers={"Authorization": f"Bearer {token}"}).json()
    prof = dash_res.get("profile", {})
    metrics = dash_res.get("academic_metrics", {})
    projects = dash_res.get("projects", [])
    skills = dash_res.get("skills", [])
    print(f"=== {prof.get('full_name')} ({prof.get('roll_number')}) ===")
    print(f"  Attendance: {metrics.get('attendance', {}).get('overall')}%")
    print(f"  CGPA: {metrics.get('cgpa')}")
    print(f"  Rank: {metrics.get('class_rank')}")
    print(f"  Projects ({len(projects)}): {[p.get('title') for p in projects]}")
    print(f"  Top Skills: {[s.get('name') for s in skills[:4]]}")
