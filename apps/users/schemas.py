from rest_framework import serializers
from apps.users.models import  Users


class GetUsersListApiSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['pk','username','email']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    
    
class GetUsersDetailApiSerializers(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['pk','username','email','is_superuser','is_active','is_admin']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas


