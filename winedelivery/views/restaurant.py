from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from winedelivery.models import Restaurant, Wine, Cart 
from django.core.paginator import Paginator
from django.contrib.auth.models import User #User追加

import random


def list_view(request):
    restaurant_list = Restaurant.objects.all().order_by('id')
    paginator = Paginator(restaurant_list, 20) # ページ当たり20個表示

    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    restaurants = paginator.get_page(page)
    return render(request, 'order/restaurant_list.html', {'restaurants': restaurants, 'page': page, 'last_page': paginator.num_pages})

def detail_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    try:
        page = int(request.GET.get('from_page'))
    except:
        page = 1
    return render(request, 'order/restaurant_detail.html', {'restaurant': restaurant, 'page': page})