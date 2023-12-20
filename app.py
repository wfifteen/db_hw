import os
import sys
import pyodbc
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
#
# name = 'Grey Li'
#
# movies = [
# {'title': 'My Neighbor Totoro', 'year': '1988'},
# {'title': 'Dead Poets Society', 'year': '1989'},
# {'title': 'A Perfect World', 'year': '1993'},
# {'title': 'Leon', 'year': '1994'},
# {'title': 'Mahjong', 'year': '1996'},
# {'title': 'Swallowtail Butterfly', 'year': '1996'},
# {'title': 'King of Comedy', 'year': '1999'},
# {'title': 'Devils on the Doorstep', 'year': '1999'},
# {'title': 'WALL-E', 'year': '2008'},
# {'title': 'The Pork of Music', 'year': '2012'},
# ]


WIN = sys.platform.startswith('win')
if WIN: # 如果是 Windows 系统，使用三个斜线
     prefix = 'sqlite:///'
else:
     #否则使用四个斜线
     prefix = 'sqlite:////'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)


@app.errorhandler(404) # 传入要处理的错误代码
def page_not_found(e): # 接受异常对象作为参数
  # user = User.query.first()
  user=('A','B','C','D')
  return render_template('404.html', user=user), 404 # 返回模板和状态码
@app.route('/index')
def index():
    # 连接到SQL Server数据库
    mconn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-CAQ82VO6;DATABASE=movieDB')
    # 创建游标对象
    mcursor = mconn.cursor()
    # 执行SQL查询语句
    msql = "SELECT * FROM movie_info"
    mcursor.execute(msql)
    # 获取查询结果
    mdata = mcursor.fetchall()
    mdatalist = []
    for item in mdata:
      mdatalist.append(item)

    # sql1="SELECT count(*) FROM movie_info"
    # cursor.execute(sql1)
    # total = cursor.fetchall()
    mcursor.close()
    mconn.close()
    return render_template('index.html',movie_info=mdatalist)
 #page=page,countnum=int(int(total[0])/15)#

@app.route('/ac')
def ac():
    # 连接到SQL Server数据库
    aconn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-CAQ82VO6;DATABASE=movieDB')
    # 创建游标对象
    acursor = aconn.cursor()
    # 执行SQL查询语句
    asql = "SELECT * FROM actor_info"
    acursor.execute(asql)
    # 获取查询结果
    adata = acursor.fetchall()
    adatalist = []
    for item in adata:
      adatalist.append(item)

    # sql1="SELECT count(*) FROM movie_info"
    # cursor.execute(sql1)
    # total = cursor.fetchall()
    acursor.close()
    aconn.close()
    return render_template('ac.html',actor_info=adatalist)
 #page=page,countnum=int(int(total[0])/15)#

app.run()

#
# class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
#    id = db.Column(db.Integer, primary_key=True)  # 主键
#    name = db.Column(db.String(20))  # 名字
# class Movie(db.Model):  # 表名将会是 movie
#   id = db.Column(db.Integer, primary_key=True)  # 主键
#   title = db.Column(db.String(60))  # 电影标题
#   year = db.Column(db.String(4))  # 电影年份
# from flask import Flask
