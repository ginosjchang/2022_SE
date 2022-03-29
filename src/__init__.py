from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

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
    app.add_url_rule('/home/<username>','home', home)
    app.add_url_rule('/upload/<username>', 'upload', upload, methods=['GET', 'POST'])
    app.add_url_rule('/search/<username>', 'search', search)
    return app

def login():
    if request.method == 'POST':
        return redirect(url_for('home', username=request.form['account']))
    return render_template('signin.html')

def home(username):
    return render_template('home.html', name=username)

def upload(username):
    if request.method == 'POST':
        file = request.files['file']
        if file:
            global app, db
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    columns_data = db.engine.execute("SHOW FIELDS FROM test")
    columns_name = {i['Field'] for i in columns_data if i['Field'] != 'ID'}
    return render_template('upload.html', name=username, options=columns_name)

def search(username):
    return render_template('search.html', name=username)