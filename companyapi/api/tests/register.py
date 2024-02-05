from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from api.models import Patient,UserData,Vitals
from datetime import datetime
from api.serializers import UserDataSerializer,PatientSerializer,VitalsSerializer
from api.utils import register_user,login_user,get_all_patients
from rest_framework.response import Response




class UserDataViewTestCase(TestCase):
    def setUp(self):
        # Create sample UserData objects for testing
        UserData.objects.create(email='user1@example.com', password='pass123', firstname='User 1', lastname='Smith', contact='1234567890', role='P')
        UserData.objects.create(email='user2@example.com', password='pass456', firstname='User 2', lastname='Doe', contact='9876543210', role='D')

    def test_user_data_view(self):
        # Create a GET request to the userdata endpoint
        url = reverse('userdata')  # Assuming you've named your URL pattern 'userdata'
        response = self.client.get(url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if the response data contains the serialized UserData objects
        expected_data = UserDataSerializer(UserData.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)

    def test_empty_user_data_view(self):
        # Delete all UserData objects to simulate an empty table
        UserData.objects.all().delete()

        # Create a GET request to the userdata endpoint
        url = reverse('userdata')  # Assuming you've named your URL pattern 'userdata'
        response = self.client.get(url)

        # Check if the response status code is 404 NOT FOUND
        self.assertEqual(response.status_code, 404)

        # Check if the response data contains the appropriate error message
        expected_data = {'error': 'Table is Empty'}
        self.assertEqual(response.data, expected_data)





#register
class RegisterUserTestCase(TestCase):
    def test_register_valid_user(self):
        # Valid user data
        valid_data = {
            'email': 'john@example.com',
            'password': 'password123',
            'firstname': 'John',
            'lastname': 'Doe',
            'contact': '1234567890',
            'role': 'P'
        }

        url = reverse('register')
        response = self.client.post(url, valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], valid_data['email'])
        self.assertEqual(response.data['firstname'], valid_data['firstname'])
        self.assertEqual(response.data['lastname'], valid_data['lastname'])
        self.assertEqual(response.data['contact'], valid_data['contact'])
        self.assertEqual(response.data['role'], valid_data['role'])


    def test_password_too_short(self):
        # Password length less than 5 characters
        data = {'email': 'john@example.com', 'password': 'pass', 'firstname': 'John', 'lastname': 'Doe', 'contact': '1234567890', 'role': 'P'}
        response = register_user(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if the error message is within the list of errors
        self.assertIn({'error': 'Password must be at least 5 characters long'}, response.data)

    def test_firstname_too_short(self):
        # Password length less than 5 characters
        data = {'email': 'john@example.com', 'password': 'pass12345', 'firstname': 'J', 'lastname': 'Doe', 'contact': '1234567890', 'role': 'P'}
        response = register_user(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if the error message is within the list of errors
        self.assertIn({'error': 'Firstname must be at least 2 characters long'}, response.data)

    def test_password_too_short(self):
        # Password length less than 5 characters
        data = {'email': 'john@example.com', 'password': 'pass', 'firstname': 'John', 'lastname': 'D', 'contact': '1234567890', 'role': 'P'}
        response = register_user(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if the error message is within the list of errors
        self.assertIn({'error': 'Password must be at least 5 characters long'}, response.data)
