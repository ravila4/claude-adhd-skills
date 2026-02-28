#!/usr/bin/env python3
"""Add a new alert to the database."""

import sqlite3
import sys
from datetime import datetime, timedelta
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


def parse_time(time_str: str) -> str:
    """Parse time string into ISO format.

    Accepts:
    - HH:MM (today)
    - YYYY-MM-DD HH:MM
    - +Nm (N minutes from now)
    - +Nh (N hours from now)
    """
    now = datetime.now()

    if time_str.startswith("+"):
        # Relative time
        try:
            amount = int(time_str[1:-1])
        except ValueError:
            raise ValueError(f"Invalid time format: {time_str!r}. Expected +30m or +2h")
        unit = time_str[-1]
        if unit == "m":
            target = now + timedelta(minutes=amount)
        elif unit == "h":
            target = now + timedelta(hours=amount)
        else:
            raise ValueError(f"Unknown unit: {unit!r}. Use 'm' (minutes) or 'h' (hours)")
        return target.strftime("%Y-%m-%d %H:%M")

    if len(time_str) == 5 and ":" in time_str:
        # HH:MM format - assume today
        return f"{now.strftime('%Y-%m-%d')} {time_str}"

    # Assume full datetime
    return time_str


def add_alert(due_at: str, message: str) -> int:
    """Add alert and return its ID."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "INSERT INTO alerts (due_at, message) VALUES (?, ?)",
            (due_at, message),
        )
        return cursor.lastrowid


def main() -> None:
    init_db()
    if len(sys.argv) < 3:
        print("Usage: add_alert.py <time> <message>")
        print("  Time formats: HH:MM, YYYY-MM-DD HH:MM, +30m, +2h")
        sys.exit(1)

    time_str = sys.argv[1]
    message = " ".join(sys.argv[2:])

    due_at = parse_time(time_str)
    alert_id = add_alert(due_at, message)
    print(f"Alert {alert_id} set for {due_at}: {message}")


if __name__ == "__main__":
    main()
