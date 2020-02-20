from django.shortcuts import render,redirect

#For creating user and flashing the messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

#For logging the user
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Custom-built imports
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter


@login_required(login_url='login')
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

	return render(request, 'accounts/index.html', context)


@login_required(login_url='login')
def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products':products})


@login_required(login_url='login')
def customer(request , pk_test):
	customer = Customer.objects.get(id = pk_test)
	orders= Order.objects.filter( customer = customer)
	total_orders = orders.count()

	myFilter = OrderFilter(request.GET , queryset = orders)
	orders = myFilter.qs
	context={
		'customer' : customer,
		'orders' : orders,
		'total_orders' : total_orders,
		'myFilter' : myFilter,
	}
	return render(request, 'accounts/customer.html',context)


@login_required(login_url='login')
def createOrder(request):
	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('accounts-home')
	context = {
		'form' : form,
	}
	return render(request , 'accounts/order_form.html' ,context)


@login_required(login_url='login')
def updateOrder(request , pk):
	order = Order.objects.get(id = pk)
	form = OrderForm(instance = order)
	if request.method == 'POST':
		form = OrderForm(request.POST ,instance=order)
		if form.is_valid():
			form.save()
			return redirect('accounts-home')
	context={
		'form':form,
	}
	return render(request ,'accounts/order_form.html' ,context)


@login_required(login_url='login')
def deleteOrder(request,pk):
	order = Order.objects.get(id = pk)
	if request.method == "POST":
		order.delete()
		return redirect('accounts-home')
	context = {
		'item' : order,
	}
	return render(request,'accounts/delete.html' , context)


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('accounts-home')
	else:
		form = CreateUserForm()
		if request.method=="POST":
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user=form.cleaned_data.get('username')
				messages.success(request,"Account created succesfull for"+user)
				return redirect('login')
		context = {
			'form' : form,
		}
		return render(request,'accounts/register.html' , context)


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('accounts-home')
	else:
		if request.method=="POST":
			username= request.POST.get('username')
			password= request.POST.get('password')

			user=authenticate(request,username=username,password=password)
			if user is not None:
				login(request,user)
				return redirect('accounts-home')
			else:
				messages.info(request , 'Username or Password is incorrect')
		context = {}
		return render(request,'accounts/login.html' , context)


def logoutUser(request):
	logout(request)
	return redirect('login')