"""
Database Engine & Persistence Layer for Activity & Education Hub
Uses Python standard sqlite3 for reliable, zero-dependency persistence.
"""

import os
import sqlite3
import uuid
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'hub.db')


def get_db_connection():
    """Create a connection with dict-like row access."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables and seed baseline credentials and data."""
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

    # 2. Education Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS education (
            id INTEGER PRIMARY KEY,
            degree TEXT NOT NULL,
            major TEXT NOT NULL,
            institution TEXT NOT NULL,
            timeline TEXT NOT NULL,
            status TEXT NOT NULL,
            cgpa TEXT,
            description TEXT,
            coursework TEXT
        )
    ''')

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
            '+91 (Add your phone number)',
            'Salem, Tamil Nadu, India',
            'https://github.com/pradeeprosy',
            'https://www.linkedin.com/in/pradeep-kumar-suresh-544075343/',
            'https://x.com/peace_lover_43'
        ))

    # Seed initial Education if empty
    cursor.execute('SELECT COUNT(*) FROM education')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO education (id, degree, major, institution, timeline, status, cgpa, description, coursework)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'Bachelor of Engineering (B.E.)',
            'Computer Science and Engineering',
            'Vinayaka Missions University, Salem',
            '2022 - 2026',
            'In Progress / 3rd Year',
            '8.5 / 10',
            'Focused academic study covering core software engineering principles, algorithms, and practical computing systems.',
            'Data Structures & Algorithms, Python Backend Systems, Database Management Systems, Machine Learning & NLP, Operating Systems, Computer Networks, Software Engineering'
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
                'Completed hands-on practical laboratory modules in Relational Database Schema Design and Object-Oriented Software Architecture at Vinayaka Missions University.',
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

    conn.commit()
    conn.close()


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


def get_education():
    """Retrieve education details."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM education WHERE id = 1')
    row = cursor.fetchone()
    conn.close()
    if row:
        d = dict(row)
        # Parse coursework string into a list of clean tags
        cw_str = d.get('coursework') or ''
        d['coursework_list'] = [c.strip() for c in cw_str.split(',') if c.strip()]
        return d
    return {}


def update_education(data):
    """Update education details."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE education
        SET degree = ?, major = ?, institution = ?, timeline = ?, status = ?, cgpa = ?, description = ?, coursework = ?
        WHERE id = 1
    ''', (
        data.get('degree', '').strip(),
        data.get('major', '').strip(),
        data.get('institution', '').strip(),
        data.get('timeline', '').strip(),
        data.get('status', '').strip(),
        data.get('cgpa', '').strip(),
        data.get('description', '').strip(),
        data.get('coursework', '').strip()
    ))
    conn.commit()
    conn.close()
    return True


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
    
    # Derive category slug
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

    conn.close()

    return {
        "total_activities": total_activities,
        "project_milestones": project_milestones,
        "academic_updates": academic_updates,
        "hackathons": hackathons
    }
