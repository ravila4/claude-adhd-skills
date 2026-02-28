#!/usr/bin/env python3
"""Acknowledge (dismiss) an alert."""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "alerts.db"


def ack_alert(alert_id: int) -> bool:
    """Mark alert as acknowledged. Returns True if found."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "UPDATE alerts SET acknowledged = 1 WHERE id = ?",
            (alert_id,),
        )
        return cursor.rowcount > 0


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: ack_alert.py <alert_id>")
        sys.exit(1)

    alert_id = int(sys.argv[1])
    if ack_alert(alert_id):
        print(f"Alert {alert_id} acknowledged")
    else:
        print(f"Alert {alert_id} not found")
        sys.exit(1)


if __name__ == "__main__":
    main()
