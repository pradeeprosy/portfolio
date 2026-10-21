"""
Database Engine & Persistence Layer for Activity, Education & Certificate Hub
Uses Python standard sqlite3 for reliable, zero-dependency persistence.
Designed for Pradeep Kumar Suresh
"""

import os
import sqlite3
import uuid
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'hub.db')
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads', 'certificates')


def get_db_connection():
    """Create a connection with dict-like row access."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables, run migrations, and seed baseline data."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Profile Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            tagline TEXT,
            bio TEXT,
            email TEXT,
            phone TEXT,
            location TEXT,
            github TEXT,
            linkedin TEXT,
            twitter TEXT
        )
    ''')

    # 2. Education Table (Multi-milestone from 10th to College)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS education (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT NOT NULL DEFAULT 'College / Degree',
            degree TEXT NOT NULL,
            major TEXT NOT NULL,
            institution TEXT NOT NULL,
            board TEXT DEFAULT '',
            timeline TEXT NOT NULL,
            status TEXT NOT NULL,
            cgpa TEXT,
            description TEXT,
            coursework TEXT,
            sort_order INTEGER DEFAULT 1
        )
    ''')

    # Run migrations on education table if columns are missing
    cursor.execute('PRAGMA table_info(education)')
    columns = [col[1] for col in cursor.fetchall()]
    if 'level' not in columns:
        cursor.execute("ALTER TABLE education ADD COLUMN level TEXT DEFAULT 'College / Degree'")
    if 'board' not in columns:
        cursor.execute("ALTER TABLE education ADD COLUMN board TEXT DEFAULT ''")
    if 'sort_order' not in columns:
        cursor.execute("ALTER TABLE education ADD COLUMN sort_order INTEGER DEFAULT 1")

    # 3. Activities Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            category_slug TEXT NOT NULL,
            date TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            description TEXT NOT NULL,
            link TEXT,
            link_text TEXT,
            badge TEXT
        )
    ''')

    # 4. Certificates & Credentials Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS certificates (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            issuer TEXT NOT NULL,
            issue_date TEXT NOT NULL,
            category TEXT NOT NULL,
            category_slug TEXT NOT NULL,
            credential_id TEXT,
            credential_url TEXT,
            file_path TEXT,
            file_name TEXT,
            description TEXT,
            timestamp TEXT NOT NULL
        )
    ''')

    conn.commit()

    # Seed initial Profile if empty
    cursor.execute('SELECT COUNT(*) FROM profile')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO profile (id, name, title, tagline, bio, email, phone, location, github, linkedin, twitter)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'Pradeep Kumar Suresh',
            'Computer Science Engineering Student | Python Developer',
            'Maintaining my active engineering journey, project milestones, and academic credentials.',
            'Undergraduate engineer focused on practical software engineering, Python application development, and continuous hands-on learning.',
            'pradeepsuresh103@gmail.com',
            '+91 6382366528',
            'Salem, Tamil Nadu, India',
            'https://github.com/pradeeprosy',
            'https://www.linkedin.com/in/pradeep-kumar-suresh-544075343/',
            'https://x.com/peace_lover_43'
        ))

    # Update row 1 of education to ensure level & sort_order are populated
    cursor.execute('SELECT COUNT(*) FROM education WHERE id = 1')
    if cursor.fetchone()[0] > 0:
        cursor.execute('''
            UPDATE education
            SET level = COALESCE(NULLIF(level, ''), 'College / Degree'),
                board = COALESCE(NULLIF(board, ''), "Vinayaka Mission's Research Foundation"),
                sort_order = 1
            WHERE id = 1
        ''')
    else:
        # Seed baseline College record if education is completely empty
        cursor.execute('''
            INSERT INTO education (id, level, degree, major, institution, board, timeline, status, cgpa, description, coursework, sort_order)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        ''', (
            'College / Degree',
            'Bachelor of Engineering (B.E.)',
            'Computer Science and Engineering',
            "Vinayaka Mission's Research Foundation, Salem",
            "Vinayaka Mission's Research Foundation",
            '2024 - 2028',
            'In Progress / 3rd Year',
            '7.4 / 10',
            'Currently pursuing a Bachelor of Engineering in Computer Science and Engineering (B.E. CSE). Interested in software development, Python programming, Artificial Intelligence, Machine Learning, and web development.',
            'Python Programming, C Programming, C++ Programming, Data Structures, Database Management Systems, Object-Oriented Programming, Operating Systems, Computer Networks, Software Engineering, Web Technology'
        ))

    # Check if 10th and 12th records exist; seed starter records if total education count == 1
    cursor.execute('SELECT COUNT(*) FROM education')
    edu_count = cursor.fetchone()[0]
    if edu_count == 1:
        # Seed 12th Standard (HSC)
        cursor.execute('''
            INSERT INTO education (level, degree, major, institution, board, timeline, status, cgpa, description, coursework, sort_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 2)
        ''', (
            'Higher Secondary (12th / HSC)',
            'Higher Secondary Certificate (HSC)',
            'Bio-Maths / Computer Science',
            'Higher Secondary School (Click Edit to update name)',
            'Tamil Nadu State Board',
            '2022 - 2024',
            'Completed',
            '85%',
            'Completed Higher Secondary education with core foundational focus on Mathematics, Physics, Chemistry, and Computer Science.',
            'Mathematics, Physics, Chemistry, Computer Science, English'
        ))

        # Seed 10th Standard (SSLC)
        cursor.execute('''
            INSERT INTO education (level, degree, major, institution, board, timeline, status, cgpa, description, coursework, sort_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 3)
        ''', (
            'Secondary School (10th / SSLC)',
            'Secondary School Leaving Certificate (SSLC)',
            'General High School Curriculum',
            'High School / Secondary School (Click Edit to update name)',
            'Tamil Nadu State Board',
            '2021 - 2022',
            'Completed',
            '88%',
            'Secondary school certification covering foundational mathematics, general sciences, social studies, and language arts.',
            'Science, Mathematics, Social Science, English, Tamil'
        ))

    # Seed baseline Activities if empty
    cursor.execute('SELECT COUNT(*) FROM activities')
    if cursor.fetchone()[0] == 0:
        now_iso = datetime.now(timezone.utc).isoformat() + "Z"
        seed_activities = [
            (
                'act-1',
                'Built Personal Activity & Academic Hub with In-Browser Editor',
                'Project Milestone',
                'projects',
                'Oct 2026',
                now_iso,
                'Architected full-stack Flask and SQLite management platform with real-time academic record tracking and instant in-browser editing controls.',
                'https://github.com/pradeeprosy',
                'View GitHub Profile',
                'Flask / SQLite'
            ),
            (
                'act-2',
                'Academic Progress: Semester Laboratory & Systems Development',
                'Academic & Coursework',
                'academic',
                'Sep 2026',
                now_iso,
                "Completed hands-on practical laboratory modules in Relational Database Schema Design and Object-Oriented Software Architecture at Vinayaka Mission's Research Foundation.",
                '',
                '',
                'Vinayaka Missions Univ'
            ),
            (
                'act-3',
                'Prototyped Citizen Safety & Travel Assistance Network',
                'Hackathon & Innovation',
                'hackathons',
                'Aug 2026',
                now_iso,
                'Engineered geofenced perimeter alert triggers and emergency responder telemetry system for public traveler assistance.',
                'https://github.com/pradeeprosy',
                'View Prototype',
                'Python / Flask'
            ),
            (
                'act-4',
                'Explored Semantic NLP Search & Sentence Transformer Models',
                'Learning & Tech Stack',
                'learnings',
                'Jul 2026',
                now_iso,
                'Investigated cosine similarity calculations and dense vector indexing in Python for conversational institutional knowledge retrieval.',
                'https://github.com/pradeeprosy',
                'NLP Exploration',
                'Python / NLP'
            )
        ]

        cursor.executemany('''
            INSERT INTO activities (id, title, category, category_slug, date, timestamp, description, link, link_text, badge)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_activities)

    # Seed baseline Certificates if empty
    cursor.execute('SELECT COUNT(*) FROM certificates')
    if cursor.fetchone()[0] == 0:
        now_iso = datetime.now(timezone.utc).isoformat() + "Z"
        seed_certificates = [
            (
                'cert-1',
                'Python Foundations & Problem Solving',
                'HackerRank / Coding Platform',
                '2024',
                'Technical Certification',
                'technical',
                'HR-PY-2024',
                'https://www.hackerrank.com',
                '',
                '',
                'Verified foundational proficiency in Python algorithmic problem solving, data structures, and conditional workflows.',
                now_iso
            ),
            (
                'cert-2',
                'Higher Secondary School Leaving Certificate (12th Marksheet)',
                'Tamil Nadu State Board',
                '2024',
                'Academic Certificate',
                'academic',
                'TNBSE-2024-HSC',
                '',
                '',
                '',
                'Official completion and academic evaluation certificate for Higher Secondary Examination (Class 12).',
                now_iso
            )
        ]
        cursor.executemany('''
            INSERT INTO certificates (id, title, issuer, issue_date, category, category_slug, credential_id, credential_url, file_path, file_name, description, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_certificates)

    conn.commit()
    conn.close()


# -------------------------------------------------------------
# Profile Functions
# -------------------------------------------------------------
def get_profile():
    """Retrieve candidate profile details."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM profile WHERE id = 1')
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return {}


def update_profile(data):
    """Update candidate profile details."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE profile
        SET name = ?, title = ?, tagline = ?, bio = ?, email = ?, phone = ?, location = ?, github = ?, linkedin = ?, twitter = ?
        WHERE id = 1
    ''', (
        data.get('name', '').strip(),
        data.get('title', '').strip(),
        data.get('tagline', '').strip(),
        data.get('bio', '').strip(),
        data.get('email', '').strip(),
        data.get('phone', '').strip(),
        data.get('location', '').strip(),
        data.get('github', '').strip(),
        data.get('linkedin', '').strip(),
        data.get('twitter', '').strip()
    ))
    conn.commit()
    conn.close()
    return True


# -------------------------------------------------------------
# Multi-Stage Education Functions (10th to College)
# -------------------------------------------------------------
def _format_edu_row(row):
    """Format an education sqlite3.Row into a clean dictionary with coursework list."""
    if not row:
        return {}
    d = dict(row)
    cw_str = d.get('coursework') or ''
    d['coursework_list'] = [c.strip() for c in cw_str.split(',') if c.strip()]
    return d


def get_education_list():
    """Retrieve all education records sorted by academic progression (College first, then 12th, 10th)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM education ORDER BY sort_order ASC, id ASC')
    rows = cursor.fetchall()
    conn.close()
    return [_format_edu_row(r) for r in rows]


def get_primary_education():
    """Retrieve top-level primary education record for hero section display."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM education ORDER BY sort_order ASC, id ASC LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    return _format_edu_row(row) if row else {}


def get_education():
    """Alias for backwards compatibility."""
    return get_primary_education()


def get_education_by_id(edu_id):
    """Retrieve specific education record by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM education WHERE id = ?', (edu_id,))
    row = cursor.fetchone()
    conn.close()
    return _format_edu_row(row) if row else None


def add_education(data):
    """Insert a new education milestone record."""
    conn = get_db_connection()
    cursor = conn.cursor()

    level = data.get('level', 'College / Degree').strip()
    degree = data.get('degree', '').strip()
    major = data.get('major', '').strip()
    institution = data.get('institution', '').strip()
    board = data.get('board', '').strip()
    timeline = data.get('timeline', '').strip()
    status = data.get('status', 'Completed').strip()
    cgpa = data.get('cgpa', '').strip()
    description = data.get('description', '').strip()
    coursework = data.get('coursework', '').strip()
    try:
        sort_order = int(data.get('sort_order', 99))
    except (ValueError, TypeError):
        sort_order = 99

    cursor.execute('''
        INSERT INTO education (level, degree, major, institution, board, timeline, status, cgpa, description, coursework, sort_order)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        level, degree, major, institution, board, timeline, status, cgpa, description, coursework, sort_order
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return get_education_by_id(new_id)


def update_education(edu_id, data=None):
    """
    Update education record by ID.
    If called with single dict argument for backwards-compatibility with id=1.
    """
    if data is None and isinstance(edu_id, dict):
        data = edu_id
        edu_id = data.get('id', 1)

    conn = get_db_connection()
    cursor = conn.cursor()

    level = data.get('level', '').strip()
    degree = data.get('degree', '').strip()
    major = data.get('major', '').strip()
    institution = data.get('institution', '').strip()
    board = data.get('board', '').strip()
    timeline = data.get('timeline', '').strip()
    status = data.get('status', '').strip()
    cgpa = data.get('cgpa', '').strip()
    description = data.get('description', '').strip()
    coursework = data.get('coursework', '').strip()
    sort_order_val = data.get('sort_order')

    update_fields = [
        'degree = ?', 'major = ?', 'institution = ?', 'timeline = ?',
        'status = ?', 'cgpa = ?', 'description = ?', 'coursework = ?'
    ]
    params = [degree, major, institution, timeline, status, cgpa, description, coursework]

    if level:
        update_fields.append('level = ?')
        params.append(level)
    if board is not None:
        update_fields.append('board = ?')
        params.append(board)
    if sort_order_val is not None:
        try:
            update_fields.append('sort_order = ?')
            params.append(int(sort_order_val))
        except (ValueError, TypeError):
            pass

    params.append(edu_id)
    query = f"UPDATE education SET {', '.join(update_fields)} WHERE id = ?"
    cursor.execute(query, params)
    conn.commit()
    conn.close()

    return get_education_by_id(edu_id)


def delete_education(edu_id):
    """Delete an education record by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM education WHERE id = ?', (edu_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


# -------------------------------------------------------------
# Certificates & Credentials Functions
# -------------------------------------------------------------
def _derive_cert_slug(category):
    cat_lower = (category or '').lower().strip()
    if 'tech' in cat_lower or 'program' in cat_lower or 'code' in cat_lower:
        return 'technical'
    if 'acad' in cat_lower or 'school' in cat_lower or 'college' in cat_lower or 'mark' in cat_lower:
        return 'academic'
    if 'work' in cat_lower or 'sem' in cat_lower:
        return 'workshops'
    if 'hack' in cat_lower or 'compet' in cat_lower or 'award' in cat_lower:
        return 'competitions'
    return 'general'


def get_certificates(category=None, search=None):
    """Retrieve certificates with optional category filter and keyword search."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = 'SELECT * FROM certificates WHERE 1=1'
    params = []

    if category and category.lower() != 'all':
        query += ' AND (category_slug = ? OR category = ?)'
        params.extend([category.lower(), category])

    if search and search.strip():
        term = f"%{search.strip()}%"
        query += ' AND (title LIKE ? OR issuer LIKE ? OR description LIKE ? OR credential_id LIKE ?)'
        params.extend([term, term, term, term])

    query += ' ORDER BY timestamp DESC'
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(r) for r in rows]


def get_certificate_by_id(cert_id):
    """Fetch single certificate by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM certificates WHERE id = ?', (cert_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def add_certificate(title, issuer, issue_date, category, credential_id='', credential_url='', file_path='', file_name='', description=''):
    """Insert a new certificate record."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cert_id = f"cert-{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat() + "Z"
    category_slug = _derive_cert_slug(category)

    if not issue_date or not issue_date.strip():
        issue_date = datetime.now(timezone.utc).strftime('%b %Y')

    cursor.execute('''
        INSERT INTO certificates (id, title, issuer, issue_date, category, category_slug, credential_id, credential_url, file_path, file_name, description, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        cert_id,
        title.strip(),
        issuer.strip(),
        issue_date.strip(),
        category.strip(),
        category_slug,
        credential_id.strip() if credential_id else '',
        credential_url.strip() if credential_url else '',
        file_path.strip() if file_path else '',
        file_name.strip() if file_name else '',
        description.strip() if description else '',
        now_iso
    ))
    conn.commit()
    conn.close()

    return get_certificate_by_id(cert_id)


def update_certificate(cert_id, data):
    """Update existing certificate record."""
    conn = get_db_connection()
    cursor = conn.cursor()

    category = data.get('category', '').strip()
    category_slug = _derive_cert_slug(category)

    update_fields = [
        'title = ?', 'issuer = ?', 'issue_date = ?', 'category = ?',
        'category_slug = ?', 'credential_id = ?', 'credential_url = ?', 'description = ?'
    ]
    params = [
        data.get('title', '').strip(),
        data.get('issuer', '').strip(),
        data.get('issue_date', '').strip(),
        category,
        category_slug,
        data.get('credential_id', '').strip(),
        data.get('credential_url', '').strip(),
        data.get('description', '').strip()
    ]

    # If new file was uploaded
    if data.get('file_path'):
        update_fields.append('file_path = ?')
        params.append(data.get('file_path'))
    if data.get('file_name'):
        update_fields.append('file_name = ?')
        params.append(data.get('file_name'))

    params.append(cert_id)
    query = f"UPDATE certificates SET {', '.join(update_fields)} WHERE id = ?"
    cursor.execute(query, params)
    conn.commit()
    conn.close()

    return get_certificate_by_id(cert_id)


def delete_certificate(cert_id):
    """Delete a certificate entry by ID and return its file_path for cleanup."""
    cert = get_certificate_by_id(cert_id)
    file_path = cert.get('file_path') if cert else None

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM certificates WHERE id = ?', (cert_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()

    return deleted, file_path


# -------------------------------------------------------------
# Activity Stream Functions
# -------------------------------------------------------------
def get_activities(category=None, search=None):
    """Retrieve activities with optional category filter and keyword search."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = 'SELECT * FROM activities WHERE 1=1'
    params = []

    if category and category.lower() != 'all':
        query += ' AND (category_slug = ? OR category = ?)'
        params.extend([category.lower(), category])

    if search and search.strip():
        term = f"%{search.strip()}%"
        query += ' AND (title LIKE ? OR description LIKE ? OR badge LIKE ?)'
        params.extend([term, term, term])

    query += ' ORDER BY timestamp DESC'
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(r) for r in rows]


def get_activity_by_id(activity_id):
    """Fetch single activity by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM activities WHERE id = ?', (activity_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def add_activity(title, category, date, description, link='', link_text='', badge=''):
    """Insert new activity entry."""
    conn = get_db_connection()
    cursor = conn.cursor()

    act_id = f"act-{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat() + "Z"

    slug_map = {
        'project milestone': 'projects',
        'hackathon & innovation': 'hackathons',
        'learning & tech stack': 'learnings',
        'academic & coursework': 'academic',
        'certification & workshop': 'certifications'
    }
    category_slug = slug_map.get(category.lower().strip(), 'general')

    if not date or not date.strip():
        date = datetime.now(timezone.utc).strftime('%b %Y')

    if not badge or not badge.strip():
        badge = category

    cursor.execute('''
        INSERT INTO activities (id, title, category, category_slug, date, timestamp, description, link, link_text, badge)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        act_id,
        title.strip(),
        category.strip(),
        category_slug,
        date.strip(),
        now_iso,
        description.strip(),
        link.strip(),
        link_text.strip() if link.strip() else '',
        badge.strip()
    ))
    conn.commit()
    conn.close()

    return get_activity_by_id(act_id)


def update_activity(activity_id, data):
    """Update existing activity entry."""
    conn = get_db_connection()
    cursor = conn.cursor()

    category = data.get('category', '').strip()
    slug_map = {
        'project milestone': 'projects',
        'hackathon & innovation': 'hackathons',
        'learning & tech stack': 'learnings',
        'academic & coursework': 'academic',
        'certification & workshop': 'certifications'
    }
    category_slug = slug_map.get(category.lower(), 'general')

    cursor.execute('''
        UPDATE activities
        SET title = ?, category = ?, category_slug = ?, date = ?, description = ?, link = ?, link_text = ?, badge = ?
        WHERE id = ?
    ''', (
        data.get('title', '').strip(),
        category,
        category_slug,
        data.get('date', '').strip(),
        data.get('description', '').strip(),
        data.get('link', '').strip(),
        data.get('link_text', '').strip(),
        data.get('badge', '').strip(),
        activity_id
    ))
    conn.commit()
    conn.close()

    return get_activity_by_id(activity_id)


def delete_activity(activity_id):
    """Delete an activity entry by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM activities WHERE id = ?', (activity_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


# -------------------------------------------------------------
# Aggregate Statistics
# -------------------------------------------------------------
def get_stats():
    """Retrieve quick aggregate counts for dashboard header."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM activities')
    total_activities = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM activities WHERE category_slug = "projects"')
    project_milestones = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM activities WHERE category_slug = "academic"')
    academic_updates = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM activities WHERE category_slug = "hackathons"')
    hackathons = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM certificates')
    total_certificates = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM education')
    total_education_stages = cursor.fetchone()[0]

    conn.close()

    return {
        "total_activities": total_activities,
        "project_milestones": project_milestones,
        "academic_updates": academic_updates,
        "hackathons": hackathons,
        "total_certificates": total_certificates,
        "total_education_stages": total_education_stages
    }
