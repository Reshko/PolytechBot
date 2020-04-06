import sqlite3
import json

__connection = None


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

    with open('groups-list.json') as f:
        templates = json.load(f)
    f.close()

    _group = templates['groups']

    for i in _group:
        c.execute('INSERT INTO all_group (numberGroup) VALUES (?)', (i,))

    # Сохранение изменений
    conn.commit()


def add_message(user_id: int, text: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO all_group (user_id, text) VALUES (?, ?)', (user_id, text))
    conn.commit()


def serach_group(number_group: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM all_group WHERE numberGroup=?', (number_group,))
    (res,) = c.fetchone()
    conn.commit()
    return res

