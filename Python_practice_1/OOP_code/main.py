import argparse  # флаги из командной строки

from db import Database
from load_data import DataLoader
from queries import QueryRunner
from exporter import JsonExporter

# --- CLI ---
parser = argparse.ArgumentParser()
parser.add_argument("--students", required=True, help="путь к students.json")
parser.add_argument("--rooms", required=True, help="путь к rooms.json")

parser.add_argument("--format", choices=["json"], default="json", help="формат вывода")
args = parser.parse_args()

db = Database().connect()
try:
    DataLoader(db).load(args.rooms, args.students)

    q = QueryRunner(db)
    exp = JsonExporter()  # по умолчанию папка results/

    exp.save("rooms_students_count.json", q.rooms_students_count(),
             ["id", "name", "students_count"])
    exp.save("rooms_avg_age_asc.json", q.rooms_avg_age_asc(),
             ["id", "name", "avg_age"])
    exp.save("rooms_age_diff.json", q.rooms_age_diff(),
             ["id", "name", "age_diff"])
    exp.save("rooms_mixed_sex.json", q.rooms_mixed_sex(),
             ["id", "name"])

    print("Готово → папка results/")
finally:
    # даже при ошибке соединение лучше закрыть
    db.close()
