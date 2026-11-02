import json
from pathlib import Path


class JsonExporter:
    """Пишет ответы запросов в JSON — отдельно от SQL, чтобы не мешать роли."""

    def __init__(self, results_dir="results"):
        self.dir = Path(results_dir)
        # если папки ещё нет — создаём; если есть — не ругаемся
        self.dir.mkdir(exist_ok=True)

    def save(self, filename, rows, keys):
        # rows — это кортежи из fetchall, keys — имена полей для JSON
        data = [dict(zip(keys, row)) for row in rows]
        with open(self.dir / filename, "w", encoding="utf-8") as f:
            # ensure_ascii=False — кириллица читаемая, indent — красиво в файле
            json.dump(data, f, ensure_ascii=False, indent=2)
