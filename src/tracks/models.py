from django.db import models
from django.contrib.auth.models import User


class Track(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    distance_m = models.FloatField()
    assessment = models.IntegerField()

    # Assessment categories
    ASSESSMENT_BAD = 0
    ASSESSMENT_NEUTRAL = 1
    ASSESSMENT_GOOD = 2

    def __str__(self):
        return f'{self.date} - {self.distance_m}'
