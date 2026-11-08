"""Convertit une feuille de planning simulateur (Excel) en document JSON pour `simu/<AAAA-MM>`.

Format attendu : une ligne par jour (jour, date, puis 5 créneaux S1..S5 avec le TRI),
suivie d'une ligne avec l'équipage ou la séance de chaque créneau.
Usage : python3 tools/import_simu.py <fichier.xlsx> "<nom de feuille>" <AAAA-MM> <sortie.json>
"""
import datetime, json, re, sys, warnings
import openpyxl

warnings.filterwarnings("ignore")
SL = ["06:00", "10:15", "14:30", "18:45", "23:00"]
clean = lambda v: "" if v is None else re.sub(r"\s+", " ", str(v)).strip()

def main(src, sheet, mois, out):
    rows = list(openpyxl.load_workbook(src, data_only=True)[sheet].iter_rows(values_only=True))
    jours = []
    for i, r in enumerate(rows):
        if len(r) > 1 and isinstance(r[1], datetime.datetime):
            nxt = rows[i + 1] if i + 1 < len(rows) and not isinstance(rows[i + 1][1], datetime.datetime) else [None] * 8
            slots = []
            for k in range(5):
                ins = clean(r[2 + k]) if len(r) > 2 + k else ""
                crew = clean(nxt[2 + k]) if len(nxt) > 2 + k else ""
                ins = re.sub(r"^TRI\s*[:;]\s*", "", ins, flags=re.I).strip()
                if ins or crew:
                    slots.append({"s": k + 1, "h": SL[k], "instr": ins, "crew": crew})
            jours.append({"date": r[1].strftime("%Y-%m-%d"), "slots": slots})
    json.dump({"mois": mois, "source": f"{src.split('/')[-1]} · feuille {sheet}", "jours": jours}, open(out, "w"), ensure_ascii=False)
    print(mois, len(jours), "jours,", sum(len(j["slots"]) for j in jours), "séances")

if __name__ == "__main__":
    main(*sys.argv[1:5])
