import jdatetime
from rest_framework import permissions, status, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from ..permissions import AllowOnlyPost
from ..serializers import CreateAccountSerializer, UpdateAccountSerializer

User = get_user_model()


class GetToken(ObtainAuthToken):
    """ This api view use for login and get token. """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=status.HTTP_200_OK)


class Account(views.APIView):
    """
    API view for get info from user, registration, edit user , and delete user.
    """

    permission_classes = (AllowOnlyPost,)

    def get(self, request, *arg, **kwargs):
        """ GET method use for get user information. """

        user = User.objects.get(id=request.user.id)
        jdate_joined = jdatetime.date.fromgregorian(date=user.date_joined)
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': '{year}-{month}-{day}'.format(
                year=jdate_joined.year,
                month=jdate_joined.month,
                day=jdate_joined.day,
            )
        })

    def post(self, request, *arg, **kwargs):
        """ POST method use for registeration. """

        serializer = CreateAccountSerializer(request.data)
        if serializer.is_valid():
            user_object = User(
                username=serializer.validated_data.get('username'),
                email=serializer.validated_data.get('email'),
                first_name=serializer.validated_data.get('first_name'),
                last_name=serializer.validated_data.get('last_name')
            )
            user_object.set_password(password)
            user_object.save()
            token, _ = Token.objects.get_or_create(user=user_object)
            return Response(data={
                'id': user_object.id,
                'username': user_object.username,
                'email': user_object.email,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                data={'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, *arg, **kwargs):

        serializer = UpdateAccountSerializer(request.data)
        if serializer.is_valid():
            user_object = User.objects.get(id=request.user.id)
            user_object.email = serializer.validated_data.get('email')
            user_object.first_name = serializer.validated_data.get(
                'first_name')
            user_object.last_name = serializer.validated_data.get('last_name')
            user_object.save()
            return Response(
                data={
                    'message': 'Your account has been updated successfully.'
                }, status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, *arg, **kwargs):

        user_object = User.objects.get(id=request.user.id)
        user_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
