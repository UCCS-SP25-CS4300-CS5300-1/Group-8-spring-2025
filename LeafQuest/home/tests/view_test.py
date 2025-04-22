from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from ..views import *
from ..models import Profile, FriendList, Leaderboard
from django.urls import reverse


class ViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@test.test', password='t3st1ng')
        self.client.login(username='testuser', password='t3st1ng')
        self.profile = Profile.objects.create(user=self.user, name='Testing', about_me='Hello World')
        self.friendlist = FriendList.objects.create(profile=self.profile)
        self.leaderboardentry = Leaderboard.objects.create(profile=self.profile, user=self.profile.user, rank=1, num_captures=2)

    def test_home_page(self):
        request = self.factory.get('')
        request.user = self.user
        res = home_view(request)
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
        request = self.factory.get('/capture/')
        request.user = self.user
        response = capture_view(request)
        self.assertEqual(response.status_code, 200)

    def test_plantdex_view(self):
        request = self.factory.get('/plantdex/')
        request.user = self.user
        response = plantdex_view(request)
        self.assertEqual(response.status_code, 200)

    def test_badges_view(self):
        request = self.factory.get('/badges/')
        request.session = {}
        request.user = self.user

        response = badges_view(request)
        self.assertEqual(response.status_code, 200)

    def test_map_view(self):
        request = self.factory.get('/map/')
        request.user = self.user
        response = map_view(request)
        self.assertEqual(response.status_code, 200)

    def test_social_view(self):
        request = self.factory.get('/social/')
        request.user = self.user
        response = social_view(request)
        self.assertEqual(response.status_code, 200)

    def test_search_view(self):
        response = self.client.get(reverse('search_results'), {'search': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")

    def test_leaderboard_view(self):
        response = self.client.get(reverse('leaderboard_view'))
        self.assertEqual(response.status_code, 200)

    def test_settings_view(self):
        request = self.factory.get('/settings/')
        request.user = self.user
        response = settings_view(request)
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