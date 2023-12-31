import os
import sys
import pyodbc
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, url_for, redirect, flash
from django.shortcuts import get_object_or_404



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

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/index')
def index():
    return render_template('index.html')



@app.route('/mv', methods=['GET','POST'])
def mv():
    # 连接到SQL Server数据库
    mconn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-CAQ82VO6;DATABASE=movieDB')
    # 创建游标对象
    mcursor = mconn.cursor()
    # 执行SQL查询语句
    msql = "SELECT movie_info.movie_id,movie_name,release_date,country,type,year,box FROM movie_info,move_box WHERE move_box.movie_id=movie_info.movie_id"
    mcursor.execute(msql)
    # 获取查询结果
    mdata = mcursor.fetchall()
    mdatalist = []
    for item in mdata:
      mdatalist.append(item)

    if request.method == 'POST':  # 判断是否是 POST 请求
        #获取表单数据
        movie_id = request.form.get('movie_id')  # 传入表单对应输入字段的name 值
        movie_name = request.form.get('movie_name')
        release_date = request.form.get('release_date')
        country = request.form.get('country')
        type = request.form.get('type')
        year = request.form.get('year')
        box = request.form.get('box')

        def test_function():
            global movie_id
            global movie_name
            global release_date
            global country
            global type
            global year
            global box

        test_function()
    #
        if not movie_id or not movie_name or not release_date or not country or not type or not year or not box:
            flash('无效输入')  # 显示错误提示
        return redirect(url_for('mv'))  # 重定向回主页

    # 信息存入数据库
        sql1 = "insert into movie_info(movie_id, movie_name, release_date, country,type,year )values(%s,%s,%s,%s,%s,%s)"
        mcursor.execute(sql1, (movie_id, movie_name, release_date, country, type, year))
        sql2 = "insert into move_box(box )values(%s)"
        mcursor.execute(sql2, (box))
        flash("成功存入一条电影信息")

    mcursor.close()
    mconn.close()

    return render_template('mv.html',movie_info=mdatalist)

movie12=[
    {
        'movieid':'1001','movie_name':'战狼2','release_date':'datetime(2017 7 27 0 0 0)','country':'中国','type':'战争','box':'56.84'
    }
]


@app.route('/movie/edit/<int:movieid>', methods=['GET', 'POST'])
def edit(movieid):
    # 连接到SQL Server数据库
    mconn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-CAQ82VO6;DATABASE=movieDB')
    # 创建游标对象
    mcursor = mconn.cursor()
    msql = "SELECT movie_info.movie_id,movie_name,release_date,country,type,year,box FROM movie_info,move_box WHERE move_box.movie_id=movie_info.movie_id"
    mcursor.execute(msql)
    # 获取查询结果
    mdata = mcursor.fetchall()
    mdatalist = []
    for item in mdata:
      mdatalist.append(item)
    mcursor.close()
    mconn.close()


    return render_template('edit.html', movieid='1001') # 传入被编辑的电影记录



@app.route('/movie/delete/<int:movieid>', methods=['POST']) #限定只接受 POST 请求
def delete(movieid):
    # 连接到SQL Server数据库
    mconn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-CAQ82VO6;DATABASE=movieDB')
    # 创建游标对象
    mcursor = mconn.cursor()
    msql = "SELECT movie_info.movie_id,movie_name,release_date,country,type,year,box FROM movie_info,move_box WHERE move_box.movie_id=movie_info.movie_id"
    mcursor.execute(msql)
    # 获取查询结果
    mdata = mcursor.fetchall()
    mdatalist = []
    for item in mdata:
        mdatalist.append(item)
    mcursor.close()
    mconn.close()
    movie = mdatalist.query.get_or_404(movieid) # 获取电影记录
    db.session.delete(movie) # 删除对应的记录
    db.session.commit() # 提交数据库会话
    flash('记录已删除')
    return redirect(url_for('mv')) # 重定向回主页
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

    if request.method == 'POST':  # 判断是否是 POST 请求
        #获取表单数据
        actor_id = request.form.get('actor_id')  # 传入表单对应输入字段的name 值
        actor_name = request.form.get('actor_name')
        gender = request.form.get('gender')
        acountry = request.form.get('acountry')


        def test_function1():
            global actor_id
            global actor_name
            global gender
            global acountry

        test_function1()
    #
        if not actor_id or not actor_name or not gender or not acountry:
            flash('无效输入')  # 显示错误提示
        return redirect(url_for('ac'))  # 重定向回主页
        sql3 = "insert into actor_info(actor_id, actor_name, gender, country )values(%s,%s,%s,%s)"
        acursor.execute(sql3, (actor_id, actor_name, gender, acountry))
        flash("成功存入一条电影信息")
    # sql1="SELECT count(*) FROM movie_info"
    # cursor.execute(sql1)
    # total = cursor.fetchall()
    acursor.close()
    aconn.close()
    return render_template('ac.html',actor_info=adatalist)

@app.route('/actor/edit2/<int:actorid>', methods=['GET', 'POST'])
def edit2(actorid):
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
    acursor.close()
    aconn.close()

    actor = get_object_or_404(adatalist,actorid)
    if request.method == 'POST': # 处理编辑表单的提交请求
        actor_id = request.form['actor_id']  # 传入表单对应输入字段的name 值
        actor_name = request.form['actor_name']
        gender = request.form['gender']
        acountry = request.form['acountry']

        if not actor_id or not actor_name or not gender or not acountry:
            flash('无效输入')  # 显示错误提示
            return redirect(url_for('edit2', acotrid=actorid ))
            # 重定向回对应的编辑页面
            actor.actor_id = actor_id # 更新标题
            actor.actor_name = actor_name # 更新年份
            actor.gender = gender
            movie.country = acountry
            db.session.commit() # 提交数据库会话
            flash('记录已更新')
        return redirect(url_for('ac')) # 重定向回主页
    return render_template('edit2.html', actor=actor) # 传入被编辑的电影记录

@app.route('/actor/delete2/<int:actorid>', methods=['POST']) #限定只接受 POST 请求
def delete2(actorid):
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
    acursor.close()
    aconn.close()
    actor = adatalist.query.get_or_404(actorid) # 获取电影记录
    db.session.delete(actor) # 删除对应的记录
    db.session.commit() # 提交数据库会话
    flash('记录已删除')
    return redirect(url_for('ac')) # 重定向回主页

app.run()

