import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class AccountTestCase(TestCase):
    """ Test case for account api view. """

    @staticmethod
    def create(email, username, password):
        """ Create new user."""
        user = User(email=email, username=username)
        user.set_password(password)
        user.save()
        return user

    def setUp(self):
        self.password = 'gb452giu523ggu'
        self.create('1@test.com', 'test1', self.password)
        self.create('2@test.com', 'test2', self.password)
        self.client.login(username='test1', password=self.password)

    def test_get_token_get_method(self):
        self.client.logout()
        response = self.client.get(reverse('get_token'))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_token_post_method(self):
        self.client.logout()
        response = self.client.post(reverse('get_token'), data=json.dumps({
            "username": "test1",
            "password": self.password
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_token_post_method_bad_user(self):
        self.client.logout()
        response = self.client.post(reverse('get_token'), data=json.dumps({
            "username": "test1",
            "password": "kdfgiuk"
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_account_details(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_account(self):
        self.client.logout()
        response = self.client.post(reverse('account'), data=json.dumps({
            'email': '3@test.com',
            'username': 'test3',
            'password': 'sadjhiusdh',
            'first_name': 'John',
            'last_name': 'Smith'
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_account_bad(self):
        response = self.client.put(reverse('account'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_account(self):
        response = self.client.put(reverse('account'), data=json.dumps({
            'email': 'new@test.com',
            'first_name': 'Arnold',
            'last_name': 'Whick'
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_account_bad(self):
        response = self.client.put(reverse('account'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_account(self):
        response = self.client.delete(reverse('account'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_account_bad(self):
        self.client.logout()
        response = self.client.delete(reverse('account'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
