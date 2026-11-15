"""Haalt de kaartachtergronden op voor index.html: de GRB-basiskaart in grijswaarden (Digitaal Vlaanderen, WMS).

Schrijft kaart-centrum.jpg, kaart-gent.jpg, kaart-regio.jpg en kaart.json (de uitsnedes in Web Mercator).
Omzetten naar JPEG gebeurt met `sips` (macOS); zonder sips blijft het een PNG.
"""
import json, math, os, shutil, subprocess, urllib.request

WMS = ("https://geo.api.vlaanderen.be/GRB-basiskaart-grijs/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap"
       "&LAYERS=GRB_BSK_GRIJS&STYLES=&CRS=EPSG:3857&FORMAT=image/png")
R = 6378137


def merc(lat, lon):
    return lon * math.pi / 180 * R, math.log(math.tan(math.pi / 4 + lat * math.pi / 360)) * R


scholen = json.load(open("schools.json", encoding="utf-8"))
lats = [s["lat"] for s in scholen]
lons = [s["lon"] for s in scholen]
# (zuid, west, noord, oost, breedte in pixels)
UITSNEDES = {
    "centrum": (51.030, 3.695, 51.066, 3.752, 1100),
    "gent": (50.997, 3.655, 51.103, 3.800, 1300),
    "regio": (min(lats) - 0.02, min(lons) - 0.04, max(lats) + 0.02, max(lons) + 0.04, 1100),
}
meta = {}
for naam, (z, w, n, o, px) in UITSNEDES.items():
    x0, y0 = merc(z, w)
    x1, y1 = merc(n, o)
    h = round(px * (y1 - y0) / (x1 - x0))
    url = f"{WMS}&BBOX={x0},{y0},{x1},{y1}&WIDTH={px}&HEIGHT={h}"
    png = f"kaart-{naam}.png"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        open(png, "wb").write(r.read())
    bestand = png
    if shutil.which("sips"):
        bestand = f"kaart-{naam}.jpg"
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "55", png, "--out", bestand],
                       check=True, capture_output=True)
        os.remove(png)
    meta[naam] = {"bestand": bestand, "bbox": [x0, y0, x1, y1], "w": px, "h": h}
    print(naam, bestand, px, h, os.path.getsize(bestand))
json.dump(meta, open("kaart.json", "w"), indent=1)
