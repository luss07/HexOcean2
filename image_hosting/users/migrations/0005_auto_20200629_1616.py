# Generated by Django 3.0.7 on 2020-06-29 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200628_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accounttype',
            name='expiring_image_link_persistence_seconds_from',
        ),
        migrations.RemoveField(
            model_name='accounttype',
            name='expiring_image_link_persistence_seconds_to',
        ),
    ]
