#!/usr/bin/env python3
"""Hook script: check for due alerts and print them."""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "alerts.db"


def init_db() -> None:
    """Create alerts table if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                due_at TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                acknowledged INTEGER NOT NULL DEFAULT 0
            )
        """)


def check_alerts() -> list[tuple[int, str, str]]:
    """Return list of (id, due_at, message) for unacknowledged due alerts."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            SELECT id, due_at, message
            FROM alerts
            WHERE due_at <= ? AND acknowledged = 0
            ORDER BY due_at
            """,
            (now,),
        )
        return cursor.fetchall()


def main() -> None:
    init_db()
    alerts = check_alerts()
    if alerts:
        print("⏰ ALERTS DUE:")
        for alert_id, due_at, message in alerts:
            print(f"  [{alert_id}] {due_at}: {message}")
        print("(Use 'python3 ~/.claude/hooks/ack_alert.py <id>' to dismiss)")


if __name__ == "__main__":
    main()
