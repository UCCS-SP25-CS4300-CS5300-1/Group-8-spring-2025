"""
Tests that target areas of Django affected by DEBUG=False
"""
from django.test import LiveServerTestCase


class CDTest(LiveServerTestCase):
    def test_css_delivery(self):
        response = self.client.get('/static/css/style.css')
        self.assertEqual(response.status_code, 200)
