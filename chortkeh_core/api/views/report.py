import jdatetime
from rest_framework import views, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from chortkeh_core.models import Income
from chortkeh_core import utils

# TODO: Rewrite code for support leap year.


class PaginationClass(LimitOffsetPagination):
    default_limit = 20


class ReportIncomeApiView(views.APIView):
    """ This api view for get report of income transaction with filters. """

    permission_classes = (permissions.IsAuthenticated,)
    allowed_methods = ('GET',)

    def get(self, request, *args, **kwargs):
        """ GET method use for get details... """

        filter_by = request.GET.get('filterby')
        filter_id = request.GET.get('id')
        year = kwargs.get('year')
        month = kwargs.get('month')
        day = kwargs.get('day')

        if (year is None) or (
                month is not None and month > 12) or (
                    day is not None and day > 31):
            return Response(
                data={'errors': 'Datetime is not valid'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if year and month and day:
            time_gte = jdatetime.datetime(year, month, day)
            time_lte = jdatetime.datetime(year, month, day, 23, 59, 59)
        elif year and month:
            if month <= 6:
                end = 31
            elif month == 12:
                end = 29
            else:
                end = 30
            time_gte = jdatetime.datetime(year, month, 1)
            time_lte = jdatetime.datetime(year, month, end, 23, 59, 59)
        elif year:
            time_gte = jdatetime.datetime(year, 1, 1)
            time_lte = jdatetime.datetime(year, 12, 29, 23, 59, 59)

        if filter_by == 'group' and filter_id is not None:
            inc_obj = Income.objects.filter(
                wallet__owner=request.user,
                time__gte=time_gte, time__lte=time_lte,
                group_id=int(filter_id)
            ).order_by('-time')
        elif filter_by == 'wallet' and filter_id is not None:
            inc_obj = Income.objects.filter(
                wallet__owner=request.user,
                time__gte=time_gte, time__lte=time_lte,
                wallet_id=int(filter_id)
            ).order_by('-time')
        else:
            inc_obj = Income.objects.filter(
                wallet__owner=request.user,
                time__gte=time_gte, time__lte=time_lte
            ).order_by('-time')
        paginator = PaginationClass()
        paginate_results = paginator.paginate_queryset(inc_obj, request)
        response_list = [{
            'id': q.id,
            'amount': q.amount,
            'time': utils.jdate_to_str(q.time),
            'comment': q.comment,
            'wallet_id': q.wallet_id,
            'wallet_name': q.wallet.name,
            'group_id': q.group_id,
            'group_name': q.group.name
        } for q in paginate_results]
        response_data = {
            'count': paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': response_list
        }
        response_status_code = status.HTTP_200_OK

        return Response(data=response_data, status=response_status_code)
