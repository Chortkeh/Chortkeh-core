from rest_framework import views, status, permissions
from rest_framework.response import Response
from chortkeh_core.models import Income, Group, Wallet
from chortkeh_core.api.serializers import IncomeTransactionSerializer
from chortkeh_core import utils


class IncomeTransactionApiView(views.APIView):
    """ This api view use for income transactions management. """

    permission_classes = (permissions.IsAuthenticated,)

    # TODO: Write GET method...

    def post(self, request, *args, **kwargs):
        """ POST method use for create new transaction. """

        rq = request.data.copy()
        rq.time = utils.to_gregorian(request.data.get('time'))
        serializer = IncomeTransactionSerializer(data=rq)
        serializer.is_valid(raise_exception=True)
        try:
            wl_obj = Wallet.objects.get(
                id=serializer.validated_data.get('wallet_id'),
                owner=request.user
            )
            gp_obj = Group.objects.get(
                id=serializer.validated_data.get('group_id'),
                owner=request.user
            )
        except wl_obj.ObjectDoesNotExist:
            response_data = {'errors': 'Wallet is not Found.'}
            response_status_code = status.HTTP_404_NOT_FOUND
        except gp_obj.ObjectDoesNotExist:
            response_data = {'errors': 'Group is not Found.'}
            response_status_code = status.HTTP_404_NOT_FOUND
        else:
            inc_obj = Income.objects.create(
                wallet=wl_obj, group=gp_obj,
                amount=serializer.validated_data.get('amount'),
                time=serializer.validated_data.get('time'),
                comment=serializer.validated_data.get('comment')
            )
            response_data = {'id': inc_obj.id}
            response_status_code = status.HTTP_201_CREATED

        return Response(data=response_data, status=response_status_code)

    def put(self, request, *args, **kwargs):
        """ PUT method use for edit a transaction. """

        if kwargs.get('pk'):
            try:
                inc_obj = Income.objects.get(
                    id=kwargs.get('pk'), wallet__owner=request.user)
                rq = request.data.copy()
                rq.time = utils.to_gregorian(request.data.get('time'))
                serializer = IncomeTransactionSerializer(data=rq)
                serializer.is_valid(raise_exception=True)
                wl_obj = Wallet.objects.get(
                    id=serializer.validated_data.get('wallet_id'),
                    owner=request.user
                )
                gp_obj = Group.objects.get(
                    id=serializer.validated_data.get('group_id'),
                    owner=request.user
                )
            except inc_obj.ObjectDoesNotExist:
                response_data = {'errors': 'Transaction not found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            except wl_obj.ObjectDoesNotExist:
                response_data = {'errors': 'Wallet is not Found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            except gp_obj.ObjectDoesNotExist:
                response_data = {'errors': 'Group is not Found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            else:
                inc_obj.amount = serializer.validated_data.get('amount')
                inc_obj.time = serializer.validated_data.get('time')
                inc_obj.comment = serializer.validated_data.get('comment')
                inc_obj.wallet = wl_obj
                inc_obj.group = gp_obj
                inc_obj.save()
                response_data = {
                    'message': 'Transaction has been updated successfully.'
                }
                response_status_code = status.HTTP_200_OK
        else:
            response_data = {'errors': 'PK is requirede.'}
            response_status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=response_data, status=response_status_code)

    def delete(self, request, *args, **kwargs):
        """ DELETE method use for delete a transaction. """

        if kwargs.get('pk'):
            try:
                inc_obj = Income.objects.get(
                    id=kwargs.get('pk'), wallet__owner=request.user)
            except inc_obj.ObjectDoesNotExist:
                response_data = {'errors': 'Transaction not found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            else:
                inc_obj.delete()
                response_data = None
                response_status_code = status.HTTP_204_NO_CONTENT
        else:
            response_data = {'errors': 'PK is requirede.'}
            response_status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=response_data, status=response_status_code)
