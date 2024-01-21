from django import forms
from .models import Player

class BindPlayerForm(forms.Form):
    player = forms.ModelChoiceField(queryset=Player.objects.filter(user__isnull=True)) # not effective