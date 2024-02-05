from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from api.models import Patient,UserData,Vitals
from datetime import datetime
from api.serializers import UserDataSerializer,PatientSerializer,VitalsSerializer
from api.utils import register_user,login_user,get_all_patients
from rest_framework.response import Response






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




