from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.forms.models import model_to_dict
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers
from datable_project import exceptions, utility
import social_login


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = serializers.UserSerializer
#
#
# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = serializers.GroupSerializer


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    permission_classes = (permissions.AllowAny,) # Or anon users can't register
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class ProfileViewSet(APIView):
    def get(self, request, format=None):
        return Response(model_to_dict(self.request.user))


class VerifyAccessToken(APIView):
    """
    to verify access token according to type
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        """
        Return a list of all users.
        """
        try:
            provider = request.POST['provider']
            access_token = request.POST['access_token']
        except KeyError as error:
            print('caught this error: ' + repr(error))
            raise exceptions.VerifyTokenKeyError()
        try:
            klass = getattr(social_login, provider.title())
            obj_cls = klass(access_token)
            user_data = obj_cls.verify()
        except AttributeError as error:
            raise exceptions.NotImplementedEXception(
                'UnimplementedExceptions: provider {} unimplemented '.format(provider)
            )
        user_data = utility.prepare_user_dict_from_social_data(user_data)
        # check if user is already present if not create one and send the token
        try:
            if User.objects.get(email=user_data['email']):
                print('attach token')
                print(User.objects.get(email=user_data['email']))
        except User.DoesNotExist:

            print('create user and attach')

        return Response(user_data)


class LoginView(APIView):
    permission_classes = ()
    model = Token

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    raise exceptions.UnAuthorizedError('User account is disabled.')
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                raise exceptions.UnAuthorizedError('Unable to login with provided credentials.')
        else:
            raise exceptions.UnAuthorizedError('Must include "username" and "password"')


