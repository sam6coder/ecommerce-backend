from rest_framework import serializers
from api.product.models import Product
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    
    #accepting a list of product_id
    product_id=serializers.PrimaryKeyRelatedField(many=True,queryset=Product.objects.all())
    class Meta:
        model=Order
        fields=('user','id','total_products','total_amount','transaction_id','product_id')
        
    def create(self,validated_data):
        products=validated_data.pop('product_id')
        order=Order.objects.create(**validated_data)  #creating a new instance of Order model and saving it to database
        order.products.set(products)  #adding products to the ManytoManyfield
        return order
        
    def update(self,instance,validated_data):
        products=validated_data.pop('product_id',None)
        if products is not None:
            instance.products.set(products)
        return super().update(instance,validated_data)