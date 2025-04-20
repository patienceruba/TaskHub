from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='slider_images/')
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.title