from django.urls import path 

from .views import ExpenseSummary

urlpatterns = [
    path('expense-summary/', ExpenseSummary.as_view()),
]