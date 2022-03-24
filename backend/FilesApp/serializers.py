from rest_framework import serializers

from .models import FileModel
from .validators import file_type_validate


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = '__all__'

    def to_representation(self, instance):
        return self.fields['file'].to_representation(instance.file)


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(validators=[file_type_validate])

    class Meta:
        model = FileModel
        fields = '__all__'
