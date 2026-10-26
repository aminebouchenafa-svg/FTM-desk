"""Convertit un export TrainerU « Crew Training Schedule » (.xlsx) en document JSON
pour la collection `vols` du tableau FTM Desk.

Usage : python3 tools/import_trainer_u.py <fichier.xlsx> <sortie.json>
Affiche l'identifiant du document (période du rapport) à utiliser comme doc_id.
"""
import json, re, sys, datetime, warnings
import openpyxl

warnings.filterwarnings("ignore")
TYPES = {"i": "Instruction ligne", "n": "Instruction PL pratique", "p": "Pré-contrôle",
         "c": "Contrôle lâché", "e": "Contrôle ligne", "v": "Vol d'évaluation"}
MONTHS = {m: i for i, m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], 1)}

def person(s):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    m = re.match(r"(.+?)\s*-\s*(CP|FO)\s*\((\d+)\)", s)
    if not m:
        return {"nom": s, "pos": "", "id": ""}
    return {"nom": m.group(1).strip(), "pos": m.group(2), "id": m.group(3)}

def main(src, out):
    ws = openpyxl.load_workbook(src, data_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    period = next((str(c) for r in rows for c in r if c and re.search(r"\d\d/\w{3}/\d{4}-", str(c))), "")
    hi = next(i for i, r in enumerate(rows) if r and any(str(c or "").strip() == "Instructor" for c in r))
    head = [str(c or "").strip() for c in rows[hi]]
    col = lambda name: next(i for i, h in enumerate(head) if h.lower().startswith(name.lower()))
    ci, ct, cd, ch, cdate, cf = col("Instructor"), col("Trainee"), col("Description"), col("Time"), col("Date"), col("Flight")
    out_rows = []
    for r in rows[hi + 1:]:
        if not r[ci] or str(r[ci]).startswith(("Selected", "*", "Generated")):
            continue
        desc = re.sub(r"\s+", " ", str(r[cd] or "")).strip()
        code = (re.search(r"\((\w)\)\s*$", desc) or [None, ""])[1]
        d = r[cdate]
        date = d.strftime("%Y-%m-%d") if isinstance(d, datetime.datetime) else "-".join(reversed(str(d).strip().split("/")))
        fl = str(r[cf] or "").strip()
        av = (re.search(r"\((B\w+)\)\s*$", fl) or [None, ""])[1]
        out_rows.append({"date": date, "heure": str(r[ch] or "").strip(), "instr": person(r[ci]), "stagiaire": person(r[ct]),
                         "code": code, "libelle": TYPES.get(code, desc), "vols": re.sub(r"\(B\w+\)\s*$", "", fl).replace("(AH)", "AH").strip(),
                         "avion": av})
    out_rows.sort(key=lambda x: (x["date"], x["heure"]))
    m = re.findall(r"(\d\d)/(\w{3})/(\d{4})", period)
    pid = "_".join(f"{y}-{MONTHS[mo]:02d}-{dd}" for dd, mo, y in m) or datetime.date.today().isoformat()
    doc = {"periode": period.replace(" UTC Times", "").strip(), "importe": datetime.date.today().isoformat(),
           "source": src.split("/")[-1].split("-", 1)[-1], "rows": out_rows}
    json.dump(doc, open(out, "w"), ensure_ascii=False)
    print(pid, len(out_rows))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
