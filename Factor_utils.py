# encoding:utf-8
"""
@author:liuzeyu
@time:2022-07-29
@version:v1.1
"""

import pandas as pd
import os
import numpy as np


class Factors:
    def __init__(self, path):
        self.path = path

    @property
    def f_series(self) -> pd.Series:
        '''
        将实例化的因子转换为一个series输出
        :return:一维的因子值序列
        '''
        df = pd.Series(pd.read_feather(self.path).iloc[:, 2])
        df.name = str(os.path.split(self.path)[1])
        return df

    @property
    def f_ndarray(self) -> np.ndarray:
        '''
        （测试中）将实例化的因子转换为一个3维ndarray输出
        :return:
        '''
        df = pd.read_feather(self.path)
        df[['date']] = df[['date']].astype(int)
        df.sort_values(by=["stockcode", "date"], inplace=True)
        n = df.iloc[:, :2].nunique()
        if n[0] * n[1] != len(df):
            print('因子值不完整，部分股票或交易日可能有缺值，无法将其reshape为三维矩阵')
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
        遍历因子文件，查看共涵盖多少只的股票（重复值仅记录一次）
        :param review:是否查看结果，默认开启
        :return:因子文件涵盖的股票列表
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
        遍历因子文件，查看共涵盖多少个的交易日（重复值仅记录一次）
        :param review:是否查看结果，默认开启
        :return:因子文件涵盖的交易日列表
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
        核心query功能，用于根据股票名称获得因子值
        :param stockcode:要获取哪只股票的因子值，股票代码示例：'000009.SZ'
        :return:存储查询结果的datafram
        '''
        if stockcode == None:
            print("请输入一个stockcode")
        else:
            df = pd.read_feather(self.path)
            df[['date']] = df[['date']].astype(int)
            df.sort_values(by=["stockcode", "date"], inplace=True)
            return df[df["stockcode"].isin([stockcode])]

    def quary_F_bydate(self, date: int = None) -> pd.DataFrame:
        '''
        核心query功能，用于根据交易日获得因子值
        :param date:要获取哪个交易日的因子值，交易日示例：'20191206'，限制int格式
        :return:存储查询结果的datafram
        '''
        if date == None:
            print("请输入一个date")
        else:
            df = pd.read_feather(self.path)
            df[['date']] = df[['date']].astype(int)
            df.sort_values(by=["date", "stockcode"], inplace=True)
            return df[df["date"].isin([date])]


def generate_query_statement(dict: dict = None) -> str:
    '''
    根据传入的字典键值对，生成文件系统存储方案的query语句
    :param dict:拟查询的条件，以键值对形式存储，如果不输入则使用一个默认值
    :return:字符串格式的query语句，作为filter_factors方法的输入
    '''
    if dict == None:
        dict = {
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
    根据query语句过滤数据
    :param query_statement:由generate_query_statement方法生成的query语句
    :param factor_description:存储所有因子meta数据的json文件绝对路径
    :return:返回一个list，存储了经过滤后的因子名称
    '''
    if factor_description == None:
        print("请指定因子配置文件的路径")
    else:
        pass
    try:
        factor_obj = pd.read_json(path_or_buf=factor_description, orient="index", dtype="str").reset_index()
        del factor_obj['index']
        factor_list = factor_obj.query(query_statement).title
        return list(factor_list)
    except Exception as e:
        print("未能成功打开factor_description.json，请检查其路径是否正确")


def get_path_list(factor_list, factor_path: str = None) -> list:
    '''
    批量生成因子的存储路径，与name_to_path的功能相近，与filter_factors方法耦合使用
    :param factor_list:由ilter_factors方法生成的因子list
    :param factor_path:将因子list转变为因子路径list
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


class Factor_board():
    def __init__(self, path_list):
        self.show_num = 5
        self.export_json = False
        self.path_list = path_list

    @property
    def factor_board(self) -> pd.DataFrame:
        '''
        核心属性方法，生成因子看板数据
        :return:因子看板需要展示的数据，拟展示的股票数量可由类初始化时的self.show_num来控制
        '''
        pathlist = self.path_list
        First = True
        factor_board = pd.DataFrame()
        lastdata = Factors(pathlist[-1]).get_F_date(review=False)[-1]
        for p in pathlist:
            df = Factors(p).quary_F_bydate(date=int(lastdata)).drop('date', axis=1)
            # 默认显示字典排序的前（self.show_num）只股票
            # result = pd.DataFrame(df.iloc[0:self.show_num, :]).reset_index().drop('index', axis=1)
            # 随机显示（self.show_num）只股票
            result = pd.DataFrame(df.sample(n=self.show_num, replace=False, axis=0)).reset_index().drop('index', axis=1)
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


def get_json(df: pd.DataFrame, toStr: bool = True) -> dict:
    '''
    用于将df格式的数据转换为类json的键值对格式，以便于前端js解析
    :param df:待转换格式的df
    :param toStr:是否将df中的int和flaot值全部转换为str，默认开启
    :return:一组嵌套字典，包含多层键值对
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
    从因子看板展示结果中挑选2个因子用于可视化
    :param df:因子看板展示的数据，pd：DataFrame格式
    :param x:因子1的名称，如："TCN-P2-43&44-M12-1912"
    :param y:因子2的名称，如："GRU-P2-43&44-M12-1912"
    :return:前端js可解析的嵌套array，在python中输出为嵌套2层的list
    '''
    df = df.loc[:, [x, y]]
    l = df.values.tolist()
    l.insert(0, list(df))
    return l


def name_to_path(factor_path: str, name: str) -> str:
    """
    将因子名称转化为在磁盘中的存储路径
    :param factor_path:指定因子库的路径，如：r"F:\WebProject\feater\待处理数据\factors\factors"
    :param name:待获取其路径的因子
    :return:因子在磁盘中的存储绝对路径，字符串格式
    """
    if name.split(".")[-1] == 'f':
        result = (factor_path + '\\' + name)
    else:
        result = (factor_path + '\\' + name + '.f')
    return result


def cal_factor_corr(x: str, y: str) -> float:
    """
    计算两个因子的相关系数，用于因子看板页下方的因子对比
    :param x:因子1的名称，如："TCN-P2-43&44-M12-1912"
    :param y:因子2的名称，如："GRU-P2-43&44-M12-1912"
    :return:因子1和因子2的相关系数，介于-1到1之间的浮点数
    """
    x_path = name_to_path(factor_path=factor_path, name=x)
    y_path = name_to_path(factor_path=factor_path, name=y)
    df = pd.concat([Factors(path=x_path).f_series, Factors(path=y_path).f_series], axis=1)
    corr = df.iloc[:, 0].corr(df.iloc[:, 1])
    return corr


if __name__ == '__main__':
    ######因子看板页配置文件
    dict = {
        "algo": "LSTM",
        "meta": "价量因子：43&44",
        "freq": "日频",
        "vol": "12个月数据",
        "end": "20191231",
    }
    factor_description = r"F:\WebProject\feater\待处理数据\factors\factors\factor_description.json"
    factor_path = r"F:\WebProject\feater\待处理数据\factors\factors"

    # 根据dict字典中的检索条件Query，返回值是查询到因子文件的绝对路径
    path_list = get_path_list(factor_list=filter_factors(query_statement=generate_query_statement(), factor_description=factor_description), factor_path=factor_path)
    # 利用因子绝对路径的list生成因子看板数据
    result = get_json(Factor_board(path_list=path_list).factor_board)

    # 从因子看板展示结果中挑选2个因子进行可视化
    # x = "TCN-P2-43&44-M12-1912"
    # y = 'GRU-P2-43&44-M12-1912'
    # data = Factor_board(path_list=path_list).factor_board
    # result=get_plot_data(df=data,x=x,y=y)
    # print(result)

    # 从因子看板展示结果中挑选2个因子计算相关系数
    # x = "TCN-P2-43&44-M12-1912"
    # y = 'GRU-P2-43&44-M12-1912'
    # corr = cal_factor_corr(x=x, y=y)

    ######因子详情页配置文件
    # factor_description = r"F:\WebProject\feater\待处理数据\factors\factors\factor_description.json"
    # factor_path = r"F:\WebProject\feater\待处理数据\factors\factors"

    # 根据股票名称获得因子值
    # fac = 'TCN-P2-43&44-M12-1912'
    # s='000009.SZ'
    # result = Factors(name_to_path(factor_path=factor_path, name=fac)).quary_F_bystock(stockcode=s)
    # print(result)

    # 根据交易日获得因子值
    # fac = 'TCN-P2-43&44-M12-1912'
    # d=20191206
    # result = Factors(name_to_path(factor_path=factor_path, name=fac)).quary_F_bydate(date=d)
    # print(result)
