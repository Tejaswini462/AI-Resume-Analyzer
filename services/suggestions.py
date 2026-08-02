from __future__ import annotations

from typing import List


class SuggestionService:
    """Generate high-level improvement suggestions for resume quality."""

    def build_suggestions(self, parsed_resume: dict) -> List[str]:
        suggestions = []

        if not parsed_resume.get("skills"):
            suggestions.append("Add missing technical skills relevant to the target role.")

        if not parsed_resume.get("projects"):
            suggestions.append("Improve project descriptions with measurable outcomes and impact.")

        if not parsed_resume.get("certifications"):
            suggestions.append("Add relevant certifications to strengthen your credibility.")

        suggestions.append("Use consistent formatting and a stronger experience timeline.")
        return suggestions
