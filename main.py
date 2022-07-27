import os
import json
import csv
import pandas as pd
from flask import *
from Factor_utils import Factors, Factor_board, get_path_list, filter_factors, generate_query_statement, get_json

app = Flask(__name__,static_folder="static")

pd.set_option('display.width', 10000) # 设置字符显示宽度
pd.set_option('display.max_rows', None) # 设置显示最大行
pd.set_option('display.max_columns', None) # 设置显示最大列，None为显示所有列

factor_description = r"C:\Users\Administrator\Desktop\feather\factor_description.json"
factor_path = r"C:\Users\Administrator\Desktop\feather\data"


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

# details页----按时间查询股票因子-----接口
@app.route('/search',methods=['GET', 'POST'])
def search():
    search = request.form.get('search')
    detail_path = './data/' + request.form.get('_path') + '.f'
    # print(search)
    table_data = Factors(detail_path).quary_F_bydate(date=int(search)).head(10)

    arr = []
    if len(table_data.index):
        for rows in table_data.values:
            data = {'stockcode': rows[0], 'alpha': rows[2]}
            arr.append(data)
    else:
        data = {'stockcode':'数据为空','alpha':'数据为空'}
        arr.append(data)
    return jsonify(arr)








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