"""
Database migration utility for InterviewPilot
Adds missing columns to existing tables without requiring a full reset.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "backend", "interview_pilot.db")

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database file not found at {DB_PATH}. Skipping migration.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 1. Add agent_state to interviews table
        try:
            cursor.execute("ALTER TABLE interviews ADD COLUMN agent_state JSON")
            print("Added 'agent_state' column to 'interviews' table.")
        except sqlite3.OperationalError as e:
            if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                print("'agent_state' column already exists in 'interviews' table.")
            else:
                print(f"Error adding 'agent_state': {e}")

        # 2. Add columns to interview_session_questions table
        session_columns = [
            ("ideal_answer", "TEXT"),
            ("problem_statement", "TEXT"),
            ("expected_approach", "TEXT"),
            ("code_solution", "TEXT")
        ]

        for col_name, col_type in session_columns:
            try:
                cursor.execute(f"ALTER TABLE interview_session_questions ADD COLUMN {col_name} {col_type}")
                print(f"Added '{col_name}' column to 'interview_session_questions' table.")
            except sqlite3.OperationalError as e:
                if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                    print(f"'{col_name}' column already exists in 'interview_session_questions' table.")
                else:
                    print(f"Error adding '{col_name}' to session questions: {e}")

        # 3. Add columns to interview_question table (singular) for consistency
        research_columns = [
            ("answer_guidelines", "TEXT"),
            ("is_repeated", "BOOLEAN DEFAULT 1"),
            ("frequency_score", "INTEGER DEFAULT 1")
        ]

        for col_name, col_type in research_columns:
            try:
                cursor.execute(f"ALTER TABLE interview_question ADD COLUMN {col_name} {col_type}")
                print(f"Added '{col_name}' column to 'interview_question' table.")
            except sqlite3.OperationalError as e:
                if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                    print(f"'{col_name}' column already exists in 'interview_question' table.")
                else:
                    print(f"Error adding '{col_name}' to interview question: {e}")

        conn.commit()
        print("Migration completed successfully.")

    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
