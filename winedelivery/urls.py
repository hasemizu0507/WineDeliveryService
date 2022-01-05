from django.urls import path
from winedelivery.views import mypage, wine, order, restaurant

app_name = 'winedelivery'

urlpatterns = [
    # ---------顧客側--------- #
    path('wine/', wine.list_view, name='wine_list'),
    path('wine/<slug:wine_id>', wine.detail_view, name='wine_detail'),

    path('mypage/', mypage.mypage_top, name='mypage_top'),
    path('edit_cart/<slug:wine_id>', wine.edit_cart, name='edit_cart'),

    path('cart_check/', wine.cart_check, name='cart_check'),

    path('checkout/', mypage.checkout, name='checkout'),
    path('success/', mypage.success, name='success'),
    path('cancel/', mypage.cancel, name='cancel'),
    path('create_checkout_session/', mypage.create_checkout_session, name='checkout_session'),
    # ---------顧客側ここまで--------- #


    # ---------業者側--------- #
    path('order/', order.list_view, name='order'),
    path('order/detail/', order.detail_view, name='order_detail'),

    path('restaurant_list/', restaurant.list_view, name='restaurant_list'),
    path('retaurant_list/<slug:restaurant_id>', restaurant.detail_view, name='restaurant_detail'),

    path('update', wine.update, name='update'),
    path('update/stocking', wine.stocking, name='stocking'),
    # ---------業者側ここまで--------- #
    ]