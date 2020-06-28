from django.contrib.auth import get_user_model
from django.db import models

from image_hosting.images.utils import create_unique_filename

User = get_user_model()


def image_upload_path(instance, filename):
    new_filename = create_unique_filename(filename)
    return f'{instance.owner.pk}/images/{new_filename}'


def thumbnail_upload_path(instance, filename):
    new_filename = create_unique_filename(filename)
    return f'{instance.original_image.owner.pk}/thumbnails/{new_filename}'


class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    name = models.CharField(max_length=255)
    file = models.ImageField(upload_to=image_upload_path)


class ImageThumbnail(models.Model):
    original_image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='thumbnails')
    thumbnail_type = models.CharField(max_length=255)
    file = models.ImageField(upload_to=thumbnail_upload_path)
