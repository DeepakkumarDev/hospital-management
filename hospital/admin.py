from django.contrib import admin
from django.contrib import messages 
from django.db.models import Count 
from django.utils.html import format_html,urlencode
from django.urls import reverse 
from . import models
# Register your models here.

class PatientInline(admin.TabularInline):
    model = models.Patient
    min_num = 1
    max_num = 5
    extra = 0

class MedicalReportInline(admin.TabularInline):
    model = models.MedicalRecord
    min_num = 1
    max_num =10
    extra = 0
    show_change_link = False 
    
    fields = ['symptoms', 'treatment', 'created_at']
    readonly_fields = ['created_at']  
    



@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','patients_count']
    list_select_related = ['user']
    list_per_page = 10
    inlines = [PatientInline]
    # search_fields =['first_name__istartswith','last_name__istartswith']
    search_fields = ['user__first_name__icontains', 'user__last_name__icontains']

    list_per_page = 10 
    
    
    @admin.display(ordering='patients_count', description='Patients')
    def patients_count(self, doctor):
        url = (
            reverse('admin:hospital_patient_changelist')
            + "?"
            + urlencode({'created_by__id': str(doctor.id)})
        )
        return format_html('<a href="{}">{}</a>', url, doctor.patients_count)
        
    def get_queryset(self,request):
        return super().get_queryset(request).annotate(patients_count=Count('patients'))
        

# class MedicalReportInline(admin.StackedInline):
class MedicalReportInline(admin.TabularInline):
    model = models.MedicalRecord
    min_num = 1
    max_num =10
    extra = 0
    show_change_link = False 
    
    fields = ['symptoms', 'treatment', 'created_at']
    readonly_fields = ['created_at']  
    




@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender', 'address', 'doctor_name']
    list_select_related = ['created_by'] 
    inlines = [MedicalReportInline]
    readonly_fields = ['created_by']
    
    @admin.display(description='Doctor')
    def doctor_name(self, patient):
        if patient.created_by and patient.created_by.user:
            return f"{patient.created_by.user.first_name} {patient.created_by.user.last_name}"
        return "-"
    
    