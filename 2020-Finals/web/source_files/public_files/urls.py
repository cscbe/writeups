from tweets.models import Tweet
from django.urls import path
from . import views


app_name = 'tweets'

urlpatterns = [
    path('new', views.TweetView.as_view(), name='new'),
    path('show/<int:pk>', views.TweetDetailView.as_view(), name='show'),
    path('', views.UserTweetView.as_view(), name='self'),
    path('<str:username>', views.UserTweetView.as_view(), name='profile')
]
