---
name: work-tracker
description: Track time on tasks with project context. Use when starting/ending work, discussing time tracking, or when user wants to see what they're working on.
---

# Work Tracker

Lightweight time tracking with task and project context. Sessions are stored in SQLite and surface via hook on prompt submission.

## When to Use

**Start tracking when:**
- User says they're starting a task ("let's work on X", "starting to debug Y")
- Beginning a defined piece of work (PR review, feature implementation, bug fix)
- Switching context to a different task

**End tracking when:**
- User says they're done ("finished with X", "wrapping up")
- Task is explicitly completed
- Before starting a different task (auto-ends via `start`)

**Do NOT track:**
- Quick questions or one-off lookups
- Tasks you'll complete in a single turn
- Research/exploration without a clear task

## CLI Reference

Scripts are located at `hooks/`:

### Starting a Task

```bash
python3 hooks/work.py start "<task>" -d <domain> [-a activity] [--project name]
```

**Domains** (required):
- `work` - Job/professional tasks
- `personal` - Side projects, learning
- `tooling` - Dev environment, config

**Activity** (optional): debugging, reviewing, planning, implementing, etc.

**Project**: Auto-inferred from PWD. Override with `--project`.

### Ending a Task

```bash
python3 hooks/work.py end           # Ends active task in current project
python3 hooks/work.py end 42        # Ends specific task by ID
```

### Checking Status

```bash
python3 hooks/work.py current
```

## Key Behaviors

1. **Auto-end on start**: Starting a new task auto-ends any active task in the *same project*
2. **Cross-project pausing**: Tasks in other projects stay "paused" (no end_time but different project)
3. **Hook visibility**: Current status shows on every prompt via hook

## Hook Output Examples

Active session:
```
Active in my-project:
  - "Review hooks" (47m)
Paused:
  - other-project: "Refactor auth" (paused 2h ago)
```

No active session:
```
No active work session. Use: work.py start "<task>" -d [work|personal|tooling]
```

## Database Schema

```sql
CREATE TABLE work_sessions (
    id INTEGER PRIMARY KEY,
    project TEXT NOT NULL,        -- From PWD or explicit
    task_name TEXT NOT NULL,
    activity TEXT,                -- debugging, reviewing, planning, etc.
    domain TEXT,                  -- work|personal|tooling
    start_time TEXT NOT NULL,     -- ISO timestamp
    end_time TEXT,                -- NULL if active
    notes TEXT,
    agent_id TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

Location: `hooks/work.db`

## Usage Examples

```bash
# Starting feature work
python3 hooks/work.py start "Implement user auth" -d work -a implementing

# Code review
python3 hooks/work.py start "Review PR #42" -d work -a reviewing

# Debugging in a specific project
python3 hooks/work.py start "Fix login bug" -d work -a debugging --project my-app

# Personal project
python3 hooks/work.py start "Add dark mode" -d personal

# Tooling/config work
python3 hooks/work.py start "Configure time tracker" -d tooling
```
