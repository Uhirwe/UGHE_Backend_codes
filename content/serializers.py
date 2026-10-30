from django.conf import settings
from rest_framework import serializers

from .models import HeroSlide, NavigationItem, SiteSettings, Statistic, WebsiteSection


def absolute_media_url(request, file_field):
    """Build an absolute URL for a media file so Next.js can load it."""
    if not file_field:
        return None
    url = file_field.url
    if request is not None:
        return request.build_absolute_uri(url)
    base = getattr(settings, 'PUBLIC_API_URL', 'http://localhost:8000').rstrip('/')
    return f'{base}{url}'


class NavigationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavigationItem
        fields = (
            'id',
            'title',
            'url',
            'display_order',
            'is_active',
            'has_dropdown',
            'nav_type',
        )


class HeroSlideSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HeroSlide
        fields = (
            'id',
            'title',
            'description',
            'image_url',
            'button_text',
            'button_url',
            'display_order',
            'is_active',
        )

    def get_image_url(self, obj):
        return absolute_media_url(self.context.get('request'), obj.image)


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ('id', 'number', 'description', 'display_order', 'is_active')


class WebsiteSectionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = WebsiteSection
        fields = (
            'id',
            'title',
            'description',
            'image_url',
            'button_text',
            'button_url',
            'display_order',
            'is_active',
        )

    def get_image_url(self, obj):
        return absolute_media_url(self.context.get('request'), obj.image)


class SiteSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = (
            'id',
            'university_name',
            'logo_url',
            'contact_email',
            'contact_phone',
            'address',
        )

    def get_logo_url(self, obj):
        return absolute_media_url(self.context.get('request'), obj.logo)
