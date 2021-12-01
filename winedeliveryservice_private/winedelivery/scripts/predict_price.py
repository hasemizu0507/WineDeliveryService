# [ REWRITE 2 ] ファイル追加

import numpy as np
import pandas as pd
import pickle

from sklearn.metrics import mean_squared_error
from sklearn import linear_model

class PredictPrice:
    def __init__(self):
        self.clf = None
        self.x_train = None
        self.Y_train = None

    def load_model(self, fpath):
      self.clf = pickle.load(open(fpath, 'rb'))

    def predict(self, dist_to_nearest_station = 0, area = 0, year_pp = 0):
        df = pd.DataFrame([{'dist_to_nearest_station':dist_to_nearest_station, 'area':area, 'year_pp':year_pp }])
        return self.clf.predict(df)[0][0]


    # -----------------------------------   学習用(Djangoでは使用しない)  ------------------------------------------------
    def load_test_data(self, path):
        self.data_all = pd.read_csv(path)# CSVファイルを読み込む
        # 読み込んだデータをトレーニングデータとテストデータに分割
        # トレーニングデータ : モデルを作成するためのデータ
        # テストデータ      : モデルの精度を評価するためにとっておくデータ
        self.Y_train = self.data_all[['price']] # 予測するものは価格（price)なので、価格データのみを取り出してY（最終的にはself.Y_train, self.y_test)に代入する
        self.X_train = self.data_all.drop(['id', 'pref_name', 'city_name', 'district_name', 'built_year', 'structure', 'price', 'top_floor_num', 'room_type', 'nearest_station_id'], axis=1)
        self.X_train = self.X_train.drop(['latitude','longitude'], axis=1) # 学習に不要な値を削除（drop)する
        self.X_train['year_pp'] = 2021 - self.data_all['built_year'] # 新しく’year_pp’のデータ列を追加

    def learn(self):
        #モデルの枠組みを設定
        self.clf = linear_model.LinearRegression()
        # clsにあわせ型を変換
        X_train = self.X_train.values
        Y_train = self.Y_train.values

        # 予測モデルを作成
        self.clf.fit(X_train, Y_train)

        print(self.clf.coef_)# 回帰係数
        print(self.clf.intercept_)# 切片 (誤差)

    def check_res(self):
        pred_train = self.clf.predict(self.X_train)
        print(np.sqrt(mean_squared_error(self.Y_train, pred_train)))

    def save_model(self, fpath):
        pickle.dump(self.clf, open(fpath, 'wb'))


if __name__ == "__main__":
    predict_price = PredictPrice()
    predict_price.load_test_data("PLEASE_INPUT_YOUR_PATH/RentRoom.csv")
    predict_price.learn()
    predict_price.check_res()
    predict_price.save_model("price_model.sav")

    predict_price.clf = None
    predict_price.load_model("price_model.sav")
    predict_price.predict(dist_to_nearest_station = 1000, area = 30, year_pp = 5)
