from django.test import TestCase
from ...models import Profile
from django.contrib.auth.models import User
from ...views import *

class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@test.test', password='t3st1ng')
        self.client.user = self.user
        self.client.force_login(self.user)
        self.profile = Profile.objects.create(user=self.user, name='Testing', aboutMe='Hello World', pfp='images/profile/defaultprofile.png')

    # test that object data is accurate
    def test_profile_info(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.name, 'Testing')
        self.assertEqual(self.profile.aboutMe, 'Hello World')

    # test that profiles can be updated via the editing form
    def test_profile_update(self):
        data = {'name': 'New Name', 'aboutMe': 'New about me text'}
        res = self.client.post('/profile/edit', data)

        # check that request was good and profile information was updated
        self.assertEqual(200, res.status_code)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.name, 'New Name')
        self.assertEqual(self.profile.aboutMe, 'New about me text')