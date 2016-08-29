from django.contrib.auth.models import User, Group
from django.forms.models import model_to_dict
from rest_framework import viewsets, mixins, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import json

from datable_project import exceptions
from . import models
from . import serializers
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


# class ProfileViewSet(mixins.RetrieveModelMixin,
#                      mixins.UpdateModelMixin,
#                      viewsets.GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#
#     def get_object(self):
#         return self.request.user


class ProfileViewSet(APIView):
    def get(self, request, format=None):
        return Response(model_to_dict(self.request.user))


class VerifyAccessToken(APIView):
    """
    to verify access token according to type
    """

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
            data = obj_cls.verify()
        except AttributeError as error:
            raise exceptions.NotImplementedEXception(
                'UnimplementedExceptions: provider {} unimplemented '.format(provider)
            )

        # check if user is already present if not create one and send the token


        return Response(json.loads(data))

