from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FriendListModel
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_friend_list(sender, instance, created, **kwargs):

    if created:
        FriendListModel.objects.create(list_owner=instance)
