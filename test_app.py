"""
Automated Test Suite for Pradeep Kumar's Portfolio Web Application
"""

import unittest
import json
from app import app, load_portfolio_data

class PortfolioTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_portfolio_json_loads(self):
        """Test that data/portfolio.json exists and loads successfully."""
        data = load_portfolio_data()
        self.assertIn("personal", data)
        self.assertEqual(data["personal"]["name"], "Pradeep Kumar")
        self.assertIn("projects", data)
        self.assertGreaterEqual(len(data["projects"]), 5)
        self.assertIn("skills", data)
        self.assertIn("programming", data["skills"])
        self.assertIn("web", data["skills"])
        self.assertIn("database", data["skills"])
        self.assertIn("ai_ml", data["skills"])
        self.assertIn("tools", data["skills"])

    def test_home_page(self):
        """Test home page returns 200 and contains essential sections."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Pradeep Kumar", html)
        self.assertIn('id="home"', html)
        self.assertIn('id="about"', html)
        self.assertIn('id="skills"', html)
        self.assertIn('id="projects"', html)
        self.assertIn('id="hackathons"', html)
        self.assertIn('id="career"', html)
        self.assertIn('id="education"', html)
        self.assertIn('id="certifications"', html)
        self.assertIn('id="achievements"', html)
        self.assertIn('id="resume"', html)
        self.assertIn('id="contact"', html)

    def test_api_projects_list(self):
        """Test API endpoint /api/projects."""
        response = self.client.get('/api/projects')
        self.assertEqual(response.status_code, 200)
        projects = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(projects, list)
        self.assertGreaterEqual(len(projects), 5)
        slugs = [p.get('slug') for p in projects]
        self.assertIn('ai-powered-college-chatbot', slugs)

    def test_api_project_single(self):
        """Test single project API endpoint /api/projects/<slug>."""
        response = self.client.get('/api/projects/ai-powered-college-chatbot')
        self.assertEqual(response.status_code, 200)
        project = json.loads(response.get_data(as_text=True))
        self.assertEqual(project['title'], "AI-Powered College Chatbot")
        self.assertIn("technologies", project)
        self.assertIn("features", project)

    def test_standalone_project_page(self):
        """Test standalone project detail view."""
        response = self.client.get('/project/ai-powered-college-chatbot')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("AI-Powered College Chatbot", html)
        self.assertIn("Problem Statement", html)

    def test_resume_download(self):
        """Test resume PDF download endpoint."""
        response = self.client.get('/resume/download')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')
        self.assertGreater(len(response.data), 100)

    def test_robots_and_sitemap(self):
        """Test robots.txt and sitemap.xml routes."""
        res_robots = self.client.get('/robots.txt')
        self.assertEqual(res_robots.status_code, 200)
        self.assertIn("Sitemap:", res_robots.get_data(as_text=True))

        res_sitemap = self.client.get('/sitemap.xml')
        self.assertEqual(res_sitemap.status_code, 200)
        self.assertIn("<urlset", res_sitemap.get_data(as_text=True))

    def test_contact_validation(self):
        """Test contact form validation with missing fields and honeypot."""
        # Invalid: missing message
        res = self.client.post('/contact', json={
            "name": "Recruiter Test",
            "email": "recruiter@company.com",
            "message": "Short"
        }, headers={'X-Requested-With': 'XMLHttpRequest'})
        self.assertEqual(res.status_code, 400)

        # Invalid: bad email
        res = self.client.post('/contact', json={
            "name": "Recruiter Test",
            "email": "not-an-email",
            "message": "We would love to discuss an internship opportunity."
        }, headers={'X-Requested-With': 'XMLHttpRequest'})
        self.assertEqual(res.status_code, 400)

        # Valid submission
        res = self.client.post('/contact', json={
            "name": "Jane Recruiter",
            "email": "jane@techcorp.com",
            "message": "Hello Pradeep, we reviewed your projects and would like to invite you for an interview."
        }, headers={'X-Requested-With': 'XMLHttpRequest'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue(data['success'])

if __name__ == '__main__':
    unittest.main()
