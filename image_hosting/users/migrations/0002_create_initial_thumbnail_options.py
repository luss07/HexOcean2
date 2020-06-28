# Created by Łukasz Setla on 2020-06-28 09:14

from django.db import migrations

from image_hosting.users.models import AccountTypeThumbnailOption


def create_default_thumbnail_options(db, app_label):
    AccountTypeThumbnailOption.objects.bulk_create([
        AccountTypeThumbnailOption(name='Small', height=200, width=200),
        AccountTypeThumbnailOption(name='Medium', height=400, width=400)
    ])


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ('users', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_default_thumbnail_options),

    ]
