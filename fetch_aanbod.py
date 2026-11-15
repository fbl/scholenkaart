"""Haalt onderwijsnet en studieaanbod op bij data-onderwijs.vlaanderen.be
(Onderwijsaanbod in Vlaanderen, Vlaams Ministerie van Onderwijs en Vorming) en schrijft aanbod.json.

Neemt alle vestigingsplaatsen secundair onderwijs in Oost-Vlaanderen. Een school uit schools.json krijgt de
instellingen op haar adres; elk ander adres met studieaanbod wordt een nieuwe school ("nieuw": true).
Opgehaalde pagina's worden bewaard in .cache/; wis die map om te verversen.
"""
import html, json, os, re, urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "https://data-onderwijs.vlaanderen.be/onderwijsaanbod/"
PROVINCIE = "4"  # Oost-Vlaanderen
HS = ["311", "312", "321"]  # gewoon, deeltijds en buitengewoon secundair onderwijs
# Scholen die in de officiële lijst op een ander adres staan dan in schools.json: naam -> instellingsnummers
EXTRA = {"Keerpunt Gent": [137381]}  # officieel "Freinetschool Keerpunt", Spitaalpoortstraat 50
DEELGEMEENTEN = {"9030": "Mariakerke", "9031": "Drongen", "9032": "Wondelgem", "9040": "Sint-Amandsberg", "9041": "Oostakker",
                 "9042": "Desteldonk", "9050": "Gentbrugge", "9051": "Sint-Denijs-Westrem", "9052": "Zwijnaarde"}
CACHE = ".cache"
os.makedirs(CACHE, exist_ok=True)


def http(url, data=None):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def cached(name, fn):
    p = os.path.join(CACHE, name)
    if not os.path.exists(p):
        open(p, "w", encoding="utf-8").write(fn())
    return open(p, encoding="utf-8").read()


def lijst(hs):
    """Alle vestigingsplaatsen van één hoofdstructuur in de provincie (per 500 opgevraagd)."""
    uit, pagina = [], 1
    while True:
        p = {
            "AantalRijenPerPagina": 500, "PaginaNummer": pagina, "SorteerVeldNaam": 1, "ToonSQL": False, "Changed": False,
            "isKaart": False, "maxAantalOpKaart": 1000,
            "GeoFilter": {"GeoFilterSoort": 2, "GeoFilterWaarde": "", "Provincie": PROVINCIE, "GeoFilterOpties": []},
            "StructuurFilter": {"HoofdStructuren": [hs], "InstellingsTypes": [], "SoortInstelling": "01", "IsHoofdZetel": False,
                                "Niveaus": [], "SoortenOnderwijs": [], "Taalstelsel": [], "Methode": []},
            "OpleidingFilter": {k: [] for k in ("ohs", "studiegebied", "opleiding", "graad", "onderwijsvorm", "typebuitengewoon",
                                                "leerjaar", "dkovak", "standaardtraject", "methode", "soortleerjaar")},
            "SpecifiekeFilter": "",
        }
        r = json.loads(cached(f"provincie-{PROVINCIE}-{hs}-{pagina}.json",
                              lambda: http(BASE + "webservice/lijsten.svc/AdresLijstPagina", json.dumps(p).encode())))
        uit += r["adressen"]
        if pagina >= r["aantalPaginas"]:
            return uit
        pagina += 1


def norm(adres):
    """'Sint-Jozefstraat 10, 9041 Gent (Oostakker)' -> ('sintjozefstraat', '10', '9041'); busnummers tellen niet mee."""
    a = re.sub(r"\(.*?\)", "", adres).lower()
    m = re.match(r"\s*(\D+?)\s*(\d+)(.*)", a)
    pc = re.search(r"\b(\d{4})\b", m.group(3)) if m else None
    if not pc:
        return None
    return re.sub(r"[^a-z]", "", m.group(1)), m.group(2), pc.group(1)


def tekst(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def fiche(sn):
    t = cached(f"instelling-{sn}.html", lambda: http(BASE + f"instelling?sn={sn}"))
    veld = {}
    for lab, dat in re.findall(r'<div class="fichelabel">(.*?)</div><div class="fichedata">(.*?)</div></div>', t, flags=re.S):
        veld[tekst(lab)] = tekst(dat)
    vest = []
    for adres, body in re.findall(r'<div class="panel-heading"><span>(.*?)</span>.*?<div class="panel-body">(.*?)</table>', t, flags=re.S):
        groep, domein, items = None, None, []
        for rij in re.findall(r"<tr[^>]*>(.*?)</tr>", body, flags=re.S):
            cellen = [(k, tekst(c)) for k, c in re.findall(r'<td[^>]*class="([^"]*)"[^>]*>(.*?)</td>', rij, flags=re.S)]
            if not cellen:
                continue
            klasse, eerste = cellen[0]
            if "gekleurdetabelrij" in klasse:  # "1ste graad", "2de en 3de graad doorstroomfinaliteit", "Opleidingsvorm 3: ..."
                groep, domein = eerste, None
            elif "V41-vet" in klasse:  # "Studiedomein stem", "Domein voeding en horeca", fase in OV3
                domein = eerste
            elif eerste:
                items.append({"groep": groep, "domein": domein, "naam": eerste, "jaren": [c for _, c in cellen[1:]]})
        vest.append({"adres": tekst(adres), "aanbod": items})
    return {"sn": sn, "naam": veld.get("naam", ""), "net": veld.get("onderwijsnet", ""), "bestuur": veld.get("bestuur", ""),
            "website": veld.get("website", ""), "telefoon": veld.get("telefoon", ""), "email": veld.get("e-mail", ""),
            "vestigingen": vest}


def adres_van(p):
    return p["adreslijn1"] + ", " + p["adreslijn2"]


def instellingen_op(hits):
    """De instellingen achter een reeks vestigingsplaatsen, elk met het aanbod op dat adres."""
    uit, gezien = [], set()
    for p in hits:
        if p["instellingsnummer"] in gezien:
            continue
        gezien.add(p["instellingsnummer"])
        f = fiche(p["instellingsnummer"])
        aanbod = [x for v in f["vestigingen"] if norm(v["adres"]) == norm(adres_van(p)) for x in v["aanbod"]]
        uit.append({"sn": f["sn"], "naam": f["naam"], "net": f["net"], "bestuur": f["bestuur"], "website": f["website"],
                    "telefoon": f["telefoon"], "email": f["email"], "adres": adres_van(p), "aanbod": aanbod})
    # een instelling zonder aanbod op dit adres telt alleen mee als er geen andere is (dan kennen we toch net en website)
    return [x for x in uit if x["aanbod"]] or uit


def main():
    plaatsen = [p for hs in HS for p in lijst(hs)]
    with ThreadPoolExecutor(4) as ex:  # vult de cache
        list(ex.map(fiche, sorted({p["instellingsnummer"] for p in plaatsen})))
    per_adres = {}
    for p in plaatsen:
        per_adres.setdefault(norm(adres_van(p)), []).append(p)

    uit, mis, gebruikt = [], [], set()
    for s in json.load(open("schools.json", encoding="utf-8")):
        hits = list(per_adres.get(norm(s["address"]), []))
        gebruikt.add(norm(s["address"]))
        for sn in EXTRA.get(s["name"], []):  # met de hand gekoppeld: alle vestigingen van die instelling
            hits += [p for p in plaatsen if p["instellingsnummer"] == sn]
            gebruikt |= {norm(adres_van(p)) for p in plaatsen if p["instellingsnummer"] == sn}
        inst = instellingen_op(hits)
        if not inst:
            mis.append(s["name"])
        uit.append({"name": s["name"], "address": s["address"], "instellingen": inst})

    nieuw = []
    for n, hits in per_adres.items():
        inst = instellingen_op(hits)
        if n is None or n in gebruikt or not any(i["aanbod"] for i in inst):
            continue
        p = hits[0]
        if not p["lat"]:  # geen ligging bekend: kan niet op de kaart
            print("overgeslagen (geen coördinaten):", p["naam"], adres_van(p))
            continue
        pc, gemeente = p["adreslijn2"].split(" ", 1)
        if gemeente == "Gent" and pc in DEELGEMEENTEN:
            gemeente += f" ({DEELGEMEENTEN[pc]})"
        naam = max(inst, key=lambda i: len(i["aanbod"]))["naam"]
        nieuw.append({"name": naam, "address": f'{p["adreslijn1"]}, {pc} {gemeente}', "lat": float(p["lat"]), "lon": float(p["lon"]),
                      "nieuw": True, "instellingen": inst})
    # zelfde naam op meerdere adressen: straat erbij, en als dat niet volstaat ook het huisnummer
    for deel in (lambda ad: re.sub(r" *[0-9].*", "", ad), lambda ad: ad.split(",")[0]):
        namen = [x["name"] for x in uit + nieuw]
        for x in nieuw:
            if namen.count(x["name"]) > 1:
                x["name"] = f'{x["name"].split(" (")[0] if x.get("dubbel") else x["name"]} ({deel(x["address"])})'
                x["dubbel"] = True
    for x in nieuw:
        x.pop("dubbel", None)
    json.dump(uit + nieuw, open("aanbod.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(uit), "scholen uit schools.json,", len(mis), "zonder koppeling:", mis, "|", len(nieuw), "nieuwe scholen uit de officiële lijst")


if __name__ == "__main__":
    main()
