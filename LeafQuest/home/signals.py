from django.db.models.signals import post_save
from django.dispatch import receiver

from .models.profile_model import Profile
from .models.captured_image_model import CapturedImage
from .models.leaderboard_models import Leaderboard

from .models import Badge
from django.contrib.auth.models import User

from django.db.models.signals import post_migrate
from django.apps import apps
from django.dispatch import receiver

@receiver(post_save, sender=CapturedImage)
def update_leaderboard_entry(sender, instance, created, **kwargs):
    user = instance.user
    this_entry = Leaderboard.objects.get_or_create(user=user)[0]
    if not this_entry.profile:
        this_entry.profile = Profile.objects.get(user=user)

    this_entry.num_captures += 1
    this_entry.save()

    capture_count = this_entry.num_captures
    unlock_milestones = {
        10: "Beginner",
        25: "Intermediate",
        50: "Expert",
        100: "Master",
        200: "Legendary"
    }

    for count, badge_name in unlock_milestones.items():
        if capture_count >= count:
            try:
                badge = Badge.objects.get(name=badge_name)
                if user not in badge.users.all():
                    badge.users.add(user)
            except Badge.DoesNotExist:
                pass 

@receiver(post_save, sender=Leaderboard)
def update_leaderboard(sender, instance, created, **kwargs):
    all_entries = Leaderboard.objects.all().order_by('-num_captures')

    for i in range(len(all_entries)):
        entry = all_entries[i]
        Leaderboard.objects.filter(pk=entry.pk).update(rank=i+1)

@receiver(post_migrate)
def create_default_badges(sender, **kwargs):
    if sender.name != "home":
        return

    from .models import Badge
    from django.core.files.base import ContentFile
    import os

    default_badges = [
        {"name": "Beginner", "description": "Captured 10 unique plants!", "image": "badges/beginner.png"},
        {"name": "Intermediate", "description": "Captured 25 unique plants!", "image": "badges/intermediate.png"},
        {"name": "Expert", "description": "Captured 50 unique plants!", "image": "badges/expert.png"},
        {"name": "Master", "description": "Captured 100 unique plants!", "image": "badges/master.png"},
        {"name": "Legendary", "description": "Captured 200 unique plants!", "image": "badges/legendary.png"},
    ]

    for badge_data in default_badges:
        if not Badge.objects.filter(name=badge_data["name"]).exists():
            badge = Badge(name=badge_data["name"], description=badge_data["description"])
            badge.image.name = badge_data["image"]
            badge.save()
