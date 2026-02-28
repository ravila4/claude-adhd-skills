# Limitations and Caveats

Critical warnings about what logs can and cannot tell you. Understanding limitations prevents false conclusions.

## Contents

- [Critical Limitation: Privacy Protection](#critical-limitation-privacy-protection)
- [Log Format Limitations](#log-format-limitations)
- [Inference Limitations](#inference-limitations)
- [Common Pitfalls](#common-pitfalls)
- [Correlation Challenges](#correlation-challenges)
- [Best Practices for Accurate Analysis](#best-practices-for-accurate-analysis)
- [The "What We Know vs Don't Know" Framework](#the-what-we-know-vs-dont-know-framework)
- [When to Skip Analysis](#when-to-skip-analysis)
- [Final Warning: Logs Are Not Mind Reading](#final-warning-logs-are-not-mind-reading)

## Critical Limitation: Privacy Protection

### Debug Logs Contain NO Conversation Content

**What's missing**:
- User prompts (what you asked Claude)
- Claude's responses (what Claude said)
- File contents that were read
- Tool outputs/results

**What's included**:
- Tool invocations (names only)
- Permission requests (structure only)
- Hook lifecycle events
- File modification tracking (paths, not content)

**Impact**: Cannot determine user intent directly from debug logs. Must infer from:
- Tool usage patterns
- Permission requests
- File modification sequences
- JSONL correlation

### Example of Inference Required

**Debug log shows**:
```
executePreToolHooks: Read (2x)
Permission suggestion: uv tool install:*
Stop event
SessionEnd
```

**Cannot determine**:
- What user asked for
- Which files were read
- What tool to install
- Why user stopped

**Must infer**:
- User requested something requiring installation
- Claude gathered context (2 reads)
- User stopped before granting permission
- Possible reasons: Changed mind / Got info from reads / Wanted to review

---

## Log Format Limitations

### 1. No Timestamps in Debug Logs

Debug logs have no explicit timestamps, only implicit ordering.

**Cannot determine**:
- Exact time of events
- Duration of operations
- Time between events

**Workaround**: Use file modification times for rough timing.

### 2. No Tool Results

See tool invocations but not outputs.

**Cannot determine**:
- What grep found
- What Read returned
- Error messages from Bash
- Search results from Glob

**Workaround**: Check file modifications and git commits for results.

### 3. Permission Outcomes Ambiguous

Debug logs show permission requests but not outcomes.

**Cannot definitively tell**:
- If permission was granted
- If permission was denied
- If user ignored the request

**Workaround - The .claude.json Size Trick**:
```bash
# Check config file size before/after session
ls -l ~/.claude.json

# If size increased during session = likely granted
# If size unchanged = likely not granted

# Verify by checking content
jq '.permissions' ~/.claude.json | grep "ruleContent"
```

### 4. JSONL Mixed Entry Types

JSONL files contain both messages and snapshots.

**Pitfall**: Not all lines are messages.

**Solution**:
```python
data = json.loads(line)
if 'message' in data:
    # It's a message
    msg = data['message']
elif data.get('type') == 'file-history-snapshot':
    # It's a snapshot, skip for conversation analysis
    continue
```

### 5. Content Format Evolution

Early JSONL entries may have string content, later ones have array format.

**Pitfall**: Assuming content is always a list.

**Solution**:
```python
content = msg.get('content', '')
if isinstance(content, str):
    text = content
elif isinstance(content, list):
    for block in content:
        if block.get('type') == 'text':
            text = block.get('text')
```

---

## Inference Limitations

### Cannot Determine from Logs Alone

**1. User Satisfaction**
- Did user get what they needed?
- Was session successful?
- Would user be satisfied with results?

**2. Actual Intent**
- Why did user ask this specific question?
- What's the broader context?
- What will they do with the information?

**3. Quality of Results**
- Was code correct?
- Were tests sufficient?
- Did solution meet requirements?

**4. Session Classification**
- Is incomplete work abandoned or in-progress?
- Was blocked permission intentional or accidental?
- Was minimal session testing or real work?

### Must Make Educated Guesses

Use multiple signals:
- Tool patterns
- Permission requests
- File modifications
- Git commits
- Prior knowledge of project

---

## Common Pitfalls

### Pitfall 1: Assuming Permission Denial

**Wrong**: "Permission was requested and session ended, so user denied it."

**Reality**: User might have:
- Gotten needed info from Read operations
- Wanted to review before granting
- Been interrupted
- Changed their mind
- Already gotten the answer

**Check**: `.claude.json` size and git status

### Pitfall 2: Equating Tool Use with Success

**Wrong**: "Edit tool was used, so code was changed correctly."

**Reality**: Edit might have:
- Failed
- Been reverted
- Been blocked by hook
- Created buggy code

**Check**: Git commits and test results

### Pitfall 3: Ignoring Context

**Wrong**: "High tool usage means productive session."

**Reality**: Might indicate:
- Thrashing (trying many approaches)
- Confusion (searching extensively)
- Complex problem (legitimately needed many tools)

**Check**: Tool sequences and thinking blocks

### Pitfall 4: Over-interpreting Permission Requests

**Wrong**: "Permission for 'uv tool install:*' means user wanted to install uvicorn."

**Reality**: Wildcard means ANY tool via uv. Could be:
- ruff
- pytest
- mypy
- black
- Any other Python tool

**Check**: JSONL for context

### Pitfall 5: Missing File Modifications

**Wrong**: "No 'Tracked file modification' means no changes made."

**Reality**: Might have:
- Modified files outside tracked directory
- Used Write instead of Edit (different tracking)
- Created new files (tracked differently)

**Check**: Git status and commits

---

## Correlation Challenges

### Challenge 1: Session ID Matching

Debug logs and JSONL use different session identifiers.

**Problem**: Hard to match debug log with JSONL log.

**Solution**:
```bash
# Extract session ID from debug log filename
DEBUG_SESSION=$(basename debug.txt .txt)

# Search for JSONL containing that ID
find ~/.claude/projects -name "*${DEBUG_SESSION}*.jsonl"
```

### Challenge 2: Multiple Sessions Per Day

Many short sessions can create confusion.

**Problem**: Which session accomplished what?

**Solution**:
- Use tool counts to identify major sessions
- Check git log timestamps
- Look for file modification patterns

### Challenge 3: Fragmented Work

Work spread across multiple sessions.

**Problem**: Single task spans multiple logs.

**Solution**:
- Group by timestamp proximity
- Follow git branch activity
- Track file modification continuity

---

## Best Practices for Accurate Analysis

### 1. Always Verify with Git

Git is ground truth. If logs say Edit happened but no git commit exists, the edit likely failed or was reverted.

### 2. Cross-Reference Multiple Sources

No single source tells complete story:
- Debug logs: Tool usage patterns
- JSONL: User intent and reasoning
- Git: Actual changes made
- File system: Current state

### 3. Make Inferences Explicit

When inferring user intent:
```markdown
**Hypothesis**: User wanted to install dependencies.
**Evidence**: Read pyproject.toml, then requested uv tool install.
**Uncertainty**: Don't know which specific tool.
```

### 4. Note What's Unknown

```markdown
**Known**: Permission requested for Bash command.
**Unknown**: Whether permission was granted, why user stopped.
**Unresolved**: Actual user goal.
```

### 5. Use Confidence Levels

- **High confidence**: Git commit shows X was changed
- **Medium confidence**: Tool pattern suggests Y approach
- **Low confidence**: Inferred Z from permission request

---

## The "What We Know vs Don't Know" Framework

For every session, explicitly list:

### What We Know (from logs)
- Tool invocations
- File tracking events
- Permission requests
- Git commits

### What We Don't Know
- User's actual words
- Tool results
- Permission outcomes
- User's thought process

### What We Can Infer
- Likely user intent (from tool patterns)
- Probable outcomes (from git)
- Possible reasons (from sequences)

### What Remains Mystery
- Specific motivations
- Satisfaction level
- Future plans

---

## When to Skip Analysis

Some sessions don't warrant deep analysis:

### Skip If:
1. **Minimal/testing session** (0-2 interactions, no work done)
2. **Duplicate session** (immediately re-opened, same content)
3. **Accidental session** (/exit immediately after open)
4. **No JSONL available** (can't determine intent without conversation)

### Focus Effort On:
1. Active working sessions (3+ interactions, commits made)
2. Blocked sessions with interesting permission requests
3. Sessions with substantial tool usage
4. Sessions resulting in significant git commits

---

## Final Warning: Logs Are Not Mind Reading

**Remember**:
- Logs show actions, not motivations
- Tools used ≠ work accomplished
- Permission requested ≠ intent understood
- Session ended ≠ work completed

Always leave room for uncertainty in analysis.

**Good practice**:
```markdown
**Context**: Goal appeared to be X based on tool pattern Y.
**Status**: Unresolved - unclear if goal was achieved.
**Note**: User stopped before expected completion.
```

**Bad practice**:
```markdown
**Context**: User wanted X and achieved it.
**Status**: Complete.
```

When in doubt, express uncertainty.
