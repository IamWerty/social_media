from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True, null=True)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)
    followers = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='user_followers')
    read_works = models.ManyToManyField('Library_app.Book', blank=True, related_name='read_by_users')
    channels = models.ManyToManyField('Library_app.Channel', blank=True, related_name='subscribed_users')

    groups = models.ManyToManyField('auth.Group', related_name='customuser_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_user_permissions')

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.username})
