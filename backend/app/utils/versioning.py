"""
Application Versioning and Release Management
"""
from datetime import datetime
from typing import Dict, List

class AppVersion:
    """Application version management"""
    
    # Current version
    MAJOR = 1
    MINOR = 0
    PATCH = 0
    BUILD = datetime.now().strftime("%Y%m%d")
    
    @classmethod
    def get_version_string(cls) -> str:
        """Get full version string"""
        return f"v{cls.MAJOR}.{cls.MINOR}.{cls.PATCH}+{cls.BUILD}"
    
    @classmethod
    def get_short_version(cls) -> str:
        """Get short version (without build)"""
        return f"v{cls.MAJOR}.{cls.MINOR}.{cls.PATCH}"
    
    @classmethod
    def get_build_info(cls) -> Dict[str, str]:
        """Get detailed build information"""
        return {
            "version": cls.get_version_string(),
            "short_version": cls.get_short_version(),
            "build_date": datetime.now().isoformat(),
            "environment": "production",
            "platform": "web"
        }

class Changelog:
    """Application changelog management"""
    
    ENTRIES = [
        {
            "version": "1.0.0",
            "date": "2024-01-15",
            "type": "release",
            "changes": [
                "Initial production release",
                "Core interview functionality",
                "Multi-agent architecture",
                "Resume analysis integration",
                "Structured evaluation system"
            ]
        },
        {
            "version": "1.0.0",
            "date": "2024-01-15",
            "type": "enhancement",
            "changes": [
                "Added production-ready session management",
                "Implemented navigation safety guards",
                "Enhanced error handling with user-friendly messages",
                "Added comprehensive logging system",
                "Created transparent data usage disclosure",
                "Implemented graceful failure recovery"
            ]
        },
        {
            "version": "1.0.0",
            "date": "2024-01-15",
            "type": "fix",
            "changes": [
                "Fixed resume projects type handling",
                "Resolved session state persistence issues",
                "Improved API error resilience",
                "Enhanced loading state management"
            ]
        }
    ]
    
    @classmethod
    def get_latest_changes(cls, limit: int = 5) -> List[Dict]:
        """Get latest changelog entries"""
        return cls.ENTRIES[:limit]
    
    @classmethod
    def get_changelog_markdown(cls) -> str:
        """Get formatted changelog as markdown"""
        markdown = "# Changelog\n\n"
        
        for entry in cls.ENTRIES:
            markdown += f"## {entry['version']} - {entry['date']}\n"
            
            if entry['type'] == 'release':
                markdown += "**Initial Release**\n\n"
            
            for change in entry['changes']:
                markdown += f"- {change}\n"
            markdown += "\n"
        
        return markdown

class AppBranding:
    """Application branding and ownership information"""
    
    NAME = "AI Interview Agent"
    TAGLINE = "Master Your Technical Interviews"
    OWNER = "Interview Agent Team"
    COPYRIGHT_YEAR = datetime.now().year
    
    @classmethod
    def get_branding_info(cls) -> Dict[str, str]:
        """Get complete branding information"""
        return {
            "name": cls.NAME,
            "tagline": cls.TAGLINE,
            "owner": cls.OWNER,
            "version": AppVersion.get_version_string(),
            "copyright": f"© {cls.COPYRIGHT_YEAR} {cls.OWNER}",
            "description": "An AI-powered interview preparation platform designed to help you master technical interviews through realistic practice sessions and detailed feedback."
        }
    
    @classmethod
    def get_footer_text(cls) -> str:
        """Get footer text with version and copyright"""
        return f"{cls.NAME} {AppVersion.get_short_version()} | {cls.COPYRIGHT_YEAR} {cls.OWNER}"

# Convenience functions
def get_app_version() -> str:
    """Get current application version"""
    return AppVersion.get_version_string()

def get_short_version() -> str:
    """Get short version string"""
    return AppVersion.get_short_version()

def get_changelog(limit: int = 5) -> List[Dict]:
    """Get recent changelog entries"""
    return Changelog.get_latest_changes(limit)

def get_branding() -> Dict[str, str]:
    """Get complete branding information"""
    return AppBranding.get_branding_info()

def get_footer() -> str:
    """Get footer text"""
    return AppBranding.get_footer_text()