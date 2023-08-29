from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm
from django.http import JsonResponse
import json
import datetime
from .models import *
from .filter import ProductFilter
from .utils import cookieCart, cartData, guestOrder

# Create your views here.

# def registerPage(request):
#       form = CreateUserForm()

#       if request.method == 'POST':
#             form = CreateUserForm(request.POST)
#             if form.is_valid():
#                   form.save()
#                   return redirect('login')

#       context = {'form': form}
#       return render(request, 'store/register.html', context)

# def loginPage(request):

#       if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')

#             user = authenticate(request, username = username, password = password)

#             if user is not None:
#                   login(request, user)
#                   return redirect('store')
#             else:
#                   messages.info(request, 'Username or password is incorrect')

#       context = {}
#       return render(request, 'store/login.html', context)

# def logoutPage(request):
#       logout(request)
#       return redirect('login')
  
def store(request):     
                
     Data = cookieCart(request)
     items = Data['items']
     order = Data['order']
     cartItems = Data['cartItems']

     products = Product.objects.all()

     myFilter = ProductFilter(request.GET, queryset = products)
     products = myFilter.qs

     context = {'products':products, 'cartItems':cartItems, 'myFilter': myFilter}
     return render(request, 'store/store.html', context)


def cart(request):
     Data = cookieCart(request)
     items = Data['items']
     order = Data['order']
     cartItems = Data['cartItems']

     context = {'items':items, 'order':order, 'cartItems':cartItems}
     return render(request, 'store/cart.html', context)

def checkout(request):
      Data = cookieCart(request)
      items = Data['items']
      order = Data['order']
      cartItems = Data['cartItems']

      context = {'items':items, 'order':order, 'cartItems':cartItems}
      return render(request, 'store/checkout.html', context)

def aboutus(request):
      context = {}
      return render(request, 'store/aboutus.html', context)

def contactus(request):
      context = {}
      return render(request, 'store/contactus.html', context)

def updateItem(request):
      data = json.loads(request.body)
      productId = data['productId']
      action = data['action']
      print('Action:', action)
      print('Product:',productId)

      customer = request.user.customer
      product = Product.objects.get(id = productId)
      order, created = Order.objects.get_or_create(coustomer = customer, complete = False)

      orderItem, created = OrdeItem.objects.get_or_create(order = order, product = product)
      
      if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
      elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)
      
      orderItem.save()

      if orderItem.quantity <= 0:
            orderItem.delete()

      return JsonResponse('Item was added', safe=False)


def processOrder(request):
      print('Data:', request.body)
      transaction_id = datetime.datetime.now().timestamp()
      data = json.loads(request.body)

      if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(coustomer = customer, complete = False)
            
            # total = float(data['form']['total'])
            # order.transaction_id = transaction_id

            # if total == float(order.get_cart_total()):
            #       order.complete = True
            # order.save()

            

      else:
            customer, order = guestOrder(request, data)


      total = float(data['form']['total'])
      order.transaction_id = transaction_id

      if total == float(order.get_cart_total()):
            order.complete = True
      order.save()

      if order.shipping == True:
            ShippingAddress.objects.create(
                  coustomer = customer,
                  Order = order,
                  address = data['shipping']['address'],
                  city = data['shipping']['city'],
                  state = data['shipping']['state'],
                  zipcode = data['shipping']['zipcode'],
            )

      return JsonResponse('Payment submitted...', safe = False)





#      if request.user.is_aunthenticated:
#          customer = request.user.customer
#            order, created = Order.objects.get_or_create(customer = customer, complete = False)
#            items = order.ordeitem_set.all()
#       else

# checkout-post
# order = {'get_cart_total':0, 'get_cart_item':0, 'shipping':False}
            # items = []
            # cartItems = order['get_cart_item']


      # store-post
      #      items = []
      #      order = {'get_cart_total':0, 'get_cart_item':0, 'shipping':False}
      #      cartItems = order['get_cart_item']