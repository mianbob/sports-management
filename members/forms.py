from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms
from cricket.models import *


class cricketteamsignupform(UserCreationForm):
    teamname = forms.CharField(max_length=32)
    captainname = forms.CharField(max_length=32)
    mobileno = forms.IntegerField()
    teamlogo = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('teamlogo', 'teamname', 'captainname',
                  'mobileno', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super(cricketteamsignupform, self).save(commit=False)
        user.is_cricket_team = True
        user.save()
        return user
