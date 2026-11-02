#!/usr/bin/env python3
"""Inline remote Kroki diagram images into a built Marp HTML deck.

The Kroki plugin renders each Mermaid block as an <img> that points to
kroki.io. A deck that depends on the network fails on conference Wi-Fi.
This tool downloads each diagram once and replaces the URL with a data
URI, so the HTML deck works offline. Run it while you are online.
"""

import base64
import re
import sys
import urllib.error
import urllib.request

USAGE = "usage: inline_kroki.py <in.html> <out.html>"

# Only https://kroki.io URLs match, so urlopen never sees another scheme.
KROKI_SRC = re.compile(r'src="(https://kroki\.io/[^"]+)"')


def fetch(url: str) -> bytes:
    if not url.startswith("https://kroki.io/"):
        raise ValueError(f"refusing to fetch a non-Kroki URL: {url[:60]}")
    request = urllib.request.Request(
        url, headers={"User-Agent": "golab-26-inline-kroki"}
    )  # noqa: S310
    with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310
        return response.read()


def main() -> int:
    if len(sys.argv) != 3:
        print(USAGE, file=sys.stderr)
        return 2
    source, target = sys.argv[1], sys.argv[2]
    try:
        with open(source, encoding="utf-8") as handle:
            html = handle.read()
    except OSError as err:
        print(f"error: cannot read {source}: {err}", file=sys.stderr)
        return 1

    urls = sorted(set(KROKI_SRC.findall(html)))
    for url in urls:
        try:
            body = fetch(url)
        except (urllib.error.URLError, TimeoutError, ValueError) as err:
            print(f"error: cannot fetch {url[:60]}...: {err}", file=sys.stderr)
            return 1
        mime = "image/svg+xml" if "/svg/" in url else "image/png"
        data = base64.b64encode(body).decode("ascii")
        html = html.replace(f'src="{url}"', f'src="data:{mime};base64,{data}"')

    # The theme scales diagrams with img[src^="https://kroki.io/mermaid/"].
    # Point that selector at the inlined SVGs so the size stays the same.
    html = html.replace(
        '[src^="https://kroki.io/mermaid/"]', '[src^="data:image/svg+xml"]'
    )

    try:
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(html)
    except OSError as err:
        print(f"error: cannot write {target}: {err}", file=sys.stderr)
        return 1
    print(f"inlined {len(urls)} diagrams into {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
