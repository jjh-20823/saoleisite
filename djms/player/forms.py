from django import forms

from .models import Player

# TODO Add a confirmaion here
class BindPlayerForm(forms.Form):
    player = forms.ModelChoiceField(
        queryset=Player.objects.filter(user__isnull=True)
    )  
