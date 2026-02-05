"""
Interview Page - Interactive chat-style interview with real-time feedback.
"""
import streamlit as st
import asyncio
import sys
import os
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.agents.orchestrator_agent import OrchestratorAgent
from app.utils.history_db import get_history_db
from app.utils.structured_logging import log_interview_start, log_interview_end, log_question_selected, log_answer_evaluated


def run_async(coro):
    """Run async coroutine in Streamlit."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def get_difficulty_color(difficulty: str) -> str:
    """Get color for difficulty badge."""
    colors = {
        "easy": "#10B981",
        "medium": "#F59E0B", 
        "hard": "#EF4444"
    }
    return colors.get(difficulty, "#6366F1")


def get_score_color(score: float) -> str:
    """Get color based on score."""
    if score >= 8:
        return "#10B981"  # Green
    elif score >= 6:
        return "#F59E0B"  # Yellow
    elif score >= 4:
        return "#F97316"  # Orange
    else:
        return "#EF4444"  # Red


def render_question_card(question: dict, question_num: int, max_questions: int):
    """Render the current question in a cyber-styled card."""
    difficulty = question.get("difficulty", "medium")
    topic = question.get("topic", "General")
    q_type = question.get("question_type", question.get("type", "Technical"))
    
    st.markdown(f"""
    <div class="question-box slide-up">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div class="question-header">
                <span class="question-tag tag-type">>> {q_type.upper()} <<</span>
                <span class="question-tag tag-difficulty" style="border: 2px solid #FF0000; color: #FF0000; background: #000000;">
                    >> {difficulty.upper()} <<
                </span>
                <span class="question-tag tag-topic">>> {topic.upper()} <<</span>
            </div>
            <div style="color: #FFFFFF; font-size: 0.9rem; font-family: 'Courier New', monospace;">
                >> QUESTION {question_num} OF {max_questions} <<
            </div>
        </div>
        <div class="question-text" style="font-family: 'Courier New', monospace;">
            {question.get('question_text', question.get('text', question.get('question', 'NO QUESTION AVAILABLE')))}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_chat_history(chat_history: list):
    """Render the chat history with cyber styling."""
    for message in chat_history[-10:]:  # Show last 10 messages
        if message["role"] == "interviewer":
            st.markdown(f"""
            <div class="chat-message interviewer">
                <div class="message-bubble" style="border: 2px solid #FF0000; background: #000000;">
                    <div style="color: #FF0000; font-size: 0.75rem; margin-bottom: 0.25rem; font-family: 'Courier New', monospace;">
                        >> AI INTERVIEWER <<
                    </div>
                    <div class="message-text" style="color: #FFFFFF; font-family: 'Courier New', monospace;">{message['content'][:500]}{'...' if len(message['content']) > 500 else ''}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message candidate">
                <div class="message-bubble" style="border: 1px solid #FFFFFF; background: #000000;">
                    <div style="color: #FFFFFF; font-size: 0.75rem; margin-bottom: 0.25rem; text-align: right; font-family: 'Courier New', monospace;">
                        >> YOU <<
                    </div>
                    <div class="message-text" style="color: #FFFFFF; font-family: 'Courier New', monospace;">{message['content'][:500]}{'...' if len(message['content']) > 500 else ''}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_feedback(evaluation: dict):
    """Render the AI feedback with cyber styling."""
    score = evaluation.get("score", 0)
    feedback = evaluation.get("feedback", "")
    strengths = evaluation.get("strengths", [])
    improvements = evaluation.get("weaknesses", evaluation.get("improvements", evaluation.get("improvement_suggestions", [])))
    
    st.markdown(f"""
    <div class="interview-card" style="margin-top: 1rem;">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="
                width: 60px; height: 60px; border: 3px solid #FF0000;
                display: flex; align-items: center; justify-content: center;
                font-size: 1.5rem; font-weight: 800; color: #FF0000;
                font-family: 'Courier New', monospace; background: #000000;
            ">{score}</div>
            <div>
                <h3 style="color: white; margin: 0; font-family: 'Courier New', monospace;">SCORE: {score}/10</h3>
                <p style="color: #FF0000; margin: 0; font-size: 0.9rem; font-family: 'Courier New', monospace;">
                    {'>> EXCELLENT <<' if score >= 8 else '>> GOOD JOB <<' if score >= 6 else '>> KEEP PRACTICING <<' if score >= 4 else '>> NEEDS IMPROVEMENT <<'}
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if feedback:
        st.markdown(f"""
        <p style="color: #FFFFFF; line-height: 1.6; font-family: 'Courier New', monospace;">{feedback}</p>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if strengths:
            st.markdown('<div class="feedback-positive">', unsafe_allow_html=True)
            st.markdown("**>> STRENGTHS <<**")
            for s in strengths[:3]:
                st.markdown(f">> {s} <<")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if improvements:
            st.markdown('<div class="feedback-negative">', unsafe_allow_html=True)
            st.markdown("**>> AREAS FOR IMPROVEMENT <<**")
            for i in improvements[:3]:
                st.markdown(f"• {i}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_interview_page():
    """Render the main interview page with cyber aesthetic."""
    
    # Add cyber grid background
    st.markdown('<div class="cyber-grid"></div>', unsafe_allow_html=True)
    
    # Initialize orchestrator agent if needed
    if st.session_state.orchestrator_agent is None:
        st.session_state.orchestrator_agent = OrchestratorAgent()
        
        # Create a new session
        session_id = st.session_state.orchestrator_agent.create_session(
            candidate_name=st.session_state.candidate_name,
            role=st.session_state.role,
            experience_level=st.session_state.experience_level,
            company=st.session_state.company,
            max_questions=st.session_state.max_questions,
            resume_skills=st.session_state.get('resume_skills', []),
            resume_projects=st.session_state.get('resume_projects', [])
        )
        st.session_state.session_id = session_id
        
        # Log interview start
        log_interview_start(
            session_id=session_id,
            candidate_name=st.session_state.candidate_name,
            role=st.session_state.role,
            experience_level=st.session_state.experience_level
        )
    
    # Get orchestrator instance
    orchestrator = st.session_state.orchestrator_agent
    session_id = st.session_state.session_id
    
    # Header with progress
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <div>
            <h2 style="color: white; margin: 0; font-family: 'Courier New', monospace; text-shadow: 0 0 10px #FF0000;">
                >> TECHNICAL INTERVIEW PROTOCOL <<
            </h2>
            <p style="color: #FF0000; margin: 0; font-family: 'Courier New', monospace;">
                >> {st.session_state.role.upper()} • {st.session_state.experience_level.upper()} LEVEL <<
            </p>
        </div>
        <div style="text-align: right;">
            <span class="score-badge" style="border: 2px solid #FF0000; color: #FF0000; background: #000000;">
                >> Q{st.session_state.question_number}/{st.session_state.max_questions} <<
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    progress = st.session_state.question_number / st.session_state.max_questions
    st.progress(progress)
    st.markdown(f'<div style="text-align: center; color: #FF0000; font-family: Courier New, monospace;">>> PROTOCOL PROGRESS: {int(progress * 100)}% <<</div>', unsafe_allow_html=True)
    
    # Get or display current question
    if st.session_state.current_question is None:
        # Fetch a new question with enhanced loading
        from app.components.ui_components import show_loading
        from app.utils.error_handler_prod import handle_exception, safe_call
        
        try:
            with st.spinner("🤖 AI is preparing your next question..."):
                question = run_async(orchestrator.get_next_question(session_id))
                
                if question:
                    st.session_state.current_question = question
                    st.session_state.question_number += 1
                    
                    # Track asked questions
                    if question.get("question_id"):
                        st.session_state.asked_ids.append(question["question_id"])
                    if question.get("topic"):
                        st.session_state.asked_topics.append(question["topic"])
                    
                    # Add to chat history
                    q_text = question.get("question_text", question.get("text", question.get("question", "")))
                    st.session_state.chat_history.append({
                        "role": "interviewer",
                        "content": q_text
                    })
                    
                    # Log question selection
                    log_question_selected(
                        session_id=session_id,
                        question_topic=question.get("topic", "General"),
                        difficulty=question.get("difficulty", "medium")
                    )
                    
                    st.rerun()
                else:
                    st.error("❌ Unable to generate question. Please try again.")
                    from app.components.ui_components import show_info_card
                    show_info_card(
                        "💡 Tip", 
                        "This might happen due to temporary AI service issues. Please refresh the page or try again in a moment.",
                        icon="🔧"
                    )
                    return
                    
        except Exception as e:
            handle_exception(e, "Question generation")
            st.error("❌ Something went wrong while preparing your question.")
            from app.components.ui_components import show_info_card
            show_info_card(
                "💡 Need Help?", 
                "Our team has been notified of this issue. Please try refreshing the page or contact support if the problem persists.",
                icon="🆘"
            )
            return
    
    # Display current question
    render_question_card(
        st.session_state.current_question,
        st.session_state.question_number,
        st.session_state.max_questions
    )
    
    # Show previous chat history
    if len(st.session_state.chat_history) > 1:
        with st.expander("📜 Previous Q&A", expanded=False):
            render_chat_history(st.session_state.chat_history[:-1])
    
    # Show feedback if available
    if st.session_state.showing_feedback and st.session_state.last_evaluation:
        render_feedback(st.session_state.last_evaluation)
        
        # Next question or finish button
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.question_number < st.session_state.max_questions:
                if st.button(">> NEXT QUESTION <<", use_container_width=True, key="next_q"):
                    st.session_state.current_question = None
                    st.session_state.showing_feedback = False
                    st.session_state.last_evaluation = None
                    st.rerun()
            else:
                if st.button(">> VIEW RESULTS <<", use_container_width=True, key="view_results"):
                    st.session_state.interview_active = False
                    st.session_state.interview_complete = True
                    st.rerun()
        
        with col2:
            if st.button(">> TERMINATE INTERVIEW <<", use_container_width=True, key="end_now"):
                st.session_state.interview_active = False
                st.session_state.interview_complete = True
                st.rerun()
    
    else:
        # Answer input
        st.markdown("<br/>", unsafe_allow_html=True)
        
        answer = st.text_area(
            "Your Answer",
            height=200,
            placeholder="Type your answer here... Be thorough and explain your reasoning.",
            key="answer_input",
            help="Provide a detailed answer. The AI will evaluate your response."
        )
        
        # Action buttons
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            submit_disabled = not answer.strip()
            if st.button("📤 Submit Answer", use_container_width=True, disabled=submit_disabled, key="submit_btn"):
                if answer.strip():
                    from app.utils.error_handler_prod import handle_exception, safe_call
                    
                    try:
                        with st.spinner("🔍 AI is evaluating your answer..."):
                            # Add answer to chat
                            st.session_state.chat_history.append({
                                "role": "candidate",
                                "content": answer.strip()
                            })
                        
                        # Get evaluation
                        q_text = st.session_state.current_question.get("question_text", 
                            st.session_state.current_question.get("text", 
                            st.session_state.current_question.get("question", "")))
                        
                        evaluation = run_async(orchestrator.evaluate_answer(
                            session_id=session_id,
                            question=st.session_state.current_question,
                            answer=answer.strip()
                        ))
                        
                        if evaluation:
                            # Store evaluation
                            st.session_state.last_evaluation = evaluation
                            st.session_state.showing_feedback = True
                            
                            # Track score
                            score = evaluation.get("score", 5)
                            st.session_state.scores.append(score)
                            
                            # Track strengths/weaknesses
                            if evaluation.get("strengths"):
                                st.session_state.strengths.extend(evaluation["strengths"][:2])
                            if evaluation.get("weaknesses"):
                                st.session_state.weaknesses.extend(evaluation["weaknesses"][:2])
                            elif evaluation.get("improvement_suggestions"):
                                st.session_state.weaknesses.extend(evaluation["improvement_suggestions"][:2])
                            
                            # Update difficulty
                            if score >= 8:
                                st.session_state.difficulty = "hard"
                            elif score <= 4:
                                st.session_state.difficulty = "easy"
                            else:
                                st.session_state.difficulty = "medium"
                            
                            # Log evaluation
                            log_answer_evaluated(
                                session_id=session_id,
                                question_topic=st.session_state.current_question.get("topic", "General"),
                                score=score
                            )
                            
                            st.rerun()
                        else:
                            st.error("❌ Unable to evaluate your answer. Please try again.")
                            from app.components.ui_components import show_info_card
                            show_info_card(
                                "💡 Tip", 
                                "This might be due to temporary AI service issues. Please try submitting your answer again.",
                                icon="🔧"
                            )
                            
                    except Exception as e:
                        from app.utils.error_handler_prod import handle_exception
                        handle_exception(e, "Answer evaluation")
                        st.error("❌ Something went wrong while evaluating your answer.")
                        from app.components.ui_components import show_info_card
                        show_info_card(
                            "💡 Need Help?", 
                            "Our team has been notified of this issue. Please try submitting your answer again or contact support.",
                            icon="🆘"
                        )
        
        with col2:
            if st.button("💡 Get Hint", use_container_width=True, key="hint_btn"):
                q_text = st.session_state.current_question.get("text", 
                    st.session_state.current_question.get("question", ""))
                topic = st.session_state.current_question.get("topic", "General")
                
                st.info(f"""
                **💡 Hint for {topic}:**
                
                Consider discussing:
                - Key concepts and definitions
                - Real-world applications
                - Trade-offs and alternatives
                - Best practices
                """)
        
        with col3:
            if st.button("⏭️ Skip", use_container_width=True, key="skip_btn"):
                st.session_state.scores.append(0)  # Record as 0
                st.session_state.current_question = None
                st.session_state.showing_feedback = False
                
                if st.session_state.question_number >= st.session_state.max_questions:
                    st.session_state.interview_active = False
                    st.session_state.interview_complete = True
                
                st.rerun()
    
    # Quick stats at bottom
    if st.session_state.scores:
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        avg_score = sum(st.session_state.scores) / len(st.session_state.scores)
        best_score = max(st.session_state.scores)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{avg_score:.1f}</div>
                <div class="metric-label">Avg Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{best_score}</div>
                <div class="metric-label">Best Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(st.session_state.scores)}</div>
                <div class="metric-label">Answered</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{st.session_state.difficulty.title()}</div>
                <div class="metric-label">Difficulty</div>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_interview_page()
