import json  # чтение/запись JSON-файлов
from db import get_connection

def load_data(rooms_path, students_path):
    try:
        connection = get_connection()
        # Без курсора просто подключился, а команды некуда писать.
        cursor = connection.cursor()

        # Выполнение SQL-запроса "Создание таблиц" DDL
        # При повторном запуске CREATE упадёт. Решение — IF NOT EXISTS
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS rooms (
            id			INT PRIMARY KEY,
            name 		VARCHAR(20) NOT NULL
        );
    
        CREATE TABLE IF NOT EXISTS students (
            id 			INT PRIMARY KEY,
            name 		VARCHAR(50) NOT NULL,
            birthday 	DATE,
            room 		INT REFERENCES rooms(id),
            sex  		CHAR(1) CHECK (sex IN ('M', 'F'))
        );
        """)
        # зафиксировать изменения в БД
        connection.commit()

        # Чтение JSON-файла rooms.json
        with open('rooms.json', 'r', encoding='utf-8') as f:
            rooms = json.load(f)  # Преобразует JSON в список словарей Python

        # Вставка данных в базу
        # Один круг цикла = одна строка в таблице
        for item in rooms:
            cursor.execute(
        '''
                INSERT INTO rooms (id, name) 
                VALUES (%s, %s    )
              ''',
                # item.get('ключ') - взять из словаря значение по ключу
            (item.get('id'), item.get('name')),
            )
        connection.commit()

        # Чтение JSON-файла students.json
        with open('students.json', 'r', encoding='utf-8') as f:
            students = json.load(f)  # Преобразует JSON в список словарей Python

        for item in students:
            cursor.execute(
        '''
                INSERT INTO students (id, name, birthday, room, sex) 
                VALUES (%s, %s, %s, %s, %s)
              ''',
            # item.get('ключ') - взять из словаря значение по ключу
        (item.get('id'), item.get('name'), item.get('birthday'), item.get('room'), item.get('sex'))
            )
        connection.commit()

    except Exception as error:
        print('Ошибка при работе с PostgreSQL:', error)

    finally:
        # 5. Закрытие курсора и соединения
        if cursor:
            cursor.close()
        if connection:
            connection.close()