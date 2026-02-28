# Section Population Guide

## Contents
- [Template Structure](#template-structure)
- [Always Include](#always-include)
- [Conditionally Include](#conditionally-include)
- [Section Decision Logic](#section-decision-logic)

When generating journal drafts, use this guide to determine which sections to include:

## Template Structure

The Daily Log template has four main sections:

1. **Summary** - One-line main focus
2. **Notes** - What happened (with subsections)
3. **Reflection** - What worked, what didn't, open questions, tomorrow's focus
4. **Related** - Linked project notes

## Always Include

**YAML frontmatter:** date and tags

**Summary:** One-line focus from first context message
- If no context available, use placeholder: `_One-line: main focus for today_`

**Notes:** Container section for what happened
- Always present, even if subsections are empty

**Day Footer:** Horizontal rule + italicized one-liner closing out the day
- Format: `*{Day character} - {One-line takeaway}*`
- Always include when closing off an entry at end of day
- Goes after last content section, before Related links

**Related:** Project links section
- If project detected: `- [[Project Name]]`
- If no project: `_Add links to related project notes_`

## Conditionally Include

**Notes subsections:**

**### Goals:** Include if todos exist
- From TodoWrite tool uses or early user messages
- Checkbox format with status grouping

**### Technical Work:** Include if:
- Git commits exist for the day
- Files were modified (Edit/Write tools used)
- Format: Bold headers for "Git Commits:" and "Files Modified:"

**### Commands:** Include if:
- 3+ significant bash commands run
- Exclude trivial commands (ls, cat, cd)
- Format as code block with optional descriptions

**## Reflection:** Include if:
- Mode is "full", OR
- Open questions exist (auto mode)
- Contains: Open Questions, What worked, What didn't, Tomorrow's focus

## Section Decision Logic

**Auto mode (recommended):**
- Always: frontmatter, Summary, Notes, Related
- Conditionally: Goals/Technical Work/Commands subsections under Notes
- Conditionally: Reflection (only if open questions exist)
- Result: Clean, relevant journal without empty sections

**Full mode:**
- Include all sections
- Add placeholders for manual completion
- Best for deep work days needing reflection

**Quick mode:**
- Only: YAML, Summary, Notes (Goals + Technical Work), Related
- Minimal structure for operational days
