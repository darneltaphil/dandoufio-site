#!/usr/bin/env python3
"""
Dandoufio — generateur d'index de galerie.

Usage :
    python3 build-gallery.py

Il scanne le dossier  images/  a cote de ce script.
Chaque SOUS-DOSSIER de images/ est un ALBUM ; les fichiers image qu'il
contient sont les photos de l'album. Le nom du dossier devient le titre
(ex. "ceremonie-2024" -> "Ceremonie 2024").

Il ecrit  gallery.js  (lu par index.html). Relancez-le a chaque fois que
vous ajoutez / retirez un album ou des photos.
"""
import os, json

ROOT = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(ROOT, "images")
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}

def pretty(name: str) -> str:
    return name.replace("-", " ").replace("_", " ").strip().title()

def natural_key(s: str):
    # tri "naturel" : 2.jpg avant 10.jpg
    import re
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]

albums = []
if os.path.isdir(IMAGES_DIR):
    for album in sorted(os.listdir(IMAGES_DIR), key=natural_key):
        apath = os.path.join(IMAGES_DIR, album)
        if not os.path.isdir(apath) or album.startswith('.'):
            continue
        imgs = sorted(
            (f for f in os.listdir(apath)
             if os.path.splitext(f)[1].lower() in EXTS and not f.startswith('.')),
            key=natural_key,
        )
        if not imgs:
            continue
        albums.append({
            "name": pretty(album),
            "slug": album,
            "images": ["images/%s/%s" % (album, f) for f in imgs],
        })

out = "window.GALLERY = " + json.dumps({"albums": albums}, ensure_ascii=False, indent=2) + ";\n"
with open(os.path.join(ROOT, "gallery.js"), "w", encoding="utf-8") as fh:
    fh.write(out)

total = sum(len(a["images"]) for a in albums)
print("%d album(s), %d image(s)  ->  gallery.js" % (len(albums), total))
for a in albums:
    print("   - %-22s %d photo(s)" % (a["name"], len(a["images"])))
if not albums:
    print("Aucun album trouve. Creez  images/<nom-album>/  et ajoutez-y des photos.")
