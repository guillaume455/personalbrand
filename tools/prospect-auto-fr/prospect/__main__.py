import os
import sys

# La console Windows n'est pas en UTF-8 par défaut : sans ça, un simple tiret
# long ou un accent dans un message fait planter le programme (UnicodeEncodeError).
for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass

from .cli import main  # noqa: E402  (après la reconfiguration des flux)

try:
    sys.exit(main())
except KeyboardInterrupt:
    print("\nInterrompu. La base garde l'état : relance la même commande pour reprendre.")
    sys.exit(130)
except BrokenPipeError:
    # `python -m prospect stats | head` ferme le tuyau : sortie propre, pas de trace.
    os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
    sys.exit(0)
