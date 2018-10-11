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

    def post(self, request, *args, **kwargs):
        """ POST method use for create new wallet. """

        serializer = WalletSerializer(request.data)
        if serializer.is_valid():
            user_object = User.objects.get(id=request.user.id)
            wallet_object = Wallet.objects.create(
                owner=user_object,
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
                    id=kwargs.get('pk'), owner=request.user
                )
            except ObjectDoesNotExist:
                return Response(
                    data={'errors': 'Wallet not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = WalletSerializer(request.data)
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
