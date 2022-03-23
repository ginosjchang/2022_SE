from flask import Flask, render_template, request, redirect, url_for

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/','login', login, methods=['GET', 'POST'])
    app.add_url_rule('/home/<username>','home', home)
    app.add_url_rule('/function/<username>', 'function', function)
    app.add_url_rule('/search/<username>', 'search', search)
    return app

def login():
    if request.method == 'POST':
        return redirect(url_for('home', username=request.form['account']))
    return render_template('signin.html')

def home(username):
    return render_template('home.html', name=username)

def function(username):
    return render_template('function.html', name=username)

def search(username):
    return render_template('search.html', name=username)