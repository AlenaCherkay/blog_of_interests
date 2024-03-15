from django.contrib import admin

# Регистрируем модель на административном сайте
from .models import Topic, Entry
admin.site.register(Topic)
admin.site.register(Entry)