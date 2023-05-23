import requests
from flask import Flask, render_template, request, redirect
import psycopg2 #импорт всех нужных библиотек

app = Flask(__name__) #создаётся приложение Фласк

conn = psycopg2.connect(database="service_db", #подключение к базе данных
                        user="postgres",
                        password="Al08042005",
                        host="localhost",
                        port="5432")

cursor = conn.cursor() #подсоединение курсора к базе данных


@app.route('/login/', methods=['POST', 'GET']) #декоратор
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if not username:
                return render_template('login.html', error="Введите логин")
            if not password:
                return render_template('login.html', error="Введите пароль")
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())

            return render_template('account.html', full_name=records[0][1], username=records[0][2], password=records[0][3])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name') #приём данных из формы
        login = request.form.get('login') #приём данных из формы
        password = request.form.get('password') #приём данных из формы

        if not name: #проверка на заполнение поля
            return render_template('registration.html', error="Введите имя") #вывод ошибки (registration.html - страница, на которой выводится ошибка)
        if not password: #проверка на заполнение поля
            return render_template('registration.html', error="Введите пароль") #вывод ошибки
        if not login: #проверка на заполнение поля
            return render_template('registration.html', error="Введите логин") #вывод ошибки

        try: #если все поля заполнены, то
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                           (str(name), str(login), str(password)))  #идёт добавление записи с именем, логином и паролем в базу данных в таблицу service.users
            conn.commit() #делается коммит
            return redirect('/login/') #идёт перенаправление пользователя на страницу с авторизацией
        except: #если такой пользователь уже зарегистрирован
            conn.commit()
            return render_template('registration.html', error="Пользователь существует")




    return render_template('registration.html')
