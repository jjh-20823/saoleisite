from django.urls import path

from . import views

app_name = "player"
urlpatterns = [
    path("", views.PlayerListView.as_view(), name="player_list"),
    path("<int:pid>/", views.player_zone, name="player_zone"),
    path("become/", views.become_player, name="become_player"),
    path("create/", views.CreatePlayerView.as_view(), name="create_player"),
    path("bind/<int:pk>/", views.BindPlayerView.as_view(), name="bind_player"),
]
