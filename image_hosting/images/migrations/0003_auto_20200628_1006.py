# Generated by Django 3.0.7 on 2020-06-28 10:06

from django.db import migrations, models
import image_hosting.images.models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_image_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagethumbnail',
            name='file',
            field=models.ImageField(upload_to=image_hosting.images.models.thumbnail_upload_path),
        ),
    ]
