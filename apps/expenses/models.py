from django.db import models
from apps.accounts.models import User

class Expense(models.Model):

    CATEGORY_OPTIONS = [
        ('food', 'Food'),
        ('transportation', 'Transportation'),
        ('entertainment', 'Entertainment'),
        ('rent', 'rent'),
        ('others', 'Others'),
    ]

    category = models.CharField(max_length=30, choices=CATEGORY_OPTIONS)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)