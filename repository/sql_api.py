from typing import List

from config import DB_URL       # параметры подключения к БД из модуля конфигурации config.py
from .connectorfactory import SQLStoreConnectorFactory

from .connector import StoreConnector


"""
    В данном модуле реализуется API (Application Programming Interface)
    для взаимодействия с БД с помощью объектов-коннекторов.
    
    ВАЖНО! Методы должны быть названы таким образом, чтобы по названию
    можно было понять выполняемые действия.
"""


def select_all_from_players() -> List[tuple]:
    """ Вывод списка автомобилей с сортировкой по количеству (age) в порядке убывания (DESC) """
    connector = open_connection()
    query = f"SELECT * FROM players ORDER BY age DESC"
    result = connector.execute(query).fetchall()
    connector.end_transaction()
    connector.close()
    return result


def select_one_player_by_id(player_id: int) -> tuple:
    """ Получение записи об автомобиле по идентификатору записи """
    connector = open_connection()
    query = f"SELECT * FROM players WHERE id = {player_id}"
    result = connector.execute(query).fetchone()
    connector.end_transaction()
    connector.close()
    return result


def select_all_from_players_by_lastname(lastname) -> List[tuple]:
    """ Поиск автомобилей, используя полное или частичное совпадение искомой строки
        в наименовании производителя (lastname).
        Значения lastname всегда приводим к заглавным буквам, чтобы поиск не зависел от типа символов """
    connector = open_connection()
    query = f"SELECT * FROM players where lastname LIKE '%{lastname.upper()}%'"
    result = connector.execute(query).fetchall()
    connector.end_transaction()
    connector.close()
    return result


def insert_into_players(name: str, lastname: str, age: int, height: int):
    """ Вставка новой записи в таблицу players """
    connector = open_connection()
    query = f"INSERT INTO players (name, lastname, age, height) VALUES ('{name}', '{lastname.upper()}', '{age}', '{height}')"
    result = connector.execute(query)
    connector.end_transaction()
    connector.close()
    return result


def update_players_by_id(player_id: int, name: str = "none", lastname: str = "none", age: int = 0, height: int = 0):
    """ Обновление значений записи об автомобиле по идентификатору.
        В функции установлены значения по умолчанию, в случае, если поля формы были незаполнены"""
    connector = open_connection()
    query = f"UPDATE players SET name = '{name}', lastname = '{lastname.upper()}', age = {age}, height = {height} WHERE id = {player_id}"
    result = connector.execute(query)
    connector.end_transaction()
    connector.close()
    return result


def delete_player_by_id(player_id: int) -> List[tuple]:
    """ Удаление записи в таблице по идентификатору """
    connector = open_connection()
    query = f"DELETE FROM players where id = {player_id}"
    result = connector.execute(query)
    connector.end_transaction()
    connector.close()
    return result


def open_connection() -> StoreConnector:
    """ Функция открывает соединение для выполнения запросов """
    connector = SQLStoreConnectorFactory().get_connector(DB_URL)  # инициализируем соединение
    connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
    return connector


