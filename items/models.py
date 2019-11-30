from django.db import models
from django.conf import settings

class Image(models.Model):
    image = models.ImageField()

# Create your models here.
class Item(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL,
                            null=True,
                            related_name='items')
    images = models.ManyToManyField(Image)