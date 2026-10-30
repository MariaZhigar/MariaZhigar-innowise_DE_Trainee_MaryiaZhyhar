import json
from db import Database


class DataLoader:
    """Загрузка JSON в таблицы. Берёт уже открытое соединение из Database."""

    def __init__(self, db: Database):
        self.db = db

    def load(self, rooms_path, students_path):
        cur = self.db.cursor

        # иначе при втором запуске упрёмся в duplicate key по PRIMARY KEY
        # students первым — из-за FK на rooms
        cur.execute("TRUNCATE students, rooms RESTART IDENTITY CASCADE;")
        self.db.commit()

        # IF NOT EXISTS — ок, если таблицы уже создавали раньше
        cur.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INT PRIMARY KEY,
            name VARCHAR(20) NOT NULL
        );
        CREATE TABLE IF NOT EXISTS students (
            id INT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            birthday DATE,
            room INT REFERENCES rooms(id),
            sex CHAR(1) CHECK (sex IN ('M', 'F'))
        );
        """)
        self.db.commit()

        # пути приходят из CLI (--rooms / --students)
        with open(rooms_path, "r", encoding="utf-8") as f:
            rooms = json.load(f)
        for item in rooms:
            cur.execute(
                "INSERT INTO rooms (id, name) VALUES (%s, %s)",
                (item.get("id"), item.get("name")),
            )
        self.db.commit()

        with open(students_path, "r", encoding="utf-8") as f:
            students = json.load(f)
        for item in students:
            # %s — плейсхолдеры psycopg2, значения отдельно
            cur.execute(
                "INSERT INTO students (id, name, birthday, room, sex) VALUES (%s, %s, %s, %s, %s)",
                (item.get("id"), item.get("name"), item.get("birthday"),
                 item.get("room"), item.get("sex")),
            )
        self.db.commit()
