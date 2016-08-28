from django.conf.urls import patterns, include, url
from user_api import views
from rest_framework import viewsets, routers

urlpatterns = patterns('',
    # Registration of new users
    url(r'^register/$', views.RegistrationView.as_view()),

    # Todos endpoint
    url(r'^todos/$', views.UserProfileView.as_view()),

    # API authentication
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
    url(r'^api-auth/', include('rest_framework.urls',\
        namespace='rest_framework')),
)

