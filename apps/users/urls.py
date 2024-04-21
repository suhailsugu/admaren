from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [

    path('create-or-update-user', views.CreateOrUpdateUserApiView.as_view(), name='create-or-update-user'),
    path(r'get-users-list', views.GetUsersListApiView.as_view()),
    path('get-user-details', views.GetUserDetailApiView.as_view()),
    
]
