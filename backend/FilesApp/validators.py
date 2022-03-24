import os

from rest_framework import serializers


def file_type_validate(file):
    name, extension = os.path.splitext(file.name)
    if extension != '.pdf':
        raise serializers.ValidationError('Тип файла должен быть pdf.')
