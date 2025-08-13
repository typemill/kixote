from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
from app.common.decorators import auto_add_client_if_needed, rate_limit, request_limit
from weasyprint import HTML, CSS
import tempfile
import os

weasyprint_bp = Blueprint("weasyprint", __name__)

@weasyprint_bp.route("/pdf", methods=["POST"])
@jwt_required()
@auto_add_client_if_needed
@request_limit("5/Minutes")
@rate_limit(cost=5)
def generate_pdf():
    data = request.get_json()
    html_content = data.get("html") if data else None
    css_content = data.get("css")
    metadata = data.get("metadata")
    zoom = data.get("zoom")
    base_url = data.get("base_url")
    presentational_hints = data.get("presentational_hints", False)
    optimize_size = data.get("optimize_size")  # e.g., ["images", "fonts"]
    filename = data.get("filename", "output.pdf")

    # --- Input validation ---
    if not html_content or not isinstance(html_content, str):
        return jsonify({"error": "Missing or invalid 'html' in request body"}), 400

    if css_content and not (isinstance(css_content, str) or isinstance(css_content, list)):
        return jsonify({"error": "'css' must be a string or a list of strings"}), 400

    if metadata and not isinstance(metadata, dict):
        return jsonify({"error": "'metadata' must be a dictionary"}), 400

    if zoom and not (isinstance(zoom, int) or isinstance(zoom, float)):
        return jsonify({"error": "'zoom' must be a number"}), 400

    if base_url and not isinstance(base_url, str):
        return jsonify({"error": "'base_url' must be a string"}), 400

    if optimize_size and not (isinstance(optimize_size, list) or isinstance(optimize_size, tuple)):
        return jsonify({"error": "'optimize_size' must be a list or tuple"}), 400

    if filename and not isinstance(filename, str):
        return jsonify({"error": "'filename' must be a string"}), 400

    # --- End input validation ---

    try:
        html_obj = HTML(string=html_content, base_url=base_url)
        # Support multiple CSS files
        stylesheets = None
        if css_content:
            if isinstance(css_content, list):
                stylesheets = [CSS(string=css) for css in css_content]
            else:
                stylesheets = [CSS(string=css_content)]

        pdf_kwargs = {}
        if metadata:
            pdf_kwargs["metadata"] = metadata
        if zoom:
            pdf_kwargs["zoom"] = zoom
        if presentational_hints:
            pdf_kwargs["presentational_hints"] = True
        if optimize_size:
            pdf_kwargs["optimize_size"] = tuple(optimize_size)

        attachments = data.get("attachments")
        if attachments:
            if not isinstance(attachments, list):
                return jsonify({"error": "'attachments' must be a list"}), 400
            try:
                pdf_kwargs["attachments"] = [
                    (a["filename"], a["content"].encode())
                    for a in attachments
                    if isinstance(a, dict) and "filename" in a and "content" in a
                ]
            except Exception:
                return jsonify({"error": "Invalid 'attachments' format"}), 400

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            html_obj.write_pdf(
                tmp.name,
                stylesheets=stylesheets,
                **pdf_kwargs
            )
            tmp_path = tmp.name

        response = send_file(tmp_path, as_attachment=True, download_name=filename, mimetype="application/pdf")

        @response.call_on_close
        def cleanup():
            try:
                os.remove(tmp_path)
            except Exception:
                pass

        return response
    except Exception as e:
        return jsonify({"error": "PDF generation failed", "details": str(e)}), 500