from django.shortcuts import render
from .models import Expense
from .permissions import IsOwner

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination  

from .serializers import ExpenseSerializer
from renderers import UserRenderer


class ExpenseListCreateAPIView(APIView, PageNumberPagination):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = self.request.user
        expenses = Expense.objects.all().filter(owner=user)
        #set the number if objects to be returned per page
        self.page_size = 10
        #from the PageNumberPagination class, paginate the queyset
        result = self.paginate_queryset(expenses, request, view=self)
        #Serialize the paginated resukts
        serializer = self.serializer_class(result, many=True)
        return self.get_paginated_response(serializer.data)
    
    def post(self, request):
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetailAPIView(APIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = 'id'

    def get(self, request, id):
        expense = Expense.objects.get(id=id)
        serializer = self.serializer_class(expense)
        return Response(serializer.data)

    def put(self, request, id):
        expense = Expense.objects.get(id=id)
        serializer = self.serializer_class(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        expense = Expense.objects.get(id=id)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
