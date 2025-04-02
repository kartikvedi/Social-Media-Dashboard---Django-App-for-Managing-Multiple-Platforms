from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    twitter_token = models.CharField(max_length=255, blank=True, null=True)
    facebook_token = models.CharField(max_length=255, blank=True, null=True)

class SocialMediaPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class ScheduledPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20)
    content = models.TextField()
    scheduled_time = models.DateTimeField()
    posted = models.BooleanField(default=False)
