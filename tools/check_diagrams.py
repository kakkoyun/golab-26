#!/usr/bin/env python3
"""Fail when a Kroki diagram does not render.

Each talk deck embeds a Mermaid diagram as a Kroki URL, and the browser fetches
that URL while Marp renders. Kroki answers over the network, so a flaky
connection leaves a broken image on the slide and the build still reports
success. This check fetches every diagram URL from the built HTML and fails with
the slide, so a missing picture stops the run instead of reaching the room.
"""

from __future__ import annotations

import argparse
import base64
import http.client
import re
import sys
import time
import urllib.parse
import zlib
from pathlib import Path

SECTION_RE = re.compile(r"<section\b")
IMG_RE = re.compile(r'<img src="(https://kroki\.io/[^"]+)"')
ATTEMPTS = 3
TIMEOUT = 20


def diagram_source(url: str) -> str:
    """Return the first content line of the diagram behind a Kroki URL."""
    try:
        payload = url.rsplit("/", 1)[-1]
        padded = payload + "=" * (-len(payload) % 4)
        text = zlib.decompress(base64.urlsafe_b64decode(padded)).decode("utf-8")
    except (ValueError, zlib.error, UnicodeDecodeError):
        return "unreadable diagram source"
    for line in text.splitlines():
        stripped = line.strip()
        # Skip the init directive, which every diagram carries.
        if stripped and not stripped.startswith("%%"):
            return stripped[:60]
    return "empty diagram source"


def diagrams(html: str) -> list[tuple[int, str]]:
    """Return (slide number, url) pairs in document order."""
    found = []
    for match in IMG_RE.finditer(html):
        slide = len(SECTION_RE.findall(html[: match.start()]))
        found.append((max(slide, 1), match.group(1)))
    return found


def reachable(url: str) -> str | None:
    """Return None when the URL answers 200, else a short reason."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.netloc != "kroki.io":
        return f"refusing to fetch {url[:40]}"
    target = parsed.path + (f"?{parsed.query}" if parsed.query else "")
    reason = "no attempt made"
    for attempt in range(ATTEMPTS):
        connection = http.client.HTTPSConnection("kroki.io", timeout=TIMEOUT)
        try:
            connection.request(
                "GET", target, headers={"User-Agent": "golab-diagram-check"}
            )
            response = connection.getresponse()
            response.read()
            if response.status == 200:
                return None
            reason = f"kroki answered {response.status}"
        except (OSError, http.client.HTTPException) as error:
            reason = f"network error: {error}"
        finally:
            connection.close()
        if attempt < ATTEMPTS - 1:
            time.sleep(2 * (attempt + 1))
    return reason


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", nargs="+", type=Path, help="built deck HTML")
    args = parser.parse_args()

    failures = False
    for path in args.html:
        if not path.is_file():
            parser.error(f"missing HTML: {path}")
        found = diagrams(path.read_text(encoding="utf-8"))
        print(f"{path}: {len(found)} diagram(s)")
        for index, (slide, url) in enumerate(found, 1):
            reason = reachable(url)
            if reason is None:
                continue
            print(
                f"{path}: slide {slide}: diagram {index} ({diagram_source(url)}): {reason}",
                file=sys.stderr,
            )
            failures = True

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
