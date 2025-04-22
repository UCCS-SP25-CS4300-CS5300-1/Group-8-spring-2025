from django.test import TestCase
from django.urls import reverse
from ...models import Profile, LeaderboardEntry, LeaderboardManager
from django.contrib.auth.models import User
from ...views import leaderboard_view

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

        self.leaderboardentry1 = LeaderboardEntry.objects.create(profile=self.profile1, rank=1, num_captures=5)
        self.leaderboardentry2 = LeaderboardEntry.objects.create(profile=self.profile2, rank=1, num_captures=5)
        self.leaderboardentry3 = LeaderboardEntry.objects.create(profile=self.profile3, rank=2, num_captures=3)
        self.leaderboardentry4 = LeaderboardEntry.objects.create(profile=self.profile4, rank=3, num_captures=1)
        self.leaderboardentry5 = LeaderboardEntry.objects.create(profile=self.profile5, rank=999999, num_captures=0)
        self.leaderboard = LeaderboardManager.objects.create(leaderboard_id=1, most_captures=5, starting_rank=3)

    # test that test data is accurate
    def test_entry_fields(self):
        self.assertEqual(self.leaderboardentry1.profile, self.profile1)
        self.assertEqual(self.leaderboardentry1.rank, 1)
        self.assertEqual(self.leaderboardentry1.num_captures, 5)

    def test_manager_fields(self):
        self.assertEqual(self.leaderboard.leaderboard_id, 1)
        self.assertEqual(self.leaderboard.most_captures, self.leaderboardentry1.num_captures)
        self.assertEqual(self.leaderboard.starting_rank, 3)

    # test that uploading a capture as the #1 user causes lower ranks to shift down
    # also test that the most_captures variable updates as expected for this event
    def test_new_number_1_captures(self):
        self.leaderboard.update_rank(self.leaderboardentry1)
        self.leaderboardentry1.refresh_from_db()
        self.leaderboardentry2.refresh_from_db()
        self.leaderboardentry3.refresh_from_db()
        self.leaderboard.refresh_from_db()
        self.assertEqual(self.leaderboardentry1.rank, 1)
        self.assertEqual(self.leaderboardentry2.rank, 2)
        self.assertEqual(self.leaderboardentry3.rank, 3)
        self.assertEqual(self.leaderboard.most_captures, self.leaderboardentry1.num_captures)

    # test that a user uploading their first capture is placed at the same rank as others with 1 capture
    def test_first_capture_tied(self):
        self.leaderboard.update_rank(self.leaderboardentry5)
        self.leaderboardentry5.refresh_from_db()
        self.leaderboard.refresh_from_db()
        self.assertEqual(self.leaderboardentry5.rank, self.leaderboardentry4.rank) # should be tied
        self.assertEqual(self.leaderboard.starting_rank, 3) # no change

    # test that a user uploading their first capture is placed below others on the leaderboard
    def test_first_capture_not_tied(self):
        self.leaderboard.update_rank(self.leaderboardentry4)
        self.leaderboard.update_rank(self.leaderboardentry5)
        self.leaderboardentry4.refresh_from_db()
        self.leaderboardentry5.refresh_from_db()
        self.leaderboard.refresh_from_db()
        self.assertNotEqual(self.leaderboardentry5.rank, self.leaderboardentry4.rank) # should not be tied
        self.assertEqual(self.leaderboard.starting_rank, 4) # new start rank 

    # test that ranks shift upwards when a rank above them is empty (all users with that rank moved up)
    def test_shift_up(self):
        self.leaderboard.update_rank(self.leaderboardentry3)
        self.leaderboard.update_rank(self.leaderboardentry3)
        self.leaderboardentry4.refresh_from_db()
        self.leaderboardentry5.refresh_from_db()
        self.leaderboard.refresh_from_db()
        self.assertEqual(self.leaderboardentry3.rank, 1)
        self.assertEqual(self.leaderboardentry4.rank, 2)
