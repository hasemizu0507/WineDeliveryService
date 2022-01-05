from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from winedelivery.models import  Wine, Cart
from django.core.paginator import Paginator
from django.contrib.auth.models import User #User追加

import random


def list_view(request):

    # 変更予定（モデルから呼び出す予定）
    order_list = [
        {'name': 'MizukiHasegawa', 'timestamp' : '2021/12/13'}
        ]
    
    return render(request, 'order/order_list.html', {'order_list': order_list})

def detail_view(request):

    # 変更予定（モデルから呼び出す予定）
    detail_list = [
        {'name': 'MizukiHasegawa', 'timestamp' : '2021/12/13', 'email' : 'hasemizu0507@ezweb.ne.jp', 'wine_id' : 'B0001', 'wine_name' : 'おたるワイン', 'price' : '3000', 'num' : '10'}
        ]
        
    return render(request, 'order/order_detail.html', {'detail_list': detail_list})