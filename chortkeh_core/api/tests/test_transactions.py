import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from chortkeh_core.models import Income, Wallet, Group

User = get_user_model()


class IncomeTransactionsTestCase(TestCase):
    """ Test case for income transactions api view. """

    @staticmethod
    def UserCreate(username, password):
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user

    def setUp(self):
        usr = 'test1'
        pwd = 'sahiusafh8f7sa98fy'
        user = self.UserCreate(username=usr, password=pwd)
        self.UserCreate(username='test2', password='test123456')
        w = Wallet.objects.create(
            name='WalletOne', owner=user)
        g = Group.objects.create(
            name='GroupOne', owner=user, action_type='inc')
        Income.objects.create(
            amount=10000, group=g, wallet=w, comment='TEST1')
        Income.objects.create(
            amount=15000, group=g, wallet=w, comment='TEST2')
        self.client.login(username=user, password=pwd)

    def test_get_transactions(self):
        response = self.client.get(reverse('income_api_view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_transactions_pk(self):
        response = self.client.get(
            reverse('income_api_view_pk', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_transactions_pk_not_found(self):
        response = self.client.get(
            reverse('income_api_view_pk', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_transactions_logout(self):
        self.client.logout()
        response = self.client.get(reverse('income_api_view'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
