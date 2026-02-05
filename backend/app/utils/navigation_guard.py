"""
Production Navigation Guard System
Prevents accidental navigation and ensures smooth user experience
"""
import streamlit as st
from typing import Optional, Callable
from .session_manager import SessionManager, get_session_info

class NavigationGuard:
    """Manages safe navigation with confirmation dialogs"""
    
    @staticmethod
    def check_interview_in_progress() -> bool:
        """Check if user is in the middle of an interview"""
        session_state = get_session_info()
        current_page = st.session_state.get("page", "")
        
        # Check if interview is active
        interview_active = (
            session_state.get("state") in ["in_progress", "question_displayed"] or
            st.session_state.get("interview_active", False) or
            st.session_state.get("current_question") is not None
        )
        
        # Allow navigation away from interview pages only if not in progress
        interview_pages = ["interview", "results"]
        on_interview_page = current_page in interview_pages
        
        return interview_active and on_interview_page
    
    @staticmethod
    def show_navigation_warning(target_page: str) -> bool:
        """
        Show warning dialog for risky navigation
        Returns True if user confirms navigation
        """
        if not NavigationGuard.check_interview_in_progress():
            return True
            
        # Store intended navigation
        st.session_state["_pending_navigation"] = target_page
        
        # Show warning in sidebar or modal-like component
        with st.sidebar:
            st.warning("⚠️ Interview in Progress")
            st.caption("Leaving now will lose your current progress")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save & Exit", key="nav_save_exit", use_container_width=True):
                    NavigationGuard._handle_safe_exit()
                    return True
            with col2:
                if st.button("❌ Cancel", key="nav_cancel", use_container_width=True):
                    st.session_state["_pending_navigation"] = None
                    st.rerun()
        
        return False
    
    @staticmethod
    def _handle_safe_exit():
        """Handle safe exit with session preservation"""
        # Mark session as intentionally ended
        SessionManager.update_state(state="user_interrupted")
        st.session_state["_pending_navigation"] = st.session_state.get("_pending_navigation", "home")
        st.rerun()
    
    @staticmethod
    def can_navigate_to(page: str) -> bool:
        """Check if navigation to target page is allowed"""
        current_page = st.session_state.get("page", "")
        
        # Always allow navigation to home/login
        if page in ["home", "login"]:
            return True
            
        # Prevent navigation during critical interview phases
        if NavigationGuard.check_interview_in_progress():
            if page != "interview":  # Allow staying on interview page
                return NavigationGuard.show_navigation_warning(page)
        
        return True
    
    @staticmethod
    def safe_navigate(page: str):
        """Safely navigate to target page"""
        if NavigationGuard.can_navigate_to(page):
            st.session_state.page = page
            st.session_state["_pending_navigation"] = None
            st.rerun()

class UserActionTracker:
    """Tracks user actions for analytics and recovery"""
    
    @staticmethod
    def record_action(action: str, details: Optional[dict] = None):
        """Record user action for session analytics"""
        session_data = get_session_info()
        if "user_actions" not in session_data:
            session_data["user_actions"] = []
            
        action_record = {
            "action": action,
            "timestamp": st.session_state.get("_current_time", ""),
            "details": details or {}
        }
        
        session_data["user_actions"].append(action_record)
        SessionManager.update_state(user_actions=session_data["user_actions"])

# Convenience functions
def check_navigation_safety(target_page: str) -> bool:
    """Check if navigation to target page is safe"""
    return NavigationGuard.can_navigate_to(target_page)

def safe_page_redirect(page: str):
    """Safely redirect to target page"""
    NavigationGuard.safe_navigate(page)

def record_user_action(action: str, details: Optional[dict] = None):
    """Record user action for analytics"""
    UserActionTracker.record_action(action, details)

def is_interview_in_progress() -> bool:
    """Check if interview is currently in progress"""
    return NavigationGuard.check_interview_in_progress()