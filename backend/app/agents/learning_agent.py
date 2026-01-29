"""
Learning Material Agent for generating preparation content
"""
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.utils.logging_config import get_logger
import json

logger = get_logger(__name__)


class LearningAgent(BaseAgent):
    """Agent for generating multi-modal learning materials"""

    def __init__(self):
        super().__init__("LearningAgent")

    async def execute(self, user_profile: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate learning materials"""
        try:
            logger.info("Generating learning materials")

            experience_level = user_profile.get("experience_level", "Junior")
            available_hours = user_profile.get("available_hours", 10)
            skills = research_data.get("required_skills", [])
            technologies = research_data.get("technologies", [])

            materials = []

            # Generate text materials
            for skill in skills[:5]:
                text_material = await self.generate_text_material(skill, experience_level)
                if text_material:
                    materials.append(text_material)

            # Generate visual concepts
            for tech in technologies[:3]:
                visual_material = await self.generate_visual_concepts(tech)
                if visual_material:
                    materials.append(visual_material)

            # Curate resources
            resources = await self.curate_resources(skills[:3])
            if resources:
                materials.extend(resources)

            # Rank and adapt
            ranked_materials = self._rank_and_adapt(materials, available_hours)

            return {
                "success": True,
                "materials": ranked_materials,
                "total_materials": len(ranked_materials)
            }

        except Exception as e:
            logger.error(f"Failed to generate learning materials: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "materials": []
            }

    async def generate_text_material(self, topic: str, experience_level: str) -> Dict[str, Any]:
        """Generate text explanation material"""
        try:
            prompt = f"""
            Generate a concise explanation for {experience_level} level:
            
            Topic: {topic}
            
            Provide:
            1. Brief overview (2-3 sentences)
            2. Key concepts (3-5 points)
            3. Practical example
            4. Common pitfalls
            
            Format as JSON:
            {{
                "topic": "{topic}",
                "overview": "...",
                "key_concepts": ["concept1", "concept2"],
                "example": "...",
                "pitfalls": ["pitfall1", "pitfall2"]
            }}
            """

            response = await self.call_llm(
                prompt,
                system_message="You are an expert educator creating learning materials.",
                temperature=0.6,
                max_tokens=1000
            )

            data = self._extract_json(response)
            if data:
                data["content_type"] = "text"
                data["relevance_score"] = 9.0
                data["difficulty_level"] = experience_level
                return data
            return None

        except Exception as e:
            logger.error(f"Failed to generate text material for {topic}: {str(e)}")
            return None

    async def generate_visual_concepts(self, technology: str) -> Dict[str, Any]:
        """Generate visual/diagram concepts"""
        try:
            prompt = f"""
            Create a visual learning concept for: {technology}
            
            Describe in ASCII art or text format:
            1. Architecture diagram description
            2. Component relationships
            3. Data flow
            4. Key visual points
            
            Format as JSON:
            {{
                "technology": "{technology}",
                "concept_title": "...",
                "description": "...",
                "visual_points": ["point1", "point2"]
            }}
            """

            response = await self.call_llm(
                prompt,
                system_message="You are a technical educator creating visual learning materials.",
                temperature=0.6,
                max_tokens=800
            )

            data = self._extract_json(response)
            if data:
                data["content_type"] = "image"
                data["relevance_score"] = 8.5
                data["difficulty_level"] = "Medium"
                return data
            return None

        except Exception as e:
            logger.error(f"Failed to generate visual for {technology}: {str(e)}")
            return None

    async def curate_resources(self, skills: List[str]) -> List[Dict[str, Any]]:
        """Curate external resources"""
        try:
            resources = []
            for skill in skills:
                prompt = f"""
                Suggest 3 high-quality learning resources for: {skill}
                
                Provide as JSON array:
                [
                    {{"type": "article|video|course", "title": "...", "url": "https://...", "description": "..."}},
                    ...
                ]
                """

                response = await self.call_llm(
                    prompt,
                    system_message="You are a learning resource curator with knowledge of best educational materials.",
                    temperature=0.6,
                    max_tokens=800
                )

                resource_list = self._extract_json(response)
                if isinstance(resource_list, list):
                    for r in resource_list:
                        r["content_type"] = "link"
                        r["relevance_score"] = 8.0
                        resources.append(r)

            return resources

        except Exception as e:
            logger.error(f"Failed to curate resources: {str(e)}")
            return []

    def _rank_and_adapt(self, materials: List[Dict[str, Any]], available_hours: float) -> List[Dict[str, Any]]:
        """Rank materials by relevance and adapt to time constraints"""
        try:
            # Sort by relevance score
            sorted_materials = sorted(
                materials,
                key=lambda x: x.get("relevance_score", 0),
                reverse=True
            )

            # Estimate time per material (in hours)
            time_per_material = {
                "text": 0.5,
                "image": 0.25,
                "video": 1.0,
                "link": 0.75
            }

            # Select materials based on available time
            selected_materials = []
            total_time = 0

            for material in sorted_materials:
                material_time = time_per_material.get(material.get("content_type"), 0.5)
                if total_time + material_time <= available_hours:
                    selected_materials.append(material)
                    total_time += material_time

            logger.info(f"Selected {len(selected_materials)} materials for {available_hours} hours")
            return selected_materials

        except Exception as e:
            logger.error(f"Error ranking materials: {str(e)}")
            return materials

    def _extract_json(self, response: str) -> Any:
        """Extract JSON from response"""
        try:
            import re
            # Try to find JSON in the response
            json_match = re.search(r'[\{\[].*[\}\]]', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return None
        except (json.JSONDecodeError, ValueError):
            logger.warning("Failed to extract JSON from learning material")
            return None
