from django.urls import path
from . import views

urlpatterns = [
    path('' , views.home , name = 'accounts-home'),
    path('products/' , views.products , name = 'accounts-products'),
    path('customer/<str:pk_test>/' , views.customer , name = 'accounts-customer'),
    path('create_order/' , views.createOrder , name = 'create-order'),
    path('update_order/<str:pk>/' , views.updateOrder , name = 'update-order'),
    path('delete/<str:pk>/' , views.deleteOrder , name = 'delete-order'),
]