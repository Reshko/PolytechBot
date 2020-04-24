import sqlite3
import json

__connection = None

#Создание базы данных
def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('univer_info.db')
    return __connection


def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS all_group')

    c.execute('''
        CREATE TABLE IF NOT EXISTS all_group(
            id      INTEGER PRIMARY KEY,
            numberGroup   TEXT NOT NULL
        )
    ''')

    #Забираем данные по группа из файла
    #TODO СДЕЛАТЬ ДИНАМИЧКОЕ ОБНОВЛЕНИЕ ЭТОГО ФАЙЛА
    with open('groups-list.json') as f:
        templates = json.load(f)
    f.close()

    _group = templates['groups']

    #Вливание данных из файла в бд
    for i in _group:
        c.execute('INSERT INTO all_group (numberGroup) VALUES (?)', (i,))

    # Сохранение изменений
    conn.commit()

def make_table_users():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS all_users(
            id      INTEGER PRIMARY KEY,
            idUsers   INTEGER NOT NULL,
            textGroup TEXT NOT NULL
        )
    ''')

    conn.commit()

#Поиск совпадений по группам
def serach_group(number_group: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM all_group WHERE numberGroup=?', (number_group,))
    (res,) = c.fetchone()
    return res

def count_group(id_users: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM all_users WHERE idUsers=?', (id_users,))
    (res,) = c.fetchone()
    return res

def search_users(id_users: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT textGroup FROM all_users WHERE idUsers=?', (id_users,))
    (res,) = c.fetchone()
    return res

def add_users(users_id: int,text: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO all_users (idUsers,textGroup) VALUES (?,?)',(users_id,text))
    conn.commit()



