from django.shortcuts import render,redirect

#For creating user and flashing the messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import Group

#For logging the user
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Custom-built imports
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import *


@login_required(login_url='login')
def home(request):
	if request.user.is_superuser:
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
	else:
		return redirect('user-page')

@login_required(login_url='login')
@staff_member_required(login_url= 'user-page')
def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products':products})


@login_required(login_url='login')
@staff_member_required(login_url= 'user-page')
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
@staff_member_required(login_url= 'user-page')
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
@staff_member_required(login_url= 'user-page')
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
@staff_member_required(login_url= 'user-page')
def deleteOrder(request,pk):
	order = Order.objects.get(id = pk)
	if request.method == "POST":
		order.delete()
		return redirect('accounts-home')
	context = {
		'item' : order,
	}
	return render(request,'accounts/delete.html' , context)


@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method=="POST":
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username=form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)
			Customer.objects.create(
				user=user
			)

			messages.success(request,"Account created succesfull for "+username)
			return redirect('login')
	context = {
		'form' : form,
	}
	return render(request,'accounts/register.html' , context)

@unauthenticated_user
def loginPage(request):
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

@login_required(login_url='login')
def userPage(request):
	orders=request.user.customer.order_set.all() 
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {
		'orders' : orders,
		'total_orders':total_orders,
		'delivered':delivered,
		'pending':pending
	}
	return render(request , 'accounts/user.html' ,context)

@login_required(login_url='login')
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)