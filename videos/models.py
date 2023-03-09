from django.db import models
from user_manager.models import User

# Create your models here.

class YouTubeVideo(models.Model):
    STATUS_CHOICES = [
        ("new", "new"),
        ("approved", "approved")
    ]
    description = models.TextField(null=True)    
    url = models.CharField(max_length=1500, null=False)
    title = models.CharField(max_length=255, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    video_status = models.CharField(max_length=255, choices=STATUS_CHOICES)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

