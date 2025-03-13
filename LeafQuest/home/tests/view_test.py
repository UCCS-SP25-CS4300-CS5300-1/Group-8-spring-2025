from django.test import TestCase, RequestFactory

from ..views import *


class ViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_home_page(self):
        res = home_view(self.factory.get(''))
        self.assertEqual(res.status_code, 200)

    def test_profile_view(self):
        response = profile_view(self.factory.get('/profile/'))
        self.assertEqual(response.status_code, 200)

    def test_capture_view(self):
        response = capture_view(self.factory.get('/capture/'))
        self.assertEqual(response.status_code, 200)

    def test_plantdex_view(self):
        response = plantdex_view(self.factory.get('/plantdex/'))
        self.assertEqual(response.status_code, 200)

    def test_badges_view(self):
        response = badges_view(self.factory.get('/badges/'))
        self.assertEqual(response.status_code, 200)

    def test_map_view(self):
        response = map_view(self.factory.get('/map/'))
        self.assertEqual(response.status_code, 200)

    def test_social_view(self):
        response = social_view(self.factory.get('/social/'))
        self.assertEqual(response.status_code, 200)

    def test_settings_view(self):
        response = settings_view(self.factory.get('/settings/'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        response = logout_view(self.factory.get('/logout/'))
        self.assertEqual(response.status_code, 200)

    def test_about_view(self):
        response = about_view(self.factory.get('/about/'))
        self.assertEqual(response.status_code, 200)