#!/usr/bin/env python3
"""Copy the SAY/DO script into the deck as Marp presenter notes.

Marp shows every HTML comment that is not a directive in the presenter view.
The script stays the source of truth. This tool writes each script entry into
the slide whose title matches its heading, as one comment that starts with
SAY or DO. Run it again after a script edit. With --check, it fails when the
deck notes and the script disagree, so the two cannot drift apart.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SEPARATOR = "\n---\n"
NOTE_RE = re.compile(r"\n*<!--\n(?:SAY|DO)\n.*?\n-->\n?", re.S)
HEADING_RE = re.compile(r"^#{1,4} (.+)$", re.M)
STOP_HEADINGS = ("Reserve answers",)


def normalize(title: str) -> str:
    """Reduce a title to the words, so slide and script headings compare."""
    title = re.sub(r"<[^>]+>|[*`]", "", title)
    title = re.sub(r"[.!?…\s]+$", "", title.strip())
    return re.sub(r"\s+", " ", title).lower()


def slide_title(slide: str) -> str | None:
    """Return the first heading, or the meme caption, or None for a bare image."""
    match = HEADING_RE.search(slide)
    if match:
        return normalize(match.group(1))
    lines = [ln for ln in slide.strip().splitlines() if ln.strip()]
    text = [ln for ln in lines if not ln.startswith(("<", "!", "#"))]
    return normalize(text[-1]) if text else None


def script_sections(script: str) -> list[tuple[str, str]]:
    """Return (normalized heading, notes text) for each slide entry."""
    sections = []
    for block in script.split(SEPARATOR):
        match = re.match(r"\s*## ([^\n]+)\n(.*)", block, re.S)
        if not match:
            continue
        heading, body = match.group(1).strip(), match.group(2)
        if heading.startswith(STOP_HEADINGS):
            break
        if "**SAY**" not in body and "**DO**" not in body:
            continue
        body = body.split("\n## ")[0]
        body = re.sub(r"\*\*(SAY|DO)\*\*", r"\1", body)
        body = body.replace("**", "").replace("-->", "->")
        body = re.sub(r"^\* ", "· ", body, flags=re.M)
        body = re.sub(r"\n{3,}", "\n\n", body).strip()
        sections.append((normalize(heading), body))
    return sections


def render(deck: str, script: str) -> tuple[str, list[str]]:
    """Return the deck with fresh notes and a list of alignment problems."""
    front, body = deck.split(SEPARATOR, 1)
    slides = [NOTE_RE.sub("\n", s).rstrip("\n") for s in body.split(SEPARATOR)]
    sections = script_sections(script)
    problems: list[str] = []
    out, j = [], 0
    for number, slide in enumerate(slides, start=1):
        title = slide_title(slide)
        match = None
        if title is None and j < len(sections):
            match = j
        else:
            for k in range(j, min(j + 4, len(sections))):
                if sections[k][0] == title:
                    match = k
                    break
        if match is None:
            problems.append(f"slide {number} has no script entry: {title}")
            out.append(slide + "\n")
            continue
        for skipped in sections[j:match]:
            problems.append(f"script entry has no slide: {skipped[0]}")
        j = match + 1
        out.append(f"{slide}\n\n<!--\n{sections[match][1]}\n-->\n")
    for skipped in sections[j:]:
        problems.append(f"script entry has no slide: {skipped[0]}")
    return front + SEPARATOR + SEPARATOR.join(out), problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Copy the SAY/DO script into Marp presenter notes.")
    parser.add_argument("deck", type=Path)
    parser.add_argument("script", type=Path)
    parser.add_argument("--check", action="store_true", help="fail on drift")
    args = parser.parse_args()
    deck = args.deck.read_text()
    new, problems = render(deck, args.script.read_text())
    for problem in problems:
        print(f"{args.deck}: {problem}", file=sys.stderr)
    if args.check:
        if new != deck:
            print(
                f"{args.deck}: presenter notes differ from {args.script}; "
                "run make sync/notes",
                file=sys.stderr,
            )
            return 1
        print(f"{args.deck}: presenter notes match the script")
        return 1 if problems else 0
    args.deck.write_text(new)
    print(f"{args.deck}: wrote notes, {len(problems)} alignment problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
