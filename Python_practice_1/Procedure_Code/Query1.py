from db import get_connection
import json

connection = get_connection()
cursor = connection.cursor()

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

# Получить все строки результата запроса (список кортежей)
rows = cursor.fetchall()
# Вывести каждую строку в консоль
for row in rows:
    print(row)

with open("results/rooms_students_count.json", "w", encoding="utf-8") as f:
    data = [{"id": r[0], "name": r[1], "students_count": r[2]} for r in rows]
    # `nsure_ascii=False` — не экранировать русские буквы в `\uXXXX`.
    # `indent=2` — красивые отступы
    json.dump(data, f, ensure_ascii=False, indent=2)

# Закрыть курсор и соединение с БД
cursor.close()
connection.close()