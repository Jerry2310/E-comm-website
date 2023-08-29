import json
from .models import *


def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
            cart = {}
        
    print('cart = ',cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_item':0, 'shipping':False}
    cartItems = order['get_cart_item']

    for i in cart:
            try:
                cartItems += cart[i]['quantity']
                product = Product.objects.get(id = i)
                total =(product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_item'] += cart[i]['quantity']

                item = {
                    'product':{
                                   'id':product.id,
                                   'name':product.name,
                                   'price':product.price,
                                   'imageURL':product.imageURL,
                              },
                              'quantity':cart[i]['quantity'],
                              'get_total':total,
                       }
                items.append(item)

                if product.digital == False:
                             order['shipping'] = True
            except:
                       pass

    return {'items':items, 'order':order, 'cartItems':cartItems}


def cartData(request):
       if request.user.is_authenticated:
           customer = request.user.customer
           order, created = Order.objects.get_or_create(coustomer=customer, complete = False)
           items = order.ordeitem_set.all()
           cartItems = order.get_cart_item
       else:
           cookieData = cookieCart(request)
           items = cookieData['items']
           order = cookieData['order']
           cartItems = cookieData['cartItems']
       return {'items':items, 'order':order, 'cartItems':cartItems}

def guestOrder(request,data):
       print('User not logged in....')

       print('COOKIES :', request.COOKIES)
       name = data['form']['name']
       email = data['form']['email']

       cookieData = cookieCart(request)
       items = cookieData['items']

       customer, created = Customer.objects.get_or_create(
            email = email,
       )
       customer.name = name
       customer.save()

       order = Order.objects.create(
            coustomer = customer,
            complete = False
       )

       for item in items:
            product = Product.objects.get(id = item['product']['id'])

            orderItem = OrdeItem.objects.create(
                    product = product,
                    order = order,
                    quantity = item['quantity']
            )
       return customer, order