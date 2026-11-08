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
        "<meta name=\"apple-mobile-web-app-capable\" content=\"yes\">\n"
        "<meta name=\"mobile-web-app-capable\" content=\"yes\">\n"
        "<meta name=\"apple-mobile-web-app-status-bar-style\" content=\"black-translucent\">\n"
        "<meta name=\"apple-mobile-web-app-title\" content=\"FTM Desk\">\n"
        "<meta name=\"theme-color\" content=\"#3A1FA6\">\n"
        "<link rel=\"manifest\" href=\"manifest.webmanifest\">\n"
        "<link rel=\"apple-touch-icon\" href=\"icons/apple-touch-icon.png\">\n"
        "<link rel=\"icon\" type=\"image/png\" href=\"icons/icon-192.png\">\n"
        "<script>if('serviceWorker' in navigator){addEventListener('load',()=>navigator.serviceWorker.register('sw.js',{updateViaCache:'none'}).then(r=>r.update()).catch(()=>{}));}</script>\n"
        "<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}"
        "body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n"
        "</head>\n<body>\n" + body + "\n</body>\n</html>\n")
(root / "index.html").write_text(html, encoding="utf-8")
print("index.html", len(html))
