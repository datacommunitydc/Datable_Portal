from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from user_api.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount


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


class ProfileViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    def get(self, request, format=None):
        """
        return profile
        """
        try:
            # get the social accounts from current user
            AccountObj = SocialAccount.objects.get(user=request.user)

            TokenObj = SocialToken.objects.get(account=AccountObj)
            data = {
                'username': request.user.username,
                'objectId': request.user.pk,
                'firstName': request.user.first_name,
                'lastName': request.user.last_name,
                'Token': TokenObj.token,
                'email': request.user.email,
                'auth_provider': AccountObj.provider,
            }

            return Response(status=200, data=data)
        except Exception, err:
            return Response(status=401, data={
                'detail': 'Bad Access Token',
                'error': str(err)
            })
