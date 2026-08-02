from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from models import db
from models.resume import Resume
from services.ats_score import ATSScoreService
from services.parser import ResumeParser
from utils.helper import allowed_file, extract_pdf_text, save_uploaded_file, validate_pdf_file

upload_bp = Blueprint("upload", __name__, url_prefix="/upload")


@upload_bp.route("/", methods=["GET", "POST"])
@login_required
def upload_resume():
    if request.method == "POST":
        file = request.files.get("resume")

        if not file or file.filename == "":
            flash("Please choose a PDF file.", "danger")
            return render_template("upload.html")

        if not allowed_file(file.filename, current_app.config["ALLOWED_EXTENSIONS"]):
            flash("Only PDF files are allowed.", "danger")
            return render_template("upload.html")

        if file.content_length and file.content_length > current_app.config["MAX_CONTENT_LENGTH"]:
            flash("File size exceeds the allowed limit.", "danger")
            return render_template("upload.html")

        is_valid_pdf, error_message = validate_pdf_file(file)
        if not is_valid_pdf:
            flash(error_message, "danger")
            return render_template("upload.html")

        file_path = save_uploaded_file(file)
        if not file_path:
            flash("Upload failed. Please try again.", "danger")
            return render_template("upload.html")

        resume_text = extract_pdf_text(file_path)
        parser = ResumeParser()
        parsed_resume = parser.parse_resume_text(resume_text)
        analysis_data = ATSScoreService().calculate_score(parsed_resume)

        resume = Resume(
            user_id=current_user.id,
            filename=secure_filename(file.filename),
            file_path=file_path,
            resume_text=resume_text,
            name=parsed_resume.get("name", ""),
            email=parsed_resume.get("email", ""),
            phone=parsed_resume.get("phone", ""),
            skills=parsed_resume.get("skills", ""),
            education=parsed_resume.get("education", ""),
            experience=parsed_resume.get("experience", ""),
            projects=parsed_resume.get("projects", ""),
            certifications=parsed_resume.get("certifications", ""),
            ats_score=float(analysis_data.get("overall_score", 0)),
        )
        db.session.add(resume)
        db.session.commit()

        flash("Resume uploaded successfully.", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("upload.html")
