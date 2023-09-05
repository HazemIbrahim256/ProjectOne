from django.urls import path
from .views import AudioUploadView, AudioListView, AudioTranscriptionView

urlpatterns = [
    path("upload/<str:source_language>/to/<str:target_language>", AudioUploadView.as_view(), name="audio-upload"),
    path('list/', AudioListView.as_view(), name='audio-list'),
    path("transcribe/<str:target_language>/", AudioTranscriptionView.as_view(), name="transcribe"),
]
