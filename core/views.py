from rest_framework.viewsets import ModelViewSet
from .models import User
from django.shortcuts import render 
from rest_framework.mixins import CreateModelMixin,UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny,IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action 
from .models import User
from .serializers import CurrentUserSerializer,UserRegistrationSerializer ,UserLoginSerializer \
    , UserChangePasswordSerialzier
from  rest_framework.views import APIView
import logging
import requests 

logger = logging.getLogger(__name__)

from rest_framework.views import APIView
from django.shortcuts import render
import requests
import logging

logger = logging.getLogger(__name__)

class HelloView(APIView):
    def get(self, request):
        data = {}  # Default empty data

        try:
            logger.info('Calling the external URL...')
            # response = requests.get('https://httpbin.org/delay/2')
            response = requests.get('https://google.com')
            logger.info('Received the response successfully.')

            if 'application/json' in response.headers.get('Content-Type', ''):
                data = response.json()
            else:
                data = {'message': 'Received non-JSON response'}

        except requests.ConnectionError:
            logger.critical('httpbin is offline.')
            data = {'error': 'Failed to connect'}

        return render(request, 'core/hello.html', {'data': data})



# class HelloView(APIView):
#     def get(self, request):
#         data = {}  # Default empty data

#         try:
#             logger.info('Calling the external URL...')
#             response = requests.get('https://httpbin.org/delay/2')
#             response = requests.get('https://google.com')
#             logger.info('Received the response successfully.')
#             data = response.json()
#         except requests.ConnectionError:
#             logger.critical('httpbin is offline.')

#         return render(request, 'core/hello.html', {'data': data})




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }



class UserRegstrationViewSet(CreateModelMixin,GenericViewSet):
    queryset = User.objects.none()
    serializer_class = UserRegistrationSerializer
    
    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            'detail':'Registration successful !',
            'token':tokens,
            'user':serializer.data
        },status=status.HTTP_201_CREATED)
        
        
    

class UserLoginViewSet(CreateModelMixin,GenericViewSet):
    serializer_class = UserLoginSerializer
    
    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        tokens = get_tokens_for_user(user)
        
        return Response({
            'msg':'Login successful',
            'tokens':tokens,
            'user':{
                'id':user.id,
                'username':user.username,
                'email':user.email,
                'role':user.role
            }
        },status=status.HTTP_200_OK)
     



class CurrentUserViewSet(ModelViewSet):
    http_method_names = ['get','put','patch','delete']
    serializer_class = CurrentUserSerializer 
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
        
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.action == 'changepassword':
            return UserChangePasswordSerialzier
        return CurrentUserSerializer


    @action(detail=False, methods=['put'], url_path='changepassword', permission_classes=[IsAuthenticated])
    def changepassword(self, request, *args, **kwargs):  
        serializer = UserChangePasswordSerialzier(instance=self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password updated successfully'}, status=status.HTTP_200_OK)
        # Set the new password and save the user
        # self.get_object().set_password(serializer.validated_data['password'])
        # self.get_object().save()
        # return Response({'detail': 'Password updated successfully'}, status=status.HTTP_200_OK)
    
    
class UserChangePasswordViewSet(UpdateModelMixin,GenericViewSet):
    serializer_class =  UserChangePasswordSerialzier
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

  
    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    

    def create(self,request,*args,**kwargs):
        serialzier = self.get_serializer(data=request.data)
        serialzier.is_valid(raise_exception=True)
        serialzier.save()
        return Response({
            'detail':'Password change succefuly'
        },status=status.HTTP_200_OK)
        
    
    
    
    