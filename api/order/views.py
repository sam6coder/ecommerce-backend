from django.shortcuts import render
from .models import Order
from .serializers import OrderSerializer
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def validate_session_token(id,token):
    UserModel=get_user_model()
    
    try:
        user=UserModel.objects.get(pk=id)
        if user.session_token==token:
            return True
        else:
            return False
        
    except UserModel.DoesNotExist:
        return False
    
@csrf_exempt
def add_order(request,id,token):
    if not validate_session_token(id,token):
        return JsonResponse({'error':'Please login again'})
    
    if request.method=='POST':
        user_id=id
        transaction_id=request.POST.get('transaction_id')
        
        
        if not transaction_id:
            return JsonResponse({'error':'Transaction ID is required'})
        amount=request.POST.get('amount')
        
        if not amount:
            return JsonResponse({'error':'Amount is required'})
        
        products=request.POST.get('product_id')
        
        
        if not products:
            return JsonResponse({'error':'Product List is required'})
        try:
            product=eval(products) 
            print(product)
        except Exception:
            return JsonResponse({"error":'"Invalid format'})
        
        
        total_no_of_products=len(product)
        
        UserModel=get_user_model()
        
        try:
            user=UserModel.objects.get(pk=user_id)
            
        except UserModel.DoesNotExist:
            return JsonResponse({'error':'User doesnt exist'})
        
        order_detail=Order(user=user,total_products=total_no_of_products,transaction_id=transaction_id)
        order_detail.save()
        print(product)

        try:
            order_detail.product_id.set(product)
        except Exception as e:
            return JsonResponse({'error':f'Failed to add products to order. Try again : {str(e)}'})
        order_Serializer=OrderSerializer(order_detail)

        
        return JsonResponse({'success':'True','msg':'Order placed successfully',"order":order_Serializer.data})
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset=Order.objects.all().order_by('id')
    serializer_class=OrderSerializer
