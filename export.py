import json,runpy,warnings
warnings.simplefilter("ignore")
g=runpy.run_path("make.py")
E,A=g["E"],g["A"]
NAMES={"led":"BenedictusPoort campus Ledeberg","dey":"BenedictusPoort campus De Deyne","cpj":"College Paters Jozefieten Melle","dbz":"Don Boscocollege Zwijnaarde","dbsp":"Don Bosco Sint-Pieters","dbsdw":"Don Bosco Sint-Denijs-Westrem","brug":"EDUGO campus De Brug","loch":"EDUGO campus Lochristi","htisa":"Hoger Technisch Instituut Sint-Antonius","ivv":"IVV Sint-Vincentius","nb":"Nieuwen Bosch Humaniora","olvi":"Onze-Lieve-Vrouwe-instituut","barb":"Sint-Barbaracollege","bavo":"Sint-Bavohumaniora","sfe":"Sint-Franciscus Evergem","sfim":"Sint-Franciscusinstituut Melle","sjc":"Sint-Janscollege campus Heiveld","wach":"Sint-Laurens Wachtebeke","zelz":"Sint-Laurens Zelzate","slcb":"Sint-Lievenscollege Business","slch":"Sint-Lievenscollege Humaniora","paul":"Sint-Paulus campus Patijntjestraat","vis":"Visitatie","visog":"VISO campus Gent","visom":"VISO campus Mariakerke","greg":"BUSO Sint-Gregorius","iviom":"IVIO Binnenhof (Molenaarsstraat)","iviop":"IVIO Binnenhof (Peperstraat)","sty":"Styrka Secundair Onderwijs","styw":"Styrka Secundair Onderwijs@Waterkant"}
S={}
def add(k,ev):
    ad,la,lo=A[k]
    key=(la,lo)
    s=S.setdefault(key,{"names":[],"address":ad,"lat":la,"lon":lo,"events":[]})
    nm=NAMES.get(k) or ev["school"]
    if nm not in s["names"]: s["names"].append(nm)
    s["events"].append(ev)
gen=[]
for d,s,e,school,what,note,k in E:
    ev={"d":d,"s":s,"e":e if s else None,"days":e if not s else 1,"what":what,"school":school,"warn":note if ("Let op" in note or "hoofdcampus" in note) else ""}
    if k: add(k,ev)
    elif school.startswith("IVIO"):
        add("iviom",dict(ev)); add("iviop",dict(ev))
    else: gen.append(ev)
for i,(nm,ad,la,lo,evs) in enumerate(g["X"]):  # scholen zonder infomoment horen ook in de lijst
    S.setdefault((la,lo),{"names":[nm],"address":ad,"lat":la,"lon":lo,"events":[]})
out=[]
for s in S.values():
    multi=len(s["names"])>1
    for ev in s["events"]:
        sc=ev.pop("school")
        ev["who"]=sc if (multi or "OV" in sc) else ""
    s["name"]=" / ".join(s["names"]) if multi else s["names"][0]
    if set(s["names"])=={"GO! middenschool Voskenslaan","GO! atheneum Voskenslaan"}: s["name"]="GO! middenschool en atheneum Voskenslaan"
    del s["names"]; s["events"].sort(key=lambda x:(x["d"],x["s"] or ""))
    out.append(s)
out.sort(key=lambda s:s["name"].lower().replace("go! ",""))
json.dump(out,open("schools.json","w"),ensure_ascii=False)
print(len(out),sum(len(s["events"]) for s in out),len(gen))
