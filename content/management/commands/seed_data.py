"""
Seed initial UGHE website content and create predefined test users.

Usage:
    python manage.py seed_data
"""
import io
import os
from pathlib import Path

import requests
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image, ImageDraw, ImageFont

from content.models import HeroSlide, NavigationItem, SiteSettings, Statistic, WebsiteSection

User = get_user_model()

# Official UGHE website images (https://ughe.org)
HERO_IMAGE_URLS = [
    'https://ughe.org/wp-content/uploads/2026/08/55325793932_50dfe2e107_k.jpg',
    'https://ughe.org/wp-content/uploads/2026/05/55269586520_bb7163c180_5k-scaled.jpg',
    'https://ughe.org/wp-content/uploads/2026/07/IMG_2169-scaled.jpg',
]
LOGO_IMAGE_URL = 'https://ughe.org/wp-content/uploads/2026/10/cropped-Shield-UGHE-270x270.png'


def create_placeholder_image(width, height, bg_color, text_lines, filename='placeholder.jpg'):
    """Create a branded placeholder image when remote downloads fail."""
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
        small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
    except OSError:
        font = ImageFont.load_default()
        small = font

    y = height // 2 - 40
    for i, line in enumerate(text_lines):
        f = font if i == 0 else small
        bbox = draw.textbbox((0, 0), line, font=f)
        tw = bbox[2] - bbox[0]
        draw.text(((width - tw) / 2, y), line, fill=(255, 255, 255), font=f)
        y += 44

    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    buffer.seek(0)
    return ContentFile(buffer.read(), name=filename)


def download_image(url, filename, timeout=20):
    """Download an image from a URL; return ContentFile or None on failure."""
    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; UGHE-Test-Web-App/1.0)'},
        )
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', '')
        if 'image' not in content_type:
            return None
        return ContentFile(response.content, name=filename)
    except Exception:
        return None


class Command(BaseCommand):
    help = 'Seed UGHE navigation, slides, statistics, settings, and test users.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Clear existing content and re-seed.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        force = options['force']
        self.stdout.write(self.style.NOTICE('Seeding UGHE Test Web App data...'))

        self._create_users()

        if force:
            HeroSlide.objects.all().delete()
            NavigationItem.objects.all().delete()
            Statistic.objects.all().delete()
            WebsiteSection.objects.all().delete()
            SiteSettings.objects.all().delete()
            self.stdout.write('Cleared existing content (--force).')

        self._seed_navigation()
        self._seed_statistics()
        self._seed_settings()
        self._seed_sections()
        self._seed_slides()

        self.stdout.write(self.style.SUCCESS('Seed data completed successfully.'))

    def _create_users(self):
        admin_username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        admin_email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@ughe.test')
        admin_password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'UgheAdmin2024!')

        test_username = os.getenv('TEST_USER_USERNAME', 'ughe_user')
        test_email = os.getenv('TEST_USER_EMAIL', 'user@ughe.test')
        test_password = os.getenv('TEST_USER_PASSWORD', 'UgheTest2024!')

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password,
            )
            self.stdout.write(f'Created superuser: {admin_username}')
        else:
            self.stdout.write(f'Superuser already exists: {admin_username}')

        if not User.objects.filter(username=test_username).exists():
            User.objects.create_user(
                username=test_username,
                email=test_email,
                password=test_password,
                first_name='UGHE',
                last_name='Tester',
            )
            self.stdout.write(f'Created test user: {test_username}')
        else:
            self.stdout.write(f'Test user already exists: {test_username}')

    def _seed_navigation(self):
        if NavigationItem.objects.exists():
            self.stdout.write('Navigation items already exist — skipping.')
            return

        primary = [
            ('About Us', '/about', True),
            ('Academics', '/academics', True),
            ('Research', '/research', False),
            ('Centres and Institutes', '/centres', True),
            ('Admissions', '/admissions', True),
            ('News and Events', '/news', True),
        ]
        for order, (title, url, dropdown) in enumerate(primary, start=1):
            NavigationItem.objects.create(
                title=title,
                url=url,
                display_order=order,
                has_dropdown=dropdown,
                nav_type='primary',
                is_active=True,
            )

        actions = [
            ('APPLY', '/apply'),
            ('GET INVOLVED', '/get-involved'),
            ('MEET THE TEAM', '/team'),
            ('MORE', '/more'),
        ]
        for order, (title, url) in enumerate(actions, start=1):
            NavigationItem.objects.create(
                title=title,
                url=url,
                display_order=order,
                has_dropdown=False,
                nav_type='action',
                is_active=True,
            )
        self.stdout.write('Created navigation items.')

    def _seed_statistics(self):
        if Statistic.objects.exists():
            self.stdout.write('Statistics already exist — skipping.')
            return

        stats = [
            ('128', 'Trained community members through UGHE entrepreneurship initiatives'),
            ('1,260', 'Community members employed for Campus projects'),
            (
                '677',
                'Leaders across 61 countries trained in our Executive Education since 2016',
            ),
            (
                '4TH',
                'Among 129 Universities in Sub-Saharan Africa (Times Higher Education Rankings 2024)',
            ),
        ]
        for order, (number, description) in enumerate(stats, start=1):
            Statistic.objects.create(
                number=number,
                description=description,
                display_order=order,
                is_active=True,
            )
        self.stdout.write('Created statistics.')

    def _seed_settings(self):
        if SiteSettings.objects.exists():
            self.stdout.write('Site settings already exist — skipping.')
            return

        settings_obj = SiteSettings(
            university_name='University of Global Health Equity',
            contact_email='info@ughe.org',
            contact_phone='+250 788 123 456',
            address='Butaro Campus, Burera District, Northern Province, Rwanda',
            is_active=True,
        )
        logo = download_image(LOGO_IMAGE_URL, 'ughe-logo.png')
        if logo is None:
            logo = create_placeholder_image(
                200,
                200,
                (177, 18, 23),
                ['UGHE', 'University of', 'Global Health Equity'],
                'ughe-logo.jpg',
            )
            self.stdout.write(self.style.WARNING('Used placeholder logo.'))
        settings_obj.logo.save(logo.name, logo, save=False)
        settings_obj.save()
        self.stdout.write('Created site settings.')

    def _seed_sections(self):
        if WebsiteSection.objects.exists():
            self.stdout.write('Website sections already exist — skipping.')
            return

        WebsiteSection.objects.create(
            title='About UGHE',
            description=(
                'The University of Global Health Equity is a new kind of university '
                'focused on delivering the highest quality medical and health sciences '
                'education based on the latest science and focused on equity.'
            ),
            button_text='Learn more',
            button_url='/about',
            display_order=1,
            is_active=True,
        )
        self.stdout.write('Created website sections.')

    def _seed_slides(self):
        if HeroSlide.objects.exists():
            self.stdout.write('Hero slides already exist — skipping.')
            return

        slides = [
            {
                'title': 'The Inaugural Paul E. Farmer Butaro Dialogues',
                'description': (
                    "Leaders, partners, students, and health practitioners gathered at "
                    "UGHE's Butaro Campus to advance innovation for maternal and newborn health"
                ),
                'button_text': 'Explore more',
                'button_url': '/news/butaro-dialogues',
                'filename': 'butaro-dialogues.jpg',
            },
            {
                'title': 'Educating the Next Generation of Global Health Leaders',
                'description': (
                    'UGHE trains physicians and health professionals committed to '
                    'delivering equitable healthcare in underserved communities worldwide.'
                ),
                'button_text': 'Explore more',
                'button_url': '/academics',
                'filename': 'ughe-education.jpg',
            },
            {
                'title': 'Research and Innovation for Health Equity',
                'description': (
                    'Our centres and institutes advance research that strengthens health '
                    'systems and improves outcomes for communities across Africa and beyond.'
                ),
                'button_text': 'Explore more',
                'button_url': '/research',
                'filename': 'ughe-research.jpg',
            },
        ]

        media_dir = Path(__file__).resolve().parents[3] / 'media' / 'heroes'
        media_dir.mkdir(parents=True, exist_ok=True)

        for order, slide in enumerate(slides, start=1):
            image_file = None
            url_index = order - 1
            if url_index < len(HERO_IMAGE_URLS):
                image_file = download_image(HERO_IMAGE_URLS[url_index], slide['filename'])

            if image_file is None:
                image_file = create_placeholder_image(
                    1600,
                    700,
                    (100, 20, 25) if order % 2 else (60, 80, 90),
                    [slide['title'][:50], 'University of Global Health Equity'],
                    slide['filename'],
                )
                self.stdout.write(
                    self.style.WARNING(
                        f'Used placeholder image for slide: {slide["title"]}'
                    )
                )

            hero = HeroSlide(
                title=slide['title'],
                description=slide['description'],
                button_text=slide['button_text'],
                button_url=slide['button_url'],
                display_order=order,
                is_active=True,
            )
            hero.image.save(slide['filename'], image_file, save=False)
            hero.save()

        self.stdout.write('Created hero slides.')
