from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from ..views import *
from ..models import Profile
from django.urls import reverse


class ViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='testuser', email='test@test.test', password='t3st1ng')
        self.client.login(username='testuser', password='t3st1ng')
        self.profile = Profile.objects.create(user=self.user, name='Testing', aboutMe='Hello World')

    def test_home_page(self):
        res = home_view(self.factory.get(''))
        self.assertEqual(res.status_code, 200)

    def test_profile_view(self):
        request = self.factory.get('/profile/')
        request.session = {}
        request.user = self.user

        response = profile_redir(request)
        self.assertEqual(response.status_code, 302)  # /profile is configured to redirect

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
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_about_view(self):
        response = about_view(self.factory.get('/about/'))
        self.assertEqual(response.status_code, 200)