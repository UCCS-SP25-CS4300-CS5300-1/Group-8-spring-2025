from django.test import TestCase
from ...models import Profile, FriendList
from django.contrib.auth.models import User
from ...views import *
from django.urls import reverse


class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.test', password='t3st1ng')
        self.client.user = self.user
        self.client.force_login(self.user)
        self.profile = Profile.objects.create(user=self.user, name='Testing', aboutMe='Hello World', pfp='images/profile/defaultprofile.png')
        self.friendList = FriendList.objects.create(profile=self.profile)

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

    # test that private setting works
    def test_private_profile(self):
        self.user2 = User.objects.create_user(username='testuser2', email='test2@test.test', password='t3st1ng')
        self.profile2 = Profile.objects.create(user=self.user2, name='Testing 2', aboutMe='Hello World', pfp='images/profile/defaultprofile.png', private=True)
        self.friendList2 = FriendList.objects.create(profile=self.profile2)

        res = self.client.get(reverse('profile_view', kwargs={"profile_id": self.user2.id}))
        self.assertContains(res, "Only testuser2's friends can see their pictures and badges")