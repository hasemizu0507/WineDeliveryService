from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from winedelivery.models import Wine, Cart 
from django.core.paginator import Paginator
from django.contrib.auth.models import User #User追加

import random


def list_view(request):
    wine_list = Wine.objects.all().order_by('id')
    paginator = Paginator(wine_list, 20) # ページ当たり20個表示

    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    wines = paginator.get_page(page)
    return render(request, 'wine/wine_list.html', {'wines': wines, 'page': page, 'last_page': paginator.num_pages})

def detail_view(request, wine_id):
    wine = get_object_or_404(Wine, id=wine_id)

    try:
        page = int(request.GET.get('from_page'))
    except:
        page = 1
    return render(request, 'wine/wine_detail.html', {'wine': wine, 'page': page})

def edit_cart(request, wine_id):
    #表示しているページのワインを取得
    wine = get_object_or_404(Wine, id=wine_id)
    #ログインしているユーザのIDを取得
    user = request.user
    restaurant_id = user.restaurant.id

    message = False

    #遷移前の一覧ページを取得
    try:
        page = int(request.GET.get('from_page'))
    except:
        page = 1

    if (request.method == 'POST'):
        num = request.POST.get("num")
        if ( num != 0 and num):
            try:
                previous_cart = Cart.objects.get(restaurant_id=restaurant_id, wine_id=wine_id)
                print(previous_cart.num)
                previous_cart.num += int(num)
                previous_cart.save()
            except :
                product = Cart(restaurant_id=restaurant_id, wine_id=wine_id, num = num)
                print("aaaaa")
                product.save()
            message = True
    return render(request, 'wine/wine_detail.html', {'wine': wine, 'page': page, 'message': message })

def cart_check(request):
    user = request.user
    restaurant = user.restaurant

    cart_wines = []

    # ユーザーIDがログインしているユーザのIDになっているproductsを取り出す。
    products = Cart.objects.filter(restaurant_id=restaurant.id)
    product_id = products.values_list('wine_id', flat=True)
    product_num = products.values_list('num', flat=True)
    # object.filter(id = id) object.filter(id__in = [1, 2, 3])のように = のあとがリストの場合__inをつける
    for (wine_id, num) in zip(product_id, product_num):
        wine = Wine.objects.get(id = wine_id)
        cart_wines.append([wine.name, wine.price, num])
    return render(request, 'wine/cart_check.html', {'products':products, "cart_wines":cart_wines})

def update(request):
    wines = Wine.objects.all().order_by('-id')
    cart_list = Cart.objects.all().order_by('-id') 
    return render(request, 'wine/update.html', {'wines': wines, 'cart_list': cart_list})   


def stocking(request):
    wines = Wine.objects.all().order_by('-id')
    cart_list = Cart.objects.all().order_by('-id') 

    stocking = request.POST.getlist('stocking') 
    stocking = [i if i  else 0 for i in stocking]

    for (wine, stock) in zip(wines, stocking):
        wine.stock += int(stock)
        wine.save()
    return render(request, 'wine/update.html', {'wines': wines, 'cart_list': cart_list})