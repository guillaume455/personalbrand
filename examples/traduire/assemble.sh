#!/bin/bash
# Assemble « Traduire »: storyboard statuses, HeyGen assembler + transitions, then the orchestrator's own layer
# (audio mix, paper bed under the light world, light flood from the caret 4→5, iris from station 0 into the end card 9→10), lint.
set -e
cd "$(dirname "$0")"
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1
S=../../.claude/skills/product-launch-video/scripts
sed -i '' 's/^- status: outline$/- status: animated/' STORYBOARD.md
node $S/assemble-index.mjs --storyboard ./STORYBOARD.md --hyperframes . | tail -3
node $S/transitions.mjs inject --storyboard ./STORYBOARD.md --hyperframes . | tail -2
node $S/transitions.mjs verify --storyboard ./STORYBOARD.md --index ./index.html | tail -1
python3 - <<'EOF'
p = 'index.html'; s = open(p).read()
# frame 9 stays mounted under the iris
i = s.index('data-composition-id="09-apprend"'); j = s.index('data-duration="', i); k = s.index('"', j + 15)
s = s[:j] + 'data-duration="6.8"' + s[k + 1:]
anchor = 'data-composition-id="10-fin"'
i = s.index(anchor); end = s.index('></div>', i) + len('></div>')
fx = '''
      <audio id="mix" data-start="0" data-duration="50.4" data-track-index="11" src="assets/audio/mix-B.wav" data-volume="1"></audio>
      <div id="fxleak" class="clip" data-start="19.65" data-duration="0.9" data-track-index="30" style="position:absolute;inset:0;overflow:hidden;pointer-events:none;z-index:60">
        <div id="fxleak-sweep" style="position:absolute;left:0;top:-200px;width:1400px;height:1480px;opacity:0;mix-blend-mode:screen;background:radial-gradient(ellipse at 50% 50%,rgba(255,176,120,.85) 0%,rgba(212,112,63,.5) 35%,rgba(194,91,40,0) 70%)"></div>
        <div id="fxleak-core" style="position:absolute;left:960px;top:540px;width:600px;height:600px;margin:-300px 0 0 -300px;border-radius:50%;opacity:0;background:radial-gradient(circle,#fffaf4 0%,#f6f1e9 30%,rgba(240,169,127,.9) 50%,rgba(194,91,40,.5) 64%,rgba(194,91,40,0) 76%)"></div>
        <div id="fxleak-streak" style="position:absolute;left:-240px;top:537px;width:2400px;height:6px;border-radius:3px;opacity:0;background:linear-gradient(90deg,rgba(255,220,196,0),#fff1e6 50%,rgba(255,220,196,0));box-shadow:0 0 34px 12px rgba(224,138,92,.7)"></div>
        <div id="fxleak-flash" style="position:absolute;inset:0;opacity:0;background:#f6f1e9"></div>
      </div>
      <div id="fxiris" class="clip" data-start="43.3" data-duration="0.95" data-track-index="31" style="position:absolute;inset:0;overflow:hidden;pointer-events:none;z-index:61">
        <svg width="1920" height="1080" viewBox="0 0 1920 1080" style="position:absolute;inset:0"><circle id="fxiris-ring" cx="560" cy="600" r="0" fill="none" stroke="#d4703f" stroke-width="6" style="filter:drop-shadow(0 0 16px #e08a5c) drop-shadow(0 0 40px rgba(194,91,40,.8))"/></svg>
      </div>'''
s = s[:end] + fx + s[end:]
# paper bed under the light world, so crossfades between two paper frames never show the dark root
bed = '''<div id="paperbed" class="clip" data-start="19.85" data-duration="24.25" data-track-index="12" style="position:absolute;inset:0;background:#f6f1e9"></div>

      '''
k = s.index('<div\n        id="el-01-decennies"')
s = s[:k] + bed + s[k:]
tl = '''        // ── orchestrator layer: light flood from the caret (4→5), iris from station 0 (9→10) ──
        tl.fromTo("#fxleak-core", { scale: 0.02, opacity: 0 }, { scale: 4.6, opacity: 1, duration: 0.22, ease: "expo.in", immediateRender: false }, 19.68);
        tl.fromTo("#fxleak-streak", { scaleX: 0, opacity: 0 }, { scaleX: 1, opacity: 1, duration: 0.16, ease: "power3.in", immediateRender: false }, 19.7);
        tl.fromTo("#fxleak-sweep", { x: 1100, opacity: 0 }, { x: -700, opacity: 1, duration: 0.5, ease: "power2.inOut", immediateRender: false }, 19.68);
        tl.fromTo("#fxleak-flash", { opacity: 0 }, { opacity: 1, duration: 0.1, ease: "power2.in", immediateRender: false }, 19.8);
        tl.to("#fxleak-flash", { opacity: 0, duration: 0.5, ease: "power2.out" }, 19.95);
        tl.to(["#fxleak-core", "#fxleak-streak", "#fxleak-sweep"], { opacity: 0, duration: 0.4, ease: "power2.out" }, 19.92);
        tl.fromTo("#el-10-fin", { clipPath: "circle(0% at 560px 600px)" }, { clipPath: "circle(160% at 560px 600px)", duration: 0.75, ease: "power2.inOut", immediateRender: false }, 43.35);
        tl.fromTo("#fxiris-ring", { attr: { r: 0 } }, { attr: { r: 2492 }, duration: 0.75, ease: "power2.inOut", immediateRender: false }, 43.35);\n        tl.fromTo("#fxiris-ring", { opacity: 0 }, { opacity: 1, duration: 0.08, ease: "none", immediateRender: false }, 43.35);
        tl.to("#fxiris-ring", { opacity: 0, duration: 0.15 }, 44.0);
'''
a = '        tl.to({}, { duration: 50.4 }, 0);'
assert a in s
s = s.replace(a, tl + a)
open(p, 'w').write(s)
print('orchestrator layer patched')
EOF
npx hyperframes lint 2>&1 | grep -E "✗|error\(s\)"
