from django.shortcuts import render
import datetime

from rest_framework.views import APIView
from rest_framework import response, status

from apps.expenses.models import Expense

class ExpenseSummary(APIView):
    def get_amount_for_category(self, expense_list, category):
        expenses = expense_list.filter(category=category)
        amount = 0

        for expense in expenses:
            amount += expense.amount
        return {
            'amount':amount
        }

    def get_category(self, expense):
        return expense.category

    def get(self, request):
        today_date = datetime.date.today()
        ayear_ago = today_date - datetime.timedelta(days=(30*12))
        expenses = Expense.objects.filter(owner=request.user,date__gte=ayear_ago, date__lte=today_date)
        final = {}

        #for each expense, return a list of category. set makes sure theres no duplicate
        categories = list(set(map(self.get_category, expenses)))
        
        for expense in expenses:
            for category in categories:
                final[category] = self.get_amount_for_category(expenses, category)

        return response.Response({"CATEGORY_DATA":final}, status=status.HTTP_200_OK)