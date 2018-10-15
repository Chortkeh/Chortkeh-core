from rest_framework import views, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from chortkeh_core.models import Income, Expense, Group, Wallet, Transfer
from chortkeh_core.api.serializers import (
    IncomeTransactionSerializer, ExpenseTransactionSerializer,
    TransferTransactionSerializer
)
from chortkeh_core import utils


class PaginationClass(LimitOffsetPagination):
    default_limit = 20


class IncomeTransactionApiView(views.APIView):
    """ This api view use for income transactions management. """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """ GET Method use for get list of transactions. """

        if not kwargs.get('pk'):
            inc_obj = Income.objects.filter(
                wallet__owner=request.user).order_by('-time')
            paginator = PaginationClass()
            paginator_res = paginator.paginate_queryset(inc_obj, request)
            response_list = [{
                'id': q.id,
                'amount': q.amount,
                'time': utils.to_jalali(q.time),
                'comment': q.comment,
                'wallet_id': q.wallet_id,
                'group_id': q.group_id,
                'type': q.group.action_type
            } for q in paginator_res]
            response_data = {
                'count': paginator.count,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'results': response_list
            }
            response_status_code = status.HTTP_200_OK
        else:
            try:
                inc_obj = Income.objects.get(
                    id=kwargs.get('pk'), wallet__owner=request.user
                )
            except inc_obj.ObjectDoesNotExist:
                response_data = {'errors': 'Transaction not found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            else:
                response_data = {
                    'id': inc_obj.id,
                    'amount': inc_obj.amount,
                    'time': utils.to_jalali(inc_obj.time),
                    'comment': inc_obj.comment,
                    'wallet_id': inc_obj.wallet_id,
                    'group_id': inc_obj.group_id,
                    'type': inc_obj.group.action_type
                }
                response_status_code = status.HTTP_200_OK

        return Response(data=response_data, status=response_status_code)

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


class ExpenseTransactionApiView(views.APIView):
    """ This api view use for expense transactions management. """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """ GET Method use for get list of transactions. """

        if not kwargs.get('pk'):
            obj = Expense.objects.filter(
                wallet__owner=request.user).order_by('-time')
            paginator = PaginationClass()
            paginator_res = paginator.paginate_queryset(obj, request)
            response_list = [{
                'id': q.id,
                'amount': q.amount,
                'time': utils.to_jalali(q.time),
                'comment': q.comment,
                'wallet_id': q.wallet_id,
                'group_id': q.group_id,
                'type': q.group.action_type
            } for q in paginator_res]
            response_data = {
                'count': paginator.count,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'results': response_list
            }
            response_status_code = status.HTTP_200_OK
        else:
            try:
                exp_obj = Expense.objects.get(
                    id=kwargs.get('pk'), wallet__owner=request.user
                )
            except exp_obj.ObjectDoesNotExist:
                response_data = {'errors': 'Transaction not found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            else:
                response_data = {
                    'id': exp_obj.id,
                    'amount': exp_obj.amount,
                    'time': utils.to_jalali(exp_obj.time),
                    'comment': exp_obj.comment,
                    'wallet_id': exp_obj.wallet_id,
                    'group_id': exp_obj.group_id,
                    'type': exp_obj.group.action_type
                }
                response_status_code = status.HTTP_200_OK

        return Response(data=response_data, status=response_status_code)

    def post(self, request, *args, **kwargs):
        """ POST method use for create new transaction. """

        rq = request.data.copy()
        rq.time = utils.to_gregorian(request.data.get('time'))
        serializer = ExpenseTransactionSerializer(data=rq)
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
            inc_obj = Expense.objects.create(
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
                inc_obj = Expense.objects.get(
                    id=kwargs.get('pk'), wallet__owner=request.user)
                rq = request.data.copy()
                rq.time = utils.to_gregorian(request.data.get('time'))
                serializer = ExpenseTransactionSerializer(data=rq)
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
                inc_obj = Expense.objects.get(
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


class TransferTransactionApiView(views.APIView):
    """ This api view use for transfer transactions management. """

    permission_classes = (permissions.IsAuthenticated,)
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')

    def get(self, request, *args, **kwargs):
        """ GET method use for get details of transfer transactions. """

        if kwargs.get('pk'):
            try:
                obj = Transfer.objects.get(
                    id=kwargs.get('pk'), source_wallet__owner=request.user)
            except obj.ObjectDoesNotExist:
                response_data = {'errors': 'Transaction not found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            else:
                response_data = {
                    'id': obj.id,
                    'amount': obj.amount,
                    'time': utils.to_jalali(obj.time),
                    'comment': obj.comment,
                    'source_wallet': obj.source_wallet,
                    'target_wallet': obj.target_wallet
                }
                response_status_code = status.HTTP_200_OK
        else:
            queryset = Transfer.objects.filter(
                source_wallet__owner=request.user).order_by('-time')
            paginator = PaginationClass()
            paginator_results = paginator.paginate_queryset(queryset, request)
            results_list = [{
                'id': q.id,
                'amount': q.amount,
                'time': utils.to_jalali(q.time),
                'comment': q.comment,
                'source_wallet': q.source_wallet,
                'target_wallet': q.target_wallet
            } for q in paginator_results]
            response_data = {
                'count': paginator.count,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'results': results_list
            }
            response_status_code = status.HTTP_200_OK

        return Response(data=response_data, status=response_status_code)

    def post(self, request, *args, **kwargs):
        """ POST method use for create new transaction. """
        rq = request.data.copy()
        rq.time = utils.to_gregorian(request.data.get('time'))
        serializer = TransferTransactionSerializer(data=rq)
        serializer.is_valid(raise_exception=True)
        try:
            src_wlt = Wallet.objects.get(
                id=serializer.validated_data.get('source_wallet'),
                owner=request.user)
            trg_wlt = Wallet.objects.get(
                id=serializer.validated_data.get('target_wallet'),
                owner=request.user)
        except src_wlt.ObjectDoesNotExist:
            response_data = {'errors': 'Source wallet is not Found.'}
            response_status_code = status.HTTP_404_NOT_FOUND
        except trg_wlt.ObjectDoesNotExist:
            response_data = {'errors': 'Target wallet is not Found.'}
            response_status_code = status.HTTP_404_NOT_FOUND
        else:
            obj = Transfer.objects.create(
                amount=serializer.validated_data.get('amount'),
                time=serializer.validated_data.get('time'),
                comment=serializer.validated_data.get('comment'),
                source_wallet=src_wlt, target_wallet=trg_wlt
            )
            response_data = {'id': obj.id}
            response_status_code = status.HTTP_201_CREATED

        return Response(data=response_data, status=response_status_code)

    def put(self, request, *args, **kwargs):
        """ PUT method use for edit a transfer transaction. """

        if kwargs.get('pk'):
            try:
                obj = Transfer.objects.get(
                    id=kwargs.get('pk'), source_wallet__owner=request.user)
                rq = request.data.copy()
                rq.time = utils.to_gregorian(request.data.get('time'))
                serializer = TransferTransactionSerializer(data=rq)
                serializer.is_valid(raise_exception=True)
                src_wlt = Wallet.objects.get(
                    id=serializer.validated_data.get('source_wallet'),
                    owner=request.user)
                trg_wlt = Wallet.objects.get(
                    id=serializer.validated_data.get('target_wallet'),
                    owner=request.user)
            except obj.ObjectDoesNotExist:
                response_data = {'errors': 'Transaction not found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            except src_wlt.ObjectDoesNotExist:
                response_data = {'errors': 'Source wallet not found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            except trg_wlt.ObjectDoesNotExist:
                response_data = {'errors': 'Target wallet not found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            else:
                obj.amount = serializer.validated_data.get('amount')
                obj.time = serializer.validated_data.get('time')
                obj.comment = serializer.validated_data.get('comment')
                obj.source_wallet = serializer.validated_data.get(
                    'source_wallet')
                obj.target_wallet = serializer.validated_data.get(
                    'target_wallet')
                obj.save()
                response_data = {
                    'message': 'Transaction has been updated successfully.'}
                response_status_code = status.HTTP_200_OK
        else:
            response_data = {'errors': 'PK is requirede.'}
            response_status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=response_data, status=response_status_code)

    def delete(self, request, *args, **kwargs):
        """ DELETE method use for delete a transfer transaction."""

        if kwargs.get('pk'):
            try:
                obj = Transfer.objects.get(
                    id=kwargs.get('pk'), source_wallet__owner=request.user)
            except obj.ObjectDoesNotExist:
                response_data = {'errors': 'Transaction not found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            else:
                obj.delet()
                response_data = None
                response_status_code = status.HTTP_204_NO_CONTENT
        else:
            response_data = {'errors': 'PK is requirede.'}
            response_status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=response_data, status=response_status_code)
