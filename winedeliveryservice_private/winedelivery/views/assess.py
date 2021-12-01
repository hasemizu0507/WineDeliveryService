# [ REWRITE ]  ファイル追加

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from winedelivery.scripts.predict_price import PredictPrice

from winedelivery.models import RentRoom

def form_view(request): # フォームを表示
    return render(request, 'winedelivery/templates/winedelivery/assessment_form.html')  #　変更

def result_view(request): # フォームの入力をAPIに伝達、リターン値を用いてテンプレートに表示
    var = request.GET
    predict_price = PredictPrice()
    station = float(var.get("station"))
    area = float(var.get("area"))
    year = float(var.get("year"))
    predict_price.load_model("winedelivery/scripts/price_model.sav") # 変更
    result = predict_price.predict(dist_to_nearest_station =station, area =area, year_pp =year)

    return render(request, 'winedelivery/templates/winedelivery/assessment_result.html', {"station":station, "area":area, "year":year, 'result':int(result*area)}) # 変更

def submit_view(request): # [ REWRITE 3 ] 追記
    # フォーム入力の読みとり
    var = request.POST
    print(var)
    predict_price = PredictPrice()
    station = float(var.get("station"))
    area = float(var.get("area"))
    year = float(var.get("year"))

    # 査定済みだろうが、クライエント側からの捏造要請を防止するため, もう一度査定を行う
    # 査定結果が時間差で変わる可能性はないか？
    predict_price.load_model("winedelivery/scripts/price_model.sav") # 変更
    kakaku = predict_price.predict(dist_to_nearest_station =station, area =area, year_pp =year)

    new_room = RentRoom()
    
    # ルームIDをインクリメンタルで設定する
    try:
        max_id = RentRoom.objects.latest('id').id
    except ObjectDoesNotExist:
        max_id = 'A00000'
    room_id = 'A'+(str(int(max_id[1:])+1).zfill(5))

    new_room.id              = room_id
    new_room.owner_id        = request.user.profile.id
    new_room.pref_name       = request.POST["pref_name"]
    new_room.city_name       = request.POST["city_name"]
    new_room.district_name   = request.POST["district_name"]
    new_room.built_year      = year
    new_room.structure       = request.POST["structure"]
    new_room.top_floor_num   = int(request.POST["top_floor_num"])
    new_room.room_type       = request.POST["room_type"]
    new_room.price           = kakaku/area
    new_room.area            = area
    new_room.latitude        = 0 # 良さそうなAPIががあれば
    new_room.longitude       = 0
    new_room.is_active       = False
    new_room.nearest_station = request.POST["nearest_station"]
    new_room.dist_to_nearest_station = station
    new_room.save() # 物件をRentRoomテーブルに保存

    # 本来ならばhtmlテンプレートを作ってきちんとしたページを表示するべきだが、簡略化のためにHttpResponseで書きました
    return HttpResponse(
        """<h1>ご登録ありがとうございます。</h1>
        <p>登録内容を確認するには、マイページにアクセスして下さい。<br>
        サイト管理者が承認を許可すると、<a href="/winedelivery/rentroom">RentRoom一覧</a>から提出いただいた物件を確認できます。</p>"""
        )



def apply_view(request, rentroom_id):
    rentroom = get_object_or_404(RentRoom, id=rentroom_id) 
    rentroom.is_active = True # 物件の承認フラグをTrueにして（承認済みにして）
    rentroom.save() # データベースに保存！
    return HttpResponse("<h1>物件{}を有効にしました。Rentroom一覧ページ等でご確認下さい。".format(rentroom_id))