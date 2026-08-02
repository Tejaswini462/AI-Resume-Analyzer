from flask import Blueprint, flash, render_template, request
from flask_login import current_user, login_required

from models import db
from models.job import JobDescription, MatchResult
from models.resume import Resume
from services.ats_score import ATSScoreService
from services.job_match import JobMatchService
from services.parser import ResumeParser
from utils.helper import extract_pdf_text

analysis_bp = Blueprint("analysis", __name__, url_prefix="/analysis")


@analysis_bp.route("/", methods=["GET", "POST"])
@login_required
def analysis():
    resume_id = request.args.get("resume_id", type=int)
    resumes = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.upload_date.desc()).all()
    selected_resume = Resume.query.filter_by(id=resume_id, user_id=current_user.id).first() if resume_id else resumes[0] if resumes else None

    if selected_resume is None:
        return render_template("analysis.html", resume=None, analysis_data=None)

    parser = ResumeParser()
    ats_service = ATSScoreService()

    raw_resume_text = selected_resume.resume_text or extract_pdf_text(selected_resume.file_path)
    parsed_resume = {
        "name": selected_resume.name or parser.parse_resume_text(raw_resume_text)["name"],
        "email": selected_resume.email or parser.parse_resume_text(raw_resume_text)["email"],
        "phone": selected_resume.phone or parser.parse_resume_text(raw_resume_text)["phone"],
        "skills": selected_resume.skills or parser.parse_resume_text(raw_resume_text)["skills"],
        "education": selected_resume.education or parser.parse_resume_text(raw_resume_text)["education"],
        "experience": selected_resume.experience or parser.parse_resume_text(raw_resume_text)["experience"],
        "projects": selected_resume.projects or parser.parse_resume_text(raw_resume_text)["projects"],
        "certifications": selected_resume.certifications or parser.parse_resume_text(raw_resume_text)["certifications"],
    }
    analysis_data = ats_service.calculate_score(parsed_resume)

    return render_template(
        "analysis.html",
        resume=selected_resume,
        analysis_data=analysis_data,
        parsed_resume=parsed_resume,
        resumes=resumes,
    )


@analysis_bp.route("/job-match", methods=["GET", "POST"])
@login_required
def job_match():
    resumes = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.upload_date.desc()).all()
    selected_resume = resumes[0] if resumes else None
    match_result = None

    if request.method == "POST":
        resume_id = request.form.get("resume_id", type=int)
        job_title = request.form.get("job_title", "Custom Job Description").strip()
        job_description = request.form.get("job_description", "").strip()

        if not job_description:
            flash("Please paste a job description.", "danger")
            return render_template("job_match_result.html", resumes=resumes, selected_resume=selected_resume, match_result=None)

        selected_resume = Resume.query.filter_by(id=resume_id, user_id=current_user.id).first() if resume_id else selected_resume

        if selected_resume is None:
            flash("Please upload or choose a resume first.", "danger")
            return render_template("job_match_result.html", resumes=resumes, selected_resume=None, match_result=None)

        resume_text = selected_resume.resume_text or selected_resume.filename
        match_service = JobMatchService()
        match_data = match_service.match_resume_to_job(resume_text, job_description)

        job = JobDescription(title=job_title, description=job_description)
        db.session.add(job)
        db.session.commit()

        result = MatchResult(
            resume_id=selected_resume.id,
            job_id=job.id,
            match_percentage=match_data["match_percentage"],
            matching_skills=", ".join(match_data["matching_skills"]),
            missing_skills=", ".join(match_data["missing_skills"]),
        )
        db.session.add(result)
        db.session.commit()

        match_result = match_data
        match_result["job_title"] = job_title
        match_result["resume_name"] = selected_resume.filename

    return render_template("job_match_result.html", resumes=resumes, selected_resume=selected_resume, match_result=match_result)
