"""
Download every card icon PNG referenced in the master_<tag>.json files into a local
card_icons/ folder, so build_dashboard.py can embed them as base64 data URLs for a
fully offline-capable crl_opponent_scout.html (no internet needed to see card art).

Pulls all icon variants present in iconUrls: the base card art ("medium"), the
evolved-form art ("evolutionMedium", for cards with an active evolution), and hero
art ("heroMedium", for hero-type cards). Not every card has every variant.

WHY THIS HAS TO RUN HERE (on your Mac, not in the Cowork cloud session): the cloud
sandbox's network is allowlisted and blocks api-assets.clashroyale.com (same
restriction that blocks the main Clash Royale API) -- confirmed via curl returning a
403 from the sandbox's own egress proxy. Your Mac has normal internet access.

HOW TO RUN:
    python3 download_card_icons.py

Then send the whole card_icons/ folder back (or just re-run build_dashboard.py here
in Cowork after staging that folder in) -- build_dashboard.py automatically embeds
the icons as base64 if it finds this folder next to it, and falls back to hotlinking
the live URLs if it doesn't.
"""
import glob
import json
import os
import re
import time
import urllib.request

OUT_DIR = "card_icons"


VARIANTS = {
    "base": "medium",
    "evolution": "evolutionMedium",
    "hero": "heroMedium",
}


def safe_filename(name, variant):
    base = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")
    suffix = "" if variant == "base" else f"_{variant}"
    return f"{base}{suffix}.png"


def find_master_paths():
    paths = sorted(glob.glob("master_*.json"))
    if not paths:
        paths = sorted(glob.glob("/mnt/user-data/uploads/CRL/master_*.json"))
    return paths


def collect_icon_urls():
    # icons[(name, variant)] = url
    icons = {}
    for path in find_master_paths():
        with open(path) as f:
            battles = json.load(f)
        for b in battles:
            for side in ("team", "opponent"):
                for p in b.get(side, []):
                    for c in p.get("cards", []) + p.get("supportCards", []):
                        name = c.get("name")
                        if not name:
                            continue
                        icon_urls = c.get("iconUrls", {})
                        for variant, key in VARIANTS.items():
                            url = icon_urls.get(key)
                            if url and (name, variant) not in icons:
                                icons[(name, variant)] = url
    return icons


def main():
    icons = collect_icon_urls()
    if not icons:
        print("No master_<tag>.json files found (or no cards in them) -- nothing to download.")
        return
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"Found {len(icons)} card/variant combos. Downloading to {OUT_DIR}/ ...")

    manifest = {}
    ok, failed = 0, []
    for (name, variant), url in sorted(icons.items()):
        fname = safe_filename(name, variant)
        dest = os.path.join(OUT_DIR, fname)
        manifest.setdefault(name, {})[variant] = fname
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            ok += 1
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
            with open(dest, "wb") as f:
                f.write(data)
            ok += 1
        except Exception as e:
            failed.append((f"{name} ({variant})", str(e)))
        time.sleep(0.05)

    with open(os.path.join(OUT_DIR, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Done. {ok}/{len(icons)} icons downloaded successfully.")
    if failed:
        print(f"{len(failed)} failed:")
        for name, err in failed:
            print(f"  {name}: {err}")
    print(f"\nNow re-run build_dashboard.py (in this same folder) to bake these into "
          f"crl_opponent_scout.html as embedded images.")


if __name__ == "__main__":
    main()
