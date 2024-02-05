from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from api.models import Patient,UserData,Vitals
from datetime import datetime
from api.serializers import UserDataSerializer,PatientSerializer,VitalsSerializer
from api.utils import register_user,login_user,get_all_patients
from rest_framework.response import Response



class LoginUserTestCase(TestCase):
    def setUp(self):
        # Create a user in UserData model
        self.user = UserData.objects.create(
            email='example@example.com',
            password='password123',
            firstname='John',
            lastname='Doe',
            contact='1234567890',
            role='P'
            )

    def test_login_user(self):
        # Valid email and password
        email = 'example@example.com'
        password = 'password123'

        response_data, status_code = login_user(email, password)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {'message': 'Login successful'})

    def test_login_user_invalid_email(self):
        # Invalid email format
        email = 'invalidemail'
        password = 'password123'

        response_data, status_code = login_user(email, password)

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {'error': 'Invalid email format'})

    def test_login_user_short_password(self):
        # Password too short
        email = 'test@example.com'
        password = 'pass'

        response_data, status_code = login_user(email, password)

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {'error': 'Password must be at least 5 characters long'})

    def test_login_user_missing_credentials(self):
        # Missing email and password
        email = ''
        password = ''

        response_data, status_code = login_user(email, password)

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {'error': 'Both email and password are required'})

    def test_login_user_invalid_credentials(self):
        # Invalid email or password
        email = 'test@example.com'
        password = 'wrongpassword'

        response_data, status_code = login_user(email, password)

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {'error': 'Invalid email or password'})