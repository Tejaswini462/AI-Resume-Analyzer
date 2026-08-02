from __future__ import annotations

from typing import Dict


class ATSScoreService:
    """Professional ATS Resume Scoring Service"""

    def calculate_score(self, parsed_resume: Dict[str, str]) -> Dict[str, object]:

        text = " ".join(
            str(parsed_resume.get(field, ""))
            for field in [
                "name",
                "email",
                "phone",
                "skills",
                "education",
                "experience",
                "projects",
                "certifications",
            ]
        )

        text_length = len(text.strip())

        # -----------------------------
        # Contact Information (10)
        # -----------------------------
        contact_score = 0

        if parsed_resume.get("email"):
            contact_score += 5

        if parsed_resume.get("phone"):
            contact_score += 5

        # -----------------------------
        # Skills (20)
        # -----------------------------
        skills = parsed_resume.get("skills", "")

        skill_count = len(
            [skill for skill in skills.split(",") if skill.strip()]
        )

        if skill_count >= 15:
            skills_score = 20
        elif skill_count >= 10:
            skills_score = 18
        elif skill_count >= 6:
            skills_score = 15
        elif skill_count >= 3:
            skills_score = 10
        else:
            skills_score = 5

        # -----------------------------
        # Education (15)
        # -----------------------------
        education = parsed_resume.get("education", "")

        if education:
            education_score = 15
        else:
            education_score = 0

        # -----------------------------
        # Experience (20)
        # -----------------------------
        experience = parsed_resume.get("experience", "")

        if len(experience) >= 400:
            experience_score = 20
        elif len(experience) >= 200:
            experience_score = 17
        elif experience:
            experience_score = 12
        else:
            experience_score = 0

        # -----------------------------
        # Projects (10)
        # -----------------------------
        projects = parsed_resume.get("projects", "")

        if len(projects) >= 300:
            project_score = 10
        elif len(projects) >= 120:
            project_score = 8
        elif projects:
            project_score = 5
        else:
            project_score = 0

        # -----------------------------
        # Certifications (10)
        # -----------------------------
        certifications = parsed_resume.get("certifications", "")

        if len(certifications) >= 100:
            cert_score = 10
        elif certifications:
            cert_score = 7
        else:
            cert_score = 0

        # -----------------------------
        # Resume Length (10)
        # -----------------------------
        if text_length >= 1800:
            length_score = 10
        elif text_length >= 1200:
            length_score = 8
        elif text_length >= 700:
            length_score = 6
        else:
            length_score = 3

        # -----------------------------
        # Formatting (5)
        # -----------------------------
        formatting_score = 5 if parsed_resume.get("name") else 2

        total_score = (
            contact_score
            + skills_score
            + education_score
            + experience_score
            + project_score
            + cert_score
            + length_score
            + formatting_score
        )

        # -----------------------------
        # Realistic deductions
        # -----------------------------
        deductions = 0

        if skill_count < 10:
            deductions += 2

        if len(projects) < 200:
            deductions += 2

        if len(experience) < 250:
            deductions += 2

        if not certifications:
            deductions += 3

        overall_score = max(60, min(total_score - deductions, 96))

        # -----------------------------
        # Strengths & Weaknesses
        # -----------------------------
        strengths = []
        weaknesses = []

        if contact_score == 10:
            strengths.append("Contact information is complete.")

        if skill_count >= 10:
            strengths.append("Strong technical skill set.")
        else:
            weaknesses.append("Add more technical skills relevant to the job.")

        if education:
            strengths.append("Education section is well structured.")
        else:
            weaknesses.append("Education section is missing.")

        if experience:
            strengths.append("Experience section is present.")
        else:
            weaknesses.append("Add internship or work experience.")

        if projects:
            strengths.append("Projects demonstrate practical knowledge.")
        else:
            weaknesses.append("Include at least two strong projects.")

        if certifications:
            strengths.append("Certifications improve credibility.")
        else:
            weaknesses.append("Include relevant certifications.")

        if text_length < 1000:
            weaknesses.append("Resume content can be more detailed.")

        if overall_score < 90:
            weaknesses.append("Tailor the resume according to the job description.")

        return {
            "overall_score": overall_score,
            "section_scores": {
                "contact_information": contact_score,
                "skills": skills_score,
                "education": education_score,
                "experience": experience_score,
                "projects": project_score,
                "certifications": cert_score,
                "resume_length": length_score,
                "formatting": formatting_score,
            },
            "strengths": strengths,
            "weaknesses": weaknesses,
        }