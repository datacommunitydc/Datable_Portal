from django.conf.urls import url, include
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^sign_up/$', views.SignUp.as_view(), name="sign_up"),
    #url(r'^profile/$', views.ProfileViewSet.as_view()),
    #url(r'^rest/facebook-login/$',csrf_exempt(RestGoogleLogin.as_view()),name='rest-facebook-login'),
]