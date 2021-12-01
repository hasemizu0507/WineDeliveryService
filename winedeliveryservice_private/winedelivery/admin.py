from django.contrib import admin 

# モデルをインポート 
from .models import Profile, RentRoom, Cart

# 管理サイトへのモデルの登録 
admin.site.register(Profile) 
admin.site.register(RentRoom) 
admin.site.register(Cart) 
