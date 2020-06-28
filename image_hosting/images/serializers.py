from rest_framework import serializers

from image_hosting.images.models import Image, ImageThumbnail


class ImageThumbnailSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = ImageThumbnail
        fields = ('thumbnail_type', 'file')
        read_only_fields = fields

    def get_file(self, obj):
        """
        This method and related field is actually
        Django REST Framework bug fix, without it
        file url contains additional 'api/image/'.
        Reason of bug is building absolute url
        with relative path instead of absolute.
        That gives file url which is no one
        is able to access (does not fit media url).
        """
        request = self.context['request']
        return request.build_absolute_uri(f'/{obj.file.url}')


class ImageSerializer(serializers.ModelSerializer):
    original_image = serializers.SerializerMethodField()
    thumbnails = ImageThumbnailSerializer(read_only=True, many=True)

    class Meta:
        model = Image
        fields = ('id', 'owner', 'name', 'file', 'original_image', 'thumbnails')
        read_only_fields = ('id', 'owner', 'original_image', 'thumbnails')
        extra_kwargs = {
            'file': {'write_only': True}
        }

    def get_original_image(self, obj):
        request = self.context['request']
        user_account_type = obj.owner.account_type
        if user_account_type and user_account_type.full_image_link_access:
            return request.build_absolute_uri(f'/{obj.file.url}')


class ImageListSerializer(serializers.HyperlinkedModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='images-detail')

    class Meta:
        model = Image
        fields = ('name', 'details')
        read_only_fields = fields


class CreateExpiringLinkSerializer(serializers.Serializer):
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())
    time_seconds = serializers.IntegerField()

    class Meta:
        fields = ('image', 'time_seconds')

    def validate_image(self, value):
        request = self.context['request']
        if value.owner != request.user:
            raise serializers.ValidationError('You have no permission to this image.')
        return value

    def validate_time_seconds(self, value):
        request = self.context['request']
        user_account_type = request.user.account_type
        min_value = user_account_type.expiring_image_link_persistence_seconds_from
        max_value = user_account_type.expiring_image_link_persistence_seconds_to

        if not min_value <= value <= max_value:
            raise serializers.ValidationError('Value is not in allowed range.')
        return value

