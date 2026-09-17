"""
Static Site Exporter for GitHub Pages Deployment
Exports Flask application routes and static assets to a standalone 'dist' folder.
"""

import os
import shutil
from app import app, load_portfolio_data

DIST_DIR = os.path.join(os.path.dirname(__file__), 'dist')

def export_static():
    print(f"Exporting static build to: {DIST_DIR}...")
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR, exist_ok=True)

    client = app.test_client()

    # 1. Export Home Page
    res = client.get('/')
    with open(os.path.join(DIST_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(res.get_data(as_text=True))
    print("[OK] Exported index.html")

    # 2. Export 404 Page
    res_404 = client.get('/nonexistent-page-trigger-404')
    with open(os.path.join(DIST_DIR, '404.html'), 'w', encoding='utf-8') as f:
        f.write(res_404.get_data(as_text=True))
    print("[OK] Exported 404.html")

    # 3. Export robots.txt & sitemap.xml
    res_robots = client.get('/robots.txt')
    with open(os.path.join(DIST_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(res_robots.get_data(as_text=True))
    print("[OK] Exported robots.txt")

    res_sitemap = client.get('/sitemap.xml')
    with open(os.path.join(DIST_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(res_sitemap.get_data(as_text=True))
    print("[OK] Exported sitemap.xml")

    # 4. Export standalone project pages
    data = load_portfolio_data()
    for project in data.get('projects', []):
        slug = project.get('slug')
        if slug:
            proj_dir = os.path.join(DIST_DIR, 'project', slug)
            os.makedirs(proj_dir, exist_ok=True)
            res_p = client.get(f'/project/{slug}')
            with open(os.path.join(proj_dir, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(res_p.get_data(as_text=True))
            print(f"[OK] Exported project/{slug}/index.html")

    # 5. Copy static assets and resume
    shutil.copytree(os.path.join(os.path.dirname(__file__), 'static'), os.path.join(DIST_DIR, 'static'))
    print("[OK] Copied static assets")

    shutil.copytree(os.path.join(os.path.dirname(__file__), 'resume'), os.path.join(DIST_DIR, 'resume'))
    print("[OK] Copied resume directory")

    # 6. Create .nojekyll file for GitHub Pages
    with open(os.path.join(DIST_DIR, '.nojekyll'), 'w') as f:
        pass
    print("[OK] Created .nojekyll for GitHub Pages")

    print(f"\nStatic site generation complete! Ready to deploy '{DIST_DIR}' to GitHub Pages or Netlify.")

if __name__ == '__main__':
    export_static()
