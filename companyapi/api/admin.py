from django.contrib import admin

# Register your models here.

from .models import UserData,Patient,Vitals

#register all the model

admin.site.register(UserData)
admin.site.register(Patient)
admin.site.register(Vitals)
