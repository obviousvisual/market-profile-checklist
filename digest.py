"""Filter scraped tweets for market-profile content and emit a markdown digest."""
import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

KEYWORDS = [
    # Core market profile
    "market profile", "tpo", "auction", "two-way auction",
    "poc", "vpoc", "naked poc", "npoc",
    "value area", "vah", "val", "value area high", "value area low",
    "initial balance", " ib ", "ib high", "ib low", "ibh", "ibl",
    "single print", "single prints", "buying tail", "selling tail",
    "excess", "no excess",
    "range extension",
    # Day types
    "trend day", "normal day", "normal variation", "neutral day",
    "neutral center", "neutral extreme", "double distribution",
    "non-trend", "non trend",
    # Open types
    "open drive", "open test drive", "open rejection reverse", "open auction",
    "open type",
    # Shapes / structure
    "d-shape", "b-shape", "p-shape", "d shape", "b shape", "p shape",
    "balance", "imbalance", "balanced", "out of balance",
    "composite", "composite profile",
    "hvn", "lvn", "high volume node", "low volume node",
    "spike", "spike base",
    # Behavior
    "acceptance", "rejection", "accepted", "rejected",
    "initiative", "responsive",
    "long liquidation", "short covering",
    "rotation", "migration",
    "otf", "other timeframe", "other time frame",
    # People / canon
    "dalton", "steidlmayer", "mind over markets", "markets in profile",
    # Common profile shorthand
    "rth", "eth", "globex",
    "prior day high", "prior day low", "pdh", "pdl",
]

# Compile word-ish boundaries; keep case-insensitive.
PATTERNS = [(kw, re.compile(rf"(?<!\w){re.escape(kw)}(?!\w)", re.IGNORECASE)) for kw in KEYWORDS]


def matches(text: str) -> list[str]:
    hits = []
    for kw, pat in PATTERNS:
        if pat.search(text):
            hits.append(kw.strip())
    return hits


def parse_date(item: dict) -> datetime | None:
    raw = item.get("createdAt") or item.get("created_at") or item.get("date")
    if not raw:
        return None
    for fmt in (
        "%a %b %d %H:%M:%S %z %Y",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
    ):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


def tweet_url(item: dict, handle: str) -> str:
    if item.get("url"):
        return item["url"]
    tid = item.get("id") or item.get("id_str") or item.get("tweetId")
    return f"https://x.com/{handle}/status/{tid}" if tid else ""


def tweet_text(item: dict) -> str:
    return (item.get("text") or item.get("fullText") or item.get("full_text") or "").strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--handle", default="smashelito")
    parser.add_argument("--in", dest="inp", default=None)
    parser.add_argument("--out", default=None)
    parser.add_argument(
        "--all",
        action="store_true",
        help="Include every tweet (skip keyword filter)",
    )
    args = parser.parse_args()

    inp = Path(args.inp or f"data/{args.handle}_raw.json")
    out = Path(args.out or f"{args.handle}.md")
    if not inp.exists():
        print(f"ERROR: {inp} not found - run scrape.py first", file=sys.stderr)
        return 1

    items = json.loads(inp.read_text())
    by_year: dict[int, list[tuple[datetime, str, str, list[str]]]] = defaultdict(list)
    total = kept = 0
    for item in items:
        total += 1
        if item.get("isRetweet") or item.get("retweeted"):
            continue
        text = tweet_text(item)
        if not text:
            continue
        tags = matches(text)
        if not args.all and not tags:
            continue
        dt = parse_date(item)
        if dt is None:
            continue
        url = tweet_url(item, args.handle)
        by_year[dt.year].append((dt, text, url, tags))
        kept += 1

    lines = [f"# @{args.handle} — market profile digest", ""]
    lines.append(f"_{kept} of {total} tweets matched_  ")
    lines.append(f"_generated {datetime.utcnow().strftime('%Y-%m-%d')}_")
    lines.append("")
    for year in sorted(by_year, reverse=True):
        lines.append(f"## {year}")
        lines.append("")
        for dt, text, url, tags in sorted(by_year[year], key=lambda x: x[0], reverse=True):
            date_str = dt.strftime("%Y-%m-%d")
            link = f"[{date_str}]({url})" if url else date_str
            tag_str = f"  \n_tags: {', '.join(sorted(set(tags)))}_" if tags else ""
            quoted = "\n".join(f"> {ln}" for ln in text.splitlines())
            lines.append(f"### {link}")
            lines.append("")
            lines.append(quoted + tag_str)
            lines.append("")
    out.write_text("\n".join(lines))
    print(f"Wrote {out} ({kept} entries across {len(by_year)} years)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
