from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin,UpdateModelMixin,RetrieveModelMixin,DestroyModelMixin
from .models import Doctor,Patient,MedicalRecord
from .serializers import DoctorSerializer,PatientSerializer,MedicalRecordSerializer,AddMedicalRecordSerializer

class DoctorViewSet(ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'delete']


    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Doctor.objects.none()

        if user.is_staff:
            return Doctor.objects.all()
        return Doctor.objects.filter(user=self.request.user)

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        doctor = Doctor.objects.filter(user=request.user).first()
        if not doctor:
            doctor = Doctor.objects.create(user=request.user)

        if request.method == 'GET':
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = DoctorSerializer(doctor, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # custom logic here
        return super().update(request, *args, **kwargs)
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class PatientViewSet(ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            user = self.request.user
            doctor = Doctor.objects.get(user=user)
            return Patient.objects.filter(created_by=doctor)
        except Doctor.DoesNotExist:
            # return Patient.objects.none()
            raise NotFound("Doctor profile not found for the current user.")

    

    def perform_create(self, serializer):
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            serializer.save(created_by=doctor)
        except Doctor.DoesNotExist:
            raise NotFound("Doctor profile not found for the current user.")

    
class MedicalRecordViewSet(ModelViewSet):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs.get('patient_pk')
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            patient = Patient.objects.get(id=patient_id, created_by=doctor)
            return MedicalRecord.objects.filter(patient=patient)
        except (Doctor.DoesNotExist, Patient.DoesNotExist):
            raise NotFound("Patient not found or not associated with the current doctor.")
    
    def get_serializer_context(self):
        return {
            'user': self.request.user,
            'patient_id': self.kwargs.get('patient_pk')
        }

    def get_serializer(self, *args, **kwargs):
        """
        Override to provide detailed error if context is invalid.
        """
        context = self.get_serializer_context()

        if not context.get('user') or not context.get('patient_id'):
            raise ValidationError("Missing 'user' or 'patient_id' in serializer context.")

        kwargs['context'] = context
        return self.serializer_class(*args, **kwargs)

    # def perform_create(self, serializer):
    #     patient_id = self.kwargs.get('patient_pk')
    #     try:
    #         doctor = Doctor.objects.get(user=self.request.user)
    #         patient = Patient.objects.get(id=patient_id, created_by=doctor)
    #         serializer.save(patient=patient)
    #     except (Doctor.DoesNotExist, Patient.DoesNotExist):
    #          raise NotFound("Patient not found or not associated with the current doctor.")
         


class AddMedicalRecordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = AddMedicalRecordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            patient_id = serializer.validated_data.get('patient_id')
            patient = Patient.objects.get(id=patient_id)
            serializer.save(patient=patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
