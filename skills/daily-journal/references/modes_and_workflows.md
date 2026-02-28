# Journal Modes and Workflows

## Contents
- [Journal Modes](#journal-modes)
- [Draft-Review-Write Workflow](#draft-review-write-workflow)
- [Handling Raw Content](#handling-raw-content)
- [Integration with Obsidian Vault Skill](#integration-with-obsidian-vault-skill)

## Journal Modes

### Batch Mode (End of Day)

Traditional workflow using log analysis scripts:

1. Run `uv run ~/.claude/skills/daily-journal/scripts/collect_day_data.py` to get session summary
2. Review active sessions
3. Compile findings into journal entry

**Best for:** Comprehensive review of complex work days

### Draft Mode (Active Assistance)

Generate complete journal draft for review:

1. Run `uv run ~/.claude/skills/daily-journal/scripts/collect_day_data.py`
2. Review draft markdown output
3. Edit/refine as needed
4. Save to Obsidian vault

**Best for:** Quick journal generation with flexible structure

### Incremental Mode (Throughout Day)

Build journal entry progressively during work (requires slash command):

1. Use `/daily-journal append` to add sections during work
2. Use `/daily-journal organize` when content is raw
3. Review and finalize at end of day

**Best for:** Active work days where you want real-time journaling

## Draft-Review-Write Workflow

**Step 1: Generate Draft**

```bash
uv run scripts/collect_day_data.py --date YYYY-MM-DD
```

**Step 2: Review Output**

- Check that sections are relevant
- Verify todos and context are accurate
- Ensure commands and files are complete
- Add missing reflections or next steps

**Step 3: Write to Obsidian**

With Claude's help (hybrid):

```
User: "Draft today's journal"
Claude: [Generates and shows draft]
User: "Looks good, write it to my vault"
Claude: [Uses obsidian-vault skill to write file]
```

## Handling Raw Content

If today's journal exists but is unstructured (just commands/notes):

**Detection:**

- No H2 headers (##)
- Mostly code blocks
- No YAML frontmatter

**Claude's response:**
"I see today's journal has raw content. Would you like me to organize it into structured sections?"

**If yes:**

1. Extract commands -> "Commands Used" section
2. Group by topic -> Create relevant H2 sections
3. Add YAML frontmatter and tags
4. Show organized version for approval

**If no:**

- Leave as-is (raw dumps are legitimate)

## Integration with Obsidian Vault Skill

When user approves writing journal to Obsidian:

**Workflow:**

1. Claude generates draft using daily-journal skill
2. Shows draft to user for review
3. User approves ("write it" or "looks good")
4. Claude uses obsidian-vault skill to write file with proper formatting
5. Confirms: "Journal written to Daily Log/YYYY-MM-DD.md"
