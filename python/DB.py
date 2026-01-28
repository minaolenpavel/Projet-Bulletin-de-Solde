import sqlite3


class DB:
    def __init__(self, db_path:str = "bulletins.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)

    def write(self, query:str, params=()) -> None:
        cur = self.conn.cursor()
        cur.execute(query, params)
        self.conn.commit()

    def write_many(self, query:str, rows) -> None:
        cur = self.conn.cursor()
        cur.executemany(query, rows)
        self.conn.commit()

    def fetch(self, sql, params=()) -> list:
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

    def close(self) -> None:
        self.conn.close()


if __name__ =="__main__":
    db = DB("test.db")

    db.write("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER
    )
    """)

    db.write(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        ("Alice", 24)
    )

    db.write(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        ("Bob", 31)
    )

    db.close()
