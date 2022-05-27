import os
import pymysql
import feather
from flask import *


app = Flask(__name__)

# 连接 feather数据库
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': 'root',
    'db' : 'feather',
    'local_infile': 1
}
conn = pymysql.connect(**config)
 # 执行 SQL 创建 表tb_student
cursor = conn.cursor()
 # sql = "CREATE TABLE testimport(ID INT NOT NULL, date VARCHAR(255) NULL,stockcode VARCHAR(255) NULL,alpha VARCHAR(255) NULL)"
sql = "CREATE TABLE testimport1(date VARCHAR(255) NULL,stockcode VARCHAR(255) NULL,alpha VARCHAR(255) NULL)"
cursor.execute(sql)
# conn.close()
df = feather.read_dataframe("F:/py_project/feather/alpha15.f")
df.to_csv("F:/py_project/feather/test1.json")
 # CSV数据高效导入 MYSQL
# cursor = conn.cursor()
sql = "LOAD DATA LOCAL INFILE '{0}' INTO TABLE {1} CHARACTER SET GBK FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' IGNORE 1 LINES"
try:
    cursor.execute(sql.format("F:/py_project/feather/test.csv", "testimport1"))
    conn.commit()
except Exception as e:
    print(e)
    conn.rollback()
# cursor = conn.cursor()
# sql = "select * from tb_student"
# cursor.execute(sql)
# rows = cursor.fetchall()
# ls2 = list(map(list, rows))
    conn.close()
# print(ls2)


if __name__ == '__main__':
        app.run(host='127.0.0.1')