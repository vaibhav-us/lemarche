from rest_framework.serializers import ModelSerializer
from .models import Product,Category,UserModel,Campus,Message,Room
from rest_framework import serializers

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class UserModelSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields ='__all__'

class CampusSerializer(ModelSerializer):
    class Meta:
        model = Campus
        fields ='__all__'

class RoomSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.title', read_only=True)
    product_img = serializers.CharField(source='product.imgUrl', read_only=True)
    buyer_name = serializers.CharField(source='user1.name', read_only=True)
    seller_name = serializers.CharField(source='user2.name', read_only=True)


    class Meta:
        model = Room
        fields = '__all__'

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields ='__all__'