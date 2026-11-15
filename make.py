from datetime import datetime, timedelta, date
import uuid
E=[]
def t(d,start,end,school,what,note=""):
    E.append((d,start,end,school,what,note))
def a(d,school,what,note="",days=1):
    E.append((d,None,days,school,what,note))
DBSP="Don Bosco Sint-Pieters";DBSDW="Don Bosco Sint-Denijs-Westrem";SB="Sint-Bavohumaniora"
t("2026-11-19","19:30","21:00",DBSP,"Infoavond","Datum en uur volgens de website van de school (15 november 2026): donderdag 19 november; de folder vermeldde 'donderdag 20 november'. Inschrijven via schoolwebsite www.dbsp.gent")
t("2026-11-21","09:30","12:30",DBSDW,"Infovoormiddag","www.donboscosdw.be")
t("2026-11-24","19:30",None,SB,"Infoavond","Inschrijven via www.sintbavogent.be")
a("2026-12-07",DBSP,"Doedagen 6de leerjaar","Voor klassen 6de leerjaar. Inschrijven via info@dbsp.gent",days=5)
for d in ("2026-12-08","2026-12-10","2026-12-11"):
    a(d,"EDUGO campus De Brug","Kennismakingsdag 5de leerjaar","www.edugo.be")
a("2026-12-11","College Paters Jozefieten Melle","Onthaaldag klassen 6de leerjaar","Contact via dir.so@collegemelle.be")
t("2027-01-14","19:30",None,"Sint-Barbaracollege","Infoavond","Inschrijven via www.sint-barbara.be")
t("2027-01-18","19:00",None,"IVIO Binnenhof (1B OV4)","Infomoment","Campus Peperstraat 27. Inschrijven via www.ivio-binnenhof.be")
t("2027-01-19","18:30","20:00","VISO campus Mariakerke","Infoavond eerste jaar","www.viso.be")
t("2027-01-21","12:30","15:40","Sint-Paulus campus Patijntjestraat","Individuele snuffeldag (openklasdag)","www.sintpaulusgent.be")
t("2027-01-21","17:00","19:00","Visitatie","Infobeurs eerste jaar","www.visitatie.be")
t("2026-11-19","19:30",None,"Sint-Lievenscollege Business","Infoavond","Niet in de folder; van de website van de school (15 november 2026). Inschrijven via www.slcb.be")
t("2026-11-19","19:30",None,"Sint-Lievenscollege Humaniora","Infoavond","Niet in de folder; van de website van de school (15 november 2026). Inschrijven via www.sintlievenscollege.be")
t("2027-01-21","19:30","21:30","Sint-Lievenscollege Business","Infoavond","Inschrijven via www.slcb.be")
t("2027-01-21","19:30","21:30","Sint-Lievenscollege Humaniora","Infoavond","Inschrijven via www.sintlievenscollege.be")
t("2027-01-23","10:00","16:00","Nieuwen Bosch Humaniora","Infomoment","www.nieuwenboschhumaniora.be")
t("2027-01-25","19:00","20:00","IVIO Binnenhof (1A OV4)","Infomoment","Campus Molenaarsstraat 30. Inschrijven via www.ivio-binnenhof.be")
t("2027-01-28","19:00",None,"Sint-Paulus campus Patijntjestraat","Infoavond","www.sintpaulusgent.be")
t("2027-01-28","19:30",None,"Sint-Barbaracollege","Infoavond","Inschrijven via www.sint-barbara.be")
t("2027-01-28","19:30",None,SB,"Infoavond","Inschrijven via www.sintbavogent.be")
t("2027-01-29","19:00",None,"EDUGO campus Lochristi","Infoavond","www.edugo.be")
t("2027-01-29","19:30",None,"EDUGO campus De Brug","Infoavond","www.edugo.be")
t("2027-02-02","19:00","21:00","BUSO Sint-Gregorius (OV2 en OV3)","Infoavond","Inschrijven via www.sintgregorius.be")
t("2027-02-02","19:30",None,DBSP,"Infoavond","Inschrijven via schoolwebsite www.dbsp.gent")
t("2027-02-02","19:30",None,"Sint-Janscollege","Infoavond","Campus Heiveld. Inschrijven via www.sjc-gent.be")
a("2027-02-03","EDUGO campus De Brug","Inleefdag 6de leerjaar","www.edugo.be")
t("2027-02-03","19:30",None,"Don Boscocollege Zwijnaarde","Infomoment","Inschrijven via www.dbz.be")
t("2027-02-04","17:00","20:00","Nieuwen Bosch Humaniora","Infoavond en rondleidingen","Voor leerlingen lager onderwijs en hun ouders. www.nieuwenboschhumaniora.be")
t("2027-02-04","18:30","20:00","Instituut voor verpleegkunde Sint-Vincentius","Infomoment eerste graad","www.ivv-gent.be")
t("2027-02-04","19:30",None,"Don Boscocollege Zwijnaarde","Infomoment","Inschrijven via www.dbz.be")
t("2027-02-16","19:00",None,"Sint-Franciscusinstituut Melle","Infoavond toekomstige eerstejaars","Inschrijven via www.sfimelle.be of 09 230 79 11")
t("2027-02-17","14:00","16:30","BUSO Sint-Gregorius (OV2 en OV3)","Infomoment","Inschrijven via www.sintgregorius.be")
t("2027-02-18","18:00","20:00","VISO campus Gent en Mariakerke","Infoavond 1ste graad","www.viso.be")
t("2027-02-20","09:30","15:30","Sint-Laurensscholen Wachtebeke en Zelzate","Openschooldag","www.sint-laurens.be")
t("2027-02-20","10:00","13:00","BenedictusPoort campus Ledeberg en De Deyne","Openschooldag","www.benedictuspoort.be")
t("2027-02-20","10:00","12:00","IVIO Binnenhof (1B OV4)","Openklasdag","Campus Peperstraat 27. Inschrijven via www.ivio-binnenhof.be")
t("2027-02-20","10:00","16:00","Sint-Lievenscollege Business","Leerfestival","Inschrijven via www.slcb.be")
t("2027-02-20","10:00","16:00","Sint-Lievenscollege Humaniora","Leerfestival","Inschrijven via www.sintlievenscollege.be")
for d in ("2027-02-23","2027-02-25"):
    t(d,"09:30","12:00",SB,"Inleefdag 6de leerjaar","Met klas of individueel, na afspraak via sint.bavohumaniora@sbhg.be")
t("2027-03-03","13:30","15:00","BUSO Sint-Gregorius (OV4)","Infomoment","Inschrijven via www.sintgregorius.be")
t("2027-03-03","15:30","17:00","BUSO Sint-Gregorius (OV4)","Infomoment","Inschrijven via www.sintgregorius.be")
t("2027-03-06","10:00","18:00",SB,"Opendeurdag","Inschrijven via www.sintbavogent.be")
t("2027-03-06","10:00","17:00","Sint-Janscollege campus Heiveld","Openschooldag","www.sjc-gent.be")
t("2027-03-06","10:00","16:30","Sint-Franciscusinstituut Melle","Open Dag","www.sfimelle.be")
t("2027-03-06","10:00","16:00","Sint-Paulus campus Patijntjestraat","Openschooldag","www.sintpaulusgent.be")
t("2027-03-06","11:00","17:00","EDUGO campus De Brug en Lochristi","Openschooldag","www.edugo.be")
t("2027-03-06","11:00","17:00","Sint-Barbaracollege","Openschooldag","Inschrijven via www.sint-barbara.be")
t("2027-03-06","13:30","17:00","Sint-Franciscus Evergem","Openschooldag","Plan je bezoek via www.sfevergem.be (knop 'inschrijven')")
t("2027-03-11","18:30","20:00","BUSO Sint-Gregorius (OV4)","Infoavond","Inschrijven via www.sintgregorius.be")
a("2027-03-13","College Paters Jozefieten Melle","Open Schooldag","Geen uur vermeld in folder. Inschrijven via www.collegemelle.be")
a("2027-03-13","VISO campus Mariakerke","Infovoormiddag alle graden","Geen uur vermeld in folder. www.viso.be")
t("2027-03-13","13:30","17:00","Instituut voor verpleegkunde Sint-Vincentius","Openklasdag eerstejaars","www.ivv-gent.be")
t("2027-03-13","13:30","17:00","IVIO Binnenhof (1A OV4)","Openklasdag","Campus Molenaarsstraat 30. Inschrijven via www.ivio-binnenhof.be")
t("2027-03-17","13:00","16:00","Sint-Paulus campus Patijntjestraat","Individuele rondleidingen","Op afspraak. www.sintpaulusgent.be")
t("2027-03-17","15:00",None,"Sint-Laurensscholen Wachtebeke en Zelzate","Infoavond (sessie 15.00 u.)","www.sint-laurens.be")
t("2027-03-17","19:00",None,"Sint-Laurensscholen Wachtebeke en Zelzate","Infoavond (sessie 19.00 u.)","www.sint-laurens.be")
t("2027-03-20","09:00","17:00","Don Boscocollege Zwijnaarde","Open School","www.dbz.be")
t("2027-03-20","09:30","16:00",DBSDW,"Infodag","www.donboscosdw.be")
t("2027-03-20","14:00","18:00","Styrka Secundair Onderwijs","Openschooldag","www.styrka.be")
t("2027-03-20","14:00","17:00","Styrka Secundair Onderwijs@Waterkant","Openschooldag","www.styrka.be/styrkasow")
a("2027-03-20","IVIO Binnenhof (OV1/2/3/4)","Openschooldag alle campussen","Geen uur vermeld in folder. www.ivio-binnenhof.be")
t("2027-03-21","10:30","16:30",DBSP,"Openschooldag","www.dbsp.gent")
a("2027-04-14",DBSP,"Rondleidingen vanaf vandaag (woensdagnamiddag)","Op woensdagnamiddag 14 april of later; afspraak via info@dbsp.gent")
t("2027-04-16","10:00","13:00","BenedictusPoort campus Ledeberg en De Deyne","Openschooldag","Let op: folder vermeldt 'zaterdag 16 april', maar 16/04/2027 is een vrijdag (zaterdag = 17 april). Datum nakijken bij de school. www.benedictuspoort.be")
t("2027-04-17","13:30","17:00","Instituut voor verpleegkunde Sint-Vincentius","Opendeurdag","www.ivv-gent.be")
a("2027-04-24","VISO campus Gent en Mariakerke","Opendeurdag","Geen uur vermeld in folder. www.viso.be")
t("2027-04-24","13:00","17:30","BUSO Sint-Gregorius","Openschooldag","www.sintgregorius.be")
t("2027-05-21","16:00","19:30","Hoger Technisch Instituut Sint-Antonius","Openschooldag","Met persoonlijke rondleidingen en workshops in werkplaatsen. www.htisa.be")
t("2027-05-22","09:30","16:00",DBSDW,"Opendeurdag","www.donboscosdw.be")
t("2027-05-22","09:00","12:00","Sint-Paulus campus Patijntjestraat","Individuele rondleidingen","Op afspraak. www.sintpaulusgent.be")
t("2027-05-22","13:00","17:00","Nieuwen Bosch Humaniora","Openschooldag","www.nieuwenboschhumaniora.be")
t("2027-05-22","13:00","17:00","Onze-Lieve-Vrouwe-instituut","Openschooldag","www.olvigent.be")
t("2027-06-26","13:30","17:00","Instituut voor verpleegkunde Sint-Vincentius","Infomiddag","www.ivv-gent.be")

A={
"led":("Hundelgemsesteenweg 93, 9050 Gent (Ledeberg)",51.0354751,3.7392369),
"dey":("Ebergiste De Deynestraat 2A, 9000 Gent",51.0176056,3.7141601),
"cpj":("Brusselsesteenweg 459, 9090 Melle",50.999432,3.8103437),
"dbz":("Grotesteenweg-Noord 113, 9052 Gent (Zwijnaarde)",51.0138893,3.7039012),
"dbsp":("Koning Albertlaan 70, 9000 Gent",51.0386136,3.7108963),
"dbsdw":("Kortrijksesteenweg 1025, 9051 Gent (Sint-Denijs-Westrem)",51.0226502,3.6993998),
"brug":("Simone Duboisstraat 15, 9041 Gent (Oostakker)",51.084263,3.7689473),
"loch":("Dorp-Oost 32, 9080 Lochristi",51.0963438,3.8362468),
"htisa":("Holstraat 66, 9000 Gent",51.0527178,3.714326),
"ivv":("Molenaarsstraat 30, 9000 Gent",51.0615852,3.7181911),
"nb":("Lange Violettestraat 65, 9000 Gent",51.047272,3.7343878),
"olvi":("Tweebruggenstraat 55, 9000 Gent",51.048276,3.7353287),
"barb":("Savaanstraat 33, 9000 Gent",51.0488586,3.7248135),
"bavo":("Reep 4, 9000 Gent",51.0523937,3.7296323),
"sfe":("Schepenhuisstraat 4, 9940 Evergem",51.1082728,3.7074183),
"sfim":("Tuinstraat 105, 9090 Melle",51.0182924,3.7698769),
"sjc":("Heiveldstraat 117, 9040 Gent (Sint-Amandsberg)",51.0631582,3.756474),
"wach":("Wachtebeke-Dorp 21, 9185 Wachtebeke",51.166756,3.8554317),
"zelz":("Patronagestraat 51, 9060 Zelzate",51.2020843,3.8137755),
"slcb":("Steendam 27, 9000 Gent",51.0572273,3.7295898),
"slch":("Zilverenberg 1, 9000 Gent",51.0554058,3.7316014),
"paul":("Patijntjestraat 45, 9000 Gent",51.0402555,3.7080815),
"vis":("Zandloperstraat 8, 9030 Gent (Mariakerke)",51.0719082,3.6784378),
"visog":("Jan-Baptist Guinardstraat 23, 9000 Gent",51.0466836,3.7249575),
"visom":("Industrieweg 230, 9030 Gent (Mariakerke)",51.0870591,3.6702388),
"greg":("Jules Destréelaan 67, 9050 Gent (Gentbrugge)",51.0296958,3.7753411),
"iviom":("Molenaarsstraat 30, 9000 Gent",51.0615852,3.7181911),
"iviop":("Peperstraat 27, 9000 Gent",51.055467,3.7139891),
"sty":("Ebergiste De Deynestraat 1, 9000 Gent",51.016177,3.7147844),
"styw":("Sint-Juliaanstraat 7, 9000 Gent",51.0337714,3.7327125),
}
M={DBSP:[(DBSP,"dbsp")],DBSDW:[(DBSDW,"dbsdw")],SB:[(SB,"bavo")],
"EDUGO campus De Brug":[(None,"brug")],"College Paters Jozefieten Melle":[(None,"cpj")],"Sint-Barbaracollege":[(None,"barb")],
"IVIO Binnenhof (1B OV4)":[(None,"iviop")],"IVIO Binnenhof (1A OV4)":[(None,"iviom")],"VISO campus Mariakerke":[(None,"visom")],
"Sint-Paulus campus Patijntjestraat":[(None,"paul")],"Visitatie":[(None,"vis")],"Sint-Lievenscollege Business":[(None,"slcb")],
"Sint-Lievenscollege Humaniora":[(None,"slch")],"Nieuwen Bosch Humaniora":[(None,"nb")],"EDUGO campus Lochristi":[(None,"loch")],
"BUSO Sint-Gregorius (OV2 en OV3)":[(None,"greg")],"BUSO Sint-Gregorius (OV4)":[(None,"greg")],"BUSO Sint-Gregorius":[(None,"greg")],
"Sint-Janscollege":[(None,"sjc")],"Sint-Janscollege campus Heiveld":[(None,"sjc")],"Don Boscocollege Zwijnaarde":[(None,"dbz")],
"Instituut voor verpleegkunde Sint-Vincentius":[(None,"ivv")],"Sint-Franciscusinstituut Melle":[(None,"sfim")],
"VISO campus Gent en Mariakerke":[("VISO campus Gent","visog"),("VISO campus Mariakerke","visom")],
"Sint-Laurensscholen Wachtebeke en Zelzate":[("Sint-Laurens Wachtebeke","wach"),("Sint-Laurens Zelzate","zelz")],
"BenedictusPoort campus Ledeberg en De Deyne":[("BenedictusPoort campus Ledeberg","led"),("BenedictusPoort campus De Deyne","dey")],
"EDUGO campus De Brug en Lochristi":[("EDUGO campus De Brug","brug"),("EDUGO campus Lochristi","loch")],
"Sint-Franciscus Evergem":[(None,"sfe")],"Styrka Secundair Onderwijs":[(None,"sty")],"Styrka Secundair Onderwijs@Waterkant":[(None,"styw")],
"IVIO Binnenhof (OV1/2/3/4)":[(None,None)],"Hoger Technisch Instituut Sint-Antonius":[(None,"htisa")],"Onze-Lieve-Vrouwe-instituut":[(None,"olvi")]}
E2=[]
for d,s_,e,school,what,note in E:
    for nm,k in M[school]:
        n2=note
        if k=="ivv": n2="Adres = hoofdcampus; check bij de school op welke campus dit doorgaat. "+note
        if k is None: n2="Alle campussen; geen adres ingevuld. "+note
        E2.append((d,s_,e,nm or school,what,n2,k))
E=E2
U="https://www.kieseenschoolregiogent.be"
E.append(("2027-03-23","09:00","09:30","Kies een school regio Gent","Start aanmeldingen","Aanmelden kan van 23 maart 2027 om 9 uur tot 16 april 2027 om 16 uur via "+U,None))
E.append(("2027-04-16","15:30","16:00","Kies een school regio Gent","Einde aanmeldingen (deadline 16 uur)","Aanmelden kan tot 16 april 2027 om 16 uur via "+U,None))

OK="Bron: onderwijskiezer.be (soort infomoment niet vermeld). Check de website van de school. "
N=[
("Freinetmiddenschool Gent","Offerlaan 1, 9000 Gent",51.0456048,3.7105428,[("2027-01-23","10:00","15:00",""),("2027-03-06","10:00","15:00","")]),
("Freinetatheneum De Wingerd","Neermeerskaai 1, 9000 Gent",51.0436038,3.7104283,[("2027-01-28","18:00","20:00",""),("2027-05-13","18:00","20:00","")]),
("Hotelschool Gent","Lange Violettestraat 12, 9000 Gent",51.0482748,3.7339926,[("2027-03-20","10:00",None,""),("2027-04-16","16:30","20:00","")]),
("Secundair Kunstinstituut (SKI)","Ottogracht 4, 9000 Gent",51.0579233,3.7280522,[("2027-03-20",None,1,"Geen uur vermeld. ")]),
("IVG-School","Nederkouter 112, 9000 Gent",51.0471897,3.7217413,[("2027-03-11",None,1,"'s Avonds; uur niet vermeld. "),("2027-03-16",None,1,"'s Avonds; uur niet vermeld. "),("2027-03-17",None,1,"Geen uur vermeld. "),("2027-04-17",None,1,"Hele dag. ")]),
("Atheneum Wispelberg","Wispelbergstraat 2, 9000 Gent",51.0525695,3.711938,[("2027-02-17","17:00",None,""),("2027-02-26","18:00",None,""),("2027-03-13",None,1,"Geen uur vermeld. ")]),
("GO! middenschool Voskenslaan","Voskenslaan 60, 9000 Gent",51.0330207,3.7066838,[("2027-01-28","19:00",None,""),("2027-03-13","10:00","17:00","")]),
("GO! atheneum Voskenslaan","Voskenslaan 60, 9000 Gent",51.0330207,3.7066838,[("2027-03-13","10:00","14:00","")]),
("GO! atheneum Gentbrugge","Ooievaarsnest 3, 9050 Gent (Gentbrugge)",51.0357021,3.7687846,[("2027-01-28","19:00",None,""),("2027-02-27","13:00","17:00",""),("2027-03-11","19:00",None,"")]),
("GO! atheneum Mariakerke","Amand Casier de ter Bekenlaan 26, 9030 Gent (Mariakerke)",51.0743003,3.6716946,[("2027-03-06","10:00","16:30",""),("2027-03-17","19:00","20:00","")]),
("GO! Einstein Atheneum","Wolfputstraat 38, 9041 Gent (Oostakker)",51.0918767,3.7629001,[("2027-02-02",None,1,"'s Avonds; uur niet vermeld. "),("2027-03-06",None,1,"Hele dag. ")]),
("GO! Tectura Groenkouter","Sint-Baafskouterstraat 129, 9040 Gent (Sint-Amandsberg)",51.0551572,3.7568194,[("2027-03-18","18:30","19:30",""),("2027-04-23","17:00","19:30","")]),
("Richtpunt campus Gent Henleykaai","Henleykaai 83, 9000 Gent",51.0425615,3.7136364,[("2027-03-11",None,1,"'s Avonds; uur niet vermeld. "),("2027-04-20",None,1,"'s Avonds; uur niet vermeld. "),("2027-05-31",None,1,"'s Avonds; uur niet vermeld. ")]),
("Richtpunt campus Godshuizenlaan","Godshuizenlaan 65-75, 9000 Gent",51.0435852,3.7154947,[("2027-03-20","14:00","17:00",""),("2027-05-23","14:00","17:00","")]),
("Kunsthumaniora Sint-Lucas","Oude Houtlei 44, 9000 Gent",51.052983,3.7166292,[("2027-03-13",None,1,"Geen uur vermeld. ")]),
("Middelbare Steinerschool","Kasteellaan 54, 9000 Gent",51.0493229,3.7394451,[("2027-05-01","10:00","18:00","")]),
("Lucernacollege (campus Tweestroom)","Ganzendries 149, 9000 Gent",51.0332255,3.7112016,[("2027-03-21","14:00","17:00","")]),
("Keerpunt Gent","Jozef Kluyskensstraat 29, 9000 Gent",51.0460367,3.7194644,[("2027-02-27",None,1,"Hele dag. ")]),
("Sint-Janscollege campus Visitatie","Visitatiestraat 5, 9040 Gent (Sint-Amandsberg)",51.0621922,3.748537,[("2027-03-06","10:00","17:00","")]),
("EDUGO campus De Toren","Sint-Jozefstraat 10, 9041 Gent (Oostakker)",51.0836271,3.7662148,[("2027-03-06","11:00","17:00","")]),
("EDUGO campus Glorieux","Sint-Jozefstraat 7, 9041 Gent (Oostakker)",51.0843914,3.7659304,[("2027-03-06","11:00","17:30","")]),
]
for i,(nm,ad,la,lo,evs) in enumerate(N):
    A["n%d"%i]=(ad,la,lo)
    for d,s_,e,nt in evs:
        E.append((d,s_,e,nm,"Infodag"+(" (avond)" if "Avonds" in nt else ""),nt+OK,"n%d"%i))
# Scholen die niet in de folder staan: Melle, Merelbeke, Wetteren en GO! Dalton Gent. Adres en coördinaten: Onderwijsaanbod in Vlaanderen.
# Events: (datum, begin, einde of aantal dagen, soort); een lege lijst = geen infomoment gevonden op de website.
WEB="Bron: website van de school, nagekeken op 15 november 2026. "
X=[
("Tectura Tuinbouwschool Melle","Brusselsesteenweg 165, 9090 Melle",51.01437,3.78726,[("2027-01-21",None,1,"Infosessie eerste graad"),("2027-02-23",None,1,"Rondleidingen"),("2027-03-05",None,1,"Rondleidingen"),("2027-04-24",None,1,"Openschooldag")]),
("GO! atheneum Merelbeke","Gaversesteenweg 195, 9820 Merelbeke",50.99833,3.74446,[]),
("GO! atheneum Merelbeke campus Potaardeberg","Potaardeberg 59, 9820 Merelbeke",50.99131,3.74025,[]),
("Scheppersinstituut Wetteren","Cooppallaan 128, 9230 Wetteren",51.00918,3.86855,[("2027-02-02",None,1,"Infomoment"),("2027-02-03",None,1,"Infomoment"),("2027-05-22",None,2,"Opendeurdagen")]),
("GO! Campus Kompas Wetteren","Noordlaan 10, 9230 Wetteren",51.00243,3.87593,[]),
("Mariagaard Wetteren","Oosterzelesteenweg 80, 9230 Wetteren",50.97905,3.83404,[("2027-02-02","18:30","21:00","Infoavond toekomstige eerstejaars"),("2027-04-25","10:00","16:00","Open dag"),("2027-07-01","14:00","19:00","Info- en inschrijfdag")]),
("Sint-Gertrudiscollege Wetteren","Wegvoeringstraat 21, 9230 Wetteren",51.00745,3.88727,[]),
("Sint-Jozefinstituut Wetteren","Wegvoeringstraat 59A, 9230 Wetteren",51.00797,3.8903,[]),
("BuSO Sint-Lodewijk Wetteren","Kwatrechtsteenweg 168, 9230 Wetteren",50.99195,3.83206,[]),
("GO! Dalton Gent campus Portus","Barrestraat 6, 9000 Gent",51.05375,3.72948,[]),
("GO! Dalton Gent campus LEF","Zwijnaardsesteenweg 6, 9820 Merelbeke",50.99638,3.74527,[]),
("Ziekenhuisschool Stad Gent (Melle)","Caritasstraat 76, 9090 Melle",50.99504,3.77589,[]),
]
for i,(nm,ad,la,lo,evs) in enumerate(X):
    A["x%d"%i]=(ad,la,lo)
    for d,s_,e,wat in evs:
        E.append((d,s_,e,nm,wat,WEB,"x%d"%i))
E.sort(key=lambda x:(x[0],x[1] or ""))

def esc(s): return s.replace("\\","\\\\").replace(",","\\,").replace(";","\\;")
def fold(l):
    b=l.encode();out=[]
    while len(b)>73:
        k=73
        while (b[k]&0xC0)==0x80:k-=1
        out.append(b[:k].decode());b=b" "+b[k:]
    out.append(b.decode());return "\r\n".join(out)
L=["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Infomomenten eerstejaars 2027-2028//NL","CALSCALE:GREGORIAN","X-WR-CALNAME:Infomomenten en opendeurdagen 2027-2028","X-WR-TIMEZONE:Europe/Brussels",
"BEGIN:VTIMEZONE","TZID:Europe/Brussels","BEGIN:DAYLIGHT","TZOFFSETFROM:+0100","TZOFFSETTO:+0200","TZNAME:CEST","DTSTART:19700329T020000","RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU","END:DAYLIGHT","BEGIN:STANDARD","TZOFFSETFROM:+0200","TZOFFSETTO:+0100","TZNAME:CET","DTSTART:19701025T030000","RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU","END:STANDARD","END:VTIMEZONE"]
n=0
for d,s,e,school,what,note,k in E:
    L+=["BEGIN:VEVENT",f"UID:{uuid.uuid5(uuid.NAMESPACE_URL,d+str(s)+school+what)}@infomomenten","DTSTAMP:20261115T110000Z"]
    if s is None:
        d0=date.fromisoformat(d);d1=d0+timedelta(days=e)
        L+=[f"DTSTART;VALUE=DATE:{d0:%Y%m%d}",f"DTEND;VALUE=DATE:{d1:%Y%m%d}"]
    else:
        st=datetime.fromisoformat(d+"T"+s)
        if e: en=datetime.fromisoformat(d+"T"+e)
        else:
            en=st+timedelta(minutes=90); note="Einduur niet vermeld in folder (1,5 uur aangenomen). "+note
        L+=[f"DTSTART;TZID=Europe/Brussels:{st:%Y%m%dT%H%M%S}",f"DTEND;TZID=Europe/Brussels:{en:%Y%m%dT%H%M%S}"]
    if k:
        L+=[f"LOCATION:{esc(school+', '+A[k][0]+', België')}",f"GEO:{A[k][1]:.6f};{A[k][2]:.6f}"]
    L+=[f"SUMMARY:{esc(school+' – '+what)}",f"DESCRIPTION:{esc(note)}","END:VEVENT"];n+=1
L.append("END:VCALENDAR")
open("infomomenten-2027-2028-met-adressen.ics","w",encoding="utf-8",newline="").write("\r\n".join(fold(x) for x in L)+"\r\n")
print(n)
