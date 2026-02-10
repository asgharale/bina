from django.urls import path
from .views import webcam_detect_view

urlpatterns = [
    path('', webcam_detect_view, name='webcam_detect'),
]