# django-winedelivery

Wine Delivery Service のサンプルコードです。 以前、依頼を受けた受発注アプリケーション制作における要件定義を基に、簡単なシステムを作成してみました。

以下のコードで実行可能です。（Windows用）
``` python
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
manage.py migrate
manage.py createsuperuser 
manage.py runserver
```