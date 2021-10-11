from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from cricket.models import *


class teamsignupform(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super(teamsignupform, self).save(commit=False)
        user.is_cricket = True
        user.save()
        return user
