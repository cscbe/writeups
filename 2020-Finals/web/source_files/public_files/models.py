from django.db import models


# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)
    link = models.CharField(max_length=1024)
    link_text = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    admin_verified = models.BooleanField(default=False)
