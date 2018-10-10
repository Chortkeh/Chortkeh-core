import jdatetime
from rest_framework import permissions, status, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from ..permissions import AllowOnlyPost

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

        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if username and password and email and first_name:
            user_object = User(username=username, email=email,
                               first_name=first_name, last_name=last_name)
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
            return Response(data={
                'message': '(username, password, email, first_name) is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
