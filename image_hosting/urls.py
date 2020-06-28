"""image_hosting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from image_hosting.images.views import ImageViewSet, image_expire_view


swagger_schema_view = get_schema_view(
   openapi.Info(
      title='Image Hosting',
      default_version='1.0',
      description='',
      terms_of_service='',
      contact=openapi.Contact(email=''),
      license=openapi.License(name=''),
   ),
   public=True,
   permission_classes=(AllowAny,),
)

router = DefaultRouter(trailing_slash=False)
router.register('images', ImageViewSet, basename='images')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.jwt')),
    path('images/<int:pk>/<int:expire_time>/<sha>', image_expire_view),
    path('api/', include(router.urls)),
    url(r'^swagger$', swagger_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
