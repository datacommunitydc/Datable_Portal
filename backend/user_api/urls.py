from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views as auth_views
from django.views.decorators.csrf import csrf_exempt

from . import views

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'signup', views.SignUpViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/', views.LoginView.as_view()),
    url(r'^api-token-auth/', auth_views.obtain_auth_token),
    url(r'verify-token/', views.VerifyAccessToken.as_view()),
    url(r'profile/', views.ProfileViewSet.as_view()),
]