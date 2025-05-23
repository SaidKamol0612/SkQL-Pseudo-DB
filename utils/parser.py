import re

from typing import Dict, Any


def parse_query_to_config(query: str) -> Dict[str, Any]:
    config = {
        "action": None,
        "table": None,
        "values": None,
        "set": None,
        "condition": None,
        "limit": None,
    }

    query = re.sub(r"\s+", " ", query).strip()

    def extract_block(s: str, keyword: str) -> str:
        start = s.find(keyword + "(")
        if start == -1:
            return ""
        i = start + len(keyword) + 1
        count = 1
        while i < len(s) and count > 0:
            if s[i] == "(":
                count += 1
            elif s[i] == ")":
                count -= 1
            i += 1
        return s[start + len(keyword) + 1 : i - 1].strip()

    # --- ASOSIY ---
    asosiym = extract_block(query, "ASOSIY")
    if asosiym:
        # --- INSERT ---
        if asosiym.startswith("QO'SH"):
            match = re.search(r"QO'SH\((\w+),\s*\((.*?)\)\)", asosiym)
            if match:
                config["action"] = "insert"
                config["table"] = match.group(1)
                items = match.group(2).split(",")
                values_dict = {}
                for item in items:
                    item = item.strip()
                    kv_match = re.match(r"'([^']+)'\s*=\s*(.+)", item)
                    if kv_match:
                        key = kv_match.group(1)
                        value = eval(kv_match.group(2).strip())
                        values_dict[key] = value
                    else:
                        values_dict[len(values_dict)] = eval(item)
                config["values"] = values_dict

        # --- SELECT ---
        elif asosiym.startswith("KO'RSAT"):
            match = re.search(r"KO'RSAT\(HAMMASI\s+(\w+)\)", asosiym)
            if match:
                config["action"] = "select"
                config["table"] = match.group(1)

        # --- UPDATE ---
        elif asosiym.startswith("YANGILA"):
            match = re.search(r"YANGILA\((\w+),\s*\((.*?)\)\)", asosiym)
            if match:
                config["action"] = "update"
                config["table"] = match.group(1)
                set_data = {}
                for pair in re.findall(r"'?(\w+)'?\s*=\s*(\d+)", match.group(2)):
                    key, value = pair
                    set_data[key] = int(value)
                config["set"] = set_data

        # --- DELETE ---
        elif asosiym.startswith("O'CHIR"):
            match = re.search(r"O'CHIR\((\w+)\)", asosiym)
            if match:
                config["action"] = "delete"
                config["table"] = match.group(1)

    # --- SHART ---
    shartm = re.search(
        r"SHART\(\s*QAYERDA\((\w+)\s+(KATTAROQ|KICHIKROQ|TENG)\s+(.*?)\)\s*\)", query
    )
    if shartm:
        col, op, val = shartm.groups()
        op_map = {"KATTAROQ": ">", "KICHIKROQ": "<", "TENG": "="}
        config["condition"] = {
            "column": col,
            "operator": op_map.get(op),
            "value": eval(val.strip()),
        }

    # --- CHEKLOV ---
    limitm = re.search(r"CHEKLOV\((\d+)\)", query)
    if limitm:
        config["limit"] = int(limitm.group(1))

    return config


# Example usage

# create_query = "ASOSIY(QO'SH(employees, ('name'='Said', 'age'=18, 'salary'=1000)))"
# read_query = "ASOSIY(KO'RSAT(HAMMASI employees)) CHEKLOV(10)"
# update_query = "ASOSIY(YANGILA(employees, ('salary'=1001, 'age'=19))) SHART(QAYERDA(salary KICHIKROQ 1000))"
# delete_query = "ASOSIY(O'CHIR(employees)) SHART(QAYERDA(age KICHIKROQ 18))"

# print("SST Queries:")
# print(create_query)
# print(read_query)
# print(update_query)
# print(delete_query)

# print("\n\nParsed Configurations:")
# print(parse_query_to_config(create_query))
# print(parse_query_to_config(read_query))
# print(parse_query_to_config(update_query))
# print(parse_query_to_config(delete_query))
