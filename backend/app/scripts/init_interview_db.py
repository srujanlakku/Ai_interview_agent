"""
Initialize interview database with seed data
Run this to populate companies, roles, rounds, and questions
"""

import sys
from pathlib import Path
import os

# Add backend directory to path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

os.environ.setdefault('DATABASE_URL', 'sqlite:///./interview_pilot.db')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import uuid

# Use raw SQL to create tables and avoid ORM complications
def init_interview_database():
    """Initialize interview intelligence database with seed data"""
    
    from app.config import Settings
    settings = Settings()
    
    # Create engine
    engine = create_engine(settings.DATABASE_URL, echo=False)
    
    # Create tables using raw SQL
    with engine.connect() as conn:
        conn.execute(text('''CREATE TABLE IF NOT EXISTS role (
            id VARCHAR PRIMARY KEY,
            name VARCHAR UNIQUE NOT NULL,
            description TEXT,
            level VARCHAR,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )'''))
        
        conn.execute(text('''CREATE TABLE IF NOT EXISTS interview_round (
            id VARCHAR PRIMARY KEY,
            name VARCHAR UNIQUE NOT NULL,
            description TEXT,
            "order" INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )'''))
        
        conn.execute(text('''CREATE TABLE IF NOT EXISTS company (
            id VARCHAR PRIMARY KEY,
            name VARCHAR UNIQUE NOT NULL,
            industry_type VARCHAR NOT NULL,
            company_type VARCHAR NOT NULL,
            description TEXT,
            headquarters VARCHAR,
            india_office_locations VARCHAR,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )'''))
        
        conn.execute(text('''CREATE TABLE IF NOT EXISTS company_role_association (
            company_id VARCHAR NOT NULL,
            role_id VARCHAR NOT NULL,
            PRIMARY KEY (company_id, role_id),
            FOREIGN KEY (company_id) REFERENCES company(id),
            FOREIGN KEY (role_id) REFERENCES role(id)
        )'''))
        
        conn.execute(text('''CREATE TABLE IF NOT EXISTS interview_question (
            id VARCHAR PRIMARY KEY,
            company_id VARCHAR,
            role_id VARCHAR,
            round_id VARCHAR,
            question_text TEXT NOT NULL,
            category VARCHAR,
            difficulty VARCHAR NOT NULL,
            topics VARCHAR,
            frequency_score INTEGER DEFAULT 1,
            is_repeated INTEGER DEFAULT 1,
            answer_guidelines TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES company(id),
            FOREIGN KEY (role_id) REFERENCES role(id),
            FOREIGN KEY (round_id) REFERENCES interview_round(id)
        )'''))
        
        conn.commit()
    
    print("✓ Database tables created")
    
    # Now populate with seed data
    from app.data.interview_seed_data import (
        COMPANIES_DATA, ROLES_DATA, INTERVIEW_ROUNDS_DATA, INTERVIEW_QUESTIONS_DATA
    )
    
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        # Check if data already exists
        result = db.execute(text('SELECT COUNT(*) FROM company')).scalar()
        if result > 0:
            print("✓ Interview database already initialized")
            db.close()
            return
        
        print("🔄 Initializing interview intelligence database...")
        
        # Create Roles
        print("\n📝 Creating roles...")
        for role_data in ROLES_DATA:
            db.execute(text('''INSERT INTO role (id, name, description, level) 
                          VALUES (:id, :name, :description, :level)'''),
                      {"id": role_data["id"], "name": role_data["name"], "description": role_data.get("description"), "level": role_data.get("level")})
        db.commit()
        print(f"✓ Created {len(ROLES_DATA)} roles")
        
        # Create Interview Rounds
        print("\n📝 Creating interview rounds...")
        for round_data in INTERVIEW_ROUNDS_DATA:
            db.execute(text('''INSERT INTO interview_round (id, name, description, "order") 
                          VALUES (:id, :name, :description, :order)'''),
                      {"id": round_data["id"], "name": round_data["name"], "description": round_data.get("description"), "order": round_data.get("order")})
        db.commit()
        print(f"✓ Created {len(INTERVIEW_ROUNDS_DATA)} interview rounds")
        
        # Create Companies
        print("\n📝 Creating companies...")
        for company_data in COMPANIES_DATA:
            db.execute(text('''INSERT INTO company (id, name, industry_type, company_type, description, headquarters, india_office_locations) 
                          VALUES (:id, :name, :industry_type, :company_type, :description, :headquarters, :india_office_locations)'''),
                      {"id": company_data["id"], "name": company_data["name"], "industry_type": company_data["industry_type"], "company_type": company_data["company_type"],
                       "description": company_data.get("description"), "headquarters": company_data.get("headquarters"), "india_office_locations": company_data.get("india_office_locations")})
        db.commit()
        print(f"✓ Created {len(COMPANIES_DATA)} companies")
        
        # Add role associations to companies
        print("\n📝 Adding role associations...")
        for company_data in COMPANIES_DATA:
            for role_data in ROLES_DATA:
                db.execute(text('''INSERT INTO company_role_association (company_id, role_id) 
                              VALUES (:company_id, :role_id)'''),
                          {"company_id": company_data["id"], "role_id": role_data["id"]})
        db.commit()
        print(f"✓ Added role associations")
        
        # Create Questions
        print("\n📝 Creating interview questions...")
        questions_created = 0
        for question_data in INTERVIEW_QUESTIONS_DATA:
            db.execute(text('''INSERT INTO interview_question (id, company_id, role_id, round_id, question_text, category, difficulty, topics, frequency_score, is_repeated, answer_guidelines) 
                          VALUES (:id, :company_id, :role_id, :round_id, :question_text, :category, :difficulty, :topics, :frequency_score, :is_repeated, :answer_guidelines)'''),
                      {"id": str(uuid.uuid4()), "company_id": question_data.get("company_id"), "role_id": question_data.get("role_id"), "round_id": question_data.get("round_id"),
                       "question_text": question_data["question_text"], "category": question_data.get("category"), "difficulty": question_data.get("difficulty"),
                       "topics": question_data.get("topics"), "frequency_score": question_data.get("frequency_score", 1), "is_repeated": 1 if question_data.get("is_repeated", True) else 0,
                       "answer_guidelines": question_data.get("answer_guidelines")})
            questions_created += 1
        db.commit()
        print(f"✓ Created {questions_created} interview questions")
        
        print("\n✅ Interview database initialized successfully!")
        print(f"\n📊 Summary:")
        print(f"   - Companies: {len(COMPANIES_DATA)}")
        print(f"   - Roles: {len(ROLES_DATA)}")
        print(f"   - Interview Rounds: {len(INTERVIEW_ROUNDS_DATA)}")
        print(f"   - Questions: {questions_created}")
        
        db.close()
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {str(e)}")
        import traceback
        traceback.print_exc()
        db.close()
        raise


if __name__ == "__main__":
    init_interview_database()
