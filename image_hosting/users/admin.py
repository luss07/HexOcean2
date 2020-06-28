from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from image_hosting.users.models import AccountType, AccountTypeThumbnailOption

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Account type'), {'fields': ('account_type',)}),
    )


@admin.register(AccountTypeThumbnailOption)
class AccountTypeThumbnailOptionAdmin(admin.ModelAdmin):
    fields = ('name', 'height', 'width')


class AccountTypeThumbnailOptionInLine(admin.TabularInline):
    model = AccountType.thumbnail_options.through
    extra = 0


@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    fields = ('name', 'full_image_link_access', 'expiring_image_link',
              'expiring_image_link_persistence_seconds_from',
              'expiring_image_link_persistence_seconds_to')
    inlines = [AccountTypeThumbnailOptionInLine]
