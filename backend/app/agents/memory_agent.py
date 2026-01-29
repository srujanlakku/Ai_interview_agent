"""
Memory Agent for long-term knowledge storage and retrieval
"""
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.database import UserMemory
from app.utils.logging_config import get_logger
from datetime import datetime

logger = get_logger(__name__)


class MemoryAgent:
    """Agent for managing user memory and progress tracking"""

    def __init__(self):
        self.name = "MemoryAgent"

    def store_strength(self, db: Session, user_id: int, strength_area: str, 
                      score: float, metadata: Dict[str, Any] = None) -> None:
        """Store a strength area"""
        try:
            memory = UserMemory(
                user_id=user_id,
                memory_type="strength",
                content=strength_area,
                data={"score": score, **(metadata or {})}
            )
            db.add(memory)
            db.commit()
            logger.info(f"Strength stored for user {user_id}: {strength_area}")
        except Exception as e:
            logger.error(f"Failed to store strength: {str(e)}")

    def store_weakness(self, db: Session, user_id: int, weakness_area: str,
                      improvement_steps: List[str] = None, metadata: Dict[str, Any] = None) -> None:
        """Store a weakness area"""
        try:
            memory = UserMemory(
                user_id=user_id,
                memory_type="weakness",
                content=weakness_area,
                data={
                    "improvement_steps": improvement_steps or [],
                    **(metadata or {})
                }
            )
            db.add(memory)
            db.commit()
            logger.info(f"Weakness stored for user {user_id}: {weakness_area}")
        except Exception as e:
            logger.error(f"Failed to store weakness: {str(e)}")

    def store_covered_topic(self, db: Session, user_id: int, topic: str,
                           proficiency_level: str = "intermediate",
                           metadata: Dict[str, Any] = None) -> None:
        """Store a covered topic"""
        try:
            memory = UserMemory(
                user_id=user_id,
                memory_type="topic_covered",
                content=topic,
                data={
                    "proficiency": proficiency_level,
                    "timestamp": datetime.utcnow().isoformat(),
                    **(metadata or {})
                }
            )
            db.add(memory)
            db.commit()
            logger.info(f"Topic stored for user {user_id}: {topic}")
        except Exception as e:
            logger.error(f"Failed to store topic: {str(e)}")

    def store_missed_topic(self, db: Session, user_id: int, topic: str,
                          priority: str = "medium", metadata: Dict[str, Any] = None) -> None:
        """Store a missed/weak topic"""
        try:
            memory = UserMemory(
                user_id=user_id,
                memory_type="missed_topic",
                content=topic,
                data={
                    "priority": priority,
                    "timestamp": datetime.utcnow().isoformat(),
                    **(metadata or {})
                }
            )
            db.add(memory)
            db.commit()
            logger.info(f"Missed topic stored for user {user_id}: {topic}")
        except Exception as e:
            logger.error(f"Failed to store missed topic: {str(e)}")

    def get_strengths(self, db: Session, user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve user strengths"""
        try:
            strengths = db.query(UserMemory).filter(
                UserMemory.user_id == user_id,
                UserMemory.memory_type == "strength"
            ).order_by(UserMemory.updated_at.desc()).limit(limit).all()
            
            return [
                {
                    "area": s.content,
                    "score": s.data.get("score") if s.data else None,
                    "updated_at": s.updated_at
                }
                for s in strengths
            ]
        except Exception as e:
            logger.error(f"Failed to retrieve strengths: {str(e)}")
            return []

    def get_weaknesses(self, db: Session, user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve user weaknesses"""
        try:
            weaknesses = db.query(UserMemory).filter(
                UserMemory.user_id == user_id,
                UserMemory.memory_type == "weakness"
            ).order_by(UserMemory.updated_at.desc()).limit(limit).all()
            
            return [
                {
                    "area": w.content,
                    "improvement_steps": w.data.get("improvement_steps") if w.data else [],
                    "updated_at": w.updated_at
                }
                for w in weaknesses
            ]
        except Exception as e:
            logger.error(f"Failed to retrieve weaknesses: {str(e)}")
            return []

    def get_covered_topics(self, db: Session, user_id: int) -> List[Dict[str, Any]]:
        """Retrieve covered topics"""
        try:
            topics = db.query(UserMemory).filter(
                UserMemory.user_id == user_id,
                UserMemory.memory_type == "topic_covered"
            ).order_by(UserMemory.updated_at.desc()).all()
            
            return [
                {
                    "topic": t.content,
                    "proficiency": t.data.get("proficiency") if t.data else "unknown",
                    "covered_at": t.updated_at
                }
                for t in topics
            ]
        except Exception as e:
            logger.error(f"Failed to retrieve covered topics: {str(e)}")
            return []

    def get_missed_topics(self, db: Session, user_id: int) -> List[Dict[str, Any]]:
        """Retrieve missed topics"""
        try:
            topics = db.query(UserMemory).filter(
                UserMemory.user_id == user_id,
                UserMemory.memory_type == "missed_topic"
            ).order_by(UserMemory.updated_at.desc()).all()
            
            return [
                {
                    "topic": t.content,
                    "priority": t.data.get("priority") if t.data else "medium",
                    "identified_at": t.updated_at
                }
                for t in topics
            ]
        except Exception as e:
            logger.error(f"Failed to retrieve missed topics: {str(e)}")
            return []

    def get_memory_summary(self, db: Session, user_id: int) -> Dict[str, Any]:
        """Get summary of user memory"""
        try:
            return {
                "strengths": self.get_strengths(db, user_id),
                "weaknesses": self.get_weaknesses(db, user_id),
                "covered_topics": self.get_covered_topics(db, user_id),
                "missed_topics": self.get_missed_topics(db, user_id)
            }
        except Exception as e:
            logger.error(f"Failed to retrieve memory summary: {str(e)}")
            return {
                "strengths": [],
                "weaknesses": [],
                "covered_topics": [],
                "missed_topics": []
            }
