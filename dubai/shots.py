"""Shot list: per scene, (clip id, source rush, source in-point s, film start cue). Cut by cut-clips.py into
assets/clips/<id>.mp4 (1080x1920, 30 fps, desaturated, plates blurred). The rushes stay out of the repository
(Drive: « Dubai rasso ») and are read from RUSHES."""
RUSHES = "/tmp/claude-0/-home-user-personalbrand/a374c73f-4307-5632-a6b9-84584e511937/scratchpad/dubai_raw"
SHOTS = {
 "01-hook": [("chiron", "20241103_170619", 23.1), ("rollsrow", "20241103_171527", 19.5)],
 "02-nombre": [("wide1", "20241103_170447", 18.5), ("lot", "20241103_170759", 24.0), ("crowd", "20241103_171527", 8.6),
               ("anim", "20241103_173437", 0.4), ("resto", "20260215_124158", 32.0), ("drift", "20241103_150808", 2.0, {"zoom": 2.2, "cx": 0.35, "cy": 0.33}),
               ("wide2", "20241103_170447", 21.0)],
 "03-niveau": [("brabus", "20241103_172121", 0.0, {"blur": [(0, .44, .525), (.7, .52, .558), (1.4, .67, .625), (1.9, .84, .70), (2.4, .95, .76)], "bw": .32, "bh": .085}), ("bugatti", "20241103_170619", 13.2), ("rolls", "20241103_171527", 26.5),
               ("bentley", "20241103_170759", 19.3), ("urus", "20241103_171301", 0.3), ("sixsix", "20241103_170332", 21.0),
               ("parc", "20241103_170759", 26.0), ("sf90", "20241103_171246", 0.0)],
 "04-indifference": [("walk", "20260215_124158", 10.0), ("ferrari", "20260215_124158", 5.5), ("sunset", "20241103_171527", 9.5)],
 "05-details": [("lowrider", "20241103_172145", 1.0), ("gt", "20241103_170619", 17.0), ("orange", "20260215_142714", 5.8),
                ("jantes", "20241103_172121", 8.3), ("concours", "20260215_142805", 3.5)],
 "06-regard": [("enzo", "20260215_124158", 1.0), ("phantom", "20241103_172315", 0.0)],
 "07-cta": [("fin", "20260215_142805", 6.7)],
}
