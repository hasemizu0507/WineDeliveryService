'''
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import json
from winedelivery.models import RentRoom, Cart, Profile

@login_required
def mypage_top(request):
    user = request.user
    profile = user.profile
    user_id = user.id
    myrooms = RentRoom.objects.filter(owner_id=profile.id)
    assessments  = RentRoom.objects.filter(owner_id=profile.id, is_active=False) # [ REWRITE 3 ]追加

    # ユーザーIDがログイン中しているユーザのIDになっているproductsを取り出す。
    products = Cart.objects.filter(user_id=user_id)
    return render(request, 'winedelivery/mypage.html', {'profile':profile,'rooms':myrooms, 'products':products, "assessments":assessments}) #'assessments':myassessments
'''
'''
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import json
from winedelivery.models import RentRoom, Cart, Profile

# 以下4つ追加（決済用）
from django.conf import settings
import json
import stripe
from django.urls import reverse


@login_required
def mypage_top(request):
    user = request.user
    profile = user.profile
    user_id = user.id
    myrooms = RentRoom.objects.filter(owner_id=profile.id)
    assessments  = RentRoom.objects.filter(owner_id=profile.id, is_active=False) # [ REWRITE 3 ]追加

    # ユーザーIDがログイン中しているユーザのIDになっているproductsを取り出す。
    products = Cart.objects.filter(user_id=user_id)
    return render(request, 'winedelivery/mypage.html', {'profile':profile,'rooms':myrooms, 'products':products, "assessments":assessments}) #'assessments':myassessments


# 決済成功時の関数
def success(request):
    # テンプレートを表示するだけ
    return render(request, 'winedelivery/success.html') 

# 決済中止時の関数
def cancel(request):
    # テンプレートを表示するだけ
    return render(request, 'winedelivery/cancel.html') 

# 決済内容確認時の関数
def checkout(request):
    # settings.pyから読み込んだ公開鍵をjson形式にしてテンプレートcheckout.htmlに渡す
    key_data = {
        "publishable_key":settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'winedelivery/checkout.html', {'data_json':json.dumps(key_data)})
# 「この商品を購入」ボタンが押された時の関数
def create_checkout_session(request):
    # settings.pyから秘密鍵を読み込む
   stripe.api_key = settings.STRIPE_SECRET_KEY

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
                       'unit_amount': 2000,
                       # 商品説明・画像
                       'product_data': {
                           'name': 'sample house',
                           'images': ['http://gahag.net/img/201606/12s/gahag-0095672681-1.jpg'],
                       },
                   },
                   # 個数
                   'quantity': 1,
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
'''

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import json
from winedelivery.models import RentRoom, Cart, Profile

# 以下5つ追加（決済用）
from django.conf import settings
import json
import stripe
from django.urls import reverse
from django.db.models import Sum


@login_required
def mypage_top(request):
    user = request.user
    profile = user.profile
    user_id = user.id
    myrooms = RentRoom.objects.filter(owner_id=profile.id)
    assessments  = RentRoom.objects.filter(owner_id=profile.id, is_active=False) # [ REWRITE 3 ]追加

    # ユーザーIDがログイン中しているユーザのIDになっているproductsを取り出す。
    products = Cart.objects.filter(user_id=user_id)
    return render(request, 'winedelivery/mypage.html', {'profile':profile,'rooms':myrooms, 'products':products, "assessments":assessments}) 

    # 決済成功時の関数
def success(request):
    # テンプレートを表示するだけ
    return render(request, 'winedelivery/success.html') 

# 決済中止時の関数
def cancel(request):
    # テンプレートを表示するだけ
    return render(request, 'winedelivery/cancel.html') 
def checkout(request):
    # settings.pyから読み込んだ公開鍵をjson形式にしてテンプレートcheckout.htmlに渡す
    key_data = {
        "publishable_key":settings.STRIPE_PUBLISHABLE_KEY,
    }

    user = request.user
    user_id = user.id
    user_name = user.username
    # ユーザーIDがログイン中しているユーザのIDになっているproductsを取り出す。
    product_id = Cart.objects.filter(user_id=user_id).values_list('product_id', flat=True)
    products = RentRoom.objects.filter(id__in=product_id).values('id', 'room_type','price')
    price_total = RentRoom.objects.filter(id__in=product_id).aggregate(Sum('price'))['price__sum']
    price_total = round(price_total)
    
    return render(request, 'winedelivery/checkout.html', {'data_json':json.dumps(key_data), "products":products, "price":price_total, "user_id":user_name})


# 「この商品を購入」ボタンが押された時の関数
def create_checkout_session(request):
    # settings.pyから秘密鍵を読み込む
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user = request.user
    user_id = user.id
    user_name = user.username
    # ユーザーIDがログイン中しているユーザのIDになっているproductsを取り出す。
    product_id = Cart.objects.filter(user_id=user_id).values_list('product_id', flat=True)
    products = RentRoom.objects.filter(id__in=product_id).values('id', 'room_type','price')
    price_total = RentRoom.objects.filter(id__in=product_id).aggregate(Sum('price'))['price__sum']
    price_total = round(price_total)
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
                        },
                    },
                    # 個数
                    'quantity': 1,
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