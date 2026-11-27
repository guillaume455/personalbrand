#!/usr/bin/env python3
"""One charte (colours, fonts, logo) for every reel, chosen by the CHARTE environment variable (perso by default).

A reel's build.py writes its HTML with tokens ⟦NAME⟧ instead of literal colours and fonts, then passes it through
apply(); the charte's values replace the tokens. Re-render a reel in another charte with:
    CHARTE=forge python3 build.py && CHARTE=forge bash assemble.sh
The charte files: charte/perso.json (the October orange look) and charte/forge.json (FORGE).
fonts(dst) copies the charte's font files into a project (assets/fonts/charte/), logo_path() gives the logo to use."""
import json, os, re, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = os.environ.get("CHARTE", "perso")
C = json.load(open(os.path.join(HERE, f"{NAME}.json"), encoding="utf-8"))
TOKENS = C["tokens"]


def get(name):
    return TOKENS[name]


def font_face_css(prefix="assets/fonts/charte"):
    """@font-face rules for the charte's fonts, relative to the project root"""
    return "".join(f'    @font-face {{ font-family: "{f["family"]}"; src: url("{prefix}/{os.path.basename(f["file"])}") '
                   f'format("{f["format"]}"); font-weight: {f["weight"]}; }}\n' for f in C["fonts"])


def fonts(project_dir):
    """copy the charte's font files into <project>/assets/fonts/charte/"""
    dst = os.path.join(project_dir, "assets", "fonts", "charte")
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)
    for f in C["fonts"]:
        shutil.copy(os.path.join(HERE, f["file"]), dst)


def logo_path(kind="logo_dark"):
    return os.path.join(HERE, C["logo"][kind]) if C.get("logo", {}).get(kind) else None


def apply(text):
    """replace every ⟦NAME⟧ token; an unknown token is an error (so nothing is left in the old colours)"""
    out = re.sub(r"⟦([A-Z0-9_]+)⟧", lambda m: str(TOKENS[m.group(1)]), text)
    if "⟦" in out:
        raise SystemExit("charte: token left in the output")
    return out
