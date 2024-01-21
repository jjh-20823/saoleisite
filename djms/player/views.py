from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, FormView

from .models import Player
from .forms import BindPlayerForm


# this is just a simple players list, not a ranking
class PlayerListView(ListView):
    # model = Player
    queryset = Player.objects.filter(is_banned=False).order_by("pid")
    # context_object_name = "player_list"
    template_name = "player/player_list.html"
    
def player_zone(request, pid):
    player = get_object_or_404(Player, pid=pid)
    context = {
        'player': player, 
        'video_list': player.video_set.all()
        # more modules in the future, eg: record: player.record.get()
    }
    # if visiting own zone
    if request.user.is_authenticated and request.user.player.exists() and request.user.player.get().pid == pid:
        return render(request, 'player/my_zone.html', context)
    # tohers
    else:
        return render(request, 'player/player_zone.html', context)

@login_required
def become_player(request):
    if request.user.player.exists(): # user is already binded to a player
        current_pid = request.user.player.get().pid
    else:
        current_pid = None
    context = {
        'current_pid': current_pid
    }
    return render(request, 'player/become_player.html', context)

class CreatePlayerView(LoginRequiredMixin, CreateView):
    model = Player
    fields = ['name', 'pid'] # pid should not be in the field in the future
    template_name = 'player/form.html'
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if request.user.player.exists(): # do not allow a user to bind mutiple players
            return self.form_invalid(form)
        else:
            return self.form_valid(form)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
        
class BindPlayerView(LoginRequiredMixin, FormView):
    form_class = BindPlayerForm
    template_name = 'player/form.html'
    success_url = '/'

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     pid = form.cleaned_data["pid"]
    #     if Player.objects.get(pid=pid): # do not allow a user to bind mutiple players
    #         return self.form_invalid(form)
    #     else:
    #         return self.form_valid(form)
    
    def form_valid(self, form):
        p = form.cleaned_data["player"]
        p.user = self.request.user
        p.save()
        return super().form_valid(form)
