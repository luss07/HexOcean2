from django.contrib.auth.models import AbstractUser
from django.db import models


class AccountType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    full_image_link_access = models.BooleanField()
    expiring_image_link = models.BooleanField()
    expiring_image_link_persistence_seconds_from = models.PositiveIntegerField(default=300)
    expiring_image_link_persistence_seconds_to = models.PositiveIntegerField(default=30000)

    def __str__(self):
        return self.name


class AccountTypeThumbnailOption(models.Model):
    account_type = models.ManyToManyField(AccountType, related_name='thumbnail_options')
    name = models.CharField(max_length=255, unique=True)
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()

    class Meta:
        unique_together = ('height', 'width')

    def __str__(self):
        return self.name


class User(AbstractUser):
    account_type = models.ForeignKey(AccountType, null=True, blank=True, on_delete=models.PROTECT)
