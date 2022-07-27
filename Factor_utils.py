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
    def __init__(self, path_list):
        self.show_num = 5
        self.export_json = False
        self.path_list = path_list

    @property
    def factor_board(self) -> pd.DataFrame:
        '''

        :return:
        '''
        pathlist = self.path_list
        First = True
        factor_board = pd.DataFrame()
        lastdata = Factors(pathlist[-1]).get_F_date(review=False)[-1]
        for p in pathlist:
            df = Factors(p).quary_F_bydate(date=int(lastdata)).drop('date', axis=1)
            result = pd.DataFrame(df.iloc[0:self.show_num, :]).reset_index().drop('index', axis=1)
            obj_name = os.path.basename(p)
            if First:
                factor_board = result.rename(columns={"alpha": str(obj_name.split(".")[0])})
                First = False
            else:
                obj_name = str(obj_name.split(".")[0])
                result = result.rename(columns={"alpha": obj_name})
                S = pd.Series(result.loc[:, obj_name])
                factor_board = pd.concat([factor_board, S], axis=1, join="outer")
        if self.export_json:
            factor_board.to_json('data.factor_board')
        else:
            pass
        return factor_board

def generate_query_statement(dict: dict = None) -> str:
    '''

    :param dict:
    :return:
    '''
    if dict == None:
        dict = {
            # "algo": "LSTM",
            "meta": "价量因子：43&44",
            "freq": "日频",
            "vol": "12个月数据",
            "end": "20191231",
        }
    else:
        pass
    list = []
    for k, v in dict.items():
        s = k + '==\'' + v + '\''
        list.append(s)
    str = "&".join(list)
    return str


def filter_factors(query_statement: str, factor_description=None) -> list:
    '''

    :param query_statement:
    :param factor_description:
    :return:
    '''
    if factor_description == None:
        print("请指定因子配置文件的路径")
    else:
        pass
    try:
        factor_obj = pd.read_json(path_or_buf=factor_description, orient="index", dtype="str").reset_index()
    except Exception as e:
        print("未能成功打开factor_description.json，请检查其路径是否正确")
    del factor_obj['index']
    factor_list = factor_obj.query(query_statement).title
    return list(factor_list)


def get_path_list(factor_list, factor_path: str = None) -> list:
    '''

    :param factor_list:
    :param factor_path:
    :return:
    '''
    if factor_path == None:
        print("请指定因子文件存储的路径")
    else:
        pass
    path_list = []
    for f in factor_list:
        for root, dirs, files in os.walk(factor_path):
            for file in files:
                if os.path.basename(file) == f + ".f":
                    path_list.append(os.path.join(root, file))
    return path_list

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

def get_plot_data(df: pd.DataFrame, x: str, y: str) -> list:
    '''

    :param df:
    :param x:
    :param y:
    :return:
    '''
    df = df.loc[:, [x, y]]
    l = df.values.tolist()
    l.insert(0, list(df))
    return l




if __name__ == '__main__':
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

    dict = {
        "algo": "LSTM",
        "meta": "价量因子：43&44",
        "freq": "日频",
        "vol": "12个月数据",
        "end": "20191231",
    }
    factor_description = r"C:\Users\Administrator\Desktop\feather\factor_description.json"
    factor_path = r"C:\Users\Administrator\Desktop\feather\data"

    # 根据dict字典中的检索条件Query，返回值是查询到因子文件的绝对路径
    path_list = get_path_list(factor_list=filter_factors(query_statement=generate_query_statement(), factor_description=factor_description), factor_path=factor_path)
    # 利用因子绝对路径的list生成因子看板数据
    # result = get_json(Factor_board(path_list=path_list).factor_board)
    # print(result)

    # result = Factor_board(LSTM_path=path_LSTM, GRU_path=path_GRU, TCN_path=path_TCN, CNN_path=path_CNN,TRANS_path=path_TRANS, HAN_path=path_HAN).JSON
    # r=result.get_json(result)


    x="TCN-P2-43&44-M12-1912"
    y='GRU-P2-43&44-M12-1912'
    result=get_plot_data(df=Factor_board(path_list=path_list).factor_board,x=x,y=y)
    print(result)