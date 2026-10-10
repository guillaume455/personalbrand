"""Shot list of the X-Bow reel: per scene, (clip id, source rush, source in-point s[, options]). Cut by cut-clips.py into
assets/clips/<id>.mp4 (1080x1920 window vx on the 1280x720 rush). The rush stays out of the repository (Drive)."""
RUSHES = "/tmp/claude-0/-home-user-personalbrand/a374c73f-4307-5632-a6b9-84584e511937/scratchpad/xbow_raw"
SRC = "chambord"
SHOTS = {
 "01-hook": [("hook", SRC, 188.6, {"vx": .45})],
 "03-cestquoi": [("cockpit", SRC, 340.6, {"inset": True, "iy": 660}), ("cockpit2", SRC, 53.7, {"inset": True, "iy": 660})],
 "04-balades": [("b1", SRC, 194.5, {"vx": .45}), ("b2", SRC, 300.0, {"vx": .5}), ("b3", SRC, 326.0, {"vx": .5}),
                ("b4", SRC, 201.0, {"vx": .5}), ("b5", SRC, 362.0, {"vx": .5}), ("b6", SRC, 386.0, {"vx": .5}),
                ("b7", SRC, 347.0, {"vx": .5}), ("b8", SRC, 324.5, {"vx": .5}), ("breath", SRC, 402.5, {"vx": .5})],
}
