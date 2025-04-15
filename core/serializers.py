from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
    write_only=True,
    style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        max_length=15,
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = User 
        fields = ['email', 'username', 'password', 'confirm_password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')  
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')  
        user = User(**validated_data)
        user.set_password(validated_data['password'])  
        user.save()
        return user



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
    write_only=True,
    style={'input_type': 'password'}
    )
    
    # class Meta:
    #     model = User 
    #     fields = ['username','password']
    
    def validate(self,attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if not username or not password:
            raise serializers.ValidationError('Both usename and password are requeired')
        
        user = authenticate(username=username,password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
    
        attrs['user'] = user
        
        return attrs 
    
        







class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']





class UserChangePasswordSerialzier(serializers.Serializer):
    password = serializers.CharField(max_length=15,style={'input_type':'password'},write_only=True)
    confirm_password = serializers.CharField(max_length=15,style={'input_type':'password'},write_only=True)
    # class Meta:
    #     model = User 
    #     fields = ['password','confirm_password']
        
    
    def validate(self,attrs):
        # user_id = self.context.get('user_id')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        
        if password != confirm_password:
            raise serializers.ValidationError('Password and confirm password do not march')
        
        
        # user = User.objects.get(id=user_id)
        # user.set_password(password)
        # user.save()
        
        return attrs 
    
    def update(self,instance,validated_data):
        password = validated_data.get('password')
        instance.set_password(password)
        instance.save()
        return instance 
    
    
    def create(self,validated_data):
        return validated_data 
    
    
    
    
        
        
    
    