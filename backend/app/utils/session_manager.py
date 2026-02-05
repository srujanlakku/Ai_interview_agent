"""
Production Session Manager for AI Interview Agent
Handles persistent state, recovery, and safe navigation
"""
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional
import streamlit as st
from .structured_logging import get_logger

logger = get_logger(__name__)

class SessionManager:
    """Manages interview session state with persistence and recovery capabilities"""
    
    SESSION_KEY = "interview_session_state"
    BACKUP_KEY = "interview_session_backup"
    VERSION = "1.0.0"
    
    @staticmethod
    def get_session_hash() -> str:
        """Generate unique session identifier"""
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "user_agent": str(st.session_state.get("__user_agent", "unknown")),
        }
        return hashlib.md5(json.dumps(session_data, sort_keys=True).encode()).hexdigest()[:12]
    
    @classmethod
    def initialize_session(cls) -> str:
        """Initialize or recover session state"""
        session_id = cls.get_session_hash()
        
        # Try to restore from backup first
        restored = cls.restore_session()
        if restored:
            logger.info(f"Session restored: {session_id}")
            st.session_state[cls.SESSION_KEY] = restored
        else:
            # Initialize fresh session
            st.session_state[cls.SESSION_KEY] = {
                "session_id": session_id,
                "created_at": datetime.now().isoformat(),
                "version": cls.VERSION,
                "state": "initialized",
                "pages_visited": [],
                "interview_data": {},
                "user_actions": []
            }
            logger.info(f"New session created: {session_id}")
        
        # Track page visit
        cls._track_page_visit()
        return session_id
    
    @classmethod
    def save_session(cls):
        """Save current session state to backup"""
        if cls.SESSION_KEY in st.session_state:
            try:
                session_data = st.session_state[cls.SESSION_KEY].copy()
                session_data["last_saved"] = datetime.now().isoformat()
                st.session_state[cls.BACKUP_KEY] = session_data
                logger.debug(f"Session saved: {session_data.get('session_id', 'unknown')}")
            except Exception as e:
                logger.error(f"Failed to save session: {str(e)}")
    
    @classmethod
    def restore_session(cls) -> Optional[Dict[str, Any]]:
        """Restore session from backup"""
        try:
            if cls.BACKUP_KEY in st.session_state:
                backup_data = st.session_state[cls.BACKUP_KEY]
                # Validate backup data
                if isinstance(backup_data, dict) and "session_id" in backup_data:
                    logger.info(f"Restoring session: {backup_data['session_id']}")
                    return backup_data
            return None
        except Exception as e:
            logger.error(f"Failed to restore session: {str(e)}")
            return None
    
    @classmethod
    def clear_session(cls):
        """Safely clear session data"""
        session_id = st.session_state.get(cls.SESSION_KEY, {}).get("session_id", "unknown")
        logger.info(f"Clearing session: {session_id}")
        
        # Log session completion before clearing
        if st.session_state.get(cls.SESSION_KEY, {}).get("state") == "completed":
            cls._log_session_completion()
        
        # Clear session data
        keys_to_clear = [cls.SESSION_KEY, cls.BACKUP_KEY, "orchestrator_agent", "session_id"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
    
    @classmethod
    def get_current_state(cls) -> Dict[str, Any]:
        """Get current session state"""
        return st.session_state.get(cls.SESSION_KEY, {})
    
    @classmethod
    def update_state(cls, **kwargs):
        """Update session state with provided data"""
        if cls.SESSION_KEY in st.session_state:
            session_data = st.session_state[cls.SESSION_KEY]
            session_data.update(kwargs)
            session_data["last_updated"] = datetime.now().isoformat()
            st.session_state[cls.SESSION_KEY] = session_data
            cls.save_session()  # Auto-save on update
            logger.debug(f"Session updated: {session_data.get('session_id', 'unknown')}")
    
    @classmethod
    def _track_page_visit(cls):
        """Track user page visits for analytics"""
        current_page = st.session_state.get("page", "unknown")
        if cls.SESSION_KEY in st.session_state:
            session_data = st.session_state[cls.SESSION_KEY]
            if "pages_visited" not in session_data:
                session_data["pages_visited"] = []
            
            # Avoid duplicate consecutive visits
            if not session_data["pages_visited"] or session_data["pages_visited"][-1] != current_page:
                session_data["pages_visited"].append(current_page)
                st.session_state[cls.SESSION_KEY] = session_data
    
    @classmethod
    def _log_session_completion(cls):
        """Log completed session for analytics"""
        session_data = st.session_state.get(cls.SESSION_KEY, {})
        logger.info("Interview session completed", extra={
            "session_id": session_data.get("session_id"),
            "duration": cls._calculate_duration(session_data),
            "questions_asked": len(session_data.get("interview_data", {}).get("questions", [])),
            "final_score": session_data.get("interview_data", {}).get("final_score"),
            "pages_visited": len(session_data.get("pages_visited", []))
        })
    
    @staticmethod
    def _calculate_duration(session_data: Dict) -> Optional[float]:
        """Calculate session duration in minutes"""
        try:
            created_at = datetime.fromisoformat(session_data.get("created_at", ""))
            ended_at = datetime.fromisoformat(session_data.get("last_updated", datetime.now().isoformat()))
            return (ended_at - created_at).total_seconds() / 60
        except Exception:
            return None

# Convenience functions for Streamlit integration
def init_production_session():
    """Initialize production session management"""
    return SessionManager.initialize_session()

def save_current_session():
    """Save current session state"""
    SessionManager.save_session()

def restore_session_state():
    """Restore session state if available"""
    return SessionManager.restore_session()

def clear_interview_session():
    """Safely clear interview session"""
    SessionManager.clear_session()

def update_session_state(**kwargs):
    """Update session state with provided data"""
    SessionManager.update_state(**kwargs)

def get_session_info():
    """Get current session information"""
    return SessionManager.get_current_state()