from django.contrib import admin
from .models import Favorite, Notification

admin.site.register(Favorite)
admin.site.register(Notification)