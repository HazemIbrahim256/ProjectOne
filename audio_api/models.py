from django.db import models

# Create your models here.
class Audio(models.Model):
    file = models.FileField(upload_to='audio/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    transcription = models.TextField(blank=True)

    def __str__(self):
        return self.file.name
