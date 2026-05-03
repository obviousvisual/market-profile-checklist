"""Fetch all tweets from a single X account via Apify's Tweet Scraper V2."""
import argparse
import json
import os
import sys
from pathlib import Path

from apify_client import ApifyClient

ACTOR_ID = "apidojo/tweet-scraper"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--handle", default="smashelito", help="X handle without @")
    parser.add_argument("--max-items", type=int, default=10000)
    parser.add_argument("--sort", default="Latest", choices=["Latest", "Top"])
    parser.add_argument("--start", help="YYYY-MM-DD lower bound (optional)")
    parser.add_argument("--end", help="YYYY-MM-DD upper bound (optional)")
    parser.add_argument(
        "--out",
        default=None,
        help="Output JSON path (defaults to data/<handle>_raw.json)",
    )
    args = parser.parse_args()

    token = os.environ.get("APIFY_TOKEN")
    if not token:
        print("ERROR: set APIFY_TOKEN env var (https://console.apify.com/account/integrations)", file=sys.stderr)
        return 1

    out_path = Path(args.out or f"data/{args.handle}_raw.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    run_input: dict = {
        "twitterHandles": [args.handle],
        "maxItems": args.max_items,
        "sort": args.sort,
        "tweetLanguage": "en",
    }
    if args.start:
        run_input["start"] = args.start
    if args.end:
        run_input["end"] = args.end

    client = ApifyClient(token)
    print(f"Starting actor {ACTOR_ID} for @{args.handle} (max {args.max_items})...")
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        print("ERROR: actor run returned no result", file=sys.stderr)
        return 1

    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    out_path.write_text(json.dumps(items, indent=2, ensure_ascii=False))
    print(f"Saved {len(items)} tweets to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
