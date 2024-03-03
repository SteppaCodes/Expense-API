from django.shortcuts import render
from .models import Expense
from .permissions import IsOwner

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiExample
from datetime import date

from .serializers import ExpenseSerializer
from renderers import UserRenderer

tags = ["Expenses"]


class ExpenseListCreateAPIView(APIView, PageNumberPagination):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=tags,
        summary="Expenses list",
        description="This endpoint returns all user's expenses",
        request=ExpenseSerializer,
        responses={"200": ExpenseSerializer},
    )
    def get(self, request):
        user = self.request.user
        expenses = Expense.objects.all().filter(owner=user)
        # set the number if objects to be returned per page
        self.page_size = 10
        # from the PageNumberPagination class, paginate the queyset
        result = self.paginate_queryset(expenses, request, view=self)
        # Serialize the paginated resukts
        serializer = self.serializer_class(result, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        tags=tags,
        summary="Create expense",
        description="tThis endpoint creates a new expense",
        request=ExpenseSerializer,
        responses={
            201: ExpenseSerializer,
            400: ExpenseSerializer,
        },
        examples=[
            OpenApiExample(
                name="Create expense request example",
                value={
                    "category": "food",
                    "amount": "10000",
                    "description":"Just got some expensive food :)",
                    "date": str(date.today()),
                },
                description="Example request for creating an expense record",
            )
        ],
    )
    def post(self, request):
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetailAPIView(APIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "id"

    @extend_schema(
        tags=tags,
        summary="Expense detail",
        description="This endpoint retreives the expense details",
        request=ExpenseSerializer,
        responses={"200": ExpenseSerializer},
    )
    def get(self, request, id):
        expense = Expense.objects.get(id=id)
        serializer = self.serializer_class(expense)
        return Response(serializer.data)

    @extend_schema(
        tags=tags,
        summary="Update detail",
        description="This endpoint updates expense details",
        request=ExpenseSerializer,
        responses={"200": ExpenseSerializer},
    )
    def put(self, request, id):
        expense = Expense.objects.get(id=id)
        serializer = self.serializer_class(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=tags,
        summary="Delete Expense",
        description="This endpoint deletes an expense",
        request=ExpenseSerializer,
        responses={"200": ExpenseSerializer},
    )
    def delete(self, request, id):
        expense = Expense.objects.get(id=id)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
