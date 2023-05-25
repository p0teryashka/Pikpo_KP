# Подключаем объект приложения Flask из __init__.py
from labapp import app
# Подключаем библиотеку для "рендеринга" html-шаблонов из папки templates
from flask import render_template, make_response, request, jsonify, redirect, url_for

from labapp.repository import sql_api   # подключаем модуль с реализацией бизнес-логики обработки запросов
from labapp import static

"""
    Модуль регистрации обработчиков маршрутов, т.е. здесь реализуется обработка запросов
    при переходе пользователя на определенные адреса веб-приложения
"""


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def render_index():
    """ Обработка запроса к индексной странице """
    # Пример вызова метода с выборкой данных из БД и вставка полученных данных в html-шаблон
    data_from_table = sql_api.select_all_from_players()
    # "рендеринг" (т.е. вставка динамически изменяемых данных) в шаблон index.html и возвращение готовой страницы
    return render_template('index.html',
                           title=static.TITLE,
                           page_name='О ВОЛЕЙБОЛИСТАХ',
                           navmenu=static.navmenu,
                           data_from_table=data_from_table)


@app.route('/search', methods=['POST'])
def search_data():
    """ Функция обработки поискового запроса """
    lastname = request.form.get('searchInput')      # получаем ввод из поисковой формы
    data_from_table = sql_api.select_all_from_players_by_lastname(lastname)
    # "рендеринг" (т.е. вставка динамически изменяемых данных) в шаблон index.html и возвращение готовой страницы
    return render_template('index.html',
                           title=static.TITLE,
                           page_name='О ВОЛЕЙБОЛИСТАХ',
                           navmenu=static.navmenu,
                           data_from_table=data_from_table)


@app.route('/add', methods=['GET'])
def render_add_form():
    """ Рендеринг шаблона с формой добавления данных add.html """
    return render_template('add.html',
                           title=static.TITLE,
                           page_name='ДОБАВЛЕНИЕ',
                           navmenu=static.navmenu)


@app.route('/add', methods=['POST'])
def add_data():
    """ Эта функция принимает данные, отправляемые формой со страницы add.html """
    name = request.form.get('nameInput')
    lastname = request.form.get('lastnameInput')
    age = int(request.form.get('ageInput'))  # форма все данные передаёт в строке, если необходимо, преобразуем в int
    height = int(request.form.get('heightInput'))      # форма все данные передаёт в строке, если необходимо, преобразуем в int
    # передаём полученные данные из формы в функцию добавления записи в БД
    sql_api.insert_into_players(name, lastname, age, height)
    # переадресуем пользователя обратно на стартовую страницу
    return redirect('/')


@app.route('/edit/<int:player_id>', methods=['GET'])
def render_edit_form(player_id: int):
    """ Рендеринг шаблона с формой редактирования данных add.html """
    data_for_edit_form = sql_api.select_one_player_by_id(player_id)   # получаем данные автомобиля по идентификатору, чтобы подставить в форму редактирования
    return render_template('edit.html',
                           title=static.TITLE,
                           page_name='РЕДАКТИРОВАНИЕ',
                           data_id=player_id,
                           edit_data=data_for_edit_form,
                           navmenu=static.navmenu)


@app.route('/edit/<int:player_id>', methods=['POST'])
def edit_data(player_id: int):
    """ Эта функция принимает данные, отправляемые формой со страницы edit.html """
    name = request.form.get('nameInput')
    lastname = request.form.get('lastnameInput')
    age = int(request.form.get('ageInput'))      # форма все данные передаёт в строке, если необходимо, преобразуем в int
    height = int(request.form.get('heightInput'))
    # передаём полученные данные из формы в функцию редактирования записи в БД
    sql_api.update_players_by_id(player_id, name, lastname, age, height)
    # переадресуем пользователя обратно на стартовую страницу
    return redirect('/')


@app.route('/delete/<int:player_id>', methods=['GET'])
def delete_data(player_id: int):
    """ Удаляем запись в БД по идентификатору """
    sql_api.delete_player_by_id(player_id)
    return redirect('/')


@app.route('/notfound', methods=['GET'])
def not_found_html():
    """ Возврат html-страницы с кодом 404 (Не найдено) """
    return render_template('404.html', title='404', err={'error': 'Not found', 'code': 404})


def bad_request():
    """ Формирование json-ответа с ошибкой 400 протокола HTTP (Неверный запрос) """
    return make_response(jsonify({'message': 'Bad request !'}), 400)
