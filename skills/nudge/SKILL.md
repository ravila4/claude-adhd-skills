---
name: nudge
description: Nudge the user with time-based reminders (stopping times, meetings, break suggestions). Surfaces via hook on prompt submission -- requires human interaction to fire. NOT for process monitoring or job polling -- use `sleep` in Bash instead.
---

# Nudge

Human-facing reminder system for managing focus and pacing. Nudges are stored in SQLite and surface via hook when due.

## When to Use

**Proactively set nudges when:**
- User mentions a stopping time ("stop me at 11", "I need to wrap up by 5")
- User mentions a deadline or meeting ("standup in 30 minutes")
- A long focus session (2+ hours) is underway without breaks
- User asks for a reminder explicitly

**Do NOT use nudge for:**
- Tasks Claude will complete in the current turn
- Information that should go in memory instead
- **Process monitoring** (e.g., "check if the build finished", "see if the pipeline completed"). Nudges require user input (prompt submission) to fire, so they cannot check on running processes. Use `sleep <seconds>` in Bash instead -- it blocks inline and resumes without requiring user interaction.

## Tools

Scripts are located at `hooks/`:

### Adding a Nudge

```bash
python3 hooks/add_alert.py "<time>" "<message>"
```

**Time formats:**
- `HH:MM` - Today at that time (e.g., `23:00`)
- `YYYY-MM-DD HH:MM` - Specific datetime
- `+30m` - 30 minutes from now
- `+2h` - 2 hours from now

### Acknowledging a Nudge

When a nudge has been addressed, dismiss it:

```bash
python3 hooks/ack_alert.py <id>
```

### Viewing Nudges

```bash
sqlite3 hooks/alerts.db "SELECT id, due_at, message FROM alerts WHERE acknowledged = 0"
```

## Message Format

Messages are notes-to-self for Claude. Include:

1. **Reason** - Why this nudge was set
2. **Action** - What to do when it fires

Format: `reason - action to take`

### Examples

```
User asked to stop at 11 PM - wrap up current work and suggest break
User mentioned standup in 30m - remind to prep notes
2 hours on debugging session - check if stuck, suggest break
Deployment window opens at 14:00 - remind user to run deploy script
```

## When Nudges Fire

Due nudges appear in the system-reminder on each prompt submission. When a nudge fires:

1. Read the message to understand context and action
2. Take the specified action (remind user, suggest break, etc.)
3. Acknowledge the nudge so it doesn't repeat

## Database Schema

```sql
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    due_at TEXT NOT NULL,           -- "YYYY-MM-DD HH:MM"
    message TEXT NOT NULL,          -- reason - action
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    acknowledged INTEGER DEFAULT 0  -- 0=pending, 1=done
)
```

Location: `hooks/alerts.db`
