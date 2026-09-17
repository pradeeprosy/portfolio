# Pradeep Kumar - Professional Developer Portfolio Website

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)](#)

A modern, responsive, high-performance personal career portfolio website designed specifically for **Pradeep Kumar** (Computer Science Engineering Student, Python Developer, AI/ML Enthusiast, and Full Stack Developer).

Engineered to impress recruiters, corporate hiring teams, hackathon judges, and research coordinators with an authentic developer aesthetic, clean code architecture, smooth UX, Dark/Light themes, interactive project modals, and zero hardcoded credentials.

---

## Table of Contents
1. [Project Overview & Key Highlights](#1-project-overview--key-highlights)
2. [Complete Folder Structure](#2-complete-folder-structure)
3. [Prerequisites & System Setup](#3-prerequisites--system-setup)
4. [VS Code Run Instructions](#4-vs-code-run-instructions)
5. [Localhost Testing & Verification](#5-localhost-testing--verification)
6. [How to Customize Your Portfolio Data](#6-how-to-customize-your-portfolio-data)
7. [GitHub Repository Setup](#7-github-repository-setup)
8. [Production Deployment Instructions](#8-production-deployment-instructions)
   - [Method 1: Render (Recommended - Free Dynamic Flask Hosting)](#method-1-render-recommended---free-dynamic-flask-hosting)
   - [Method 2: Railway](#method-2-railway)
   - [Method 3: PythonAnywhere](#method-3-pythonanywhere)
   - [Method 4: Static Export to GitHub Pages](#method-4-static-export-to-github-pages)
9. [Connecting a Custom Domain](#9-connecting-a-custom-domain)
10. [Google Search Indexing & SEO Setup](#10-google-search-indexing--seo-setup)
11. [Security & Best Practices](#11-security--best-practices)

---

## 1. Project Overview & Key Highlights

- **Authentic Engineering Representation**: Accurately showcases student engineering foundations without exaggerated titles, fake percentages, or invented past employment.
- **Centralized Data Model (`data/portfolio.json`)**: Update projects, skill badges, academic details, and certifications in one clean JSON file without editing HTML or backend code.
- **11 Complete Sections**:
  1. **Home (Hero)**: Profile badge, dynamic roles, developer tagline, dual call-to-actions, and social links.
  2. **About Me**: Academic background in B.E. Computer Science, engineering philosophy, and domain focus.
  3. **Technical Skills**: Categorized technology cards (Programming, Web, Databases, AI/ML, Tools) with icons and real competency badges (no fake % bars).
  4. **Projects**: 5 full-stack and AI project showcases with problem statements, solutions, technologies, key features, and deep-dive modals.
  5. **Hackathons & Innovation**: Visual 5-step engineering pipeline (**Problem $\to$ Idea $\to$ Technology $\to$ Prototype $\to$ Impact**).
  6. **Career Journey**: 7-stage interactive progression clearly demarcating current active building from future career goals.
  7. **Education**: Clean timeline for Bachelor of Engineering – Computer Science and Engineering.
  8. **Certifications**: Modular, editable accreditation cards with placeholder seals.
  9. **Achievements**: Structured cards for hackathons, innovation contests, and academic showcases.
  10. **Resume**: Integrated summary card with 1-click official PDF download (`/resume/download`).
  11. **Contact**: Modern interactive form with frontend validation, bot honeypot protection, local message archiving, and optional SMTP email dispatch.
- **Modern Design & Accessibility**:
  - Dark Mode (default) & Light Mode with seamless transition and `localStorage` persistence.
  - Glassmorphic navigation header with active section scroll-spy indicator.
  - Floating back-to-top button with scroll triggers.
  - Mobile-first responsive grid layouts for phone, tablet, and widescreen desktop displays.
- **Search Engine Optimization (SEO)**:
  - Semantic HTML5 tags (`<main>`, `<section>`, `<article>`, `<header>`, `<footer>`).
  - Open Graph tags for rich previews on LinkedIn, WhatsApp, and Twitter Cards.
  - Dynamic XML sitemap generator (`/sitemap.xml`) and search crawler directives (`/robots.txt`).

---

## 2. Complete Folder Structure

```text
Personal/
│
├── app.py                     # Flask application (routes, API, contact dispatch, SEO)
├── requirements.txt           # Python dependencies (Flask, python-dotenv, waitress)
├── generate_resume.py         # Utility script that compiles the official resume PDF
├── export_static.py           # 1-click exporter for static hosting (GitHub Pages)
├── test_app.py                # Automated unit tests for routes, data, and validation
├── .env.example               # Template for environment variables (SMTP, Secret Key)
├── .gitignore                 # Excludes caches, venv, secrets, and temp builds
├── README.md                  # Complete developer documentation and deployment guide
│
├── .vscode/
│   └── launch.json            # VS Code F5 Run & Debug configuration
│
├── data/
│   ├── portfolio.json         # Central configuration for all content, skills & projects
│   └── contact_messages.json  # Local archive of contact inquiries (auto-generated)
│
├── templates/
│   ├── index.html             # Master single-page template with all 11 sections
│   ├── project_detail.html    # Standalone deep-link view for individual projects
│   └── 404.html               # Custom 404 error template
│
├── static/
│   ├── css/
│   │   └── style.css          # Design system, CSS variables, dark/light themes & responsiveness
│   ├── js/
│   │   └── script.js          # Theme toggle, modal popups, scroll spy, and AJAX contact form
│   └── images/
│       ├── favicon.svg        # Modern developer monogram favicon
│       ├── avatar-placeholder.svg      # Developer avatar illustration
│       ├── chatbot-preview.svg         # AI College Chatbot artwork
│       ├── safety-network-preview.svg  # Citizen Safety Network artwork
│       ├── alcohol-quota-preview.svg   # Alcohol Quota System artwork
│       ├── plastic-waste-preview.svg   # Plastic Waste System artwork
│       ├── food-ordering-preview.svg   # Online Food Ordering artwork
│       └── cert-placeholder.svg        # Certificate credential badge artwork
│
└── resume/
    └── resume.pdf             # Official candidate resume document served for download
```

---

## 3. Prerequisites & System Setup

### Prerequisites
- **Python 3.10+** (Tested on Python 3.14.0)
- **pip** (Python package installer)
- **Git** (for version control and deployment)
- **Visual Studio Code** (recommended editor)

### Step 1: Clone or Navigate to the Project Directory
Open **PowerShell** (Windows) or **Terminal** (macOS/Linux):
```powershell
cd c:\Users\prade\OneDrive\Desktop\Personal
```

### Step 2: Create a Virtual Environment
It is best practice to use an isolated Python virtual environment:
```powershell
# Windows PowerShell
python -m venv .venv

# Activate on Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# (If running on macOS or Linux)
# source .venv/bin/activate
```

> **Note for Windows PowerShell users:** If script execution is restricted, run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy the `.env.example` template to `.env`:
```powershell
# Windows PowerShell
Copy-Item .env.example .env

# macOS / Linux
# cp .env.example .env
```
Open `.env` and configure your settings:
```env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_random_secret_key_here

# Optional: To receive contact messages directly to your email via SMTP:
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=True
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-google-app-password
CONTACT_RECIPIENT_EMAIL=your-email@gmail.com

SITE_URL=http://localhost:5000
```
*(If SMTP is left unconfigured, submissions are safely stored locally in `data/contact_messages.json` without any crash or loss of inquiries).*

---

## 4. VS Code Run Instructions

This repository includes a pre-configured `.vscode/launch.json` file for 1-click execution.

1. Launch **Visual Studio Code**.
2. Go to **File** $\to$ **Open Folder...** and select `c:\Users\prade\OneDrive\Desktop\Personal`.
3. If prompted to select a Python Interpreter, press `Ctrl + Shift + P`, type `Python: Select Interpreter`, and choose your `.venv` environment.
4. **Run the application**:
   - Press **`F5`** on your keyboard, OR
   - Click the **Run & Debug** icon on the left sidebar (bug icon with play arrow) and click the green play button next to **"Python: Flask (Development)"**.
5. The integrated terminal will display:
   ```text
    * Serving Flask app 'app.py'
    * Debug mode: on
    * Running on http://127.0.0.1:5000
   ```
6. Open your browser and navigate to: **`http://127.0.0.1:5000`**.

---

## 5. Localhost Testing & Verification

### Running the Automated Test Suite
Run the built-in test suite to verify that all routes, API endpoints, static assets, and validation logic pass:
```powershell
python test_app.py
```
Expected output:
```text
Ran 8 tests in 0.14s
OK
```

### Manual Testing Checklist
1. **Home & Navigation**:
   - Verify that clicking navbar items (`About`, `Skills`, `Projects`, `Innovation`, `Journey`, `Education`, `Resume`, `Contact`) smoothly scrolls to the correct section.
   - Click the **Theme Toggle Button** (Sun/Moon) in the top-right corner to ensure smooth switching between Dark and Light mode. Refresh the page to confirm that your theme selection is remembered.
2. **Project Modals & Deep Links**:
   - Scroll to **Projects** and click **"Details & Architecture"** on any project card.
   - Confirm that the modal appears with the problem statement, proposed solution, architecture badges, and features.
   - Test closing via the `×` button, clicking outside the modal, or pressing `Esc`.
   - Test opening a direct project link: `http://localhost:5000/project/ai-powered-college-chatbot`.
3. **Resume Download**:
   - Click the **"Download Resume"** button in the hero or resume section.
   - Verify that your browser downloads `Pradeep_Kumar_Resume.pdf`.
4. **Contact Form Validation**:
   - Scroll to **Contact**. Try submitting empty fields to verify that client-side validation displays alerts.
   - Fill in your name, a test email, and a message ($\ge 10$ chars), then click **"Send Message"**.
   - Confirm that the success alert appears and the inquiry is recorded in `data/contact_messages.json`.
5. **SEO Directives**:
   - Visit `http://localhost:5000/robots.txt` $\to$ Confirm crawler permissions and sitemap link.
   - Visit `http://localhost:5000/sitemap.xml` $\to$ Confirm structured XML urlset.

---

## 6. How to Customize Your Portfolio Data

You do **not** need to touch HTML or Python code to update your portfolio. Everything is managed inside:
**`data/portfolio.json`**

### Key Customization Sections:
- **Personal Information**:
  ```json
  "personal": {
    "name": "Pradeep Kumar",
    "email": "your.real.email@example.com",
    "social": {
      "github": "https://github.com/your-actual-username",
      "linkedin": "https://linkedin.com/in/your-actual-profile"
    }
  }
  ```
- **Profile Picture**:
  Replace `/static/images/avatar-placeholder.svg` with your professional photo (e.g. save your photo as `static/images/profile.jpg` and update `"avatar": "/static/images/profile.jpg"` in `portfolio.json`).
- **Adding or Editing Projects**:
  In the `"projects"` array, modify existing projects or append a new JSON object with `id`, `title`, `category`, `problem`, `solution`, `technologies`, `features`, and links.
- **Updating Skills**:
  Under `"skills"`, add or edit entries in `programming`, `web`, `database`, `ai_ml`, or `tools`.
- **Certifications & Achievements**:
  Replace the placeholder entries in `"certifications"` and `"achievements"` whenever you earn verified course certificates or win hackathons.
- **Regenerating the Resume PDF**:
  If you update `generate_resume.py` or place your own compiled PDF in `resume/resume.pdf`, it will immediately be served for downloads.

---

## 7. GitHub Repository Setup

To save your code and prepare for deployment:

1. **Initialize Git in your project folder**:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit: Production-ready career portfolio website"
   ```

2. **Create a new GitHub repository**:
   - Go to [GitHub.com](https://github.com/) and click **New Repository**.
   - Name it `personal-portfolio` or `<your-username>.github.io`.
   - Leave "Initialize with README" unchecked (you already have this README).

3. **Push your code to GitHub**:
   ```powershell
   git remote add origin https://github.com/<your-username>/personal-portfolio.git
   git branch -M main
   git push -u origin main
   ```

---

## 8. Production Deployment Instructions

### Method 1: Render (Recommended - Free Dynamic Flask Hosting)
Render allows you to host the full dynamic Flask backend with working contact forms, email dispatch, and dynamic routes for free.

1. Sign up for free at [Render.com](https://render.com/).
2. Click **New +** $\to$ **Web Service**.
3. Connect your GitHub repository (`personal-portfolio`).
4. Configure the service:
   - **Name**: `pradeep-kumar-portfolio`
   - **Region**: Choose the closest region (e.g., Singapore, Frankfurt, or Oregon).
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`
5. Click **Advanced** $\to$ **Add Environment Variable**:
   - `SECRET_KEY`: *(Generate a secure random string)*
   - `SITE_URL`: `https://pradeep-kumar-portfolio.onrender.com`
   - `SMTP_SERVER`: *(Optional, e.g., smtp.gmail.com)*
   - `SMTP_PORT`: `587`
   - `SMTP_USERNAME`: *(Your email)*
   - `SMTP_PASSWORD`: *(Your app password)*
   - `CONTACT_RECIPIENT_EMAIL`: *(Your email)*
6. Click **Deploy Web Service**. Render will build and launch your site at a live `https://*.onrender.com` URL within 2 minutes!

---

### Method 2: Railway
1. Sign up at [Railway.app](https://railway.app/).
2. Click **New Project** $\to$ **Deploy from GitHub repo**.
3. Select your repository. Railway automatically detects Python and Flask.
4. Add your environment variables in the **Variables** tab.
5. In **Settings** $\to$ **Networking**, click **Generate Domain**.

---

### Method 3: PythonAnywhere
1. Create a free account on [PythonAnywhere.com](https://www.pythonanywhere.com/).
2. Go to the **Web** tab and click **Add a new web app**.
3. Select **Manual Configuration** $\to$ **Python 3.10+**.
4. In the **Virtualenv** section, enter the path to your virtual environment.
5. In the **WSGI configuration file**, point it to your `app.py`:
   ```python
   import sys
   path = '/home/yourusername/Personal'
   if path not in sys.path:
       sys.path.append(path)
   from app import app as application
   ```
6. Click **Reload your web app**.

---

### Method 4: Static Export to GitHub Pages
If you want zero-cost static hosting directly on GitHub Pages:

1. Run the static exporter:
   ```powershell
   python export_static.py
   ```
   This generates a completely self-contained static build inside the `dist/` directory, including `index.html`, all project pages, `robots.txt`, `sitemap.xml`, static images, CSS, and resume PDF.

2. Deploy the `dist` folder to GitHub Pages:
   ```powershell
   # Install gh-pages or push dist to gh-pages branch
   git subtree push --prefix dist origin gh-pages
   ```
3. In your GitHub repository:
   - Go to **Settings** $\to$ **Pages**.
   - Under **Build and deployment**, select source: **Deploy from a branch**.
   - Branch: `gh-pages` / `/ (root)`.
   - Click **Save**. Your site will be live at `https://<your-username>.github.io/personal-portfolio/`.

---

## 9. Connecting a Custom Domain

Once deployed (e.g. on Render, Railway, or GitHub Pages), you can attach your own professional domain (e.g., `www.pradeepkumar.dev` or `pradeepkumar.in`):

1. **Purchase a domain** from Namecheap, Cloudflare Registrar, Google Domains (Squarespace), or GoDaddy.
2. In your hosting platform (e.g., Render Web Service $\to$ **Settings** $\to$ **Custom Domains**):
   - Enter your domain: `www.yourname.dev` and `yourname.dev`.
3. In your Domain Registrar's **DNS Management Console**, add the following records:
   | Type | Name / Host | Value / Target | TTL |
   | :--- | :--- | :--- | :--- |
   | **CNAME** | `www` | `<your-service>.onrender.com` | Automatic / 300 |
   | **A** (or ALIAS) | `@` | `216.24.57.1` *(provided by your host)* | Automatic / 300 |
4. **SSL / HTTPS**:
   Render, Railway, Cloudflare, and GitHub Pages automatically issue a free **Let's Encrypt SSL Certificate** for your custom domain within 15–30 minutes of DNS verification.

---

## 10. Google Search Indexing & SEO Setup

To ensure recruiters and hiring managers find your portfolio when searching your name on Google:

### Step 1: Verify Ownership on Google Search Console
1. Visit [Google Search Console](https://search.google.com/search-console).
2. Click **Add Property** and enter your live URL (e.g. `https://www.yourname.dev`).
3. Choose verification method:
   - **HTML Tag**: Copy the `<meta name="google-site-verification" content="..." />` tag and paste it inside `<head>` in `templates/index.html`.
   - **DNS TXT Record**: Add the TXT record to your domain's DNS manager.
4. Click **Verify**.

### Step 2: Submit Your Sitemap
1. In Google Search Console, click **Sitemaps** on the left menu.
2. Under "Add a new sitemap", enter:
   ```text
   sitemap.xml
   ```
3. Click **Submit**. Google will discover and crawl your pages (`/`, `/#about`, `/#skills`, `/#projects`, and `/project/<slug>`).

### Step 3: Test Crawler Access (`robots.txt`)
Verify that search engines can read your directives by visiting:
`https://your-domain.com/robots.txt`

### Step 4: Request Immediate Indexing
1. Use the URL Inspection tool at the top of Google Search Console.
2. Paste `https://your-domain.com/`.
3. Click **Request Indexing**. Your portfolio will typically be indexed within 24 to 48 hours.

---

## 11. Security & Best Practices

- **Zero Hardcoded Secrets**: All sensitive credentials (SMTP passwords, secret keys) reside in environment variables (`.env`), which are strictly ignored in `.gitignore`.
- **Spam Protection**: The contact form features an invisible honeypot field (`#formWebsite`). Automated spam bots fill this field, resulting in their requests being silently dropped without polluting your logs or inbox.
- **Input Sanitization**: Email formats and message lengths are rigorously validated on both the client side and the server side before storage or transmission.
- **Fail-Safe Message Storage**: Even if SMTP credentials are not configured or the email provider experiences downtime, contact inquiries are persisted safely to `data/contact_messages.json`.

---

## License

This project is open source and available under the [MIT License](LICENSE). Feel free to customize and expand it as you progress in your engineering career!
