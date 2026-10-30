from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from content.models import NavigationItem, Statistic

User = get_user_model()


class ContentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='tester',
            password='TestPass123!',
        )
        NavigationItem.objects.create(
            title='About Us',
            url='/about',
            display_order=1,
            nav_type='primary',
        )
        Statistic.objects.create(
            number='128',
            description='Test statistic',
            display_order=1,
        )

    def test_navigation_requires_auth(self):
        response = self.client.get('/api/content/navigation/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_navigation_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/content/navigation/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_statistics_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/content/statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['number'], '128')

    def test_login(self):
        response = self.client.post(
            '/api/auth/login/',
            {'username': 'tester', 'password': 'TestPass123!'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
