# django-winedelivery

Wine Delivery Service のサンプルコードです。 以前に開発依頼を受けた受発注アプリケーション制作における要件定義を基に、簡単なシステムを作成してみました。

以下のコードで実行可能です。（Windows用）
``` python
python -m venv env_django
. env_django/Scripts/activate
cd ./hasemizu0507.github.io
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser 
python manage.py runserver
```
→デフォルトアドレス（http://127.0.0.1:8000/）にアクセス

CSVファイル内のデータをインポートする場合は、以下のコードで実行可能です。（Windows用）
``` 
python manage.py dbshell
sqlite> .mode csv
sqlite> .separator ,

sqlite> .import ./data/Restaurant.csv temp_restaurant
sqlite> INSERT INTO winedelivery_restaurant (id,pref_name,city_name,district_name,name,appearance,phone_number) SELECT id,pref_name,city_name,district_name,name,appearance,phone_number FROM temp_restaurant WHERE 1;

sqlite> .import ./data/Wine.csv temp_wine
sqlite> INSERT INTO winedelivery_wine (id,name,kind,origin,type,year,price,stock) SELECT id,name,kind,origin,type,year,price,stock FROM temp_wine WHERE 1;
```