# Writing Guidelines for Daily Development Journals

Best practices for creating useful daily log entries.

## Content Priority (Signal-to-Noise)

### HIGH Priority (Always Include)
1. **Context** - What was the goal? Why?
2. **Problems Encountered** - What blocked you?
3. **Status** - Resolved/Unresolved (be honest!)
4. **Open Questions** - What still needs answering?
5. **Key Numbers** - Performance metrics, test counts, commit stats

### MEDIUM Priority (Include If Relevant)
6. **Technical Work** - Tools built, refactorings done
7. **Decisions Made** - And WHY you made them
8. **Reflection** - What did you learn?

### LOW Priority (Usually Skip)
9. ~~File names and function names~~ - Focus on WHAT and WHY, not WHERE
10. ~~Chronological blow-by-blow~~ - Organize by theme, not time
11. ~~Implementation details~~ - Unless they caused problems

---

## Writing Style

### DO
- Use concise, factual language
- Lead with status (Unresolved/Resolved)
- Include specific numbers (96.5 MiB/s, 17 commits)
- Organize by problem, not by time
- Be honest about failures and unknowns
- Use bullet points and numbered lists
- Include hypotheses ("Hypothesis: network saturation")

### DON'T
- Use dramatic language ("shocking discovery", "unrelenting question")
- Repeat yourself across sections
- List every file touched
- Make it a story with narrative arc
- Hide problems or unresolved issues

---

## Section Guidelines

### Context (1-2 lines)
```markdown
Goal: [Main objective or question driving the day]
```

**Good**:
```markdown
Goal: Validate whether custom implementation (~1,000 lines) is worth
the complexity vs simple approach (~130 lines).
```

**Bad**:
```markdown
Today was driven by a single, unrelenting question: Was all this
complexity worth it? I've built a custom solution with over
1,000 lines of streaming code...
```

### Main Issues (3-5 max)
```markdown
#### 1. [Problem Name] (Status)
**[Phase]:** [What happened]
**Status:** [Current state]
```

**Good**:
```markdown
#### 1. Data Format Problem (Unresolved)
**Morning:** Fixed by extracting from metadata column 2.
**Evening:** Problem returned. Baseline data has wrong format.
**Status:** Still unresolved. Blocks validation.
```

**Bad**:
```markdown
#### 1. The Data Problem
The day began with a mysterious bug. The data was malformed,
creating confusion across the entire codebase...
```

### Technical Work (Categorized Bullets)
```markdown
**[Category]:**
- Tool/feature (brief description)
- Another item

**Stats:** [Numbers that matter]
```

**Good**:
```markdown
**Performance tools:**
- `analyze_throughput.py` with SVG visualizations
- HTTP timing instrumentation
- Dataset statistics: 2.5M records (65.6% type A, 34.4% type B)

**Stats:** 17 commits, ~8,000 lines added
```

**Bad**:
```markdown
Modified scripts/processor.py, scripts/validate_cli.py,
and test_data/merge_test/output.csv to add performance analysis
capabilities including throughput visualization and HTTP timing...
```

### Open Questions (Specific, Actionable)
```markdown
1. **[Specific question]:** Brief context
2. **[Another question]:** Why it matters
```

**Good**:
```markdown
1. **Core question:** Does complexity justify itself? Tools ready, validation pending.
2. **Performance:** Is 4-worker degradation fundamental or local artifact?
```

**Bad**:
```markdown
1. I'm wondering if the approach I took was the right one
2. Need to figure out the performance issues
3. Should probably look into the testing more
```

### Reflection (1-2 sentences)
```markdown
[What did you learn or realize? Be honest.]
```

**Good**:
```markdown
Built validation infrastructure that might prove the complex
solution wasn't necessary. All pieces ready but can't validate
without resolving the baseline data issue.
```

**Bad**:
```markdown
Today was a productive day where I learned a lot about the system
and made significant progress on multiple fronts. Looking forward
to continuing this important work tomorrow.
```

---

## Common Pitfalls

### Pitfall 1: Too Verbose
Bad: Long narrative paragraphs
Right: `Goal: Validate custom implementation correctness vs baseline.`

### Pitfall 2: Too Detailed
Bad: Listing every file and function name
Right: `Fixed data extraction by parsing metadata column 2 instead of columns 5-6.`

### Pitfall 3: Hiding Problems
Bad: `Built comprehensive validation infrastructure with 11 passing tests.`
Right: `Built validation infrastructure (11 tests passing) but validation not run yet. Blocked by disk space.`

### Pitfall 4: Vague Questions
Bad: `Need to look into the performance issues`
Right: `**Performance:** Is 4-worker degradation (80% loss) fundamental or local artifact?`

---

## Key Principles

1. **Write for Future You** - Who needs to remember WHY, not WHAT
2. **Organize by Problem** - Not by chronology
3. **Status-First** - Be upfront about unresolved issues
4. **Numbers Matter** - Performance metrics, commit counts
5. **Honesty over Completeness** - "Still blocked" is valuable info
6. **Breadcrumbs** - Links to related work for context

---

## Quick Checklist

Before finalizing your journal entry, verify:

- [ ] Context is 1-2 lines maximum
- [ ] Each main issue has clear status (Resolved/Unresolved)
- [ ] Specific numbers included (commits, metrics, test counts)
- [ ] Open questions are actionable and specific
- [ ] Reflection is honest (1-2 sentences max)
- [ ] No file/function names unless critical
- [ ] Organized by theme, not chronology
- [ ] Writing is concise and factual
