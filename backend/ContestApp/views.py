from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, permissions

from ContestApp.filters import (ContestResultFilter, ContestResultConfigFilter, ResultFilter)
from ContestApp.models import (ContestModel, ContestResultModel, ContestResultConfigModel, ResultModel)
from ContestApp.serializers import (ContestSerializer, ContestCreateSerializer, ContestResultSerializer,
                                    ContestResultCreateSerializer, ContestResultConfigSerializer,
                                    ContestResultConfigCreateSerializer, ResultSerializer)
from backend.utils import DeleteMixin


class ContestViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     DeleteMixin,
                     GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ContestSerializer
    queryset = ContestModel.objects.filter(is_delete=False)

    def get_serializer_class(self):
        if self.action in ('create',):
            return ContestCreateSerializer
        return self.serializer_class


class ContestResultViewSet(mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           DeleteMixin,
                           GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ContestResultSerializer
    queryset = ContestResultModel.objects.filter(is_delete=False)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ContestResultFilter

    def get_serializer_class(self):
        if self.action in ('create',):
            return ContestResultCreateSerializer
        return self.serializer_class


class ContestResultConfigViewSet(mixins.CreateModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 DeleteMixin,
                                 GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ContestResultConfigSerializer
    queryset = ContestResultConfigModel.objects.filter(is_delete=False)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ContestResultConfigFilter

    def get_serializer_class(self):
        if self.action in ('create',):
            return ContestResultConfigCreateSerializer
        return self.serializer_class


class ResultViewSet(mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    DeleteMixin,
                    GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ResultSerializer
    queryset = ResultModel.objects.filter(is_delete=False)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ResultFilter
