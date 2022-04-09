import os, re

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import cv2

from recongnize import loadModel, recongnize


app = app = Flask(__name__)
db = SQLAlchemy()

def create_app(upload_path='./upload'):
    global app, db

    app.config['UPLOAD_FOLDER'] = upload_path
    os.makedirs(upload_path, exist_ok=True)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:00000000@localhost:3306/score"
    db.init_app(app)

    app.add_url_rule('/','login', login, methods=['GET', 'POST'])
    app.add_url_rule('/home/<username>','home', home, methods=['GET', 'POST'])
    app.add_url_rule('/register/','register', register, methods=['GET', 'POST'])
    app.add_url_rule('/upload/<username>', 'upload', upload, methods=['GET', 'POST'])
    app.add_url_rule('/search/<username>', 'search', search, methods=['GET', 'POST'])
    return app

def register():
    
    if request.method == 'POST':
        
        register_username = request.form['register_account']
        register_password = request.form['Password']
        
        char_check = re.search('[a-zA-Z]', register_username[0:-10])
        
        if register_password == "" or register_username  == "":
            return render_template('register.html', failed_message = "帳號或密碼未輸入，請重新輸入")
        
        elif char_check == None:
            return render_template('register.html', failed_message = "帳號中請包含英文字母")
            
        else:
            register_result = insert_to_database(register_username, register_password)
        
        if register_result == "ok":
            global database_name 
            database_name = register_username[0:-10]
            db.engine.execute("CREATE DATABASE " + database_name + ";")
            return render_template('signin.html')
        
        elif register_result == "register failed":
            return render_template('register.html', failed_message = "該帳號已被註冊，請重新輸入")
        
    
    return render_template('register.html')

def login():
    if request.method == 'POST':
        
        input_username = request.form['account']
        input_password = request.form['password']
        check_username, check_password = check_account(input_username, input_password)

        if check_username == 0 or check_password == 0:
            return render_template('signin.html', failed_message = "帳號或密碼輸入錯誤")
        
        else :
            return redirect(url_for('home', username = request.form['account']))
        
    return render_template('signin.html')

def home(username):
    
    if request.method == 'POST':
        
        table_name = request.form['table_name']
        
        db.engine.execute("CREATE TABLE " + username[0:-10] + "." + table_name + 
                          "(`Student_Number` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,`Score` int(3) NOT NULL);")
        
        return render_template('home.html', name=username)
    
    
    return render_template('home.html', name=username)

def check_account(input_username, input_password):
    
    query = db.engine.execute("SELECT EXISTS(SELECT * FROM account WHERE Account = '"+ input_username +"');")
    result = query.fetchone()
    if result[0] == 1:
        check_username = 1
    else:
        check_username = 0
        
    query = db.engine.execute("SELECT EXISTS(SELECT * FROM account WHERE Password = '"+ input_password +"');")
    result = query.fetchone()
    if result[0] == 1:
        check_password = 1
    else:
        check_password = 0
    
    return  check_username, check_password


    

def insert_to_database(register_username, register_password):
    
    query = db.engine.execute("SELECT EXISTS(SELECT * FROM account WHERE Account = '"+ register_username +"');")
    result = query.fetchone()
    
    if result[0] == 1:
        return "register failed"
    else:
        db.engine.execute("INSERT INTO account (Account, Password)\nVALUES ('" + register_username +"', '"+ register_password + "');")
        return "ok"



def upload(username):
    

    
    if request.method == 'POST':
        
        file = request.files['file']
        if file:
            global app, db
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            ### process picure's path
            basepath = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
            file_path = os.path.join(basepath, 'upload', secure_filename(file.filename))
            
            file_path = repr(file_path)
            
            print(file_path)
            print(type(file_path))
            reader = loadModel()
            result = recongnize(reader, file_path)
            
            ###
            
            table_option = str(request.form.get("table_names"))
            table_option = table_option.replace('\'', "")
            database_name = username[0:-10]
            db.engine.execute("INSERT INTO " + database_name + "." + table_option + "(Student_Number, Score)\nVALUES('" + result[0] +"', "+ result[1] +");")
    
    database_name = username[0:-10]
    query = db.engine.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = '"+ database_name +"';")
    result = query.fetchall()
    table_options = set()
    

    for item in result:
        table_name = str(' ,'.join(item))
        table_options.add(table_name)
    
    return render_template('upload.html', name = username, options = table_options)

def search(username):
    
    if request.method == 'POST':
        
        database_name = username[0:-10]
        query = db.engine.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = '"+ database_name +"';")
        result = query.fetchall()
        table_options = set()
    
        for item in result:
            table_name = str(' ,'.join(item))
            table_options.add(table_name)
           
        table_option = str(request.form.get("table_names"))
        table_option = table_option.replace('\'', "")
        
        col_names = getName(username, table_option)
        print("ues")
        database_name = username[0:-10]
        datas = db.engine.execute("SELECT * FROM " + database_name + "." + table_option)
        return render_template('search.html', name = username, options = table_options, col_names = col_names, students = datas)
    
    database_name = username[0:-10]
    query = db.engine.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = '"+ database_name +"';")
    result = query.fetchall()
    table_options = set()
    
    for item in result:
        table_name = str(' ,'.join(item))
        table_options.add(table_name)
    
    return render_template('search.html', name = username, options = table_options)

def getName(username, table_option):
    global db
    
    database_name = username[0:-10]
    columns_data = db.engine.execute("SHOW COLUMNS FROM "+ database_name + "." + table_option)
    columns_name = []
    for item in columns_data:
        columns_name.append(item[0])
    return columns_name