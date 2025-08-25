from django.db import models

class File(models.Model):
    filedoc = models.FileField(upload_to="uploads/")
