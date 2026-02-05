"""
Pages module for the AI Interview Agent web application.
"""
from pages.home_page import render_home_page
from pages.login_page import render_login_page
from pages.interview_page import render_interview_page
from pages.results_page import render_results_page
from pages.history_page import render_history_page
from pages.admin_page import render_admin_page

__all__ = [
    "render_home_page",
    "render_login_page", 
    "render_interview_page",
    "render_results_page",
    "render_history_page",
    "render_admin_page"
]
