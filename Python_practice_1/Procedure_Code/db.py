# db.py
import psycopg2


def get_connection():
    return psycopg2.connect(
        dbname='rooms_hw',
        user='admin',
        password='admin123',
        host='localhost',
        port='5432',
    )