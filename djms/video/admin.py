from django.contrib import admin

from .models import Video

admin.site.register(Video)  # so that videos are shown in /admin/
