"""
Resume Parser - Extract skills and projects from PDF resumes.
"""
import fitz  # PyMuPDF
from typing import Dict, List, Optional
import re
import json
from io import BytesIO


class ResumeParser:
    """
    Parses PDF resumes to extract skills and projects.
    Used for resume-aware interviewing.
    """
    
    def __init__(self):
        # Common skill patterns
        self.skill_patterns = {
            'programming_languages': [
                r'\b(python|java|javascript|typescript|c\+\+|c#|php|ruby|go|rust|scala|kotlin|swift|objective-c)\b',
                r'\b(sql|mysql|postgresql|mongodb|redis|oracle)\b',
                r'\b(html|css|sass|less|bootstrap|tailwind|react|vue|angular|svelte|jquery)\b',
                r'\b(node\.js|express|django|flask|spring boot|laravel|rails)\b',
                r'\b(docker|kubernetes|aws|azure|gcp|terraform|jenkins|git|github|gitlab)\b',
                r'\b(tensorflow|pytorch|scikit-learn|pandas|numpy|matplotlib)\b',
                r'\b(agile|scrum|kanban|jira|confluence|figma|adobe)\b',
            ],
            'technologies': [
                r'\b(linux|windows|macos|unix)\b',
                r'\b(api|rest|graphql|microservices|monolith)\b',
                r'\b(cloud|saas|paas|iaas|devops|ci/cd)\b',
                r'\b(machine learning|artificial intelligence|data science|big data|nlp)\b',
                r'\b(security|cybersecurity|encryption|oauth|ssl|tls)\b',
            ]
        }
        
        # Common section headers
        self.section_headers = [
            r'skills?', r'technical skills?', r'core competencies?', r'expertise',
            r'projects?', r'work experience?', r'education', r'certifications?',
            r'achievements?', r'publications?'
        ]
    
    def parse_pdf_resume(self, pdf_bytes: bytes) -> Dict[str, any]:
        """
        Parse a PDF resume and extract relevant information.
        
        Args:
            pdf_bytes: PDF file as bytes
            
        Returns:
            Dictionary with extracted information
        """
        try:
            # Extract text from PDF
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            
            # Process the text
            return self._extract_information(text)
        
        except Exception as e:
            print(f"Error parsing PDF: {str(e)}")
            return self._get_empty_result()
    
    def _get_empty_result(self) -> Dict[str, any]:
        """Return an empty result when parsing fails."""
        return {
            "skills": [],
            "programming_languages": [],
            "technologies": [],
            "projects": [],
            "experience_years": 0,
            "education": [],
            "summary": ""
        }
    
    def _extract_information(self, text: str) -> Dict[str, any]:
        """Extract information from resume text."""
        # Normalize text
        text = re.sub(r'\s+', ' ', text.lower())
        
        # Extract skills
        skills = self._extract_skills(text)
        
        # Extract projects
        projects = self._extract_projects(text)
        
        # Extract education
        education = self._extract_education(text)
        
        # Estimate experience years
        experience_years = self._estimate_experience(text)
        
        # Extract summary/objective
        summary = self._extract_summary(text)
        
        return {
            "skills": list(set(skills["all_skills"])),
            "programming_languages": list(set(skills["programming_languages"])),
            "technologies": list(set(skills["technologies"])),
            "projects": projects,
            "experience_years": experience_years,
            "education": education,
            "summary": summary
        }
    
    def _extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract various types of skills."""
        all_skills = []
        programming_languages = []
        technologies = []
        
        for category, patterns in self.skill_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text)
                if category == 'programming_languages':
                    programming_languages.extend(matches)
                elif category == 'technologies':
                    technologies.extend(matches)
                all_skills.extend(matches)
        
        return {
            "all_skills": all_skills,
            "programming_languages": programming_languages,
            "technologies": technologies
        }
    
    def _extract_projects(self, text: str) -> List[Dict[str, str]]:
        """Extract project information."""
        # Look for common project indicators
        project_keywords = [
            r'project:', r'projects:', r'personal project', r'individual project',
            r'academic project', r'course project', r'capstone project',
            'built', 'developed', 'created', 'designed', 'engineered'
        ]
        
        # Split text into sentences
        sentences = re.split(r'[.!?]+', text)
        
        projects = []
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence for keyword in ['project', 'built', 'developed', 'created']):
                if len(sentence) > 20:  # Meaningful project description
                    projects.append({
                        "description": sentence.capitalize(),
                        "technologies_used": self._extract_technologies_from_sentence(sentence)
                    })
        
        return projects[:5]  # Limit to top 5 projects
    
    def _extract_technologies_from_sentence(self, sentence: str) -> List[str]:
        """Extract technologies mentioned in a sentence."""
        tech_list = []
        for category, patterns in self.skill_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, sentence)
                tech_list.extend(matches)
        return list(set(tech_list))
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract educational qualifications."""
        # Look for education patterns
        education_patterns = [
            r'(bs|b\.s\.|bachelor\'?s?)\s+(in|of)\s+([a-z\s]+?)(?:\s+(?:degree|major|field)|\s+from|\s+at)',
            r'(ms|m\.s\.|master\'?s?)\s+(in|of)\s+([a-z\s]+?)(?:\s+(?:degree|major|field)|\s+from|\s+at)',
            r'(phd|ph\.d\.|doctorate?)\s+(in|of)\s+([a-z\s]+?)(?:\s+(?:degree|major|field)|\s+from|\s+at)',
            r'(degree|diploma|certificate)\s+(?:in|of)\s+([a-z\s]+?)(?:\s+(?:from|at)|\s+with)'
        ]
        
        education = []
        for pattern in education_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                edu_str = ' '.join(match).strip()
                if len(edu_str) > 5:  # Valid education string
                    education.append(edu_str)
        
        return list(set(education))
    
    def _estimate_experience(self, text: str) -> int:
        """Estimate years of experience."""
        # Look for experience indicators
        experience_patterns = [
            r'(\d+)\s+years?\s+of\s+experience',
            r'(\d+)\s+years?\s+experience',
            r'experience:\s*(\d+)\s+years?',
            r'(\d+)\s+yrs?\s+of\s+experience'
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text)
            if matches:
                try:
                    return max(int(match) for match in matches)
                except ValueError:
                    pass
        
        # Fallback: Look for years of experience in a general way
        # Count mentions of years in work-related context
        year_mentions = re.findall(r'\b(\d{4})\b', text)
        if len(year_mentions) >= 2:
            years = sorted([int(y) for y in year_mentions if 1950 < int(y) < 2030])
            if len(years) >= 2:
                # Estimate based on first and last year mentioned
                return min(20, max(0, years[-1] - years[0]))
        
        return 0
    
    def _extract_summary(self, text: str) -> str:
        """Extract summary or objective section."""
        # Look for summary/objective keywords
        summary_start = -1
        for keyword in ['summary', 'objective', 'about', 'profile']:
            pos = text.find(keyword)
            if pos != -1 and (summary_start == -1 or pos < summary_start):
                summary_start = pos
        
        if summary_start != -1:
            # Extract text around the summary section
            start = max(0, summary_start - 100)
            end = min(len(text), summary_start + 300)
            summary_section = text[start:end]
            
            # Look for end markers
            for end_marker in ['experience', 'education', 'skills', 'projects']:
                end_pos = summary_section.find(end_marker)
                if end_pos != -1:
                    summary_section = summary_section[:end_pos]
                    break
            
            return summary_section.strip().capitalize()
        
        return ""


# Singleton instance
_resume_parser = None


def get_resume_parser():
    """Get singleton resume parser instance."""
    global _resume_parser
    if _resume_parser is None:
        _resume_parser = ResumeParser()
    return _resume_parser