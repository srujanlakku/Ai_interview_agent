"""
Persistent storage for interview history using SQLite.
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import os
from pathlib import Path


class InterviewHistoryDB:
    """
    SQLite database for storing interview history.
    Stores completed interviews with scores and feedback.
    """
    
    def __init__(self, db_path: str = "interview_history.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create interviews table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE,
                candidate_name TEXT NOT NULL,
                role TEXT NOT NULL,
                experience_level TEXT NOT NULL,
                company TEXT,
                final_score REAL,
                total_questions INTEGER,
                strengths TEXT,
                weaknesses TEXT,
                started_at TIMESTAMP,
                ended_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create questions table (for detailed tracking)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interview_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interview_id INTEGER,
                question_text TEXT,
                question_type TEXT,
                topic TEXT,
                answer TEXT,
                score REAL,
                feedback TEXT,
                strengths TEXT,
                improvements TEXT,
                FOREIGN KEY (interview_id) REFERENCES interviews (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_interview(self, session_data: Dict[str, Any]) -> int:
        """
        Save a completed interview session to the database.
        
        Args:
            session_data: Complete session data from orchestrator
            
        Returns:
            ID of the saved interview
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert main interview record
        cursor.execute("""
            INSERT INTO interviews (
                session_id, candidate_name, role, experience_level, 
                company, final_score, total_questions, 
                strengths, weaknesses, started_at, ended_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_data.get("session_id"),
            session_data.get("candidate_name"),
            session_data.get("role"),
            session_data.get("experience_level"),
            session_data.get("company"),
            session_data.get("average_score"),
            session_data.get("current_question_num"),
            json.dumps(session_data.get("strengths", [])),
            json.dumps(session_data.get("weaknesses", [])),
            session_data.get("started_at"),
            session_data.get("ended_at")
        ))
        
        interview_id = cursor.lastrowid
        
        # Insert question details if available
        if "detailed_coverage" in session_data:
            history = session_data.get("detailed_coverage", {}).get("history", [])
            for item in history:
                cursor.execute("""
                    INSERT INTO interview_questions (
                        interview_id, question_text, question_type, topic,
                        answer, score, feedback, strengths, improvements
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    interview_id,
                    item.get("question"),
                    item.get("type"),
                    item.get("topic"),
                    item.get("answer"),
                    item.get("score"),
                    item.get("feedback"),
                    json.dumps(item.get("strengths", [])),
                    json.dumps(item.get("improvements", []))
                ))
        
        conn.commit()
        conn.close()
        
        return interview_id
    
    def get_all_interviews(self) -> List[Dict[str, Any]]:
        """Get all stored interviews with basic info."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, session_id, candidate_name, role, experience_level,
                   company, final_score, total_questions, created_at
            FROM interviews
            ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        interviews = []
        for row in rows:
            interview = dict(zip(columns, row))
            interviews.append(interview)
        
        conn.close()
        return interviews
    
    def get_interview_by_id(self, interview_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed interview information by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get main interview data
        cursor.execute("""
            SELECT * FROM interviews WHERE id = ?
        """, (interview_id,))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        
        columns = [description[0] for description in cursor.description]
        interview = dict(zip(columns, row))
        
        # Parse JSON fields
        interview["strengths"] = json.loads(interview.get("strengths", "[]"))
        interview["weaknesses"] = json.loads(interview.get("weaknesses", "[]"))
        
        # Get detailed questions
        cursor.execute("""
            SELECT * FROM interview_questions WHERE interview_id = ?
        """, (interview_id,))
        
        question_rows = cursor.fetchall()
        question_columns = [description[0] for description in cursor.description]
        
        questions = []
        for q_row in question_rows:
            question = dict(zip(question_columns, q_row))
            question["strengths"] = json.loads(question.get("strengths", "[]"))
            question["improvements"] = json.loads(question.get("improvements", "[]"))
            questions.append(question)
        
        interview["questions"] = questions
        conn.close()
        
        return interview
    
    def get_interviews_by_candidate(self, candidate_name: str) -> List[Dict[str, Any]]:
        """Get all interviews for a specific candidate."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM interviews WHERE candidate_name = ?
            ORDER BY created_at DESC
        """, (candidate_name,))
        
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        interviews = []
        for row in rows:
            interview = dict(zip(columns, row))
            interview["strengths"] = json.loads(interview.get("strengths", "[]"))
            interview["weaknesses"] = json.loads(interview.get("weaknesses", "[]"))
            interviews.append(interview)
        
        conn.close()
        return interviews
    
    def get_interviews_by_role(self, role: str) -> List[Dict[str, Any]]:
        """Get all interviews for a specific role."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM interviews WHERE role = ?
            ORDER BY created_at DESC
        """, (role,))
        
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        interviews = []
        for row in rows:
            interview = dict(zip(columns, row))
            interview["strengths"] = json.loads(interview.get("strengths", "[]"))
            interview["weaknesses"] = json.loads(interview.get("weaknesses", "[]"))
            interviews.append(interview)
        
        conn.close()
        return interviews
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get overall performance statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total interviews
        cursor.execute("SELECT COUNT(*) FROM interviews")
        total_interviews = cursor.fetchone()[0]
        
        # Average score
        cursor.execute("SELECT AVG(final_score) FROM interviews WHERE final_score IS NOT NULL")
        avg_score = cursor.fetchone()[0]
        
        # By role
        cursor.execute("""
            SELECT role, COUNT(*), AVG(final_score)
            FROM interviews
            GROUP BY role
        """)
        role_stats = cursor.fetchall()
        
        # By experience level
        cursor.execute("""
            SELECT experience_level, COUNT(*), AVG(final_score)
            FROM interviews
            GROUP BY experience_level
        """)
        exp_stats = cursor.fetchall()
        
        conn.close()
        
        return {
            "total_interviews": total_interviews,
            "average_score": round(avg_score, 2) if avg_score else 0.0,
            "by_role": [{"role": r[0], "count": r[1], "avg_score": round(r[2], 2)} for r in role_stats],
            "by_experience": [{"level": e[0], "count": e[1], "avg_score": round(e[2], 2)} for e in exp_stats]
        }


# Singleton instance
_history_db: Optional[InterviewHistoryDB] = None


def get_history_db() -> InterviewHistoryDB:
    """Get singleton history database instance."""
    global _history_db
    if _history_db is None:
        # Use a database file in the backend directory
        db_path = os.path.join(os.path.dirname(__file__), "..", "..", "interview_history.db")
        _history_db = InterviewHistoryDB(db_path=db_path)
    return _history_db
