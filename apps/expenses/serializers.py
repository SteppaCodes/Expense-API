from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["category", "amount", "description", "owner", "date"]

        read_only_fields = ["owner"]
