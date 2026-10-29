"""Zet de laatste nieuwsbrief-edities op de website.

Gebruik (vanuit de map van de website, na een nieuwe editie):
    python scripts/nieuwsbrief.py

Wat het doet:
1. Haalt de 3 laatste edities op van Substack en schrijft ze naar substack.json.
2. Is er iets veranderd, dan commit en pusht het alleen dat bestand.
   GitHub Pages zet de site daarna binnen een paar minuten online.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import update_substack  # noqa: E402


def git(*args, check=True):
    return subprocess.run(["git", *args], cwd=ROOT, check=check, text=True, capture_output=True)


def main():
    print("Edities ophalen bij Substack...")
    if update_substack.main() != 0:
        print("Gestopt: er is niets gecommit.")
        return 1

    if git("diff", "--quiet", "--", "substack.json", check=False).returncode == 0:
        print("Geen nieuwe edities: de site is al up-to-date.")
        return 0

    titel = json.loads((ROOT / "substack.json").read_text(encoding="utf-8"))[0]["title"]
    print(f"Nieuwe editie gevonden: {titel}")

    try:
        git("pull", "--rebase", "--autostash", "origin", "main")
        git("add", "substack.json")
        git("commit", "-m", f"Nieuwsbrief: {titel}", "--", "substack.json")
        git("push", "origin", "main")
    except subprocess.CalledProcessError as error:
        print("Git gaf een fout:")
        print(error.stderr or error.stdout)
        return 1

    print("Gepusht. Binnen een paar minuten staat de nieuwe editie op wimcasteels.be.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
