from rest_framework import status, views, permissions
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from chortkeh_core.models import Group
from chortkeh_core.api.serializers import GroupSerializer


class GroupApiView(views.APIView):
    """ Api view for group management. """

    permission_classes = (permissions.IsAuthenticated,)
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')

    def get(self, request, *args, **kwargs):
        """ GET method use for get details of groups. """

        if kwargs.get('pk'):
            try:
                group_query = Group.objects.get(
                    id=kwargs.get('pk'), owner=request.user)
            except ObjectDoesNotExist:
                response_data = {'errors': 'Group not found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            else:
                response_data = {
                    'id': group_query.id,
                    'name': group_query.name,
                    'action_type': group_query.action_type
                }
                response_status_code = status.HTTP_200_OK
        else:
            group_queryset = Group.objects.filter(owner=request.user)
            if group_queryset.count() > 0:
                group_list = [{
                    'id': q.id,
                    'name': q.name,
                    'action_type': q.action_type
                } for q in group_queryset]
                response_data = {
                    'count': group_queryset.count(),
                    'items': group_list
                }
                response_status_code = status.HTTP_200_OK
            else:
                response_data = {'errors': 'You don\'t have a group.'}
                response_status_code = status.HTTP_404_NOT_FOUND

        return Response(data=response_data, status=response_status_code)

    def post(self, request, *args, **kwargs):
        """ POST method use for create a new group. """

        serializer = GroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group_object = Group.objects.create(
            owner=request.user,
            name=serializer.validated_data.get('name'),
            action_type=serializer.validated_data.get('action_type')
        )
        return Response(
            data={'id': group_object.id}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """ PUT method use for update a group. """

        if kwargs.get('pk'):
            try:
                group_query = Group.objects.get(id=kwargs.get('pk'))
            except ObjectDoesNotExist:
                response_data = {'errors': 'Group not found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            else:
                serializer = GroupSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                group_query.name = serializer.validated_data.get('name')
                group_query.action_type = serializer.validated_data.get(
                    'action_type')
                group_query.save()
                response_data = {
                    'message': 'Group has been updated successfully.'
                }
                response_status_code = status.HTTP_200_OK
        else:
            response_data = {'errors': 'PK is requirede.'}
            response_status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=response_data, status=response_status_code)

    def delete(self, request, *args, **kwargs):
        """ DELETE method use for delete a group. """

        if kwargs.get('pk'):
            try:
                group_query = Group.objects.get(
                    id=kwargs.get('pk'), owner=request.user)
            except ObjectDoesNotExist:
                response_data = {'errors': 'Group not found.'}
                response_status_code = status.HTTP_404_NOT_FOUND
            else:
                group_query.delete()
                response_data = None
                response_status_code = status.HTTP_204_NO_CONTENT
        else:
            response_data = {'errors': 'PK is required.'}
            response_status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=response_data, status=response_status_code)
