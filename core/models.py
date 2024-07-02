from django.db import models
from django.contrib.auth.models import User


class Campus(models.Model):
    campusName = models.CharField(max_length=150)
    
    def __str__(self):
        return self.campusName


class UserModel(models.Model):
    email= models.CharField(max_length = 50 )
    name =models.CharField(max_length = 50)
    pic = models.TextField(max_length=200, null =True, blank =True)
    contactNo = models.IntegerField()
    campus = models.ForeignKey(Campus,on_delete=models.CASCADE,null=True,blank=True)
    location = models.TextField(max_length=200, null =True, blank =True)
    address = models.JSONField(blank=True,null=True)
    def __str__(self):
        return self.name

class Category(models.Model):
    categoryName = models.CharField(max_length = 50)
    imgUrl =models.TextField(max_length=200, null =True, blank =True)

    def __str__(self):
        return self.categoryName
    

class Product(models.Model):
    userId = models.ForeignKey(UserModel,on_delete = models.CASCADE)
    categoryId = models.ForeignKey(Category,on_delete = models.CASCADE)
    title = models.CharField(max_length = 50)
    brand = models.CharField(max_length = 50, null =True, blank =True)
    description = models.TextField(max_length=600, null =True, blank =True)
    price = models.IntegerField()
    datePosted = models.DateTimeField(auto_now = True)
    status = models.BooleanField(default = True)
    imgUrl = models.TextField(max_length=200, null =True, blank =True)
    liked_by = models.ManyToManyField(UserModel,related_name="liked_by", blank=True)
    campus = models.ForeignKey(Campus,on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title
    

class Room(models.Model):
    user1 = models.ForeignKey(UserModel, null=True, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(UserModel, null=True, on_delete=models.CASCADE, related_name='user2')
    room_name = models.CharField(unique=True)
    def save(self, *args, **kwargs):
        if not self.room_name:
            self.room_name = f"{self.user1.id}-{self.user2.id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.room_name
    
class Message(models.Model):
    message = models.TextField(max_length=200)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    def __str__(self):
        return self.message


