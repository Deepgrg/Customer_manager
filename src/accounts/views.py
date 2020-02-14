from django.shortcuts import render

def home(request):
    context={}
    return render(request,'accounts/index.html',context)

def products(request):
    context={}
    return render(request,'accounts/products.html',context)

def customer(request):
    context={}
    return render(request,'accounts/customer.html',context)