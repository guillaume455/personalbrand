import os
import sys

from .cli import main

try:
    sys.exit(main())
except KeyboardInterrupt:
    print("\nInterrompu. La base garde l'état : relance la même commande pour reprendre.")
    sys.exit(130)
except BrokenPipeError:
    # `python -m prospect stats | head` ferme le tuyau : sortie propre, pas de trace.
    os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
    sys.exit(0)
