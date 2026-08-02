from __future__ import annotations

from . import db


class JobDescription(db.Model):
    """Represents a job description stored for match comparison."""

    __tablename__ = "job_descriptions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)


class MatchResult(db.Model):
    """Stores the result of comparing a resume with a job description."""

    __tablename__ = "match_results"

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("job_descriptions.id"), nullable=False)
    match_percentage = db.Column(db.Float, nullable=False)
    matching_skills = db.Column(db.Text, nullable=True)
    missing_skills = db.Column(db.Text, nullable=True)
