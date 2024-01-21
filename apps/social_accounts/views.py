from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response 

from .serializers import GoogleSignInSerializer

class GoogleSignInView(APIView):
    serialiser_class = GoogleSignInSerializer

    def post(self, request):
        serializer = self.serialiser_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['access_token'])
        return Response(data, status=status.HTTP_200_OK)