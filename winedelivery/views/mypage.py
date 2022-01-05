from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import json
from winedelivery.models import Wine, Cart, Wine

# 以下5つ追加（決済用）
from django.conf import settings
import json
import stripe
from django.urls import reverse
from django.db.models import Sum


@login_required
def mypage_top(request):
    user = request.user
    restaurant_id = user.restaurant.id
    # mywines = Wine.objects.filter(owner_id=profile.id)
    # assessments  = Wine.objects.filter(owner_id=profile.id, is_active=False) # [ REWRITE 3 ]追加

    # ユーザーIDがログイン中しているユーザのIDになっているproductsを取り出す。
    products = Cart.objects.filter(restaurant_id=restaurant_id)
    return render(request, 'wine/mypage.html', {'products':products})#, 'wines':mywines, "assessments":assessments}) 

# 決済成功時の関数
def success(request):
    # テンプレートを表示するだけ
    return render(request, 'wine/success.html') 

# 決済中止時の関数
def cancel(request):
    # テンプレートを表示するだけ
    return render(request, 'wine/cancel.html') 

# 決済内容確認時の関数
def checkout(request):
    # settings.pyから読み込んだ公開鍵をjson形式にしてテンプレートcheckout.htmlに渡す
    key_data = {
        "publishable_key":settings.STRIPE_PUBLISHABLE_KEY,
    }

    price_total = 0
    cart_wines = []
    user = request.user
    restaurant_id = user.restaurant.id
    user_id = user.id
    # wine_idと発注数でリストを作る
    product = Cart.objects.filter(restaurant_id=restaurant_id)
    product_id = product.values_list('wine_id', flat=True)
    product_num = product.values_list('num', flat=True)
    # object.filter(id = id) object.filter(id__in = [1, 2, 3])のように = のあとがリストの場合__inをつける
    for (wine_id, num) in zip(product_id, product_num):
        #[wine.name, wine.price, num],[wine.name, wine.price, num],[wine.name, wine.price, num]]のようなリストを作っている
        wine = Wine.objects.get(id = wine_id)
        cart_wines.append([wine.name, wine.price, num])
        price_total +=  wine.price * int(num)
    # price_total = round(price_total)
    return render(request, 'wine/checkout.html', {'data_json':json.dumps(key_data), "cart_wines":cart_wines, "price":price_total, "user_id":user_id})

# 「この商品を購入」ボタンが押された時の関数
def create_checkout_session(request):
    # settings.pyから秘密鍵を読み込む
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user = request.user
    user_id = user.id
    user_name = user.username
    # ユーザーIDがログインしているユーザのIDになっているproductsを取り出す。
    product_id = Cart.objects.filter(restaurant_id=user_id).values_list('wine_id', flat=True)
    products = Wine.objects.filter(id__in=product_id).values('id', 'name','price')
    price_total = Wine.objects.filter(id__in=product_id).aggregate(Sum('price'))['price__sum']
    num = Cart.objects.filter(wine_id__in=product_id).aggregate(Sum('num'))['num__sum']

    try:
        checkout_session = stripe.checkout.Session.create(
            # カード決済
            payment_method_types=['card'],
            # 決済内容を記述
            line_items=[
                {
                    'price_data': {
                        # 通貨（円）
                        'currency': 'jpy',
                        # 金額
                        'unit_amount': price_total,
                        # 商品説明・画像
                        'product_data': {
                            'name': user_name + '様',
                            'images': ['http://gahag.net/img/201606/12s/gahag-0095672681-1.jpg'],
                            # 'images': ['http://gahag.net/img/201606/12s/gahag-0095672681-1.jpg'],
                        },
                    },
                    # 個数
                    'quantity': num,
                },
            ],
           mode='payment',
           # 成功すれば"success"へ
           success_url=request.build_absolute_uri(reverse('winedelivery:success')),
           # 中止すれば"cancel"へ
           cancel_url=request.build_absolute_uri(reverse('winedelivery:cancel')),
       )

        print(checkout_session.id)
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error':str(e)})