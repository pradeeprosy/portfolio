"""
Automated Unit Test Suite for Activity, Education & Certificate Hub
"""

import unittest
import json
import os
import io
import database
from app import app, ADMIN_PIN

class HubTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        database.init_db()

    def test_database_baseline_data(self):
        """Test that profile, multi-stage education, and baseline certificates exist."""
        profile = database.get_profile()
        self.assertIn("Pradeep Kumar Suresh", profile['name'])
        self.assertEqual(profile['email'], "pradeepsuresh103@gmail.com")

        edu_list = database.get_education_list()
        self.assertGreaterEqual(len(edu_list), 3)  # College, 12th, 10th

        levels = [e['level'] for e in edu_list]
        self.assertTrue(any('College' in l or 'Degree' in l for l in levels))
        self.assertTrue(any('12th' in l or 'Higher' in l for l in levels))
        self.assertTrue(any('10th' in l or 'Secondary' in l for l in levels))

        certs = database.get_certificates()
        self.assertGreaterEqual(len(certs), 1)

    def test_home_page_renders(self):
        """Test public home page returns HTTP 200 with all core sections."""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)
        self.assertIn("Pradeep Kumar Suresh", html)
        self.assertIn('id="education"', html)
        self.assertIn('id="certificates"', html)
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

    def test_multi_milestone_education_api(self):
        """Test adding, editing, and querying multi-stage education records."""
        # Unauthenticated without PIN
        res_unauth = self.client.post('/api/education', json={
            "institution": "Test School",
            "degree": "10th SSLC",
            "timeline": "2021 - 2022"
        })
        self.assertEqual(res_unauth.status_code, 401)

        # Add new education milestone with PIN
        res = self.client.post('/api/education', json={
            "level": "Diploma / Polytechnic",
            "degree": "Diploma in Computer Technology",
            "major": "Computer Technology",
            "institution": "State Polytechnic College",
            "board": "DOTE",
            "timeline": "2020 - 2022",
            "cgpa": "91%",
            "status": "Completed",
            "description": "Practical foundation in electronics and coding.",
            "coursework": "C Programming, Digital Electronics",
            "admin_pin": ADMIN_PIN
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue(data['success'])
        new_id = data['education']['id']

        # Verify record exists
        edu_rec = database.get_education_by_id(new_id)
        self.assertIsNotNone(edu_rec)
        self.assertEqual(edu_rec['institution'], "State Polytechnic College")
        self.assertEqual(edu_rec['cgpa'], "91%")

        # Update record with PIN
        res_upd = self.client.put(f'/api/education/{new_id}', json={
            "institution": "Updated Polytechnic College",
            "degree": "Diploma in Computer Technology",
            "timeline": "2020 - 2022",
            "cgpa": "93%",
            "admin_pin": ADMIN_PIN
        })
        self.assertEqual(res_upd.status_code, 200)
        self.assertEqual(database.get_education_by_id(new_id)['cgpa'], "93%")

        # Delete record
        self.client.post('/api/auth/verify', json={"pin": ADMIN_PIN})
        res_del = self.client.delete(f'/api/education/{new_id}')
        self.assertEqual(res_del.status_code, 200)
        self.assertIsNone(database.get_education_by_id(new_id))

    def test_certificate_crud_and_upload(self):
        """Test adding, uploading, and deleting certificates."""
        # 1. Unauthenticated add fails
        res_unauth = self.client.post('/api/certificates', json={
            "title": "AWS Cloud Practitioner",
            "issuer": "Amazon Web Services"
        })
        self.assertEqual(res_unauth.status_code, 401)

        # 2. Add certificate with file upload
        data = {
            'title': '10th Standard State Board Marksheet',
            'issuer': 'State Board of Tamil Nadu',
            'issue_date': 'May 2022',
            'category': 'Academic Certificate',
            'credential_id': 'SSLC-2022-9842',
            'description': 'Verified secondary school completion.',
            'admin_pin': ADMIN_PIN,
            'certificate_file': (io.BytesIO(b'%PDF-1.4 test certificate pdf content'), 'marksheet_10th.pdf')
        }
        res_upload = self.client.post('/api/certificates', data=data, content_type='multipart/form-data')
        self.assertEqual(res_upload.status_code, 201)
        data_resp = json.loads(res_upload.get_data(as_text=True))
        self.assertTrue(data_resp['success'])
        cert_id = data_resp['certificate']['id']
        file_path = data_resp['certificate']['file_path']
        self.assertIn('.pdf', file_path)

        # 3. Query certificate list
        res_list = self.client.get('/api/certificates?category=academic')
        self.assertEqual(res_list.status_code, 200)
        certs = json.loads(res_list.get_data(as_text=True))
        self.assertTrue(any(c['id'] == cert_id for c in certs))

        # 4. Delete certificate
        self.client.post('/api/auth/verify', json={"pin": ADMIN_PIN})
        res_del = self.client.delete(f'/api/certificates/{cert_id}')
        self.assertEqual(res_del.status_code, 200)
        self.assertIsNone(database.get_certificate_by_id(cert_id))

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
