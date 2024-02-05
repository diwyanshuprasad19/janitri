from rest_framework import serializers
from .models import UserData,Patient,Vitals	

#Serializer for User 

class UserDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserData
		fields ='__all__'



#Serializer for Patient	
class PatientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Patient
		fields ='__all__'

#Serializer for Heartrate
			
class VitalsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vitals
		fields ='__all__'