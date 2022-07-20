import os
import json
import csv
import pandas as pd
from flask import *
from Factor_utils import Factors, Factor_board

app = Flask(__name__,static_folder="static")

pd.set_option('display.width', 10000) # 设置字符显示宽度
pd.set_option('display.max_rows', None) # 设置显示最大行
pd.set_option('display.max_columns', None) # 设置显示最大列，None为显示所有列



# 路由
# 首页显示
@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# 详情页显示
@app.route('/details/<string:details>',methods=['GET','POST'])
def details(details):
    details_path = './utils/' + details + '.f'
    search = request.form.get('search')
    if search:
        table_data = Factors(details_path).quary_F_bydate(date=search)
    else:
        table_data = Factors(details_path).quary_F_bydate(date=20191206)
    return render_template('details.html', table_data=table_data,details=details)



# 数据接口
# 首页---因子看板----数据接口
@app.route('/home',methods=['GET','POST'])
def home():
    fr = open('./utils/test.json', 'r', encoding='utf-8')
    return str(fr.read())

# 首页---多条件查询表单-----接口
@app.route('/formsub',methods=['GET','POST'])
def formsub():
    # combination = request.form.get('combination')
    # pool = request.form.get('pool')
    # search_all_data = return_all('select * from test where date="' + combination + '" or stockcode <'+ pool)
    # 统计
    pool_all = 0
    # for i in search_all_data:
    #     pool_all += int(float(i[1]))
        # print(i[2])
    return str(pool_all)



# details页---三维立体echarts图形展示----数据接口
@app.route('/echarts',methods=['GET','POST'])
def echarts():
    arr = json.load(open(os.path.join('static/data/','echarts.json'),'r',encoding="utf-8"))
    # print(json.dumps(arr))
    return json.dumps(arr)

# details页----按时间查询股票因子-----接口
@app.route('/search',methods=['GET', 'POST'])
def search():
    search = request.form.get('search')
    detail_path = './utils/' + request.form.get('_path') + '.f'
    # print(search)
    table_data = Factors(detail_path).quary_F_bydate(date=int(search))
    # print(table_data)
    return str(table_data)



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