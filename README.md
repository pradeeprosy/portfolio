# Pradeep Kumar Suresh - Activity & Academic Hub

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Status](https://img.shields.io/badge/Status-Active%20%26%20Live-success.svg)](#)

A dedicated, modern web platform designed specifically for **Pradeep Kumar Suresh** to maintain and showcase:
1. **Live Continuous Activity Stream & Dev Journal**: Actively document what you are building, project milestones, hackathons, certifications, and technical advancements.
2. **Academic & Education Dashboard**: Maintain and display degree credentials (*B.E. Computer Science and Engineering*), university records (*Vinayaka Missions University, Salem*), batch timeline (*2022 – 2026*), CGPA badge (*8.5 / 10*), and core coursework.
3. **Instant In-Browser Quick Editors**: Click **"Edit Education"** or **"Post Activity"** right from your browser without editing code or JSON files!

---

## Key Features

- **Academic Hub**:
  - **University**: Vinayaka Missions University, Salem
  - **Degree**: Bachelor of Engineering (B.E.) in Computer Science and Engineering
  - **Batch Timeline**: 2022 – 2026 (In Progress / 3rd Year)
  - **CGPA Display**: 8.5 / 10
  - **Technical Coursework**: Data Structures & Algorithms, Python Backend Systems, Database Management Systems, Machine Learning & NLP, Operating Systems, Computer Networks.
- **Continuous Activity Stream**:
  - 🚀 **Project Milestones**: Track software applications and system prototypes.
  - 🎓 **Academic & Labs**: Document university laboratory work and systems coursework.
  - 🏆 **Hackathons & Competitions**: Log innovation prototypes and competitive events.
  - 💡 **Learnings & Tech Stack**: Document new libraries, frameworks, and algorithms learned.
  - 📜 **Certifications & Workshops**: Maintain accredited course credentials.
- **Interactive Controls**:
  - Live keyword search bar and category filter chips.
  - Dark Mode (default) and Light Mode toggle with `localStorage` memory.
  - Responsive design for mobile smartphones, tablets, and desktop displays.
- **In-Browser Quick Edit Modals**:
  - Update your education details or publish new activities directly from the website.
  - Protected with an **Admin PIN** (default: `pradeep2026`).

---

## Project Structure

```text
Personal/
├── app.py                     # Flask server & REST endpoints
├── database.py                # SQLite database persistence layer & seed models
├── requirements.txt           # Python dependencies
├── README.md                  # Complete documentation
├── .env.example               # Environment template
├── .gitignore                 # Exclusion rules
│
├── data/
│   └── hub.db                 # SQLite database (auto-created on startup)
│
├── static/
│   ├── css/
│   │   └── style.css          # Design system, themes, and modal styling
│   ├── js/
│   │   └── app.js             # Real-time search, filters, and AJAX CRUD modals
│   └── images/
│       └── favicon.svg        # Developer favicon icon
│
└── templates/
    ├── index.html             # Main dashboard (Education + Activity feed)
    └── 404.html               # Custom 404 error template
```

---

## Local Setup & Quick Start

### 1. Open Terminal or PowerShell
```powershell
cd c:\Users\prade\OneDrive\Desktop\Personal
```

### 2. Create and Activate Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Run the Application
```powershell
python app.py
```
Open **`http://127.0.0.1:5000`** in your browser!

---

## How to Edit Details In-Browser

1. Click **"Edit Education"** in the navigation header or on the education card.
2. Edit your university name, batch, CGPA, or coursework.
3. Enter your Admin PIN: **`pradeep2026`** (only needed once per session).
4. Click **"Save Education Details"** — the page updates immediately!

---

## How to Post a New Activity In-Browser

1. Click **"Post Activity"** in the top navigation.
2. Enter the title, choose a category (*Project Milestone*, *Hackathon*, *Learning*, etc.), and write a brief description.
3. (Optional) Add a reference link to a GitHub repository or demo.
4. Click **"Publish Activity"** — it appears on your live feed instantly!

---

## Automated Unit Testing
Run the automated test suite:
```powershell
python test_app.py
```
*(All 6 unit tests pass in < 0.1s).*

---

## Production Deployment (Render)

1. Push your repository to GitHub.
2. On [Render.com](https://render.com), create a new **Web Service** and connect your repository.
3. Settings:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Add environment variables in Render:
   - `ADMIN_PIN`: `your_custom_pin`
   - `SECRET_KEY`: `your_random_secret_key`
5. Click **Deploy Web Service** — your hub will be live online!
