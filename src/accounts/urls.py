from django.urls import path
from . import views

urlpatterns = [
    #Home-page
    path('' , views.home , name = 'accounts-home'),

    #To handle the products
    path('products/' , views.products , name = 'accounts-products'),

    #To get to a certain customer
    path('customer/<str:pk_test>/' , views.customer , name = 'accounts-customer'),

    #To handle orders
    path('create_order/' , views.createOrder , name = 'create-order'),
    path('update_order/<str:pk>/' , views.updateOrder , name = 'update-order'),
    path('delete/<str:pk>/' , views.deleteOrder , name = 'delete-order'),

    # To handle the user
    path('login/' , views.loginPage , name='login'),
    path('logout/' , views.logoutUser , name='logout'),
    path('register/' , views.registerPage , name='register'),
]