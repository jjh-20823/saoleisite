from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
# from django.contrib import messages

from .models import Video
from .video_anal import video_anal
    
class VideoListView(ListView):
    model = Video
    template_name = "video/video_list.html"

class VideoDetailView(DetailView):
    model = Video
    template_name = "video/video.html"
    
class UploadView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Video
    fields = ['file']
    template_name = 'video/upload.html'
    success_message = "上传成功!"
    
    def form_valid(self, form):
        uploaded_file = self.request.FILES["file"]
        form.instance.player = self.request.user.player.get()
        for k, v in video_anal(uploaded_file).items():
            setattr(form.instance, k, v) # TODO not a safe way
        # messages.success(self.request, "上传成功!")
        return super().form_valid(form)
    
    # make sure the user has conntected to a player
    def test_func(self):
        return self.request.user.player.exists()
    