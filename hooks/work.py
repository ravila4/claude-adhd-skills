#!/usr/bin/env python3
"""Work session time tracker CLI.

Usage:
    work.py start "<task>" [-d domain] [-a activity] [--project name]
    work.py end [task_id]
    work.py current
"""

import argparse
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "work.db"


def init_db() -> None:
    """Create work_sessions table and indexes if they don't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS work_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project TEXT NOT NULL,
                task_name TEXT NOT NULL,
                activity TEXT,
                domain TEXT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                notes TEXT,
                agent_id TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_project_date
            ON work_sessions(project, date(start_time))
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_active
            ON work_sessions(end_time) WHERE end_time IS NULL
        """)


def infer_project(path: Path) -> str:
    """Infer project name from directory path."""
    return path.name


def start_task(
    task_name: str,
    project: str,
    domain: str,
    activity: str | None = None,
    agent_id: str | None = None,
) -> int:
    """Start a new work session. Auto-ends any active task in same project.

    Returns the new session ID.
    """
    now = datetime.now().isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        # Auto-end active task in same project
        conn.execute(
            """
            UPDATE work_sessions
            SET end_time = ?
            WHERE project = ? AND end_time IS NULL
            """,
            (now, project),
        )

        cursor = conn.execute(
            """
            INSERT INTO work_sessions (project, task_name, activity, domain, start_time, agent_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (project, task_name, activity, domain, now, agent_id),
        )
        return cursor.lastrowid


def end_task(project: str | None = None, task_id: int | None = None) -> bool:
    """End a work session.

    If task_id is provided, ends that specific task.
    Otherwise, ends the active task in the given project.

    Returns True if a task was ended, False otherwise.
    """
    now = datetime.now().isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        if task_id is not None:
            cursor = conn.execute(
                "UPDATE work_sessions SET end_time = ? WHERE id = ? AND end_time IS NULL",
                (now, task_id),
            )
        else:
            cursor = conn.execute(
                "UPDATE work_sessions SET end_time = ? WHERE project = ? AND end_time IS NULL",
                (now, project),
            )
        return cursor.rowcount > 0


def get_current_status(current_project: str) -> dict:
    """Get current work status.

    Returns dict with:
        - active: The active task in current_project (or None)
        - paused: List of active tasks in other projects
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        # Active task in current project
        cursor = conn.execute(
            """
            SELECT id, project, task_name, activity, domain, start_time
            FROM work_sessions
            WHERE project = ? AND end_time IS NULL
            """,
            (current_project,),
        )
        active_row = cursor.fetchone()
        active = dict(active_row) if active_row else None

        # Paused tasks (active in other projects)
        cursor = conn.execute(
            """
            SELECT id, project, task_name, activity, domain, start_time
            FROM work_sessions
            WHERE project != ? AND end_time IS NULL
            ORDER BY start_time DESC
            """,
            (current_project,),
        )
        paused = [dict(row) for row in cursor.fetchall()]

    return {"active": active, "paused": paused}


def format_duration(start_time: str) -> str:
    """Format duration from start_time to now as human-readable string."""
    start = datetime.fromisoformat(start_time)
    delta = datetime.now() - start
    total_minutes = int(delta.total_seconds() / 60)

    if total_minutes < 60:
        return f"{total_minutes}m"
    hours = total_minutes // 60
    minutes = total_minutes % 60
    if minutes == 0:
        return f"{hours}h"
    return f"{hours}h {minutes}m"


def print_current_status(current_project: str) -> None:
    """Print current work status in hook-friendly format."""
    status = get_current_status(current_project)

    if status["active"]:
        task = status["active"]
        duration = format_duration(task["start_time"])
        print(f"Active in {task['project']}:")
        print(f'  - "{task["task_name"]}" ({duration})')

    if status["paused"]:
        print("Paused:")
        for task in status["paused"]:
            duration = format_duration(task["start_time"])
            print(f'  - {task["project"]}: "{task["task_name"]}" (paused {duration} ago)')

    if not status["active"] and not status["paused"]:
        print('No active work session. Use: work.py start "<task>" -d [work|personal|tooling]')


def main() -> None:
    parser = argparse.ArgumentParser(description="Work session time tracker")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Start command
    start_parser = subparsers.add_parser("start", help="Start a new task")
    start_parser.add_argument("task", help="Task name/description")
    start_parser.add_argument(
        "-d", "--domain", choices=["work", "personal", "tooling"], help="Domain category"
    )
    start_parser.add_argument("-a", "--activity", help="Activity type (debugging, reviewing, etc.)")
    start_parser.add_argument("--project", help="Project name (default: inferred from PWD)")
    start_parser.add_argument("--agent-id", help="Agent ID for tracking")

    # End command
    end_parser = subparsers.add_parser("end", help="End current or specific task")
    end_parser.add_argument("task_id", nargs="?", type=int, help="Specific task ID to end")
    end_parser.add_argument("--project", help="Project name (default: inferred from PWD)")

    # Current command
    subparsers.add_parser("current", help="Show current work status")

    args = parser.parse_args()
    init_db()

    if args.command == "start":
        project = args.project or infer_project(Path.cwd())
        session_id = start_task(
            task_name=args.task,
            project=project,
            domain=args.domain,
            activity=args.activity,
            agent_id=args.agent_id,
        )
        print(f"Started [{session_id}]: {args.task} ({project})")

    elif args.command == "end":
        if args.task_id:
            success = end_task(task_id=args.task_id)
        else:
            project = args.project or infer_project(Path.cwd())
            success = end_task(project=project)

        if success:
            print("Task ended.")
        else:
            print("No active task to end.")

    elif args.command == "current":
        project = infer_project(Path.cwd())
        print_current_status(project)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
