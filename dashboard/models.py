# models.py
from django.db import models

class Header(models.Model):
    background = models.ImageField(upload_to="headers/")

    def __str__(self):
        return f"Header {self.id} - {self.background.name if self.background else 'No Image'}"



class Banner(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="banners/")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title or f"Banner {self.id}"
