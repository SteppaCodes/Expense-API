
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt

from .serializers import (RegisterSerializer, LoginSerializer)
from .models import User
from .senders import Sendmail


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.validated_data['email']

        Sendmail.verification(request, email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])

            if not user.is_email_verified:
                user.is_email_verified = True
                user.save()
                return Response({
                    'email': 'email verified'
                }, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({
                'error': 'token expired'
            }, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({
                'error':'token is invalid'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
            