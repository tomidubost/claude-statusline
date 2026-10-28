#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
RED = "\x1b[31m"
CYAN = "\x1b[36m"
MAGENTA = "\x1b[35m"
GRAY = "\x1b[90m"

WEEKDAYS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]


def pct_color(p):
    if p >= 80:
        return RED
    if p >= 50:
        return YELLOW
    return GREEN


def mini_bar(p, width=8):
    filled = min(width, int(round(p / 100 * width)))
    return pct_color(p) + "▰" * filled + GRAY + "▱" * (width - filled) + RESET


def reset_label(epoch):
    try:
        dt = datetime.fromtimestamp(epoch)
    except (TypeError, ValueError, OSError):
        return ""
    now = datetime.now()
    hhmm = dt.strftime("%H:%M")
    if dt.date() == now.date():
        return hhmm
    return f"{WEEKDAYS[dt.weekday()]} {hhmm}"


def git_branch(cwd):
    path = cwd
    while path and path != os.path.dirname(path):
        git = os.path.join(path, ".git")
        if os.path.isdir(git):
            head = os.path.join(git, "HEAD")
        elif os.path.isfile(git):
            try:
                with open(git) as f:
                    gitdir = f.read().split("gitdir:", 1)[1].strip()
            except (OSError, IndexError):
                return ""
            if not os.path.isabs(gitdir):
                gitdir = os.path.join(path, gitdir)
            head = os.path.join(gitdir, "HEAD")
        else:
            path = os.path.dirname(path)
            continue
        try:
            with open(head) as f:
                ref = f.read().strip()
        except OSError:
            return ""
        if ref.startswith("ref: refs/heads/"):
            return ref[len("ref: refs/heads/"):]
        return ref[:7]
    return ""


def remaining_label(epoch):
    try:
        secs = epoch - datetime.now().timestamp()
    except TypeError:
        return ""
    if secs <= 0:
        return ""
    mins = int(secs // 60)
    if mins >= 60:
        return f"{mins // 60}h{mins % 60:02d}m"
    return f"{mins}m"


def limit_chunk(name, data):
    if not isinstance(data, dict):
        return None
    pct = data.get("used_percentage")
    if pct is None:
        return None
    resets_at = data.get("resets_at")
    resets = reset_label(resets_at)
    remaining = remaining_label(resets_at)
    chunk = (
        f"{DIM}{name}{RESET} {mini_bar(pct)} "
        f"{pct_color(pct)}{pct:.0f}%{RESET}"
    )
    if resets:
        chunk += f" {DIM}↺ {resets}{RESET}"
        if remaining:
            chunk += f" {DIM}· {remaining}{RESET}"
    return chunk


def main():
    try:
        d = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        print("…")
        return

    line1 = []

    model = d.get("model", {}).get("display_name") or ""
    if model:
        line1.append(f"{BOLD}{CYAN}{model}{RESET}")

    cwd = d.get("workspace", {}).get("current_dir") or d.get("cwd") or ""
    branch = git_branch(cwd) if cwd else ""
    if branch:
        if len(branch) > 50:
            branch = branch[:49] + "…"
        line1.append(f"{MAGENTA}⎇ {branch}{RESET}")

    line2 = []

    ctx = d.get("context_window") or {}
    used = ctx.get("used_percentage")
    if used is not None:
        line2.append(
            f"{DIM}ctx{RESET} {mini_bar(used)} {pct_color(used)}{used:.0f}%{RESET}"
        )

    five = limit_chunk("5h", (d.get("rate_limits") or {}).get("five_hour"))
    if five:
        line2.append(five)

    cost = (d.get("cost") or {}).get("total_cost_usd")
    if cost is not None:
        line2.append(f"{YELLOW}${cost:.2f}{RESET}")

    if line1:
        print(f" {DIM}·{RESET} ".join(line1))
    print("   ".join(line2))


if __name__ == "__main__":
    main()
