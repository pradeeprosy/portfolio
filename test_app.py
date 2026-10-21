"""
Automated Unit Test Suite for Activity & Education Hub
"""

import unittest
import json
import os
import database
from app import app, ADMIN_PIN

class HubTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        database.init_db()

    def test_database_baseline_data(self):
        """Test that profile and education are seeded properly."""
        profile = database.get_profile()
        self.assertIn("Pradeep Kumar Suresh", profile['name'])
        self.assertEqual(profile['email'], "pradeepsuresh103@gmail.com")

        education = database.get_education()
        self.assertEqual(education['institution'], "Vinayaka Missions University, Salem")
        self.assertEqual(education['timeline'], "2022 - 2026")
        self.assertIn("Python", education['coursework'])

        activities = database.get_activities()
        self.assertGreaterEqual(len(activities), 1)

    def test_home_page_renders(self):
        """Test public home page returns HTTP 200 with all core sections."""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)
        self.assertIn("Pradeep Kumar Suresh", html)
        self.assertIn("Vinayaka Missions University, Salem", html)
        self.assertIn('id="education"', html)
        self.assertIn('id="activities"', html)
        self.assertIn('id="contact"', html)

    def test_admin_pin_verification(self):
        """Test admin PIN verification."""
        # Invalid PIN
        res_fail = self.client.post('/api/auth/verify', json={"pin": "wrongpin"})
        self.assertEqual(res_fail.status_code, 401)

        # Valid PIN
        res_ok = self.client.post('/api/auth/verify', json={"pin": ADMIN_PIN})
        self.assertEqual(res_ok.status_code, 200)
        data = json.loads(res_ok.get_data(as_text=True))
        self.assertTrue(data['success'])

    def test_update_education_api(self):
        """Test updating education credentials."""
        # Unauthenticated without PIN
        res_unauth = self.client.post('/api/education', json={
            "institution": "Vinayaka Missions University, Salem",
            "degree": "Bachelor of Engineering (B.E.)",
            "major": "Computer Science and Engineering",
            "timeline": "2022 - 2026",
            "cgpa": "8.7 / 10"
        })
        self.assertEqual(res_unauth.status_code, 401)

        # With PIN
        res = self.client.post('/api/education', json={
            "institution": "Vinayaka Missions University, Salem",
            "degree": "Bachelor of Engineering (B.E.)",
            "major": "Computer Science and Engineering",
            "timeline": "2022 - 2026",
            "cgpa": "8.7 / 10",
            "status": "In Progress",
            "description": "Updated academic focus",
            "coursework": "Data Structures, Python, Machine Learning",
            "admin_pin": ADMIN_PIN
        })
        self.assertEqual(res.status_code, 200)
        edu = database.get_education()
        self.assertEqual(edu['cgpa'], "8.7 / 10")

    def test_create_and_delete_activity(self):
        """Test publishing and deleting a live activity."""
        # Create
        res = self.client.post('/api/activities', json={
            "title": "Automated Test Activity",
            "category": "Project Milestone",
            "date": "Oct 2026",
            "description": "Testing live activity creation via REST endpoint.",
            "admin_pin": ADMIN_PIN
        })
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue(data['success'])
        act_id = data['activity']['id']

        # Verify in database
        act = database.get_activity_by_id(act_id)
        self.assertIsNotNone(act)
        self.assertEqual(act['title'], "Automated Test Activity")

        # Delete
        # Authenticate first
        self.client.post('/api/auth/verify', json={"pin": ADMIN_PIN})
        res_del = self.client.delete(f'/api/activities/{act_id}')
        self.assertEqual(res_del.status_code, 200)
        self.assertIsNone(database.get_activity_by_id(act_id))

    def test_activity_search_and_filter(self):
        """Test filtering activities by category and search."""
        res_filter = self.client.get('/api/activities?category=projects')
        self.assertEqual(res_filter.status_code, 200)
        acts = json.loads(res_filter.get_data(as_text=True))
        for a in acts:
            self.assertEqual(a['category_slug'], 'projects')

        res_search = self.client.get('/api/activities?search=NLP')
        self.assertEqual(res_search.status_code, 200)

if __name__ == '__main__':
    unittest.main()
