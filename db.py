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


#Поиск совпадений по группам
def serach_group(number_group: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM all_group WHERE numberGroup=?', (number_group,))
    (res,) = c.fetchone()
    conn.commit()
    return res
