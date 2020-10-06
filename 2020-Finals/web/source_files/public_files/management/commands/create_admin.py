from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from tweets.models import Tweet
from os import getenv
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        username = "admin"
        if not User.objects.filter(username=username).exists():
            password = getenv("ADMIN_PASSWORD")
            admin = User.objects.create_user(username=username, password=password)
            tweet_type = ContentType.objects.get(app_label='tweets', model='tweet')
            admin.user_permissions.add(Permission.objects.get(codename='view_tweet', content_type=tweet_type))
            admin.save()
            tweet = Tweet()
            tweet.link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            tweet.link_text = "Congratulations"
            tweet.text = getenv("FLAG")
            tweet.user = admin
            tweet.save()