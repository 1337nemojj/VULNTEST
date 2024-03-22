from flask import Flask, render_template, request, redirect, url_for, jsonify, session
#from flask_basicauth import BasicAuth
import sqlite3
import subprocess


app = Flask(__name__)

# app.config['BASIC_AUTH_USERNAME'] = 'suuser'
# app.config['BASIC_AUTH_PASSWORD'] = 'A1234567a'

# basic_auth = BasicAuth(app)

#bd


def connect_db():
    return sqlite3.connect('users.db')


@app.route('/')
#@basic_auth.required
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    cursor.execute(query)
    user = cursor.fetchone()  
    print(user)
    conn.close() 

    if user is not None:
        session['logged_in'] = True  # Устанавливаем флаг входа в сеансе
        session['username'] = username  # Сохраняем имя пользователя в сеансе
        return redirect(url_for('search'))
    else:
        return 'Неправильное имя пользователя или пароль'
    
# @app.route('/welcome/<username>')
# def welcome(username):
#     return f'Добро пожаловать, {username}!'
@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Удаляем флаг входа из сеанса
    session.pop('username', None)  # Удаляем имя пользователя из сеанса
    return redirect(url_for('home'))


@app.route('/index', methods=['POST', 'GET'])
def index():
    if not session.get('logged_in'):  # Если пользователь не авторизован
        return redirect(url_for('login')) 

    if request.method == 'POST':
        # Уязвимый код для удаленного выполнения команд
        command = request.form['RCE_term']
        result = subprocess.check_output(command, shell=True)
        return result
    
    return render_template('index.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    if not session.get('logged_in'):  # Если пользователь не авторизован
        return redirect(url_for('login'))  # Перенаправляем на страницу входа


    if request.method == 'POST':
        search_term = request.form['search_term']

        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username='" + search_term + "'"
        cursor.execute(query)
        user_found = cursor.fetchone()  
        
        
        print(user_found)
        conn.close()   

        if user_found:
            results = [{'username': search_term}]
        else:
            results = []

        return jsonify(results)

    return render_template('search.html')

if __name__ == '__main__':
    #app.run(host="10.0.2.7", port="5000",  debug=True)
    app.secret_key = 'super_secret_key'
    app.run(host="127.0.0.1", port="5000",  debug=True)