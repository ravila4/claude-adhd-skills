# Log Formats Deep-Dive

Understanding the three types of logs and how to correlate them.

## Contents

- [Debug Logs (.txt files)](#debug-logs-txt-files)
- [JSONL Session Logs](#jsonl-session-logs)
- [Git History](#git-history)
- [Correlation Strategy](#correlation-strategy)
- [Finding Logs by Time](#finding-logs-by-time)
- [.claude.json Correlation](#claudejson-correlation)
- [Limitations](#limitations)

## Debug Logs (.txt files)

**Location**: `~/.claude/debug/*.txt`

**Purpose**: Session metadata, tool invocations, hooks, permissions

**CRITICAL LIMITATION**: Debug logs DO NOT contain user prompts or Claude responses (privacy protection). Only metadata.

### Structure

Debug logs contain:
- Hook lifecycle events (SessionStart, PreToolUse, PostToolUse, SessionEnd)
- Tool invocation patterns
- Permission requests (with JSON details)
- File modification tracking
- MCP server connections
- Config file writes (atomic pattern)

### Key Patterns to Search

**Session lifecycle**:
```bash
grep -n "SessionStart\|SessionEnd\|Cleaned up session snapshot" debug.txt
```

**Tool usage**:
```bash
# Tool invocations
grep "executePreToolHooks" debug.txt

# Tool completions
grep "PostToolUse" debug.txt

# If counts don't match, operation was blocked
```

**Permission requests**:
```bash
# Full permission request JSON
awk '/Permission suggestions/,/^\]/' debug.txt

# Just the rules requested
grep -A5 "Permission suggestions" debug.txt | grep "ruleContent"
```

**File modifications**:
```bash
# Files tracked for changes
grep "Tracked file modification" debug.txt

# Atomic writes completed
grep "written atomically" debug.txt
```

**Timeline**:
```bash
# High-level event sequence
grep -n "UserCommandMessage\|executePreToolHooks\|Permission" debug.txt
```

### Hook System

Claude uses hooks for lifecycle events:
- **SessionStart** - Session initialization
- **UserPromptSubmit** - User sent a message
- **PreToolUse** - Before tool execution
- **PostToolUse** - After tool execution (absence = blocked)
- **Stop** - Session interrupted
- **SessionEnd** - Session cleanup

### File Operations

All config changes use atomic pattern:
1. Write to temp file
2. Preserve permissions
3. Atomic rename

Example:
```
Writing .claude.json atomically (72092 → 72506 bytes)
```
Size increase suggests permission rule was added.

---

## JSONL Session Logs

**Location**: `~/.claude/projects/<project-hash>/*.jsonl`

**Purpose**: Complete conversation including user prompts, Claude responses, thinking blocks, tool uses

**THIS IS WHERE THE CONTENT IS**. Debug logs only have metadata; JSONL has the actual conversation.

### Structure

One JSON object per line. Entry types:
- `{"message": {...}}` - User/assistant messages
- `{"type": "file-history-snapshot"}` - File state snapshots

### Message Structure

```json
{
  "message": {
    "role": "user" | "assistant",
    "content": [
      {"type": "text", "text": "..."},
      {"type": "thinking", "thinking": "..."},
      {"type": "tool_use", "name": "...", "input": {...}}
    ]
  },
  "timestamp": "..."
}
```

### Extracting Content

**User messages** (what was requested):
```python
import json

with open('session.jsonl') as f:
    for line in f:
        msg = json.loads(line).get('message', {})
        if msg.get('role') == 'user':
            for block in msg.get('content', []):
                if block.get('type') == 'text':
                    print(block['text'])
```

**Thinking blocks** (Claude's reasoning):
```python
for block in msg.get('content', []):
    if block.get('type') == 'thinking':
        print(block['thinking'])
```

**Tool uses**:
```python
for block in msg.get('content', []):
    if block.get('type') == 'tool_use':
        print(f"Tool: {block['name']}")
        print(f"Input: {block['input']}")
```

### Common Pitfalls

**Mixed entry types**: Not all lines are messages. Filter by checking for `message` key or `role` field.

**Content can be string or list**: Early messages might have string content, later ones are arrays. Handle both:
```python
content = msg.get('content', '')
if isinstance(content, str):
    # Old format
    text = content
elif isinstance(content, list):
    # Current format
    for block in content:
        if block.get('type') == 'text':
            text = block.get('text')
```

---

## Git History

**Purpose**: Ground truth for what actually changed

### Essential Commands

**Commits for a date range**:
```bash
git log --since="2025-11-05 00:00:00" --until="2025-11-05 23:59:59" \
  --pretty=format:"%h - %s (%cr)" --date=relative
```

**Detailed commit info**:
```bash
git log --since="2025-11-05 00:00:00" --stat --pretty=format:"%n%h - %s%n%b"
```

**Specific commit details**:
```bash
git log --format="%h %s%n%b" <commit-hash> -1
```

**What changed today**:
```bash
git diff --stat HEAD@{yesterday}..HEAD
```

### Why Git is Ground Truth

- Debug logs show tool usage but not results
- JSONL shows conversation but not final state
- Git shows what actually got committed
- Commit messages explain WHY

---

## Correlation Strategy

Combine all three sources for complete picture:

### Step 1: Identify Sessions (Debug Logs)
```bash
# Find today's debug logs
find ~/.claude/debug -name "*.txt" -newermt "2025-11-05 00:00"

# Count tool usage per session
for log in *.txt; do
    echo "=== $log ==="
    grep "executePreToolHooks" "$log" | sed 's/.*tool: //' | sort | uniq -c
done
```

### Step 2: Extract User Intent (JSONL)
```bash
# Find corresponding JSONL logs
find ~/.claude/projects -name "*.jsonl" -newermt "2025-11-05 00:00"

# Extract user journey
python3 extract_user_journey.py session.jsonl
```

### Step 3: Extract Reasoning (JSONL)
```bash
# Get thinking blocks and insights
python3 extract_thinking.py session.jsonl
```

### Step 4: Verify with Git
```bash
# What actually changed
git log --since="2025-11-05 00:00:00" --stat
```

### Step 5: Build Narrative

Combine:
- **User intent** (from JSONL user messages)
- **Claude's reasoning** (from JSONL thinking blocks)
- **Tool usage patterns** (from debug logs)
- **Actual changes** (from git history)
- **Blockers** (from debug permission flows)

Result: Complete story of WHY and WHAT happened.

---

## Finding Logs by Time

**Find logs from specific hour**:
```bash
find ~/.claude/debug -name "*.txt" \
  -newermt "2025-11-05 14:00" ! -newermt "2025-11-05 15:00" \
  -exec ls -lh {} \;
```

**Find logs from today**:
```bash
find ~/.claude/debug -name "*.txt" -newermt "$(date +%Y-%m-%d) 00:00"
```

**Find JSONL by session ID** (from debug log):
```bash
# Extract session ID from debug log filename
SESSION_ID=$(basename debug.txt .txt)

# Find matching JSONL
find ~/.claude/projects -name "*${SESSION_ID}*.jsonl"
```

---

## .claude.json Correlation

Check config changes to verify permission grants:

```bash
# Check file size changes
ls -lh ~/.claude.json

# Search for specific permission
jq '.permissions' ~/.claude.json | grep "uv tool install"
```

If `.claude.json` grew in size during a session, likely a permission rule was added.

---

## Limitations

### What You CAN'T Get from Logs

1. **Debug logs**: No conversation content (by design)
2. **Tool results**: See invocations, not outputs
3. **Timestamps**: Debug logs lack precise timing
4. **Permission outcomes**: Can't definitively tell if granted/denied
5. **Error details**: Errors not explicitly logged
6. **File paths**: Debug logs don't show which files were read

### What Requires Inference

- User intent (from JSONL user messages + context)
- Why permissions were blocked (debug shows request, not reason)
- Which session accomplished what (correlate JSONL + git + debug)
- Session success/failure (no explicit success marker)

### Best Practices

1. **Always correlate multiple sources** - No single log tells full story
2. **Check git for ground truth** - Logs show attempts, git shows results
3. **Look for patterns** - Tool sequences reveal strategy
4. **Verify permission grants** - Check .claude.json size/content
5. **Use session IDs** - Track across log files
