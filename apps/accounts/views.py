
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (RegisterSerializer, LoginSerializer, 
                          ResetPasswordRequestSerializer, SetNewPasswordserializer)
from .models import User
from .senders import SendMail
from renderers import UserRenderer


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.validated_data['email']

        SendMail.verification(request, email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    def get(self, request, token):
        
        try:
            decoded_token = AccessToken(token)
            user_id = decoded_token['user_id']

            user = User.objects.get(id=user_id)

            if not user.is_email_verified:
                user.is_email_verified = True
                user.save()
                return Response({
                    'email': 'email verified'
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
            

class ResetPasswordRequest(APIView):
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer=  self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            SendMail.resetpassword(request, email)
            return Response({
                'message':"An email containing the link to reset your password has been sent to you"
            })
        
class PasswordResetConfirm(APIView):
    def get(self, request, uidb64, token):
        user_id = smart_str(urlsafe_base64_decode(uidb64))
        try:
            user = User.objects.get(id=user_id)
            if PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    'success':True, 'message':'credentials are valid',
                    'token':token, 'uidb64':uidb64
                })
            return Response({'message':'Token is invalid or expired'})
        except DjangoUnicodeDecodeError:
            return Response({'message':'User does not exist'})

class SetNewPassword(APIView):
    serializer_class = SetNewPasswordserializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response({'success':True, 'message':"Password update successful"})