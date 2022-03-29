from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './upload'

def create_app():
    app = Flask(__name__)
    global UPLOAD_FOLDER
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.add_url_rule('/','login', login, methods=['GET', 'POST'])
    app.add_url_rule('/home/<username>','home', home)
    app.add_url_rule('/upload/<username>', 'upload', function, methods=['GET', 'POST'])
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
            filename = secure_filename(file.filename)
            global UPLOAD_FOLDER
            file.save(os.path.join(UPLOAD_FOLDER, filename))
    return render_template('function.html', name=username)

def search(username):
    return render_template('search.html', name=username)