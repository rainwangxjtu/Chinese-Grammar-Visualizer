import sqlite3
from typing import Dict, List, Tuple

class GrammarLogDatabase:
    """
    Handles data persistence for parsed sentences.
    Demonstrates secure database initialization, parameterized SQL queries,
    and structured transaction handling using context managers.
    """
    def __init__(self, db_name: str = "grammar_logs.db"):
        self.db_name = db_name
        self._initialize_table()

    def _get_connection(self) -> sqlite3.Connection:
        """Returns a thread-safe connection to the SQLite database."""
        return sqlite3.connect(self.db_name)

    def _initialize_table(self) -> None:
        """Creates the log table if it doesn't already exist."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS sentence_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            raw_text TEXT NOT NULL,
            subject TEXT NOT NULL,
            verb TEXT NOT NULL,
            object TEXT NOT NULL
        );
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()

    def log_transaction(self, raw_text: str, svo_schema: Dict[str, str]) -> None:
        """Inserts a freshly analyzed sentence schema vector into the database securely."""
        insert_sql = """
        INSERT INTO sentence_logs (raw_text, subject, verb, object)
        VALUES (?, ?, ?, ?);
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(insert_sql, (
                raw_text,
                svo_schema.get("subject", "Unknown"),
                svo_schema.get("verb", "Unknown"),
                svo_schema.get("object", "Unknown")
            ))
            conn.commit()

    def fetch_recent_logs(self, limit: int = 5) -> List[Tuple[Any, ...]]:
        """Queries historical transaction vectors to display inside the UI telemetry monitor."""
        query_sql = "SELECT timestamp, raw_text, subject, verb, object FROM sentence_logs ORDER BY id DESC LIMIT ?;"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query_sql, (limit,))
            return cursor.fetchall()



