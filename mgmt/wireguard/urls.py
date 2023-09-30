from django.urls import path, include

from . import views

app_name = "wireguard"
urlpatterns = [
    path("", views.index, name="index"),
    path("server", views.server, name="server"),
]
