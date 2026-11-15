"""Bouwt index.html: alle scholen met adres, onderwijsnet, studieaanbod en infomomenten, met filters en een kaart.

Invoer: schools.json (export.py), aanbod.json (fetch_aanbod.py), kaart.json + kaart-*.jpg (fetch_kaart.py), tpl.html.
"""
import base64, datetime, html, json, math, re, uuid

D = json.load(open("schools.json", encoding="utf-8"))
AANBOD = {a["name"]: a for a in json.load(open("aanbod.json", encoding="utf-8"))}
assert len(AANBOD) == len(json.load(open("aanbod.json", encoding="utf-8"))), "dubbele schoolnaam in aanbod.json"
# scholen die alleen in de officiële lijst staan (geen infomomenten opgezocht)
D += [{"name": a["name"], "address": a["address"], "lat": a["lat"], "lon": a["lon"], "events": [], "nieuw": True}
      for a in AANBOD.values() if a.get("nieuw")]
D.sort(key=lambda s: s["name"].lower().replace("go! ", ""))
KAART = json.load(open("kaart.json", encoding="utf-8"))
STEAM = {k: v for k, v in json.load(open("steam.json", encoding="utf-8")).items() if not k.startswith("_")}
assert all(k in AANBOD for k in STEAM), "onbekende schoolnaam in steam.json"
WD = ["ma", "di", "wo", "do", "vr", "za", "zo"]
MN = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
esc = html.escape

# ---------- infomomenten ----------

RAND = ("Melle", "Merelbeke", "Lochristi", "Wachtebeke", "Evergem", "Zelzate", "Wetteren", "Destelbergen", "De Pinte",
        "Sint-Martens-Latem", "Lievegem")


def gemeente(adres):
    """'Reep 4, 9000 Gent' -> 'Gent'; 'Ooievaarsnest 3, 9050 Gent (Gentbrugge)' -> 'Gent (Gentbrugge)'."""
    return adres.split(", ")[-1].split(" ", 1)[1]


def groep(adres):
    """0 = Gent (9000), 1 = deelgemeente van Gent, 2 = gemeente rond Gent, 3 = rest van Oost-Vlaanderen."""
    g = gemeente(adres)
    if g == "Gent":
        return 0
    if g.startswith("Gent ("):
        return 1
    return 2 if any(r in g for r in RAND) else 3


def uur(u):
    return u.replace(":", ".")


def dag(ev):
    d = datetime.date.fromisoformat(ev["d"])
    s = f"{WD[d.weekday()]} {d.day} {MN[d.month - 1]}"
    if ev["days"] > 1:
        e = d + datetime.timedelta(days=ev["days"] - 1)
        s += f" – {WD[e.weekday()]} {e.day} {MN[e.month - 1]}"
    return s


def tijd(ev):
    if not ev["s"]:
        return ""
    return uur(ev["s"]) + (f"–{uur(ev['e'])}" if ev["e"] else "") + " u."


def wie(ev, naam, gemeen=()):
    """Korte aanduiding als een event maar voor een deel van de school geldt."""
    w = ev["who"]
    if not w:
        return ""
    if w.startswith("Instituut voor verpleegkunde"):
        return "IVV"
    m = re.search(r"\(([^)]+)\)$", w)
    if m and (w.startswith(naam) or naam.startswith(w.split(" (")[0])):
        return m.group(1)
    # laat weg wat alle deelscholen gemeen hebben ("GO! middenschool Voskenslaan" -> "middenschool")
    rest = [x for x in w.split() if x not in gemeen]
    return " ".join(rest) or w


def let_op(ev):
    if not ev["warn"]:
        return ""
    return "campus nakijken" if "hoofdcampus" in ev["warn"] else "datum nakijken"


# ---------- onderwijsnet en studieaanbod ----------

NETTEN = [  # sleutel, label, uitleg die verschijnt als je over het label beweegt
    ("go", "GO!", "GO! onderwijs van de Vlaamse Gemeenschap. Officieel onderwijs, ingericht door de Vlaamse Gemeenschap zelf. "
                  "Neutraal: je kiest tussen de erkende godsdiensten of niet-confessionele zedenleer."),
    ("stad", "Stad Gent", "Stedelijk onderwijs Gent. Officieel gesubsidieerd onderwijs, ingericht door de stad. "
                          "Je kiest tussen de erkende godsdiensten of niet-confessionele zedenleer."),
    ("prov", "Provincie", "Provinciaal onderwijs. Officieel gesubsidieerd onderwijs, ingericht door de provincie Oost-Vlaanderen. "
                          "Je kiest tussen de erkende godsdiensten of niet-confessionele zedenleer."),
    ("vrij", "Vrij", "Vrij gesubsidieerd onderwijs. Ingericht door een privé-organisatie, meestal een vzw. De meeste scholen zijn "
                     "katholiek; ook methodescholen zoals Steiner en Freinet horen hierbij. De officiële gegevens maken dat onderscheid niet."),
]
SOORTEN = [("1a", "1ste leerjaar A"), ("1b", "1ste leerjaar B"), ("d", "Doorstroom"), ("da", "Dubbele finaliteit"),
           ("a", "Arbeidsmarkt"), ("bu", "Buitengewoon secundair")]
FIN = {"d": "Doorstroom", "da": "Dubbele finaliteit", "a": "Arbeidsmarkt"}
DOMEINEN = {  # officiële naam (kleine letters) -> (naam op de pagina, afkorting voor de afdruk)
    "stem": ("STEM", "STEM"), "steam": ("STEAM", "STEAM"), "economie en organisatie": ("Economie en organisatie", "Eco"),
    "maatschappij en welzijn": ("Maatschappij en welzijn", "M&W"), "taal en cultuur": ("Taal en cultuur", "Taal"),
    "kunst en creatie": ("Kunst en creatie", "Kunst"), "sport": ("Sport", "Sport"),
    "land- en tuinbouw": ("Land- en tuinbouw", "Land"), "voeding en horeca": ("Voeding en horeca", "Voeding"),
    "domeinoverschrijdend": ("Domeinoverschrijdend", "Algemeen"),
}


BASIS_DOMEIN = {"stem": ["stem"], "economie en organisatie": ["econom", "eco.-org"], "maatschappij en welzijn": ["maatsch"],
                "taal en cultuur": ["talen"], "kunst en creatie": ["kunst"], "sport": ["sport"], "voeding en horeca": ["voeding"]}


METHODES = {"dalton": "Dalton", "freinet": "Freinet", "steiner": "Steiner"}  # herkend aan de (officiële) schoolnaam


def net_van(inst):
    if inst["net"] == "Gemeenschapsonderwijs":
        return "go"
    if inst["net"].startswith("Officieel"):
        return "prov" if "Provincie" in inst["bestuur"] else "stad"
    return "vrij" if inst["net"].startswith("Vrij") else None


def uniek(xs):
    return list(dict.fromkeys(xs))


def profiel(naam):
    """Vat de officiële gegevens van alle instellingen op het adres van de school samen."""
    a = AANBOD.get(naam, {"instellingen": []})
    p = {"netten": [], "tags": [], "basis": [], "fin": {k: {"2": [], "3": []} for k in FIN}, "zeven": [], "anders": [],
         "ov": {}, "dom": [], "officieel": uniek(i["naam"] for i in a["instellingen"]),
         "sites": uniek(i["website"].strip().rstrip("/") for i in a["instellingen"] if i["website"].strip()), "bekend": bool(a["instellingen"])}
    for inst in a["instellingen"]:
        n = net_van(inst)
        if n and n not in p["netten"]:
            p["netten"].append(n)
        for it in inst["aanbod"]:
            g, nm, jaren = it["groep"] or "", it["naam"], it["jaren"]
            dom = re.sub(r"^(studie)?domein ", "", (it["domein"] or "").lower())
            if g == "1ste graad":
                if nm == "1ste leerjaar A":
                    p["tags"].append("1a")
                elif nm == "1ste leerjaar B":
                    p["tags"].append("1b")
                else:
                    p["basis"].append(nm)
                    # basisopties in de eerste graad tellen mee voor het domein ("2A Stem-wetenschappen" -> STEM)
                    p["dom"] += [d for d, sleutels in BASIS_DOMEIN.items() if any(k in nm.lower() for k in sleutels)]
                continue
            if g.startswith("Opleidingsvorm"):
                ov = g.split(":")[0].replace("Opleidingsvorm ", "OV")
                p["tags"].append("bu")
                lijst = p["ov"].setdefault(ov, [])
                if jaren or nm.startswith("ingerichte types"):
                    lijst.append(nm[0].upper() + nm[1:])
                if dom in DOMEINEN and jaren:
                    p["dom"].append(dom)
                continue
            f = "d" if "doorstroomfinaliteit" in g else "da" if "dubbele finaliteit" in g else "a" if "arbeidsmarkt" in g else None
            if f:
                p["tags"].append(f)
                if dom in DOMEINEN:
                    p["dom"].append(dom)
                if "2de" in g and "3de" not in g:
                    p["fin"][f]["2"].append(nm)
                elif "3de" in g and "2de" not in g:
                    p["fin"][f]["3"].append(nm)
                else:
                    if len(jaren) > 0 and jaren[0] != "-":
                        p["fin"][f]["2"].append(nm)
                    if len(jaren) > 1 and jaren[1] != "-":
                        p["fin"][f]["3"].append(nm)
            elif g == "7de leerjaar":
                p["zeven"].append(nm)
            else:
                p["anders"].append(nm)
    namen = " ".join([naam] + p["officieel"]).lower()
    p["meth"] = [m for m in METHODES if m in namen]
    p["steam"] = STEAM.get(naam)
    if p["steam"]:
        p["dom"].append("steam")
        p["bekend"] = True
    for k in ("tags", "basis", "zeven", "anders", "dom"):
        p[k] = uniek(p[k])
    for f in FIN:
        for gr in "23":
            p["fin"][f][gr] = sorted(set(p["fin"][f][gr]), key=str.lower)
    p["ov"] = {k: uniek(v) for k, v in sorted(p["ov"].items())}
    p["tags"] = [k for k, _ in SOORTEN if k in p["tags"]]
    p["dom"] = [d for d in DOMEINEN if d in p["dom"]]
    r = p["basis"] + p["zeven"] + p["anders"] + [x for f in FIN for gr in "23" for x in p["fin"][f][gr]]
    r += [x for v in p["ov"].values() for x in v if not x.startswith("Ingerichte types")]
    if p["steam"]:
        r.append("STEAM")  # zo vindt ook het zoekveld "Studierichting" deze scholen
    p["richtingen"] = uniek(r)
    return p


def aanbod_html(p):
    if not p["bekend"]:
        return '<p class="ab geen">Geen officiële gegevens gevonden over net en studieaanbod.</p>', ""
    kort, krt = [], []
    eerste = [t.upper() for t in p["tags"] if t in ("1a", "1b")]
    if eerste:
        kort.append(" · ".join(eerste))
        krt.append("·".join(eerste))
    fins = [t for t in p["tags"] if t in FIN]
    if fins:
        kort.append(", ".join(FIN[t].lower() for t in fins))
        krt.append(", ".join({"d": "D", "da": "D/A", "a": "A"}[t] for t in fins))
    if p["ov"]:
        kort.append("buitengewoon " + ", ".join(p["ov"]))
        krt.append("BuSO " + ", ".join(p["ov"]))
    if not kort and not p["dom"]:
        kort = krt = ["geen studieaanbod op dit adres in de officiële gegevens"]
    regel = (f'<p class="ab"><span class="soort lang">{esc(" — ".join(kort))}</span>'
             f'<span class="soort krt">{esc(" — ".join(krt))}</span>')
    if p["dom"]:
        lang = ", ".join(DOMEINEN[d][0] for d in p["dom"])
        krt = ", ".join(DOMEINEN[d][1] for d in p["dom"])
        regel += f' <span class="dom lang">{esc(lang)}</span><span class="dom krt">{esc(krt)}</span>'
    regel += "</p>"

    blokken = []

    def blok(titel, items):
        if items:
            blokken.append(f"<dt>{esc(titel)}</dt><dd>{esc(', '.join(items))}</dd>")

    blok("Basisopties 2de jaar", p["basis"])
    for f, titel in FIN.items():
        blok(f"{titel}, 2de graad", p["fin"][f]["2"])
        blok(f"{titel}, 3de graad", p["fin"][f]["3"])
    blok("7de leerjaar", p["zeven"])
    for ov, items in p["ov"].items():
        blok(f"Buitengewoon {ov}", items)
    blok("Andere", p["anders"])
    if p["steam"]:
        blokken.append(f'<dt>STEAM (volgens de school zelf)</dt><dd>{esc(p["steam"]["wat"])} · '
                       f'<a href="{esc(p["steam"]["bron"])}">website van de school</a></dd>')
    detail = ""
    if not blokken and p["sites"]:
        u = p["sites"][0]
        detail = (f'<p class="ab">Website: <a href="{esc(u if u.startswith("http") else "https://" + u)}">'
                  f'{esc(re.sub(r"^https?://(www[.])?", "", u))}</a></p>')
    if blokken:
        n = len(p["richtingen"])
        bron = "Officiële naam: " + "; ".join(p["officieel"])
        links = ", ".join(f'<a href="{esc(u if u.startswith("http") else "https://" + u)}">{esc(re.sub(r"^https?://(www[.])?", "", u))}</a>'
                          for u in p["sites"])
        site = f'<p class="site">Website: {links}</p>' if links else ""
        detail = (f'<details><summary>Studierichtingen ({n})</summary>{site}<dl>{"".join(blokken)}</dl>'
                  f'<p class="bron">{esc(bron)}</p></details>')
    return regel, detail


# ---------- kaart ----------
R = 6378137


def merc(lat, lon):
    return lon * math.pi / 180 * R, math.log(math.tan(math.pi / 4 + lat * math.pi / 360)) * R


VIEWS = [("centrum", "Centrum"), ("gent", "Gent"), ("regio", "Hele regio")]


def netklasse(p):
    """Kleurklasse voor het nummer van de school: één net -> dat net, anders grijs."""
    return "n-" + (p["netten"][0] if len(p["netten"]) == 1 else "geen")


def kaart_html():
    uit = []
    for key, _ in VIEWS:
        k = KAART[key]
        x0, y0, x1, y1 = k["bbox"]
        b64 = base64.b64encode(open(k["bestand"], "rb").read()).decode()
        mime = "image/jpeg" if k["bestand"].endswith(".jpg") else "image/png"
        pins = []
        for i, s in enumerate(D):
            mx, my = merc(s["lat"], s["lon"])
            px, py = (mx - x0) / (x1 - x0) * 100, (y1 - my) / (y1 - y0) * 100
            if 1 < px < 99 and 1 < py < 99:
                pins.append(f'<button type="button" class="pin {netklasse(P[i])}" data-i="{i}" style="left:{px:.2f}%;top:{py:.2f}%" '
                            f'title="{esc(s["name"])}" aria-label="{esc(s["name"])}">{i + 1}</button>')
        uit.append(f'<div class="view" id="view-{key}" data-n="{len(pins)}"{"" if key == "gent" else " hidden"}>'
                   f'<img src="data:{mime};base64,{b64}" width="{k["w"]}" height="{k["h"]}" alt="Kaart {key} met de ligging van de scholen">'
                   f'{"".join(pins)}</div>')
    knoppen = "".join(f'<button type="button" class="tab" data-view="{k}" aria-pressed="{"true" if k == "gent" else "false"}">{t}</button>'
                      for k, t in VIEWS)
    return knoppen, "\n".join(uit)


# ---------- kalender (.ics) ----------
# De pagina plakt de blokken van de aangevinkte scholen tussen KAL_KOP en KAL_VOET; zelfde opbouw als in make.py.
KAL_KOP = "\r\n".join([
    "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Infomomenten eerstejaars 2027-2028//NL", "CALSCALE:GREGORIAN",
    "X-WR-CALNAME:Infomomenten en opendeurdagen 2027-2028", "X-WR-TIMEZONE:Europe/Brussels",
    "BEGIN:VTIMEZONE", "TZID:Europe/Brussels",
    "BEGIN:DAYLIGHT", "TZOFFSETFROM:+0100", "TZOFFSETTO:+0200", "TZNAME:CEST", "DTSTART:19700329T020000",
    "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU", "END:DAYLIGHT",
    "BEGIN:STANDARD", "TZOFFSETFROM:+0200", "TZOFFSETTO:+0100", "TZNAME:CET", "DTSTART:19701025T030000",
    "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU", "END:STANDARD", "END:VTIMEZONE"]) + "\r\n"
KAL_VOET = "END:VCALENDAR\r\n"


def ics_esc(s):
    return s.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;")


def ics_fold(regel):
    b, uit = regel.encode(), []
    while len(b) > 73:
        k = 73
        while (b[k] & 0xC0) == 0x80:
            k -= 1
        uit.append(b[:k].decode())
        b = b" " + b[k:]
    uit.append(b.decode())
    return "\r\n".join(uit)


def ics_info(s, p):
    """Regels over de school voor de beschrijving van elk kalenderitem."""
    r = [s["name"], "Adres: " + s["address"]]
    net = [vol.split(".")[0] for n, _, vol in NETTEN if n in p["netten"]] + [METHODES[m] for m in p["meth"]]
    if net:
        r.append("Onderwijsnet: " + ", ".join(net))
    soort = [t.upper() for t in p["tags"] if t in ("1a", "1b")] + [FIN[t].lower() for t in p["tags"] if t in FIN]
    if p["ov"]:
        soort.append("buitengewoon " + ", ".join(p["ov"]))
    if soort:
        r.append("Aanbod: " + ", ".join(soort))
    if p["dom"]:
        r.append("Studiedomeinen: " + ", ".join(DOMEINEN[d][0] for d in p["dom"]))
    if p["sites"]:
        r.append("Website: " + ", ".join(u if u.startswith("http") else "https://" + u for u in p["sites"]))
    return r


def ics_school(s, p):
    L, info = [], ics_info(s, p)
    for ev in s["events"]:
        d0 = datetime.date.fromisoformat(ev["d"])
        L += ["BEGIN:VEVENT", f"UID:{uuid.uuid5(uuid.NAMESPACE_URL, ev['d'] + str(ev['s']) + s['name'] + ev['what'] + ev['who'])}@infomomenten",
              "DTSTAMP:20261115T110000Z"]
        nota = [x for x in (ev["who"], ev["warn"]) if x]
        if ev["s"] is None:
            L += [f"DTSTART;VALUE=DATE:{d0:%Y%m%d}", f"DTEND;VALUE=DATE:{d0 + datetime.timedelta(days=ev['days']):%Y%m%d}"]
        else:
            st = datetime.datetime.fromisoformat(ev["d"] + "T" + ev["s"])
            if ev["e"]:
                en = datetime.datetime.fromisoformat(ev["d"] + "T" + ev["e"])
            else:
                en = st + datetime.timedelta(minutes=90)
                nota.append("Einduur niet bekend (1,5 uur aangenomen).")
            L += [f"DTSTART;TZID=Europe/Brussels:{st:%Y%m%dT%H%M%S}", f"DTEND;TZID=Europe/Brussels:{en:%Y%m%dT%H%M%S}"]
        nota.append("Controleer datum en uur op de website van de school.")
        L += [f"LOCATION:{ics_esc(s['name'] + ', ' + s['address'] + ', België')}", f"GEO:{s['lat']:.6f};{s['lon']:.6f}",
              f"SUMMARY:{ics_esc(s['name'] + ' – ' + ev['what'])}", "DESCRIPTION:" + "\\n".join(ics_esc(x) for x in [ev["what"] + (" (" + ev["who"] + ")" if ev["who"] else "")] + nota[bool(ev["who"]):] + [""] + info),
              "END:VEVENT"]
    return "".join(ics_fold(x) + "\r\n" for x in L)


# ---------- pagina ----------

def school(i, s, p):
    rows = []
    whos = {ev["who"] for ev in s["events"] if ev["who"]}
    gemeen = set.intersection(*(set(w.split()) for w in whos)) if len(whos) > 1 else set()
    for ev in s["events"]:
        extra = "".join(
            f' <span class="{c}">{esc(x)}</span>'
            for c, x in (("who", wie(ev, s["name"], gemeen)), ("warn", let_op(ev)))
            if x
        )
        rows.append(
            f'<li><span class="dt">{dag(ev)}</span><span class="tm">{tijd(ev)}</span>'
            f'<span class="wt">{esc(ev["what"])}{extra}</span></li>'
        )
    netlabels = "".join(f'<span class="net net-{n}" tabindex="0" data-tip="{esc(vol)}">{esc(lab)}</span>'
                        for n, lab, vol in NETTEN if n in p["netten"])
    netlabels += "".join(f'<span class="meth">{METHODES[m]}</span>' for m in p["meth"])
    regel, detail = aanbod_html(p)
    data = (f'data-i="{i}" data-ll="{s["lat"]},{s["lon"]}" data-net="{" ".join(p["netten"])}" data-meth="{" ".join(p["meth"])}" data-tags="{" ".join(p["tags"])}" '
            f'data-dom="{esc("|".join(p["dom"]))}" data-r="{esc("|".join(x.lower() for x in p["richtingen"]))}"')
    return (
        f'<article class="school" id="s{i}" {data}><h3>'
        + (f'<input type="checkbox" class="kies" id="k{i}" value="{i}" aria-label="Selecteer {esc(s["name"])} voor de kalender">' if rows else "")
        + f'<button type="button" class="num {netklasse(p)}" data-i="{i}" '
        f'aria-label="Toon op de kaart">{i + 1}</button>{esc(s["name"])}</h3>'
        f'<p class="ad">{esc(s["address"])} {netlabels}</p>{regel}{detail}'
        + (f'<ul>{"".join(rows)}</ul>' if rows else '<p class="ab geen">Infomomenten niet opgezocht; zie de website van de school.</p>' if s.get("nieuw")
           else '<p class="ab geen">Geen infomoment gevonden op de website van de school.</p>')
        + "</article>"
    )


P = [profiel(s["name"]) for s in D]
TITELS = ["Gent (9000)", "Deelgemeenten van Gent", "Rond Gent", "Rest van Oost-Vlaanderen"]
groepen = [[], [], [], []]
for i, s in enumerate(D):  # i + 1 is het nummer van de school op de kaart
    groepen[groep(s["address"])].append((i, s))

secties = []
for g, (titel, items) in enumerate(zip(TITELS, groepen)):
    if g:  # buiten 9000: per plaats bij elkaar
        items.sort(key=lambda x: (gemeente(x[1]["address"]).lower(), x[1]["name"].lower().replace("go! ", "")))
    secties.append(
        f'<section class="groep"><h2>{titel} <span class="n"><span class="cnt">{len(items)}</span> scholen</span></h2>'
        f'<div class="cols">{"".join(school(i, s, P[i]) for i, s in items)}</div></section>'
    )

netopties = "".join(
    f'<label class="chip" data-tip="{esc(vol)}"><input type="checkbox" name="net" id="net-{n}" value="{n}"><span><i class="n-{n}"></i>{esc(lab)}</span></label>'
    for n, lab, vol in NETTEN if any(n in p["netten"] for p in P))
soortopties = "".join(f'<option value="{k}">{esc(t)}</option>' for k, t in SOORTEN if any(k in p["tags"] for p in P))
domopties = "".join(f'<option value="{esc(d)}">{esc(DOMEINEN[d][0])}</option>' for d in DOMEINEN if any(d in p["dom"] for p in P))
methopties = "".join(f'<option value="{m}">{lab}</option>' for m, lab in METHODES.items() if any(m in p["meth"] for p in P))
richtingen = sorted({x for p in P for x in p["richtingen"]}, key=str.lower)
datalist = "".join(f'<option value="{esc(x)}">' for x in richtingen)
knoppen, views = kaart_html()
legende = "".join(f'<span tabindex="0" data-tip="{esc(vol)}"><i class="n-{n}"></i>{esc(lab)}</span>' for n, lab, vol in NETTEN if any(n in p["netten"] for p in P))
if any(netklasse(p) == "n-geen" for p in P):
    legende += ('<span tabindex="0" data-tip="Geen net gevonden in de officiële gegevens, of meerdere netten op hetzelfde adres.">'
                '<i class="n-geen"></i>Onbekend of gemengd</span>')

page = open("tpl.html", encoding="utf-8").read()
# Leaflet-stijlen moeten in de pagina zelf staan; verwijzingen naar afbeeldingen die we niet gebruiken gaan eruit
leaflet_css = re.sub(r"url\(images/[^)]*\)", "none", open("leaflet.css", encoding="utf-8").read())
kal = json.dumps({"kop": KAL_KOP, "voet": KAL_VOET, "scholen": {str(i): ics_school(s, P[i]) for i, s in enumerate(D) if s["events"]}},
                 ensure_ascii=False).replace("</", "<\\/")
for k, v in {"__LEAFLET_CSS__": leaflet_css, "__KAL__": kal, "__LEGENDE__": legende, "__SECTIES__": "\n".join(secties), "__N_SCHOLEN__": str(len(D)), "__NETTEN__": netopties, "__SOORTEN__": soortopties,
             "__DOMEINEN__": domopties, "__METHODES__": methopties, "__RICHTINGEN__": datalist, "__TABS__": knoppen, "__VIEWS__": views}.items():
    page = page.replace(k, v)
open("index.html", "w", encoding="utf-8").write(page)
print(len(D), "scholen,", len(richtingen), "studierichtingen,", sum(not p["bekend"] for p in P), "zonder officiële gegevens,",
      round(len(page) / 1e6, 2), "MB")
