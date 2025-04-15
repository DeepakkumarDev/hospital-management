from django.db import models
from django.conf import settings
from django.contrib import admin
from django.core.validators import MinValueValidator
from . validators import validate_age 


class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    birth_date = models.DateField(blank=True,null=True)
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name 
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    
    class Meta:
        ordering = ['user__first_name','user__last_name']
    




class Patient(models.Model):
    GENDER_CHOICES_MALE = 'M'
    GENDER_CHOICES_FEMALE = 'F'
    GENDER_CHOICES_OTHER = 'O'
    GENDER_CHOICES =[
        (GENDER_CHOICES_MALE,'Male'),
        (GENDER_CHOICES_FEMALE,'Female'),
        (GENDER_CHOICES_OTHER,'Other')
        
    ]
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField(validators=[validate_age])
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default=GENDER_CHOICES_OTHER)
    address = models.TextField()
    created_by = models.ForeignKey(Doctor,on_delete=models.PROTECT,related_name='patients')
    
    def __str__(self):
        return self.name 
    
    


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='medical_record')
    symptoms = models.TextField()
    treatment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symptoms[:30]} - {self.treatment[:30]}"
    
    
    