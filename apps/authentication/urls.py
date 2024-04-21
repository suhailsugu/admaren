from django.urls import include, path, re_path
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework import routers

app_name = 'authentication'



urlpatterns = [
    
    path('login', views.LoginAPIView.as_view(), name= 'login'),
    path('token/refresh/', views.TokenRefreshAPIView.as_view(), name='token_refresh'),
    re_path(r'^logout', views.LogoutAPIView.as_view(), name='logout'),
    
    
]
