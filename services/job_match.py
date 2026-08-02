from __future__ import annotations

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class JobMatchService:
    """Compare a resume against a job description using TF-IDF and cosine similarity."""

    TECHNICAL_SKILL_HINTS = {
        "java", "spring boot", "springboot", "rest api", "rest apis", "microservices",
        "python", "flask", "sql", "mysql", "docker", "kubernetes", "aws",
        "azure", "machine learning", "ai", "ml", "javascript", "html", "css",
        "pandas", "numpy", "scikit-learn", "opencv", "spacy", "git"
    }

    def match_resume_to_job(self, resume_text: str, job_description: str) -> dict:
        resume_norm = self._normalize_text(resume_text)
        job_norm = self._normalize_text(job_description)

        vectorizer = TfidfVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform([resume_norm, job_norm])
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

        match_percentage = round(float(max(similarity, 0.0) * 100), 2)

        resume_keywords = self._extract_skill_phrases(resume_text)
        job_keywords = self._extract_skill_phrases(job_description)

        matching_skills = sorted(set(resume_keywords).intersection(job_keywords))
        missing_skills = sorted(set(job_keywords) - set(resume_keywords))
        recommendations = [
            f"Add the missing keyword(s): {', '.join(missing_skills[:5]) or 'No clear keyword gaps detected.'}",
            "Strengthen the resume with measurable impact statements in the project section.",
            "Align your experience bullets with the job’s required cloud, tooling, and delivery responsibilities.",
        ]

        return {
            "match_percentage": match_percentage,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "recommendations": recommendations,
            "recommended_skills": sorted(set(job_keywords) - set(resume_keywords)),
            "improvement_suggestions": recommendations,
        }

    def _normalize_text(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text or "").strip()
        return text.lower()

    def _extract_skill_phrases(self, text: str) -> list[str]:
        cleaned = re.sub(r"[^a-zA-Z0-9\s-]", " ", text or "")
        tokens = [token.strip().lower() for token in cleaned.split() if token.strip()]

        phrases = []
        for candidate in self.TECHNICAL_SKILL_HINTS:
            if candidate in " ".join(tokens):
                phrases.append(candidate)

        for index in range(len(tokens) - 1):
            pair = f"{tokens[index]} {tokens[index + 1]}"
            if pair in self.TECHNICAL_SKILL_HINTS:
                phrases.append(pair)

        return sorted(set(phrases))
