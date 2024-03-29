# Django-Assignemnt
Api assignemnt by Janitri

### Technologies Used: 
+ Python
+ Django
+ Django Rest Framework

### Additional Python Modules Required:: 
+ Django
+ Django Rest Framework

### Goal:Create Endpoint 
+  User Registration and Login : For registration and login you can consider
email and password validation, no need to use any authentication or
authorization protocols, just match the email and password.
+  Manage Patients : Endpoint to add a patient, and to retrieve patient details.
+  Heart rate details : Endpoint to record and retrieve heart rate data for
patients.

## Prerequisite
Python 

## Installing

Step by step commands on how to run this project on your computer

1)- Install Django

```
 pip install django
```

2)- Create django RestFramework

```
pip install djangorestframework
```

5)- Execute below commands

```
python manage.py makemigrations
python manage.py migrate
```
Note: Above commands should be executed if there is any db level changes

6)- Create superuser for admin access and follow instruction, if not created one

```
python manage.py createsuperuser
```

## Running the server

```
python manage.py runserver
```

<br>

## Assumptions 

+ One-to-One Relationship: Users to Patients : Each user can have only one patient profile, and each patient is linked to a single user account.
  
+ One-to-Many Relationship: Patients to Vitals Details : Each patient can have multiple Vitals records associated with them.
  
## Running the Test scripts

There are 4 files named login, registration, Patient and Vitals in the tests folder.In each file there will be classes.To executetest cases run the below commnad
```
python manage.py test api.tests.[classname]
```

