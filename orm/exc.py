from utils import parse_query_to_config
from .model import Table

def build_condition(condition_config: dict):
    if not condition_config:
        return None

    col = condition_config['column']
    op = condition_config['operator']
    val = condition_config['value']

    if op == '=':
        return lambda row: row.get(col) == val
    elif op == '!=':
        return lambda row: row.get(col) != val
    elif op == '<':
        return lambda row: row.get(col) < val
    elif op == '<=':
        return lambda row: row.get(col) <= val
    elif op == '>':
        return lambda row: row.get(col) > val
    elif op == '>=':
        return lambda row: row.get(col) >= val
    else:
        raise ValueError(f"Unsupported operator: {op}")

def execute_query(query: str) -> dict:
    config = parse_query_to_config(query)

    action = config.get("action")
    table_name = config.get("table")
    if not action or not table_name:
        raise ValueError("Query must include action and table")

    table = Table(table_name)
    condition = build_condition(config.get("condition"))

    if action == "insert":
        values = config.get("values")
        if not values:
            raise ValueError("INSERT requires 'values'")
        table.insert(values)
        return {"status": "success", "message": "1 row inserted"}

    elif action == "select":
        result = table.read(where=condition)
        return {"status": "success", "rows": result}

    elif action == "update":
        updates = config.get("set")
        if not updates:
            raise ValueError("UPDATE requires 'set'")
        count = table.update(updates, where=condition)
        return {"status": "success", "updated": count}

    elif action == "delete":
        count = table.delete(where=condition)
        return {"status": "success", "deleted": count}

    else:
        raise ValueError(f"Unknown action: {action}")