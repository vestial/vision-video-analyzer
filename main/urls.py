from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("videos/", views.videos, name="videos"),
    path("videos/<int:id>/", views.video, name="video"),
    path("videos/<int:id>/shots", views.shots, name="shots"),
    path("videos/<int:id>/delete", views.delete, name="delete"),
]