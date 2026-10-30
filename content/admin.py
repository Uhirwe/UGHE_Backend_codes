from django.contrib import admin

from .models import HeroSlide, NavigationItem, SiteSettings, Statistic, WebsiteSection


@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'nav_type', 'url', 'display_order', 'has_dropdown', 'is_active')
    list_editable = ('display_order', 'is_active', 'has_dropdown')
    list_filter = ('nav_type', 'is_active')
    search_fields = ('title', 'url')
    ordering = ('display_order',)


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'button_text', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('display_order',)


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('number', 'description', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('number', 'description')
    ordering = ('display_order',)


@admin.register(WebsiteSection)
class WebsiteSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('display_order',)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('university_name', 'contact_email', 'is_active')
    list_filter = ('is_active',)
