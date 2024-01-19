from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import User

from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.translation import gettext_lazy as _

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
    password = serializers.CharField(max_length=30, write_only=True)
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


class ResetPasswordRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email']

class SetNewPasswordserializer(serializers.Serializer):
    password = serializers.CharField(max_length=30, min_length=8, write_only=True)
    confirm_password = serializers.CharField(max_length=30, min_length=8, write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    
    class Meta:
        fields = [
            'password',
            'confirm_password',
            'token',
            'uidb64'
        ]

        def validate(self, attrs):
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            uidb64 = attrs.get('uidb64')
            token = attrs.get("token")
            
            try:
                user_id = smart_str(urlsafe_base64_decode(uidb64))

                user = User.objects.get(id=user_id)
                if PasswordResetTokenGenerator().check_token(user, token):
                    if password == confirm_password:
                        user.set_password(password)
                        user.save()
                    raise AuthenticationFailed(_("Passwords do not match"))
                raise AuthenticationFailed(_("Link is invalid or expired"))
            except Exception as e:
                raise AuthenticationFailed('Link is expired or invalid')

