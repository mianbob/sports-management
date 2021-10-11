from django.db import models
from django.conf import settings


class Participant(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField(default=15)
    speciality = models.CharField(max_length=32)
    playerimage = models.ImageField(upload_to='playersimage', null=True)

    class Meta:
        verbose_name_plural = 'Participant'

    def __str__(self):
        return '%s%s%s' % (self.name, self.age, self.speciality)


class CricketTeam(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    teamname = models.CharField(max_length=32)
    logo = models.ImageField(upload_to='cricketteamlogo',
                             default="cricketteamlogo/logo.png")
    captain_name = models.CharField(max_length=32)
    contactno = models.IntegerField(default=0)
    participant = models.ManyToManyField(Participant)
    manager = models.CharField(max_length=32)
    coach = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = 'CricketTeam'

    def __str__(self):
        return '%s%s' % (self.contactno, self.captain_name)

class Training(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    contactno = models.IntegerField(default=0)
    type=models.CharField(max_length=10)
    class Meta:
        verbose_name_plural = 'Training'

    def __str__(self):
        return self.name