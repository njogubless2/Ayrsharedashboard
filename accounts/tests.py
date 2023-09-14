from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

CustomUser = get_user_model()

class CustomUserTests(TestCase):

    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.client = APIClient()

    def test_create_user(self):
        response = self.client.post('/api/user/', self.user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CustomUser.objects.count(), 2)  # Assuming you already have an admin user

    def test_user_login(self):
        response = self.client.post('/api/token/', {'email': 'test@example.com', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data)

    def test_get_user_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/user/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'test@example.com')
