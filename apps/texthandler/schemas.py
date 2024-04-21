
from rest_framework import serializers
from apps.texthandler.models import Snippet, TagModel

"""Snippet Text Schemas"""
class SnippetTextListSchema(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Snippet
        fields = ['id','content','title','timestamp','detail_url']
    
    def get_detail_url(self, instance):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(f'/api/texthandler/v1/get-snippet-text-details?id={instance.id}')
        return None
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    

class SnippetTextDetailSchema(serializers.ModelSerializer):
    title = serializers.CharField(source='title.tagtitle',allow_null=True)
    
    class Meta:
        model = Snippet
        fields = ['pk','content','title','timestamp']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas



"""Tag Title Schemas"""
class TagTitlesListSchema(serializers.ModelSerializer):
 
    class Meta:
        model = TagModel
        fields = ['id','tagtitle']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas


class TagTitlesDetailSchema(serializers.ModelSerializer):
    snippets = serializers.SerializerMethodField()
    
    class Meta:
        model = TagModel
        fields = ['id','tagtitle','snippets']
    
    def get_snippets(self, instance):
        snippet_queryset = Snippet.objects.filter(title=instance)

        if snippet_queryset is not None and len(snippet_queryset)>0:
            return SnippetTextDetailSchema(snippet_queryset,many=True).data
        
        return []
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
 