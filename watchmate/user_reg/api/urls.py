from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urls import path
from . import views

urlpatterns= [
    path('/login/',obtain_auth_token,name='login'),
    path('/register/',views.register_view,name='register'),
]