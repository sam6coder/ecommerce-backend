from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import authentication_classes,permission_classes

from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    
    def create(self,validated_data):
       password= validated_data.pop('password',None)
       instance=self.Meta.model(**validated_data)   #this syntax unpacks the dictionary into keyword arguments to create a new instance of model
       if password is not None:        
            instance.set_password(password)  #hashes the password and stores in model instance
   
       instance.save()        #saves model instance to database
       return instance
        
        
    
    def update(self,instance,validated_data):
        
        for attr,value in validated_data.items():
            if attr=='password':
                instance.set_password(value)
            else:
                setattr(instance,attr,value)
                
        instance.save()
        return instance
                
    
    class Meta:
        model=CustomUser
        fields=('name','email','password','phone','gender','is_active','is_staff','is_superuser','home_address','pincode','area')
        
        extra_kwargs={
            'password':{
                'write_only':True,
                'style':{'input_type':'password'}
            }
        }