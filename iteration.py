import os
import json
# import feather
import pymysql.cursors
import csv
import pandas as pd
from flask import *
from Factor_utils import Factors


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



# 第一个数据图表展示查询
@app.route('/search1/<string:search1>',methods=['GET'])
def search1(search1):
    # print(search1)
    search_all_data = return_all('select * from test where date="' + search1 + '.0"')
    list2 = json.dumps(search_all_data)
    return list2


# 详情页数据接口
@app.route('/stockcode',methods=['GET','POST'])
def stockcode():
    search = request.form.get('search')
    if search:
        path_TCN = "./utils/GRU-F2-D-M3.f"
        TCN = Factors(path_TCN)
        TCN = TCN.quary_F_bydate(date=20191206)
        table_data = TCN
    else:
        path_TCN = "./utils/GRU-F2-D-M3.f"
        TCN = Factors(path_TCN)
        TCN = TCN.quary_F_bydate(date=20191206)
        table_data = TCN
    return str(table_data)


@app.route('/csvpasue',methods=['GET','POST'])
def obama():
    arrcsv = json.load(open(os.path.join('static/data/example/testdemo/','8.csv'),'r',encoding="utf-8"))
    print(json.dumps(arrcsv))
    return json.dumps(arrcsv)

@app.route('/len')
def handler_feather(filr_path):
    df=pd.read_feather(filr_path)
    print(df)



if __name__ == '__main__':
        app.run(host='127.0.0.1')