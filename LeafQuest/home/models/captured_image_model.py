"""
Model for user-captured images
Images are stored in the linked IdentRequest
"""
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class CapturedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ident_request = models.ForeignKey('identify_api.IdentRequest', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Image {self.id} uploaded by {self.user.username}"
