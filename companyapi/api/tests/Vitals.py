from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from api.models import Patient,UserData,Vitals
from datetime import datetime
from api.serializers import UserDataSerializer,PatientSerializer,VitalsSerializer
from api.utils import register_user,login_user,get_all_patients
from rest_framework.response import Response




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