from django.db import models
from django.urls import reverse
from home.models import UserProfile
# Create your models here.


class Battle(models.Model):
    player1 = models.ForeignKey(UserProfile,
                                   on_delete=models.SET('player1'),
                                   related_name="homes_users_related"
                                   )
    player2 = models.ForeignKey(UserProfile,
                                   on_delete=models.SET('player2'),
                                   related_name="homes_users_related2"
                                   )
    max_score = models.IntegerField()
    player1_score = models.IntegerField(default=0, blank=True)
    player2_score = models.IntegerField(default=0, blank=True)
    delta = models.IntegerField(default=0, blank=True)
    winner = models.BooleanField(default=True, blank=True)
    active = models.BooleanField(default=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('battles:battle-detail-id', kwargs={'id': self.id})