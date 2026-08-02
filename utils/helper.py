from __future__ import annotations

from pathlib import Path

import fitz
from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


def extract_pdf_text(pdf_path: str) -> str:
    """Extract plain text from a PDF file using PyMuPDF."""
    if not pdf_path:
        return ""

    try:
        with fitz.open(pdf_path) as document:
            pages = [page.get_text("text") for page in document]
    except Exception:
        return ""

    return "\n".join(page.strip() for page in pages if page and page.strip())


def allowed_file(filename: str, allowed_extensions: set[str]) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def validate_pdf_file(file: FileStorage) -> tuple[bool, str | None]:
    file.stream.seek(0)
    file_bytes = file.stream.read()
    file.stream.seek(0)

    if not file_bytes.startswith(b"%PDF"):
        return False, "Uploaded file is not a valid PDF."

    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as document:
            if document.page_count < 1:
                return False, "The uploaded PDF appears to be empty."
    except Exception:
        return False, "The uploaded file could not be opened as a valid PDF."

    return True, None


def save_uploaded_file(file: FileStorage, upload_folder: str | None = None) -> str | None:
    if upload_folder is None:
        upload_folder = current_app.config["UPLOAD_FOLDER"]

    upload_path = Path(upload_folder)
    upload_path.mkdir(parents=True, exist_ok=True)

    original_name = secure_filename(file.filename)
    if not original_name:
        return None

    filename = original_name
    counter = 1
    while (upload_path / filename).exists():
        stem = Path(original_name).stem
        suffix = Path(original_name).suffix
        filename = f"{stem}_{counter}{suffix}"
        counter += 1

    destination = upload_path / filename
    file.stream.seek(0)
    file.save(destination)

    return str(destination)
