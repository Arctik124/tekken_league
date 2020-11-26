from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    main_char = models.CharField(max_length=20)
    rating = models.IntegerField(default=1000)

    def __str__(self):
        return self.user.username
