import os
import json
import csv
import pandas as pd
from flask import *
import numpy as np

# from CCRS import bASSL4CCR, bCCRCNN, bCCRGNN
from Factor_utils import Factors, Factor_board, get_path_list, filter_factors, generate_query_statement, get_json, \
    get_plot_data, cal_factor_corr,name_to_path

app = Flask(__name__,static_folder="static")

pd.set_option('display.width', 10000) # 设置字符显示宽度
pd.set_option('display.max_rows', None) # 设置显示最大行
pd.set_option('display.max_columns', None) # 设置显示最大列，None为显示所有列

factor_description = r"C:\Users\Administrator\Desktop\feather\factor_description.json"
factor_path = r"C:\Users\Administrator\Desktop\feather\data"


x = np.random.rand(39)
std = np.array([5.27138270e-01, 8.25752230e+00, 9.95533666e-01, 2.26933173e+09,
    1.01670778e+00, 7.87983283e+09, 6.64906142e+09, 1.30192999e+02,
    1.38856619e+03, 1.78234935e+03, 5.24114252e+03, 5.14663385e-01,
    2.39990120e-01, 1.73779538e+00, 2.79022304e-01, 6.83370576e+01,
    6.80914889e+00, 7.50007005e+00, 1.54219387e+00, 1.35281783e+00,
    6.63452952e-01, 5.58468562e-01, 2.47359585e+00, 3.68025702e+00,
    2.74342540e+00, 3.71265192e-01, 6.53042120e-01, 2.58621214e+02,
    5.98361612e+00, 7.29341857e+01, 3.72839459e+00, 5.27138270e-01,
    1.50166855e+01, 2.39990120e-01, 4.33075673e+00, 8.60610288e+00,
    1.74420606e+01, 1.48476654e+01, 1.59381980e+00])
mean = np.array([ 4.49396750e-04, -2.22269479e-01,  2.72138836e-01,  5.33585321e+08,
    3.28045229e-01,  2.80571117e+09,  2.35327421e+09,  1.86014395e+01,
    1.70753112e+02,  7.17274753e+01,  7.16284455e+02,  5.83205251e-01,
    2.64915407e-01, -6.14608971e-03,  1.05549025e-01, -3.06572374e+00,
    -4.43146209e-01, -4.33107792e-01,  1.63866649e+00,  1.24622301e+00,
    4.91154084e-01,  1.71464830e-01,  6.29593370e-01,  2.83910118e+00,
    6.00980812e-01,  4.92503620e-01,  3.34616178e-01,  2.53245673e+01,
    2.26663399e-02,  1.44388696e+00,  1.17646309e-01,  4.49396750e-04,
    3.29824905e+00,  2.64915407e-01,  1.21270507e+00, -3.27024112e-01,
    3.91242440e-01,  1.00338497e+00,  3.64050784e-02])
tensorinput = (x-mean)/(std)


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


# 数组去重
def array_repeat(source):
    dest = []
    for e in source:
        if e not in dest:
            dest.append(e)
    return dest


# 路由
# 首页显示
@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# 详情页显示
@app.route('/details/<string:details>',methods=['GET','POST'])
def details(details):
    return render_template('details.html',details=details)

# 搜索页面
@app.route('/search',methods=['GET', 'POST'])
def search():
    return render_template('search.html')

# 自助评级
@app.route('/ccrs',methods=['GET', 'POST'])
def ccrs():
    return render_template('ccrs.html')


# 数据接口
# 首页---表单选框内容---数据接口
@app.route('/initform', methods=['GET', 'POST'])
def initform():
    data = []
    obj = {}
    list_key = ['algo','meta','freq','vol','end']
    with open('./factor_description.json', 'r', encoding='utf-8') as f:
        dataset = pd.read_json(f)
        for key in dataset.values:
            data.append(array_repeat(key))
        del data[0]
        for i in range(len(list_key)):
            obj.update({list_key[i]:data[i]})
        # print(obj)
    return jsonify(obj)


# 首页---多条件查询表单-----接口
@app.route('/formsub',methods=['GET','POST'])
def formsub():
    algo = request.form.get('algo')
    freq = request.form.get('freq')
    vol = request.form.get('vol')
    meta = request.form.get('meta')
    end = request.form.get('end')
    # print(algo,freq,vol,meta,end)
    dict = {}
    if algo != 'no':
        dict.update({'algo':algo})
    if freq != 'no':
        dict.update({'freq': freq})
    if vol != 'no':
        dict.update({'vol': vol})
    if meta != 'no':
        dict.update({'meta': meta})
    if end != 'no':
        dict.update({'end': end})


    # 根据dict字典中的检索条件Query，返回值是查询到因子文件的绝对路径
    if algo == 'no' and freq == 'no' and vol == 'no' and meta == 'no' and end == 'no':
        dict = None

    path_list = get_path_list(factor_list=filter_factors(query_statement=generate_query_statement(dict=dict),
                                                         factor_description=factor_description),
                              factor_path=factor_path)
    # 利用因子绝对路径的list生成因子看板数据
    result = get_json(Factor_board(path_list=path_list).factor_board)
    return jsonify(result)



# 首页---分页获取总条数---数据接口
@app.route('/tol_page', methods=['GET', 'POST'])
def tol_page():
    path_list = get_path_list(factor_list=filter_factors(query_statement=generate_query_statement(),
                                                         factor_description=factor_description),
                              factor_path=factor_path)
    # 利用因子绝对路径的list生成因子看板数据
    result = get_json(Factor_board(path_list=path_list).factor_board)
    length = len(result)
    return str(length)


# 首页---分页----数据接口
@app.route('/page', methods=['GET', 'POST'])
def page():
    page = request.args.get('page')

    path_list = get_path_list(factor_list=filter_factors(query_statement=generate_query_statement(),
                                                         factor_description=factor_description),
                              factor_path=factor_path)
    # 利用因子绝对路径的list生成因子看板数据
    result = get_json(Factor_board(path_list=path_list).factor_board)

    arr = []
    res = {}
    for key in result:
        if key == 'stockcode':
            continue
        arr.append(key)
    arr = arr[(int(page)-1)*15:int(page)*15]
    for key in arr:
        data = {key: result[key]}
        res.update(data)
    # print(res)
    return json.dumps(res)

# 首页 --- 换一换 ---  数据接口
@app.route('/changeList', methods=['GET', 'POST'])
def changeList():
    path_list = get_path_list(factor_list=filter_factors(query_statement=generate_query_statement(),
                                                         factor_description=factor_description),
                              factor_path=factor_path)
    # 利用因子绝对路径的list生成因子看板数据
    result = get_json(Factor_board(path_list=path_list).factor_board)
    return jsonify(result)


# 首页 --- 弹框信息 --- 数据接口
@app.route('/indexdes', methods=['GET', 'POST'])
def indexdes():
    des_data = json.load(open('./factor_description.json', 'r', encoding='utf-8'))
    return jsonify(des_data)


# 首页 --- echarts表格 ---- 数据接口
@app.route('/indexEcharts',methods=['GET','POST'])
def indexEcharts():
    y = request.args.get('y_axis')
    x = request.args.get('x_axis')
    if y == '':
        y='GRU-P2-43&44-M12-1912'
    if x == '':
        x="TCN-P2-43&44-M12-1912"
    path_list = get_path_list(factor_list=filter_factors(query_statement=generate_query_statement(),factor_description=factor_description),factor_path=factor_path)
    result=get_plot_data(df=Factor_board(path_list=path_list).factor_board,x=x,y=y)
    return jsonify(result)


# 首页 --- 计算相关系数 --- 数据接口
@app.route('/coefficient',methods=['GET','POST'])
def coefficient():
    y = request.args.get('y_axis')
    x = request.args.get('x_axis')
    corr = cal_factor_corr(x=x, y=y)
    return str(corr)


# details页---描述信息----数据接口
@app.route('/des',methods=['GET','POST'])
def des():
    title = request.args.get('title')
    des_data = json.load(open('./factor_description.json', 'r', encoding='utf-8'))
    return jsonify(des_data[title])

# details页---三维立体echarts图形展示----数据接口
@app.route('/echarts',methods=['GET','POST'])
def echarts():
    arr = json.load(open(os.path.join('static/data/','echarts.json'),'r',encoding="utf-8"))
    return jsonify(arr)

# details页 --- 按条件查询因子 --- 数据接口
@app.route('/condition',methods=['GET', 'POST'])
def condition():
    fac = request.args.get('_path')
    s = request.args.get('s')
    table_data = Factors(name_to_path(factor_path=factor_path, name=fac)).quary_F_bystock(stockcode=s).head(10)
    arr = []
    if len(table_data.index):
        for rows in table_data.values:
            data = {'stockcode': rows[0], 'alpha': rows[2]}
            arr.append(data)
    else:
        data = {'stockcode': '数据为空', 'alpha': '数据为空'}
        arr.append(data)
    return jsonify(arr)


# details页----按时间查询股票因子-----接口
@app.route('/dateSearch',methods=['GET', 'POST'])
def dateSearch():
    search = request.form.get('search')
    _path = request.form.get('_path')
    table_data = Factors(name_to_path(factor_path=factor_path, name=_path)).quary_F_bydate(date=int(search)).head(10)
    # print(table_data)
    arr = []
    if len(table_data.index):
        for rows in table_data.values:
            data = {'stockcode': rows[0], 'alpha': rows[2]}
            arr.append(data)
    else:
        data = {'stockcode':'数据为空','alpha':'数据为空'}
        arr.append(data)
    return jsonify(arr)


# 自助评级页面 ---  评级查询 ----  数据接口
@app.route('/grade',methods=['POST', 'GET'])
def grade():
    # if request.method == 'POST':
    #     que = json.loads(request.get_data())
    #     print(que)
    #     model = que['model']
    #     tensorinput = (np.array(que['x'])-mean)/(std)
    #     asslout = bASSL4CCR(tensorinput)
    #     print(asslout)
    #     cnnout = bCCRCNN(tensorinput)
    #     print(cnnout)
    #     gnnout = bCCRGNN(tensorinput)
    #     print(gnnout)
    #     if model == "ASSL4CCR":
    #         return asslout
    #     elif model == "CCRGNN":
    #         return gnnout
    #     elif model=="CCRCNN":
    #         return cnnout
    #     else:
    #         return 'model error!!! select from CCRCNN,CCRGNN,ASSL4CCR'
    # else:
        return "error"



# example案例
# obama数据接口
@app.route('/obama',methods=['GET','POST'])
def obama():
    arr = json.load(open(os.path.join('static/data/','obama_budget_proposal_2012.json'),'r',encoding="utf-8"))
    # print(json.dumps(arr))
    return json.dumps(arr)

# music数据接口
@app.route('/music',methods=['GET','POST'])
def music():
    arr = []
    with open(os.path.join('static/data/', 'music.csv'), 'r',encoding="utf-8") as f:
        reader = csv.DictReader(f) #csv中字典方式的读
        for row in reader:
            dic = {'name':row['\ufeffFormat'],'year':row['Year'],'value':row['Revenue (Inflation Adjusted)']}
            arr.append(dic)
    return json.dumps(arr)







if __name__ == '__main__':
        app.run(host='127.0.0.1')