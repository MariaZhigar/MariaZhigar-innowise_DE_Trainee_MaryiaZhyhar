from db import get_connection


connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_students_room ON students(room);
               """)

connection.commit()

cursor.close()
connection.close()