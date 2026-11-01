import os
import sys

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import UserAccount
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(backend_dir, 'campusmind.db')}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def seed_users():
    session = SessionLocal()
    try:
        # Create tables if not exist
        UserAccount.__table__.create(engine, checkfirst=True)

        users_to_seed = [
            {
                "id": "STU_2024_015",
                "email": "student.ai@campus.edu",
                "role": "student",
                "full_name": "Gadde Sandeep",
                "department": "Artificial Intelligence",
                "password_hash": pwd_context.hash("password123")
            },
            {
                "id": "STU_2024_016",
                "email": "sindhu.viplav@campus.edu",
                "role": "student",
                "full_name": "Sindhu Viplav",
                "department": "Artificial Intelligence",
                "password_hash": pwd_context.hash("password123")
            },
            {
                "id": "STU_2024_017",
                "email": "vaishnavi@campus.edu",
                "role": "student",
                "full_name": "Vaishnavi",
                "department": "Artificial Intelligence",
                "password_hash": pwd_context.hash("password123")
            },
            {
                "id": "STU_2024_018",
                "email": "satyajit@campus.edu",
                "role": "student",
                "full_name": "Satyajit",
                "department": "Artificial Intelligence",
                "password_hash": pwd_context.hash("password123")
            },
            {
                "id": "FAC_DEMO_01",
                "email": "faculty@college.edu",
                "role": "faculty",
                "full_name": "Dr. Demo Faculty",
                "department": "Computer Science and Engineering",
                "password_hash": pwd_context.hash("password123")
            },
            {
                "id": "student1",
                "email": "student1@ifheindia.edu",
                "role": "student",
                "full_name": "Aarav Rao",
                "department": "CSE",
                "password_hash": pwd_context.hash("password123")
            },
            {
                "id": "faculty1",
                "email": "faculty1@ifheindia.edu",
                "role": "faculty",
                "full_name": "Dr. Alan Turing",
                "department": "CSE",
                "password_hash": pwd_context.hash("password123")
            },
            {
                "id": "admin1",
                "email": "admin1@ifheindia.edu",
                "role": "admin",
                "full_name": "System Administrator",
                "department": "Administration",
                "password_hash": pwd_context.hash("password123")
            }
        ]

        for user_data in users_to_seed:
            existing_user = session.query(UserAccount).filter_by(id=user_data["id"]).first()
            if existing_user:
                for key, value in user_data.items():
                    setattr(existing_user, key, value)
            else:
                new_user = UserAccount(**user_data)
                session.add(new_user)

        session.commit()
        print("Successfully seeded demo accounts with standard bcrypt hashes.")
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_users()
