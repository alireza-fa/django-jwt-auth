from django.db.models import Manager
from django.utils import timezone


class NotExpiredManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(expired_at__gt=timezone.now())
