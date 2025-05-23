# Pseudo-DB with SkQL (Saidkamol Query Language)

This is a lightweight, file-based pseudo-database system written in Python.  
It uses JSON for storage and includes a custom DSL (Domain-Specific Language)  
inspired by Uzbek to perform SQL-like operations.

## ✨ Features

- JSON-based data storage
- Custom DSL for queries in Uzbek syntax (SST)
- Basic ORM-like API for creating, reading, updating, and deleting records
- Automatic schema registration and persistence

## 📦 Example

```python
from exc import execute_query

query = "ASOSIY(QO'SH(employees, ('name'='Said', 'age'=18, 'salary'=1000)))"
execute_query(query)
```

## 📁 Storage

- All data is stored as `.json` in the `data/` directory.
- Table schemas are stored in `data/schema.json` and are automatically loaded when tables are created or accessed.

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/SaidKamol0612/SkQL-Pseudo-DB.git
   cd SkQL-Pseudo-DB
   ```
2. Run your queries using custom DSL:

   ```python
   from exc import execute_query

   execute_query("ASOSIY(QO'SH(employees, ('name'='Said', 'age'=18, 'salary'=1000)))")
   ```

3. All data will be automatically saved as `.json` files in the `data/` directory, and schemas tracked in `data/schema.json`.

### Enjoy building your own minimal DB engine with an Uzbek flair!
