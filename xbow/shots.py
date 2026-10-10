"""Shot list of the X-Bow reel: per scene, (clip id, source rush, source in-point s[, options]). Cut by cut-clips.py into
assets/clips/<id>.mp4 (1080x1920 window vx on the 1280x720 rush). The rush stays out of the repository (Drive)."""
RUSHES = "/tmp/claude-0/-home-user-personalbrand/a374c73f-4307-5632-a6b9-84584e511937/scratchpad/xbow_raw"
SRC = "chambord"
SHOTS = {
 "01-hook": [("hook", SRC, 107.3, {"vx": .6})],
 "03-cestquoi": [("cockpit", SRC, 53.2, {"inset": True, "iy": 660})],
 "04-balades": [("b1", SRC, 116.0, {"vx": .5}), ("b2", SRC, 64.0, {"vx": .55}), ("b3", SRC, 255.0, {"vx": .5}),
                ("b4", SRC, 283.0, {"vx": .36}), ("b5", SRC, 345.0, {"vx": .5}), ("b6", SRC, 100.5, {"vx": .42}),
                ("b7", SRC, 208.0, {"vx": .5}), ("b8", SRC, 286.5, {"vx": .5}), ("breath", SRC, 124.0, {"vx": .5})],
}
