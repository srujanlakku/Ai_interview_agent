#!/usr/bin/env python3
"""
AI Interview Agent - Main Entry Point

A production-ready AI Interview Agent that conducts adaptive technical interviews.

Usage:
    python app.py

Requirements:
    - Python 3.10+
    - OpenAI API key set in environment or .env file
"""
import os
import sys
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List

# Ensure the app directory is in path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import rich for CLI formatting
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, IntPrompt
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.markdown import Markdown
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Note: Install 'rich' for better CLI experience: pip install rich")

# Import interview components
from app.agents.question_selector_agent import QuestionSelectorAgent
from app.agents.evaluation_agent import EvaluationAgent
from app.evaluation.scorer import Scorer
from app.evaluation.report_generator import ReportGenerator
from app.memory.memory_manager import MemoryManager, InterviewState
from app.schemas.question_schema import InterviewQuestion
from app.data.question_repository import get_question_repository


# ============================================================================
# CLI Helper Functions
# ============================================================================

def get_console() -> Optional['Console']:
    """Get Rich console if available."""
    if RICH_AVAILABLE:
        return Console()
    return None


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner(console: Optional['Console'] = None):
    """Display the welcome banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║           🎯  AI INTERVIEW AGENT  🎯                      ║
    ║                                                           ║
    ║     Adaptive Technical Interview Simulator                ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    if console:
        console.print(Panel(banner, style="bold blue"))
    else:
        print(banner)


def print_question(question: Dict[str, Any], question_num: int, total: int, console: Optional['Console'] = None):
    """Display a question to the user."""
    q_type = question.get("question_type", "technical").upper()
    difficulty = question.get("difficulty", "medium").upper()
    topic = question.get("topic", "General")
    
    header = f"Question {question_num}/{total} | {q_type} | {difficulty} | Topic: {topic}"
    
    if console:
        console.print()
        console.print(Panel(
            question["question_text"],
            title=header,
            title_align="left",
            border_style="cyan",
            padding=(1, 2),
        ))
    else:
        print(f"\n{'=' * 60}")
        print(header)
        print('=' * 60)
        print(f"\n{question['question_text']}\n")
        print('-' * 60)


def print_feedback(evaluation: Dict[str, Any], console: Optional['Console'] = None):
    """Display feedback for an answer."""
    score = evaluation.get("score", 0)
    feedback = evaluation.get("feedback", "No feedback available.")
    strengths = evaluation.get("strengths", [])
    weaknesses = evaluation.get("weaknesses", [])
    
    # Color based on score
    if score >= 7:
        score_style = "bold green"
    elif score >= 5:
        score_style = "bold yellow"
    else:
        score_style = "bold red"
    
    if console:
        console.print()
        console.print(f"Score: [{score_style}]{score:.1f}/10[/]")
        console.print()
        console.print(f"[italic]{feedback}[/italic]")
        
        if strengths:
            console.print("\n[green]Strengths:[/green]")
            for s in strengths[:3]:
                console.print(f"  + {s}")
        
        if weaknesses:
            console.print("\n[yellow]Areas to improve:[/yellow]")
            for w in weaknesses[:3]:
                console.print(f"  - {w}")
    else:
        print(f"\nScore: {score:.1f}/10")
        print(f"\n{feedback}")
        if strengths:
            print("\nStrengths:")
            for s in strengths[:3]:
                print(f"  + {s}")
        if weaknesses:
            print("\nAreas to improve:")
            for w in weaknesses[:3]:
                print(f"  - {w}")


def print_report(report: Dict[str, Any], console: Optional['Console'] = None):
    """Display the final report."""
    if console:
        console.print()
        console.print(Panel("INTERVIEW COMPLETE", style="bold green"))
        console.print()
        
        # Score table
        table = Table(title="Performance Summary", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right")
        
        table.add_row("Overall Score", f"{report.get('overall_score', 0):.1f}/10")
        table.add_row("Readiness Level", report.get("readiness_level", "N/A"))
        table.add_row("Questions Completed", str(report.get("total_questions", 0)))
        table.add_row("Strongest Area", report.get("strongest_area", "N/A"))
        table.add_row("Focus Area", report.get("weakest_area", "N/A"))
        
        console.print(table)
        console.print()
        
        # Assessment
        console.print(Panel(
            report.get("overall_assessment", "No assessment available."),
            title="Assessment",
            border_style="blue",
        ))
        
        # Strengths and improvements
        console.print()
        console.print("[bold green]Top Strengths:[/bold green]")
        for s in report.get("top_strengths", [])[:5]:
            console.print(f"  ✓ {s}")
        
        console.print()
        console.print("[bold yellow]Priority Improvements:[/bold yellow]")
        for i in report.get("priority_improvements", [])[:5]:
            console.print(f"  → {i}")
        
        # Next steps
        console.print()
        console.print("[bold cyan]Recommended Next Steps:[/bold cyan]")
        for idx, step in enumerate(report.get("next_steps", [])[:4], 1):
            console.print(f"  {idx}. {step}")
        
        console.print()
        console.print(Panel(
            report.get("encouragement", "Keep practicing!"),
            style="bold blue",
        ))
    else:
        # Plain text fallback
        from app.evaluation.report_generator import ReportGenerator
        rg = ReportGenerator()
        print(rg.generate_text_report(report))


# ============================================================================
# Main Interview Class
# ============================================================================

class InterviewSession:
    """
    Manages a complete interview session.
    
    Coordinates:
    - Question selection
    - Answer evaluation
    - Score tracking
    - Report generation
    """
    
    def __init__(self, console: Optional['Console'] = None):
        self.console = console
        self.question_selector = QuestionSelectorAgent()
        self.evaluator = EvaluationAgent()
        self.scorer = Scorer()
        self.report_generator = ReportGenerator()
        self.memory_manager = MemoryManager()
        self.state: Optional[InterviewState] = None
        
        # Configuration
        self.max_questions = int(os.getenv("INTERVIEW_MAX_QUESTIONS", "8"))
        self.all_strengths: List[str] = []
        self.all_weaknesses: List[str] = []
    
    def select_role(self) -> str:
        """Allow user to select their target role."""
        roles = self.question_selector.get_available_roles()
        
        if self.console:
            self.console.print("\n[bold]Select your target role:[/bold]\n")
            for i, role in enumerate(roles, 1):
                self.console.print(f"  {i}. {role}")
            self.console.print()
            
            while True:
                try:
                    choice = IntPrompt.ask("Enter number", default=1)
                    if 1 <= choice <= len(roles):
                        return roles[choice - 1]
                    self.console.print("[red]Invalid choice. Try again.[/red]")
                except Exception:
                    self.console.print("[red]Please enter a valid number.[/red]")
        else:
            print("\nSelect your target role:\n")
            for i, role in enumerate(roles, 1):
                print(f"  {i}. {role}")
            
            while True:
                try:
                    choice = int(input("\nEnter number (default: 1): ") or "1")
                    if 1 <= choice <= len(roles):
                        return roles[choice - 1]
                    print("Invalid choice. Try again.")
                except ValueError:
                    print("Please enter a valid number.")
    
    def select_experience_level(self) -> str:
        """Allow user to select their experience level."""
        levels = ["fresher", "mid", "senior"]
        descriptions = {
            "fresher": "0-2 years (Entry level / New graduate)",
            "mid": "2-5 years (Intermediate)",
            "senior": "5+ years (Experienced / Lead)",
        }
        
        if self.console:
            self.console.print("\n[bold]Select your experience level:[/bold]\n")
            for i, level in enumerate(levels, 1):
                self.console.print(f"  {i}. {level.title()} - {descriptions[level]}")
            self.console.print()
            
            while True:
                try:
                    choice = IntPrompt.ask("Enter number", default=2)
                    if 1 <= choice <= len(levels):
                        return levels[choice - 1]
                    self.console.print("[red]Invalid choice. Try again.[/red]")
                except Exception:
                    self.console.print("[red]Please enter a valid number.[/red]")
        else:
            print("\nSelect your experience level:\n")
            for i, level in enumerate(levels, 1):
                print(f"  {i}. {level.title()} - {descriptions[level]}")
            
            while True:
                try:
                    choice = int(input("\nEnter number (default: 2): ") or "2")
                    if 1 <= choice <= len(levels):
                        return levels[choice - 1]
                    print("Invalid choice. Try again.")
                except ValueError:
                    print("Please enter a valid number.")
    
    def get_user_answer(self) -> str:
        """Get the user's answer to a question."""
        if self.console:
            self.console.print("\n[dim]Type your answer (press Enter twice to submit, or type 'skip' to skip):[/dim]\n")
        else:
            print("\nType your answer (press Enter twice to submit, or type 'skip' to skip):\n")
        
        lines = []
        empty_count = 0
        
        while True:
            try:
                line = input()
                if line.lower() == 'skip':
                    return "I would like to skip this question."
                if line == "":
                    empty_count += 1
                    if empty_count >= 2:
                        break
                    lines.append("")
                else:
                    empty_count = 0
                    lines.append(line)
            except EOFError:
                break
        
        answer = "\n".join(lines).strip()
        return answer if answer else "I don't have an answer for this question."
    
    async def run_interview(self):
        """Run the complete interview session."""
        # Validate API key
        if not os.getenv("OPENAI_API_KEY"):
            if self.console:
                self.console.print("[bold red]Error: OPENAI_API_KEY not set![/bold red]")
                self.console.print("\nPlease set your OpenAI API key:")
                self.console.print("  1. Create a .env file in the backend directory")
                self.console.print("  2. Add: OPENAI_API_KEY=your_key_here")
            else:
                print("Error: OPENAI_API_KEY not set!")
                print("\nPlease set your OpenAI API key in .env file")
            return
        
        # Welcome and setup
        clear_screen()
        print_banner(self.console)
        
        if self.console:
            self.console.print("\nWelcome to the AI Interview Agent!")
            self.console.print("This is a mock interview to help you prepare for real interviews.\n")
        else:
            print("\nWelcome to the AI Interview Agent!")
            print("This is a mock interview to help you prepare for real interviews.\n")
        
        # Select role and experience
        role = self.select_role()
        experience_level = self.select_experience_level()
        
        # Determine initial difficulty based on experience
        initial_difficulty = {
            "fresher": "easy",
            "mid": "medium",
            "senior": "medium",
        }.get(experience_level, "medium")
        
        # Initialize session state
        self.state = self.memory_manager.create_session(
            role=role,
            experience_level=experience_level,
            initial_difficulty=initial_difficulty,
        )
        
        if self.console:
            self.console.print(f"\n[bold green]Starting interview for {role} ({experience_level} level)[/bold green]")
            self.console.print(f"You will be asked up to {self.max_questions} questions.\n")
            self.console.print("[dim]Press Enter to begin...[/dim]")
        else:
            print(f"\nStarting interview for {role} ({experience_level} level)")
            print(f"You will be asked up to {self.max_questions} questions.\n")
            print("Press Enter to begin...")
        
        input()
        
        # Interview loop
        question_num = 0
        while question_num < self.max_questions:
            question_num += 1
            
            # Get next question
            if self.console:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=self.console,
                ) as progress:
                    progress.add_task("Preparing question...", total=None)
                    question = await self.question_selector.execute(
                        role=role,
                        experience_level=experience_level,
                        difficulty=self.state.current_difficulty,
                        asked_question_ids=self.state.asked_question_ids,
                        asked_topics=self.state.asked_topics,
                    )
            else:
                print("\nPreparing question...")
                question = await self.question_selector.execute(
                    role=role,
                    experience_level=experience_level,
                    difficulty=self.state.current_difficulty,
                    asked_question_ids=self.state.asked_question_ids,
                    asked_topics=self.state.asked_topics,
                )
            
            # Display question
            print_question(question, question_num, self.max_questions, self.console)
            
            # Get answer
            answer = self.get_user_answer()
            
            # Check for quit
            if answer.lower() in ['quit', 'exit', 'q']:
                if self.console:
                    self.console.print("\n[yellow]Interview ended early.[/yellow]")
                else:
                    print("\nInterview ended early.")
                break
            
            # Evaluate answer
            if self.console:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=self.console,
                ) as progress:
                    progress.add_task("Evaluating your answer...", total=None)
                    evaluation = await self.evaluator.execute(
                        question=question["question_text"],
                        answer=answer,
                        question_type=question.get("question_type", "technical"),
                        ideal_answer_points=question.get("ideal_answer_points", []),
                        experience_level=experience_level,
                    )
            else:
                print("\nEvaluating your answer...")
                evaluation = await self.evaluator.execute(
                    question=question["question_text"],
                    answer=answer,
                    question_type=question.get("question_type", "technical"),
                    ideal_answer_points=question.get("ideal_answer_points", []),
                    experience_level=experience_level,
                )
            
            # Process score
            score_breakdown = self.scorer.score_answer(
                evaluation,
                question.get("question_type", "technical"),
            )
            
            # Display feedback
            print_feedback(evaluation, self.console)
            
            # Update state
            q_obj = InterviewQuestion(
                question_id=question.get("question_id", f"q_{question_num}"),
                question_text=question["question_text"],
                question_type=question.get("question_type", "technical"),
                role=role,
                difficulty=question.get("difficulty", "medium"),
                topic=question.get("topic", "General"),
                ideal_answer_points=question.get("ideal_answer_points", []),
            )
            
            self.memory_manager.add_interaction(
                state=self.state,
                question=q_obj,
                answer=answer,
                score=evaluation.get("score", 5),
                feedback=evaluation.get("feedback", ""),
                strengths=evaluation.get("strengths", []),
                weaknesses=evaluation.get("weaknesses", []),
            )
            
            # Collect strengths and weaknesses
            self.all_strengths.extend(evaluation.get("strengths", []))
            self.all_weaknesses.extend(evaluation.get("weaknesses", []))
            
            # Continue prompt
            if question_num < self.max_questions:
                if self.console:
                    self.console.print("\n[dim]Press Enter for next question (or type 'quit' to end)...[/dim]")
                else:
                    print("\nPress Enter for next question (or type 'quit' to end)...")
                
                user_input = input()
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
        
        # Generate final report
        if self.console:
            self.console.print("\n")
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
            ) as progress:
                progress.add_task("Generating your interview report...", total=None)
                await self._generate_report(role, experience_level)
        else:
            print("\nGenerating your interview report...")
            await self._generate_report(role, experience_level)
    
    async def _generate_report(self, role: str, experience_level: str):
        """Generate and display the final report."""
        performance_summary = self.scorer.get_performance_summary()
        
        report = await self.report_generator.execute(
            role=role,
            experience_level=experience_level,
            performance_summary=performance_summary,
            all_strengths=self.all_strengths,
            all_weaknesses=self.all_weaknesses,
        )
        
        print_report(report, self.console)


# ============================================================================
# Main Entry Point
# ============================================================================

def ensure_directories():
    """Ensure required directories exist."""
    dirs = ["logs", "temp"]
    base_path = Path(__file__).parent
    
    for dir_name in dirs:
        dir_path = base_path / dir_name
        dir_path.mkdir(exist_ok=True)


def main():
    """Main entry point for the AI Interview Agent."""
    ensure_directories()
    
    console = get_console()
    session = InterviewSession(console)
    
    try:
        asyncio.run(session.run_interview())
    except KeyboardInterrupt:
        if console:
            console.print("\n\n[yellow]Interview interrupted. Goodbye![/yellow]")
        else:
            print("\n\nInterview interrupted. Goodbye!")
    except Exception as e:
        if console:
            console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
        else:
            print(f"\nError: {str(e)}")
        raise


if __name__ == "__main__":
    main()
