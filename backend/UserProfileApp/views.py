from rest_framework import status, mixins, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from .models import User
from .renderers import UserJSONRenderer
from .serializers import (LoginSerializer, RegistrationSerializer, UserDataSerializer)


class UserViewSet(mixins.ListModelMixin,
                  GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserDataSerializer
    queryset = User.objects.none()

    @action(methods=['POST'],
            detail=False,
            permission_classes=(permissions.AllowAny,),
            serializer_class=LoginSerializer)
    def login(self, request):
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
                serializer_data.update({f'{item}': data})
        serializer = self.serializer_class(data=serializer_data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'],
            detail=False,
            permission_classes=(permissions.AllowAny,),
            serializer_class=RegistrationSerializer)
    def register(self, request):
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
                serializer_data.update({f'{item}': data})
        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        serializer = self.serializer_class(data=serializer_data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['GET'],
            detail=False,
            permission_classes=(permissions.IsAuthenticated,),
            serializer_class=UserDataSerializer)
    def user(self, request):
        serializer = self.serializer_class(request.user, data={'user': request.user}, partial=True,
                                           context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
