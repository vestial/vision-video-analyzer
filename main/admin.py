from django.contrib import admin
from main.models import Video


# Register your models here.
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass
