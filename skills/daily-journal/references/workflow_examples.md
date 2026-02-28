# Daily Journal Workflow Examples

## Contents
- [Scenario 1: End of Deep Work Day](#scenario-1-end-of-deep-work-day)
- [Scenario 2: Operational Day with Raw Commands](#scenario-2-operational-day-with-raw-commands)
- [Scenario 3: Incremental Journaling Throughout Day](#scenario-3-incremental-journaling-throughout-day)

## Scenario 1: End of Deep Work Day

**User:** "Can you draft today's journal?"

**Claude actions:**

1. Use daily-journal skill
2. Run `uv run ~/.claude/skills/daily-journal/scripts/collect_day_data.py --date YYYY-MM-DD`
3. Show draft with: Goals (from TodoWrite), Context (first user messages), Technical Work (git commits + files), Commands Used (bash history), Reflection placeholder

**Output:**

````markdown
---
date: 2025-11-12
tags: [daily-log, my-project, api-work]
---

## 2025-11-12

Working on [[My Project]]

## Goals

- [x] Fix logging severity field mapping
- [ ] Implement status tracking
- [ ] Test manifest pre-generation

## Context

Improving API logging to include proper severity fields and clearer context...

## Technical Work

### Git Commits

- 76e8a97 - fix: sort output CSV by numeric position
- 4dd6bb1 - fix: handle concurrent checkpoint writes

### Files Modified

- `scripts/api_client.py`
- `scripts/pipeline.py`

## Commands Used

```bash
# Test with new logging
uv run pytest tests/ -v

# Check log output
tail -f /var/log/app.log
```

## Reflection

_What did I learn today?_
````

**User:** "Looks good, write it to my vault"

**Claude:** Uses obsidian-vault skill to write to `Daily Log/2025-11-12.md`

## Scenario 2: Operational Day with Raw Commands

**User:** "I've been dumping commands all day. Can you organize my journal?"

**Claude actions:**
1. Read today's daily log entry
2. Detect unstructured content (no headers, code blocks only)
3. Ask: "I see raw bash commands. Should I organize them into sections?"
4. If yes: Extract commands, add YAML frontmatter, create sections, show for approval

**Before:**
```markdown
uv run pytest
git commit -m "fix bug"
curl localhost:8080/health
cat output.csv
```

**After:**

````markdown
---
date: 2025-11-12
tags: [daily-log, debugging]
---

## 2025-11-12

## Commands Used

```bash
# Run tests
uv run pytest

# Check service health
curl localhost:8080/health

# Review output
cat output.csv
```

## Technical Work

### Git Commits

- abc1234 - fix bug
````

## Scenario 3: Incremental Journaling Throughout Day

**Mid-afternoon:**
User: "/daily-journal append context"

Claude: "Based on our conversation, I'll add this context:
_Working on fixing the logging severity bug in the API client..._
Should I append to today's journal?"

**Before ending:**
User: "/daily-journal review"

Claude: "Today's journal is missing Reflection section. Based on our work, here's what you learned:
- The API requires top-level `severity` field, not nested in payload
- Status indicators improve log readability
Want me to add this?"
