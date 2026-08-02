from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.resume import Resume


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
def dashboard():
    resumes = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.upload_date.desc()).all()
    latest_resume = resumes[0] if resumes else None
    latest_score = latest_resume.ats_score if latest_resume else 0
    if latest_resume and latest_resume.skills:
        skills_found=len([
            skill.strip()
            for skill in latest_resume.skills.split(",")
            if skill.strip()
        ])
    else:
        skills_found=0
    return render_template(
        "dashboard.html",
        resumes=resumes,
        latest_score=latest_score,
        skills_found=skills_found,
        total_uploaded=len(resumes),
    )
