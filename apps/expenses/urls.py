from django.urls import path
from .views import (ExpenseListCreateAPIView, ExpenseDetailAPIView)

urlpatterns = [
    path('expenses/', ExpenseListCreateAPIView.as_view()),
    path('expenses/<int:id>/', ExpenseDetailAPIView.as_view()),

]