from db import get_connection
import json

connection = get_connection()
cursor = connection.cursor()

# COUNT(DISTINCT s.sex) - количество уникальных полов должно быть равным 2
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

# Получить все строки результата запроса (список кортежей)
rows = cursor.fetchall()
# Вывести каждую строку в консоль
for row in rows:
    print(row)

with open("results/mixed_sex_rooms.json", "w", encoding="utf-8") as f:
    data = [{"id": r[0], "name": r[1]} for r in rows]
    json.dump(data, f, ensure_ascii=False, indent=2)

# Закрыть курсор и соединение с БД
cursor.close()
connection.close()