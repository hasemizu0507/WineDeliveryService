from django.contrib import admin 

# モデルをインポート 
from .models import History, Cart, Restaurant, Wine

# 管理サイトへのモデルの登録 
admin.site.register(Restaurant) 
admin.site.register(Wine) 
admin.site.register(Cart) 
admin.site.register(History)
