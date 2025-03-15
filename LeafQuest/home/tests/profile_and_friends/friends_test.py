from django.test import TestCase
from django.urls import reverse
from home.models import *
from django.contrib.auth.models import User
from home.views import *

class FriendTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='testuser', email='test@test.test', password='t3st1ng')
        self.user2 = User.objects.create(username='testing', email='test2@test.test', password='t3st1ng')
        self.profile1 = Profile.objects.create(user=self.user1, name='Test User', aboutMe='Hello World')
        self.profile2 = Profile.objects.create(user=self.user2, name='Testing', aboutMe='Hello World')
        self.friendList1 = FriendList.objects.create(profile=self.profile1)
        self.friendList2 = FriendList.objects.create(profile=self.profile2)

    # test that a user can send and cancel friend requests
    def test_friend_req_create_and_cancel(self):
        self.client.user = self.user1
        self.client.force_login(self.user1)

        res = self.client.get(reverse('add_friend', kwargs={"profile_id": self.user2.id}))
        self.assertEqual(302, res.status_code)    # url should redirect

        friend_req_exists = FriendRequest.objects.filter(sender=self.profile1, receiver=self.profile2).exists()
        self.assertTrue(friend_req_exists)

        # Cancel friend request

        res = self.client.get(reverse('cancel_friend', kwargs={"profile_id": self.user2.id}))
        self.assertEqual(302, res.status_code)    # url should redirect

        friend_req_exists = FriendRequest.objects.filter(sender=self.profile1, receiver=self.profile2).exists()
        self.assertFalse(friend_req_exists)

    # test that a friend request can be accepted and users be added to each other's friend lists
    # then, test that a user can remove a friend
    def test_friend_req_accept_and_rm_friend(self):
        # send a friend request from user1 to user2
        self.client.user = self.user1
        self.client.force_login(self.user1)

        res = self.client.get(reverse('add_friend', kwargs={"profile_id": self.user2.id}))
        self.assertEqual(302, res.status_code)    # url should redirect

        friend_req = FriendRequest.objects.get(sender=self.profile1, receiver=self.profile2)

        # log into user2 and accept request
        self.client.user = self.user2
        self.client.force_login(self.user2)

        res = self.client.get(reverse('accept_req', kwargs={'request_id': friend_req.id}))
        self.assertEqual(302, res.status_code)    # url should redirect

        # check that each user's friend list now contains the other user
        self.assertTrue(self.profile1 in self.friendList2.friends.all())
        self.assertTrue(self.profile2 in self.friendList1.friends.all())

        # Removing a friend

        res = self.client.get(reverse('remove_friend', kwargs={"profile_id": self.user1.id}))
        self.assertEqual(302, res.status_code)    # url should redirect

        # check that each user's friend list no longer contains the other user
        self.assertFalse(self.profile1 in self.friendList2.friends.all())
        self.assertFalse(self.profile2 in self.friendList1.friends.all())

    # test that a user can decline a friend request from another user
    def test_friend_req_decline(self):
        # send a friend request from user1 to user2
        self.client.user = self.user1
        self.client.force_login(self.user1)

        res = self.client.get(reverse('add_friend', kwargs={"profile_id": self.user2.id}))
        self.assertEqual(302, res.status_code)    # url should redirect

        friend_req = FriendRequest.objects.get(sender=self.profile1, receiver=self.profile2)

        # log into user2 and accept request
        self.client.user = self.user2
        self.client.force_login(self.user2)

        res = self.client.get(reverse('decline_req', kwargs={'request_id': friend_req.id}))
        self.assertEqual(302, res.status_code)    # url should redirect

        # check that each user's friend list doesn't contain the other user
        self.assertFalse(self.profile1 in self.friendList2.friends.all())
        self.assertFalse(self.profile2 in self.friendList1.friends.all())