import sys, json, re, datetime
from numbers_parser import Document
src, out = sys.argv[1], sys.argv[2]
d = Document(src)
isd = lambda v: isinstance(v,(datetime.datetime,datetime.date)) and v.year > 2000
clean = lambda v: "" if v is None else re.sub(r"\s+"," ",str(v)).strip()
SKIP = {"PEQ","SKT","ZFTT","FFS","FBS","FFBS","FFFS","CLVO","RNAV","LVO","UPRT","SIMU","R","CDB","FO","CPT","TRI","TRE","IC","IE","CBTA","B737","NG"}
def names_from(cell):
    t = clean(cell)
    if not t or re.search(r"PEQ\s*\d", t, re.I): return []
    out = []
    for part in re.split(r"\+", t):
        part = re.sub(r"^\s*(CDB|FO|CPT|Cdb|cdb|fo)\s*[:;]?\s*", "", part).strip(" :;-")
        if not part: continue
        w = re.sub(r"[^A-Za-zÀ-ÿ' \-]", " ", part).split()
        if not w or w[0].upper() in SKIP or len(w[0]) < 3: continue
        out.append(" ".join(w[:4]))
    return out
ev = []  # (name, date, sheet)
for sh in d.sheets:
    rows = sh.tables[0].rows(values_only=True)
    grid = sum(1 for r in rows if len(r)>1 and isd(r[1])) >= 8
    if grid:
        for i, r in enumerate(rows):
            if len(r)>1 and isd(r[1]) and i+1 < len(rows):
                nxt = rows[i+1]
                for k in range(2, min(7, len(nxt))):
                    for n in names_from(nxt[k]): ev.append((n, r[1].date().isoformat(), sh.name, "grille"))
    else:
        block = None
        def flush(b):
            if b and b["dates"] and b["names"]:
                last = max(b["dates"])
                for n in b["names"]: ev.append((n, last, sh.name, "équipage"))
        for r in rows:
            cells = [clean(v) if not isd(v) else v for v in r]
            txt = " ".join(c for c in cells if isinstance(c,str))
            if re.search(r"\bCrew\s*\d+", txt, re.I):
                flush(block); block = {"dates": [], "names": []}
            if block is None: continue
            if re.search(r"D[ée]part|Retour", txt, re.I): pass
            else:
                for v in r:
                    if isd(v): block["dates"].append(v.date().isoformat())
            for j, c in enumerate(cells):
                if not isinstance(c, str): continue
                m = re.match(r"^(CDB|FO|CPT)\s*[:;]\s*(.+)$", c, re.I)
                if m: block["names"] += names_from(m.group(2)); continue
                if re.match(r"^(CDB|FO|CPT)\s*[:;]?$", c, re.I):
                    for c2 in cells[j+1:j+3]:
                        if isinstance(c2, str) and c2: block["names"] += names_from(c2); break
        flush(block)
json.dump(ev, open(out, "w"), ensure_ascii=False)
print(len(ev), "séances-pilote")
