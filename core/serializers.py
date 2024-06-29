from rest_framework.serializers import ModelSerializer
from .models import Product,Category,UserModel,Campus,Message,Room

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

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields ='__all__'

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields ='__all__'