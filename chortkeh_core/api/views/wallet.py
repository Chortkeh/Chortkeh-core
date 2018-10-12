from rest_framework import views, status, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from chortkeh_core.models import Wallet
from chortkeh_core.api.serializers import WalletSerializer

User = get_user_model()


class WalletApiView(views.APIView):
    """ This API view use for wallet managment. """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """ GET method use for get wallets list and details. """

        if kwargs.get('pk'):
            try:
                wallet_query = Wallet.objects.get(
                    id=kwargs.get('pk'), owner=request.user)
            except ObjectDoesNotExist:
                response_data = {'errors': 'Wallet not found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            else:
                response_data = {
                    'id': wallet_query.id,
                    'name': wallet_query.name
                }
                response_status_code = status.HTTP_200_OK
        else:
            wallet_query_set = Wallet.objects.filter(owner=request.user)
            if wallet_query_set.count() > 0:
                wallet_list = [
                    {'id': q.id, 'name': q.name} for q in wallet_query_set]
                response_data = {
                    'count': wallet_query_set.count(), 'items': wallet_list}
                response_status_code = status.HTTP_200_OK
            else:
                response_data = {'errors': 'You don\'t have a wallet.'}
                response_status_code = status.HTTP_404_NOT_FOUND

        return Response(data=response_data, status=response_status_code)

    def post(self, request, *args, **kwargs):
        """ POST method use for create new wallet. """

        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            wallet_object = Wallet.objects.create(
                owner=request.user,
                name=serializer.validated_data.get('name'),
            )
            response_data = {'id': wallet_object.id}
            response_status_code = status.HTTP_201_CREATED
        else:
            response_data = {'errors': serializer.errors}
            response_status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=response_data, status=response_status_code)

    def put(self, request, *args, **kwargs):
        """ PUT method use for update a wallet. """

        if kwargs.get('pk'):
            try:
                wallet_object = Wallet.objects.get(
                    id=kwargs.get('pk'), owner=request.user)
            except ObjectDoesNotExist:
                response_data = {'errors': 'Wallet not found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            else:
                serializer = WalletSerializer(data=request.data)
                if serializer.is_valid():
                    wallet_object.name = serializer.validated_data.get('name')
                    wallet_object.save()
                    response_data = {
                        'message': 'Wallet has been updated successfully.'
                    }
                    response_status_code = status.HTTP_200_OK
                else:
                    response_data = {'errors': serializer.errors}
                    response_status_code = status.HTTP_400_BAD_REQUEST
        else:
            response_data = {'errors': 'PK is requirede.'}
            response_status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=response_data, status=response_status_code)

    def delete(self, request, *args, **kwargs):
        """ DELETE method use for delete a wallet. """

        if kwargs.get('pk'):
            try:
                wallet_query = Wallet.objects.get(
                    id=kwargs.get('pk'), owner=request.user)
            except ObjectDoesNotExist:
                response_data = {'errors': 'Group not found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            else:
                wallet_query.delete()
                response_data = None
                response_status_code = status.HTTP_204_NO_CONTENT
        else:
            response_data = {'errors': 'PK is requirede.'}
            response_status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=response_data, status=response_status_code)
