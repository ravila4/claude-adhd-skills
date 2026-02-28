# Callout Conventions

Obsidian callout types used in daily journal entries, with placement guidance and real examples.

## `[!info]` -- Context and References

**Placement:** Top of entry for continuity; inline for reference material.

```markdown
> [!info] Context
> Continued from [[2026-01-30]] - testing whether the new config fixes the offset mismatch.
```

**Collapsible variant** (`[!info]-`) for bulky reference material:

```markdown
> [!info]- Reference URLs
> - [Dashboard](https://your-dashboard-url)
> - [Logs](https://your-logging-url)
```

## `[!success]` -- Wins, Milestones, Progress

Flexible title -- scale to match the magnitude. "Win" for a single thing, "Big day" for multiple breakthroughs, "Progress" for incremental.

```markdown
> [!success] Win
> Tests pass with **identical results** between the two implementations (r=1.0000 for both metrics).
```

```markdown
> [!success] Big day
>
> - Solved the configuration mystery (environment variable mismatch)
> - Confirmed both paths produce consistent output
> - Designed clean architecture for the job registry
```

```markdown
> [!success] Progress
>
> - Created filtered dataset (non-null only: 166K records from 370K total)
> - Submitted batch job with filtered inputs
```

## `[!warning]` -- Concerns, Friction, Blockers

For things that are impeding work or showing signs of future trouble.

```markdown
> [!warning] Blocker
> Still can't get the API to recognize the config file format.
```

```markdown
> [!warning] Growing Pain
> The flat config file is starting to show friction as the option count grows. The core issue isn't the format -- it's that many options are **structurally null** depending on the mode.
```

## `[!question]` -- Open Loops

For things still being thought through. Strikethrough completed items rather than deleting them.

```markdown
> [!question] Still thinking about...
>
> - ~~Need to run the comparison test, then analyze both outputs~~ Done!
> - Should we switch to a relational config format?
```

## `[!bug]` -- Bugs Discovered

For bugs found during the day's work.

```markdown
> [!bug] Script Bug Found
> The filtering script was silently dropping records with missing ID fields instead of mapping them.
```

## `[!note]` -- Observations

For non-actionable insights, things noticed but not necessarily acted on.

```markdown
> [!note] Observation: batch job performance
> The new implementation completes in ~40min vs the old one's ~2hr for the same dataset.
```
