"""
Database layer - SQLite persistence for query logs.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "smartroute.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS queries (
    id TEXT PRIMARY KEY,
    timestamp REAL,
    query TEXT,
    difficulty TEXT,
    score INTEGER,
    confidence INTEGER,
    selected_model TEXT,
    routing_reason TEXT,
    routing_time_ms REAL,
    generation_time_ms REAL,
    actual_cost REAL,
    baseline_cost REAL,
    savings_pct REAL,
    override_mode TEXT,
    response_preview TEXT,
    model_source TEXT
);
"""


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.execute(SCHEMA)
    conn.commit()
    conn.close()


def reset_db():
    conn = get_conn()
    conn.execute("DELETE FROM queries")
    conn.commit()
    conn.close()


def save_query(record: dict):
    conn = get_conn()
    conn.execute(
        """INSERT INTO queries
        (id, timestamp, query, difficulty, score, confidence, selected_model,
         routing_reason, routing_time_ms, generation_time_ms, actual_cost,
         baseline_cost, savings_pct, override_mode, response_preview, model_source)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            record["id"], record["timestamp"], record["query"], record["difficulty"],
            record["score"], record["confidence"], record["selected_model"],
            record["routing_reason"], record["routing_time_ms"], record["generation_time_ms"],
            record["actual_cost"], record["baseline_cost"], record["savings_pct"],
            record["override_mode"], record["response_preview"], record["model_source"],
        ),
    )
    conn.commit()
    conn.close()


def get_history(limit: int = 50):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM queries ORDER BY timestamp DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM queries ORDER BY timestamp ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
