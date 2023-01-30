from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.shortcuts import reverse


FRIEND_LIST_STATUS = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
    ]


class CustomUserModel(AbstractUser):
    picture = models.ImageField(blank=True)
    info = models.TextField(max_length=400, blank=True)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('other-user-panel', args=[str(self.username)])


class FriendListModel(models.Model):
    list_owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="list_owner")

    def get_absolute_url(self):
        return reverse('user-friend-list', args=[str(self.list_owner)])


class FriendModel(models.Model):
    friend_list = models.ForeignKey(FriendListModel, on_delete=models.CASCADE, related_name="friend_list")
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friend")
    status = models.CharField(max_length=10, choices=FRIEND_LIST_STATUS)

