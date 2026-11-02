from db import Database


class QueryRunner:
    """Все аналитические SELECT здесь."""

    def __init__(self, db: Database):
        self.db = db

    def rooms_students_count(self):
        # LEFT JOIN — комнаты без студентов тоже попадут (count = 0)
        self.db.cursor.execute("""
            SELECT r.id, r.name, COUNT(s.id) AS students_count
            FROM rooms AS r
            LEFT JOIN students AS s ON r.id = s.room
            GROUP BY r.id, r.name
            ORDER BY students_count DESC
        """)
        return self.db.cursor.fetchall()

    def rooms_avg_age_asc(self):
        self.db.cursor.execute("""
            SELECT r.id, r.name,
                   ROUND(AVG(EXTRACT(YEAR FROM age(current_date, s.birthday))), 2)::float AS average_age
            FROM rooms AS r
            INNER JOIN students AS s ON r.id = s.room
            GROUP BY r.id, r.name
            ORDER BY average_age
            LIMIT 5
        """)
        return self.db.cursor.fetchall()

    def rooms_age_diff(self):
        # разброс = max возраст − min возраст в комнате
        self.db.cursor.execute("""
            SELECT r.id, r.name,
                   ROUND(MAX(EXTRACT(YEAR FROM age(current_date, s.birthday)))
                       - MIN(EXTRACT(YEAR FROM age(current_date, s.birthday))))::float AS diff_age
            FROM rooms AS r
            INNER JOIN students AS s ON r.id = s.room
            GROUP BY r.id, r.name
            ORDER BY diff_age DESC
            LIMIT 5
        """)
        return self.db.cursor.fetchall()

    def rooms_mixed_sex(self):
        # HAVING после GROUP BY: оставляем комнаты, где два разных пола
        self.db.cursor.execute("""
            SELECT r.id, r.name
            FROM rooms AS r
            INNER JOIN students AS s ON r.id = s.room
            GROUP BY r.id, r.name
            HAVING COUNT(DISTINCT s.sex) = 2
        """)
        return self.db.cursor.fetchall()
