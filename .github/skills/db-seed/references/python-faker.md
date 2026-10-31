# Python (faker) Seed Scripts

A reproducible Python seeder built on the `faker` library. It works for both SQL Server (via
`pyodbc`) and Oracle (via `oracledb`) through a thin driver switch. Output a standalone `seed.py`.

Generating INSERTs from Python with **parameterized queries** sidesteps almost all manual SQL
quoting and escaping, which is the main reason to choose this format over raw `.sql`. It still does
not deploy anything on its own — the user runs `python seed.py` against their own database.

## Requirements

```
pip install faker pyodbc oracledb
```

`pyodbc` needs the Microsoft ODBC Driver for SQL Server installed on the host. `oracledb` runs in
thin mode and needs no Oracle client. Install only the driver for the engine you target.

## Template

```python
"""seed.py - populate the database with realistic sample data.

Run:
    DB_ENGINE=mssql  python seed.py     # SQL Server
    DB_ENGINE=oracle python seed.py     # Oracle

Connection settings are read from environment variables (see connect()).
"""
import os
from faker import Faker

fake = Faker()
Faker.seed(42)        # reproducible data: same seed -> same rows every run

ENGINE = os.environ.get("DB_ENGINE", "mssql")


def connect():
    if ENGINE == "mssql":
        import pyodbc
        return pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={os.environ['DB_HOST']};DATABASE={os.environ['DB_NAME']};"
            f"UID={os.environ['DB_USER']};PWD={os.environ['DB_PASSWORD']};"
            "TrustServerCertificate=yes;"
        )
    if ENGINE == "oracle":
        import oracledb
        return oracledb.connect(
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            dsn=os.environ["DB_DSN"],   # e.g. host:1521/service
        )
    raise ValueError(f"Unknown DB_ENGINE: {ENGINE}")


def ph(i):
    """Positional placeholder for the active driver."""
    return "?" if ENGINE == "mssql" else f":{i}"


def seed(conn):
    cur = conn.cursor()

    # Clear existing data (child -> parent order) so the script is safe to re-run.
    for table in ("comments", "posts", "users"):
        cur.execute(f"DELETE FROM {table}")

    # users
    users = []
    for _ in range(10):
        name = fake.name()
        email = f"{name.split()[0].lower()}.{fake.unique.user_name()}@example.com"
        users.append((name, email, 1, fake.date_time_this_year()))
    cur.executemany(
        f"INSERT INTO users (name, email, is_active, created_at) "
        f"VALUES ({ph(1)}, {ph(2)}, {ph(3)}, {ph(4)})",
        users,
    )

    # Re-read ids so children reference real parents (portable across both engines).
    cur.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cur.fetchall()]

    # posts (FK -> users)
    posts = []
    for _ in range(30):
        posts.append((
            fake.random_element(user_ids),
            fake.sentence(nb_words=6).rstrip("."),
            fake.paragraph(nb_sentences=4),
            fake.date_time_this_year(),
        ))
    cur.executemany(
        f"INSERT INTO posts (user_id, title, body, published_at) "
        f"VALUES ({ph(1)}, {ph(2)}, {ph(3)}, {ph(4)})",
        posts,
    )

    conn.commit()
    print(f"Seeded: {len(users)} users, {len(posts)} posts")


if __name__ == "__main__":
    connection = connect()
    try:
        seed(connection)
    finally:
        connection.close()
```

## Notes & gotchas

| Topic           | Guidance                                                                                                              |
| --------------- | --------------------------------------------------------------------------------------------------------------------- |
| Reproducibility | `Faker.seed(42)` makes every run produce identical data; drop it for fresh random data each time                      |
| Placeholders    | `pyodbc` uses `?`; `oracledb` uses `:1`, `:2`, ... — the `ph()` helper switches between them                          |
| Booleans        | Send `1` / `0` (SQL Server `BIT`, Oracle `NUMBER(1)`)                                                                 |
| Generated keys  | Insert parents, then `SELECT id FROM parent` to read them back; `cursor.lastrowid` is unreliable across these drivers |
| Batch size      | `executemany` handles thousands of rows; set `cursor.fast_executemany = True` on pyodbc for large loads               |
| Transactions    | Neither driver autocommits here — call `conn.commit()` once at the end                                                |
| Idempotency     | The leading `DELETE`s make the script safe to re-run; switch to `MERGE` if you must preserve user-added rows          |
| Unique values   | Use `fake.unique.<provider>` to avoid UNIQUE-constraint collisions                                                    |
| Domain data     | Choose faker providers that match the schema — `fake.company()`, `fake.address()`, `fake.job()`, etc.                 |
