# Pradeep Kumar Suresh - Activity, Education & Certificate Hub

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Status](https://img.shields.io/badge/Status-Active%20%26%20Live-success.svg)](#)

A dedicated, comprehensive web platform designed specifically for **Pradeep Kumar Suresh** to maintain and showcase:
1. **Academic Journey (10th to College)**: Complete educational records from Secondary Schooling (SSLC), Higher Secondary (HSC), to Undergraduate Engineering (B.E. Computer Science and Engineering at Vinayaka Mission's Research Foundation).
2. **Certificates & Verified Credentials**: Upload and maintain academic marksheets, course completion certificates, competition badges, and workshop credentials with PDF and image file storage.
3. **Live Continuous Activity Stream & Dev Journal**: Actively document projects, laboratory systems, hackathons, and new tech stack learnings.
4. **Instant In-Browser Quick Editors**: Full manual control to Add, Edit, or Delete any academic stage or certificate directly through intuitive web modals without touching code!

---

## Key Features

- **Multi-Stage Academic Progression (10th to College)**:
  - 🎓 **Undergraduate (College / B.E.)**: Vinayaka Mission's Research Foundation, Salem (2024 – 2028 | CGPA: 7.4 / 10 | Computer Science & Engineering).
  - 🏫 **Higher Secondary (12th / HSC)**: School name, State Board / CBSE, batch, percentage, and key subjects (Click "Edit" on card to customize).
  - 📘 **Secondary School (10th / SSLC)**: School name, State Board / CBSE, batch, percentage, and core foundations (Click "Edit" on card to customize).
  - ➕ **Add Education**: Option to add additional milestones (e.g., Diploma, Master's, or specialized degrees).
- **Certificate Management & File Uploads**:
  - Upload certificates directly in PDF, PNG, JPG, JPEG, or WEBP formats (up to 16MB).
  - Option to provide online verification links or digital badge URLs (Coursera, HackerRank, Credly, etc.).
  - Category filters: *Technical & Programming, Academic & Marksheets, Workshops & Seminars, Competitions & Hackathons*.
  - View / Download certificates in one click directly from the UI.
- **Continuous Activity Stream**:
  - 🚀 **Project Milestones**: Track software applications and system prototypes.
  - 🎓 **Academic & Labs**: Document university laboratory work and systems coursework.
  - 🏆 **Hackathons & Competitions**: Log innovation prototypes and competitive events.
  - 💡 **Learnings & Tech Stack**: Document new libraries, frameworks, and algorithms learned.
  - 📜 **Certifications & Workshops**: Maintain accredited course credentials.
- **In-Browser Quick Editors (Admin PIN Protected)**:
  - Add, edit, or delete activities, certificates, and education milestones directly in the browser.
  - Protected with Admin PIN (default: `pradeep2026`).

---

## Project Structure

```text
Personal/
├── app.py                     # Flask server, REST APIs, & certificate upload handlers
├── database.py                # SQLite database persistence layer & migrations
├── requirements.txt           # Python dependencies
├── runtime.txt                # Python runtime specification (python-3.11.9)
├── test_app.py                # 7 automated unit tests
├── README.md                  # Documentation
├── .env.example               # Environment template
├── .gitignore                 # Exclusion rules
│
├── data/
│   └── hub.db                 # Persistent SQLite database
│
├── static/
│   ├── css/
│   │   └── style.css          # Design system, timeline cards, & certificate grid
│   ├── js/
│   │   └── app.js             # Real-time search, filters, and AJAX CRUD modals
│   ├── images/
│   │   └── favicon.svg        # Developer favicon icon
│   └── uploads/
│       └── certificates/      # Uploaded certificate PDF and image files (.gitkeep)
│
└── templates/
    ├── index.html             # Main dashboard (Education + Certificates + Activities)
    └── 404.html               # Custom 404 error template
```

---

## Local Setup & Quick Start

### 1. Open Terminal or PowerShell
```powershell
cd c:\Users\prade\OneDrive\Desktop\Personal
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Run the Application
```powershell
python app.py
```
Open **`http://127.0.0.1:5000`** in your browser!

---

## How to Manage Your Data Manually in the Browser

All management options are available directly on the web page:

### 1. Update 10th, 12th, or College Details
- Scroll to the **Education & Qualifications** section.
- On any card (College, 12th, or 10th), click **"Edit"**.
- Update your school name, board, marks percentage, or coursework.
- Enter your Admin PIN: **`pradeep2026`** (only prompted once per session).
- Click **"Save Education Record"** — it updates immediately on screen and in SQLite!

### 2. Upload Your Certificates & Marksheets
- Click the **"Upload Certificate"** button in the header or section title.
- Enter the certificate title (e.g. *10th Marksheet*, *Python Problem Solving*).
- Enter the issuing organization (e.g. *Tamil Nadu State Board*, *HackerRank*).
- Click the upload dropzone to choose your **PDF, PNG, or JPG** file (or provide a verification link).
- Enter your Admin PIN: **`pradeep2026`**.
- Click **"Upload & Save Certificate"** — your certificate appears instantly with a View/Download button!

### 3. Post Live Dev Activities
- Click **"Post Activity"** in the top navigation bar.
- Choose category (*Project Milestone, Academic, Hackathon, Learning, etc.*).
- Write your update and click **"Publish Activity"**.

---

## Running Automated Tests

Run the unit test suite at any time:
```powershell
python test_app.py
```
All 7 unit tests pass with 100% test coverage for authentication, multi-stage education CRUD, certificate uploads, and live activity streams.
