# High-Signal Patterns for Log Analysis

Patterns are ranked by signal-to-noise ratio for generating development journals.

## Contents

- [⭐⭐⭐ Highest Signal: User Message Extraction](#-highest-signal-user-message-extraction)
- [⭐⭐⭐ Highest Signal: Thinking Blocks + Tool Usage](#-highest-signal-thinking-blocks-tool-usage)
- [⭐⭐ High Signal: Conversation Flow with Keyword Tagging](#-high-signal-conversation-flow-with-keyword-tagging)
- [⭐⭐ High Signal: File Tracking (Debug Logs)](#-high-signal-file-tracking-debug-logs)
- [⭐ Medium Signal: Permission Flows](#-medium-signal-permission-flows)
- [Additional Useful Patterns](#additional-useful-patterns)
- [Correlation Strategy](#correlation-strategy)

## ⭐⭐⭐ Highest Signal: User Message Extraction

**Purpose**: Understand what the user actually asked for (the "journey")

**Script** (from JSONL logs):
```python
sed -n '9,100p' session.jsonl | python3 << 'SCRIPT'
import json
import sys

for line in sys.stdin:
    if line.strip():
        msg = json.loads(line)
        role = msg.get('message', {}).get('role')
        if role == 'user':
            content = msg.get('message', {}).get('content', '')
            if isinstance(content, str):
                print(f"\n[USER]: {content[:600]}\n")
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get('type') == 'text':
                        print(f"\n[USER]: {block['text'][:600]}\n")
SCRIPT
```

**What it reveals**:
- What problem the user was trying to solve
- WHY they needed help
- Evolution of requests throughout the day

**Signal-to-noise**: 10/10 - Directly answers "what was the user doing?"

---

## ⭐⭐⭐ Highest Signal: Thinking Blocks + Tool Usage

**Purpose**: Extract Claude's reasoning process and tool invocations

**Script**:
```python
python3 << 'SCRIPT'
import json

with open('session.jsonl', 'r') as f:
    messages = [json.loads(line) for line in f if line.strip()]

tool_uses = []
thinking_moments = []
for msg in messages:
    msg_content = msg.get('message', {}).get('content', [])
    if isinstance(msg_content, list):
        for block in msg_content:
            if isinstance(block, dict):
                if block.get('type') == 'thinking':
                    think_text = block.get('thinking', '')[:300]
                    thinking_moments.append(think_text)
                elif block.get('type') == 'tool_use':
                    tool_name = block.get('name', 'unknown')
                    tool_uses.append(tool_name)

print(f"Tools used: {set(tool_uses)}")
print(f"Thinking moments: {len(thinking_moments)}\n")

print("="*80)
print("KEY INSIGHTS / REALIZATIONS:")
print("="*80)
for i, think in enumerate(thinking_moments[:5], 1):
    print(f"\n[Insight {i}]")
    print(think)
    print()
SCRIPT
```

**What it reveals**:
- Why Claude made decisions
- What insights emerged
- What approach/strategy was used
- Key realizations during problem-solving

**Signal-to-noise**: 10/10 - Shows reasoning, not just actions

---

## ⭐⭐ High Signal: Conversation Flow with Keyword Tagging

**Purpose**: Timeline of back-and-forth with automatic pattern detection

**Script**:
```python
python3 << 'PYTHON_EOF'
import json
import re

conversation_flow = []

with open('session.jsonl', 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if 'message' in data:
                msg = data['message']
                role = msg.get('role', '')

                content = msg.get('content', [])
                text = ''
                for block in content:
                    if isinstance(block, dict) and block.get('type') == 'text':
                        text = block.get('text', '')
                        break

                conversation_flow.append({
                    'role': role,
                    'text': text,
                    'timestamp': data.get('timestamp', '')
                })
        except:
            pass

# Print with keyword highlighting
for i, turn in enumerate(conversation_flow):
    if turn['role'] == 'user':
        print(f"\n[USER #{i//2 + 1}]: {turn['text'][:300]}")
    elif turn['role'] == 'assistant':
        text = turn['text']

        # Look for key phrases
        if 'memory' in text.lower() or 'scale' in text.lower():
            print(f"  → INSIGHT: Memory/scaling concern")
        if 'refactor' in text.lower():
            print(f"  → ACTION: Refactoring code")
        if 'test' in text.lower() and ('passing' in text.lower() or 'failed' in text.lower()):
            print(f"  → TESTING: Running tests")
        if 'commit' in text.lower():
            print(f"  → COMPLETION: Committing changes")

        errors = re.findall(r'(Error|Failed|Exception|FAILED).*', text, re.IGNORECASE)
        if errors:
            print(f"  → PROBLEM: {errors[0][:100]}")

        preview = text[:400].replace('\n', ' ')
        print(f"  Assistant: {preview}...")

print(f"\nTotal turns: {len(conversation_flow)}")
PYTHON_EOF
```

**What it reveals**:
- Key decision points (INSIGHT, ACTION, TESTING)
- Problems encountered (PROBLEM tag)
- Completion milestones (COMPLETION tag)
- Overall session narrative

**Signal-to-noise**: 8/10 - Good overview but needs manual review

---

## ⭐⭐ High Signal: File Tracking (Debug Logs)

**Purpose**: Identify actual changes made to the codebase

**Patterns to search in debug logs**:
```bash
# File modifications tracked
grep "Tracked file modification" debug.txt

# Files written
grep "written atomically" debug.txt

# Snapshot creation
grep "FileHistory: Making snapshot" debug.txt
```

**What it reveals**:
- Which files were actually modified
- When modifications occurred
- Edit patterns (multiple edits to same file)

**Signal-to-noise**: 8/10 - Shows what changed, not why

---

## ⭐ Medium Signal: Permission Flows

**Purpose**: Identify blocked operations

**Patterns**:
```bash
# Permission requests
grep -A10 "Permission suggestions" debug.txt

# Find blocks (PreToolUse without PostToolUse)
grep "executePreToolHooks" debug.txt
grep "PostToolUse" debug.txt
# If counts don't match, something was blocked
```

**What it reveals**:
- What operations required permission
- Whether user granted or denied
- What Claude attempted but couldn't complete

**Signal-to-noise**: 6/10 - Useful for understanding blockers, but doesn't show outcome

---

## Additional Useful Patterns

### Git Log Integration
```bash
# Get commits for a day
git log --since="2025-11-05 00:00:00" --until="2025-11-05 23:59:59" \
  --pretty=format:"%h - %s (%cr)" --date=relative

# Get detailed commit with changes
git log --since="2025-11-05 00:00:00" --stat --pretty=format:"%n%h - %s%n%b"
```

**Signal-to-noise**: 9/10 - Ground truth for what actually changed

### Tool Usage Counts (Debug Logs)
```bash
grep "executePreToolHooks" debug.txt | sed 's/.*tool: //' | sort | uniq -c
```

**Signal-to-noise**: 7/10 - Shows Claude's strategy pattern

### Timeline Extraction (Debug Logs)
```bash
grep -n "UserCommandMessage\|executePreToolHooks\|Permission suggestions" debug.txt
```

**Signal-to-noise**: 6/10 - Shows sequence but lacks context

---

## Correlation Strategy

**Highest value**: Combine multiple sources
1. JSONL logs → WHY (user intent, Claude reasoning)
2. Debug logs → WHAT (tool usage, file changes)
3. Git history → GROUND TRUTH (actual commits)

**Workflow**:
1. Extract user journey from JSONL
2. Extract thinking blocks for insights
3. Correlate with debug log tool usage
4. Verify with git log commits
5. Generate narrative combining all sources
