import os
import json
from typing import List, Tuple, Dict, Any, Callable, Optional

DATA_DIR = "data"
SCHEMA_FILE = os.path.join(DATA_DIR, "schema.json")

def load_schema() -> dict:
    if os.path.exists(SCHEMA_FILE):
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_schema(schema: dict):
    with open(SCHEMA_FILE, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=4)

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def create_file(filename: str, tablename: str):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({tablename: []}, f, indent=4)

def parse_condition(where: Optional[Callable[[Dict[str, Any]], bool] | Dict[str, Any]]):
    if where is None:
        return lambda row: True
    if callable(where):
        return where
    if isinstance(where, dict):
        return lambda row: all(row.get(k) == v for k, v in where.items())
    raise TypeError("Condition must be a callable or a dict")

class Table:
    def __init__(self, tablename: str, columns: Optional[List[Tuple[str, type]]] = None, primary_key: str = "id"):
        ensure_data_dir()
        self.tablename = tablename
        self.filename = f"{tablename}.json"
        self.primary_key = primary_key

        schema = load_schema()
        if columns is None:
            if tablename not in schema:
                raise ValueError(f"Schema not found for table: {tablename}")
            self.columns = [(name, eval(tp)) for name, tp in schema[tablename]]
        else:
            if primary_key not in [col[0] for col in columns]:
                columns.insert(0, (primary_key, int))
            self.columns = columns
            schema[tablename] = [(name, col_type.__name__) for name, col_type in self.columns]
            save_schema(schema)

        create_file(self.filename, self.tablename)
        self.auto_increment = self._get_max_id() + 1

    def _get_max_id(self) -> int:
        data = self._load()
        rows = data.get(self.tablename, [])
        return max((row.get(self.primary_key, 0) for row in rows), default=0)

    def _register_schema(self):
        schema_data = {}
        if os.path.exists(SCHEMA_FILE):
            with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
                schema_data = json.load(f)

        if self.tablename not in schema_data:
            schema_data[self.tablename] = [
                (name, typ.__name__) for name, typ in self.columns
            ]
            with open(SCHEMA_FILE, "w", encoding="utf-8") as f:
                json.dump(schema_data, f, indent=4)

    def _load_schema(self) -> Optional[List[Tuple[str, type]]]:
        if not os.path.exists(SCHEMA_FILE):
            return None
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            schema_data = json.load(f)
        if self.tablename in schema_data:
            return [(name, eval(tp)) for name, tp in schema_data[self.tablename]]
        return None

    def insert(self, record: dict) -> dict:
        validated_record = {self.primary_key: self.auto_increment}
        self.auto_increment += 1

        for name, _ in self.columns:
            if name != self.primary_key and name in record:
                validated_record[name] = record[name]

        data = self._load()
        data[self.tablename].append(validated_record)
        self._save(data)
        return validated_record

    def read(self, where: Optional[Callable[[Dict[str, Any]], bool]] = None) -> List[Dict[str, Any]]:
        data = self._load().get(self.tablename, [])
        return data if where is None else [row for row in data if where(row)]

    def update(self, updates: Dict[str, Any], where=None) -> int:
        where = parse_condition(where)
        data = self._load()
        updated_count = 0

        for row in data[self.tablename]:
            if where(row):
                for key, value in updates.items():
                    if key in row:
                        row[key] = value
                updated_count += 1

        self._save(data)
        return updated_count

    def delete(self, where=None) -> int:
        where = parse_condition(where)
        data = self._load()
        original_len = len(data[self.tablename])
        data[self.tablename] = [row for row in data[self.tablename] if not where(row)]
        deleted = original_len - len(data[self.tablename])
        self._save(data)
        return deleted

    def _load(self) -> Dict[str, Any]:
        path = os.path.join(DATA_DIR, self.filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data: Dict[str, Any]):
        path = os.path.join(DATA_DIR, self.filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def __repr__(self):
        return f"Table({self.tablename}, Columns: {self.columns}, Primary Key: {self.primary_key})"

    def __str__(self):
        cols = ", ".join(col[0] for col in self.columns)
        return f"Table: {self.tablename}, Columns: {cols}, Primary Key: {self.primary_key}"
