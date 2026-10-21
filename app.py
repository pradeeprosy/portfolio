"""
Activity, Education & Certificate Hub - Web Application Server
Designed for Pradeep Kumar Suresh
"""

import os
import uuid
from datetime import datetime, timezone
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    Response,
    redirect,
    url_for
)
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import database

# Load environment configuration
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'hub-secret-pradeep-2026-key')
app.config['SITE_URL'] = os.getenv('SITE_URL', 'http://localhost:5000').rstrip('/')
ADMIN_PIN = os.getenv('ADMIN_PIN', 'pradeep2026')

# File Upload Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads', 'certificates')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Ensure database tables exist on startup
database.init_db()


def allowed_file(filename):
    """Check if uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_admin_authorized(req_data=None):
    """Check if session is authorized or if correct PIN is provided in payload or form."""
    if session.get('hub_admin'):
        return True

    # Check in JSON payload
    if req_data and isinstance(req_data, dict):
        pin = str(req_data.get('admin_pin', '')).strip()
        if pin and pin == ADMIN_PIN:
            session['hub_admin'] = True
            return True

    # Check in form data
    pin = request.form.get('admin_pin', '').strip()
    if pin and pin == ADMIN_PIN:
        session['hub_admin'] = True
        return True

    # Check in request header
    header_pin = request.headers.get('X-Admin-PIN', '').strip()
    if header_pin and header_pin == ADMIN_PIN:
        session['hub_admin'] = True
        return True

    return False


@app.after_request
def add_cache_headers(response):
    """Ensure HTML pages are not aggressively cached by browsers for instant updates."""
    if response.mimetype == 'text/html':
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response


@app.context_processor
def inject_globals():
    return {
        "current_year": datetime.now(timezone.utc).year,
        "site_url": app.config['SITE_URL']
    }


# -------------------------------------------------------------
# Main Hub View
# -------------------------------------------------------------
@app.route('/')
def home():
    """Main dashboard displaying Education Milestones (10th to College), Certificates, and Live Activity Stream."""
    profile = database.get_profile()
    education_list = database.get_education_list()
    primary_education = database.get_primary_education()
    certificates = database.get_certificates()
    activities = database.get_activities()
    stats = database.get_stats()

    return render_template(
        'index.html',
        profile=profile,
        education_list=education_list,
        education=primary_education,  # Backwards compatibility for hero card
        certificates=certificates,
        activities=activities,
        stats=stats
    )


# -------------------------------------------------------------
# Authentication APIs
# -------------------------------------------------------------
@app.route('/api/auth/verify', methods=['POST'])
def api_auth_verify():
    """Verify admin PIN to unlock in-browser editing controls."""
    req_data = request.get_json(silent=True) or {}
    pin = req_data.get('pin', '').strip()

    if pin and pin == ADMIN_PIN:
        session['hub_admin'] = True
        return jsonify({"success": True, "message": "Admin mode unlocked!"}), 200

    return jsonify({"success": False, "message": "Invalid Admin PIN. Please try again."}), 401


@app.route('/api/auth/logout', methods=['POST'])
def api_auth_logout():
    """Lock editing mode and clear admin session."""
    session.pop('hub_admin', None)
    return jsonify({"success": True, "message": "Admin session locked."}), 200


@app.route('/api/auth/status')
def api_auth_status():
    """Check if current browser session has admin authorization."""
    return jsonify({"authenticated": bool(session.get('hub_admin'))})


# -------------------------------------------------------------
# Education Management APIs (10th to College Multi-milestones)
# -------------------------------------------------------------
@app.route('/api/education', methods=['GET', 'POST'])
def api_education():
    """Fetch education list or create / update an education record."""
    if request.method == 'GET':
        return jsonify(database.get_education_list())

    req_data = request.get_json(silent=True) or request.form.to_dict()
    if not is_admin_authorized(req_data):
        return jsonify({"success": False, "message": "Admin PIN required to modify education details."}), 401

    institution = req_data.get('institution', '').strip()
    degree = req_data.get('degree', '').strip()
    if not institution or not degree:
        return jsonify({"success": False, "message": "Institution and degree/title are required."}), 400

    edu_id = req_data.get('id')
    if edu_id and str(edu_id).strip() and str(edu_id).lower() != 'new':
        updated = database.update_education(int(edu_id), req_data)
        message = "Education milestone updated successfully!"
        target_edu = updated
    else:
        new_edu = database.add_education(req_data)
        message = "New education milestone added successfully!"
        target_edu = new_edu

    return jsonify({
        "success": True,
        "message": message,
        "education": target_edu,
        "education_list": database.get_education_list(),
        "primary_education": database.get_primary_education(),
        "stats": database.get_stats()
    }), 200


@app.route('/api/education/<int:edu_id>', methods=['GET', 'PUT', 'DELETE'])
def api_education_detail(edu_id):
    """Retrieve, update, or delete a specific education record."""
    if request.method == 'GET':
        edu = database.get_education_by_id(edu_id)
        if edu:
            return jsonify(edu)
        return jsonify({"error": "Education milestone not found."}), 404

    req_data = request.get_json(silent=True) or request.form.to_dict()
    if not is_admin_authorized(req_data):
        return jsonify({"success": False, "message": "Admin authorization required."}), 401

    if request.method == 'DELETE':
        deleted = database.delete_education(edu_id)
        if deleted:
            return jsonify({
                "success": True,
                "message": "Education record deleted.",
                "education_list": database.get_education_list(),
                "primary_education": database.get_primary_education(),
                "stats": database.get_stats()
            }), 200
        return jsonify({"success": False, "message": "Education record not found."}), 404

    # PUT
    updated = database.update_education(edu_id, req_data)
    if updated:
        return jsonify({
            "success": True,
            "message": "Education record updated successfully!",
            "education": updated,
            "education_list": database.get_education_list(),
            "primary_education": database.get_primary_education(),
            "stats": database.get_stats()
        }), 200

    return jsonify({"success": False, "message": "Failed to update education record."}), 500


# -------------------------------------------------------------
# Certificate Management & Upload APIs
# -------------------------------------------------------------
@app.route('/api/certificates', methods=['GET', 'POST'])
def api_certificates():
    """Fetch certificates or upload / register a new certificate."""
    if request.method == 'GET':
        category = request.args.get('category')
        search = request.args.get('search')
        return jsonify(database.get_certificates(category=category, search=search))

    # Support JSON or multipart/form-data for file uploads
    is_form = bool(request.form)
    data = request.form.to_dict() if is_form else (request.get_json(silent=True) or {})

    if not is_admin_authorized(data):
        return jsonify({"success": False, "message": "Admin PIN required to upload certificates."}), 401

    title = data.get('title', '').strip()
    issuer = data.get('issuer', '').strip()
    if not title or not issuer:
        return jsonify({"success": False, "message": "Certificate title and issuing organization are required."}), 400

    file_path = ''
    file_name = ''

    # Handle file upload if present
    if 'certificate_file' in request.files:
        file = request.files['certificate_file']
        if file and file.filename and file.filename.strip():
            if not allowed_file(file.filename):
                return jsonify({
                    "success": False,
                    "message": "Invalid file format. Allowed formats: PDF, PNG, JPG, JPEG, WEBP."
                }), 400

            clean_name = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex[:8]}_{clean_name}"
            dest_disk_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(dest_disk_path)

            file_path = f"/static/uploads/certificates/{unique_filename}"
            file_name = clean_name

    cert_id = data.get('id') or data.get('cert_id')
    if cert_id and str(cert_id).strip() and str(cert_id).lower() != 'new':
        # Update existing
        update_payload = {
            "title": title,
            "issuer": issuer,
            "issue_date": data.get('issue_date', '').strip(),
            "category": data.get('category', 'Technical Certification').strip(),
            "credential_id": data.get('credential_id', '').strip(),
            "credential_url": data.get('credential_url', '').strip(),
            "description": data.get('description', '').strip()
        }
        if file_path:
            update_payload['file_path'] = file_path
            update_payload['file_name'] = file_name

        updated = database.update_certificate(cert_id, update_payload)
        return jsonify({
            "success": True,
            "message": "Certificate updated successfully!",
            "certificate": updated,
            "stats": database.get_stats()
        }), 200

    # Add new
    new_cert = database.add_certificate(
        title=title,
        issuer=issuer,
        issue_date=data.get('issue_date', '').strip(),
        category=data.get('category', 'Technical Certification').strip(),
        credential_id=data.get('credential_id', '').strip(),
        credential_url=data.get('credential_url', '').strip(),
        file_path=file_path,
        file_name=file_name,
        description=data.get('description', '').strip()
    )

    return jsonify({
        "success": True,
        "message": "Certificate uploaded & registered successfully!",
        "certificate": new_cert,
        "stats": database.get_stats()
    }), 201


@app.route('/api/certificates/<cert_id>', methods=['GET', 'PUT', 'DELETE'])
def api_certificate_detail(cert_id):
    """Retrieve, update, or delete a specific certificate."""
    if request.method == 'GET':
        cert = database.get_certificate_by_id(cert_id)
        if cert:
            return jsonify(cert)
        return jsonify({"error": "Certificate not found."}), 404

    req_data = request.form.to_dict() if request.form else (request.get_json(silent=True) or {})
    if not is_admin_authorized(req_data):
        return jsonify({"success": False, "message": "Admin authorization required."}), 401

    if request.method == 'DELETE':
        deleted, file_path = database.delete_certificate(cert_id)
        if deleted:
            # Clean up uploaded file from disk if exists
            if file_path and file_path.startswith('/static/uploads/certificates/'):
                rel_file = os.path.basename(file_path)
                disk_path = os.path.join(app.config['UPLOAD_FOLDER'], rel_file)
                if os.path.exists(disk_path):
                    try:
                        os.remove(disk_path)
                    except OSError:
                        pass

            return jsonify({
                "success": True,
                "message": "Certificate deleted successfully.",
                "stats": database.get_stats()
            }), 200
        return jsonify({"success": False, "message": "Certificate not found."}), 404

    # PUT update
    file_path = ''
    file_name = ''
    if 'certificate_file' in request.files:
        file = request.files['certificate_file']
        if file and file.filename and file.filename.strip() and allowed_file(file.filename):
            clean_name = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex[:8]}_{clean_name}"
            dest_disk_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(dest_disk_path)
            file_path = f"/static/uploads/certificates/{unique_filename}"
            file_name = clean_name

    update_payload = dict(req_data)
    if file_path:
        update_payload['file_path'] = file_path
        update_payload['file_name'] = file_name

    updated = database.update_certificate(cert_id, update_payload)
    if updated:
        return jsonify({
            "success": True,
            "message": "Certificate updated successfully!",
            "certificate": updated,
            "stats": database.get_stats()
        }), 200

    return jsonify({"success": False, "message": "Failed to update certificate."}), 500


# -------------------------------------------------------------
# Profile APIs
# -------------------------------------------------------------
@app.route('/api/profile', methods=['GET', 'POST'])
def api_profile():
    """Fetch or update profile details."""
    if request.method == 'GET':
        return jsonify(database.get_profile())

    req_data = request.form.to_dict() if request.form else (request.get_json(silent=True) or {})
    if not is_admin_authorized(req_data):
        return jsonify({"success": False, "message": "Admin PIN required to update profile."}), 401

    if 'profile_avatar' in request.files:
        avatar_file = request.files['profile_avatar']
        if avatar_file and avatar_file.filename and allowed_file(avatar_file.filename):
            avatar_path = os.path.join(BASE_DIR, 'static', 'images', 'profile.jpg')
            avatar_file.save(avatar_path)

    database.update_profile(req_data)
    return jsonify({
        "success": True,
        "message": "Profile updated successfully!",
        "profile": database.get_profile()
    }), 200


# -------------------------------------------------------------
# Activity Stream APIs
# -------------------------------------------------------------
@app.route('/api/activities', methods=['GET', 'POST'])
def api_activities():
    """Fetch activity feed or publish a new live activity update."""
    if request.method == 'GET':
        category = request.args.get('category')
        search = request.args.get('search')
        activities = database.get_activities(category=category, search=search)
        return jsonify(activities)

    req_data = request.get_json(silent=True) or request.form.to_dict()
    if not is_admin_authorized(req_data):
        return jsonify({"success": False, "message": "Admin PIN required to publish activities."}), 401

    title = req_data.get('title', '').strip()
    description = req_data.get('description', '').strip()
    category = req_data.get('category', 'Project Milestone').strip()

    if not title or not description:
        return jsonify({"success": False, "message": "Title and description are required."}), 400

    new_act = database.add_activity(
        title=title,
        category=category,
        date=req_data.get('date', '').strip(),
        description=description,
        link=req_data.get('link', '').strip(),
        link_text=req_data.get('link_text', '').strip(),
        badge=req_data.get('badge', '').strip()
    )

    return jsonify({
        "success": True,
        "message": "Live activity published successfully!",
        "activity": new_act,
        "stats": database.get_stats()
    }), 201


@app.route('/api/activities/<activity_id>', methods=['GET', 'PUT', 'DELETE'])
def api_activity_detail(activity_id):
    """Retrieve, edit, or delete a specific activity update."""
    if request.method == 'GET':
        act = database.get_activity_by_id(activity_id)
        if act:
            return jsonify(act)
        return jsonify({"error": "Activity not found"}), 404

    req_data = request.get_json(silent=True) or request.form.to_dict()
    if not is_admin_authorized(req_data):
        return jsonify({"success": False, "message": "Admin authorization required."}), 401

    if request.method == 'DELETE':
        deleted = database.delete_activity(activity_id)
        if deleted:
            return jsonify({
                "success": True,
                "message": "Activity deleted.",
                "stats": database.get_stats()
            }), 200
        return jsonify({"success": False, "message": "Activity ID not found."}), 404

    # PUT
    updated_act = database.update_activity(activity_id, req_data)
    if updated_act:
        return jsonify({
            "success": True,
            "message": "Activity updated successfully!",
            "activity": updated_act,
            "stats": database.get_stats()
        }), 200

    return jsonify({"success": False, "message": "Failed to update activity."}), 500


@app.route('/api/stats')
def api_stats():
    """Retrieve live statistics counters."""
    return jsonify(database.get_stats())


# -------------------------------------------------------------
# SEO Routes
# -------------------------------------------------------------
@app.route('/robots.txt')
def robots_txt():
    site_url = app.config['SITE_URL']
    content = f"""User-agent: *
Allow: /
Disallow: /api/

Sitemap: {site_url}/sitemap.xml
"""
    return Response(content, mimetype="text/plain")


@app.route('/sitemap.xml')
def sitemap_xml():
    site_url = app.config['SITE_URL']
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{site_url}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>"""
    return Response(xml, mimetype="application/xml")


# -------------------------------------------------------------
# Error Handlers
# -------------------------------------------------------------
@app.errorhandler(413)
def file_too_large(e):
    return jsonify({"success": False, "message": "File is too large. Maximum upload size is 16MB."}), 413


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
