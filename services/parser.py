from __future__ import annotations

import re
from typing import Dict


class ResumeParser:
    """Professional Resume Parser"""

    SECTION_HEADINGS = {
        "skills": [
            "skills",
            "technical skills",
            "core skills",
            "technical expertise",
        ],
        "education": [
            "education",
            "academic details",
            "academic qualification",
            "educational qualification",
            "educational background",
            "qualification",
        ],
        "experience": [
            "experience",
            "professional experience",
            "work experience",
            "internship",
            "internships",
        ],
        "projects": [
            "projects",
            "project",
            "academic projects",
            "personal projects",
        ],
        "certifications": [
            "certifications",
            "certification",
            "achievements & certifications",
            "achievements",
            "licenses",
        ],
    }

    SKILL_DATABASE = [
        "Python",
        "Java",
        "C",
        "C++",
        "JavaScript",
        "HTML",
        "CSS",
        "Bootstrap",
        "React",
        "Angular",
        "Vue",
        "Node.js",
        "Express",
        "Flask",
        "Django",
        "Spring",
        "Spring Boot",
        "SQL",
        "MySQL",
        "PostgreSQL",
        "SQLite",
        "MongoDB",
        "Git",
        "GitHub",
        "Docker",
        "AWS",
        "Azure",
        "Google Cloud",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn",
        "NumPy",
        "Pandas",
        "OpenCV",
        "spaCy",
        "REST API",
        "Data Structures",
        "Algorithms",
        "DBMS",
        "OOP",
        "CN",
    ]

    def parse_resume_text(self, text: str) -> Dict[str, str]:

        raw_text = re.sub(r"\r", "\n", text or "")
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        flat_text = re.sub(r"\s+", " ", raw_text)

        return {
            "name": self._extract_name(lines),
            "email": self._extract_email(flat_text),
            "phone": self._extract_phone(flat_text),
            "skills": self._extract_skills(raw_text),
            "education": self._extract_education(raw_text),
            "experience": self._extract_experience(raw_text),
            "projects": self._extract_projects(raw_text),
            "certifications": self._extract_certifications(raw_text),
        }

    def _extract_name(self, lines):

        ignore_words = [
            "objective",
            "summary",
            "profile",
            "resume",
            "curriculum vitae",
            "computer science",
            "student",
            "skills",
            "education",
            "experience",
            "projects",
            "certifications",
        ]

        for line in lines[:8]:

            line = line.strip()

            if not line:
                continue

            if "@" in line:
                continue

            if re.search(r"\d", line):
                continue

            if any(word in line.lower() for word in ignore_words):
                continue

            if len(line.split()) < 2 or len(line.split()) > 4:
                continue

            if line.isupper():
                return line.title()

            return line.title()

        return ""

    def _extract_email(self, text):

        match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text,
        )

        return match.group() if match else ""

    def _extract_phone(self, text):

        match = re.search(
            r"(?:\+91[- ]?)?[6-9]\d{9}",
            text,
        )

        return match.group() if match else ""

    def _extract_skills(self, text):

        found = []

        lower = text.lower()

        for skill in self.SKILL_DATABASE:

            if skill.lower() in lower:
                found.append(skill)

        return ", ".join(sorted(set(found)))

    def _extract_education(self, text):

        return self._extract_section(text, "education")

    def _extract_experience(self, text):

        return self._extract_section(text, "experience")

    def _extract_projects(self, text):

        return self._extract_section(text, "projects")

    def _extract_certifications(self, text):

        return self._extract_section(text, "certifications")

    def _extract_section(self, text, section_name):

        lines = [line.strip() for line in text.splitlines() if line.strip()]

        headings = self.SECTION_HEADINGS[section_name]

        all_headings = []

        for values in self.SECTION_HEADINGS.values():
            all_headings.extend(values)

        collecting = False

        section = []

        for line in lines:

            lower = line.lower()

            if not collecting:

                for heading in headings:

                    if lower == heading or lower.startswith(heading + ":"):

                        collecting = True

                        remaining = (
                            line[len(heading):]
                            .replace(":", "")
                            .strip()
                        )

                        if remaining:
                            section.append(remaining)

                        break

            else:

                stop = False

                for heading in all_headings:

                    if lower == heading or lower.startswith(heading + ":"):

                        stop = True
                        break

                if stop:
                    break

                section.append(line)

        return self._clean_section(" ".join(section))

    def _clean_section(self, text):

        return re.sub(r"\s+", " ", text).strip()