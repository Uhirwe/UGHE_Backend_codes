from django.urls import path

from .views import (
    HeroSlideListView,
    NavigationListView,
    SiteSettingsView,
    StatisticListView,
    WebsiteSectionListView,
)

urlpatterns = [
    path('navigation/', NavigationListView.as_view(), name='content-navigation'),
    path('slides/', HeroSlideListView.as_view(), name='content-slides'),
    path('statistics/', StatisticListView.as_view(), name='content-statistics'),
    path('sections/', WebsiteSectionListView.as_view(), name='content-sections'),
    path('settings/', SiteSettingsView.as_view(), name='content-settings'),
]
