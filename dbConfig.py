import sqlite3

__connection = None

#Создание базы данных
def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('univer_info.db')
    return __connection

def make_table_users():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS all_users(
            id      INTEGER PRIMARY KEY,
            idUsers   INTEGER NOT NULL,
            nameUsers TEXT NOT NULL,
            lastNameUsers TEXT NOT NULL,
            logitUsers TEXT,
            textGroup TEXT NOT NULL
        )
    ''')

    conn.commit()

def make_table_address():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS address(
            id      INTEGER PRIMARY KEY,
            keyWord TEXT NOT NULL,
            nameAddress   TEXT NOT NULL,
            linkAddress TEXT NOT NULL
        )
    ''')

    conn.commit()

def time_lesson():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS time_lesson(
            id      INTEGER PRIMARY KEY,
            timeLesson   TEXT NOT NULL
        )
    ''')

    conn.commit()

