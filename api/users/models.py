from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    name=models.CharField(max_length=50,default='Anonymous')
    email=models.EmailField(max_length=254,unique=True)
    
    username=None
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    CATEGORY_CHOICES=[
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other')
    ]
    
    phone=models.CharField(max_length=10,blank=True,null=True)
    gender=models.CharField(max_length=10,choices=CATEGORY_CHOICES,default='Male')
    home_address=models.CharField(max_length=100,null=True,blank=True)
    pincode=models.CharField(max_length=10,null=True,blank=True)
    area=models.CharField(max_length=100,null=True,blank=True)
    session_token=models.CharField(max_length=10,default='0')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    
    
