from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.db.models import Count


class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    friends = models.ManyToManyField('self', symmetrical=True, related_name='friend_with', blank=True)
    follows = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='user_follows')
    read_works = models.ManyToManyField('Library_app.Book', blank=True, related_name='read_by_users')
    channels = models.ManyToManyField('Library_app.Channel', blank=True, related_name='subscribed_users')
    is_private = models.BooleanField(default=False)

    groups = models.ManyToManyField('auth.Group', related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_user_permissions', blank=True)

    def get_absolute_url(self):
        return reverse('profile')

    def delete(self, *args, **kwargs):
        self.friends.clear()
        self.followers.clear()
        self.follows.clear()
        self.read_works.clear()
        self.channels.clear()

        super().delete(*args, **kwargs)
