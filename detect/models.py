from django.db import models


class ImageFeedback(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%m/%d')
    prompt = models.TextField(blank=True)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"بازخورد {self.id}"