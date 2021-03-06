import sqlite3
import json

__connection = None


def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('univer_info.db')
    return __connection


class DB():

    # Создание базы данных
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

        # Забираем данные по группа из файла
        # TODO СДЕЛАТЬ ДИНАМИЧКОЕ ОБНОВЛЕНИЕ ЭТОГО ФАЙЛА
        with open('config/groups-list.json') as f:
            templates = json.load(f)
        f.close()

        _group = templates['groups']

        # Вливание данных из файла в бд
        for i in _group:
            c.execute('INSERT INTO all_group (numberGroup) VALUES (?)', (i,))

        # Сохранение изменений
        conn.commit()

    # Поиск совпадений по группам
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

    def add_users(users_id: int, name_users: str, lastname_users: str, login_users: str, text: str):
        conn = get_connection()
        c = conn.cursor()
        c.execute('INSERT INTO all_users (idUsers,nameUsers,lastNameUsers,logitUsers,textGroup) VALUES (?,?,?,?,?)',
                  (users_id, name_users, lastname_users, login_users, text))
        conn.commit()

    def search_time_lesson(id: int):
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT timeLesson FROM time_lesson WHERE id=?', (id,))
        (res,) = c.fetchone()
        return res

    def get_address(self, keyword: str):
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT nameAddress FROM address WHERE keyWord=?', (keyword,))
        (res,) = c.fetchone()
        return res

    def get_url_address(keyword: str):
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT linkAddress FROM address WHERE keyWord=?', (keyword,))
        (res,) = c.fetchone()
        return res

    def update_group(number_group: str, id_users: int):
        conn = get_connection()
        c = conn.cursor()
        c.execute('UPDATE all_users SET textGroup =? WHERE idUsers=?', (number_group, id_users))
        conn.commit()

    def search_dayWeek(id: int, self):
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT dayWeek FROM day_of_week WHERE id=?', (id,))
        (res,) = c.fetchone()
        return res

    def get_address(keyword: str):
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT nameAddress FROM address WHERE keyWord=?', (keyword,))
        (res,) = c.fetchone()
        return res

    def check_access(a: str, id: int):
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT ' + a + ' FROM access WHERE id_users=?', (id,))
        (res,) = c.fetchone()
        return res

    def select_all_users(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM all_users ')
        (res,) = c.fetchone()
        return res