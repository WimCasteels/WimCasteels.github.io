"""Download LinkedIn member data via the official DMA Portability APIs.

  python dma_sync.py snapshot    # full historical snapshot (all domains)
  python dma_sync.py changelog   # incremental sync of changelog events (last 28 days)
  python dma_sync.py             # both

Afterwards your posts are merged into posts.json (see posts_store.py).

The access token is read from the LINKEDIN_TOKEN environment variable
(on Windows also from the user-level registry entry, so a fresh shell is not needed).
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from posts_store import update_posts

API = "https://api.linkedin.com"
API_VERSION = "202312"  # the only version these endpoints accept
CHANGELOG_COUNT = 10  # recommended by LinkedIn; max 50
CHANGELOG_WINDOW_MS = 28 * 24 * 3600 * 1000

# Documented snapshot domains (case sensitive). The query without a domain does not
# return all of them, so missing ones are requested individually.
KNOWN_DOMAINS = [
    "ADS_CLICKED", "MEMBER_FOLLOWING", "LOGIN", "RICH_MEDIA", "SEARCHES", "INFERENCE_TAKEOUT",
    "ALL_COMMENTS", "CONTACTS", "EVENTS", "RECEIPTS", "AD_TARGETING", "REGISTRATION", "REVIEWS",
    "ARTICLES", "PATENTS", "GROUPS", "COMPANY_FOLLOWS", "INVITATIONS", "PHONE_NUMBERS",
    "CONNECTIONS", "EMAIL_ADDRESSES", "JOB_POSTINGS", "JOB_APPLICATIONS", "JOB_SEEKER_PREFERENCES",
    "LEARNING", "INBOX", "SAVED_JOBS", "SAVED_JOB_ALERTS", "PROFILE", "SKILLS", "POSITIONS",
    "EDUCATION", "TEST_SCORES", "CAUSES_YOU_CARE_ABOUT", "PUBLICATIONS", "PROJECTS",
    "ORGANIZATIONS", "LANGUAGES", "HONORS", "COURSES", "CERTIFICATIONS", "RECOMMENDATIONS",
    "ENDORSEMENTS", "MEMBER_SHARE_INFO", "SECURITY_CHALLENGE_PIPE", "TRUSTED_GRAPH",
    "MARKETPLACE_ENGAGEMENTS", "MARKETPLACE_PROVIDERS", "MARKETPLACE_OPPORTUNITIES",
    "ACTOR_SAVE_ITEM", "JOB_APPLICANT_SAVED_ANSWERS", "TALENT_QUESTION_SAVED_RESPONSE",
    "PROFILE_SUMMARY", "ALL_LIKES", "ALL_VOTES", "RECEIPTS_LBP", "EASYAPPLY_BLOCKING",
    "LEARNING_COACH_AI_TAKEOUT", "LEARNING_COACH_INBOX", "LEARNING_ROLEPLAY_INBOX",
    "VOLUNTEERING_EXPERIENCES", "ACCOUNT_HISTORY", "INSTANT_REPOSTS",
    "IDENTITY_CREDENTIALS_AND_ASSETS", "ADS_LAN", "PREMIUM_NOTES",
]

DATA_DIR = Path(__file__).parent / "data"
SNAPSHOT_DIR = DATA_DIR / "snapshot"
CHANGELOG_FILE = DATA_DIR / "changelog" / "events.jsonl"
STATE_FILE = DATA_DIR / "changelog" / "state.json"


def get_token():
    token = os.environ.get("LINKEDIN_TOKEN")
    if not token and sys.platform == "win32":
        import winreg

        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
                token, _ = winreg.QueryValueEx(key, "LINKEDIN_TOKEN")
        except OSError:
            pass
    if not token:
        sys.exit("LINKEDIN_TOKEN is not set")
    return token


class ApiError(Exception):
    def __init__(self, status, body):
        super().__init__(f"HTTP {status}: {body[:500]}")
        self.status = status
        self.body = body


def api_get(path, token, retries=5):
    """GET a path (relative to API) and return the parsed JSON, retrying on 429/5xx."""
    req = urllib.request.Request(
        API + path,
        headers={
            "Authorization": f"Bearer {token}",
            "Linkedin-Version": API_VERSION,
            "Content-Type": "application/json",
        },
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                wait = 2 ** attempt * 5
                print(f"  HTTP {e.code}, retrying in {wait}s...")
                time.sleep(wait)
                continue
            raise ApiError(e.code, body) from None
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < retries - 1:
                wait = 2 ** attempt * 5
                print(f"  {e}, retrying in {wait}s...")
                time.sleep(wait)
                continue
            raise


def next_link(response):
    for link in response.get("paging", {}).get("links", []):
        if link.get("rel") == "next":
            return link["href"]
    return None


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def group_articles(records):
    """ARTICLES arrives as HTML files split into one record per line, as if parsed as CSV
    with header "<html>" (so text after the first comma on each line is lost by LinkedIn).
    Reassemble the lines into one record per article."""
    articles, lines = [], []
    for record in records:
        line = record.get("<html>", "")
        lines.append(line)
        if line.strip() == "</html>":
            html = "\n".join(["<html>"] + lines)
            # Titles containing a comma are cut off without a closing tag.
            title = re.search(r"<title>(.*?)(?:</title>|$)", html, re.M)
            url = re.search(r'<h1><a href="([^"]+)"', html)
            created = re.search(r"Created on ([\d-]+ [\d:]+)", html)
            published = re.search(r"Published on ([\d-]+ [\d:]+)", html)
            articles.append(
                {
                    "Title": title.group(1) if title else None,
                    "Url": url.group(1) if url else None,
                    "Created On": created.group(1) if created else None,
                    "Published On": published.group(1) if published else None,
                    "Html": html,
                }
            )
            lines = []
    return articles


def fetch_snapshot_pages(token, domain, domains):
    """Page through the snapshot (optionally for one domain), adding records to domains.
    Returns the number of pages fetched."""
    query = f"&domain={domain}" if domain else ""
    start = 0
    while True:
        try:
            resp = api_get(f"/rest/memberSnapshotData?q=criteria{query}&start={start}", token)
        except ApiError as e:
            # The documented end-of-data signal; "total" is not reliable.
            if "No data found" in e.body:
                return start
            raise
        for element in resp.get("elements", []):
            name = element.get("snapshotDomain", "UNKNOWN")
            records = element.get("snapshotData", [])
            domains.setdefault(name, []).extend(records)
            print(f"  page {start}: {name} (+{len(records)})")
        start += 1
        if not next_link(resp):
            return start


def sync_snapshot(token):
    """Fetch every snapshot page and store the records per domain."""
    print("Snapshot: fetching all domains...")
    domains = {}
    pages = fetch_snapshot_pages(token, None, domains)

    print("Snapshot: requesting domains missing from the full query...")
    seen = {d.upper() for d in domains}
    unavailable = []
    for domain in KNOWN_DOMAINS:
        if domain in seen:
            continue
        try:
            if fetch_snapshot_pages(token, domain, domains) == 0:
                unavailable.append(domain)
        except ApiError as e:
            if e.status != 400:  # 400: domain not supported (anymore)
                raise
            unavailable.append(domain)

    if "ARTICLES" in domains:
        domains["ARTICLES"] = group_articles(domains["ARTICLES"])
    for domain, records in domains.items():
        write_json(SNAPSHOT_DIR / f"{domain}.json", records)
    write_json(
        SNAPSHOT_DIR / "_index.json",
        {
            "fetchedAt": datetime.now(timezone.utc).isoformat(),
            "pages": pages,
            "domains": {d: len(r) for d, r in sorted(domains.items())},
            "unavailable": unavailable,
        },
    )
    total = sum(len(r) for r in domains.values())
    print(f"Snapshot: {total} records in {len(domains)} domains -> {SNAPSHOT_DIR}")
    print(f"  not (yet) available: {', '.join(unavailable)}")


def load_seen_ids():
    seen = set()
    if CHANGELOG_FILE.exists():
        with CHANGELOG_FILE.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    seen.add(json.loads(line)["id"])
    return seen


def sync_changelog(token):
    """Fetch changelog events since the last run and append new ones to events.jsonl."""
    state = json.loads(STATE_FILE.read_text(encoding="utf-8")) if STATE_FILE.exists() else {}
    window_start = int(time.time() * 1000) - CHANGELOG_WINDOW_MS
    start_time = max(state.get("lastProcessedAt", 0), window_start)
    if state.get("lastProcessedAt") and state["lastProcessedAt"] < window_start:
        print("  WARNING: last sync is older than 28 days; events in between may be lost")

    print(f"Changelog: fetching events since {datetime.fromtimestamp(start_time / 1000, timezone.utc):%Y-%m-%d %H:%M} UTC...")
    seen = load_seen_ids()
    new_events = []
    max_processed = state.get("lastProcessedAt", 0)
    path = f"/rest/memberChangeLogs?q=memberAndApplication&count={CHANGELOG_COUNT}&startTime={start_time}"
    while path:
        resp = api_get(path, token)
        elements = resp.get("elements", [])
        for event in elements:
            max_processed = max(max_processed, event.get("processedAt", 0))
            # startTime is inclusive, so the last event of the previous run comes back.
            if event["id"] not in seen:
                seen.add(event["id"])
                new_events.append(event)
        # "total" is unreliable (often 0), so follow next links until a page is empty.
        path = next_link(resp) if elements else None

    if new_events:
        CHANGELOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with CHANGELOG_FILE.open("a", encoding="utf-8") as f:
            for event in sorted(new_events, key=lambda e: e.get("processedAt", 0)):
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
    write_json(
        STATE_FILE,
        {
            "lastProcessedAt": max_processed or start_time,
            "lastRun": datetime.now(timezone.utc).isoformat(),
        },
    )

    summary = {}
    for event in new_events:
        key = f"{event.get('resourceName')} {event.get('method')}"
        summary[key] = summary.get(key, 0) + 1
    print(f"Changelog: {len(new_events)} new events -> {CHANGELOG_FILE}")
    for key, n in sorted(summary.items()):
        print(f"  {n:4d}  {key}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", choices=["snapshot", "changelog", "all"], default="all")
    args = parser.parse_args()

    token = get_token()
    try:
        if args.command in ("snapshot", "all"):
            sync_snapshot(token)
        if args.command in ("changelog", "all"):
            sync_changelog(token)
    except ApiError as e:
        sys.exit(f"API error: {e}")
    total, added = update_posts()
    print(f"posts.json: {total} posts ({added} new)")


if __name__ == "__main__":
    main()
