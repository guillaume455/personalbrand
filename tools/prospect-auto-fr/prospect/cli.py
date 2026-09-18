"""Ligne de commande du pipeline.

    python -m prospect selfcheck        # que vaut mon accès réseau ?
    python -m prospect sirene           # 1. liste officielle (Sirene open data)
    python -m prospect osm              # 2. POI OpenStreetMap (emails directs)
    python -m prospect match            # 3. appariement Sirene <-> OSM
    python -m prospect resolve          # 4. découverte des sites web
    python -m prospect crawl            # 5. extraction des emails
    python -m prospect validate         # 6. MX + classement
    python -m prospect export           # 7. CSV
    python -m prospect run              # tout d'affilée
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import config, crawl, export, match, osm, resolve, sirene, store, validate


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m prospect",
        description="Pipeline open data : pros de l'auto en France -> emails.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--db", help="chemin de la base SQLite (défaut : data/prospect.sqlite)")
    sub = p.add_subparsers(dest="commande", required=True)

    sub.add_parser("selfcheck", help="teste l'accès aux sources distantes")

    s = sub.add_parser("sirene", help="télécharge et filtre le stock Sirene")
    s.add_argument("--groupes", default=",".join(config.DEFAULT_GROUPS),
                   help="groupes NAF : marchand,reparation,pieces,location")
    s.add_argument("--date-min", default=config.DEFAULT_DATE_MIN)
    s.add_argument("--date-max", default=config.default_date_max())
    s.add_argument("--url-etablissement", dest="url_etab")
    s.add_argument("--url-unite-legale", dest="url_ul")
    s.add_argument("--inclure-fermes", action="store_true",
                   help="garde aussi les établissements fermés")
    s.add_argument("--supprimer-zips", action="store_true")

    o = sub.add_parser("osm", help="récupère les POI auto d'OpenStreetMap")
    o.add_argument("--zones", help="zones à interroger (défaut : toutes)")

    sub.add_parser("match", help="apparie les POI OSM aux SIRET")

    r = sub.add_parser("resolve", help="cherche le site web des établissements")
    r.add_argument("--limite", type=int)
    r.add_argument("--workers", type=int, default=config.CRAWL_WORKERS)
    r.add_argument("--searx", help="URL d'une instance SearXNG (optionnel)")
    r.add_argument("--refaire", action="store_true")

    c = sub.add_parser("crawl", help="extrait les emails des sites retenus")
    c.add_argument("--limite", type=int)
    c.add_argument("--workers", type=int, default=config.CRAWL_WORKERS)
    c.add_argument("--confiance-min", type=int, default=config.MIN_SITE_CONFIDENCE)
    c.add_argument("--refaire", action="store_true")
    c.add_argument("--ignorer-robots", action="store_true",
                   help="déconseillé : ignore robots.txt")

    v = sub.add_parser("validate", help="MX + classement pro/perso")
    v.add_argument("--refaire", action="store_true")

    e = sub.add_parser("export", help="écrit les CSV")
    e.add_argument("--prefixe")
    e.add_argument("--sans-filtre-mx", action="store_true",
                   help="exporte aussi les emails dont le domaine n'a pas de MX")

    sub.add_parser("stats", help="état de la base")

    op = sub.add_parser("opposition", help="ajoute des emails/domaines à ne plus contacter")
    op.add_argument("valeurs", nargs="*", help="emails ou domaines")
    op.add_argument("--fichier", help="fichier texte, une valeur par ligne")
    op.add_argument("--motif", default="demande de la personne")

    ih = sub.add_parser("inspect-header", help="affiche l'en-tête d'un zip Sirene")
    ih.add_argument("zip", help="chemin du zip (data/cache/StockEtablissement.zip)")

    run = sub.add_parser("run", help="enchaîne toutes les étapes")
    run.add_argument("--groupes", default=",".join(config.DEFAULT_GROUPS))
    run.add_argument("--date-min", default=config.DEFAULT_DATE_MIN)
    run.add_argument("--date-max", default=config.default_date_max())
    run.add_argument("--limite", type=int, help="limite resolve/crawl (test rapide)")
    run.add_argument("--workers", type=int, default=config.CRAWL_WORKERS)
    run.add_argument("--searx")
    return p


def selfcheck() -> int:
    """Dit lesquelles des sources sont joignables depuis cette machine."""
    import requests

    from . import net
    sess = net.session()
    tests = [
        ("data.gouv.fr (jeu Sirene)",
         config.DATAGOUV_API.format(slug=config.DATAGOUV_DATASET), "GET"),
        ("Overpass (OpenStreetMap)", config.OVERPASS_ENDPOINTS[0] + "?data=[out:json];out count;",
         "GET"),
    ]
    ok = True
    if not config.CONTACT_EMAIL:
        print("! PROSPECT_CONTACT_EMAIL non défini : mets-y ton email, c'est la "
              "courtoisie minimale pour crawler (et ça évite des blocages).")
    for nom, url, _ in tests:
        try:
            resp = sess.get(url, timeout=30)
            print(f"  {'OK ' if resp.status_code < 400 else 'KO '} {nom} "
                  f"-> HTTP {resp.status_code}")
            ok = ok and resp.status_code < 400
        except requests.RequestException as exc:
            print(f"  KO  {nom} -> {type(exc).__name__}: {exc}")
            ok = False
    try:
        import dns.resolver
        dns.resolver.Resolver().resolve("insee.fr", "MX")
        print("  OK  résolution DNS/MX")
    except Exception as exc:
        print(f"  KO  résolution DNS/MX -> {type(exc).__name__}")
        ok = False
    if ok:
        print("\nTout est joignable : `python -m prospect run --limite 200` pour un "
              "premier lot de test.")
    else:
        print("\nAu moins une source est injoignable (proxy, pare-feu, VPN ?). "
              "Les étapes concernées échoueront.")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.commande == "selfcheck":
        return selfcheck()
    if args.commande == "inspect-header":
        for col in sirene.inspect_header(Path(args.zip)):
            print(col)
        return 0

    conn = store.connect(args.db)
    if args.commande == "sirene":
        sirene.run(conn, groupes=tuple(args.groupes.split(",")),
                   date_min=args.date_min, date_max=args.date_max,
                   url_etab=args.url_etab, url_ul=args.url_ul,
                   garder_zips=not args.supprimer_zips,
                   inclure_fermes=args.inclure_fermes)
    elif args.commande == "osm":
        osm.run(conn, boites=tuple(args.zones.split(",")) if args.zones else None)
    elif args.commande == "match":
        match.run(conn)
    elif args.commande == "resolve":
        resolve.run(conn, limite=args.limite, workers=args.workers,
                    searx=args.searx, refaire=args.refaire)
    elif args.commande == "crawl":
        if args.ignorer_robots:
            config.RESPECT_ROBOTS = False
            print("! robots.txt ignoré : à tes risques, et jamais sur un site qui "
                  "l'interdit explicitement.")
        config.MIN_SITE_CONFIDENCE = args.confiance_min
        crawl.run(conn, limite=args.limite, workers=args.workers,
                  confiance_min=args.confiance_min, refaire=args.refaire)
    elif args.commande == "validate":
        validate.run(conn, refaire=args.refaire)
    elif args.commande == "export":
        export.run(conn, prefixe=args.prefixe, mx_obligatoire=not args.sans_filtre_mx)
    elif args.commande == "stats":
        export.stats(conn)
    elif args.commande == "opposition":
        valeurs = list(args.valeurs)
        if args.fichier:
            valeurs += Path(args.fichier).read_text(encoding="utf-8").split()
        n = validate.ajouter_opposition(conn, valeurs, args.motif)
        print(f"{n} entrées ajoutées à la liste d'opposition.")
    elif args.commande == "run":
        groupes = tuple(args.groupes.split(","))
        sirene.run(conn, groupes=groupes, date_min=args.date_min, date_max=args.date_max)
        osm.run(conn)
        match.run(conn)
        resolve.run(conn, limite=args.limite, workers=args.workers, searx=args.searx)
        crawl.run(conn, limite=args.limite, workers=args.workers)
        validate.run(conn)
        export.run(conn)
        export.stats(conn)
    return 0


if __name__ == "__main__":
    sys.exit(main())
