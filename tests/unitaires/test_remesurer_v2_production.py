"""Tests du script de remesure du prototype v2.0, fiche « production et stocks » (#34).

Les parties qui ne lancent pas le prototype (arguments, empreintes,
agrégation, verdicts, JSON) sont testées sur des données fabriquées. Deux
tests exécutent le pilote : l'un avec l'interpréteur du projet, sans scipy,
pour vérifier qu'un échec est consigné ; l'autre, de bout en bout, sur un an
et la seule branche nominale, dans l'environnement `uv` du pilote, hors
ligne (`UV_OFFLINE=1`) : la batterie ne dépend pas de PyPI. Une sonde
préalable, qui n'importe que numpy et scipy, saute le test si cet
environnement n'est pas en cache ; environnement présent, un échec du
prototype fait échouer le test.
"""

import ast
import json
import shutil
import subprocess
import sys

import pytest

SEMAINES = 52


def semaine(valeur=1.0, excess=0.0, d_sup_s=0.0):
    """Relevé hebdomadaire fabriqué : même valeur dans les quatre secteurs."""
    releve = {g: [valeur] * 4 for g in ("sinv_sur_q", "sinv_sur_cible", "rationnement_relatif", "y_sur_yhat")}
    releve["part_excess_positif"] = [excess] * 4
    releve["part_d_sup_s"] = [d_sup_s] * 4
    return releve


def annees_constantes(remesure, n, **kw):
    return remesure.agreger([semaine(**kw) for _ in range(n * SEMAINES)])


def branche(annees):
    return {"statut": "remesuré", "annees": annees}


# --- Arguments -------------------------------------------------------------

def test_arguments_par_defaut(remesure, tmp_path):
    args = remesure.analyser_arguments(["--sortie", str(tmp_path / "s.json")])
    assert (args.annees, args.graine) == (60, 0)
    assert args.branches == ["nominal", "mu_x0.5", "mu_x2", "lam_x0.5", "lam_x2"]
    assert args.archive == remesure.ARCHIVE_DEFAUT
    assert args.delai == 120.0 + 60.0 * 60


def test_branches_en_ordre_canonique_sans_doublon(remesure):
    args = remesure.analyser_arguments(["--sortie", "s.json", "--branches", "lam_x2", "nominal", "lam_x2"])
    assert args.branches == ["nominal", "lam_x2"]


@pytest.mark.parametrize(
    "arguments",
    [
        ["--sortie", "s.json", "--branches", "mu_x3"],
        ["--sortie", "s.json", "--annees", "0"],
        ["--sortie", "s.json", "--delai", "0"],
        [],
    ],
)
def test_arguments_refuses(remesure, arguments):
    with pytest.raises(SystemExit):
        remesure.analyser_arguments(arguments)


def test_surcharges_des_branches(remesure):
    # Une seule surcharge par branche, facteurs 0,5 et 2 sur les deux vitesses.
    assert remesure.BRANCHES["nominal"] == {}
    assert remesure.BRANCHES["mu_x0.5"] == {"mu_ema": 0.5}
    assert remesure.BRANCHES["lam_x2"] == {"lam_inv_2": 2.0}


# --- Empreintes -------------------------------------------------------------

@pytest.fixture
def copie(remesure, tmp_path):
    destination = tmp_path / "prototype"
    shutil.copytree(remesure.ARCHIVE_DEFAUT, destination, ignore=shutil.ignore_patterns("__pycache__"))
    return destination


def test_empreintes_conformes(remesure, copie):
    prefixe = remesure.prefixe_du_manifeste(remesure.ARCHIVE_DEFAUT)
    assert prefixe == "archive/v2.0/prototype"
    sha = remesure.verifier_empreintes(copie, prefixe)
    assert "model.py" in sha and len(sha) == len(remesure.empreintes_attendues(remesure.MANIFESTE, prefixe))


def test_cache_de_compilation_ignore(remesure, copie):
    (copie / "__pycache__").mkdir()
    (copie / "__pycache__" / "model.cpython-312.pyc").write_bytes(b"\x00")
    remesure.verifier_empreintes(copie, "archive/v2.0/prototype")


@pytest.mark.parametrize("ecart", ["modifie", "ajoute", "manquant"])
def test_empreintes_non_conformes(remesure, copie, ecart):
    if ecart == "modifie":
        with (copie / "model.py").open("a", encoding="utf-8") as f:
            f.write("\n")
    elif ecart == "ajoute":
        (copie / "intrus.py").write_text("", encoding="utf-8")
    else:
        (copie / "reference.py").unlink()
    with pytest.raises(remesure.EmpreintesNonConformes):
        remesure.verifier_empreintes(copie, "archive/v2.0/prototype")


def test_prefixe_absent_du_manifeste(remesure, copie):
    with pytest.raises(remesure.EmpreintesNonConformes):
        remesure.verifier_empreintes(copie, "archive/v9.9/prototype")


def test_main_refuse_un_dossier_hors_manifeste(remesure, tmp_path, capsys):
    # Un dossier du dépôt sans empreinte au manifeste : rien n'est exécuté.
    sortie = tmp_path / "s.json"
    code = remesure.main(["--sortie", str(sortie), "--archive", str(remesure.RACINE / "outils")])
    assert code == 2 and not sortie.exists()
    assert "empreintes non conformes" in capsys.readouterr().err


@pytest.mark.parametrize("cas", ["inexistant", "hors_depot"])
def test_main_refuse_un_prototype_introuvable(remesure, tmp_path, capsys, cas):
    dossier = tmp_path / "absent" if cas == "inexistant" else tmp_path
    sortie = tmp_path / "s.json"
    code = remesure.main(["--sortie", str(sortie), "--archive", str(dossier)])
    erreur = capsys.readouterr().err
    assert code == 2 and not sortie.exists()
    assert "prototype introuvable" in erreur and "Traceback" not in erreur


# --- Agrégation --------------------------------------------------------------

def test_agregation_annuelle(remesure):
    semaines = [semaine(2.0, excess=1.0)] * 13 + [semaine(4.0)] * 39 + [semaine(1.0)] * SEMAINES
    annees = remesure.agreger(semaines)
    assert [a["annee"] for a in annees] == [1, 2]
    premiere = annees[0]["secteurs"]["equipement"]
    assert premiere["sinv_sur_q"] == pytest.approx(3.5)
    assert premiere["part_excess_positif"] == pytest.approx(0.25)
    assert annees[1]["secteurs"]["alimentation"]["sinv_sur_q"] == 1.0


def test_semaines_exclues_et_valeurs_absentes(remesure):
    trou = semaine(2.0)
    trou["sinv_sur_q"] = [None, 2.0, 2.0, 2.0]
    semaines = [None] * 2 + [trou] + [semaine(2.0)] * (SEMAINES - 3)
    trou["y_sur_yhat"] = [float("nan"), 2.0, 2.0, 2.0]
    annee = remesure.agreger(semaines)[0]
    assert (annee["semaines_valides"], annee["semaines_exclues"]) == (SEMAINES - 2, 2)
    assert annee["secteurs"]["alimentation"]["sinv_sur_q"] == 2.0
    assert annee["secteurs"]["alimentation"]["y_sur_yhat"] == 2.0
    # Valeurs retenues et omises, par grandeur et secteur.
    effectifs = annee["effectifs"]
    assert effectifs["alimentation"]["sinv_sur_q"] == {"retenues": SEMAINES - 3, "omises": 1}
    assert effectifs["alimentation"]["y_sur_yhat"] == {"retenues": SEMAINES - 3, "omises": 1}
    assert effectifs["energie"]["sinv_sur_q"] == {"retenues": SEMAINES - 2, "omises": 0}
    vide = remesure.agreger([None] * SEMAINES)[0]
    assert vide["secteurs"]["energie"]["y_sur_yhat"] is None


def test_agregation_refuse_une_annee_incomplete(remesure):
    with pytest.raises(ValueError):
        remesure.agreger([semaine()] * (SEMAINES + 1))


def test_moyenne_fenetre(remesure):
    annees = remesure.agreger([semaine(float(k // SEMAINES)) for k in range(4 * SEMAINES)])
    assert remesure.moyenne_fenetre(annees, "sinv_sur_q", "energie", (2, 4)) == pytest.approx(2.0)
    assert remesure.moyenne_fenetre(annees, "sinv_sur_q", "energie", (3, 5)) is None


# --- Verdicts ---------------------------------------------------------------

def test_criteres_figes(remesure):
    # Critères écrits avant l'essai (S1) : ils ne se déplacent pas.
    assert remesure.FENETRE == (31, 60)
    assert remesure.SECTEURS_CRITERES == ("consommation", "equipement")
    assert remesure.SEUIL_SINV_SUR_CIBLE == 0.99
    assert remesure.SEUIL_PART_EXCESS == 0.05
    assert remesure.SEUIL_ECART_RELATIF == 1e-6


@pytest.mark.parametrize(
    ("ratio", "part", "attendu"),
    [
        (0.989, 0.0, "satisfait"),
        (0.991, 0.0, "non satisfait"),
        (0.93, 0.049, "satisfait"),
        (0.93, 0.051, "non satisfait"),
    ],
)
def test_verdict_i_encadre_les_seuils(remesure, ratio, part, attendu):
    branches = {"nominal": branche(annees_constantes(remesure, 2, valeur=ratio, excess=part))}
    assert remesure.verdict_i(branches, (1, 2))["verdict"] == attendu


@pytest.mark.parametrize(("ecart", "attendu"), [(1.1e-6, "satisfait"), (0.9e-6, "non satisfait")])
def test_verdict_ii_encadre_le_seuil(remesure, ecart, attendu):
    reference = annees_constantes(remesure, 1, valeur=4.0)
    decale = annees_constantes(remesure, 1, valeur=4.0 * (1 + ecart))
    branches = {"mu_x0.5": branche(reference), "mu_x2": branche(decale),
                "lam_x0.5": branche(reference), "lam_x2": branche(decale)}
    resultat = remesure.verdict_ii(branches, (1, 1))
    assert resultat["vitesses"]["mu_ema"]["verdict"] == attendu
    assert resultat["vitesses"]["lam_inv_2"]["verdict"] == attendu
    assert resultat["verdict"] == attendu

def test_verdict_i_satisfait_et_non_satisfait(remesure):
    fenetre = (2, 3)
    actif = {"nominal": branche(annees_constantes(remesure, 3, valeur=0.93, excess=0.0))}
    assert remesure.verdict_i(actif, fenetre)["verdict"] == "satisfait"
    au_dessus = {"nominal": branche(annees_constantes(remesure, 3, valeur=0.995))}
    assert remesure.verdict_i(au_dessus, fenetre)["verdict"] == "non satisfait"
    borne_jouee = {"nominal": branche(annees_constantes(remesure, 3, valeur=0.93, excess=1.0))}
    assert remesure.verdict_i(borne_jouee, fenetre)["verdict"] == "non satisfait"


def test_verdict_i_non_evaluable(remesure):
    courte = {"nominal": branche(annees_constantes(remesure, 1, valeur=0.93))}
    assert remesure.verdict_i(courte)["verdict"] == "non évaluable"
    echec = {"nominal": {"statut": "non remesurable", "exception": "x"}}
    assert remesure.verdict_i(echec, (1, 1))["verdict"] == "non évaluable"
    assert remesure.verdict_i({}, (1, 1))["verdict"] == "non évaluable"


def test_verdict_ii(remesure):
    fenetre = (1, 2)
    branches = {
        "mu_x0.5": branche(annees_constantes(remesure, 2, valeur=4.0)),
        "mu_x2": branche(annees_constantes(remesure, 2, valeur=4.0 * (1 + 1e-3))),
        "lam_x0.5": branche(annees_constantes(remesure, 2, valeur=4.0)),
        "lam_x2": branche(annees_constantes(remesure, 2, valeur=4.0)),
    }
    resultat = remesure.verdict_ii(branches, fenetre)
    assert resultat["vitesses"]["mu_ema"]["verdict"] == "satisfait"
    assert resultat["vitesses"]["mu_ema"]["valeurs"]["equipement"]["ecart_relatif"] == pytest.approx(1e-3)
    assert resultat["vitesses"]["lam_inv_2"]["verdict"] == "non satisfait"
    assert resultat["verdict"] == "non satisfait"
    del branches["lam_x2"]
    resultat = remesure.verdict_ii(branches, fenetre)
    assert resultat["vitesses"]["lam_inv_2"]["verdict"] == "non évaluable"
    assert resultat["verdict"] == "non évaluable"


def test_semaines_exclues_publiees_avec_chaque_verdict(remesure):
    # Deux semaines d'effondrement en année 2 (dans la fenêtre (2, 3)), une en
    # année 1 (hors fenêtre) : le verdict se calcule quand même.
    semaines = [semaine(0.93) for _ in range(3 * SEMAINES)]
    semaines[5] = semaines[SEMAINES + 1] = semaines[SEMAINES + 2] = None
    avec = branche(remesure.agreger(semaines))
    sans = branche(annees_constantes(remesure, 3, valeur=0.93))
    resultat = remesure.verdict_i({"nominal": avec}, (2, 3))
    assert resultat["verdict"] == "satisfait"
    assert (resultat["semaines_exclues"], resultat["effondrement_dans_fenetre"]) == (2, True)
    resultat = remesure.verdict_i({"nominal": sans}, (2, 3))
    assert (resultat["semaines_exclues"], resultat["effondrement_dans_fenetre"]) == (0, False)
    branches = {"mu_x0.5": sans, "mu_x2": avec, "lam_x0.5": sans, "lam_x2": sans}
    resultat = remesure.verdict_ii(branches, (2, 3))
    assert resultat["vitesses"]["mu_ema"]["semaines_exclues"] == {"mu_x0.5": 0, "mu_x2": 2}
    assert resultat["vitesses"]["mu_ema"]["effondrement_dans_fenetre"] is True
    assert resultat["vitesses"]["lam_inv_2"]["effondrement_dans_fenetre"] is False
    assert resultat["effondrement_dans_fenetre"] is True
    assert resultat["verdict"] == "non satisfait"  # écart nul : calculé malgré l'effondrement
    echec = remesure.verdict_i({"nominal": {"statut": "non remesurable", "exception": "x"}}, (2, 3))
    assert (echec["semaines_exclues"], echec["effondrement_dans_fenetre"]) == (None, False)


def test_annee_sans_semaine_valide_non_evaluable(remesure):
    semaines = [semaine(0.93)] * SEMAINES + [None] * SEMAINES
    resultat = remesure.verdict_i({"nominal": branche(remesure.agreger(semaines))}, (1, 2))
    assert resultat["verdict"] == "non évaluable"
    assert resultat["semaines_exclues"] == SEMAINES


def test_ecart_relatif(remesure):
    assert remesure.ecart_relatif(4.0, 2.0) == 0.5
    # r = Sinv/Q non négatif : deux zéros, écart nul ; zéro seul, indéfini.
    assert remesure.ecart_relatif(0.0, 0.0) == 0.0
    assert remesure.ecart_relatif(0.0, 1.0) is None


def _branches_vitesses(remesure, moitie, double):
    reference = branche(annees_constantes(remesure, 1, valeur=moitie))
    autre = branche(annees_constantes(remesure, 1, valeur=double))
    return {"mu_x0.5": reference, "mu_x2": autre, "lam_x0.5": reference, "lam_x2": autre}


def test_verdict_ii_deux_zeros_non_satisfait(remesure):
    # r(× 0,5) = r(× 2) = 0 : écart nul, pas un faux « satisfait ».
    resultat = remesure.verdict_ii(_branches_vitesses(remesure, 0.0, 0.0), (1, 1))
    assert resultat["vitesses"]["mu_ema"]["valeurs"]["equipement"]["ecart_relatif"] == 0.0
    assert resultat["vitesses"]["mu_ema"]["verdict"] == "non satisfait"
    assert resultat["verdict"] == "non satisfait"


def test_verdict_ii_zero_seul_non_evaluable(remesure):
    # r(× 0,5) = 0 et r(× 2) > 0 : écart indéfini, publié `null`.
    resultat = remesure.verdict_ii(_branches_vitesses(remesure, 0.0, 3.0), (1, 1))
    assert resultat["vitesses"]["mu_ema"]["valeurs"]["equipement"]["ecart_relatif"] is None
    assert resultat["vitesses"]["mu_ema"]["verdict"] == "non évaluable"
    assert resultat["verdict"] == "non évaluable"


# --- Rédaction du JSON ------------------------------------------------------

def test_json_strict(remesure, tmp_path):
    branches = {"nominal": branche(remesure.agreger([None] * SEMAINES))}
    document = remesure.rediger({"mention": "m", "valeur": float("inf")}, branches, (1, 1))
    chemin = tmp_path / "sous" / "r.json"
    remesure.ecrire(document, chemin)
    texte = chemin.read_text(encoding="utf-8")
    relu = json.loads(texte)
    assert "Infinity" not in texte and "NaN" not in texte
    assert relu["contexte"]["valeur"] is None
    assert relu["criteres"]["i"]["verdict"] == "non évaluable"
    assert set(relu["criteres"]) == {"i", "ii"}


# --- Pilote -----------------------------------------------------------------

def test_pilote_syntaxe_et_sans_reference_a_l_archive(remesure):
    ast.parse(remesure.PILOTE)
    assert "archive" not in remesure.PILOTE
    # Les fonctions de relevé sont celles du module, recopiées.
    assert "def rapport(" in remesure.PILOTE and "def indicatrice(" in remesure.PILOTE


def test_indicatrice_omet_un_operande_non_fini(remesure):
    nan, inf = float("nan"), float("inf")
    assert remesure.indicatrice([2.0, 1.0, nan, 1.0, inf], [1.0, 1.0, 0.0, nan, 0.0]) == [
        1.0, 0.0, None, None, None,
    ]
    # Une semaine NaN est omise et comptée, pas comptée comme « non ».
    releve = semaine(1.0)
    releve["part_excess_positif"] = remesure.indicatrice([nan, 2.0, 2.0, 2.0], [0.0, 1.0, 1.0, 1.0])
    annee = remesure.agreger([releve] + [semaine(1.0, excess=1.0)] * (SEMAINES - 1))[0]
    assert annee["secteurs"]["alimentation"]["part_excess_positif"] == 1.0
    assert annee["effectifs"]["alimentation"]["part_excess_positif"] == {"retenues": SEMAINES - 1, "omises": 1}


def test_rapport_omet_denominateur_nul_et_non_fini(remesure):
    nan = float("nan")
    assert remesure.rapport([4.0, 1.0, 1.0, nan, 1.0], [2.0, 0.0, -1.0, 1.0, nan]) == [
        2.0, None, None, None, None,
    ]


def test_rapport_omet_denominateur_infini(remesure):
    inf = float("inf")
    assert remesure.rapport([1.0, 1.0, 1.0], [inf, -inf, 2.0]) == [None, None, 0.5]
    # Omis de la moyenne et compté, pas retenu comme 0.
    releve = semaine(1.0)
    releve["sinv_sur_q"] = remesure.rapport([1.0] * 4, [inf, 1.0, 1.0, 1.0])
    annee = remesure.agreger([releve] + [semaine(2.0)] * (SEMAINES - 1))[0]
    assert annee["secteurs"]["alimentation"]["sinv_sur_q"] == 2.0
    assert annee["effectifs"]["alimentation"]["sinv_sur_q"] == {"retenues": SEMAINES - 1, "omises": 1}


def test_echec_du_prototype_consigne(remesure, tmp_path):
    # L'interpréteur du projet n'a pas scipy : le prototype ne s'importe pas,
    # la branche est déclarée non remesurable, l'exception est consignée.
    pytest.importorskip("numpy")
    try:
        import scipy  # noqa: F401
        pytest.skip("scipy présent : l'échec n'est pas reproductible ainsi")
    except ImportError:
        pass
    args = remesure.analyser_arguments(["--sortie", str(tmp_path / "s.json"), "--annees", "1", "--branches", "nominal"])
    document = remesure.remesurer(args, commande=[sys.executable])
    nominal = document["branches"]["nominal"]
    assert nominal["statut"] == "non remesurable"
    assert "scipy" in nominal["exception"]
    assert document["contexte"]["mention"].endswith("profil par défaut, non D1")
    assert document["criteres"]["i"]["verdict"] == "non évaluable"


def sonder_environnement_du_pilote(remesure) -> str | None:
    """Motif de saut si l'environnement du pilote n'est pas disponible hors
    ligne ; `None` s'il l'est. La sonde n'importe que numpy et scipy."""
    if shutil.which("uv") is None:
        return "uv absent : environnement du pilote indisponible"
    sonde = subprocess.run(
        [*remesure.commande_pilote(), "-c", "import numpy, scipy"],
        capture_output=True, text=True, timeout=120,
    )
    if sonde.returncode != 0:
        return (
            "environnement du pilote (numpy, scipy==" + remesure.VERSION_SCIPY
            + ") absent du cache uv, hors ligne : " + sonde.stderr.strip()[-300:]
        )
    return None


def test_bout_en_bout_un_an(remesure, tmp_path, monkeypatch):
    # Hors ligne : la sonde et le pilote n'atteignent jamais PyPI.
    monkeypatch.setenv("UV_OFFLINE", "1")
    motif = sonder_environnement_du_pilote(remesure)
    if motif:
        pytest.skip(motif)
    sortie = tmp_path / "r.json"
    code = remesure.main(["--sortie", str(sortie), "--annees", "1", "--branches", "nominal"])
    document = json.loads(sortie.read_text(encoding="utf-8"))
    assert code == 0, document["branches"]
    annee = document["branches"]["nominal"]["annees"][0]
    assert annee["semaines_valides"] == SEMAINES
    for secteur in remesure.SECTEURS:
        valeurs = annee["secteurs"][secteur]
        # Propriétés attendues : stock de l'ordre de la cible de 4 semaines,
        # parts dans [0, 1].
        assert 1.0 < valeurs["sinv_sur_q"] < 10.0
        assert 0.0 <= valeurs["part_excess_positif"] <= 1.0
        assert 0.0 <= valeurs["part_d_sup_s"] <= 1.0
    assert document["contexte"]["versions"]["pilote"]["scipy"] == remesure.VERSION_SCIPY
    assert document["criteres"]["i"]["verdict"] == "non évaluable"
