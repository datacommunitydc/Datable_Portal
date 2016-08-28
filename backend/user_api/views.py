from datetime import datetime

# Django
from django.shortcuts import render
from django.contrib.auth.models import User

# REST Framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Provider OAuth2
from provider.oauth2.models import Client

# User App
from user_api.serializers import (RegistrationSerializer, UserProfileSerializer,
    UserSerializer)

from user_api.models import UserProfile


class RegistrationView(APIView):
    """ Allow registration of new users. """
    permission_classes = ()

    def post(self, request):
        serializer = RegistrationSerializer(data=request.DATA)

        # Check format and unique constraint
        if not serializer.is_valid():
            return Response(serializer.errors,\
                            status=status.HTTP_400_BAD_REQUEST)
        data = serializer.data

        u = User.objects.create(username=data['username'])
        u.set_password(data['password'])
        u.save()

        # Create OAuth2 client
        name = u.username
        client = Client(user=u, name=name, url='' + name,\
                client_id=name, client_secret='', client_type=1)
        client.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """ Get all todos """
        todos = UserProfile.objects.filter(owner=request.user.id)
        serializer = UserProfileSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Adding a new todo. """
        serializer = UserProfileSerializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors, status=
                status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            owner = request.user
            t = UserProfile(owner=owner, description=data['description'], done=False)
            t.save()
            request.DATA['id'] = t.pk # return id
            return Response(request.DATA, status=status.HTTP_201_CREATED)

    def put(self, request, todo_id):
        """ Update a todo """
        serializer = UserProfileSerializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors, status=
                status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            desc = data['description']
            done = data['done']
            t = UserProfile(id=todo_id, owner=request.user, description=desc,\
                     done=done, updated=datetime.now())
            t.save()
            return Response(status=status.HTTP_200_OK)


