from rest_framework import mixins, viewsets
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework import permissions
from rest_framework.request import Request

from FilesApp.models import FileModel
from FilesApp.serializers import FileUploadSerializer


class FileUploadViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = FileUploadSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FileUploadParser)
    queryset = FileModel.objects.none()

    def put(self, request: Request, **kwargs):
        # Raw body contents are stored in `request.data['file']`.
        # Multipart form fields are also stored in `request.data`.
        # We use `file` field name for multipart form, thus the file is always
        # stored in the `request.data['file']` regardless
        # of content encoding (raw body/multipart form).
        # Hence we can simply use the POST logic here w/o any modifications.
        return super().create(request)

    def get_object(self):  # pragma: no cover
        """
        Fixes `OPTIONS`: the default one raises AssertionError.
        # See rest_framework.generics.GenericAPIView#get_object
        :return:
        """
        return None
