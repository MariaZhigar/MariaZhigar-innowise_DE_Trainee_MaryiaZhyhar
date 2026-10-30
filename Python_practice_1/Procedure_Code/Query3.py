from db import get_connection
import json

connection = get_connection()
cursor = connection.cursor()

# age(...)             интервал «от дня рождения до сегодня»
# EXTRACT(YEAR FROM …)  только целые годы (возраст)
# ROUND(..., 2)        округление до 2 знаков
# ::float              обычный float вместо numeric/Decimal (для вывода поставила)
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

# Получить все строки результата запроса (список кортежей)
rows = cursor.fetchall()
# Вывести каждую строку в консоль
for row in rows:
    print(row)

with open("results/largest_age_diff.json", "w", encoding="utf-8") as f:
    data = [{"id": r[0], "name": r[1], "diff_age": r[2]} for r in rows]
    json.dump(data, f, ensure_ascii=False, indent=2)

# Закрыть курсор и соединение с БД
cursor.close()
connection.close()