from db import get_connection

__connection = None

#Создание базы данных

class MakeDb():
    def make_table_users(self):
        conn = get_connection()
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS all_users(
                id      INTEGER PRIMARY KEY,
                idUsers   INTEGER NOT NULL,
                nameUsers TEXT,
                lastNameUsers TEXT,
                logitUsers TEXT,
                textGroup TEXT NOT NULL
            )
        ''')

        conn.commit()

    def make_table_address(self):
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

    def time_lesson(self):
        conn = get_connection()
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS time_lesson(
                id      INTEGER PRIMARY KEY,
                timeLesson   TEXT NOT NULL
            )
        ''')

        conn.commit()

    def droptp(self):
        conn = get_connection()
        c = conn.cursor()

        c.execute('''
                    DROP ALL TABLES
                ''')

        conn.commit()

    def dayOfWeek(self):
        conn = get_connection()
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS day_of_week(
                id      INTEGER PRIMARY KEY,
                dayWeek   TEXT NOT NULL
            )
        ''')

        conn.commit()

    def make_info(self):
        conn = get_connection()
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS information2(
                id      INTEGER PRIMARY KEY,
                buttonnName   TEXT NOT NULL,
                numberPhone TEXT NOT NULL,
                addPhoneNumber TEXT,
                email TEXT NOT NULL
            )
        ''')

        conn.commit()




if __name__ == '__main__':
    MakeDb.make_info(None)