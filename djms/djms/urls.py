"""
URL configuration for djms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/", include("registration.backends.simple.urls"), name="registration"
    ),  # Simple backend: register and login without any confirmation, see https://django-registration-redux.readthedocs.io/en/latest/simple-backend.html
    path("player/", include("player.urls")),
    path("video/", include("video.urls")),
    path(
        "", lambda request: render(request, "base.html")
    ),  # TODO A temporary main page
]
# Serving files in development
if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]
