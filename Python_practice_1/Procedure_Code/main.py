import argparse  # разбор флагов из командной строки
from pathlib import Path
import json

from load_data import load_data  # функция загрузки JSON в БД
from db import get_connection

# создаём парсер аргументов
parser = argparse.ArgumentParser()

# --students PATH  (обязательный путь к students.json)
parser.add_argument("--students", required=True, help="путь к students.json")
# --rooms PATH  (обязательный путь к rooms.json)
parser.add_argument("--rooms", required=True, help="путь к rooms.json")
# --format json  (по умолчанию json)
parser.add_argument("--format", choices=["json"], default="json", help="формат вывода")

# читаем флаги из терминала в args
args = parser.parse_args()

connection = get_connection()
cursor = connection.cursor()

cursor.execute("TRUNCATE students, rooms RESTART IDENTITY CASCADE;")
connection.commit()

# загружаем данные в Postgres по путям из CLI
load_data(args.rooms, args.students)

# Создаёт папку results в текущей директории. exist_ok=True — не падать с ошибкой, если она уже есть.
Path("results").mkdir(exist_ok=True)

# --- 1. кол-во студентов по комнатам ---
cursor.execute("""
   SELECT 
            r.id, 
            r.name, 
            COUNT(s.id) AS students_count
        FROM 
            rooms AS r
        LEFT JOIN students AS s 
            ON r.id = s.room
        GROUP BY
            r.id, 
            r.name
        ORDER BY 
            students_count DESC;
""")
rows = cursor.fetchall()
data = [{"id": r[0], "name": r[1], "students_count": r[2]} for r in rows]
with open("results/rooms_students_count.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
# --- 2. топ-5 комнат с наименьшим средним возрастом ---
cursor.execute("""
    SELECT 
            r.id, 
            r.name, 
            ROUND(AVG(EXTRACT(YEAR FROM age(current_date, s.birthday))), 2)::float AS average_age
        FROM 
            rooms AS r
        INNER JOIN students AS s 
            ON r.id = s.room
        GROUP BY
            r.id, 
            r.name
        ORDER BY 
            average_age
        LIMIT 5;
""")
rows = cursor.fetchall()
data = [{"id": r[0], "name": r[1], "avg_age": r[2]} for r in rows]
with open("results/rooms_avg_age_asc.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
# --- 3. топ-5 комнат с наибольшим разбросом возраста ---
cursor.execute("""
    SELECT 
            r.id, 
            r.name,  
            ROUND(MAX(EXTRACT(YEAR FROM age(current_date, s.birthday))) - MIN(EXTRACT(YEAR FROM age(current_date, s.birthday))))::float AS diff_age
        FROM 
            rooms AS r
        INNER JOIN students AS s 
            ON r.id = s.room
        GROUP BY
            r.id, 
            r.name
        ORDER BY 
            diff_age DESC
        LIMIT 5;
""")
rows = cursor.fetchall()
data = [{"id": r[0], "name": r[1], "age_diff": r[2]} for r in rows]
with open("results/rooms_age_diff.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
# --- 4. комнаты, где живут и M, и F ---
cursor.execute("""
    SELECT 
            r.id, 
            r.name
        FROM 
            rooms AS r
        INNER JOIN students AS s 
            ON r.id = s.room
        GROUP BY
            r.id, 
            r.name
        HAVING 
            COUNT(DISTINCT s.sex) = 2
""")
rows = cursor.fetchall()
data = [{"id": r[0], "name": r[1]} for r in rows]
with open("results/rooms_mixed_sex.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
cursor.close()
connection.close()
print("готово → папка results/")