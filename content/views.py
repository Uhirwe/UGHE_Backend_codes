from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import HeroSlide, NavigationItem, SiteSettings, Statistic, WebsiteSection
from .serializers import (
    HeroSlideSerializer,
    NavigationItemSerializer,
    SiteSettingsSerializer,
    StatisticSerializer,
    WebsiteSectionSerializer,
)


class NavigationListView(generics.ListAPIView):
    """GET /api/content/navigation/"""

    serializer_class = NavigationItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NavigationItem.objects.filter(is_active=True)


class HeroSlideListView(generics.ListAPIView):
    """GET /api/content/slides/"""

    serializer_class = HeroSlideSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HeroSlide.objects.filter(is_active=True)


class StatisticListView(generics.ListAPIView):
    """GET /api/content/statistics/"""

    serializer_class = StatisticSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Statistic.objects.filter(is_active=True)


class WebsiteSectionListView(generics.ListAPIView):
    """GET /api/content/sections/"""

    serializer_class = WebsiteSectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WebsiteSection.objects.filter(is_active=True)


class SiteSettingsView(generics.RetrieveAPIView):
    """GET /api/content/settings/"""

    serializer_class = SiteSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        settings_obj = SiteSettings.objects.filter(is_active=True).first()
        if settings_obj is None:
            settings_obj = SiteSettings.objects.create()
        return settings_obj
