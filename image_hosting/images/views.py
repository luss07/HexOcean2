import PIL
import hashlib

from io import BytesIO
import time

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import transaction
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from image_hosting.images.models import Image, ImageThumbnail
from image_hosting.images.serializers import ImageSerializer, ImageListSerializer, CreateExpiringLinkSerializer
from image_hosting.users.permissions import IsCustomer


class ImageViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    # TODO: pagination, filtering
    permission_classes = (IsCustomer,)
    queryset = Image.objects.all()

    def check_permissions(self, request):
        super().check_permissions(request)
        if self.action == 'create_expiring_link':
            if not request.user.account_type.expiring_image_link:
                self.permission_denied(request)

    def get_serializer_class(self):
        if self.action in ['create', 'retrieve']:
            return ImageSerializer
        elif self.action == 'list':
            return ImageListSerializer
        elif self.action == 'create_expiring_link':
            return CreateExpiringLinkSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def perform_create(self, serializer):
        with transaction.atomic():
            instance = serializer.save(owner=self.request.user)
            owner_thumbnail_options = instance.owner.account_type.thumbnail_options.all()
            for option in owner_thumbnail_options:
                original_file = instance.file
                thumb_io = BytesIO()
                image_thumbnail = PIL.Image.open(original_file)
                image_thumbnail.thumbnail((option.height, option.width))
                image_thumbnail.save(thumb_io, image_thumbnail.format)
                thumbnail_instance = ImageThumbnail(
                    original_image=instance,
                    thumbnail_type=option.name,
                )
                thumbnail_instance.file.save(original_file.name, ContentFile(thumb_io.getvalue()))
                thumbnail_instance.save()

    @action(['post'], detail=False, url_path='create_expiring_link')
    def create_expiring_link(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        image = validated_data['image']
        expire_time_seconds = validated_data['time_seconds']
        expire_time = int(time.time()) + expire_time_seconds
        hash_object = hashlib.sha256(f'{image.pk}{expire_time}{settings.SECRET_KEY}'.encode())

        url_path = reverse('expiring-link', args=[image.pk, expire_time, hash_object.hexdigest()])
        url = request.build_absolute_uri(url_path)

        return Response({'expiring_image_url': url}, status=status.HTTP_201_CREATED)


def image_expire_view(request, pk, expire_time, sha):
    hash_object = hashlib.sha256(f'{pk}{expire_time}{settings.SECRET_KEY}'.encode())
    invalid_url_conditions = [
        hash_object.hexdigest() != sha,
        int(time.time()) > expire_time
    ]
    if any(invalid_url_conditions):
        raise Http404
    image = get_object_or_404(Image, pk=pk)
    return FileResponse(image.file)


