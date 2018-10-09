from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Wallet(models.Model):
    """ This model for wallets """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    balance = models.BigIntegerField()


class Group(models.Model):
    """ This model use for group of income and expense. """

    action_type_choices = (
        ('inc', 'Income'), ('exp', 'Expense'), ('und', 'undefined'),
    )
    action_type = models.CharField(
        max_length=3, choices=action_type_choices, default='und')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    default = models.BooleanField(default=False)
    name = models.CharField(max_length=255)


class Income(models.Model):
    """ This model for income transactions. """

    amount = models.BigIntegerField()
    time = models.DateTimeField()
    comment = models.CharField(max_length=255, blank=True, null=True)
    Wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL)


class Expense(models.Model):
    """ This model for expense transactions. """

    amount = models.BigIntegerField()
    time = models.DateTimeField()
    comment = models.CharField(max_length=255, blank=True, null=True)
    Wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL)
