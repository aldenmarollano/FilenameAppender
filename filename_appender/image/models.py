from django.db import models
from PIL import Image
from django.core.validators import FileExtensionValidator

# Create your models here.
class Images(models.Model):
    image = models.ImageField(max_length=500, null=True, blank=True, validators=[FileExtensionValidator( ['jpg', 'jpeg'] )])

    def __str__(self):
        imagename = self.image.name 
        return  imagename