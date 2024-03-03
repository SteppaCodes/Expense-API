from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import AccessToken
from drf_spectacular.utils import extend_schema, OpenApiExample

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    ResetPasswordRequestSerializer,
    SetNewPasswordserializer,
)
from .models import User
from .senders import SendMail
from renderers import UserRenderer

tags = ["Auth"]


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    renderer_classes = [UserRenderer]

    @extend_schema(
        tags=tags,
        summary="Register user",
        description="Register user",
        request=RegisterSerializer,
        responses={
            201: RegisterSerializer,
            400: RegisterSerializer,
        },
        examples=[
            OpenApiExample(
                name="Register User example",
                value={
                    "email": "testuser@mail.com",
                    "password": "testuser",
                    "first_name": "test",
                    "last_nsme": "user",
                },
                description="Example request for registering a user",
            )
        ],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.validated_data["email"]

        SendMail.verification(request, email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):

    @extend_schema(
        tags=tags,
        summary="Verify User email",
        description="This endpoint verifies a user's email",
    )
    def get(self, request, token):

        try:
            decoded_token = AccessToken(token)
            user_id = decoded_token["user_id"]

            user = User.objects.get(id=user_id)

            if not user.is_email_verified:
                user.is_email_verified = True
                user.save()
                return Response({"email": "email verified"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    serializer_class = LoginSerializer

    @extend_schema(
        tags=tags,
        summary="Login User",
        description="This endpoint authenticates a user",
        request=LoginSerializer,
        responses={"200": LoginSerializer},
        examples=[
            OpenApiExample(
                name="Login User example",
                value={
                    "email": "steppaapitestuser@gmail.com",
                    "password": "testuser",
                },
                description="Example request for authenticating a user",
            )
        ],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class ResetPasswordRequest(APIView):
    serializer_class = ResetPasswordRequestSerializer

    @extend_schema(
        tags=tags,
        summary="Reset Password request",
        description="This endpoint sends an email containing password reset link",
        request=ResetPasswordRequestSerializer,
        responses={"200": ResetPasswordRequestSerializer},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]
            SendMail.resetpassword(request, email)
            return Response(
                {
                    "message": "An email containing the link to reset your password has been sent to you"
                }
            )


class PasswordResetConfirm(APIView):
    @extend_schema(
        tags=tags,
        summary="Confirm password reset for user",
        description="This endpoint confirms the token and encoded user id sent from the url"        
    )
    def get(self, request, uidb64, token):
        user_id = smart_str(urlsafe_base64_decode(uidb64))
        try:
            user = User.objects.get(id=user_id)
            if PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {
                        "success": True,
                        "message": "credentials are valid",
                        "token": token,
                        "uidb64": uidb64,
                    }
                )
            return Response({"message": "Token is invalid or expired"})
        except DjangoUnicodeDecodeError:
            return Response({"message": "User does not exist"})


class SetNewPassword(APIView):
    serializer_class = SetNewPasswordserializer

    @extend_schema(
        tags=tags,
        summary="Set new password",
        description="This endpoint sets the new password for a user account",
        request=SetNewPasswordserializer,
        responses={"200": SetNewPasswordserializer},
        
    )
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"success": True, "message": "Password update successful"})


class LogoutAPiView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=tags,
        summary="Logout User",
        description="This endpoint Logs out a user",
        request=LogoutSerializer,
        responses={"200": LogoutSerializer},
        
    )    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "message": "Successfully logged out"})
