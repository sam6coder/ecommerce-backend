from django.urls import path,include

from api import views

urlpatterns = [
    path('',views.home,name="home"),
    path('category/',include('api.category.urls')),
    path('user/',include('api.users.urls')),
    path('products/',include('api.product.urls')),
    path('order/',include('api.order.urls'))
]
