from rest_framework import serializers
from .models import Doctor,Patient,MedicalRecord

class DoctorSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'user_id', 'first_name', 'last_name', 'phone', 'birth_date']


    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name


class SimpleDoctorSerializer(serializers.ModelSerializer):
    # first_name = serializers.CharField(source='user.first_name', read_only=True)
    # last_name = serializers.CharField(source='user.last_name', read_only=True)
    doctor_name = serializers.SerializerMethodField(method_name='get_doctor_name')
    
    class Meta:
        model = Doctor
        # fields = ['first_name', 'last_name','doctor_name']
        fields = ['doctor_name'] 

    # def get_first_name(self, obj):
    #     return obj.user.first_name

    # def get_last_name(self, obj):
    #     return obj.user.last_name
    
    def get_doctor_name(self,obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    



class PatientSerializer(serializers.ModelSerializer):
    doctor = SimpleDoctorSerializer(read_only=True,source='created_by')

    class Meta:
        model = Patient
        fields = ['id', 'name', 'age', 'gender', 'address', 'doctor']
        
 
        
        
class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['id', 'symptoms', 'treatment', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        user = self.context.get('user')
        patient_id = self.context.get('patient_id')

        try:
            doctor = Doctor.objects.get(user=user)
            patient = Patient.objects.get(id=patient_id, created_by=doctor)
        except (Doctor.DoesNotExist, Patient.DoesNotExist):
            raise serializers.ValidationError("Patient not found or not associated with the current doctor.")
        # Make sure patient is explicitly passed into the create method
        validated_data['patient_id'] = patient_id

        # return super().create(validated_data)
        return MedicalRecord.objects.create(patient=patient, **validated_data)



class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['id', 'symptoms', 'treatment', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        """
        Validates that the patient exists and belongs to the doctor.
        """
        user = self.context.get('user')
        patient_id = self.context.get('patient_id')

        if not user or not patient_id:
            raise serializers.ValidationError("Missing user or patient ID in context.")

        try:
            doctor = Doctor.objects.get(user=user)
        except Doctor.DoesNotExist:
            raise serializers.ValidationError("Doctor not found for the given user.")

        try:
            patient = Patient.objects.get(id=patient_id, created_by=doctor)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient not found or not associated with the current doctor.")

        # Save validated patient object to use later in create()
        self._validated_patient = patient
        return attrs

    def create(self, validated_data):
        # Use the validated patient from validate()
        return MedicalRecord.objects.create(
            patient=self._validated_patient,
            **validated_data
        )

    
        
class AddMedicalRecordSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MedicalRecord
        fields = ['patient_id', 'id', 'symptoms', 'treatment', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_patient_id(self, value):
        request = self.context['request']
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            raise serializers.ValidationError("Authenticated user is not associated with any doctor.")

        if not Patient.objects.filter(id=value, created_by=doctor).exists():
            raise serializers.ValidationError("Patient not found or not associated with the authenticated doctor.")
        return value