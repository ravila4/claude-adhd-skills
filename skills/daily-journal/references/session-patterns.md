# Session Pattern Library

Three common patterns that reveal different session types. Recognizing patterns helps quickly categorize sessions and extract relevant information.

## Contents

- [Pattern 1: Active Working Session](#pattern-1-active-working-session)
- [Pattern 2: Permission-Blocked Session](#pattern-2-permission-blocked-session)
- [Pattern 3: Minimal/Testing Session](#pattern-3-minimaltesting-session)
- [How to Identify Patterns Quickly](#how-to-identify-patterns-quickly)
- [Advanced: Workflow Patterns](#advanced-workflow-patterns)
- [Using Patterns for Journal Generation](#using-patterns-for-journal-generation)
- [Correlation with JSONL](#correlation-with-jsonl)
- [Common Combinations](#common-combinations)

## Pattern 1: Active Working Session

### Indicators
- **3+ user interactions** (multiple back-and-forth exchanges)
- **Varied tool usage** (Read, Edit, Bash, Glob, Grep, etc.)
- **File modifications tracked** (FileHistory snapshots created)
- **Multiple tool sequences** (Read → Edit → Bash patterns)
- **Git commits** (work completed and saved)

### Debug Log Signature
```bash
# Multiple user prompts
grep "UserCommandMessage" debug.txt | wc -l
# Output: 5+

# Varied tools
grep "executePreToolHooks" debug.txt | sed 's/.*tool: //' | sort -u
# Output: Bash, Edit, Glob, Grep, Read, Write

# File tracking
grep "Tracked file modification" debug.txt | wc -l
# Output: 3+

# Commits
grep "git commit" debug.txt
# Output: Multiple commit operations
```

### What This Reveals
- User was actively working with Claude on a task
- Task involved reading, modifying, and testing code
- Work resulted in concrete changes (commits)
- Session was productive and goal-oriented

### Example Timeline
```
1. User requests feature implementation
2. Claude reads relevant files
3. Claude edits code
4. User requests changes
5. Claude refines implementation
6. Tests run
7. Commit created
8. User requests documentation
9. Claude updates README
10. Final commit
```

### Journal Entry Focus
- **Context**: What feature/problem was being solved?
- **Technical Work**: What was built/modified?
- **Decisions**: Why these approaches?
- **Results**: What got committed?

---

## Pattern 2: Permission-Blocked Session

### Indicators
- **executePreToolHooks followed by Permission suggestions**
- **No corresponding PostToolUse event** (operation never executed)
- **Session ends shortly after** (Stop → SessionEnd)
- **Short session** (1-3 interactions)
- **Stop event with undefined query**

### Debug Log Signature
```bash
# Permission requested
awk '/Permission suggestions/,/^\]/' debug.txt
# Output: JSON with toolName, ruleContent, behavior

# No completion
grep "executePreToolHooks.*Bash" debug.txt
grep "PostToolUse.*Bash" debug.txt
# If first exists but second doesn't = blocked

# Quick exit
grep -A5 "Permission suggestions" debug.txt | grep "Stop\|SessionEnd"
# Output: Session ended right after permission request
```

### What This Reveals
- Claude attempted an operation requiring permission
- User either:
  - Denied permission
  - Ignored request
  - Stopped session before responding
  - Got needed info from earlier Read operations
- Session incomplete/interrupted

### Example Timeline
```
1. User requests something
2. Claude reads files for context
3. Claude attempts Bash command (e.g., uv tool install)
4. Permission requested
5. User stops session
6. Session ends
```

### What to Infer
Check `.claude.json` file size:
- **Size increased** = Permission granted before stopping
- **Size unchanged** = Permission not granted

Look for patterns:
- **Read → Bash (blocked)** = Wanted to execute based on files read
- **Specific permission** = Shows what was attempted (e.g., "uv tool install:*")

### Journal Entry Focus
- **Context**: What was user trying to accomplish?
- **Blocker**: What permission was needed and why?
- **Hypothesis**: Why did user stop? (3 hypotheses from /tmp/)
  1. Got info from Read operations (didn't need execution)
  2. Wanted to review before granting permission
  3. Changed mind about the task
- **Status**: Unresolved/incomplete

---

## Pattern 3: Minimal/Testing Session

### Indicators
- **0-2 user interactions** (very short session)
- **Only system commands** (/clear, /exit)
- **Minimal tool usage** (0-2 tools used)
- **No permission issues** (no permission requests)
- **No file modifications** (no tracking events)

### Debug Log Signature
```bash
# Very few user prompts
grep "UserCommandMessage" debug.txt | wc -l
# Output: 0-2

# System commands only
grep "UserCommandMessage rendering" debug.txt
# Output: "/clear" or "/exit"

# Minimal tools
grep "executePreToolHooks" debug.txt | wc -l
# Output: 0-2

# No files modified
grep "Tracked file modification" debug.txt
# Output: (empty)
```

### What This Reveals
- User opened session briefly
- Possibly:
  - Testing if Claude Code works
  - Quick question answered
  - Cleared old session
  - Opened by mistake
- No substantial work done

### Example Timeline
```
1. User opens Claude Code
2. User types /clear (or nothing)
3. User types /exit
4. Session ends
```

### Journal Entry Focus
**Skip these sessions** - Not worth documenting unless testing a new feature.

---

## How to Identify Patterns Quickly

### Quick Pattern Detection Script
```bash
# Count key indicators
INTERACTIONS=$(grep "UserCommandMessage" debug.txt | wc -l)
TOOLS=$(grep "executePreToolHooks" debug.txt | wc -l)
FILES=$(grep "Tracked file modification" debug.txt | wc -l)
PERMISSIONS=$(grep "Permission suggestions" debug.txt | wc -l)

echo "Interactions: $INTERACTIONS"
echo "Tools used: $TOOLS"
echo "Files modified: $FILES"
echo "Permissions requested: $PERMISSIONS"

# Pattern classification
if [ $INTERACTIONS -ge 3 ] && [ $FILES -ge 1 ]; then
    echo "Pattern: ACTIVE WORKING SESSION"
elif [ $PERMISSIONS -ge 1 ]; then
    echo "Pattern: PERMISSION-BLOCKED SESSION"
else
    echo "Pattern: MINIMAL/TESTING SESSION"
fi
```

### Quick Indicators Table

| Metric | Active | Blocked | Minimal |
|--------|--------|---------|---------|
| Interactions | 3+ | 1-3 | 0-2 |
| Tools | 5+ varied | 2-4 | 0-2 |
| Files modified | 1+ | 0 | 0 |
| Permissions | 0-1 | 1+ | 0 |
| Commits | 1+ | 0 | 0 |
| Duration | Long | Short | Very short |

---

## Advanced: Workflow Patterns

### TDD Pattern
**Signature**: Edit (test) → Bash (pytest) → Edit (fix) → Bash (pytest) → repeat

```bash
grep -A2 "executePreToolHooks.*Edit" debug.txt | \
    grep -A1 "test_" | \
    grep -A3 "Bash.*pytest"
```

### Code Review Pattern
**Signature**: Read (multiple files) → git diff → git log → git commit

```bash
grep "executePreToolHooks.*Read" debug.txt | wc -l  # Multiple reads
grep "git diff\|git log" debug.txt                   # Review commands
grep "git commit" debug.txt                          # Commit created
```

### Debugging Pattern
**Signature**: Bash (error) → Read (code) → Edit (fix) → Bash (retry)

```bash
grep -i "error\|failed" debug.txt                    # Error occurred
grep "executePreToolHooks.*Read" debug.txt           # Investigated
grep "executePreToolHooks.*Edit" debug.txt           # Fixed
```

### Exploration Pattern
**Signature**: Multiple Glob/Grep → Read files → few edits

```bash
grep "executePreToolHooks.*Glob\|.*Grep" debug.txt | wc -l  # Many searches
grep "executePreToolHooks.*Read" debug.txt | wc -l           # Many reads
grep "executePreToolHooks.*Edit" debug.txt | wc -l           # Few edits
```

---

## Using Patterns for Journal Generation

### Active Session → Comprehensive Entry
- Full context section
- Multiple main issues
- Detailed technical work
- Specific commits and changes

### Blocked Session → Focus on Blocker
- Brief context
- Emphasize what was attempted
- Note permission details
- Hypothesize why blocked
- Mark as unresolved

### Minimal Session → Skip or Brief Note
- One-line note if relevant
- Otherwise ignore in daily log

---

## Correlation with JSONL

After identifying pattern from debug logs, use JSONL to fill in details:

### For Active Sessions
Extract:
- User messages → understand goals
- Thinking blocks → understand reasoning
- Tool sequences → understand approach

### For Blocked Sessions
Extract:
- User's initial request → what was attempted
- Thinking before permission → why it was needed
- Last user message → why they stopped

### For Minimal Sessions
Skip JSONL analysis - not worth the time.

---

## Common Combinations

### "Active but Incomplete"
- Many interactions and tools
- No commits at end
- Often means: work in progress, will continue tomorrow
- Journal focus: Status of incomplete work

### "Blocked but Productive"
- Permission requested
- But extensive Read operations before
- Often means: User got needed info, didn't need execution
- Journal focus: Information gathered, not implementation

### "Minimal but Important"
- Very short session
- But critical command executed
- Often means: Quick fix or config change
- Journal focus: What changed and why
