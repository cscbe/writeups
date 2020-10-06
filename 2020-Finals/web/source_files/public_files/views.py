from django.views.generic.edit import CreateView
from tweets.models import Tweet
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

@method_decorator(login_required, name='dispatch')
class TweetView(UserPassesTestMixin, CreateView):
    model = Tweet
    fields = ['text', 'link', 'link_text']

    def test_func(self):
        return self.request.user.username != 'admin'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tweets:self')


@method_decorator(login_required, name='dispatch')
class UserTweetView(PermissionRequiredMixin, DetailView):
    model = User
    template_name = 'tweets/user.html'
    context_object_name = 'profile'

    def has_permission(self):
        return self.get_object() == self.request.user or self.request.user.has_perm('tweets.view_tweet')

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if 'username' not in self.kwargs:
            return self.request.user

        return queryset.get(username=self.kwargs['username'])


@method_decorator(login_required, name='dispatch')
class TweetDetailView(PermissionRequiredMixin, DetailView):
    model = Tweet
    template_name = 'tweets/tweet.html'

    def has_permission(self):
        return self.get_object().user == self.request.user or self.request.user.has_perm('tweets.view_tweet')

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        return queryset.get(pk=self.kwargs['pk'])