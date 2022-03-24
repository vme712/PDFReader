from django.db import models


class FileModel(models.Model):
    def get_file_path(instance, filename):
        import os
        return os.path.join('', filename)

    file = models.FileField(upload_to=get_file_path, verbose_name='Файл')

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return f'{self.file.url}'
