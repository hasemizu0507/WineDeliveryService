from django.contrib.auth.models import User 
from django.db import models
from django.db.models.fields import IntegerField 

# GENDER_LIST = ( (0, '男性'), (1, '女性') )
# dict_gender_list = {0:'男性',1:'女性'}

#デフォルトであるdjango.dbのmodelsを継承して作成する
# class Profile(models.Model):
    
#     #django仕様のメタクラス(クラス自体の設定を記述)(管理画面での表示内容を設定)
#     class Meta:
#         verbose_name = 'ユーザー情報データ'
#         verbose_name_plural = 'ユーザー情報データ'
#     #ユーザーの設定。下記のフィールドとの紐づけはビューで行う
#     user = models.OneToOneField(User, verbose_name='ユーザー',null=True, blank=True, on_delete=models.CASCADE)

#     #フィールドの設定。コード１行がフィールド１列に対応する。
#     id = models.CharField(max_length=6,primary_key=True)
#     age = models.IntegerField('年齢')
#     gender = models.IntegerField('性別',choices=GENDER_LIST)
#     household_num = models.IntegerField('世帯人数')
    
#     #管理画面で表示される文字列を定義する
#     def __str__(self):
        
#         user_str = ''
#         if self.user is not None:
#             user_str = '(' + self.user.username + ')'

#         return self.id+' '+str(self.age)+'歳 ' \
#             +dict_gender_list.get(self.gender)+' ' \
#             +str(self.household_num)+'人世帯 ' 

class Restaurant(models.Model):
    
    #django仕様のメタクラス(クラス自体の設定を記述)(管理画面での表示内容を設定)
    class Meta:
        verbose_name = 'ユーザー情報データ'
        verbose_name_plural = 'ユーザー情報データ'
    #ユーザーの設定。下記のフィールドとの紐づけはビューで行う
    user = models.OneToOneField(User, verbose_name='ユーザー',null=True, blank=True, on_delete=models.CASCADE)

    #フィールドの設定。コード１行がフィールド１列に対応する。
    id = models.CharField(max_length=6,primary_key=True)
    name = models.CharField('レストラン名', max_length=20)
    pref_name = models.CharField('都道府県',max_length=20)      # '東京都'
    city_name = models.CharField('市区',max_length=50)      # '世田谷区'
    district_name = models.CharField('町村',max_length=50)    # '喜多見７丁目'
    phone_number = models.CharField('電話番号',max_length=18)    # '11112222'
    appearance = models.ImageField('店舗写真', upload_to='media', null=True, blank=True) # 'appearance'に変更
    
    #管理画面で表示される文字列を定義する
    def __str__(self):
        
        user_str = ''
        if self.user is not None:
            user_str = '(' + self.user.username + ')'

        return self.id+' '+str(self.name)+' ' \
            +str(self.pref_name)+' ' \
            +str(self.city_name)+' ' \
            +str(self.district_name)+' '\
            +str(self.phone_number)+' ' \
            +str(self.appearance)

class Wine(models.Model):

    #django仕様のメタクラス(クラス自体の設定を記述)(管理画面での表示内容を設定)
    class Meta:
        verbose_name = 'ワインの情報'
        verbose_name_plural = 'ワイン情報'

    #フィールドの設定。コード１行がフィールド１列に対応する。
    id = models.CharField(max_length=6,primary_key=True) # 'B00001'
    name = models.CharField('ワイン名', max_length=30) # '小樽のワイン'
    kind = models.CharField('タイプ', max_length=20) # '赤', '白', '泡'
    origin = models.CharField('産地', max_length=30) # '小樽'
    type = models.CharField('品種', max_length=30) # 'カルベネ・ソーヴィニョン'
    year = models.IntegerField('収穫年') # '1990'
    price = models.IntegerField('価格') # '3000'
    stock = models.IntegerField('在庫') # '5'
    def __str__(self):
        return self.id

class Cart(models.Model):
    
    # django仕様のメタクラス(クラス自体の設定を記述)(管理画面での表示内容を設定)
    class Meta:
        verbose_name = 'カート情報'
        verbose_name_plural = 'カート情報'
    # レストランID
    restaurant_id = models.CharField('レストランID', max_length=6)
    # ワインID
    wine_id = models.CharField('ワインID', max_length=6)
    # 本数
    num = IntegerField('本数')
    # 追加時刻
    timestamp = models.DateTimeField('追加日時', auto_now_add=True)
    # 管理画面で表示される文字列を定義する
    def __str__(self):
        return self.restaurant_id + ' ' \
            + self.wine_id +' ' \
            + self.num + ' ' \
            + str(self.timestamp)

class History(models.Model):

    # django仕様のメタクラス(クラス自体の設定を記述)(管理画面での表示内容を設定)
    class Meta:
        verbose_name = '発注履歴情報'
        verbose_name_plural = '発注履歴情報'
    # レストランID
    restaurant_id = models.CharField('レストランID', max_length=6)
    # ワインID
    wine_id = models.CharField('ワインID', max_length=6)
    # 本数
    num = IntegerField('本数')
    # 追加時刻
    timestamp = models.DateTimeField('追加日時', auto_now_add=True)
    # 管理画面で表示される文字列を定義する
    def __str__(self):
        return self.restaurant_id + ' ' \
            + self.wine_id +' ' \
            + self.num + ' ' \
            + str(self.timestamp)