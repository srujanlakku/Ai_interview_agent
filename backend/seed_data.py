
import os
import uuid
import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.utils.database import SessionLocal, engine
from app.models.interview_data import Company, Role, CompanyQuestion, InterviewRound
from app.models.database import Base

def seed_data():
    print("Seeding database with initial MNC data...")
    db = SessionLocal()
    try:
        # 1. Create Interview Rounds
        rounds = [
            {"id": str(uuid.uuid4()), "name": "Online Assessment", "description": "initial coding and aptitude test", "order": 1},
            {"id": str(uuid.uuid4()), "name": "Technical Interview 1", "description": "Focus on data structures and algorithms", "order": 2},
            {"id": str(uuid.uuid4()), "name": "Technical Interview 2", "description": "Focus on system design and core subjects", "order": 3},
            {"id": str(uuid.uuid4()), "name": "Managerial Round", "description": "Behavioral and project-based discussion", "order": 4},
            {"id": str(uuid.uuid4()), "name": "HR Round", "description": "Final behavioral and salary discussion", "order": 5}
        ]
        
        round_objs = []
        for r in rounds:
            existing = db.query(InterviewRound).filter(InterviewRound.name == r["name"]).first()
            if not existing:
                obj = InterviewRound(**r)
                db.add(obj)
                round_objs.append(obj)
            else:
                round_objs.append(existing)
        db.commit()

        # 2. Create Companies
        companies = [
            {
                "name": "Google", 
                "industry_type": "tech", 
                "company_type": "mnc", 
                "description": "Global leader in search, AI, and cloud.",
                "headquarters": "Mountain View, CA",
                "india_office_locations": "Bangalore, Hyderabad, Pune, Gurgaon"
            },
            {
                "name": "Microsoft", 
                "industry_type": "tech", 
                "company_type": "mnc", 
                "description": "Leader in software, services, and devices.",
                "headquarters": "Redmond, WA",
                "india_office_locations": "Bangalore, Hyderabad, Noida"
            },
            {
                "name": "Amazon", 
                "industry_type": "tech", 
                "company_type": "mnc", 
                "description": "Global e-commerce and cloud computing giant.",
                "headquarters": "Seattle, WA",
                "india_office_locations": "Bangalore, Hyderabad, Chennai, Delhi"
            },
            {
                "name": "TCS", 
                "industry_type": "it_services", 
                "company_type": "indian_it", 
                "description": "Tata Consultancy Services - Global IT leader.",
                "headquarters": "Mumbai, India",
                "india_office_locations": "Mumbai, Bangalore, Chennai, Hyderabad, Pune, Delhi"
            },
            {
                "name": "Infosys", 
                "industry_type": "it_services", 
                "company_type": "indian_it", 
                "description": "Next-generation digital services and consulting.",
                "headquarters": "Bangalore, India",
                "india_office_locations": "Bangalore, Pune, Hyderabad, Chennai, Mysore"
            },
            {
                "name": "Wipro", 
                "industry_type": "it_services", 
                "company_type": "indian_it", 
                "description": "Leading global IT, consulting and business process services.",
                "headquarters": "Bangalore, India",
                "india_office_locations": "Bangalore, Pune, Chennai, Kochi"
            },
            {
                "name": "PhonePe", 
                "industry_type": "fintech", 
                "company_type": "startup", 
                "description": "India's leading digital payments company.",
                "headquarters": "Bangalore, India",
                "india_office_locations": "Bangalore, Pune"
            },
            {
                "name": "Zomato", 
                "industry_type": "startup", 
                "company_type": "startup", 
                "description": "Food delivery and restaurant discovery platform.",
                "headquarters": "Gurgaon, India",
                "india_office_locations": "Gurgaon, Bangalore, Mumbai"
            }
        ]

        company_objs = {}
        for c in companies:
            existing = db.query(Company).filter(Company.name == c["name"]).first()
            if not existing:
                c_id = str(uuid.uuid4())
                obj = Company(id=c_id, **c)
                db.add(obj)
                company_objs[c["name"]] = obj
            else:
                company_objs[c["name"]] = existing
        db.commit()

        # 3. Create Roles
        roles = [
            {"name": "Software Engineer", "level": "Junior", "description": "Entry level engineering role"},
            {"name": "Senior Software Engineer", "level": "Senior", "description": "Experienced engineering role"},
            {"name": "Backend Developer", "level": "Mid", "description": "Server-side developer"},
            {"name": "Frontend Developer", "level": "Mid", "description": "UI/UX developer"},
            {"name": "Full Stack Developer", "level": "Mid", "description": "End-to-end developer"},
            {"name": "Data Scientist", "level": "Mid", "description": "Data analysis and ML role"},
            {"name": "DevOps Engineer", "level": "Mid", "description": "Infrastructure and automation role"}
        ]

        role_objs = {}
        for r in roles:
            existing = db.query(Role).filter(Role.name == r["name"], Role.level == r["level"]).first()
            if not existing:
                r_id = str(uuid.uuid4())
                obj = Role(id=r_id, **r)
                db.add(obj)
                role_objs[f"{r['name']}_{r['level']}"] = obj
            else:
                role_objs[f"{r['name']}_{r['level']}"] = existing
        db.commit()

        # 4. Link Roles to Companies
        for c_obj in company_objs.values():
            if not c_obj.roles:
                # Add most roles to each company for variety
                for r_obj in role_objs.values():
                    c_obj.roles.append(r_obj)
        db.commit()

        # 5. Create Questions
        example_questions = [
            {
                "question_text": "How do you handle large datasets in memory?",
                "category": "technical",
                "difficulty": "Medium",
                "topics": "Algorithms, Memory Management",
                "is_repeated": True,
                "frequency_score": 85,
                "answer_guidelines": "Discuss streaming, batching, and data structures like generators or iterators."
            },
            {
                "question_text": "Explain the difference between SQL and NoSQL databases.",
                "category": "technical",
                "difficulty": "Easy",
                "topics": "Databases",
                "is_repeated": True,
                "frequency_score": 95,
                "answer_guidelines": "Mention schema vs schemaless, scaling (vertical vs horizontal), and use cases."
            },
            {
                "question_text": "Write a function to find the first non-repeating character in a string.",
                "category": "technical",
                "difficulty": "Easy",
                "topics": "Coding, Strings",
                "is_repeated": True,
                "frequency_score": 75,
                "answer_guidelines": "Use a hash map or frequency array. Explain O(n) time complexity."
            },
            {
                "question_text": "Tell me about a time you had a conflict with a team member.",
                "category": "soft_skill",
                "difficulty": "Medium",
                "topics": "Behavioral, Leadership",
                "is_repeated": True,
                "frequency_score": 90,
                "answer_guidelines": "Use the STAR method. Focus on professional resolution and positive outcome."
            }
        ]

        for q in example_questions:
            existing = db.query(CompanyQuestion).filter(CompanyQuestion.question_text == q["question_text"]).first()
            if not existing:
                q_id = str(uuid.uuid4())
                obj = CompanyQuestion(id=q_id, **q)
                db.add(obj)
        db.commit()

        print("Successfully seeded database!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
