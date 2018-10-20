import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from chortkeh_core.models import Group

User = get_user_model()


class GroupTestCase(TestCase):
    """ Test for group api view. """

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
        Group.objects.create(name='GroupOne', owner=user, action_type='inc')
        Group.objects.create(name='GroupTwo', owner=user, action_type='exp')
        self.client.login(username=user, password=pwd)

    def test_get_group_no_pk(self):
        response = self.client.get(reverse('group_api_view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_group_no_pk_no_user(self):
        self.client.logout()
        self.client.login(username='test', password='test123456')
        response = self.client.get(reverse('group_api_view'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_group_pk(self):
        response = self.client.get(
            reverse('group_api_view_pk', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_group_pk_not_found(self):
        response = self.client.get(
            reverse('group_api_view_pk', kwargs={'pk': 10})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_group(self):
        response = self.client.post(reverse('group_api_view'), data=json.dumps({
            'name': 'Group NEw',
            'action_type': 'exp'
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_group_bad_type(self):
        response = self.client.post(reverse('group_api_view'), data=json.dumps({
            'name': 'Group NEw',
            'action_type': 'aaa'
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_group_empty_type(self):
        response = self.client.post(reverse('group_api_view'), data=json.dumps({
            'name': 'Group NEw',
            'action_type': ''
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_group_no_pk(self):
        response = self.client.put(reverse('group_api_view'), data=json.dumps({
            'name': 'Group NEw',
            'action_type': 'inc'
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_group_pk(self):
        response = self.client.put(
            reverse('group_api_view_pk', kwargs={'pk': 1}), data=json.dumps({
                'name': 'Edited group',
                'action_type': 'exp'
            }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_group_pk_not_found(self):
        response = self.client.put(
            reverse('group_api_view_pk', kwargs={'pk': 10}), data=json.dumps({
                'name': 'Edited group',
                'action_type': 'exp'
            }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_group_no_pk(self):
        response = self.client.delete(reverse('group_api_view'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_group_pk(self):
        response = self.client.delete(
            reverse('group_api_view_pk', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_group_pk_not_found(self):
        response = self.client.delete(
            reverse('group_api_view_pk', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
