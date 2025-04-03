from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from ..views import *
from ..models import Profile, FriendList
from django.urls import reverse


class ViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@test.test', password='t3st1ng')
        self.client.login(username='testuser', password='t3st1ng')
        self.profile = Profile.objects.create(user=self.user, name='Testing', aboutMe='Hello World')
        self.friendlist = FriendList.objects.create(profile=self.profile)

    def test_home_page(self):
        res = home_view(self.factory.get(''))
        self.assertEqual(res.status_code, 200)

    def test_profile_redirect(self):
        request = self.factory.get('/profile/')
        request.session = {}
        request.user = self.user

        response = profile_redir(request)
        self.assertEqual(response.status_code, 302)  # /profile is configured to redirect

    def test_profile_view(self):
        request = self.factory.get('/profile/1')
        request.session = {}
        request.user = self.user

        response = profile_view(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_capture_view(self):
        response = capture_view(self.factory.get('/capture/'))
        self.assertEqual(response.status_code, 200)

    def test_plantdex_view(self):
        response = plantdex_view(self.factory.get('/plantdex/'))
        self.assertEqual(response.status_code, 200)

    def test_badges_view(self):
        request = self.factory.get('/badges/')
        request.session = {}
        request.user = self.user

        response = badges_view(request)
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

    def test_register_view(self):
        self.client.get(reverse('logout'))  # log out first

        response = self.client.post(reverse('register'), {'username': 'testuser2', 'email': 'test2@testing.test', 'password1': 'registert3st', 'password2': 'registert3st'})
        self.assertEqual(response.status_code, 302)

    def test_login_view(self):
        self.client.get(reverse('logout'))  # log out first

        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 't3st1ng'})
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_about_view(self):
        response = about_view(self.factory.get('/about/'))
        self.assertEqual(response.status_code, 200)