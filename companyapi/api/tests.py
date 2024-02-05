from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Patient,UserData,Vitals
from datetime import datetime
from .serializers import UserDataSerializer,PatientSerializer,VitalsSerializer
from .utils import register_user,login_user,get_all_patients
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


#login

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

#getspecific patient
class GetPatientTestCase(TestCase):
    def setUp(self):
        self.user = UserData.objects.create(
            email='john@example.com',
            password='password123',
            firstname='John',
            lastname='Doe',
            contact='1234567890',
            role='P'
            )
        # Create a patient for testing
        self.patient = Patient.objects.create(
            user=self.user,
            firstname='John',
            lastname='Doe',
            email='john.doe@example.com',
            contact='1234567890',
            date_of_birth='1990-01-01',
            gender='M',
            address='123 Street, City, Country',
        )

    def test_get_existing_patient(self):
        # Test retrieving an existing patient
        url = reverse('patientone', args=[self.patient.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['firstname'], self.patient.firstname)
        self.assertEqual(response.data['lastname'], self.patient.lastname)
        self.assertEqual(response.data['email'], self.patient.email)
        # Add more assertions for other fields as needed

    def test_get_non_existing_patient(self):
        # Test retrieving a non-existing patient
        url = reverse('patientone', args=[9999])  # Non-existing ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Patient not found'})        


#create patient on condition(user exist or not)
class AddPatientTestCase(TestCase):
    def setUp(self):
        self.valid_payload = {
            'email': 'test@example.com',
            'firstname': 'John',
            'lastname': 'Doe',
            'contact': '1234567890',
            'date_of_birth': '1990-01-01',
            'gender': 'M',
            'address': '123 Test Street',
            'medical_history': 'None'
        }

    def test_create_patient(self):
        url = reverse('patientadd')
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)

    def test_update_patient(self):
        # Create a patient first
        patient = Patient.objects.create(
            user=UserData.objects.create(email='test@example.com', password='password', firstname='John', lastname='Doe', contact='1234567890', role='P'),
            **self.valid_payload
        )
        
        # Update payload
        updated_payload = self.valid_payload.copy()
        updated_payload['contact'] = '9876543210'

        # Make PUT request
        url = reverse('patientadd')
        response = self.client.post(url, updated_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_missing_fields(self):
        url = reverse('patientadd')
        invalid_payload = {}
        response = self.client.post(url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)








#create vitals for specific patient
class AddVitalsTestCase(TestCase):
    def setUp(self):
        self.user = UserData.objects.create(
            email='john@example.com',
            password='password123',
            firstname='John',
            lastname='Doe',
            contact='1234567890',
            role='P'
                 )
        self.client = APIClient()
        # Create a patient
        self.patient = Patient.objects.create(
            user=self.user,
            firstname='John',
            lastname='Doe',
            email='john@example.com',
            contact='1234567890',
            date_of_birth='2000-01-01',
            gender='M',
            address='123 Main St',
        )

    def test_add_vitals_to_existing_patient(self):
        url = reverse('add_vitals', kwargs={'pk': self.patient.pk})
        data = {'paramtype': 'Heart rate', 'paramvalue': '70 bpm'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_missing_parameters(self):
        url = reverse('add_vitals', kwargs={'pk': self.patient.pk})
        data = {'paramtype': 'Heart rate'}  # Missing paramvalue
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'paramtype and paramvalue are required')

    def test_add_vitals_to_nonexistent_patient(self):
        url = reverse('add_vitals', kwargs={'pk': 9999})  # Non-existent patient
        data = {'paramtype': 'Heart rate', 'paramvalue': '70 bpm'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Patient does not exist')        







#retrieve hearbeat for specific user
class GetVitalsForPatientTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a patient with heart rate entries
        self.user = UserData.objects.create(
            email='john@example.com',
            password='password123',
            firstname='John',
            lastname='Doe',
            contact='1234567890',
            role='P'
                 )
        
        self.patient = Patient.objects.create(
            user=self.user,
            firstname='John',
            lastname='Doe',
            email='john@example.com',
            contact='1234567890',
            date_of_birth='1990-01-01',
            gender='M',
            address='123 Street, City',
        )
        Vitals.objects.create(
            patient=self.patient,
            paramtype='heartbeat',
            paramvalue='80 82 85',
        )
    
    def test_get_vitals_for_existing_patient(self):
        url = reverse('show_heart_rate', kwargs={'pk': self.patient.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vitals_for_nonexistent_patient(self):
        url = reverse('show_heart_rate', kwargs={'pk': 999})  # Assuming 999 is a non-existent patient pk
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Patient does not exist'})