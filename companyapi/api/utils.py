from rest_framework import status
from rest_framework.response import Response
from .models import UserData, Patient, Vitals
from .serializers import UserDataSerializer, PatientSerializer, VitalsSerializer
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import random
import string
from datetime import datetime


# User-related utility functions
def validate_password_length(password):
    if password is None:
        return {'error': 'Password missing'}  # Error message when password is None
    elif len(password) < 5:
        return {'error': 'Password must be at least 5 characters long'}


def validate_email_format(email):
    if not email:  # Check if email is empty or None
        return {'error': 'Email is required'}
    try:
        validate_email(email)
    except ValidationError:
        return {'error': 'Invalid email format'}


def validate_field_length(value, field_name, min_length):
    if value is None:
        return {'error': f"{field_name.capitalize()} is missing"}  # Error message when value is None
    elif len(value) < min_length:
        return {'error': f"{field_name.capitalize()} must be at least {min_length} characters long"}


def validate_role(role):
    if not role:
        return {'error': 'Role is missing'}
    valid_roles = ['D', 'N', 'P']
    if role not in valid_roles:
        return {'error': 'Invalid role. Must be one of Doctor (D), Nurse (N), or Patient (P)'}


def validate_user_data(data):
    validation_errors = []
    validation_errors.extend([validate_password_length(data.get('password'))])
    validation_errors.extend([validate_field_length(data.get(field), field, 2) for field in ['firstname', 'lastname']])
    validation_errors.extend([validate_field_length(data.get('contact'), 'contact', 10)])
    validation_errors.extend([validate_role(data.get('role'))])
    validation_errors = [error for error in validation_errors if error is not None]
    return validation_errors


#register
def register_user(data):
    validation_errors = validate_user_data(data)

    if validation_errors:
        return Response(validation_errors, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserDataSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#login


def login_user(email, password):
    # Check if email and password are provided
    if not email or not password:
        return {'error': 'Both email and password are required'}, status.HTTP_400_BAD_REQUEST

    # Validate email format
    try:
        validate_email(email)
    except ValidationError:
        return {'error': 'Invalid email format'}, status.HTTP_400_BAD_REQUEST

    # Check password length
    if len(password) < 5:
        return {'error': 'Password must be at least 5 characters long'}, status.HTTP_400_BAD_REQUEST

    try:
        user = UserData.objects.get(email=email, password=password)
    except UserData.DoesNotExist:
        return {'error': 'Invalid email or password'}, status.HTTP_400_BAD_REQUEST

    return {'message': 'Login successful'}, status.HTTP_200_OK




#get all user

def get_user_data():
    users = UserData.objects.all()
    if not users:
        return Response({'error': 'Table is Empty'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserDataSerializer(users, many=True)
    return Response(serializer.data)





#add [patient


# Patient-related utility functions

def add_patient(data):
    email = data.get('email')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    contact = data.get('contact')
    date_of_birth = data.get('date_of_birth')
    gender = data.get('gender')
    address = data.get('address')
    medical_history = data.get('medical_history')

    # Check for missing fields
    missing_fields = []
    if not email:
        missing_fields.append('email')
    if not firstname:
        missing_fields.append('firstname')
    if not lastname:
        missing_fields.append('lastname')
    if not contact:
        missing_fields.append('contact')
    if not date_of_birth:
        missing_fields.append('date_of_birth')
    if not gender:
        missing_fields.append('gender')
    if not address:
        missing_fields.append('address')
    if missing_fields:
        return {'error': f'Missing required fields: {", ".join(missing_fields)}'}, status.HTTP_400_BAD_REQUEST

    # Validate email format
    try:
        validate_email(email)
    except ValidationError:
        return {'error': 'Invalid email format'}, status.HTTP_400_BAD_REQUEST

    # Validate first name and last name length
    if len(firstname) < 2:
        return {'error': 'First name must be at least 2 characters long'}, status.HTTP_400_BAD_REQUEST
    if len(lastname) < 2:
        return {'error': 'Last name must be at least 2 characters long'}, status.HTTP_400_BAD_REQUEST

    # Validate contact length
    if len(contact) < 10:
        return {'error': 'Contact must be at least 10 characters long'}, status.HTTP_400_BAD_REQUEST

    # Validate date_of_birth format
    try:
        datetime.strptime(date_of_birth, '%Y-%m-%d')
    except ValueError:
        return {'error': 'Invalid date format. Date of birth should be in YYYY-MM-DD format'}, status.HTTP_400_BAD_REQUEST

    # Validate gender
    valid_genders = ['M', 'F', 'O']
    if gender not in valid_genders:
        return {'error': 'Invalid gender. Must be one of Male (M), Female (F), or Other (O)'}, status.HTTP_400_BAD_REQUEST

    # Check if a UserData instance with the provided email exists
    try:
        user_data = UserData.objects.get(email=email)
        if user_data.role != 'P':
            return {'error': 'Email already exists with a different role'}, status.HTTP_400_BAD_REQUEST
        user_id = user_data.id
    except UserData.DoesNotExist:
        # If no UserData instance exists, create a new one with a random password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        user_data = UserData.objects.create(
            email=email,
            password=password,
            firstname=firstname,
            lastname=lastname,
            contact=contact,
            role='P'  # Assuming 'P' denotes Patient role
        )
        user_id = user_data.id

    # Create or update the Patient instance with the retrieved or newly created UserData
    patient_data = {
        'user_id': user_id,
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'contact': contact,
        'date_of_birth': date_of_birth,
        'gender': gender,
        'address': address,
        'medical_history': medical_history
    }

    # If the patient already exists, update it; otherwise, create a new one
    patient, created = Patient.objects.update_or_create(email=email, defaults=patient_data)

    if created:
        return {'message': 'Patient created successfully'}, status.HTTP_201_CREATED
    else:
        return {'message': 'Patient updated successfully'}, status.HTTP_200_OK
    



#get all patient

def get_all_patients():
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#get patient by id
def get_patient(pk):
    try:
        # Check if pk is provided and is a valid integer
        if not pk:
            return Response({'error': 'Patient ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            pk = int(pk)
        except ValueError:
            return Response({'error': 'Invalid patient ID format'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve patient by pk
        patient = Patient.objects.get(pk=pk)
        
        # Serialize patient data if found
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
    
    except ValidationError as e:
        return Response({'error': 'Invalid patient ID format'}, status=status.HTTP_400_BAD_REQUEST)





# Vitals-related utility functions
def add_vitals(patient_pk, data):

    if not patient_pk:
        return Response({'error': 'Patient ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        patient_pk = int(patient_pk)
    except ValueError:
        return Response({'error': 'Invalid patient ID format'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        patient = Patient.objects.get(pk=patient_pk)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # Extract paramtype and paramvalue from request data
    paramtype = data.get('paramtype')
    paramvalue = data.get('paramvalue')

    # Check if paramtype and paramvalue are provided
    if not paramtype or not paramvalue:
        return Response({'error': 'paramtype and paramvalue are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Create Vitals instance for the patient
    Vitals.objects.create(patient=patient, paramtype=paramtype, paramvalue=paramvalue)

    return Response({'message': 'Heart rate added successfully'}, status=status.HTTP_201_CREATED)


def get_all_vitals():
    heart = Vitals.objects.all()
    if not heart:
        return {'error': 'Table is Empty'}, status.HTTP_404_NOT_FOUND

    serializer = VitalsSerializer(heart, many=True)
    return serializer.data, status.HTTP_200_OK




def get_vitals_for_patient(pk):
    # Check if pk is provided and is a valid integer
    if not pk:
        return {'error': 'Patient ID is required'}, status.HTTP_400_BAD_REQUEST

    try:
        pk = int(pk)
    except ValueError:
        return {'error': 'Invalid patient ID format'}, status.HTTP_400_BAD_REQUEST

    try:
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return {'error': 'Patient does not exist'}, status.HTTP_404_NOT_FOUND

    # Retrieve heart rate entries for the patient
    heart_rate_entries = Vitals.objects.filter(patient=patient, paramtype='heartbeat')

    # Serialize heart rate data
    heart_rate_data = []
    for entry in heart_rate_entries:
        heart_rate_data.append({
            'timestamp': entry.timestamp,
            'heart_rate_values': entry.paramvalue.split()  # Splitting paramvalues into a list
        })

    return heart_rate_data, status.HTTP_200_OK