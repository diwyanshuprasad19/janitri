from django.db import models

# Create your models here.



#Creating User Model

class UserData(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    contact = models.CharField(max_length=20)
    role = models.CharField(max_length=1, choices=[('D', 'Doctor'), ('N', 'Nurse'), ('P', 'Patient')])


    
#Patient Model
class Patient(models.Model):
    user = models.OneToOneField(UserData, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    address = models.TextField()
    medical_history = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


#Vitals
class Vitals(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE) 
    paramtype = models.CharField(max_length=128,default='')
    paramvalue = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)
