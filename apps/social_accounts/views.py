from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response 
from drf_spectacular.utils import extend_schema

from .serializers import GoogleSignInSerializer

tags = ["Social Auth"]

class GoogleSignInView(APIView):
    serialiser_class = GoogleSignInSerializer

    @extend_schema(
        tags=tags,
        summary="Sign in with google",
        description="This endpoint allows users to sign in or sign up with Google",
        request=GoogleSignInSerializer,
        responses={
            201: GoogleSignInSerializer,
            400: GoogleSignInSerializer,
        }
    )
    def post(self, request):
        serializer = self.serialiser_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['access_token'])
        return Response(data, status=status.HTTP_200_OK)