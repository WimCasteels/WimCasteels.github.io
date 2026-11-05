"""posts.json: just your posts, safe to commit, and the only input of build_posts_page.py.

  python posts_store.py      merge the local raw data (data/) into posts.json

dma_sync.py calls update_posts() after every sync. The raw data in data/ stays local:
besides your posts it holds messages, invitations, contacts, ...

Fields per post: date (local time, "YYYY-MM-DD HH:MM"), text, url, sharedUrl, deleted.
Existing posts are kept, so posts.json keeps growing even after the changelog's
28-day window has passed or the raw data is gone.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
POSTS_FILE = ROOT / "posts.json"
CHANGELOG_FILE = ROOT / "data" / "changelog" / "events.jsonl"
SHARES_FILE = ROOT / "data" / "snapshot" / "MEMBER_SHARE_INFO.json"


def post_key(text):
    """Numeric post id from a URN or URL, used to merge the sources."""
    match = re.search(r"(?:share|activity|ugcPost)[:%3A]+(\d+)", text or "")
    return match.group(1) if match else None


def load_posts():
    if not POSTS_FILE.exists():
        return []
    return json.loads(POSTS_FILE.read_text(encoding="utf-8"))


def clean_commentary(text):
    # The export wraps every line in CSV quotes: lines are joined by '"\n"',
    # so a blank line shows up as '"\n""\n"'.
    return text.replace('"\n"', "\n").strip("\n")


def utc_to_local(stamp):
    """'2026-07-01 17:38:57' (UTC) -> '2026-07-01 19:38' in local time."""
    try:
        utc = datetime.strptime(stamp[:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    except ValueError:
        return stamp[:16]
    return utc.astimezone().strftime("%Y-%m-%d %H:%M")


def add_snapshot(posts):
    """Historical posts from the snapshot; they only fill in posts we don't have yet."""
    if not SHARES_FILE.exists():
        return
    # Field names follow LinkedIn's Shares export; read tolerantly in case they differ.
    for record in json.loads(SHARES_FILE.read_text(encoding="utf-8")):
        url = record.get("ShareLink") or record.get("Share Link") or ""
        posts.setdefault(post_key(url) or url, {
            "date": utc_to_local(record.get("Date") or ""),
            "text": clean_commentary(record.get("ShareCommentary") or record.get("Share Commentary") or ""),
            "url": url,
            "sharedUrl": record.get("SharedUrl") or record.get("Shared Url") or "",
            "deleted": False,
        })


def apply_changelog(posts):
    """ugcPosts events: the latest version of a post wins, and deletes are marked."""
    if not CHANGELOG_FILE.exists():
        return
    with CHANGELOG_FILE.open(encoding="utf-8") as f:
        events = [json.loads(line) for line in f if line.strip()]
    for event in sorted(events, key=lambda e: e.get("processedAt", 0)):
        if event.get("resourceName") != "ugcPosts":
            continue
        key = post_key(event.get("resourceId")) or event.get("resourceId")
        if event.get("method") == "DELETE":
            if key in posts:
                posts[key]["deleted"] = True
            continue
        activity = event.get("activity") or {}
        content = activity.get("specificContent", {}).get("com.linkedin.ugc.ShareContent", {})
        urn = activity.get("id") or event.get("resourceId")
        published = activity.get("firstPublishedAt") or activity.get("created", {}).get("time") or event.get("capturedAt")
        posts[key] = {
            "date": datetime.fromtimestamp(published / 1000).strftime("%Y-%m-%d %H:%M"),
            "text": content.get("shareCommentary", {}).get("text", ""),
            "url": f"https://www.linkedin.com/feed/update/{urn}/",
            "sharedUrl": "",
            "deleted": False,
        }


def update_posts():
    """Merge posts.json, the snapshot and the changelog; returns (total, added)."""
    existing = load_posts()
    posts = {post_key(p["url"]) or p["url"]: p for p in existing}
    add_snapshot(posts)
    apply_changelog(posts)
    ordered = sorted(posts.values(), key=lambda p: p["date"], reverse=True)
    POSTS_FILE.write_text(json.dumps(ordered, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return len(ordered), len(ordered) - len(existing)


if __name__ == "__main__":
    total, added = update_posts()
    print(f"posts.json: {total} posts ({added} new) -> {POSTS_FILE}")
