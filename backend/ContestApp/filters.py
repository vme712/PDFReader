import django_filters.rest_framework as filters

from ContestApp.models import (ContestResultModel, ContestResultConfigModel, ResultModel)


class ContestResultFilter(filters.FilterSet):
    class Meta:
        model = ContestResultModel
        fields = {
            'contest__id': ['exact'],
            'is_draft': ['exact'],
        }


class ContestResultConfigFilter(filters.FilterSet):
    class Meta:
        model = ContestResultConfigModel
        fields = {
            'contest_result__id': ['exact'],
            'contest_result__contest__id': ['exact'],
            'is_check': ['exact'],
        }


class ResultFilter(filters.FilterSet):
    class Meta:
        model = ResultModel
        fields = {
            'contest_result__id': ['exact'],
            'contest_result__contest__id': ['exact'],
            'is_verified': ['exact'],
            'is_download': ['exact'],
            'is_winner': ['exact'],
        }
