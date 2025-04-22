from django.db.models.signals import post_save
from django.dispatch import receiver

from .models.profile_model import Profile
from .models.captured_image_model import CapturedImage
from .models.leaderboard_models import Leaderboard


@receiver(post_save, sender=CapturedImage)
def update_leaderboard_entry(sender, instance, created, **kwargs):
    user = instance.user
    this_entry = Leaderboard.objects.get_or_create(user=user)[0]
    if not this_entry.profile:
        this_entry.profile = Profile.objects.get(user=user)

    # Update the capture number
    this_entry.num_captures = this_entry.num_captures + 1
    this_entry.save()


@receiver(post_save, sender=Leaderboard)
def update_leaderboard(sender, instance, created, **kwargs):
    all_entries = Leaderboard.objects.all().order_by('-num_captures')

    for i in range(len(all_entries)):
        entry = all_entries[i]
        Leaderboard.objects.filter(pk=entry.pk).update(rank=i+1)
