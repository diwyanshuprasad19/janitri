from rest_framework.decorators import api_view
from .utils import register_user, login_user, get_user_data, add_patient, get_all_patients, get_patient, add_vitals, get_all_vitals, get_vitals_for_patient
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'UserData':'/userdata/',
        'Register':'/register/',
		'Login': '/login/', 
        'PatientAll': '/patient/',
        'AddPatient': '/patientadd/',
        'Patientone': '/patient/<str:pk>/',
        'vitalsall': '/vitals/',
        'vitalsadd': '/patient/<str:pk>/heartadd/',
        'heartbeatshow': '/patient/<str:pk>/heartshow/',
		}
		
    return Response(api_urls)

# User-related views
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        return register_user(request.data)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        response_data, status_code = login_user(email, password)
        return Response(response_data, status=status_code)


@api_view(['GET'])
def userdata(request):
    if request.method == 'GET':
        return get_user_data()


# Patient-related views
@api_view(['POST'])
def addpatient(request):
    if request.method == 'POST':
        response_data, status_code = add_patient(request.data)
        return Response(response_data, status=status_code)


@api_view(['GET'])
def patientall(request):
    if request.method == 'GET':
        return get_all_patients()


@api_view(['GET'])
def patientone(request, pk):
    if request.method == 'GET':
        return get_patient(pk)


# Vitals-related views
@api_view(['POST'])
def add_vitals_to_patient(request, pk):
    if request.method == 'POST':
        response = add_vitals(pk, request.data)
        return response



@api_view(['GET'])
def vitalsall(request):
    if request.method == 'GET':
        response_data, status_code = get_all_vitals()
        return Response(response_data, status=status_code)




@api_view(['GET'])
def patientvitals(request, pk):
    if request.method == 'GET':
        heart_rate_data, status_code = get_vitals_for_patient(pk)
        return Response(heart_rate_data, status=status_code)