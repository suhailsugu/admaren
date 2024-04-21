from rest_framework import serializers
from apps.texthandler.models import Snippet, TagModel
from admaren.helpers.helper import get_object_or_none, get_token_user_or_none


"""Snippet Text Serializers"""
class CreateSnippetTextserializer(serializers.Serializer):
    content   = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    title     = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model   = Snippet
        fields = ['content','title']

    def validate(self, attrs):
        return super().validate(attrs)
    

    def create(self, validated_data):
        request = self.context.get('request')
        title   = validated_data.get('title', None)
        
        title_instance = TagModel.objects.filter(tagtitle=title).last()

        if title_instance is None:
            title_instance = TagModel.objects.create(tagtitle=title)
       
 
        instance            = Snippet()
        instance.content    = validated_data.get('content', None)
        instance.title      = title_instance
        instance.created_by = get_token_user_or_none(request)
        instance.save()
        
        return instance


class UpdateSnippetTextserializer(serializers.Serializer):
    id        = serializers.IntegerField(required=True,allow_null=True)
    content   = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    title     = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model   = Snippet
        fields = ['id','content','title']

    def validate(self, attrs):
        return super().validate(attrs)


    def update(self, instance, validated_data):
        request = self.context.get('request')
        title   = validated_data.get('title', None)
        
        title_instance = TagModel.objects.filter(tagtitle=title).last()

        if title_instance is None:
            title_instance = TagModel.objects.create(tagtitle=title)

       
        instance.content    = validated_data.get('content', None)
        instance.title      = title_instance
        instance.updated_by = get_token_user_or_none(request)
        instance.save()
        return instance

    
class DeleteSnippetTextSerializer(serializers.ModelSerializer): 
    id= serializers.ListField(child=serializers.IntegerField(), required=True)
   
    class Meta: 
        model= Snippet
        fields= ['id']

