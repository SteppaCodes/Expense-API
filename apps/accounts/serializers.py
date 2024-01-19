from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=6)
    password = serializers.CharField(max_length=30)
    full_name = serializers.CharField(read_only=True)
    access_token= serializers.CharField(read_only=True)
    refresh_token= serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Email does not exist')
        if not user.is_active:
            raise AuthenticationFailed('Account is inactive, please contact admin')
        if not user.is_email_verified:
            raise AuthenticationFailed('Email not verified')
        tokens = user.tokens()
        return {
            'email': email,
            'access_token': str(tokens['access']),
            'refresh_token': str(tokens['refresh'])
        }
