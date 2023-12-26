# admin.py
from django.contrib import admin
from .models import CustomUser,Plot

admin.site.register(CustomUser)
admin.site.register(Plot)
