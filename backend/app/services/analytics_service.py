"""
Analytics service for tracking question frequency and dashboard data
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Optional
from datetime import datetime
from app.models.database import QuestionFrequency, Interview, InterviewSessionQuestion
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class AnalyticsService:
    """Service for analytics and dashboard data"""

    @staticmethod
    def track_question(
        db: Session,
        company_name: str,
        job_role: str,
        question_text: str,
        question_type: str,
        category: Optional[str] = None
    ) -> QuestionFrequency:
        """Track a question being asked, increment frequency if exists"""
        try:
            # Check if question already exists for this company/role
            existing = db.query(QuestionFrequency).filter(
                QuestionFrequency.company_name == company_name,
                QuestionFrequency.job_role == job_role,
                QuestionFrequency.question_text == question_text
            ).first()

            if existing:
                # Increment frequency
                existing.frequency_count += 1
                existing.last_asked_date = datetime.utcnow()
                db.commit()
                db.refresh(existing)
                logger.info(f"Updated question frequency: {existing.id}, count: {existing.frequency_count}")
                return existing
            else:
                # Create new entry
                new_freq = QuestionFrequency(
                    company_name=company_name,
                    job_role=job_role,
                    question_text=question_text,
                    question_type=question_type,
                    category=category,
                    frequency_count=1
                )
                db.add(new_freq)
                db.commit()
                db.refresh(new_freq)
                logger.info(f"Created new question frequency: {new_freq.id}")
                return new_freq

        except Exception as e:
            db.rollback()
            logger.error(f"Error tracking question: {str(e)}")
            raise

    @staticmethod
    def get_top_questions(
        db: Session,
        company_name: str,
        job_role: str,
        limit: int = 20
    ) -> List[QuestionFrequency]:
        """Get top frequently asked questions for a company/role"""
        try:
            questions = db.query(QuestionFrequency).filter(
                QuestionFrequency.company_name == company_name,
                QuestionFrequency.job_role == job_role
            ).order_by(
                desc(QuestionFrequency.frequency_count),
                desc(QuestionFrequency.last_asked_date)
            ).limit(limit).all()

            logger.info(f"Retrieved {len(questions)} top questions for {company_name} - {job_role}")
            return questions

        except Exception as e:
            logger.error(f"Error getting top questions: {str(e)}")
            raise

    @staticmethod
    def get_company_stats(db: Session, company_name: str) -> Dict:
        """Get statistics for a company"""
        try:
            # Get total interviews for this company
            total_interviews = db.query(Interview).filter(
                Interview.company_name == company_name
            ).count()

            # Get most asked roles
            role_counts = db.query(
                Interview.job_role,
                func.count(Interview.id).label('count')
            ).filter(
                Interview.company_name == company_name,
                Interview.job_role.isnot(None)
            ).group_by(
                Interview.job_role
            ).order_by(
                desc('count')
            ).limit(5).all()

            most_asked_roles = [role for role, count in role_counts]

            # Get common topics from questions
            topic_counts = db.query(
                InterviewSessionQuestion.topic,
                func.count(InterviewSessionQuestion.id).label('count')
            ).join(
                Interview,
                InterviewSessionQuestion.interview_id == Interview.id
            ).filter(
                Interview.company_name == company_name,
                InterviewSessionQuestion.topic.isnot(None)
            ).group_by(
                InterviewSessionQuestion.topic
            ).order_by(
                desc('count')
            ).limit(10).all()

            common_topics = [topic for topic, count in topic_counts if topic]

            stats = {
                "company": company_name,
                "total_interviews": total_interviews,
                "most_asked_roles": most_asked_roles,
                "common_topics": common_topics
            }

            logger.info(f"Retrieved stats for {company_name}: {total_interviews} interviews")
            return stats

        except Exception as e:
            logger.error(f"Error getting company stats: {str(e)}")
            raise

    @staticmethod
    def get_question_categories_for_role(db: Session, job_role: str) -> Dict[str, int]:
        """Get breakdown of question types for a specific role"""
        try:
            category_counts = db.query(
                InterviewSessionQuestion.question_type,
                func.count(InterviewSessionQuestion.id).label('count')
            ).join(
                Interview,
                InterviewSessionQuestion.interview_id == Interview.id
            ).filter(
                Interview.job_role == job_role
            ).group_by(
                InterviewSessionQuestion.question_type
            ).all()

            return {q_type: count for q_type, count in category_counts}

        except Exception as e:
            logger.error(f"Error getting question categories: {str(e)}")
            raise

    @staticmethod
    def get_sure_questions(db: Session, company_name: str, job_role: str) -> Dict[str, List[QuestionFrequency]]:
        """
        Get 'Sure Questions' (high frequency) grouped by category.
        """
        try:
            questions = db.query(QuestionFrequency).filter(
                QuestionFrequency.company_name == company_name,
                QuestionFrequency.job_role == job_role
            ).order_by(
                desc(QuestionFrequency.frequency_count)
            ).all()

            # Group by type (behavioral, technical, coding)
            grouped = {
                "behavioral": [],
                "technical": [],
                "coding": []
            }

            for q in questions:
                q_type = q.question_type.lower()
                if "soft" in q_type or "behavioral" in q_type:
                    grouped["behavioral"].append(q)
                elif "coding" in q_type:
                    grouped["coding"].append(q)
                else:
                    grouped["technical"].append(q)

            return grouped

        except Exception as e:
            logger.error(f"Error getting sure questions: {str(e)}")
            raise
