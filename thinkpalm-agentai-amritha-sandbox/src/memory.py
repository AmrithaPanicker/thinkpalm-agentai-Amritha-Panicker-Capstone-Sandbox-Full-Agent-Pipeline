import sqlite3

DB_NAME = "memory.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket TEXT,
            feature TEXT,
            gherkin TEXT,
            script TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_memory(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO test_memory (ticket, feature, gherkin, script)
        VALUES (?, ?, ?, ?)
    """, (
        data["ticket"],
        data["feature"],
        data["gherkin"],
        data["script"]
    ))

    conn.commit()
    conn.close()


def retrieve_memory(ticket_id=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        if ticket_id:
            cursor.execute("""
                SELECT ticket, feature, gherkin, script
                FROM test_memory
                WHERE ticket = ?
                ORDER BY created_at DESC
            """, (ticket_id,))
        else:
            cursor.execute("""
                SELECT ticket, feature, gherkin, script
                FROM test_memory
                ORDER BY created_at DESC
                LIMIT 5
            """)

        rows = cursor.fetchall()
        return rows

    except Exception as e:
        print("Memory Retrieval Error:", e)
        return []

    finally:
        conn.close()