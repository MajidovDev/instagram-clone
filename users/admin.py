from django.contrib import admin
from users.models import UserModel, UserConfirmationModel


class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'phone_number']


admin.site.register(UserModel, UserModelAdmin)
admin.site.register(UserConfirmationModel)