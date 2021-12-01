from django.urls import path
from . import views 
from iekari.views import rentroom, mypage, recommend, assess 

app_name = 'iekari'


urlpatterns = [ 
    path('rentroom', rentroom.list_view, name='rentroom_list'),
    path('rentroom/<slug:rentroom_id>', rentroom.detail_view, name='rentroom_detail'),
    
    path('recommend', recommend.form_view, name='recommend_form'),
    path('recommend/result', recommend.result_view, name='recommend_result'), 

    path('assess', assess.form_view, name='assess_form'), 
    path('assess/result', assess.result_view, name='assess_result'), 
 
    path('assess/submit', assess.submit_view, name='assess_submit'), # [ REWRITE 3 ]追加
    path('assess/apply/<slug:rentroom_id>', assess.apply_view, name='assess_apply'), # [ REWRITE 3 ]追加

    path('mypage', mypage.mypage_top, name='mypage_top'),
    path('edit_cart/<slug:rentroom_id>', rentroom.edit_cart, name='edit_cart'), #追加

    # 追加
    path('checkout/', mypage.checkout, name='checkout'),
    path('success/', mypage.success, name='success'),
    path('cancel/', mypage.cancel, name='cancel'),
    path('create_checkout_session/', mypage.create_checkout_session, name='checkout_session'),
]




