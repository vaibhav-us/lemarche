from django.urls import path
from . import views

urlpatterns = [
    path('products/<str:id>/campus/<str:campus>/key/<str:key>/',views.list_products),
    path('categories/',views.list_categories),
    path('user/<str:id>/liked_products/',views.list_liked_products),
    path('user/<str:id>/my_ads/',views.create_list_myads),
    path('user/<str:id>/',views.retrieve_update_acc),
    path('user/<str:usr>/prod/<str:prod>/like/',views.like_retrive_products),
    path('list_campuses/',views.list_campuses),
    path('user/<str:id>/rooms/',views.list_rooms),
    path('getroom/<str:buyer>/<str:seller>/<str:id>/',views.retrieve_room),
]
