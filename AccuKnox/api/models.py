from django.db import models
from django.conf import settings

# Create your models here.
class FriendRequest(models.Model):
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='to_user',on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='from_user',on_delete=models.CASCADE)

    PENDING = 'p'
    ACCEPTED = 'a'
    REJECTED = 'r'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected')
    ]

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)