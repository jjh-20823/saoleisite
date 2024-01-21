from django.urls import path

from . import views

app_name = "video"
urlpatterns = [
    path("", views.VideoListView.as_view(), name="video_list"),
    path("<int:pk>/", views.VideoDetailView.as_view(), name="video_detail"),
    path("upload/", views.UploadView.as_view(), name="upload"),
]
