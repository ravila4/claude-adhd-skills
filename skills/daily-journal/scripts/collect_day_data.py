#!/usr/bin/env -S uv run --script
# /// script
# dependencies = []
# ///
"""
Collect development activity data for a specific date.

Unified data collector that gathers:
1. Git commits across ~/Projects/
2. Claude Code session log insights (JSONL parsing)

Outputs structured JSON for LLM synthesis into narrative journal entries.

Usage:
    uv run collect_day_data.py                    # Today's data
    uv run collect_day_data.py --date 2026-01-20  # Specific date
    uv run collect_day_data.py --skip-sessions    # Skip JSONL parsing (faster)
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class Commit:
    """A git commit."""

    hash: str
    message: str
    files_changed: int = 0


@dataclass
class ProjectActivity:
    """Activity in a single git repository."""

    name: str
    path: str
    commits: list[Commit] = field(default_factory=list)

    @property
    def commit_count(self) -> int:
        return len(self.commits)

    @property
    def total_files_changed(self) -> int:
        return sum(c.files_changed for c in self.commits)


@dataclass
class KeyMoment:
    """A tagged key moment from the session."""

    type: str  # PROBLEM, TESTING, COMPLETION, INSIGHT, ACTION
    summary: str


@dataclass
class SessionInsights:
    """Insights extracted from Claude Code JSONL session logs."""

    user_requests: list[str] = field(default_factory=list)
    tools_used: dict[str, int] = field(default_factory=dict)
    errors_encountered: list[str] = field(default_factory=list)
    key_moments: list[KeyMoment] = field(default_factory=list)
    questions_raised: list[str] = field(default_factory=list)
    files_modified: list[str] = field(default_factory=list)


@dataclass
class SummaryStats:
    """Computed summary statistics."""

    total_commits: int = 0
    total_files_changed: int = 0
    total_sessions: int = 0
    dominant_tools: list[str] = field(default_factory=list)
    had_errors: bool = False


@dataclass
class DayData:
    """All collected data for a given day."""

    date: str
    git_activity: dict[str, ProjectActivity] = field(default_factory=dict)
    session_insights: SessionInsights = field(default_factory=SessionInsights)
    main_project: str | None = None
    side_projects: list[str] = field(default_factory=list)
    suggested_tags: list[str] = field(default_factory=list)
    summary_stats: SummaryStats = field(default_factory=SummaryStats)


# =============================================================================
# Utility Functions
# =============================================================================


def run_command(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr)."""
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return result.returncode, result.stdout, result.stderr


def extract_text_content(content: Any) -> str:
    """Extract text from various content structures in JSONL."""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        texts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    texts.append(item.get("text", ""))
            elif isinstance(item, str):
                texts.append(item)
        return " ".join(texts)
    return str(content)


# =============================================================================
# Git Collection
# =============================================================================


def scan_git_repos(projects_dir: Path, date_str: str) -> dict[str, ProjectActivity]:
    """Find all repos in projects_dir with commits on given date."""
    repos: dict[str, ProjectActivity] = {}

    if not projects_dir.exists():
        return repos

    for item in projects_dir.iterdir():
        if not item.is_dir():
            continue

        git_dir = item / ".git"
        if not git_dir.exists():
            continue

        commits = get_commits_for_date(item, date_str)
        if commits:
            repos[item.name] = ProjectActivity(
                name=item.name, path=str(item), commits=commits
            )

    return repos


def get_commits_for_date(repo_path: Path, date_str: str) -> list[Commit]:
    """Get commits from a repo for a specific date."""
    start = f"{date_str} 00:00:00"
    end = f"{date_str} 23:59:59"

    cmd = [
        "git",
        "log",
        f"--since={start}",
        f"--until={end}",
        "--pretty=format:%h|%s",
        "--shortstat",
    ]

    returncode, stdout, _ = run_command(cmd, cwd=repo_path)
    if returncode != 0 or not stdout.strip():
        return []

    commits: list[Commit] = []
    lines = stdout.strip().split("\n")

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if "|" in line:
            parts = line.split("|", 1)
            if len(parts) == 2:
                hash_val, message = parts
                files_changed = 0

                # Look for stat line
                if i + 1 < len(lines):
                    stat_line = lines[i + 1].strip()
                    if "file" in stat_line and "changed" in stat_line:
                        # Use regex to handle "N file(s) changed" format
                        match = re.search(r"(\d+) files? changed", stat_line)
                        if match:
                            try:
                                files_changed = int(match.group(1))
                            except ValueError:
                                pass
                        i += 1

                commits.append(
                    Commit(
                        hash=hash_val.strip(),
                        message=message.strip(),
                        files_changed=files_changed,
                    )
                )
        i += 1

    return commits


# =============================================================================
# JSONL Session Log Parsing
# =============================================================================


def find_session_logs(date_str: str) -> list[Path]:
    """Find JSONL files modified on target date.

    Uses Python-based filtering to avoid find command boundary issues.
    """
    projects_dir = Path.home() / ".claude" / "projects"

    if not projects_dir.exists():
        return []

    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return []

    matching_files = []
    try:
        for jsonl_file in projects_dir.rglob("*.jsonl"):
            try:
                mtime = datetime.fromtimestamp(jsonl_file.stat().st_mtime).date()
                if mtime == target_date:
                    matching_files.append(jsonl_file)
            except OSError:
                # Skip files we can't stat
                continue
    except PermissionError:
        print(f"Warning: Cannot read {projects_dir}", file=sys.stderr)
        return []

    return matching_files


def parse_jsonl_file(log_path: Path) -> list[dict]:
    """Parse a JSONL file into a list of message dicts."""
    messages = []
    try:
        with open(log_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    messages.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except (OSError, IOError):
        pass
    return messages


def extract_user_requests(messages: list[dict]) -> list[str]:
    """Extract user messages (first 200 chars each)."""
    requests = []
    for msg in messages:
        if msg.get("type") == "user":
            message = msg.get("message", {})
            content = extract_text_content(message.get("content", ""))

            # Skip system messages and interrupts
            if content and not content.startswith("<") and not content.startswith(
                "[Request interrupted"
            ):
                # Truncate to 200 chars
                truncated = content[:200]
                if len(content) > 200:
                    truncated += "..."
                requests.append(truncated)

    return requests


def extract_tool_usage(messages: list[dict]) -> dict[str, int]:
    """Count tool invocations by name."""
    tool_counts: dict[str, int] = {}

    for msg in messages:
        if msg.get("type") == "assistant":
            message = msg.get("message", {})
            content = message.get("content", [])

            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "tool_use":
                        tool_name = item.get("name", "unknown")
                        tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1

    return tool_counts


def extract_errors(messages: list[dict]) -> list[str]:
    """Find tool results with isError=true."""
    errors = []

    for msg in messages:
        if msg.get("type") == "tool_result":
            if msg.get("isError"):
                content = msg.get("content", "")
                if isinstance(content, str) and content:
                    # Truncate long error messages
                    truncated = content[:300]
                    if len(content) > 300:
                        truncated += "..."
                    errors.append(truncated)

    return errors


def extract_key_moments(messages: list[dict]) -> list[KeyMoment]:
    """Tag moments: PROBLEM, TESTING, COMPLETION, INSIGHT, ACTION."""
    moments = []

    for msg in messages:
        if msg.get("type") != "assistant":
            continue

        message = msg.get("message", {})
        content = message.get("content", [])

        text = ""
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block.get("text", "")
                    break
        elif isinstance(content, str):
            text = content

        if not text:
            continue

        text_lower = text.lower()

        # Check for key patterns
        if "memory" in text_lower or "scale" in text_lower:
            moments.append(KeyMoment(type="INSIGHT", summary="Memory/scaling concern"))

        if "refactor" in text_lower:
            moments.append(KeyMoment(type="ACTION", summary="Refactoring code"))

        if "test" in text_lower and (
            "passing" in text_lower or "failed" in text_lower or "error" in text_lower
        ):
            moments.append(KeyMoment(type="TESTING", summary="Running tests"))

        if "commit" in text_lower:
            moments.append(KeyMoment(type="COMPLETION", summary="Committing changes"))

        # Extract error mentions
        error_matches = re.findall(
            r"(Error|Failed|Exception|FAILED).*", text, re.IGNORECASE
        )
        if error_matches:
            summary = error_matches[0][:100]
            moments.append(KeyMoment(type="PROBLEM", summary=summary))

    # Deduplicate by type+summary
    seen = set()
    unique_moments = []
    for m in moments:
        key = (m.type, m.summary)
        if key not in seen:
            seen.add(key)
            unique_moments.append(m)

    return unique_moments


def extract_questions(messages: list[dict]) -> list[str]:
    """Find messages with uncertainty/questions."""
    questions = []

    for msg in messages:
        if msg.get("type") not in ["user", "assistant"]:
            continue

        message = msg.get("message", {})
        content = extract_text_content(message.get("content", ""))

        if not content:
            continue

        # Look for questions or uncertainty markers
        if "?" in content or "unclear" in content.lower() or "not sure" in content.lower():
            sentences = content.split(".")
            for sent in sentences:
                if (
                    "?" in sent
                    or "unclear" in sent.lower()
                    or "not sure" in sent.lower()
                ):
                    cleaned = sent.strip()[:200]
                    if cleaned:
                        questions.append(cleaned)

    return questions[:10]  # Limit to top 10


def extract_files_modified(messages: list[dict]) -> list[str]:
    """Collect Edit/Write tool file paths."""
    files = set()

    for msg in messages:
        if msg.get("type") == "assistant":
            message = msg.get("message", {})
            content = message.get("content", [])

            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "tool_use":
                        tool_name = item.get("name", "")
                        if tool_name in ["Edit", "Write"]:
                            file_path = item.get("input", {}).get("file_path")
                            if file_path:
                                files.add(file_path)

    return sorted(list(files))


def collect_session_insights(date_str: str) -> tuple[SessionInsights, int]:
    """Aggregate all JSONL extraction into SessionInsights.

    Returns (insights, log_count) to avoid redundant find_session_logs calls.
    """
    log_files = find_session_logs(date_str)
    log_count = len(log_files)

    insights = SessionInsights()
    all_tool_counts: dict[str, int] = {}

    for log_path in log_files:
        messages = parse_jsonl_file(log_path)
        if not messages:
            continue

        # Extract from this session
        insights.user_requests.extend(extract_user_requests(messages))

        # Merge tool counts
        for tool, count in extract_tool_usage(messages).items():
            all_tool_counts[tool] = all_tool_counts.get(tool, 0) + count

        insights.errors_encountered.extend(extract_errors(messages))
        insights.key_moments.extend(extract_key_moments(messages))
        insights.questions_raised.extend(extract_questions(messages))
        insights.files_modified.extend(extract_files_modified(messages))

    insights.tools_used = all_tool_counts

    # Deduplicate files
    insights.files_modified = sorted(set(insights.files_modified))

    # Limit user requests to first 20
    insights.user_requests = insights.user_requests[:20]

    return insights, log_count


# =============================================================================
# Main Collection & Analysis
# =============================================================================


def determine_main_project(
    git_activity: dict[str, ProjectActivity],
) -> str | None:
    """Determine main project by commit count (weighted)."""
    if not git_activity:
        return None

    scores: dict[str, float] = {}
    for name, repo in git_activity.items():
        scores[name] = repo.commit_count * 10 + repo.total_files_changed

    if not scores:
        return None
    return max(scores, key=lambda k: scores[k])


def generate_tags(
    main_project: str | None, git_activity: dict[str, ProjectActivity]
) -> list[str]:
    """Generate suggested tags for the journal entry."""
    tags = ["daily-log"]

    if main_project:
        tag = main_project.lower().replace("_", "-").replace(" ", "-")
        if tag not in tags:
            tags.append(tag)

    # Add tags based on commit messages
    all_messages = []
    for repo in git_activity.values():
        all_messages.extend([c.message.lower() for c in repo.commits])

    message_text = " ".join(all_messages)
    if any(word in message_text for word in ["test", "testing", "spec"]):
        tags.append("testing")
    if any(word in message_text for word in ["fix", "bug", "error"]):
        tags.append("debugging")
    if any(word in message_text for word in ["refactor", "cleanup", "clean up"]):
        tags.append("refactoring")

    return tags


def compute_summary_stats(
    git_activity: dict[str, ProjectActivity],
    session_insights: SessionInsights,
) -> SummaryStats:
    """Compute summary statistics."""
    total_commits = sum(repo.commit_count for repo in git_activity.values())
    total_files = sum(repo.total_files_changed for repo in git_activity.values())
    total_sessions = 0

    # Get top 3 tools by usage
    sorted_tools = sorted(
        session_insights.tools_used.items(), key=lambda x: x[1], reverse=True
    )
    dominant_tools = [tool for tool, _ in sorted_tools[:3]]

    return SummaryStats(
        total_commits=total_commits,
        total_files_changed=total_files,
        total_sessions=total_sessions,
        dominant_tools=dominant_tools,
        had_errors=len(session_insights.errors_encountered) > 0,
    )


def collect_day_data(
    date_str: str, projects_dir: Path, skip_sessions: bool = False
) -> DayData:
    """Collect all data sources into unified structure."""
    print(f"Collecting data for {date_str}...", file=sys.stderr)

    # Git activity
    print(f"Scanning git repos in {projects_dir}...", file=sys.stderr)
    git_activity = scan_git_repos(projects_dir, date_str)
    print(f"Found {len(git_activity)} repo(s) with activity", file=sys.stderr)

    # Session insights from JSONL
    if skip_sessions:
        print("Skipping session log parsing (--skip-sessions)", file=sys.stderr)
        session_insights = SessionInsights()
    else:
        print("Parsing session logs...", file=sys.stderr)
        insights_result = collect_session_insights(date_str)
        session_insights, log_count = insights_result
        print(f"Parsed {log_count} session log(s)", file=sys.stderr)

    # Compute derived fields
    main_project = determine_main_project(git_activity)
    side_projects = [name for name in git_activity if name != main_project]
    suggested_tags = generate_tags(main_project, git_activity)
    summary_stats = compute_summary_stats(git_activity, session_insights)

    return DayData(
        date=date_str,
        git_activity=git_activity,
        session_insights=session_insights,
        main_project=main_project,
        side_projects=side_projects,
        suggested_tags=suggested_tags,
        summary_stats=summary_stats,
    )


# =============================================================================
# Custom JSON Serialization
# =============================================================================


def dataclass_to_dict(obj: Any) -> Any:
    """Convert dataclasses to dicts recursively, handling special cases."""
    if hasattr(obj, "__dataclass_fields__"):
        result = {}
        for field_name in obj.__dataclass_fields__:
            value = getattr(obj, field_name)
            result[field_name] = dataclass_to_dict(value)
        return result
    elif isinstance(obj, dict):
        return {k: dataclass_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [dataclass_to_dict(item) for item in obj]
    elif isinstance(obj, Path):
        return str(obj)
    else:
        return obj


# =============================================================================
# Main
# =============================================================================


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect development activity data for daily journal synthesis"
    )
    parser.add_argument(
        "--date",
        help="Date in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--projects-dir",
        default=str(Path.home() / "Projects"),
        help="Directory containing git repositories (default: ~/Projects)",
    )
    parser.add_argument(
        "--skip-sessions",
        action="store_true",
        help="Skip JSONL session log parsing (faster, git only)",
    )

    args = parser.parse_args()

    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    projects_dir = Path(args.projects_dir)

    data = collect_day_data(date_str, projects_dir, args.skip_sessions)

    # Output as JSON
    print(json.dumps(dataclass_to_dict(data), indent=2, default=str))


if __name__ == "__main__":
    main()
