import requests

test_cases = [
    ("STU_2024_015", "password123"),
    ("sandeep", "password123"),
    ("STU_2024_016", "password123"),
    ("sindhu", "password123"),
    ("sindhu", "sindhu123"),
    ("sindhu.viplav@campus.edu", "password123"),
    ("STU_2024_017", "password123"),
    ("vaishnavi", "password123"),
    ("vaishnavi", "vaishnavi123"),
    ("STU_2024_018", "password123"),
    ("satyajit", "password123"),
    ("satyajit", "satyajit123"),
]

for ident, pw in test_cases:
    resp = requests.post("http://127.0.0.1:8000/api/auth/login", json={"identifier": ident, "password": pw})
    if resp.status_code == 200:
        data = resp.json()
        print(f"SUCCESS: {ident} (pw: {pw}) -> Name: {data.get('user', {}).get('name')}, Role: {data.get('user', {}).get('role')}")
    else:
        print(f"FAILED: {ident} -> {resp.status_code} {resp.text}")
