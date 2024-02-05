from django.urls import path
from . import views

#contain all the url for api

urlpatterns = [
     path('',views.apiOverview,name='api-overview'),
     path('userdata/', views.userdata, name="userdata"),
     path('register/', views.register, name="register"),
     path('login/', views.login, name="login"),
     path('patient/', views.patientall, name="patientall"),
     path('patientadd/', views.addpatient, name="patientadd"),
     path('patient/<str:pk>/', views.patientone, name="patientone"),
     path('vitals/', views.vitalsall, name="vitalsall"),
     path('patient/<str:pk>/heartadd/', views.add_vitals_to_patient, name="add_vitals"),
     path('patient/<str:pk>/heartshow/', views.patientvitals, name="show_heart_rate"),
]
