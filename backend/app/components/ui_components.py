"""
Production UI Components for AI Interview Agent
Reusable, accessible, and production-ready UI elements
"""
import streamlit as st
from typing import Optional, List, Dict, Any, Union
import time
from contextlib import contextmanager

class ProductionUI:
    """Production-ready UI components with consistent styling"""
    
    # Color palette
    COLORS = {
        "primary": "#2563eb",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444",
        "info": "#3b82f6",
        "background": "#0f172a",
        "card": "#1e293b",
        "text_primary": "#f1f5f9",
        "text_secondary": "#94a3b8"
    }
    
    @staticmethod
    def loading_spinner(message: str = "Processing...", size: str = "large"):
        """Production-ready loading spinner"""
        with st.spinner(message):
            # Add subtle animation effect
            time.sleep(0.1)  # Brief pause for visual feedback
            yield
    
    @staticmethod
    @contextmanager
    def loading_overlay(message: str = "Processing your request..."):
        """Full-screen loading overlay"""
        # Create overlay container
        overlay_placeholder = st.empty()
        
        with overlay_placeholder.container():
            st.markdown(f"""
            <div style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(15, 23, 42, 0.9);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                z-index: 9999;
                backdrop-filter: blur(4px);
            ">
                <div style="
                    background: #1e293b;
                    padding: 2rem;
                    border-radius: 12px;
                    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
                    text-align: center;
                    border: 1px solid #334155;
                ">
                    <div style="font-size: 2rem; margin-bottom: 1rem;">🔄</div>
                    <div style="color: #f1f5f9; font-size: 1.1rem; font-weight: 500;">
                        {message}
                    </div>
                    <div style="color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem;">
                        This may take a few moments
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            try:
                yield
            finally:
                overlay_placeholder.empty()
    
    @staticmethod
    def success_banner(message: str, subtitle: Optional[str] = None):
        """Success notification banner"""
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #10b981, #059669);
            border: 1px solid #047857;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.2);
        ">
            <div style="display: flex; align-items: flex-start; gap: 1rem;">
                <div style="font-size: 1.5rem;">✅</div>
                <div>
                    <div style="color: white; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.25rem;">
                        {message}
                    </div>
                    {f'<div style="color: #d1fae5; font-size: 0.9rem;">{subtitle}</div>' if subtitle else ''}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def error_banner(message: str, details: Optional[str] = None):
        """Error notification banner"""
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #ef4444, #dc2626);
            border: 1px solid #b91c1c;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.2);
        ">
            <div style="display: flex; align-items: flex-start; gap: 1rem;">
                <div style="font-size: 1.5rem;">⚠️</div>
                <div>
                    <div style="color: white; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.25rem;">
                        {message}
                    </div>
                    {f'<div style="color: #fee2e2; font-size: 0.9rem;">{details}</div>' if details else ''}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def info_card(title: str, content: str, icon: str = "ℹ️", color: str = "info"):
        """Information card component"""
        color_map = {
            "info": ("#3b82f6", "#dbeafe"),
            "warning": ("#f59e0b", "#fef3c7"),
            "success": ("#10b981", "#d1fae5")
        }
        
        bg_color, text_color = color_map.get(color, color_map["info"])
        
        st.markdown(f"""
        <div style="
            background: {ProductionUI.COLORS['card']};
            border-left: 4px solid {bg_color};
            border-radius: 8px;
            padding: 1.25rem;
            margin: 0.75rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                <div style="font-size: 1.25rem; margin-top: 0.1rem;">{icon}</div>
                <div>
                    <div style="color: {ProductionUI.COLORS['text_primary']}; font-weight: 600; margin-bottom: 0.5rem;">
                        {title}
                    </div>
                    <div style="color: {ProductionUI.COLORS['text_secondary']}; line-height: 1.5;">
                        {content}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def progress_tracker(steps: List[str], current_step: int):
        """Visual progress tracker"""
        st.markdown(f"""
        <div style="margin: 2rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                {''.join([
                    f'<div style="flex: 1; text-align: center; color: {"#2563eb" if i <= current_step else "#64748b"}; font-weight: {"600" if i <= current_step else "400"}; font-size: 0.9rem;">{step}</div>'
                    for i, step in enumerate(steps)
                ])}
            </div>
            <div style="height: 6px; background: #334155; border-radius: 3px; overflow: hidden;">
                <div style="
                    height: 100%;
                    width: {(current_step + 1) / len(steps) * 100}%;
                    background: linear-gradient(90deg, #2563eb, #3b82f6);
                    border-radius: 3px;
                    transition: width 0.3s ease;
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def empty_state(icon: str, title: str, message: str, action_text: Optional[str] = None, action_callback=None):
        """Empty state component"""
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 3rem 1rem;
            background: {ProductionUI.COLORS['card']};
            border-radius: 12px;
            margin: 2rem 0;
            border: 1px dashed #334155;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.7;">{icon}</div>
            <div style="color: {ProductionUI.COLORS['text_primary']}; font-size: 1.25rem; font-weight: 600; margin-bottom: 0.75rem;">
                {title}
            </div>
            <div style="color: {ProductionUI.COLORS['text_secondary']}; font-size: 1rem; line-height: 1.6; max-width: 500px; margin: 0 auto 1.5rem;">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if action_text and action_callback:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(action_text, use_container_width=True, type="primary"):
                    action_callback()

# Convenience functions
def show_loading(message: str = "Processing..."):
    """Show loading spinner"""
    return ProductionUI.loading_spinner(message)

def show_success(message: str, subtitle: Optional[str] = None):
    """Show success banner"""
    ProductionUI.success_banner(message, subtitle)

def show_error(message: str, details: Optional[str] = None):
    """Show error banner"""
    ProductionUI.error_banner(message, details)

def show_info_card(title: str, content: str, icon: str = "ℹ️", color: str = "info"):
    """Show information card"""
    ProductionUI.info_card(title, content, icon, color)

def show_progress(steps: List[str], current_step: int):
    """Show progress tracker"""
    ProductionUI.progress_tracker(steps, current_step)

def show_empty_state(icon: str, title: str, message: str, action_text: Optional[str] = None, action_callback=None):
    """Show empty state"""
    ProductionUI.empty_state(icon, title, message, action_text, action_callback)