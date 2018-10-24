import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from chortkeh_core.models import Wallet

User = get_user_model()


class WalletTestCase(TestCase):
    """ Test case for wallet api view. """

    @staticmethod
    def UserCreate(username, password):
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user

    def setUp(self):
        usr = 'grouptest'
        pwd = 'sahiusafh8f7sa98fy'
        user = self.UserCreate(username=usr, password=pwd)
        self.UserCreate(username='test', password='test123456')
        Wallet.objects.create(name='GroupOne', owner=user)
        Wallet.objects.create(name='GroupTwo', owner=user)
        self.client.login(username=user, password=pwd)

    def test_wallet_no_pk(self):
        response = self.client.get(reverse('wallet_api_view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wallet_no_pk_no_wallet(self):
        self.client.logout()
        self.client.login(username='test', password='test123456')
        response = self.client.get(reverse('wallet_api_view'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wallet_pk(self):
        response = self.client.get(
            reverse('wallet_api_view_pk', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wallet_pk_not_found(self):
        response = self.client.get(
            reverse('wallet_api_view_pk', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wallet_post_object(self):
        response = self.client.post(
            reverse('wallet_api_view'), data=json.dumps({
                'name': 'Wallet Two'
            }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_wallet_post_bad_object(self):
        response = self.client.post(
            reverse('wallet_api_view'), data=json.dumps({
                'name': ''
            }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_wallet_no_pk(self):
        response = self.client.put(reverse('wallet_api_view'), data=json.dumps({
            'name': 'Update'
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_wallet_pk(self):
        response = self.client.put(
            reverse('wallet_api_view_pk', kwargs={'pk': 1}), data=json.dumps({
                'name': 'updated'
            }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_wallet_pk_not_found(self):
        response = self.client.put(
            reverse('wallet_api_view_pk', kwargs={'pk': 10}), data=json.dumps({
                'name': 'Edited'
            }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_wallet_no_pk(self):
        response = self.client.delete(reverse('wallet_api_view'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_wallet_pk(self):
        response = self.client.delete(
            reverse('wallet_api_view_pk', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_wallet_pk_not_found(self):
        response = self.client.delete(
            reverse('wallet_api_view_pk', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
