#!/usr/bin/env python3
"""Claude Code custom status line — 2-line layout with project/git + model/resources."""

import hashlib
import json
import os
import subprocess
import sys
import time

# ─── CONFIG ──────────────────────────────────────────────────────────────────

SHOW_WORKTREE = True
SHOW_RATE_LIMITS = True

# Color thresholds: (yellow_start, red_start)
CONTEXT_THRESHOLDS = (50, 75)
RATE_LIMIT_THRESHOLDS = (50, 80)

PROGRESS_BAR_WIDTH = 10

# Git cache max age in seconds
GIT_CACHE_MAX_AGE = 5

# ─── ANSI HELPERS ────────────────────────────────────────────────────────────

GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"


def color(value, thresholds):
    """Return ANSI-colored string for a numeric value based on thresholds."""
    yellow_start, red_start = thresholds
    if value >= red_start:
        c = RED
    elif value >= yellow_start:
        c = YELLOW
    else:
        c = GREEN
    return f"{c}{round(value)}{RESET}"


def progress_bar(percentage, width=PROGRESS_BAR_WIDTH, thresholds=CONTEXT_THRESHOLDS):
    """Return a colored progress bar string."""
    filled = round(percentage / (100 / width))
    filled = max(0, min(width, filled))
    empty = width - filled
    bar = "█" * filled + "░" * empty

    yellow_start, red_start = thresholds
    if percentage >= red_start:
        c = RED
    elif percentage >= yellow_start:
        c = YELLOW
    else:
        c = GREEN
    return f"{c}{bar}{RESET}"


def format_countdown(epoch):
    """Convert a future epoch timestamp to a human-readable countdown."""
    if not epoch:
        return ""
    diff = max(0, epoch - time.time())
    hours = int(diff // 3600)
    minutes = int((diff % 3600) // 60)
    if hours >= 24:
        days = hours // 24
        remaining_hours = hours % 24
        return f"{days}d{remaining_hours}h"
    return f"{hours}h{minutes:02d}m"


# ─── GIT ─────────────────────────────────────────────────────────────────────


def _run_git(cwd, *args):
    """Run a git command and return stdout, or empty string on failure."""
    try:
        result = subprocess.run(
            ["git", "-C", cwd] + list(args),
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except Exception:
        return ""


def _fetch_git_info(cwd):
    """Fetch all git info from subprocess calls."""
    branch = _run_git(cwd, "branch", "--show-current") or "?"

    ahead, behind = 0, 0
    lr = _run_git(cwd, "rev-list", "--left-right", "--count", "HEAD...@{upstream}")
    if lr:
        parts = lr.split()
        if len(parts) == 2:
            ahead, behind = int(parts[0]), int(parts[1])

    staged_lines = _run_git(cwd, "diff", "--cached", "--numstat", "-z")
    staged = len([l for l in staged_lines.split("\0") if "\t" in l]) if staged_lines else 0

    unstaged_lines = _run_git(cwd, "diff", "--numstat", "-z")
    unstaged = len([l for l in unstaged_lines.split("\0") if "\t" in l]) if unstaged_lines else 0

    untracked_lines = _run_git(cwd, "ls-files", "--others", "--exclude-standard")
    untracked = len(untracked_lines.splitlines()) if untracked_lines else 0

    return {
        "branch": branch,
        "ahead": ahead,
        "behind": behind,
        "staged": staged,
        "unstaged": unstaged,
        "untracked": untracked,
    }


def get_git_info(cwd, session_id):
    """Get git info with caching based on session_id."""
    cwd_hash = hashlib.md5(cwd.encode()).hexdigest()[:8]
    cache_file = f"/tmp/statusline-git-cache-{session_id}-{cwd_hash}"

    # Try reading cache
    try:
        if os.path.exists(cache_file):
            mtime = os.path.getmtime(cache_file)
            if time.time() - mtime < GIT_CACHE_MAX_AGE:
                with open(cache_file, "r") as f:
                    return json.loads(f.read())
    except Exception:
        pass

    # Cache miss or stale — fetch fresh
    info = _fetch_git_info(cwd)

    # Write cache
    try:
        with open(cache_file, "w") as f:
            f.write(json.dumps(info))
    except Exception:
        pass

    return info


# ─── LINE BUILDERS ───────────────────────────────────────────────────────────


def build_line1(data, git_info):
    """Build Line 1: Project + Git."""
    cwd = data.get("workspace", {}).get("current_dir", "")
    project = os.path.basename(cwd) if cwd else "?"

    parts = [f"📁 {project}"]

    if git_info:
        # Branch + ahead/behind (hide when both are zero)
        branch = git_info.get("branch", "?")
        ahead = git_info.get("ahead", 0)
        behind = git_info.get("behind", 0)
        branch_str = f"🌿 {branch}"
        if ahead or behind:
            ab_parts = []
            if ahead:
                ab_parts.append(f"↑{ahead}")
            if behind:
                ab_parts.append(f"↓{behind}")
            branch_str += " " + " ".join(ab_parts)
        parts.append(branch_str)

        # Worktree
        if SHOW_WORKTREE:
            worktree = data.get("workspace", {}).get("git_worktree")
            if worktree:
                parts.append(f"🌳 {worktree}")

        # Git status
        staged = git_info.get("staged", 0)
        unstaged = git_info.get("unstaged", 0)
        untracked = git_info.get("untracked", 0)

        lines_added = data.get("cost", {}).get("total_lines_added", 0) or 0
        lines_removed = data.get("cost", {}).get("total_lines_removed", 0) or 0

        is_clean = staged == 0 and unstaged == 0 and untracked == 0
        no_line_changes = lines_added == 0 and lines_removed == 0

        if is_clean and no_line_changes:
            parts.append("✓")
        else:
            if not is_clean:
                parts.append(f"S:{staged} U:{unstaged} A:{untracked}")
            if not no_line_changes:
                parts.append(f"+{lines_added} -{lines_removed}")

    return " | ".join(parts)


def _format_tokens(count):
    """Format token count in human-readable form (e.g. 24k, 1.2M)."""
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    if count >= 1_000:
        return f"{count / 1_000:.0f}k"
    return str(count)


def build_line2(data):
    """Build Line 2: Model + Resources."""
    parts = []

    # Model
    model_name = data.get("model", {}).get("display_name", "?")
    parts.append(f"🤖 {model_name}")

    # Agent name (if running with --agent)
    agent_name = data.get("agent", {}).get("name") if data.get("agent") else None
    if agent_name:
        parts.append(f"🕵️ {agent_name}")

    # Context usage with token counts
    ctx = data.get("context_window", {})
    ctx_pct = ctx.get("used_percentage", 0) or 0
    total_input = ctx.get("total_input_tokens", 0) or 0
    total_output = ctx.get("total_output_tokens", 0) or 0
    ctx_size = ctx.get("context_window_size", 0) or 0
    total_tokens = total_input + total_output

    usage = ctx.get("current_usage") or {}
    cache_read = usage.get("cache_read_input_tokens", 0) or 0
    cache_create = usage.get("cache_creation_input_tokens", 0) or 0
    cache_total = cache_read + cache_create
    cache_pct = round(cache_read / cache_total * 100) if cache_total > 0 else 0

    bar = progress_bar(ctx_pct, PROGRESS_BAR_WIDTH, CONTEXT_THRESHOLDS)
    colored_pct = color(ctx_pct, CONTEXT_THRESHOLDS)
    token_str = f"{_format_tokens(total_tokens)}/{_format_tokens(ctx_size)}" if ctx_size else ""
    parts.append(f"🧠 {bar} {colored_pct}% ({token_str} cache {cache_pct}%)")

    # Session cost
    cost = data.get("cost", {}).get("total_cost_usd", 0) or 0
    parts.append(f"💰 ${cost:.2f}")

    # Rate limits
    if SHOW_RATE_LIMITS:
        rate_limits = data.get("rate_limits", {})

        five_hour = rate_limits.get("five_hour", {})
        if five_hour and five_hour.get("used_percentage") is not None:
            pct_5h = five_hour.get("used_percentage", 0)
            reset_5h = five_hour.get("resets_at")
            colored_5h = color(pct_5h, RATE_LIMIT_THRESHOLDS)
            countdown_5h = format_countdown(reset_5h)
            parts.append(f"⏱️ 5h {colored_5h}% ({countdown_5h})")

        seven_day = rate_limits.get("seven_day", {})
        if seven_day and seven_day.get("used_percentage") is not None:
            pct_7d = seven_day.get("used_percentage", 0)
            reset_7d = seven_day.get("resets_at")
            colored_7d = color(pct_7d, RATE_LIMIT_THRESHOLDS)
            countdown_7d = format_countdown(reset_7d)
            parts.append(f"📅 7d {colored_7d}% ({countdown_7d})")

    return " | ".join(parts)


# ─── MAIN ────────────────────────────────────────────────────────────────────


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
    except Exception:
        print("[statusline: no data]")
        return

    cwd = data.get("workspace", {}).get("current_dir", os.getcwd())
    session_id = data.get("session_id", "default")

    # Only fetch git info when inside a git repository
    is_git_repo = _run_git(cwd, "rev-parse", "--is-inside-work-tree") == "true"
    git_info = get_git_info(cwd, session_id) if is_git_repo else None

    line1 = build_line1(data, git_info)
    line2 = build_line2(data)

    print(line1)
    print(line2)


if __name__ == "__main__":
    main()
