---
name: obsidian-vault
description: Manage Obsidian vault operations. Handles markdown formatting, YAML frontmatter, folder organization, internal linking, and vault-specific conventions. Use when creating, updating, or organizing Obsidian notes.
---

# Obsidian Vault

## Overview

This skill provides vault-specific knowledge and technical operations for managing an Obsidian vault. It handles markdown formatting, YAML frontmatter structure, folder hierarchy, attachment organization, and internal linking conventions specific to the vault structure.

## When to Use This Skill

Use this skill when:
- Creating new notes in the Obsidian vault
- Updating existing notes with proper formatting
- Organizing notes into correct folder hierarchy
- Managing attachments and images
- Formatting YAML frontmatter with appropriate tags
- Creating internal links between notes
- Following vault-specific naming conventions
- Ensuring notes meet quality and structure standards

## Core Capabilities

### 1. Vault Structure and Organization

Understand and apply the folder hierarchy defined for the vault:

**Main folders:**
- `Programming/` - Code concepts, languages, tools (subfolders: Python/, UNIX/)
- `Projects/` - Project-specific notes and documentation
- `Daily Log/` - Daily notes and meeting logs
- `Templates/` - Note templates

<!-- Add your own topic folders here (e.g., Research/, Art/, Recipes/) -->

**See `references/vault_structure.md`** for complete hierarchy, placement rules, and decision trees.

### 2. File Naming Conventions

Apply proper naming based on note type:

**Regular notes:**
- Format: Descriptive name with spaces
- Examples: `Python Decorators.md`, `Docker Tips.md`
- Rule: Filename serves as title (no H1 header inside)

**Daily notes:**
- Format: `YYYY-MM-DD.md`
- Location: `Daily Log/` folder
- Examples: `2025-02-26.md`, `2025-10-21.md`

**Meeting notes:**
- Format: `YYYY-MM-DD - Meeting Topic.md`
- Location: `Daily Log/` or relevant topic folder
- Example: `2025-10-21 - Sprint Review.md`

**See `references/vault_structure.md`** for complete naming rules and conventions.

### 3. Markdown Formatting Standards

Format notes according to vault-specific markdown conventions:

**YAML Frontmatter (required):**
```yaml
---
tags:
  - relevant_tag1
  - relevant_tag2
---
```

**Header hierarchy:**
- NO H1 (`#`) - filename is the title
- Start with H2 (`##`) for main sections
- Use H3 (`###`) for subsections

**Internal linking:**
- Use `[[Note Title]]` for wiki-links
- **READ target notes before linking** - verify relevance from actual content, not just titles
- Only link when there's genuine topical overlap with specific content justification
- Never guess link relevance from note titles alone
- Remove links that seem related by title but aren't after reading content
- Create connections between related notes
- Link to related concepts

**Code blocks:**
- Use fenced blocks with language specification
- Include working examples

**See `references/markdown_formatting.md`** for comprehensive formatting guide, callouts, tables, and content patterns.

### 4. Attachment Management

Store and reference images/files correctly:

**Storage location:**
- Folder-specific: Each main folder has `attachments/` subfolder
- Example: Programming images -> `Programming/attachments/`

**Referencing:**
```markdown
![Alt text](attachments/image_name.png)
```

**Naming:**
- Use descriptive names for images
- Include context: `docker_architecture_diagram.png`

### 5. Semantic Search

Use [`obsidian-semantic`](https://github.com/ravila4/obsidian-semantic) to find existing notes by meaning, not just keywords.

```bash
# Find notes about a topic
obsidian-semantic search "dependency injection patterns" -n 5

# Find notes related to a specific note
obsidian-semantic related "Programming/Python/Unit Testing.md" -n 5

# Search within a folder
obsidian-semantic search "docker" --folder "Programming/"

# Filter by tag
obsidian-semantic search "habits" --tag "review"
```

**When to use `search`:** Before creating new notes (check for duplicates/related content), when looking for notes to link to, when user asks to find notes on a topic.

**When to use `related`:** After creating/updating a note to suggest links, when user asks "what's related to X?"

### 6. Tag System

Apply appropriate tags from established taxonomy:

**Tag categories:**
- **Technical:** `python`, `docker`, `git`, `data_processing`
- **Tools:** `pandas`, `numpy`, `matplotlib`, `jupyter`
- **Content types:** `meeting_notes`, `concepts`, `tools`, `analysis`, `reference`, `tutorial`, `troubleshooting`

<!-- Add your own domain-specific tags here -->

**Selection rules:**
- Choose 2-5 relevant tags
- Include domain/technical tag
- Include content type when appropriate
- Use lowercase with underscores

**See `references/markdown_formatting.md`** for complete tag catalog and guidelines.

## Workflow

When creating or updating notes:

1. **Determine note type** - Regular, daily, or meeting note
2. **Choose location** - Use folder decision tree from `references/vault_structure.md`
3. **Name appropriately** - Follow naming conventions for note type
4. **Create frontmatter** - Add YAML with relevant tags
5. **Format content** - Apply markdown standards from `references/markdown_formatting.md`
6. **Add internal links** - Connect to related notes
7. **Store attachments** - Place in correct folder's `attachments/` subfolder
8. **Verify quality** - Check against standards

## Resources

### references/

**vault_structure.md** - Complete folder hierarchy, file naming conventions, attachment storage rules, folder placement decision tree, tag catalog, and organization guidelines. Load when determining where notes should be placed or how they should be named.

**markdown_formatting.md** - YAML frontmatter structure, markdown formatting standards, header hierarchy rules, internal linking syntax, code blocks, callouts, tables, content organization patterns, and quality guidelines. Load when creating or formatting note content.

## Quality Standards

All notes must:
- Include YAML frontmatter with relevant tags
- Follow naming conventions for note type
- Be placed in correct folder hierarchy
- Use NO H1 header (filename is title)
- Start content with H2 headers
- Include internal links to related notes
- Store attachments in correct folder's `attachments/` subfolder
- Follow markdown formatting standards
- Be focused and avoid duplication

## Common Operations

### Creating a New Note

1. Search vault with `obsidian-semantic search "<topic>" -n 5` for existing related content
2. Decide: extend existing or create new
3. Determine correct folder from hierarchy
4. Choose appropriate filename
5. Add YAML frontmatter with tags
6. Format content with H2+ headers
7. Include code examples if technical
8. Add internal links (use `obsidian-semantic related "<note_path>" -n 5` to find candidates)
9. Store any images in folder's `attachments/`

### Updating an Existing Note

1. Verify YAML frontmatter is present
2. Check tags are appropriate
3. Ensure no H1 header duplicating filename
4. Add internal links to new related notes
5. Format new content consistently
6. Update any moved images to correct attachments folder

### Organizing Content

1. Review folder placement (see decision tree)
2. Verify attachments are in correct location
3. Check internal links are valid
4. Ensure tags reflect current taxonomy
5. Consider splitting if note >500 lines
6. Consolidate duplicate content if found

## Waypoint Plugin Awareness

**Important:** Index files use Waypoint plugin for auto-generated content listings.

**Never modify content between:**
```markdown
%% Begin Waypoint %%
...
%% End Waypoint %%
```

These sections are automatically managed by the plugin.

## Integration with Other Skills

**Diagram tools (Mermaid, Graphviz, TikZ, etc.):**
- Store rendered diagrams in the appropriate `attachments/` subfolder
- Embed diagrams in notes using image links

## Best Practices

1. **Search before creating** - Avoid duplication
2. **Follow hierarchy** - Use established folder structure
3. **Be consistent** - Apply formatting standards uniformly
4. **Link generously** - Create knowledge connections
5. **Verify links by reading** - Never add links based on note titles alone; always read target notes first
6. **Tag appropriately** - Use existing taxonomy
7. **Keep focused** - One main topic per note
8. **Include examples** - Make notes practical
9. **Organize attachments** - Folder-specific storage
10. **No redundant H1** - Filename is the title
11. **Respect Waypoint** - Don't modify auto-generated sections

## Validation Checklist

Before finalizing any note:
- [ ] Searched for existing related content
- [ ] Placed in correct folder
- [ ] Used proper naming convention
- [ ] Included YAML frontmatter with tags
- [ ] No H1 header (filename is title)
- [ ] Used H2 for main sections
- [ ] Added internal links to related notes
- [ ] Verified each link's relevance by reading target note content (never guess from titles)
- [ ] Stored attachments in folder's `attachments/`
- [ ] Included practical examples for technical content
- [ ] Checked for quality and focus
