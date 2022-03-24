from rest_framework import serializers

from FilesApp.models import FileModel
from FilesApp.serializers import FileSerializer
from UserProfileApp.serializers import UserDataSerializer
from .models import (ContestModel, ContestResultModel, ContestResultConfigModel, ResultModel)


class ContestCreateSerializer(serializers.ModelSerializer):
    add_user = UserDataSerializer(read_only=True)

    class Meta:
        model = ContestModel
        fields = ('id', 'name', 'link', 'add_user',)

    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}
        validated_data.update({'add_user': self.context['request'].user})
        if self.instance is None:
            self.instance = self.create(validated_data)
        else:
            return self.instance


class ContestSerializer(serializers.ModelSerializer):
    add_user = UserDataSerializer(read_only=True)

    class Meta:
        model = ContestModel
        exclude = ('is_delete',)


class ContestResultCreateSerializer(serializers.ModelSerializer):
    contest = serializers.PrimaryKeyRelatedField(queryset=ContestModel.objects.all())
    file = serializers.PrimaryKeyRelatedField(queryset=FileModel.objects.all())

    class Meta:
        model = ContestResultModel
        fields = ('id', 'contest', 'file',)

    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}
        validated_data.update({'add_user': self.context['request'].user})
        if self.instance is None:
            self.instance = self.create(validated_data)
        else:
            return self.instance


class ContestResultSerializer(serializers.ModelSerializer):
    add_user = UserDataSerializer(read_only=True)
    # contest = ContestSerializer(read_only=True)
    file = FileSerializer(read_only=True)

    class Meta:
        model = ContestResultModel
        exclude = ('is_delete',)
        read_only_fields = ('contest',)


class ContestResultConfigCreateSerializer(serializers.ModelSerializer):
    contest_result = serializers.PrimaryKeyRelatedField(queryset=ContestResultModel.objects.all())

    class Meta:
        model = ContestResultConfigModel
        exclude = ('is_delete', 'is_check',)


class ContestResultConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestResultConfigModel
        exclude = ('is_delete',)
        read_only_fields = ('contest_result', 'is_check',)

    def save(self, **kwargs):
        if self.instance is not None and self.instance.is_check:
            return self.instance
        super().save(**kwargs)


class ResultSerializer(serializers.ModelSerializer):
    file_row = FileSerializer(read_only=True, many=True)

    class Meta:
        model = ResultModel
        exclude = ('is_delete',)
        read_only_fields = ('file_row', 'contest_result', 'is_download', 'is_verified', )

    def save(self, **kwargs):
        if self.instance is not None and self.instance.is_check:
            return self.instance
        super().save(**kwargs)
