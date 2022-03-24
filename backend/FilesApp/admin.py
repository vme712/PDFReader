from django.contrib import admin

# Register your models here.
from FilesApp.models import FileModel


from django.contrib import admin
from django.utils.html import format_html

from .models import FileModel


@admin.register(FileModel)
class FileModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'link')

    def link(self, obj: FileModel):  # pragma: no cover
        if not obj.file:
            return "-"
        return format_html('<a href="{}" target="_blank" rel="noopener">{}</a>', obj.file.url,
                           obj.file.url)

    link.short_description = 'Ссылка на файл'
