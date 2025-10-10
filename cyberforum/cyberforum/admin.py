from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group

admin.site.register(User, BaseUserAdmin)
admin.site.register(Group)
