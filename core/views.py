from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Category,Product,UserModel,Campus,Room,Message
from .serializers import CategorySerializer,ProductSerializer,UserModelSerializer,CampusSerializer,RoomSerializer,MessageSerializer
from django.db.models import Q

@api_view(['GET'])
def list_products(request,id,campus,key):
    campusData = Campus.objects.get(id = campus)
    products = Product.objects.filter(campus = campusData)

    if id != 'All':
        category = Category.objects.get(categoryName=id)
        products = products.filter(categoryId=category)
        
    else:
        if key == "null":
            pass
        else:
            products = products.filter(
            Q(title__icontains=key) | 
            # Q(category__icontains=keyword) |
            Q(brand__icontains=key)
            )

        
    
    user = [product.userId for product in products]

    products_serializer = ProductSerializer(products,many=True)
    userSerializer  =UserModelSerializer(user,many=True)
    combined_data =[]
    for product in products_serializer.data:
        user_data =next((item for item in userSerializer.data ), None)
        combined_data.append({**product , "user":user_data})
    return Response({"data":combined_data})

@api_view(['GET'])
def list_categories(request):
    categorys = Category.objects.all()
    categorys_serializer = CategorySerializer(categorys,many=True)
    return Response({"data":categorys_serializer.data})

@api_view(['POST'])
def like_retrive_products(request,usr,prod):

    user_model = UserModel.objects.get(email = usr)
    product = Product.objects.get(id=prod)
   
    if user_model in product.liked_by.all():
        product.liked_by.remove(user_model)
    else:
        product.liked_by.add(user_model)
    product.save()
    prod_serializer = ProductSerializer(product)
    return Response({'data':prod_serializer.data})
    




@api_view(['GET'])
def list_liked_products(request,id):
    user = UserModel.objects.get(email=id)
    liked_products = Product.objects.filter(liked_by=user)
    data = ProductSerializer(liked_products,many=True)
    return Response({"data":data.data})



@api_view(['GET','POST'])
def create_list_myads(request,id):
    user  = UserModel.objects.get(email=id)
    if request.method == 'GET':
        products = Product.objects.filter(userId = user)
        data = ProductSerializer(products,many=True)
        return Response({"data":data.data})
    elif request.method == 'POST':
        category = request.data['category']
        category_model = Category.objects.get(categoryName = category)
        title = request.data['title']
        brand = request.data['brand']
        description = request.data['description']
        imgUrl = request.data['imgUrl']
        price = request.data['price']
        campus = user.campus
        ad = Product.objects.create(userId=user,categoryId=category_model,title=title,brand=brand,description=description,imgUrl=imgUrl,price=price,campus=campus)
        ad.save()
        ad_data = ProductSerializer(ad)
        return Response(ad_data.data)

@api_view(['PUT'])
def update_ad(request,id,user):
    try:
        ad = Product.objects.get(id=id)
        user_model = UserModel.objects.get(email=user)
    except Product.DoesNotExist:
        return Response({'error': 'Ad not found'}, status=404)
    if request.method =='PUT':
        ad.userId=user_model
        ad.categoryId = Category.objects.get(id=request.data['category'])
        ad.title = request.data['title']
        ad.brand = request.data['brand']
        ad.description = request.data['description']
        ad.imgUrl = request.data['imgUrl']
        ad.price = request.data['price']
        ad.campus = user_model.campus  

        ad.save()
        ad_data = ProductSerializer(ad)
        return Response(ad_data.data)
    elif request.method == 'DELETE':
        ad.delete()
        return Response("deleted")



@api_view(['GET', 'PUT'])
def retrieve_update_acc(request, id):
    if request.method == 'GET':
        try:
            user = UserModel.objects.get(email=id)
            user_serializer = UserModelSerializer(user)
            
            campus_serializer = CampusSerializer(user.campus)
            data ={
                **user_serializer.data,"campusName":campus_serializer.data['campusName']
            }
            return Response({"data": data})
        except UserModel.DoesNotExist:
            campus = Campus.objects.get(id=1)
            user = UserModel.objects.create(email=id, name='new user', contactNo=000000,campus=campus)
            user.save()
            user_serializer = UserModelSerializer(user)
            return Response({"data": user_serializer.data})

    elif request.method == 'PUT':
        try:
            user = UserModel.objects.get(email=id)
        except UserModel.DoesNotExist:
            return Response({"error": "User not found."})

        data = {
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'pic': request.data.get('pic'),
            'contactNo': request.data.get('contact'),
            'location': request.data.get('location'),
            'campus':request.data.get('campus'),
        }
        user_serializer = UserModelSerializer(user, data=data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors)
    
@api_view(['GET'])
def list_campuses(request):
    campuses = Campus.objects.all()
    campus_serializer = CampusSerializer(campuses,many=True)
    return Response({"data":campus_serializer.data})

@api_view(['GET'])
def list_rooms(request,id):
    user = UserModel.objects.get(id=id)
    rooms = Room.objects.filter(
        Q(user1=user) |
        Q(user2 = user)
    )

    rooms_serializer = RoomSerializer(rooms,many=True)
    return Response({'data':rooms_serializer.data})

@api_view(['GET'])
def retrieve_room(request,buyer,seller,id):
    buyer = UserModel.objects.get(id=buyer)
    seller = UserModel.objects.get(id=seller)
    product = Product.objects.get(id=id)
    room,created = Room.objects.get_or_create(user1=buyer,user2=seller,product=product)
    room_serializer = RoomSerializer(room)
    return Response({'data':room_serializer.data})

