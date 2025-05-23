# SkQL (Saidkamol Query Language)

**SkQL** is a domain-specific query language inspired by SQL and adapted to Uzbek language structure. It is designed for basic CRUD operations on a JSON-like database: create, read, update, and delete records.

Each query in SkQL consists of sections:

- `ASOSIY(...)` — main operation (`QO'SH`, `KO'RSAT`, `YANGILA`, `O'CHIR`)
- `SHART(...)` — condition (`QAYERDA`)
- `CHEKLOV(...)` — limit

---

## 🔨 Create a new record (CREATE)

### SkQL:

```skql
ASOSIY(QO'SH(employees, ('name'='Said', 'age'=18, 'salary'=1000)))
```

### SQL:

```sql
INSERT INTO employees VALUES ('Said', 18, 1000);
```

## 📖 Read records (READ)

### SkQL:

```skql
ASOSIY(KO'RSAT(HAMMASI employees))
```

### SQL:

```sql
SELECT * FROM employees;
```

## ✏️ Update records (UPDATE)

### SkQL:

```skql
ASOSIY(YANGILA(employees, ('salary'=1001, 'age'=19))) SHART(QAYERDA(salary KICHIKROQ 1000))
```

## SQL:

```sql
UPDATE employees SET salary = 1001, age = 19 WHERE salary < 1000;
```

## 🗑️ Delete records (DELETE)

### SkQL:
```skql
ASOSIY(O'CHIR(employees)) SHART(QAYERDA(age KICHIKROQ 18))
```

### SQL:
```sql
DELETE FROM employees WHERE age < 18;
```

## 📦 Supported Commands and Operators
| SkQL Command    | SQL Equivalent | Description                 |
| --------------- | -------------- | --------------------------- |
| QO'SH           | INSERT         | Add a new record            |
| KO'RSAT HAMMASI | SELECT \*      | Retrieve all records        |
| YANGILA         | UPDATE         | Update records              |
| O'CHIR          | DELETE         | Delete records              |
| QAYERDA         | WHERE          | Condition                   |
| KICHIKROQ       | <              | Less than                   |
| KATTAROQ        | >              | Greater than                |
| TENG            | =              | Equals                      |
| CHEKLOV         | LIMIT          | Limit the number of results |
