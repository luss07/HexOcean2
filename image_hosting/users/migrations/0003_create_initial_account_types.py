# Created by Łukasz Setla on 2020-06-28 09:14

from django.db import migrations, transaction

from image_hosting.users.models import AccountTypeThumbnailOption, AccountType


def create_default_account_types(db, app_label):
    small_thumbnail_option = AccountTypeThumbnailOption.objects.get(name='Small')
    medium_thumbnail_option = AccountTypeThumbnailOption.objects.get(name='Medium')

    with transaction.atomic():
        basic_account = AccountType.objects.create(
            name='Basic',
            full_image_link_access=False,
            expiring_image_link=False,
        )
        basic_account.thumbnail_options.set([small_thumbnail_option])

        premium_account = AccountType.objects.create(
            name='Premium',
            full_image_link_access=True,
            expiring_image_link=False,
        )
        premium_account.thumbnail_options.set([small_thumbnail_option, medium_thumbnail_option])

        premium_account = AccountType.objects.create(
            name='Enterprise',
            full_image_link_access=True,
            expiring_image_link=True,
            expiring_image_link_persistence_seconds_from=300,
            expiring_image_link_persistence_seconds_to=30000
        )
        premium_account.thumbnail_options.set([small_thumbnail_option, medium_thumbnail_option])


class Migration(migrations.Migration):
    initial = False
    atomic = False

    dependencies = [
        ('users', '0002_create_initial_thumbnail_options')
    ]

    operations = [
        migrations.RunPython(create_default_account_types)

    ]
