
from django.urls import path,include,re_path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [

    re_path(r'^v1/', include([
        path('create-snippet-text',views.CreateSnippetTextApiView.as_view()),
        path('update-snippet-text',views.UpdateSnippetTextApiView.as_view()),
        path('get-snippet-text-list', views.GetSnippetTextListApiView.as_view()),
        path('get-snippet-text-details', views.GetSnippetTextDetailApiView.as_view()),
        path('delete-snippet-text', views.DeleteSnippetTextApiView.as_view()),
        
        
        path('get-tag-titles-list', views.GetTagTitlesListApiView.as_view()),
        path('get-tag-titles-details', views.GetTagTitlesDetailApiView.as_view()),




    ]))
]

