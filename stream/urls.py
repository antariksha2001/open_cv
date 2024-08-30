from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Root URL for the stream app
    path('video_feed/', views.camera_feed, name='video_feed'),  # URL for video feed
]
