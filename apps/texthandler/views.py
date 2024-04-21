import sys,os
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.texthandler.models import  TagModel,Snippet
from admaren.helpers.helper import get_object_or_none
from admaren.helpers.pagination import RestPagination
from admaren.helpers.response import ResponseInfo
from admaren.helpers.custom_messages import _success,_record_not_found
from rest_framework.permissions import IsAuthenticated
from apps.texthandler.serializers import  CreateSnippetTextserializer, DeleteSnippetTextSerializer, UpdateSnippetTextserializer
from apps.texthandler.schemas import SnippetTextListSchema, SnippetTextDetailSchema, TagTitlesDetailSchema, TagTitlesListSchema
import logging
from drf_yasg import openapi
from django.db.models import Q



logger = logging.getLogger(__name__)


"""Snippet Text Views"""
class CreateSnippetTextApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateSnippetTextApiView, self).__init__(**kwargs)
    
    serializer_class          = CreateSnippetTextserializer
    permission_classes        = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Snippet"])
    def post(self, request):
        try:
            
            serializer = self.serializer_class(data=request.data, context = {'request' : request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()

            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class UpdateSnippetTextApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UpdateSnippetTextApiView, self).__init__(**kwargs)
    
    serializer_class          = UpdateSnippetTextserializer
    response_class            = SnippetTextDetailSchema
    permission_classes        = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Snippet"])
    def put(self, request):
        try:

            snippet_instance = get_object_or_none(Snippet,pk=request.data.get('id'))
            
            if snippet_instance is None:
                self.response_format['status_code'] = status.HTTP_204_NO_CONTENT
                self.response_format["message"] = _record_not_found
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_200_OK)

            serializer = self.serializer_class(snippet_instance,data=request.data, context = {'request' : request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            snippet_instance = serializer.save()

            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["data"] = self.response_class(snippet_instance, context={'request': request}).data
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetSnippetTextListApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetSnippetTextListApiView, self).__init__(**kwargs)
    
    serializer_class    = SnippetTextListSchema
    permission_classes  = [IsAuthenticated]
    pagination_class    = RestPagination
  
    search        = openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING,description="The search value ", required=False)
  
    @swagger_auto_schema(tags=["Snippet"], manual_parameters=[search], pagination_class=RestPagination)
    def get(self, request):
        
        try:
            search_value    = request.GET.get('search', None)

            filter_set = Q()
            if search_value not in ['',None]:
                filter_set = Q(content=search_value)
     
            queryset    = Snippet.objects.filter(filter_set).order_by('-id')
            page        = self.paginate_queryset(queryset)
            serializer  = self.serializer_class(page, many=True,context={'request':request})
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class GetSnippetTextDetailApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetSnippetTextDetailApiView, self).__init__(**kwargs)

    serializer_class = SnippetTextDetailSchema
    permission_classes  = (IsAuthenticated,)

    id = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=True, description="Enter id")

    @swagger_auto_schema(tags=["Snippet"], manual_parameters=[id])
    def get(self, request):

        try:
            snippet_instance = get_object_or_none(Snippet, pk=request.GET.get('id', None))

            if snippet_instance is None:
                self.response_format['status_code'] = status.HTTP_204_NO_CONTENT
                self.response_format["message"] = _record_not_found
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_200_OK)

            self.response_format['status_code'] = status.HTTP_200_OK
            self.response_format["data"] = self.serializer_class(snippet_instance, context={'request': request}).data
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)

        except Exception as e:

            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

      
class DeleteSnippetTextApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DeleteSnippetTextApiView, self).__init__(**kwargs)

    serializer_class   = DeleteSnippetTextSerializer
    permission_classes = (IsAuthenticated,)

    pk= openapi.Schema('Destroy reason codes record', in_=openapi.IN_BODY,required=['pk'], properties={'pk': openapi.Schema(type=openapi.TYPE_INTEGER)},type=openapi.TYPE_OBJECT)


    @swagger_auto_schema(tags=["Snippet"])
    def delete(self, request):
        try:
            serializer = self.serializer_class(data=request.data,context={'request':request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            ids = serializer.validated_data.get('id',None)
            Snippet.objects.filter(id__in = ids).delete()


            self.response_format['status_code'] = status.HTTP_200_OK
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)



        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



"""Tag Title Views"""
class GetTagTitlesListApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetTagTitlesListApiView, self).__init__(**kwargs)
    
    serializer_class    = TagTitlesListSchema
    permission_classes  = [IsAuthenticated]
    pagination_class    = RestPagination
  
    search        = openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING,description="The search value ", required=False)
  
    @swagger_auto_schema(tags=["Tag Title"], manual_parameters=[search], pagination_class=RestPagination)
    def get(self, request):
        
        try:
            search_value    = request.GET.get('search', None)

            filter_set = Q()
            if search_value not in ['',None]:
                filter_set = Q(tagtitle=search_value)
     
            queryset    = TagModel.objects.filter(filter_set).order_by('-id')
            page        = self.paginate_queryset(queryset)
            serializer  = self.serializer_class(page, many=True,context={'request':request})
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class GetTagTitlesDetailApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetTagTitlesDetailApiView, self).__init__(**kwargs)

    serializer_class = TagTitlesDetailSchema
    permission_classes  = (IsAuthenticated,)

    id = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=True, description="Enter id")

    @swagger_auto_schema(tags=["Snippet"], manual_parameters=[id])
    def get(self, request):

        try:
            tag_instance = get_object_or_none(TagModel, pk=request.GET.get('id', None))

            if tag_instance is None:
                self.response_format['status_code'] = status.HTTP_204_NO_CONTENT
                self.response_format["message"] = _record_not_found
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_200_OK)

            self.response_format['status_code'] = status.HTTP_200_OK
            self.response_format["data"] = self.serializer_class(tag_instance, context={'request': request}).data
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)

        except Exception as e:

            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



