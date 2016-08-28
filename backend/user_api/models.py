from django.contrib.auth.models import User, Group
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    description = models.CharField(max_length=30)
    updated = models.DateTimeField(auto_now_add=True)