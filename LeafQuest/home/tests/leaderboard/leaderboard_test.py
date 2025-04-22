from django.test import TestCase
from django.urls import reverse
from ...models import Profile, Leaderboard
from django.contrib.auth.models import User
from ...views import leaderboard_view
from ... import signals


class LeaderboardTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser', email='test@test.test', password='t3st1ng')
        self.user2 = User.objects.create_user(username='testuser2', email='test2@test.test', password='t3st1ng')
        self.user3 = User.objects.create_user(username='testuser3', email='test3@test.test', password='t3st1ng')
        self.user4 = User.objects.create_user(username='testuser4', email='test4@test.test', password='t3st1ng')
        self.user5 = User.objects.create_user(username='testuser5', email='test5@test.test', password='t3st1ng')

        self.client.user = self.user1
        self.client.force_login(self.user1)

        self.profile1 = Profile.objects.create(user=self.user1, name='Testing', about_me='Hello World', pfp='images/profile/defaultprofile.png')
        self.profile2 = Profile.objects.create(user=self.user2, name='Testing', about_me='Hello World', pfp='images/profile/defaultprofile.png')
        self.profile3 = Profile.objects.create(user=self.user3, name='Testing', about_me='Hello World', pfp='images/profile/defaultprofile.png')
        self.profile4 = Profile.objects.create(user=self.user4, name='Testing', about_me='Hello World', pfp='images/profile/defaultprofile.png')
        self.profile5 = Profile.objects.create(user=self.user5, name='Testing', about_me='Hello World', pfp='images/profile/defaultprofile.png')

        self.leaderboardentry1 = Leaderboard.objects.create(profile=self.profile1, user=self.profile1.user, rank=1, num_captures=5)
        self.leaderboardentry2 = Leaderboard.objects.create(profile=self.profile2, user=self.profile2.user, rank=1, num_captures=5)
        self.leaderboardentry3 = Leaderboard.objects.create(profile=self.profile3, user=self.profile3.user, rank=1, num_captures=3)
        self.leaderboardentry4 = Leaderboard.objects.create(profile=self.profile4, user=self.profile4.user, rank=1, num_captures=1)
        self.leaderboardentry5 = Leaderboard.objects.create(profile=self.profile5, user=self.profile5.user, rank=1, num_captures=0)

        self.leaderboardentry1.save()

    # test that test data is accurate
    def test_entry_fields(self):
        self.assertEqual(self.leaderboardentry1.profile, self.profile1)
        self.assertEqual(self.leaderboardentry1.rank, 1)
        self.assertEqual(self.leaderboardentry1.num_captures, 5)

    # test that uploading a capture as the #1 user causes lower ranks to shift down
    # also test that the most_captures variable updates as expected for this event
    def test_new_number_1_captures(self):
        self.leaderboardentry1.num_captures = self.leaderboardentry1.num_captures + 1
        self.leaderboardentry1.save()

        self.leaderboardentry2.refresh_from_db()
        self.leaderboardentry3.refresh_from_db()

        self.assertEqual(self.leaderboardentry1.rank, 1)
        self.assertEqual(self.leaderboardentry2.rank, 2)
        self.assertEqual(self.leaderboardentry3.rank, 3)

