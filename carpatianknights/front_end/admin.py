from django.contrib import admin
from .models import Photo, File

admin.site.register(Photo)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
