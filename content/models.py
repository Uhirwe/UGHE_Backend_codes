"""
Content models for the UGHE Test Web App.
All homepage dynamic content is managed through these models via Django Admin.
"""
from django.db import models


class NavigationItem(models.Model):
    """Primary navigation link shown in the site header."""

    NAV_TYPE_CHOICES = [
        ('primary', 'Primary Navigation'),
        ('action', 'Action Button'),
    ]

    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255, help_text='Relative path or absolute URL')
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    has_dropdown = models.BooleanField(
        default=False,
        help_text='Show a dropdown chevron next to the link',
    )
    nav_type = models.CharField(
        max_length=20,
        choices=NAV_TYPE_CHOICES,
        default='primary',
    )

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'Navigation Item'
        verbose_name_plural = 'Navigation Items'

    def __str__(self):
        return self.title


class HeroSlide(models.Model):
    """Hero carousel slide displayed on the homepage."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='heroes/')
    button_text = models.CharField(max_length=100, default='Explore more')
    button_url = models.CharField(max_length=255, default='#')
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'Hero Slide'
        verbose_name_plural = 'Hero Slides'

    def __str__(self):
        return self.title


class Statistic(models.Model):
    """Facts & Stats card displayed on the homepage."""

    number = models.CharField(
        max_length=50,
        help_text='Display value, e.g. 128, 1,260, or 4TH',
    )
    description = models.TextField()
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'Statistic'
        verbose_name_plural = 'Statistics'

    def __str__(self):
        return f'{self.number} — {self.description[:40]}'


class WebsiteSection(models.Model):
    """Optional supporting content section below Facts & Stats."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='sections/', blank=True, null=True)
    button_text = models.CharField(max_length=100, blank=True)
    button_url = models.CharField(max_length=255, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'Website Section'
        verbose_name_plural = 'Website Sections'

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    """
    Singleton-style site branding and contact settings.
    Use only one active record; the API returns the first active instance.
    """

    university_name = models.CharField(
        max_length=255,
        default='University of Global Health Equity',
    )
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    contact_email = models.EmailField(blank=True, default='info@ughe.org')
    contact_phone = models.CharField(max_length=50, blank=True, default='')
    address = models.TextField(blank=True, default='Butaro, Burera District, Rwanda')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.university_name
