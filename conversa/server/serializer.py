from rest_framework import serializers
from .models import Server,Channel,Category
from drf_spectacular.utils import extend_schema_field

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"

class ServerSerializer(serializers.ModelSerializer):
    num_members = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many=True)
    category = serializers.StringRelatedField() # to change dafault item.name(id) into name 
    
    class Meta:
        model = Server
        exclude = ("member",) 
    
    @extend_schema_field(int)
    def get_num_members(self,obj) -> int:
        if hasattr(obj,"num_members"):
            return obj.num_members
        return None
    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")
        # remove key num_members from api data if there is no member
        if not num_members:
            data.pop("num_members",None)
        return data