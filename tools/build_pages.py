"""Construit index.html (GitHub Pages) à partir de ftm-desk.html.

La page publiée sur claude.ai reçoit son squelette HTML au moment de la publication ;
pour GitHub Pages on l'ajoute ici. Usage : python3 tools/build_pages.py
"""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
body = (root / "ftm-desk.html").read_text(encoding="utf-8")
html = ("<!doctype html>\n<html lang=\"fr\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
        "<meta name=\"robots\" content=\"noindex,nofollow\">\n"
        "<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}"
        "body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n"
        "</head>\n<body>\n" + body + "\n</body>\n</html>\n")
(root / "index.html").write_text(html, encoding="utf-8")
print("index.html", len(html))
