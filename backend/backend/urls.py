"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from FilesApp.views import (FileUploadViewSet)
from UserProfileApp.views import (UserViewSet)
from ContestApp.views import (ContestViewSet, ContestResultViewSet, ContestResultConfigViewSet, ResultViewSet)

# router = routers.SimpleRouter(trailing_slash=False)
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'/users', UserViewSet, basename='users')
router.register(r'/file_load', FileUploadViewSet, basename='file_load')
router.register(r'/contest', ContestViewSet, basename='contest')
router.register(r'/contest_result', ContestResultViewSet, basename='contest_result')
router.register(r'/contest_result_config', ContestResultConfigViewSet, basename='contest_result_config')
router.register(r'/result', ResultViewSet, basename='result')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
