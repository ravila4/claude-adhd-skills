# Obsidian Markdown Formatting Guide

This document defines the markdown formatting standards, YAML frontmatter structure, and content patterns for notes in the Obsidian vault.

## Contents

- [YAML Frontmatter](#yaml-frontmatter)
- [Note Title Rules](#note-title-rules)
- [Header Hierarchy](#header-hierarchy)
- [Internal Linking](#internal-linking)
- [Code Blocks](#code-blocks)
- [Lists](#lists)
- [Callouts/Admonitions](#calloutsadmonitions)
- [Tables](#tables)
- [Embedding Images](#embedding-images)
- [Emphasis and Formatting](#emphasis-and-formatting)
- [Blockquotes](#blockquotes)
- [Content Organization Patterns](#content-organization-patterns)
- [Content Quality Guidelines](#content-quality-guidelines)
- [Maintenance Patterns](#maintenance-patterns)

## YAML Frontmatter

Every note must include YAML frontmatter at the top of the file.

### Standard Format

```yaml
---
tags:
  - tag1
  - tag2
  - tag3
---
```

### Tag Guidelines

**Use existing tags when possible** - See `vault_structure.md` for full tag catalog

**Tag selection rules:**
1. Choose 2-5 relevant tags
2. Include at least one technical/domain tag
3. Include a content type tag when appropriate
4. Use lowercase with underscores
5. Be specific but not overly granular

### Examples

**Python programming note:**
```yaml
---
tags:
  - python
  - pandas
  - data_processing
  - reference
---
```

**Meeting notes:**
```yaml
---
tags:
  - meeting_notes
  - project_name
---
```

## Note Title Rules

**CRITICAL:** The filename serves as the note title

**NEVER include an H1 (`#`) header** inside the note that duplicates the filename

**Correct:**
```
Filename: Python Decorators.md

---
tags:
  - python
  - concepts
---

Decorators are a powerful feature in Python...

## Basic Syntax

...
```

**Wrong:**
```
Filename: Python Decorators.md

---
tags:
  - python
---

# Python Decorators   <-- NEVER DO THIS

Decorators are a powerful feature...
```

**Rationale:** Obsidian displays the filename as the note title. Adding an H1 creates redundancy and visual clutter.

## Header Hierarchy

Start content with H2 (`##`) as the highest level header.

**Standard structure:**
```markdown
---
tags:
  - relevant_tags
---

Brief introduction or overview paragraph...

## Main Section 1

Content...

### Subsection 1.1

Details...

### Subsection 1.2

More details...

## Main Section 2

More content...
```

**Header guidelines:**
- Use H2 (`##`) for main sections
- Use H3 (`###`) for subsections
- Rarely use H4 (`####`) or deeper
- Keep hierarchy logical and not too deep

## Internal Linking

Use Obsidian's wiki-link syntax to connect notes.

### Basic Linking

```markdown
See [[Note Title]] for more information.

Related concepts: [[Python]], [[Data Processing]], [[Pandas]]
```

### Section Linking

```markdown
For details, see [[Python Decorators#Basic Syntax]]
```

### Alias Linking

```markdown
The [[API Gateway|gateway service]] handles routing...
```

### Linking Guidelines

**When to create links:**
- Mentioning another note topic
- Referencing related concepts
- Cross-referencing between domains
- Building knowledge connections

**Link placement:**
- Inline within sentences (natural flow)
- Dedicated "Related Notes" section at bottom
- Within list items for organization

**Example with multiple link styles:**
```markdown
When working with [[Pandas]], understanding [[Python#Data Types]] is essential.

## Related Concepts

- [[NumPy]] - Array operations
- [[Matplotlib]] - Data visualization
- [[Data Cleaning]] - Preprocessing techniques
```

## Code Blocks

Use fenced code blocks with language specification for syntax highlighting.

### Python Code

````markdown
```python
import pandas as pd

df = pd.read_csv('data.csv')
df.groupby('category').mean()
```
````

### Shell Commands

````markdown
```bash
# Run the test suite
pytest tests/ -v --tb=short
```
````

### Inline Code

Use single backticks for inline code references:

```markdown
The `pandas.DataFrame.groupby()` method aggregates data efficiently.

Use the `--verbose` flag for detailed output.
```

## Lists

### Unordered Lists

```markdown
- First item
- Second item
  - Nested item
  - Another nested item
- Third item
```

### Ordered Lists

```markdown
1. First step
2. Second step
   1. Sub-step
   2. Another sub-step
3. Third step
```

### Task Lists

```markdown
- [x] Completed task
- [ ] Pending task
- [ ] Another pending task
```

## Callouts/Admonitions

Obsidian supports various callout types (also called admonitions) for emphasis. Each has a different color and icon.

### Informational Callouts

**Note** - General notes and information
```markdown
> [!note]
> This is an important note to remember.
```

**Info/Todo** - Information or action items
```markdown
> [!info]
> The dataset contains 500K samples.

> [!todo]
> Need to validate these results with external data.
```

**Abstract/Summary/TLDR** - Summaries and overviews
```markdown
> [!summary]
> Key takeaway: Use caching to reduce API calls by 80%.
```

**Tip/Hint/Important** - Helpful tips and best practices
```markdown
> [!tip]
> Pro tip: Use keyboard shortcuts to speed up workflow.

> [!important]
> Always validate input data before processing.
```

**Example** - Code examples and demonstrations
```markdown
> [!example]
> Here's how to use the groupby function:
> ```python
> df.groupby('category').sum()
> ```
```

### Success/Completion Callouts

**Success/Check/Done** - Successful completion
```markdown
> [!success]
> Migration completed successfully with zero data loss.
```

### Question Callouts

**Question/Help/FAQ** - Questions or areas needing clarification
```markdown
> [!question]
> Is this the right abstraction for this use case?

> [!faq]
> **Q: What is dependency injection?**
> A: A design pattern where dependencies are provided to a class rather than created by it.
```

### Warning Callouts

**Warning/Caution/Attention** - Warnings and cautions
```markdown
> [!warning]
> Be careful with this approach - it can cause race conditions.

> [!caution]
> This API is deprecated and will be removed in v3.0.
```

### Error Callouts

**Failure/Fail/Missing** - Failures or missing information
```markdown
> [!failure]
> This method failed due to insufficient memory.

> [!missing]
> Documentation for this endpoint is not available.
```

**Danger/Error** - Critical errors
```markdown
> [!danger]
> This will delete all records - cannot be undone.

> [!error]
> Pipeline failed: Invalid configuration.
```

**Bug** - Known bugs or issues
```markdown
> [!bug]
> Known issue: Connection pool exhaustion under high load.
```

### Quote Callouts

**Quote/Cite** - Quotations and citations
```markdown
> [!quote]
> "Premature optimization is the root of all evil."
> -- Donald Knuth
```

### Callout Features

**Collapsible callouts** - Add a `+` or `-` to make them foldable:
```markdown
> [!note]- Click to expand
> Hidden content here...

> [!example]+ Expanded by default
> This starts open but can be collapsed.
```

**Titles** - Customize the callout title:
```markdown
> [!tip] Performance Optimization
> Use batching to process multiple items simultaneously.
```

**Nested callouts** - Callouts can contain other callouts:
```markdown
> [!info] Data Sources
> We use multiple datasets:
>
> > [!example] Primary Dataset
> > 500K records with full metadata
```

## Tables

Use markdown tables for structured data:

```markdown
| Parameter | Type | Description |
|-----------|------|-------------|
| --verbose | flag | Enable detailed output |
| --output  | path | Output file path |
| --workers | int  | Number of parallel workers |
```

**Table guidelines:**
- Use for structured, tabular information
- Keep tables reasonably sized (< 10 columns)
- Align headers clearly
- Consider lists for simple key-value pairs

## Embedding Images

Reference images from the appropriate `attachments/` folder:

```markdown
![Alt text description](attachments/image_name.png)
```

**Image guidelines:**
- Store in topic folder's `attachments/` subfolder
- Use descriptive alt text
- Include captions when helpful
- Keep images reasonably sized

**Example:**
```markdown
The architecture diagram shows the service layout:

![Service architecture diagram](attachments/service_architecture.png)

*Figure 1: Microservice communication flow*
```

## Emphasis and Formatting

### Bold

```markdown
**Important concept** or __alternative syntax__
```

### Italic

```markdown
*Emphasis* or _alternative syntax_
```

### Bold + Italic

```markdown
***Very important*** or ___alternative___
```

### Strikethrough

```markdown
~~Deprecated approach~~
```

## Blockquotes

```markdown
> This is a quote from a paper or documentation.
> It can span multiple lines.

-- Author Name (if applicable)
```

## Content Organization Patterns

### Concept Notes

```markdown
---
tags:
  - concepts
  - relevant_domain
---

Brief definition or overview...

## Background

Context and foundational information...

## Key Concepts

Main ideas explained...

## Examples

Practical examples with code...

## Related Notes

- [[Related Topic 1]]
- [[Related Topic 2]]
```

### Tool/Technology Notes

```markdown
---
tags:
  - tools
  - relevant_domain
---

What it is and what it does...

## Installation

Setup instructions...

## Basic Usage

Common commands and patterns...

## Advanced Features

More complex use cases...

## Troubleshooting

Common issues and solutions...

## Related Notes

Links to related tools and concepts...
```

### Meeting Notes

```markdown
---
tags:
  - meeting_notes
  - relevant_domain
---

**Date:** 2025-10-21
**Attendees:** Names or roles
**Purpose:** Meeting objective

## Discussion Points

- Topic 1
  - Details...
- Topic 2
  - Details...

## Action Items

- [ ] Task 1 - Owner
- [ ] Task 2 - Owner

## Decisions

Key decisions made...

## Follow-up

Next steps and future meetings...
```

### Reference Notes

```markdown
---
tags:
  - reference
  - relevant_domain
---

Quick reference for [topic]...

## Quick Reference

Most commonly needed information...

## Parameters/Options

| Name | Type | Description |
|------|------|-------------|
| ... | ... | ... |

## Examples

Common use cases...

## See Also

- [[Related Reference 1]]
- [[Related Reference 2]]
```

## Content Quality Guidelines

**Keep notes focused:**
- One main topic per note
- Split large notes (>500 lines) into focused sub-notes
- Use clear, descriptive section headers

**Include practical information:**
- Working code examples
- Real-world use cases
- Troubleshooting tips
- Personal insights and learnings

**Make notes self-contained:**
- Include enough context to understand standalone
- Link to prerequisites or background
- Explain domain-specific terminology

**Avoid:**
- Redundant information (link instead of duplicating)
- Overly broad notes covering too many topics
- Notes that are just lists of links (add value)
- Copying entire documentation (summarize key points)

## Search-Friendly Writing

**Use clear terminology:**
- Use both formal terms and common names
- Include acronyms with full expansions
- Use consistent naming across notes

**This helps with:**
- Obsidian's search functionality
- Grep searches across vault
- Finding related notes
- Building connections

## Maintenance Patterns

**When updating notes:**
- Check for broken links
- Update related notes if structure changes
- Consolidate if content becomes outdated
- Add new connections as knowledge grows

**Periodic review:**
- Identify notes that could be split or merged
- Update tags to match current taxonomy
- Add missing internal links
- Move notes to better folders if organization has evolved
