import os
import json
import feather
import pymysql.cursors
import csv
import pandas as pd
from flask import *

app = Flask(__name__,static_folder="static")

pd.set_option('display.width', 10000) # 设置字符显示宽度
pd.set_option('display.max_rows', None) # 设置显示最大行
pd.set_option('display.max_columns', None) # 设置显示最大列，None为显示所有列


def test(args):
    print(args)

# @app.route('/len')
def handler_feather(filr_path):
    # df = feather.read_dataframe("./alpha15.f")
    df = feather.read_dataframe(filr_path)
    print(df)
    # df.to_csv(name)
    # print(df.shape[0])
    # return 'len'

# 查询所有
def return_all(sql):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='feather', charset="utf8")
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
            conn.commit()
    finally:
        conn.close()
    return res

# 执行sql语句方法
def execute_sql(sql):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='feather', charset="utf8")
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
    finally:
        conn.close()




# 上传文件，将文件保存在本地
@app.route('/upload',methods=['GET', 'POST'])
def upload():
    # 通过request获取表单上传的文件
    f = request.files['file']
    # 这里注意大小冒号的区别
    sql = 'insert into filename(dname) value ("' + f.filename + '")'
    execute_sql(sql)
    f.save(os.path.join('static/',f.filename))
    return render_template('index.html')


#测试文件上传存入数据库
@app.route('/insert',methods=['GET', 'POST'])
def insert():
    # 将名字插入数据库表中
    sql = 'insert into filename(dname) value ("zxc")'
    execute_sql(sql)
    return render_template('index.html')



# 首页显示
@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('index.html')



# 按时间查询
@app.route('/search',methods=['GET', 'POST'])
def search():
    search = request.form.get('search')
    # print(search)
    search_all_data = return_all('select * from test where date="' + search + '.0"')
    list1 = json.dumps(search_all_data)
    return list1


# 第一个数据图表展示查询
@app.route('/search1/<string:search1>',methods=['GET'])
def search1(search1):
    # print(search1)
    search_all_data = return_all('select * from test where date="' + search1 + '.0"')
    list2 = json.dumps(search_all_data)
    return list2

# 第一个数据表单多条件查询语句
@app.route('/formsub',methods=['GET','POST'])
def formsub():
    combination = request.form.get('combination')
    pool = request.form.get('pool')

    search_all_data = return_all('select * from test where date="' + combination + '" or stockcode <'+ pool)

    # 统计
    pool_all = 0
    for i in search_all_data:
        pool_all += int(float(i[1]))
        # print(i[2])
    return str(pool_all)


# 详情页显示
@app.route('/details/<string:details>',methods=['GET','POST'])
def details(details):
    # print(details)
    search = request.form.get('search')
    if search:
        table_data = return_all('select * from test where date="' + search + '.0"')
    else:
        table_data = return_all('select * from test where date="20150115.0" limit 10')
    # print(table_data)
    return render_template('details.html', table_data=table_data,details=details)



# echarts
@app.route('/echarts',methods=['GET','POST'])
def echarts():
    arr = json.load(open(os.path.join('static/data/','echarts.json'),'r',encoding="utf-8"))
    # print(json.dumps(arr))
    return json.dumps(arr)

# obama
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