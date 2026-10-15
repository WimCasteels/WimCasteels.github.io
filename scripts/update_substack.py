"""Haalt de laatste edities van de Substack-nieuwsbrief op en schrijft ze naar substack.json.

Draait elke zaterdag via .github/workflows/substack.yml. Lukt het ophalen niet,
dan blijft het bestaande bestand ongewijzigd, zodat de site nooit een leeg blok toont.
"""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

FEED_URL = "https://wimcasteels.substack.com/feed"
OUTPUT = Path(__file__).resolve().parent.parent / "substack.json"
AANTAL = 3


def main():
    try:
        request = urllib.request.Request(FEED_URL, headers={"User-Agent": "wimcasteels.be feed updater"})
        with urllib.request.urlopen(request, timeout=30) as response:
            root = ET.fromstring(response.read())
    except Exception as error:
        print(f"Feed niet opgehaald, bestaand bestand blijft staan: {error}")
        return 0

    edities = []
    for item in root.iter("item"):
        enclosure = item.find("enclosure")
        beschrijving = unescape(re.sub(r"<[^>]+>", "", item.findtext("description") or "")).strip()
        edities.append({
            "title": (item.findtext("title") or "").strip(),
            "date": parsedate_to_datetime(item.findtext("pubDate")).date().isoformat(),
            "url": (item.findtext("link") or "").strip(),
            "description": beschrijving,
            "image": enclosure.get("url") if enclosure is not None else None,
        })
        if len(edities) == AANTAL:
            break

    if not edities:
        print("Geen edities gevonden, bestaand bestand blijft staan.")
        return 0

    OUTPUT.write_text(json.dumps(edities, ensure_ascii=False, indent=4) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(edities)} edities geschreven naar {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
