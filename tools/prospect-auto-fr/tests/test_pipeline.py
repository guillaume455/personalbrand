"""Tests hors ligne : aucune requête réseau, tout est simulé."""
from __future__ import annotations

import csv
import io
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from prospect import (annuaire, config, crawl, domaines, export, extract, match, net,  # noqa: E402
                      osm, resolve, sirene, store, validate)

ETAB_HEADER = [
    "siren", "nic", "siret", "statutDiffusionEtablissement", "dateCreationEtablissement",
    "trancheEffectifsEtablissement", "etablissementSiege", "numeroVoieEtablissement",
    "typeVoieEtablissement", "libelleVoieEtablissement", "codePostalEtablissement",
    "libelleCommuneEtablissement", "enseigne1Etablissement",
    "denominationUsuelleEtablissement", "activitePrincipaleEtablissement",
    "nomenclatureActivitePrincipaleEtablissement", "etatAdministratifEtablissement",
    "activitePrincipaleNAF25Etablissement", "complementAdresseEtablissement",
]
UL_HEADER = [
    "siren", "statutDiffusionUniteLegale", "denominationUniteLegale", "nomUniteLegale",
    "prenom1UniteLegale", "categorieJuridiqueUniteLegale",
]


def _zip_csv(path: Path, header: list[str], rows: list[dict]) -> Path:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=header)
    writer.writeheader()
    for row in rows:
        writer.writerow({h: row.get(h, "") for h in header})
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(path.stem + ".csv", buf.getvalue())
    return path


def etab(siret, naf="4511Z", date="2025-03-01", etat="A", diffusion="O", **kw):
    base = {
        "siren": siret[:9], "nic": siret[9:], "siret": siret,
        "statutDiffusionEtablissement": diffusion, "dateCreationEtablissement": date,
        "etablissementSiege": "true", "activitePrincipaleEtablissement": naf,
        "etatAdministratifEtablissement": etat, "codePostalEtablissement": "77000",
        "libelleCommuneEtablissement": "MELUN", "numeroVoieEtablissement": "12",
        "typeVoieEtablissement": "RUE", "libelleVoieEtablissement": "DE PARIS",
        "trancheEffectifsEtablissement": "02",
    }
    base.update(kw)
    return base


class TestSirene(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.conn = store.connect(self.tmp / "db.sqlite")

    def test_filtre_naf_date_etat_diffusion(self):
        rows = [
            etab("11111111100011", enseigne1Etablissement="AUTO PRESTIGE 77"),      # gardé
            etab("22222222200022", naf="4540Z"),                                    # gardé (moto)
            etab("33333333300033", naf="4520A"),                                    # exclu : réparation
            etab("44444444400044", date="2023-12-31"),                              # exclu : trop vieux
            etab("55555555500055", etat="F"),                                       # exclu : fermé
            etab("66666666600066", diffusion="P"),                                  # exclu : non diffusible
            etab("77777777700077", date="2026-09-01", naf="45.11Z"),                # gardé (NAF pointé)
        ]
        zip_path = _zip_csv(self.tmp / "StockEtablissement.zip", ETAB_HEADER, rows)
        gardes = list(sirene.filtrer_etablissements(
            zip_path, sirene.codes_naf(("marchand",)), "2024-01-01", "2026-09-18",
            progress_every=0))
        self.assertEqual(
            sorted(g["siret"] for g in gardes),
            ["11111111100011", "22222222200022", "77777777700077"])
        premier = next(g for g in gardes if g["siret"] == "11111111100011")
        self.assertEqual(premier["adresse"], "12 RUE DE PARIS")
        self.assertEqual(premier["departement"], "77")
        self.assertEqual(premier["enseigne"], "AUTO PRESTIGE 77")
        self.assertEqual(premier["naf_libelle"],
                         "Commerce de voitures et de véhicules automobiles légers")

    def test_enrichissement_unite_legale_et_personne_physique(self):
        rows = [etab("11111111100011"), etab("22222222200022")]
        store.upsert_many(self.conn, "etablissements", list(sirene.filtrer_etablissements(
            _zip_csv(self.tmp / "StockEtablissement.zip", ETAB_HEADER, rows),
            sirene.codes_naf(("marchand",)), "2024-01-01", "2026-12-31", progress_every=0)))
        ul = _zip_csv(self.tmp / "StockUniteLegale.zip", UL_HEADER, [
            {"siren": "111111111", "statutDiffusionUniteLegale": "O",
             "denominationUniteLegale": "AUTO PRESTIGE 77", "categorieJuridiqueUniteLegale": "5710"},
            # personne physique : pas de dénomination, mais nom + prénom
            {"siren": "222222222", "statutDiffusionUniteLegale": "O",
             "nomUniteLegale": "DUPRE", "prenom1UniteLegale": "Jean",
             "categorieJuridiqueUniteLegale": "1000"},
        ])
        sirene.enrichir_unites_legales(ul, self.conn, progress_every=0)
        lignes = {r["siret"]: r for r in self.conn.execute("SELECT * FROM etablissements")}
        self.assertEqual(lignes["11111111100011"]["raison_sociale"], "AUTO PRESTIGE 77")
        self.assertEqual(lignes["11111111100011"]["personne_physique"], 0)
        self.assertEqual(lignes["22222222200022"]["raison_sociale"], "Jean DUPRE")
        self.assertEqual(lignes["22222222200022"]["personne_physique"], 1)

    def test_unite_legale_non_diffusible_supprime_letablissement(self):
        store.upsert_many(self.conn, "etablissements", list(sirene.filtrer_etablissements(
            _zip_csv(self.tmp / "StockEtablissement.zip", ETAB_HEADER, [etab("11111111100011")]),
            sirene.codes_naf(("marchand",)), "2024-01-01", "2026-12-31", progress_every=0)))
        ul = _zip_csv(self.tmp / "StockUniteLegale.zip", UL_HEADER, [
            {"siren": "111111111", "statutDiffusionUniteLegale": "P",
             "nomUniteLegale": "SECRET", "prenom1UniteLegale": "Jean"}])
        sirene.enrichir_unites_legales(ul, self.conn, progress_every=0)
        self.assertEqual(store.count(self.conn, "etablissements"), 0)

    def test_header_inattendu_leve_une_erreur_explicite(self):
        zip_path = _zip_csv(self.tmp / "Bidon.zip", ["colonneA", "colonneB"], [{"colonneA": "x"}])
        with self.assertRaises(RuntimeError) as ctx:
            list(sirene.filtrer_etablissements(zip_path, {"4511Z"}, "2024-01-01",
                                               "2026-12-31", progress_every=0))
        self.assertIn("inspect-header", str(ctx.exception))


class TestMatchOSM(unittest.TestCase):
    def setUp(self):
        self.conn = store.connect(Path(tempfile.mkdtemp()) / "db.sqlite")
        store.upsert_many(self.conn, "etablissements", [
            {"siret": "11111111100011", "siren": "111111111",
             "raison_sociale": "AUTO PRESTIGE 77", "enseigne": None,
             "code_postal": "77000", "commune": "MELUN"},
            {"siret": "22222222200022", "siren": "222222222",
             "raison_sociale": "SARL GARAGE DUPRE ET FILS", "enseigne": "GARAGE DUPRE",
             "code_postal": "69003", "commune": "LYON"},
        ])

    def test_parser_reponse_overpass(self):
        payload = {"elements": [
            {"type": "node", "id": 1, "lat": 48.5, "lon": 2.6, "tags": {
                "shop": "car", "name": "Auto Prestige 77", "addr:postcode": "77000",
                "addr:city": "Melun", "contact:email": "Contact@AutoPrestige77.fr",
                "website": "https://autoprestige77.fr"}},
            {"type": "way", "id": 2, "center": {"lat": 45.7, "lon": 4.8}, "tags": {
                "shop": "car_repair", "name": "Garage Dupré", "addr:city": "Lyon",
                "website": "http://garage-dupre.fr", "ref:FR:SIRET": "22222222200022"}},
            {"type": "node", "id": 3, "tags": {"shop": "car", "name": "Sans contact"}},
        ]}
        lignes = osm.parser_reponse(payload)
        self.assertEqual(len(lignes), 2)  # le POI sans contact est écarté
        self.assertEqual(lignes[0]["email"], "contact@autoprestige77.fr")
        self.assertEqual(lignes[1]["siret_ref"], "22222222200022")

    def test_appariement_par_siret_puis_par_nom(self):
        store.upsert_many(self.conn, "osm_pois", osm.parser_reponse({"elements": [
            {"type": "node", "id": 1, "tags": {
                "name": "AUTO PRESTIGE 77", "addr:postcode": "77000",
                "contact:email": "contact@autoprestige77.fr"}},
            {"type": "way", "id": 2, "tags": {
                "name": "Peu importe", "ref:FR:SIRET": "22222222200022",
                "website": "http://garage-dupre.fr"}},
            {"type": "node", "id": 9, "tags": {
                "name": "Garage Inconnu", "addr:city": "Brest",
                "email": "x@inconnu.fr"}},
        ]}))
        self.assertEqual(match.run(self.conn), 2)
        emails = {r["siret"]: r for r in self.conn.execute("SELECT * FROM emails")}
        self.assertEqual(emails["11111111100011"]["email"], "contact@autoprestige77.fr")
        self.assertEqual(emails["11111111100011"]["source"], "osm:nom_cp")
        sites = {r["siret"]: r for r in self.conn.execute("SELECT * FROM sites")}
        self.assertEqual(sites["22222222200022"]["source"], "osm:ref_siret")
        self.assertEqual(sites["22222222200022"]["confiance"], 5)

    def test_normalisation_ignore_forme_juridique_et_accents(self):
        self.assertEqual(match.normaliser("SARL Garage Dupré & Fils"), "garage dupre fils")
        self.assertEqual(match.normaliser("S.A.S. AUTO-PRESTIGE 77"), "auto prestige 77")


class TestExtraction(unittest.TestCase):
    def cfencode(self, email: str, cle: int = 0x3f) -> str:
        return format(cle, "02x") + "".join(format(ord(c) ^ cle, "02x") for c in email)

    def test_tous_les_patterns_reels(self):
        html = f"""<html><body>
        <a href="mailto:Contact@Garage-Dupre.FR?subject=hello">écrire</a>
        <p>vente &#64;garage-dupre.fr — commercial (at) garage-dupre (dot) fr</p>
        <a class="__cf_email__" data-cfemail="{self.cfencode('direction@garage-dupre.fr')}">x</a>
        <script type="application/ld+json">{{"email":"sav@garage-dupre.fr"}}</script>
        </body></html>"""
        trouves = extract.extraire(html, "https://garage-dupre.fr/")
        self.assertEqual(set(trouves), {
            "contact@garage-dupre.fr", "vente@garage-dupre.fr",
            "commercial@garage-dupre.fr", "direction@garage-dupre.fr",
            "sav@garage-dupre.fr"})
        self.assertEqual(trouves["direction@garage-dupre.fr"], "cfemail")

    def test_faux_positifs_ecartes(self):
        for mauvais in ("logo@2x.png", "sprite@1.5x.jpg", "a@b.css",
                        "deadbeefdeadbeef1234@o1.ingest.sentry.io",
                        "webmaster@site.fr", "nom@votredomaine.fr",
                        "test@example.com", "x@wixpress.com"):
            self.assertIsNone(extract.nettoyer(mauvais), mauvais)

    def test_texte_sans_email_ne_produit_rien(self):
        html = "<p>Ouvert du lundi au vendredi. Véhicules à partir de 12 000 euros a melun.fr</p>"
        self.assertEqual(extract.extraire(html), {})

    def test_liens_contact_priorises_et_internes(self):
        html = """<a href="/mentions-legales">ML</a><a href="/contact">Contact</a>
        <a href="/vehicules-occasion">VO</a><a href="https://facebook.com/x">FB</a>"""
        liens = extract.liens_contact(html, "https://garage-dupre.fr/")
        self.assertEqual(liens, ["https://garage-dupre.fr/mentions-legales",
                                 "https://garage-dupre.fr/contact"])


class TestResolution(unittest.TestCase):
    def test_candidats_domaines(self):
        cands = resolve.candidats_domaines(["SARL GARAGE DUPRE ET FILS"], max_candidats=12)
        self.assertIn("garage-dupre-fils.fr", cands)
        self.assertIn("duprefils.com", cands)
        self.assertTrue(all(c.endswith((".fr", ".com")) for c in cands))

    def test_score_page(self):
        conn = store.connect(Path(tempfile.mkdtemp()) / "db.sqlite")
        store.upsert_many(conn, "etablissements", [
            {"siret": "11111111100011", "siren": "123456789",
             "raison_sociale": "GARAGE DUPRE", "enseigne": None,
             "code_postal": "77000", "commune": "MELUN"}])
        row = conn.execute("SELECT * FROM etablissements").fetchone()
        self.assertGreaterEqual(resolve.score_page(
            "<p>Garage Dupré — 77000 Melun — SIREN 123 456 789</p>", row),
            config.MIN_SITE_CONFIDENCE)
        self.assertLess(resolve.score_page("<p>Ce domaine est à vendre</p>", row), 0)
        self.assertLess(resolve.score_page("<p>Boulangerie Martin, Lyon</p>", row),
                        config.MIN_SITE_CONFIDENCE)


class FausseReponse:
    def __init__(self, url, texte, code=200):
        self.url, self.text, self.status_code = url, texte, code
        self.headers = {"Content-Type": "text/html; charset=utf-8"}


class TestCrawlEtValidation(unittest.TestCase):
    def setUp(self):
        self.conn = store.connect(Path(tempfile.mkdtemp()) / "db.sqlite")
        self._get = net.get

    def tearDown(self):
        net.get = self._get
        crawl.net.get = self._get

    def test_crawl_suit_la_page_contact(self):
        pages = {
            "https://garage-dupre.fr": '<a href="/contact">Contact</a>',
            "https://garage-dupre.fr/contact": '<a href="mailto:contact@garage-dupre.fr">a</a>',
        }
        crawl.net.get = lambda url, sess=None, **kw: (
            FausseReponse(url, pages[url]) if url in pages else None)
        emails, tels, journal = crawl.crawler_site("https://garage-dupre.fr", None)
        self.assertEqual(set(emails), {"contact@garage-dupre.fr"})
        self.assertEqual(emails["contact@garage-dupre.fr"][1],
                         "https://garage-dupre.fr/contact")
        self.assertEqual(len(journal), 2)

    def test_crawl_respecte_le_plafond_de_pages(self):
        liens = "".join(f'<a href="/contact-{i}">contact {i}</a>' for i in range(20))
        crawl.net.get = lambda url, sess=None, **kw: FausseReponse(url, liens)
        _, _, journal = crawl.crawler_site("https://gros-site.fr", None)
        self.assertLessEqual(len(journal), config.MAX_PAGES_PER_SITE)

    def test_classement_des_emails(self):
        self.assertEqual(validate.classer("contact@garage-dupre.fr",
                                          "garage-dupre.fr")[0], "pro_role")
        self.assertEqual(validate.classer("jean.dupre@garage-dupre.fr")[0], "pro_nominatif")
        self.assertEqual(validate.classer("garagedupre@gmail.com")[0], "perso")
        role = validate.classer("contact@garage-dupre.fr", "garage-dupre.fr")[1]
        autre = validate.classer("contact@autre-domaine.fr", "garage-dupre.fr")[1]
        self.assertGreater(role, autre)  # même domaine que le site = plus fiable

    def test_opposition_purge_et_bloque(self):
        store.upsert_many(self.conn, "emails", [
            {"siret": "1" * 14, "email": "contact@garage-dupre.fr", "source": "test"},
            {"siret": "2" * 14, "email": "vente@stop.fr", "source": "test"}])
        validate.ajouter_opposition(self.conn, ["stop.fr"], "demande")
        restants = [r[0] for r in self.conn.execute("SELECT email FROM emails")]
        self.assertEqual(restants, ["contact@garage-dupre.fr"])
        self.assertIn("stop.fr", validate.charger_opposition(self.conn))


class TestExport(unittest.TestCase):
    def test_trois_fichiers_et_segmentation(self):
        tmp = Path(tempfile.mkdtemp())
        config.EXPORT_DIR = tmp
        conn = store.connect(tmp / "db.sqlite")
        store.upsert_many(conn, "etablissements", [
            {"siret": "1" * 14, "siren": "111111111", "raison_sociale": "AUTO PRO",
             "naf": "4511Z", "naf_libelle": "Commerce de voitures",
             "date_creation": "2025-01-05", "code_postal": "77000", "commune": "MELUN",
             "departement": "77", "personne_physique": 0},
            {"siret": "2" * 14, "siren": "222222222", "raison_sociale": "Jean DUPRE",
             "naf": "4511Z", "date_creation": "2025-06-01", "personne_physique": 1},
            {"siret": "3" * 14, "siren": "333333333", "raison_sociale": "SANS SITE",
             "naf": "4511Z", "date_creation": "2026-01-01"}])
        store.upsert_many(conn, "sites", [
            {"siret": "1" * 14, "url": "https://auto-pro.fr", "domaine": "auto-pro.fr",
             "source": "devine", "confiance": 4, "statut": "retenu"}])
        store.upsert_many(conn, "emails", [
            {"siret": "1" * 14, "email": "contact@auto-pro.fr", "source": "site:mailto",
             "url_source": "https://auto-pro.fr/contact", "type_email": "pro_role",
             "mx_ok": 1, "score": 85},
            {"siret": "2" * 14, "email": "jean.dupre@gmail.com", "source": "site:texte",
             "url_source": "https://x.fr", "type_email": "perso", "mx_ok": 1, "score": 10}])
        fichiers = export.run(conn, prefixe="test")
        self.assertEqual(fichiers["contacts_pro_test.csv"], 1)
        self.assertEqual(fichiers["contacts_perso_prudence_test.csv"], 1)
        self.assertEqual(fichiers["sans_email_test.csv"], 1)
        contenu = (tmp / "contacts_pro_test.csv").read_text(encoding="utf-8-sig")
        self.assertIn("contact@auto-pro.fr", contenu)
        self.assertNotIn("gmail", contenu)  # le perso ne fuite pas dans l'export pro
        self.assertIn("url_source", contenu.splitlines()[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestTelephones(unittest.TestCase):
    def test_extraction_et_normalisation(self):
        html = """<a href="tel:+33 1 23 45 67 89">appeler</a>
        <p>Tél 06.12.34.56.78 — SIRET 12345678900012 — 12 000 € — fax 04-91-22-33-44
        — bidon 01 11 11 11 11</p>"""
        tels = extract.extraire_telephones(html)
        self.assertEqual(set(tels), {"+33123456789", "+33612345678", "+33491223344"})
        self.assertEqual(tels["+33123456789"], "tel")

    def test_formats_acceptes_et_rejetes(self):
        self.assertEqual(extract.normaliser_tel("0033 6 12 34 56 78"), "+33612345678")
        self.assertEqual(extract.normaliser_tel("+33 (0)1 64 12 34 56"), "+33164123456")
        for mauvais in ("00 12 34", "0012345678", "12345678900012", "0111111111"):
            self.assertIsNone(extract.normaliser_tel(mauvais), mauvais)


class TestIndexDomaines(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.conn = store.connect(self.tmp / "db.sqlite")

    def test_normalisation_des_ecritures(self):
        self.assertEqual(domaines.domaine_enregistrable("fr.exemple.www"), "exemple.fr")
        self.assertEqual(domaines.domaine_enregistrable("www.Garage-Dupre.FR"),
                         "garage-dupre.fr")
        self.assertEqual(domaines.domaine_enregistrable("https://auto.fr/contact"), "auto.fr")
        self.assertEqual(domaines.domaine_enregistrable("fr.gouv.insee"), "insee.gouv.fr")
        self.assertIsNone(domaines.domaine_enregistrable("pas un domaine"))

    def test_lecture_format_afnic_csv(self):
        fichier = self.tmp / "afnic.csv"
        fichier.write_text(
            "Nom de domaine;Date de création;Titulaire\n"
            "garage-dupre.fr;2024-03-01;DUPRE\n"
            "autoprestige77.fr;2025-01-01;AP77\n"
            "exemple.com;2020-01-01;HORS TLD\n", encoding="utf-8")
        self.assertEqual(sorted(domaines.iter_domaines(fichier)),
                         ["autoprestige77.fr", "garage-dupre.fr"])

    def test_lecture_format_common_crawl(self):
        fichier = self.tmp / "host-vertices.txt"
        fichier.write_text("1\tfr.garage-dupre.www\n2\tfr.autoprestige77\n"
                           "3\tcom.exemple.www\n", encoding="utf-8")
        self.assertEqual(sorted(domaines.iter_domaines(fichier)),
                         ["autoprestige77.fr", "garage-dupre.fr"])

    def test_lecture_texte_brut(self):
        fichier = self.tmp / "liste.txt"
        fichier.write_text("garage-dupre.fr\nautoprestige77.fr\n", encoding="utf-8")
        self.assertEqual(sorted(domaines.iter_domaines(fichier)),
                         ["autoprestige77.fr", "garage-dupre.fr"])

    def _index(self):
        fichier = self.tmp / "liste.txt"
        fichier.write_text("\n".join([
            "garagedupre.fr",            # concaténé : doit matcher « GARAGE DUPRE »
            "dupre-automobiles.fr",      # token distinctif + mot métier
            "autoprestige77.fr",
            "boulangerie-martin.fr",     # bruit
            "auto.fr",                   # trop générique
        ]) + "\n", encoding="utf-8")
        domaines.construire(self.conn, fichier)

    def test_candidats_exacts_et_flous(self):
        self._index()
        self.assertTrue(domaines.index_disponible(self.conn))
        trouves = dict(domaines.candidats(self.conn, ["SARL GARAGE DUPRE"], "Melun"))
        # correspondance exacte insensible aux tirets, indice maximal
        self.assertEqual(trouves.get("garagedupre.fr"), 6)
        # correspondance floue sur le token distinctif « dupre »
        self.assertIn("dupre-automobiles.fr", trouves)
        self.assertNotIn("boulangerie-martin.fr", trouves)

    def test_candidats_pour_nom_chiffre(self):
        self._index()
        trouves = dict(domaines.candidats(self.conn, ["AUTO PRESTIGE 77"]))
        self.assertIn("autoprestige77.fr", trouves)

    def test_nom_sans_correspondance_ne_renvoie_rien(self):
        self._index()
        self.assertEqual(domaines.candidats(self.conn, ["JEAN DUPONT"]), [])


class TestAnnuaireGenerique(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.conn = store.connect(self.tmp / "db.sqlite")
        self.cfg = dict(annuaire.GABARIT, nom="test-annuaire",
                        selecteurs={"nom": "h1", "commune": ".ville",
                                    "code_postal": ".cp", "telephone": "a[href^='tel:']",
                                    "site_web": "a.site-web",
                                    "email": "a[href^='mailto:']"})

    def test_pagination(self):
        cfg = dict(self.cfg, pages=["https://x.fr/a?p={page}"],
                   pagination={"debut": 2, "fin": 6, "pas": 2})
        self.assertEqual(annuaire.urls_de_liste(cfg),
                         ["https://x.fr/a?p=2", "https://x.fr/a?p=4", "https://x.fr/a?p=6"])

    def test_extraction_par_selecteurs(self):
        html = """<div><h1>Garage Dupré</h1><span class="ville">Melun</span>
        <span class="cp">77000</span><a class="site-web" href="https://garage-dupre.fr">s</a>
        <a href="tel:01 64 12 34 56">t</a><a href="mailto:contact@garage-dupre.fr">m</a></div>"""
        fiche = annuaire.extraire_fiche(html, "https://annuaire.fr/f/1", self.cfg)
        self.assertEqual(fiche["nom"], "Garage Dupré")
        self.assertEqual(fiche["commune"], "Melun")
        self.assertEqual(fiche["code_postal"], "77000")
        self.assertEqual(fiche["telephone"], "+33164123456")
        self.assertEqual(fiche["email"], "contact@garage-dupre.fr")
        self.assertEqual(fiche["site_web"], "https://garage-dupre.fr")

    def test_secours_extraction_generique_sans_selecteur(self):
        cfg = dict(self.cfg, selecteurs={"nom": "h1"})
        html = "<h1>Garage Dupré</h1><p>contact@garage-dupre.fr — 01 64 12 34 56</p>"
        fiche = annuaire.extraire_fiche(html, "https://annuaire.fr/f/2", cfg)
        self.assertEqual(fiche["email"], "contact@garage-dupre.fr")
        self.assertEqual(fiche["telephone"], "+33164123456")

    def test_fiche_sans_contact_ignoree(self):
        self.assertIsNone(annuaire.extraire_fiche(
            "<h1>Garage Sans Contact</h1>", "https://annuaire.fr/f/3", self.cfg))

    def test_appariement_alimente_sites_emails_telephones(self):
        store.upsert_many(self.conn, "etablissements", [
            {"siret": "1" * 14, "siren": "111111111", "raison_sociale": "GARAGE DUPRE",
             "code_postal": "77000", "commune": "MELUN"}])
        store.upsert_many(self.conn, "annuaire_fiches", [{
            "cle": "test|garage dupre|77000", "source": "test-annuaire",
            "nom": "Garage Dupré", "commune": "Melun", "code_postal": "77000",
            "telephone": "+33164123456", "site_web": "https://garage-dupre.fr",
            "email": "contact@garage-dupre.fr", "url_source": "https://annuaire.fr/f/1"}])
        self.assertEqual(annuaire.apparier(self.conn), 1)
        self.assertEqual(store.count(self.conn, "emails"), 1)
        self.assertEqual(store.count(self.conn, "telephones"), 1)
        site = self.conn.execute("SELECT * FROM sites").fetchone()
        self.assertEqual(site["source"], "annuaire:test-annuaire:nom_cp")

    def test_config_incomplete_refusee(self):
        chemin = self.tmp / "cfg.json"
        chemin.write_text('{"nom": "x"}', encoding="utf-8")
        with self.assertRaises(SystemExit):
            annuaire.charger_config(chemin)
