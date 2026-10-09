"""Instagram covers (1080x1920) of the reels, same grammar as dubai/cover: hero, hook pill, Anton title with the
orange stroke, orange subtitle, tiles. Key content stays inside the 4:5 grid crop (y 285-1635)."""
import os, subprocess
R = "/home/user/personalbrand"
CSS = """
@font-face { font-family: "Anton"; src: url("../assets/fonts/Anton-400.woff2") format("woff2"); }
@font-face { font-family: "Space Mono"; src: url("../assets/fonts/SpaceMono-700.woff2") format("woff2"); font-weight: 700; }
html, body { margin: 0; background: #0A0A0A; }
#c { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #0A0A0A; }
#halo { position: absolute; left: -60px; top: 200px; width: 1200px; height: 1200px; border-radius: 50%;
  background: radial-gradient(closest-side, rgba(251,128,0,0.22), rgba(251,128,0,0.06) 60%, rgba(251,128,0,0)); }
#hero { position: absolute; left: 0; top: 0; width: 1080px; height: 1240px; object-fit: cover; }
#fade { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px;
  background: linear-gradient(rgba(10,10,10,0.75) 0%, rgba(10,10,10,0.1) 18%, rgba(10,10,10,0) 34%, rgba(10,10,10,0.55) 48%, #0A0A0A 64%); }
#hook { position: absolute; left: 0; top: 300px; width: 1080px; text-align: center; }
#hook span { display: inline-block; padding: 10px 30px; border-radius: 40px; background: #FB8000; color: #0A0A0A;
  font: 50px/1.2 "Anton", sans-serif; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
#t { position: absolute; left: 0; width: 1080px; text-align: center; color: #fff; font-family: "Anton", sans-serif; line-height: 1.04;
  text-shadow: 0 10px 50px rgba(0,0,0,0.6); }
#t i { position: relative; display: inline-block; font-style: normal; }
#t i.u:after { content: ""; position: absolute; left: -2%; right: -2%; bottom: -0.05em; height: 0.09em; background: #FB8000;
  border-radius: 999px; transform: rotate(-1.5deg); clip-path: polygon(0 0, 100% 32%, 100% 68%, 0 100%); }
#t b { color: #FB8000; font-weight: 400; }
#s { position: absolute; left: 0; width: 1080px; text-align: center; color: #FB8000; font: 70px/1.1 "Anton", sans-serif;
  text-shadow: 0 6px 30px rgba(0,0,0,0.6); }
.tile { position: absolute; top: 1240px; width: 320px; height: 380px; border-radius: 22px; overflow: hidden; border: 3px solid #2e2e2e;
  box-shadow: 0 16px 40px rgba(0,0,0,0.55); background: #151515; }
.tile img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; filter: saturate(1.15) contrast(1.06); }
.tile b { position: absolute; left: 0; bottom: 0; width: 100%; padding: 60px 0 16px; text-align: center; font: 40px/1 "Anton", sans-serif;
  color: #fff; font-weight: 400; background: linear-gradient(rgba(0,0,0,0), rgba(0,0,0,0.85)); }
.tile.or { border-color: #FB8000; }
#k { position: absolute; left: 0; top: 1665px; width: 1080px; text-align: center; font: 700 30px/1 "Space Mono", monospace;
  color: #9a9a9a; letter-spacing: 0.14em; }
"""

def tiles(lst):
    x = [30, 380, 730]
    return "".join(f'<div class="tile{" or" if i == 1 else ""}" style="left:{x[i]}px"><img src="{src}" style="object-position:{pos}"><b>{lab}</b></div>'
                   for i, (src, pos, lab) in enumerate(lst))

C = {
 "reprise": dict(hero='<div id="halo"></div><img src="band.png" style="position:absolute;left:0;top:400px;width:1080px;-webkit-mask-image:radial-gradient(closest-side,#000 60%,transparent 100%);mask-image:radial-gradient(closest-side,#000 60%,transparent 100%)">',
   hook="2 ACHETEURS, MÊME PRIX.", title='PRENDS<br><i class="u">L\'ACHETEUR</i><br><b>AVEC REPRISE</b>', ttop=900, tsize=150,
   sub="LA PLUPART CHOISISSENT L'AUTRE", stop=1400, extra="", k="ACHAT-REVENTE AUTO"),
 "montre": dict(hero='<div id="halo"></div><img src="band.png" style="position:absolute;left:90px;top:330px;width:900px;transform:rotate(-2deg)">'
                 '<div style="position:absolute;left:0;top:0;width:1080px;height:1920px;background:linear-gradient(rgba(10,10,10,0) 30%,rgba(10,10,10,0.85) 52%,#0A0A0A 60%)"></div>',
   hook="L'EXTENSION DE GARANTIE", title='NE <s style="text-decoration-color:#FB8000;text-decoration-thickness:0.08em">VENDS</s> PAS.<br><i class="u"><b>MONTRE.</b></i>',
   ttop=1060, tsize=190, sub="MONTRE-LUI 3 CHOSES", stop=1500, extra="", k="VENDEURS AUTO"),
 "pire-marge": dict(hero='<img id="hero" src="achat.jpg" style="object-position:50% 70%;filter:saturate(1.2) contrast(1.08)"><div id="fade"></div>',
   hook="FERRARI 360 MODENA", title='MA PIRE <i class="u"><b>MARGE</b></i>', ttop=690, tsize=200, sub="EN 16 ANS DE MÉTIER",
   stop=1135, ssize=62, extra=tiles([("ph-moteur19.jpg", "50% 50%", "LE MOTEUR"), ("ph-interieur.jpg", "50% 50%", "L'INTÉRIEUR"), ("ph-feux.jpg", "50% 50%", "LES FEUX")]),
   k="JE ME SUIS FAIT AVOIR"),
 "cycles": dict(hero='<img id="hero" src="parc1.jpg" style="object-position:50% 50%;filter:saturate(1.2) contrast(1.08)"><div id="fade"></div>',
   hook="30 000 € · 12 MOIS", title='3 VOITURES,<br><i class="u"><b>3 CYCLES</b></i>', ttop=700, tsize=170, sub="UNE SEULE SORT DU LOT",
   stop=1100, extra=tiles([("mustang.jpg", "50% 50%", "SPORTIVE"), ("x4.jpg", "50% 50%", "SUV"), ("golf.jpg", "50% 50%", "CITADINE")]),
   k="ACHAT-REVENTE AUTO"),
 "marchand": dict(hero='<div id="halo"></div><div style="position:absolute;left:90px;top:420px;width:900px;height:520px;border-radius:26px;overflow:hidden;border:4px solid #FB8000;box-shadow:0 20px 60px rgba(0,0,0,0.6)"><img src="mini.jpg" style="width:100%;height:100%;object-fit:cover"></div>',
   hook="MÊME VOITURE, 2 MÉTIERS", title='MARCHAND<br><span style="font-size:0.5em">OU</span><br><i class="u"><b>INTERMÉDIAIRE ?</b></i>', ttop=990, tsize=150,
   sub="", stop=0, extra="",
   k="ACHAT-REVENTE AUTO"),
 "chiffres": dict(hero='<div id="halo"></div>' + "".join(
     f'<div style="position:absolute;left:0;top:{330 + i * 110}px;width:1080px;text-align:center;font:{100}px/1 Anton;color:{c};opacity:{o}">{v}</div>'
     for i, (v, c, o) in enumerate([("5 500 000", "#fff", .9), ("47 %", "#fff", .7), ("11,1 ANS", "#fff", .55), ("20 200 €", "#fff", .4), ("147 JOURS", "#FB8000", 1)])),
   hook="", title='LE MARCHÉ VO<br>EN <i class="u"><b>5 CHIFFRES</b></i>', ttop=1000, tsize=150, sub="SI T'ES DANS L'AUTO, TU DOIS LES CONNAÎTRE",
   stop=1340, extra="", k="SOURCES : SDES · NGC-DATA · LA CENTRALE · MOBILIANS", ssize=44, ksize=22),
}
for p, c in C.items():
    d = f"{R}/{p}/cover"
    hook = f'<div id="hook"><span>{c["hook"]}</span></div>' if c["hook"] else ""
    sub = f'<div id="s" style="top:{c["stop"]}px;font-size:{c.get("ssize", 70)}px">{c["sub"]}</div>' if c["sub"] else ""
    html = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div id="c">{c["hero"]}{hook}'
            f'<div id="t" style="top:{c["ttop"]}px;font-size:{c["tsize"]}px">{c["title"]}</div>{sub}{c["extra"]}<div id="k" style="font-size:{c.get("ksize", 30)}px">{c["k"]}</div></div></body></html>')
    open(f"{d}/cover.html", "w").write(html)
    open(f"{d}/shot.js", "w").write(open(f"{R}/dubai/cover/shot.js").read().replace("cover-dubai.png", f"cover-{p}.png"))
    subprocess.run(["node", f"{d}/shot.js"], check=True, stdin=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"{d}/cover-{p}.png", "-q:v", "2", f"{d}/cover-{p}.jpg"], check=True)
    os.remove(f"{d}/cover-{p}.png")
    print(p)
