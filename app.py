"""
Personal Career Portfolio Website - Flask Backend
Candidate: Pradeep Kumar
Role: Computer Science Engineering Student | Python Developer | AI/ML Enthusiast | Full Stack Developer
"""

import os
import re
import json
import smtplib
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory,
    redirect,
    url_for,
    flash,
    Response
)
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-dev-key-change-in-production')
app.config['SITE_URL'] = os.getenv('SITE_URL', 'http://localhost:5000').rstrip('/')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'portfolio.json')
MESSAGES_LOG_FILE = os.path.join(BASE_DIR, 'data', 'contact_messages.json')


def load_portfolio_data():
    """Load and parse data/portfolio.json with error handling and caching fallback."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        app.logger.error(f"Error loading portfolio.json: {e}")
        return {
            "personal": {
                "name": "Pradeep Kumar",
                "title": "Computer Science Engineering Student",
                "tagline": "Building practical technology solutions with Python and modern web technologies.",
                "roles": ["Computer Science Engineering Student", "Python Developer", "AI/ML Enthusiast", "Full Stack Developer"]
            },
            "projects": [],
            "skills": {},
            "about": {},
            "education": [],
            "certifications": [],
            "achievements": [],
            "hackathons_innovation": [],
            "career_journey": []
        }


def validate_email_format(email: str) -> bool:
    """Validate email using regular expression."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email.strip()))


def save_contact_message(name: str, email: str, message: str, user_ip: str) -> bool:
    """Save contact submission to local JSON storage so messages are never lost."""
    os.makedirs(os.path.dirname(MESSAGES_LOG_FILE), exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        "name": name,
        "email": email,
        "message": message,
        "ip_address": user_ip
    }
    
    try:
        messages = []
        if os.path.exists(MESSAGES_LOG_FILE):
            with open(MESSAGES_LOG_FILE, 'r', encoding='utf-8') as f:
                try:
                    messages = json.load(f)
                except json.JSONDecodeError:
                    messages = []
        messages.append(entry)
        with open(MESSAGES_LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2)
        return True
    except Exception as e:
        app.logger.error(f"Error saving message to storage: {e}")
        return False


def send_contact_email(name: str, email: str, message: str) -> bool:
    """Optionally send email via SMTP if configured in environment variables."""
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT', 587)
    smtp_user = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    recipient_email = os.getenv('CONTACT_RECIPIENT_EMAIL')

    if not (smtp_server and smtp_user and smtp_password and recipient_email):
        # SMTP not configured; messages are stored safely in contact_messages.json
        return True

    try:
        port = int(smtp_port)
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Portfolio Message from {name}"
        msg["From"] = smtp_user
        msg["To"] = recipient_email
        msg["Reply-To"] = email

        text_body = (
            f"New message from your portfolio contact form:\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
            f"Message:\n{message}\n"
        )
        msg.attach(MIMEText(text_body, "plain"))

        with smtplib.SMTP(smtp_server, port, timeout=10) as server:
            if os.getenv('SMTP_USE_TLS', 'True').lower() in ('true', '1', 'yes'):
                server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, recipient_email, msg.as_string())
        return True
    except Exception as e:
        app.logger.error(f"SMTP error while sending message: {e}")
        return False


# -------------------------------------------------------------
# Context Processors
# -------------------------------------------------------------
@app.context_processor
def inject_global_data():
    """Inject current year and basic site metadata into all templates."""
    return {
        "current_year": datetime.now(timezone.utc).year,
        "site_url": app.config['SITE_URL']
    }


# -------------------------------------------------------------
# Application Routes
# -------------------------------------------------------------
@app.route('/')
def home():
    """Main single-page portfolio view rendering all sections."""
    data = load_portfolio_data()
    return render_template('index.html', portfolio=data)


@app.route('/projects')
def projects():
    """Projects view: renders main page anchored at projects section."""
    return redirect(url_for('home', _anchor='projects'))


@app.route('/project/<slug>')
def project_detail(slug):
    """Detailed view for an individual project (accessible directly or via modal deep-link)."""
    data = load_portfolio_data()
    all_projects = data.get('projects', [])
    project = next((p for p in all_projects if p.get('slug') == slug or p.get('id') == slug), None)
    
    if not project:
        return render_template('404.html', message=f"Project '{slug}' was not found."), 404
        
    return render_template('project_detail.html', project=project, portfolio=data)


@app.route('/api/projects')
def api_projects():
    """API endpoint returning all projects as JSON."""
    data = load_portfolio_data()
    return jsonify(data.get('projects', []))


@app.route('/api/projects/<slug>')
def api_project_single(slug):
    """API endpoint returning single project details for interactive modals."""
    data = load_portfolio_data()
    all_projects = data.get('projects', [])
    project = next((p for p in all_projects if p.get('slug') == slug or p.get('id') == slug), None)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(project)


@app.route('/resume')
def resume_view():
    """Resume view: redirects to resume section on main page."""
    return redirect(url_for('home', _anchor='resume'))


@app.route('/resume/download')
def resume_download():
    """Download the official PDF resume."""
    resume_dir = os.path.join(BASE_DIR, 'resume')
    filename = 'resume.pdf'
    if not os.path.exists(os.path.join(resume_dir, filename)):
        return render_template('404.html', message="Resume file is currently unavailable."), 404
        
    return send_from_directory(
        resume_dir,
        filename,
        as_attachment=True,
        download_name='Pradeep_Kumar_Resume.pdf'
    )


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Handle contact submissions with validation and spam protection."""
    if request.method == 'GET':
        return redirect(url_for('home', _anchor='contact'))

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json

    if request.is_json:
        req_data = request.get_json()
    else:
        req_data = request.form

    name = req_data.get('name', '').strip()
    email = req_data.get('email', '').strip()
    message = req_data.get('message', '').strip()
    honeypot = req_data.get('website', '').strip()  # Hidden honeypot field for bot detection

    # Honeypot spam trap
    if honeypot:
        if is_ajax:
            return jsonify({"success": True, "message": "Message sent successfully!"}), 200
        flash("Message sent successfully!", "success")
        return redirect(url_for('home', _anchor='contact'))

    # Validation
    errors = []
    if not name or len(name) < 2:
        errors.append("Please provide a valid name (at least 2 characters).")
    if not email or not validate_email_format(email):
        errors.append("Please enter a valid email address.")
    if not message or len(message) < 10:
        errors.append("Please provide a message of at least 10 characters.")

    if errors:
        error_msg = " ".join(errors)
        if is_ajax:
            return jsonify({"success": False, "message": error_msg}), 400
        flash(error_msg, "error")
        return redirect(url_for('home', _anchor='contact'))

    # Save to local storage
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    save_contact_message(name, email, message, user_ip)

    # Dispatch email if SMTP configured
    send_contact_email(name, email, message)

    success_msg = "Thank you! Your message has been received. I will get back to you shortly."
    if is_ajax:
        return jsonify({"success": True, "message": success_msg}), 200

    flash(success_msg, "success")
    return redirect(url_for('home', _anchor='contact'))


# -------------------------------------------------------------
# SEO Routes: robots.txt and sitemap.xml
# -------------------------------------------------------------
@app.route('/robots.txt')
def robots_txt():
    """Serve robots.txt for search engine crawlers."""
    site_url = app.config['SITE_URL']
    content = f"""User-agent: *
Allow: /
Disallow: /api/
Disallow: /resume/download

Sitemap: {site_url}/sitemap.xml
"""
    return Response(content, mimetype="text/plain")


@app.route('/sitemap.xml')
def sitemap_xml():
    """Dynamically generate standard XML sitemap for Google and search engines."""
    data = load_portfolio_data()
    projects_list = data.get('projects', [])
    site_url = app.config['SITE_URL']
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    pages = [
        {"loc": f"{site_url}/", "changefreq": "weekly", "priority": "1.0"},
        {"loc": f"{site_url}/#about", "changefreq": "monthly", "priority": "0.8"},
        {"loc": f"{site_url}/#skills", "changefreq": "monthly", "priority": "0.8"},
        {"loc": f"{site_url}/#projects", "changefreq": "weekly", "priority": "0.9"},
        {"loc": f"{site_url}/#hackathons", "changefreq": "monthly", "priority": "0.8"},
        {"loc": f"{site_url}/#education", "changefreq": "monthly", "priority": "0.7"},
        {"loc": f"{site_url}/#career", "changefreq": "monthly", "priority": "0.7"},
        {"loc": f"{site_url}/#resume", "changefreq": "monthly", "priority": "0.8"},
        {"loc": f"{site_url}/#contact", "changefreq": "monthly", "priority": "0.7"},
    ]

    for p in projects_list:
        slug = p.get('slug')
        if slug:
            pages.append({
                "loc": f"{site_url}/project/{slug}",
                "changefreq": "monthly",
                "priority": "0.85"
            })

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    for page in pages:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{page['loc']}</loc>")
        xml_lines.append(f"    <lastmod>{today}</lastmod>")
        xml_lines.append(f"    <changefreq>{page['changefreq']}</changefreq>")
        xml_lines.append(f"    <priority>{page['priority']}</priority>")
        xml_lines.append("  </url>")

    xml_lines.append('</urlset>')

    return Response("\n".join(xml_lines), mimetype="application/xml")


# -------------------------------------------------------------
# Error Handlers
# -------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', message="The requested page could not be found."), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('404.html', message="An internal server error occurred."), 500


if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
