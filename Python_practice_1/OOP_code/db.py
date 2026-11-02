import psycopg2  # драйвер Postgres для Python


class Database:
    """Одно место для подключения к БД — чтобы не копировать connect по всем файлам."""

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        # параметры как в Docker-контейнере (rooms_hw)
        self.connection = psycopg2.connect(
            dbname='rooms_hw',
            user='admin',
            password='admin123',
            host='localhost',
            port='5432',
        )
        # через курсор дальше шлём SQL
        self.cursor = self.connection.cursor()
        return self

    def commit(self): 
        self.connection.commit()

    def close(self):
        # закрываем в конце, даже если что-то упало (см. finally в main)
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
