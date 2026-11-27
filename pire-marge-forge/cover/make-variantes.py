import subprocess, os
D = "/home/user/personalbrand/pire-marge-forge/cover"
HEAD = '''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: "T"; src: url("FUJECKA-ExtraBold.ttf"); } @font-face { font-family: "U"; src: url("FUJECKA-Bold.ttf"); }
html,body{margin:0;background:#0A0A0A} #c{position:relative;width:1080px;height:1920px;overflow:hidden;background:#0A0A0A}
.hero{position:absolute;left:0;top:0;width:1080px;object-fit:cover;filter:saturate(0.8) contrast(1.05)}
.fade{position:absolute;left:0;top:0;width:1080px;height:1920px}
.t{position:absolute;left:0;width:1080px;text-align:center;color:#F8F6F3;font-family:"T";text-shadow:0 10px 50px rgba(0,0,0,.6)}
.u{position:absolute;left:0;width:1080px;text-align:center;color:#F8F6F3;font-family:"U";letter-spacing:.04em}
.rule{position:absolute;height:6px;background:#8B7355}
.pill{position:absolute;left:0;width:1080px;text-align:center}
.pill span{display:inline-block;padding:12px 34px;border:2px solid #8B7355;border-radius:6px;background:rgba(10,10,10,.72);color:#F8F6F3;font:46px/1.2 "U";letter-spacing:.06em}
.logo{position:absolute;left:390px;top:1700px;width:300px}
</style></head><body><div id="c">'''
FADE = '<div class="fade" style="background:linear-gradient(rgba(10,10,10,.75) 0%,rgba(10,10,10,.1) 18%,rgba(10,10,10,0) 30%,rgba(10,10,10,.6) 44%,#0A0A0A 60%)"></div>'
END = '<img class="logo" src="forge-entete-fond-sombre.svg"></div></body></html>'
V = {
 "A-ma-pire-marge": None,   # the existing cover
 "B-moins-16800": f'''<img class="hero" src="achat.jpg" style="height:1240px;object-position:50% 70%">{FADE}
  <div class="pill" style="top:330px"><span>MA PIRE MARGE</span></div>
  <div class="t" style="top:780px;font-size:250px;line-height:1">−16 800 €</div><div class="rule" style="left:240px;top:1060px;width:600px"></div>
  <div class="u" style="top:1100px;font-size:72px">SUR UNE FERRARI.</div>
  <div class="u" style="top:1200px;font-size:44px;opacity:.75">ACHETÉE SUR PHOTOS, SANS CONTRÔLE</div>''',
 "C-49000-bloques": f'''<img class="hero" src="cta.jpg" style="height:1240px;object-position:50% 60%;filter:saturate(.45) brightness(.8)">{FADE}
  <div class="t" style="top:700px;font-size:200px;line-height:1">49 000 €</div>
  <div class="t" style="top:910px;font-size:120px;line-height:1">BLOQUÉS</div><div class="rule" style="left:240px;top:1060px;width:600px"></div>
  <div class="u" style="top:1100px;font-size:66px">PENDANT PLUS DE 3 ANS.</div>
  <div class="u" style="top:1200px;font-size:44px;opacity:.75">L'ERREUR QUI COÛTE CHER EN ACHAT-REVENTE</div>''',
 "D-rien-achete": f'''<img class="hero" src="export.jpg" style="height:1240px;object-position:50% 60%">{FADE}
  <div class="pill" style="top:330px"><span>FERRARI 360 MODENA · −16 800 €</span></div>
  <div class="t" style="top:740px;font-size:138px;line-height:1.05">ET SI TU<br>N'AVAIS RIEN<br>ACHETÉ ?</div><div class="rule" style="left:240px;top:1180px;width:600px"></div>
  <div class="u" style="top:1220px;font-size:56px">VENDRE SANS ACHETER.</div>''',
 "E-portrait": '''<img src="guillaume-forge.png" style="position:absolute;left:120px;top:560px;width:840px;filter:saturate(.85)">
  <div class="fade" style="background:linear-gradient(#0A0A0A 0%,rgba(10,10,10,0) 30%,rgba(10,10,10,0) 60%,rgba(10,10,10,.85) 75%,#0A0A0A 85%)"></div>
  <div class="t" style="top:300px;font-size:150px;line-height:1">MA PIRE MARGE</div><div class="rule" style="left:240px;top:470px;width:600px"></div>
  <div class="t" style="top:1300px;font-size:200px;line-height:1">−16 800 €</div>
  <div class="u" style="top:1520px;font-size:56px">SUR UNE FERRARI</div>''',
}
for k, body in V.items():
    if body is None:
        continue
    open(f"{D}/{k}.html", "w").write(HEAD + body + END)
    subprocess.run(["/opt/pw-browsers/chromium_headless_shell", "--no-sandbox", "--allow-file-access-from-files", "--hide-scrollbars",
                    "--window-size=1080,1920", "--virtual-time-budget=3000", f"--screenshot={D}/{k}.png", f"file://{D}/{k}.html"], capture_output=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{D}/{k}.png", "-q:v", "2", f"{D}/variantes/cover-pire-marge-forge-{k}.jpg"])
    os.remove(f"{D}/{k}.png")
subprocess.run(["cp", f"{D}/cover-pire-marge-forge.jpg", f"{D}/variantes/cover-pire-marge-forge-A-ma-pire-marge.jpg"])
