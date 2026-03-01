# Obsidian Vault Structure

This document defines the folder hierarchy, naming conventions, and organization rules for the Obsidian vault.

<!-- Set your vault path in the skill description or CLAUDE.md -->

## Contents

- [Obsidian Vault Structure](#obsidian-vault-structure)
  - [Contents](#contents)
  - [Folder Hierarchy](#folder-hierarchy)
    - [Folder Purposes](#folder-purposes)
  - [Attachment Storage Rules](#attachment-storage-rules)
  - [File Naming Conventions](#file-naming-conventions)
    - [Regular Notes](#regular-notes)
    - [Daily Notes](#daily-notes)
    - [Meeting Notes](#meeting-notes)
  - [Index Files and Waypoint Plugin](#index-files-and-waypoint-plugin)
  - [Note Placement Decision Tree](#note-placement-decision-tree)
  - [Folder Creation Rules](#folder-creation-rules)
  - [Tag Organization](#tag-organization)
  - [Cross-Folder Linking](#cross-folder-linking)
  - [Ambiguous Cases](#ambiguous-cases)
  - [Quality Guidelines](#quality-guidelines)

## Folder Hierarchy

The vault uses this top-level folder structure:

<!-- Customize this to match your vault. Add/remove folders as needed. -->

```
Obsidian-Notes/
├── Programming/
│   ├── Python/
│   └── attachments/
├── Projects/
│   └── attachments/
├── Daily Log/
│   └── attachments/
└── Templates/
```

### Folder Purposes

**Programming/**
- General programming concepts, languages, tools
- Subfolders for specific languages (Python/, Rust/)
- Technical documentation, code patterns, tool usage

**Projects/**
- Project-specific notes and documentation
- Active and archived project content

**Daily Log/**
- Daily notes with date-based naming
- Meeting notes
- Work logs and progress tracking

**Templates/**
- Note templates for reuse
- Frontmatter templates
- Structure examples

## Attachment Storage Rules

**Folder-specific attachments:**
- Each main folder has its own `attachments/` subfolder
- Images and files are stored in the `attachments/` folder of their topic area
- Example: Python-related images -> `Programming/attachments/`

**File naming for attachments:**
- Use descriptive names
- Include context about what the image shows
- Example: `docker_architecture_diagram.png`, `pandas_groupby_diagram.svg`

## File Naming Conventions

### Regular Notes

**Format:** Descriptive name with spaces allowed

**Examples:**
- `Python Decorators.md`
- `Docker Tips.md`
- `Git Best Practices.md`

**Rules:**
- Use descriptive, clear names
- Spaces are allowed and preferred for readability
- Title case for proper nouns and first letter
- The filename serves as the title - no H1 header inside the note

### Daily Notes

**Format:** `YYYY-MM-DD.md`

**Location:** `Daily Log/` folder

**Examples:**
- `2025-02-26.md`
- `2025-10-21.md`

**Rules:**
- Always use ISO date format (YYYY-MM-DD)
- Stored exclusively in `Daily Log/` folder
- Created automatically or manually for daily logs
- May include meeting notes, work progress, daily reflections

### Meeting Notes

**Format:** `YYYY-MM-DD - Meeting Topic.md`

**Location:** Typically in `Daily Log/` or relevant topic folder

**Example:**
- `2025-10-21 - Sprint Review.md`

**Rules:**
- Start with ISO date
- Follow with descriptive meeting topic
- Can be stored in Daily Log/ or moved to relevant topic folder if the content becomes reference material

## Index Files and Waypoint Plugin

Several index files (e.g., `Programming.md`) use the Waypoint plugin to automatically generate folder content listings.

**Important:** Content between `%% Begin Waypoint %%` and `%% End Waypoint %%` markers is automatically managed by the plugin.

**Never manually modify content within these markers.**

Example:
```markdown
# Programming

Overview of programming topics...

%% Begin Waypoint %%
- [[Python]]
- [[Git Best Practices]]
- [[Docker Tips]]
%% End Waypoint %%
```

The Waypoint plugin will automatically update the list of links based on folder contents.

## Note Placement Decision Tree

When creating or organizing notes:

1. **Is it a daily log or meeting note?**
   - YES -> `Daily Log/` with date prefix
   - NO -> Continue

2. **What is the primary topic?**
   - Programming concepts/tools -> `Programming/` (or subfolder)
   - Project-specific -> `Projects/`
   <!-- Add your own topic folders to this decision tree -->

3. **Is there a more specific subfolder?**
   - Python-specific -> `Programming/Python/`
   - UNIX/shell-specific -> `Programming/UNIX/`
   - If no specific subfolder, place in main topic folder

4. **Could it fit in multiple folders?**
   - Choose based on **primary focus**
   - Create links from related index files
   - Use tags to indicate cross-cutting concerns

## Folder Creation Rules

**When to create new folders:**
- A topic has accumulated 5+ related notes
- Clear subcategory emerges (like Python/ within Programming/)
- Logical grouping improves organization

**When NOT to create new folders:**
- Only 1-2 notes in the category
- Topic is closely related to existing folder
- Would create too much nesting (max 2 levels preferred)

**Naming new folders:**
- Use existing naming pattern (Title Case, descriptive)
- Keep names concise but clear
- Avoid abbreviations unless universally known

## Tag Organization

Tags are defined in YAML frontmatter and follow these categories:

**Technical tags:**
- `python`, `data_processing`, `unix`, `shell`, `git`, `docker`

**Tools:**
- `pandas`, `numpy`, `matplotlib`, `jupyter`

**Content types:**
- `meeting_notes`, `concepts`, `tools`, `analysis`, `tutorial`, `reference`, `troubleshooting`

<!-- Add your own domain-specific tags here -->

**Best practices:**
- Use existing tags when possible
- Create new tags sparingly
- Use lowercase with underscores
- Keep tags specific and meaningful

## Cross-Folder Linking

**When notes relate across folders:**
- Use `[[Note Title]]` syntax to create bidirectional links
- Mention related concepts in both notes
- Consider if one note should reference the other in its content

**Example:**
- `Programming/Python/Pandas.md` might link to `Projects/Data Pipeline.md`

## Ambiguous Cases

**Multiple valid locations:**
- Choose primary focus
- Use tags to indicate secondary topics
- Link from related index files

**Very long notes (>500 lines):**
- Consider splitting into focused sub-notes
- Create a main note with links to detailed sub-notes
- Use folder structure to organize related sub-notes

**Duplicate content:**
- Consolidate into single authoritative note
- Update links from old notes
- Add redirects or merge information

## Quality Guidelines

**Before creating any note:**
- Search for existing related content
- Verify correct folder placement
- Ensure attachments go in correct folder's attachments/
- Use proper naming convention
- Include YAML frontmatter with tags

**Maintaining organization:**
- Review folder structure periodically
- Consolidate duplicate content
- Update links when moving notes
- Keep Waypoint sections untouched (auto-managed)
