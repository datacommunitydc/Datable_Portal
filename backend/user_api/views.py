from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets
#from permissions import IsAuthenticatedOrCreate
from datable_project.permissions import IsAuthenticatedOrCreate
from user_api.serializers import UserSerializer, GroupSerializer, SignUpSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)
