import numpy as np
import pandas as pd
import os


class Factors:
    def __init__(self, path):
        self.path = path

    @property
    def f_series(self) -> pd.DataFrame:
        '''

        :return:
        '''
        df = pd.Series(pd.read_feather(self.path).iloc[:, 2])
        df.name = str(os.path.split(self.path)[1])
        return df

    @property
    def f_ndarray(self) -> np.ndarray:
        '''

        :return:
        '''
        df = pd.read_feather(self.path)
        df[['date']] = df[['date']].astype(int)
        df.sort_values(by=["stockcode", "date"], inplace=True)
        n = df.iloc[:, :2].nunique()
        if n[0] * n[1] != len(df):
            print('因子值不完整，部分股票或交易日可能有缺值，无法将其reshape为三维矩阵')
            return AttributeError
        else:
            arr = np.array(df)
            # arr = np.array(df).reshape(n[1], -1, 3)
            res = []
            for i in range(n[0] - 1):
                r = arr[59 * i:59 * (i + 1), :]
                res.append(r)
            res = np.stack(res)
            return res

    def get_F_stocklist(self, review=True) -> list:
        '''

        :param review:
        :return:
        '''
        df = pd.read_feather(self.path)
        list = df['stockcode'].drop_duplicates()
        if review:
            print("因子覆盖" + str(len(list)) + '只股票，清单如下：')
            print(list)
        else:
            pass
        return list.tolist()

    def get_F_date(self, review=True) -> list:
        '''

        :param review:
        :return:
        '''
        df = pd.read_feather(self.path)
        df[['date']] = df[['date']].astype(int)
        list = df['date'].drop_duplicates()
        if review:
            print("因子覆盖" + str(len(list)) + '个交易日，清单如下：')
            print(list)
        else:
            pass
        return list.tolist()

    def quary_F_bystock(self, stockcode: str = None) -> pd.DataFrame:
        '''

        :param stockcode:
        :return:
        '''
        if stockcode == None:
            print("请输入一个stockcode")
            return AttributeError
        else:
            df = pd.read_feather(self.path)
            df[['date']] = df[['date']].astype(int)
            df.sort_values(by=["stockcode", "date"], inplace=True)
            return df[df["stockcode"].isin([stockcode])]

    def quary_F_bydate(self, date: int = None) -> pd.DataFrame:
        '''

        :param date:
        :return:
        '''
        if date == None:
            print("请输入一个date")
            return AttributeError
        else:
            df = pd.read_feather(self.path)
            df[['date']] = df[['date']].astype(int)
            df.sort_values(by=["date", "stockcode"], inplace=True)
            return df[df["date"].isin([date])]


class Factor_board():
    def __init__(self, LSTM_path=None, GRU_path=None, TCN_path=None, CNN_path=None, TRANS_path=None, HAN_path=None):
        self.show_num = 5
        self.export_json = False
        self.LSTM_path = LSTM_path
        self.GRU_path = GRU_path
        self.TCN_path = TCN_path
        self.CNN_path = CNN_path
        self.TRANS_path = TRANS_path
        self.HAN_path = HAN_path

    @property
    def JSON(self) -> pd.DataFrame:
        '''

        :return:
        '''
        pathlist = [self.LSTM_path, self.GRU_path, self.TCN_path, self.CNN_path, self.TRANS_path, self.HAN_path]
        First = True
        json = pd.DataFrame()
        lastdata = Factors(pathlist[-1]).get_F_date(review=False)[-1]
        for p in pathlist:
            df = Factors(p).quary_F_bydate(date=int(lastdata)).drop('date', axis=1)
            result = pd.DataFrame(df.iloc[0:self.show_num, :]).reset_index().drop('index', axis=1)
            obj_name = str(p.split("/")[1])
            if First:
                json = result.rename(columns={"alpha": str(obj_name.split(".")[0])})
                First = False
            else:
                obj_name = str(obj_name.split(".")[0])
                result = result.rename(columns={"alpha": obj_name})
                S = pd.Series(result.loc[:, obj_name])
                json = pd.concat([json, S], axis=1, join="outer")
        if self.export_json:
            json.to_json('data.json')
        else:
            pass
        return json


    def get_json(df: pd.DataFrame, toStr: bool = True) -> list:
        '''

        :param df:
        :param toStr:
        :return:
        '''
        if 'date' in df.columns:
            df.drop(columns=["date"], inplace=True)
        else:
            pass
        df.set_index("stockcode", inplace=True)
        if toStr:
            df = df.astype(str)
        else:
            pass
        return df.to_dict("dict")



if __name__ == '__main__':
    # 因子保存路径
    path_GRU = "../data/CNN-P2-43&44-M12-1912.f"
    path_TCN = "../data/GRU-P2-43&44-M12-1912.f"
    path_CNN = "../data/HAN-P2-43&44-M12-1912.f"
    path_LSTM = "../data/LSTM-P2-43&44-M12-1912.f"
    path_TRANS = "../data/TCN-P2-43&44-M12-1912.f"
    path_HAN = "../data/TRANS-P2-43&44-M12-1912.f"

    # 实例化
    # GRU = Factors(path_GRU)
    # TCN = Factors(path_TCN)
    # CNN = Factors(path_CNN)
    # LSTM = Factors(path_LSTM)
    # TRANS = Factors(path_TRANS)
    # HAN = Factors(path_HAN)

    # 计算相关系数
    # df = pd.concat([GRU.f_series, TCN.f_series, CNN.f_series, LSTM.f_series, TRANS.f_series, HAN.f_series], axis=1)
    # c = pd.DataFrame(df.iloc[:, :].corr()).to_csv("corr_matrix.csv")

    # 根据股票名称获得因子值
    # result = CNN.quary_F_bystock(stockcode='000009.SZ')

    # 根据交易日获得因子值
    # result = LSTM.quary_F_bydate(date=20191206)
    # result=result.sort_values(by="alpha")

    # 获得.f文件中存储的股票和交易日清单
    # l = TRANS.get_F_stocklist()
    # s = TRANS.get_F_date()

    # print(result)

    result = Factor_board(LSTM_path=path_LSTM, GRU_path=path_GRU, TCN_path=path_TCN, CNN_path=path_CNN,TRANS_path=path_TRANS, HAN_path=path_HAN).JSON
    print(result)

    # print(r)