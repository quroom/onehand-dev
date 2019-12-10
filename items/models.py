from django.db import models
from django.conf import settings

# Create your models here.
class Item(models.Model):    
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL,
                            null=True,
                            related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Image(models.Model):
    image = models.ImageField()
    item = models.ForeignKey(Item,
                            on_delete=models.CASCADE,
                            related_name='images')