
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from winedelivery.models import Restaurant

# class RegisterForm(UserCreationForm):
#     age = forms.IntegerField(required=True)
#     gender = forms.ChoiceField(choices=GENDER_LIST, required=True)
#     household_num = forms.IntegerField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'password1', 'password2','age','gender','household_num']
#         labels = {
#             'username': 'ユーザー名',
#             'password1': 'パスワード',
#             'password2': 'パスワード確認',
#             'age': '年齢',
#             'gender': '性別',
#             'household_num': '世帯人数',
#         }

#     def save(self, commit=True):
#         if not commit:
#             raise NotImplementedError('Cannot create User and Profile without database save')
        
#         user = super().save()

#         try:
#             max_id = Profile.objects.latest('id').id
#         except ObjectDoesNotExist:
#             max_id = 'B00000'

#         prof_id = 'B'+(str(int(max_id[1:])+1).zfill(5))

#         age = self.cleaned_data['age']
#         gender = self.cleaned_data['gender']
#         household_num = self.cleaned_data['household_num']

#         profile = Profile(id=prof_id,age=age,gender=gender,household_num=household_num,user_id=user.id)
#         profile.save()

#         return user

class RegisterForm(UserCreationForm):

    pref_name = forms.CharField(required=True)
    city_name = forms.CharField(required=True)
    district_name = forms.CharField(required=True)
    name = forms.CharField(required=True)
    appearance = forms.ImageField(required=False)
    phone_number = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2','pref_name','city_name','district_name', 'name', 'appearance', 'phone_number']
        labels = {
            'username': 'ユーザー名',
            'password1': 'パスワード',
            'password2': 'パスワード確認',
            'pref_name': '都道府県',
            'city_name': '市区',
            'district_name': '町村', 
            'name': 'レストラン名', 
            'appearance': '店舗写真', 
            'phone_number': '電話番号'
        }

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError('Cannot create User and Restaurant without database save')
        
        user = super().save()

        try:
            max_id = Restaurant.objects.latest('id').id
        except ObjectDoesNotExist:
            max_id = 'A00000'

        restaurant_id = 'A'+(str(int(max_id[1:])+1).zfill(5))

        pref_name = self.cleaned_data['pref_name']
        city_name = self.cleaned_data['city_name']
        district_name = self.cleaned_data['district_name']
        name = self.cleaned_data['name']
        appearance = self.cleaned_data['appearance']
        phone_number = self.cleaned_data['phone_number']

        restaurant = Restaurant(id=restaurant_id,pref_name=pref_name,city_name=city_name,district_name=district_name,name=name,appearance=appearance,phone_number=phone_number,user_id=user.id)
        restaurant.save()

        return user


