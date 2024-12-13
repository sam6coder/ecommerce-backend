from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout
import random
import re
import json
from django.utils.decorators import method_decorator
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny



def generate_session_token(length=10):   #number of characters in session token is 10
    char_list=[chr(i) for i in range(97,123)]   # a to z
    int_list=[str(i) for i in range(10)]     # strings ['0','1','2'......'9']
    
    return ''.join(random.SystemRandom().choice(char_list+int_list) for _ in range(length))


@csrf_exempt
def signin(request):
    if not request.method=='POST':
        return JsonResponse({'error':'You are not eligible for login'})
    # print(request.POST)
    # data=json.loads(request.body)
    username=request.POST.get('email')
    password=request.POST.get('password')
    
    if not username:
        return JsonResponse({'error':'Email is required'})
    
    if not password:
        return JsonResponse({'error':'Password is required'})
    
    if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$",username):
        return JsonResponse({'error':'Enter a valid email'})

    if len(password)<6:
        return JsonResponse({'error':'Password must be 6 characters long'})

    UserModel=get_user_model()
    
    try:
        user=UserModel.objects.get(email=username)
        
        if user.check_password(password):
            usr=UserModel.objects.filter(email=username).values().first()
            usr.pop('password')
            
            #if session_token is not 0 , it's already running(user is logged in )
            
            if user.session_token!='0':
                user.session_token='0'   # if user is not logged in we set session_token to 0
                user.save()
                return JsonResponse({'error':'Previous session exists'})
            
            
            token=generate_session_token()
            user.session_token=token
            
            user.save()
            login(request,user) #log user in
            return JsonResponse({'token':token,'user':usr})

        else:
            return JsonResponse({'token':'Invalid password'})
        
    except UserModel.DoesNotExist:
        return JsonResponse({'token':'Invalid Email'})
    
@csrf_exempt
def signout(request,id):
    # data=json.loads(request.body)
    username=request.POST.get('email')
    password=request.POST.get('password')
    token=request.POST.get('token')
    
    UserModel=get_user_model()
    
    
    if not username:
        return JsonResponse({'error':'Email is required'})
    if not password:
        return JsonResponse({'error':'Password is required'})
    if not token:
        return JsonResponse({'error':'Token is required'})
    
    try:
        user=UserModel.objects.get(pk=id)   
        user.session_token='0'
        user.save()
        logout(request)
        
    except UserModel.DoesNotExist:
        return JsonResponse({'error':'Invalid user id'})
    
    return JsonResponse({'success':'Logout Successful'})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create' : [AllowAny]}
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[AllowAny]
    
    @method_decorator(csrf_exempt)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    def get_permissions(self):
        try:
            # Return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]

        except KeyError:
            # If action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
            
                    
            
                

