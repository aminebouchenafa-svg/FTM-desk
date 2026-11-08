import sys, json, re, datetime
from numbers_parser import Document
SL = ["06:00","10:15","14:30","18:45","23:00"]
clean = lambda v: "" if v is None else re.sub(r"\s+"," ",str(v)).strip()
src, out = sys.argv[1], sys.argv[2]
d = Document(src); res = {}
for name, mois in [("NOV 26","2026-11"),("dec v2","2026-12"),("dec dec","2026-12b"),("JAN 27","2027-01")]:
    sh = [s for s in d.sheets if s.name==name]
    if not sh: continue
    rows = sh[0].tables[0].rows(values_only=True)
    isd = lambda v: isinstance(v,(datetime.datetime,datetime.date))
    jours = []
    for i, r in enumerate(rows):
        if len(r)>1 and isd(r[1]):
            nxt = rows[i+1] if i+1<len(rows) and not isd(rows[i+1][1]) else [None]*8
            slots = []
            for k in range(5):
                ins = clean(r[2+k]) if len(r)>2+k else ""; crew = clean(nxt[2+k]) if len(nxt)>2+k else ""
                ins = re.sub(r"^TRI\s*[:;]\s*","",ins,flags=re.I).strip()
                if ins or crew: slots.append({"s":k+1,"h":SL[k],"instr":ins,"crew":crew})
            jours.append({"date":r[1].strftime("%Y-%m-%d"),"slots":slots})
    res[mois] = {"mois":mois[:7],"source":f"DOUNIA_SIMU_NG_2027.numbers · feuille {name}","jours":jours}
    print(name, mois, len(jours), jours[0]["date"] if jours else "", jours[-1]["date"] if jours else "", sum(len(j["slots"]) for j in jours))
json.dump(res, open(out,"w"), ensure_ascii=False)
