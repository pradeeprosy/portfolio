"""
Activity & Academic Hub - Web Application Server
Designed for Pradeep Kumar Suresh
"""

import os
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
from dotenv import load_dotenv
import database

# Load environment configuration
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'hub-secret-pradeep-2026-key')
app.config['SITE_URL'] = os.getenv('SITE_URL', 'http://localhost:5000').rstrip('/')
ADMIN_PIN = os.getenv('ADMIN_PIN', 'pradeep2026')

# Ensure database tables exist on startup
database.init_db()


def is_admin_authorized(req_data=None):
    """Check if session is authorized or if correct PIN is provided in payload."""
    if session.get('hub_admin'):
        return True
    if req_data and isinstance(req_data, dict):
        pin = req_data.get('admin_pin', '').strip()
        if pin and pin == ADMIN_PIN:
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
    """Main dashboard displaying Academic Overview and Live Activity Stream."""
    profile = database.get_profile()
    education = database.get_education()
    activities = database.get_activities()
    stats = database.get_stats()
    return render_template(
        'index.html',
        profile=profile,
        education=education,
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
# Education Management APIs
# -------------------------------------------------------------
@app.route('/api/education', methods=['GET', 'POST'])
def api_education():
    """Fetch or update education credentials."""
    if request.method == 'GET':
        return jsonify(database.get_education())

    req_data = request.get_json(silent=True) or {}
    if not is_admin_authorized(req_data):
        return jsonify({"success": False, "message": "Admin PIN required to update education details."}), 401

    institution = req_data.get('institution', '').strip()
    degree = req_data.get('degree', '').strip()
    if not institution or not degree:
        return jsonify({"success": False, "message": "Institution and degree are required."}), 400

    database.update_education(req_data)
    return jsonify({
        "success": True,
        "message": "Education details updated successfully!",
        "education": database.get_education()
    }), 200


# -------------------------------------------------------------
# Profile APIs
# -------------------------------------------------------------
@app.route('/api/profile', methods=['GET', 'POST'])
def api_profile():
    """Fetch or update profile details."""
    if request.method == 'GET':
        return jsonify(database.get_profile())

    req_data = request.get_json(silent=True) or {}
    if not is_admin_authorized(req_data):
        return jsonify({"success": False, "message": "Admin PIN required to update profile."}), 401

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

    req_data = request.get_json(silent=True) or {}
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

    req_data = request.get_json(silent=True) or {}
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
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
