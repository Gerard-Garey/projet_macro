"""Tests du banc d'empreintes `outils/empreintes_des_bancs.py` (#144, P173).

Bancs courts (`NB_PAS_COURT` pas) : le critère « identiques au bit » sur 720 pas se mesure par
le script lui-même, pas ici. Vérifiés : encodage sans ambiguïté, déterminisme (deux appels,
même empreinte), sensibilité à un écart d'un ulp (état, montant de clôture, variable du pas ;
grandeurs d'ouverture hors empreinte), refus bruyant d'un bloc manquant (en appel direct et sur
une racine extraite sans un module de bloc), arrêt du moteur consigné comme écart (code 1),
écart signalé par `--comparer` (code 1) ; réserves du rang 1a (P185) : sous-classe d'un bloc
réel refusée (code 2), bloc 9 composé admis dans les seuls bancs D et BF (m-a), écart des
seules grandeurs d'ouverture en code 3, ajout comme retrait (m-c ; P186, P189) ; variables du pas
exclues (`--exclure-variables`, P187) : nom inconnu refusé, seule `variables` changée, noms
consignés dans le document, règles de comparabilité à une référence (référence avec
exclusion refusée : M1 de l'audit), banc arrêté (m1).
"""

import dataclasses
import importlib.util
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[2]
NB_PAS_COURT = 3


@pytest.fixture(scope="module")
def emp():
    chemin = RACINE / "outils" / "empreintes_des_bancs.py"
    spec = importlib.util.spec_from_file_location("empreintes_des_bancs", chemin)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def racine(emp):
    return emp.Racine(RACINE)


def test_encodage_sans_ambiguite(emp):
    assert emp.encoder(0.0) != emp.encoder(-0.0)
    assert emp.encoder(True) != emp.encoder(1) != emp.encoder(1.0)
    assert emp.encoder(("ab", "c")) != emp.encoder(("a", "bc"))
    assert emp.encoder(2**64 + 1) != emp.encoder(1)
    with pytest.raises(TypeError):
        emp.encoder([1.0])
    with pytest.raises(TypeError):
        emp.encoder(None)


def test_deux_appels_meme_empreinte(emp, racine):
    un = emp.empreintes(racine, emp.BANCS, NB_PAS_COURT)
    deux = emp.empreintes(racine, emp.BANCS, NB_PAS_COURT)
    assert un["globale"] == deux["globale"]
    assert emp.comparer(un, deux) == []
    assert un["arrets"] == []
    # 24 empreintes distinctes : chaque banc et chaque π* est bien un essai différent.
    toutes = {v["empreinte"] for par_pi in un["bancs"].values() for v in par_pi.values()}
    assert len(toutes) == len(emp.BANCS) * len(racine.socle.POINTS_PI) == 24


def _ulp(x):
    return math.nextafter(x, math.inf)


def _hacher(emp, racine, evenements, initial=None):
    h = emp.Hacheur(racine.champs, racine.cloture, racine.fin_de_pas)
    if initial is not None:
        h.initial(initial)
    for e in evenements:
        h.relever(e)
    return h


def test_un_ulp_de_l_etat_change_l_empreinte(emp, racine):
    """Le hacheur voit un écart d'un ulp sur une seule valeur de l'état initial."""
    _, initial, _ = racine.construire(emp.SOCLE_COMPLET, 0.02)
    autre = dataclasses.replace(initial, D_H=_ulp(initial.D_H))
    un, deux = (_hacher(emp, racine, (), e) for e in (initial, autre))
    assert un.complet.hexdigest() != deux.complet.hexdigest()
    assert un.parties["etats"].hexdigest() != deux.parties["etats"].hexdigest()


def test_un_ulp_d_un_montant_de_cloture_change_l_empreinte(emp, racine):
    """m-5 : clôture fabriquée, un ulp sur un terme d'une ligne."""
    def cloture(x):
        return racine.cloture(t=0, phase="2", rapports=(),
                              montants=(("1", (("C", 2.0), ("autre", x))),))
    un, deux = (_hacher(emp, racine, (cloture(x),)) for x in (1.0, _ulp(1.0)))
    assert un.complet.hexdigest() != deux.complet.hexdigest()
    assert un.parties["montants"].hexdigest() != deux.parties["montants"].hexdigest()
    assert un.parties["etats"].hexdigest() == deux.parties["etats"].hexdigest()


def test_un_ulp_d_une_variable_du_pas_change_l_empreinte(emp, racine):
    """m-5 : fin de pas fabriquée, un ulp sur une variable du pas ; les grandeurs d'ouverture
    ont leur sous-empreinte mais n'entrent pas dans l'empreinte du banc (m-3) ; l'ordre
    d'inscription des variables ne compte pas (tri par nom)."""
    _, initial, _ = racine.construire(emp.SOCLE_COMPLET, 0.02)

    def fin(x, g=1.0, ordre=1):
        variables = (("a", x), ("b", 3.0))[::ordre]
        return racine.fin_de_pas(t=0, etat=initial, variables_du_pas=variables,
                                 grandeurs_ouverture=(("g", g),))
    base = _hacher(emp, racine, (fin(1.0),))
    variable = _hacher(emp, racine, (fin(_ulp(1.0)),))
    grandeur = _hacher(emp, racine, (fin(1.0, g=_ulp(1.0)),))
    inverse = _hacher(emp, racine, (fin(1.0, ordre=-1),))
    assert base.complet.hexdigest() != variable.complet.hexdigest()
    assert base.parties["variables"].hexdigest() != variable.parties["variables"].hexdigest()
    assert base.complet.hexdigest() == grandeur.complet.hexdigest()
    assert base.parties["grandeurs"].hexdigest() != grandeur.parties["grandeurs"].hexdigest()
    assert base.complet.hexdigest() == inverse.complet.hexdigest()


def test_arret_du_moteur_consigne_comme_ecart(emp, racine, monkeypatch, capsys):
    """m-1 : une exception du moteur pendant un banc est un écart (code 1), avec banc, π*,
    pas atteint et type d'erreur ; jamais une empreinte."""
    executer = racine.ordo.executer_pas

    class DefautFabrique(Exception):
        pass

    def executer_puis_arreter(etat, *args, **kwargs):
        if etat.t == 1:
            raise DefautFabrique("arrêt fabriqué")
        return executer(etat, *args, **kwargs)
    monkeypatch.setattr(racine.ordo, "executer_pas", executer_puis_arreter)
    v = emp.empreinte_du_banc(racine, emp.SANS_X4, 0.02, NB_PAS_COURT)
    assert v == {"arret": {"type": "DefautFabrique", "message": "arrêt fabriqué", "pas": 1}}
    assert emp.main(["--bancs", "J3-d1 sans X4", "--pas", "3"]) == 1
    err = capsys.readouterr().err
    assert "J3-d1 sans X4, π* = 0.02 : arrêt au pas 1, DefautFabrique" in err


def test_bloc_manquant_refuse_en_appel_direct(emp, racine):
    """`blocs_reels()` saute un module absent : le banc qui en résulte est refusé."""
    s = racine.socle
    sentier = s.sentier(0.02)
    reels = tuple(b for b in s.blocs_reels() if b.declaration.radical != "investissement")
    blocs = s.blocs(sentier, reels=reels)  # bloc d'essai 6 à la place du bloc réel
    with pytest.raises(emp.BancNonConforme, match="manquants : \\['investissement'\\]"):
        emp.verifier_blocs(emp.SANS_X4, blocs, s.RADICAUX)
    with pytest.raises(emp.BancNonConforme, match="radicaux"):
        emp.verifier_blocs(emp.SOCLE_COMPLET, s.blocs_du_socle_complet()[:-1], s.RADICAUX)


@pytest.mark.parametrize("module", ["investissement", "production"])
def test_racine_sans_un_module_de_bloc_refusee(tmp_path, module):
    """Version « avant » extraite sans un module de bloc : refus bruyant, code 2 (m-1 :
    `ImportError` compris)."""
    for dossier in ("src", "tests", "outils"):
        shutil.copytree(RACINE / dossier, tmp_path / dossier,
                        ignore=shutil.ignore_patterns("__pycache__"))
    (tmp_path / "src" / "nations" / "blocs" / f"{module}.py").unlink()
    sortie = subprocess.run(
        [sys.executable, str(RACINE / "outils" / "empreintes_des_bancs.py"), "--racine",
         str(tmp_path), "--bancs", "J3-d1 sans X4", "--pas", "1"],
        capture_output=True, text=True, cwd=tmp_path, check=False)
    assert sortie.returncode == 2, sortie.stderr
    assert module in sortie.stderr and "refus" in sortie.stderr


def test_comparer_signale_un_ecart(emp, tmp_path, capsys):
    reference = tmp_path / "reference.json"
    assert emp.main(["--bancs", "essai pur", "--pas", "1", "--ecrire", str(reference)]) == 0
    assert emp.main(["--bancs", "essai pur", "--pas", "1", "--comparer", str(reference)]) == 0
    document = json.loads(reference.read_text(encoding="utf-8"))
    document["bancs"]["essai pur"]["0.02"]["empreinte"] = "0" * 64
    reference.write_text(json.dumps(document), encoding="utf-8")
    capsys.readouterr()
    assert emp.main(["--bancs", "essai pur", "--pas", "1", "--comparer", str(reference)]) == 1
    assert "essai pur, π* = 0.02, empreinte" in capsys.readouterr().err
    # Nombre de pas différent : écart, jamais une comparaison silencieuse.
    assert emp.main(["--bancs", "essai pur", "--pas", "2", "--comparer", str(reference)]) == 1


# --------------------------------------------------------------------------
# Réserves du rang 1a (P185) : m-a (bloc réel), m-c (code 3)
# --------------------------------------------------------------------------


def _remplacer(blocs, radical, bloc):
    return tuple(bloc if b.declaration.radical == radical else b for b in blocs)


def test_sous_classe_vide_d_un_bloc_reel_refusee(emp, racine):
    """m-a : une sous-classe vide d'un bloc réel, définie hors de `nations.blocs`, n'est pas un
    bloc réel (test strict sur `type(b).__module__`), quel que soit le banc, bloc 9 des bancs D
    et BF compris."""
    s = racine.socle
    for banc, radical in ((emp.SANS_X4, "production"), (emp.SOCLE_COMPLET, "production"),
                          (emp.SOCLE_COMPLET_D, "production"),
                          (emp.SOCLE_COMPLET, "finances_publiques"),
                          (emp.SOCLE_COMPLET_D, "finances_publiques"),
                          (emp.SOCLE_COMPLET_BF, "finances_publiques")):
        blocs, _, _ = racine.construire(banc, 0.02)
        reel, = (b for b in blocs if b.declaration.radical == radical)
        classe = type(reel)
        if classe.__module__ != f"nations.blocs.{radical}":
            classe = classe.__bases__[0]
        vide = type(f"{classe.__name__}Vide", (classe,), {"__slots__": ()})()
        assert type(vide).__module__ == __name__
        with pytest.raises(emp.BancNonConforme, match=f"manquants : \\['{radical}'\\]"):
            emp.verifier_blocs(banc, _remplacer(blocs, radical, vide), s.RADICAUX)


def test_bloc_9_compose_admis_dans_les_seuls_bancs_d_et_bf(emp, racine):
    """m-a : le bloc 9 composé (module des scénarios du socle complet, base directe unique la
    classe réelle) est réel dans les bancs D et BF, et refusé ailleurs ; une composition à deux
    bases ou d'une autre base est refusée."""
    s = racine.socle
    for banc in (emp.SOCLE_COMPLET_D, emp.SOCLE_COMPLET_BF):
        blocs, _, _ = racine.construire(banc, 0.02)
        compose, = (b for b in blocs if b.declaration.radical == "finances_publiques")
        assert type(compose).__module__ == emp.MODULE_DU_SOCLE_COMPLET
        emp.verifier_blocs(banc, blocs, s.RADICAUX)
    blocs, _, _ = racine.construire(emp.SOCLE_COMPLET, 0.02)
    with pytest.raises(emp.BancNonConforme, match="manquants : \\['finances_publiques'\\]"):
        emp.verifier_blocs(emp.SOCLE_COMPLET, _remplacer(blocs, "finances_publiques", compose),
                           s.RADICAUX)
    reel = type(compose).__bases__[0]

    class Melange:
        __slots__ = ()
    deux_bases = type("Deux", (reel, Melange), {"__slots__": (),
                                                "__module__": emp.MODULE_DU_SOCLE_COMPLET})()
    fausse_base = type("Faux", (type(compose),), {"__slots__": (),
                                                  "__module__": emp.MODULE_DU_SOCLE_COMPLET})()
    for intrus in (deux_bases, fausse_base):
        with pytest.raises(emp.BancNonConforme, match="manquants : \\['finances_publiques'\\]"):
            emp.verifier_blocs(emp.SOCLE_COMPLET_D, _remplacer(blocs, "finances_publiques",
                                                               intrus), s.RADICAUX)


def test_sous_classe_vide_d_un_bloc_reel_sort_en_code_2(emp, racine, monkeypatch, capsys):
    """m-a : par le script, un banc dont un bloc réel est remplacé par une sous-classe vide est
    un refus (code 2), jamais une empreinte."""
    construire = emp.Racine.construire

    def construire_avec_une_sous_classe(self, banc, pi):
        blocs, initial, derouler = construire(self, banc, pi)
        reel, = (b for b in blocs if b.declaration.radical == "travail")
        vide = type("TravailVide", (type(reel),), {"__slots__": ()})()
        return _remplacer(blocs, "travail", vide), initial, derouler
    monkeypatch.setattr(emp.Racine, "construire", construire_avec_une_sous_classe)
    assert emp.main(["--bancs", "J3-d1 sans X4", "--pas", "1"]) == emp.REFUS == 2
    assert "manquants : ['travail']" in capsys.readouterr().err


def _reference(emp, tmp_path, bancs=("essai pur",)):
    reference = tmp_path / "reference.json"
    assert emp.main(["--bancs", *bancs, "--pas", "2", "--ecrire", str(reference)]) == 0
    return reference


def test_comparer_grandeurs_seules_differentes_code_3(emp, tmp_path, capsys):
    """m-c (P186, P189) : seules les sous-empreintes `grandeurs` diffèrent : code 3,
    « trajectoires identiques, grandeurs d'ouverture différentes » ; dès qu'une empreinte de
    trajectoire diffère aussi, code 1."""
    reference = _reference(emp, tmp_path)
    document = json.loads(reference.read_text(encoding="utf-8"))
    document["bancs"]["essai pur"]["0.02"]["grandeurs"] = "0" * 64
    reference.write_text(json.dumps(document), encoding="utf-8")
    capsys.readouterr()
    assert emp.main(["--bancs", "essai pur", "--pas", "2", "--comparer", str(reference)]) == 3
    err = capsys.readouterr().err
    assert "trajectoires identiques, grandeurs d'ouverture différentes" in err
    assert "essai pur, π* = 0.02, grandeurs" in err
    for partie in ("empreinte", "etats", "montants", "variables"):
        autre = json.loads(json.dumps(document))
        autre["bancs"]["essai pur"]["0.1"][partie] = "0" * 64
        reference.write_text(json.dumps(autre), encoding="utf-8")
        capsys.readouterr()
        assert emp.main(["--bancs", "essai pur", "--pas", "2", "--comparer",
                         str(reference)]) == 1, partie
        err = capsys.readouterr().err
        assert f"essai pur, π* = 0.1, {partie}" in err and "grandeurs" in err
        assert "trajectoires identiques" not in err


@pytest.mark.parametrize("sens", ["ajout", "retrait"])
def test_ajout_ou_retrait_d_une_grandeur_d_ouverture_code_3(emp, racine, tmp_path, monkeypatch,
                                                            capsys, sens):
    """m-c (P189) : l'ajout d'une grandeur d'ouverture sans lecteur, ou son retrait (forme du
    retrait de `g`, #144 point 3 : la référence porte la grandeur, la mesure ne la porte plus),
    laisse les trajectoires identiques au bit : code 3."""
    grandeurs = racine.ordo.GRANDEURS_OUVERTURE
    type_ = type(grandeurs[0])
    avec_essai = grandeurs + (type_("grandeur_d_essai", lambda e, p, d: 1.0, None,
                                    "sans dimension"),)
    if sens == "ajout":
        reference = _reference(emp, tmp_path, ("socle complet", "essai pur"))
        monkeypatch.setattr(racine.ordo, "GRANDEURS_OUVERTURE", avec_essai)
    else:
        monkeypatch.setattr(racine.ordo, "GRANDEURS_OUVERTURE", avec_essai)
        reference = _reference(emp, tmp_path, ("socle complet", "essai pur"))
        monkeypatch.setattr(racine.ordo, "GRANDEURS_OUVERTURE", grandeurs)
    capsys.readouterr()
    assert emp.main(["--bancs", "socle complet", "essai pur", "--pas", "2", "--comparer",
                     str(reference)]) == 3
    assert "trajectoires identiques, grandeurs d'ouverture différentes" in (
        capsys.readouterr().err)


def test_aide_cite_les_codes_de_sortie(emp, capsys):
    with pytest.raises(SystemExit):
        emp.main(["--help"])
    aide = " ".join(capsys.readouterr().out.split())
    assert "3 trajectoires identiques, grandeurs d'ouverture différentes" in aide
    assert "3 si seules les grandeurs d'ouverture diffèrent" in aide
    assert "référence mesurée avec exclusion" in aide and "critère de P187 tenu" in aide


# --------------------------------------------------------------------------
# Variables exclues (`--exclure-variables`, P187)
# --------------------------------------------------------------------------

EXCLUES = ("iB_BH", "iB_BBk", "iB_BCB")
BANCS_COURTS = ("socle complet", "essai pur")


def test_nom_exclu_inconnu_refuse_code_2(emp, racine, capsys):
    """Un nom qui n'est une variable du pas d'aucun banc mesuré est refusé (code 2), y compris
    à côté de noms valides, et y compris quand il n'existe que dans un banc non mesuré : jamais
    une exclusion silencieuse d'une faute de frappe."""
    for bancs, noms in ((BANCS_COURTS, ("iB_BH", "iB_BHH")), (("essai pur",), ("iB_BH",))):
        capsys.readouterr()
        assert emp.main(["--bancs", *bancs, "--pas", "1", "--exclure-variables",
                         *noms]) == emp.REFUS == 2
        err = capsys.readouterr().err
        assert "refus" in err and "variable du pas d'aucun banc mesuré" in err
    with pytest.raises(emp.BancNonConforme, match="iB_BHH"):
        emp.empreintes(racine, ("socle complet",), 1, ("iB_BHH",))


def test_exclusion_ne_change_que_les_variables(emp, racine):
    """L'exclusion change `variables` et l'empreinte qui en dépend (banc à π*, banc, globale),
    et seulement elles : `etats`, `montants` et `grandeurs` égaux ; sans retrait, la
    sous-empreinte est celle de la mesure sans exclusion ; un banc sans ces variables est
    inchangé."""
    sans = emp.empreintes(racine, BANCS_COURTS, NB_PAS_COURT)
    avec = emp.empreintes(racine, BANCS_COURTS, NB_PAS_COURT, EXCLUES)
    assert sans["variables_exclues"] == [] and avec["variables_exclues"] == sorted(EXCLUES)
    for pi, v in avec["bancs"]["socle complet"].items():
        s = sans["bancs"]["socle complet"][pi]
        for partie in ("etats", "montants", "grandeurs"):
            assert v[partie] == s[partie], (pi, partie)
        assert v["variables"] != s["variables"] and v["empreinte"] != s["empreinte"]
        assert v["variables_sans_exclusion"] == s["variables"]
        assert v["exclues_presentes"] == sorted(EXCLUES)
        assert "variables_sans_exclusion" not in s and "exclues_presentes" not in s
    for pi, v in avec["bancs"]["essai pur"].items():
        s = sans["bancs"]["essai pur"][pi]
        assert {p: v[p] for p in s} == s and v["exclues_presentes"] == []
    assert avec["par_banc"]["essai pur"] == sans["par_banc"]["essai pur"]
    assert avec["par_banc"]["socle complet"] != sans["par_banc"]["socle complet"]
    assert avec["globale"] != sans["globale"]


def test_hacheur_retire_les_seules_variables_exclues(emp, racine):
    """Fin de pas fabriquée : exclure `b` équivaut à ne pas l'avoir écrite ; état et grandeurs
    inchangés."""
    _, initial, _ = racine.construire(emp.SOCLE_COMPLET, 0.02)

    def fin(variables):
        return racine.fin_de_pas(t=0, etat=initial, variables_du_pas=variables,
                                 grandeurs_ouverture=(("g", 1.0),))
    avec_b = (("a", 1.0), ("b", 3.0))
    exclu = emp.Hacheur(racine.champs, racine.cloture, racine.fin_de_pas, {"b"})
    exclu.relever(fin(avec_b))
    sans_b = _hacher(emp, racine, (fin((("a", 1.0),)),))
    complet = _hacher(emp, racine, (fin(avec_b),))
    assert exclu.complet.hexdigest() == sans_b.complet.hexdigest()
    for partie in emp.PARTIES + emp.HORS_EMPREINTE:
        assert exclu.parties[partie].hexdigest() == sans_b.parties[partie].hexdigest()
    assert exclu.sans_exclusion.hexdigest() == complet.parties["variables"].hexdigest()
    assert exclu.exclues_presentes == {"b"}


def test_document_json_porte_les_noms_exclus(emp, tmp_path, capsys):
    """`--ecrire` consigne les noms exclus (triés, sans doublon), l'affichage les cite ; sans
    l'option, la liste est vide."""
    chemin = tmp_path / "avec.json"
    assert emp.main(["--bancs", *BANCS_COURTS, "--pas", "1", "--ecrire", str(chemin),
                     "--exclure-variables", "iB_BH", "iB_BCB", "iB_BBk", "iB_BH"]) == 0
    assert "variables du pas exclues (P187) : iB_BBk, iB_BCB, iB_BH" in capsys.readouterr().out
    document = json.loads(chemin.read_text(encoding="utf-8"))
    assert document["variables_exclues"] == ["iB_BBk", "iB_BCB", "iB_BH"]
    assert document["bancs"]["socle complet"]["0.02"]["exclues_presentes"] == document[
        "variables_exclues"]
    assert emp.main(["--bancs", "essai pur", "--pas", "1", "--ecrire", str(chemin)]) == 0
    assert json.loads(chemin.read_text(encoding="utf-8"))["variables_exclues"] == []


def _ecrire(emp, tmp_path, nom, exclues=()):
    chemin = tmp_path / nom
    options = ["--exclure-variables", *exclues] if exclues else []
    assert emp.main(["--bancs", *BANCS_COURTS, "--pas", "2", "--ecrire", str(chemin),
                     *options]) == 0
    return chemin


def _comparer(emp, chemin, exclues=()):
    options = ["--exclure-variables", *exclues] if exclues else []
    return emp.main(["--bancs", *BANCS_COURTS, "--pas", "2", "--comparer", str(chemin),
                     *options])


def test_comparaison_avec_exclusion(emp, tmp_path, capsys):
    """Règles de comparabilité (P187 : seules des variables absentes de la référence
    s'excluent) :
    - référence sans exclusion où les variables exclues sont **absentes** (simulée par une
      mesure avec exclusion dont la clé `variables_exclues` est retirée) : code 0 ;
    - référence sans exclusion qui **porte** les variables exclues : refus (code 2), et une
      seule présence établie (un π* sur trois) suffit ;
    - référence mesurée avec exclusion, mesure sans, avec les mêmes ou d'autres exclusions :
      refus (code 2) ;
    - référence sans exclusion, `variables` différente des deux sous-empreintes à tous les π* :
      écart (code 1), absence non établie signalée et décomptée."""
    sans = _ecrire(emp, tmp_path, "sans.json")
    avec = _ecrire(emp, tmp_path, "avec.json", EXCLUES)
    absentes = json.loads(avec.read_text(encoding="utf-8"))
    del absentes["variables_exclues"]
    absentes_chemin = tmp_path / "absentes.json"
    absentes_chemin.write_text(json.dumps(absentes), encoding="utf-8")
    assert _comparer(emp, absentes_chemin, EXCLUES) == 0
    capsys.readouterr()
    assert _comparer(emp, sans, EXCLUES) == 2
    err = capsys.readouterr().err
    assert "présentes dans la référence" in err and "socle complet, π* = 0.02" in err
    assert "essai pur" not in err
    for exclues in (EXCLUES, (), ("iB_BH",)):
        capsys.readouterr()
        assert _comparer(emp, avec, exclues) == 2, exclues
        assert "référence mesurée avec exclusion" in capsys.readouterr().err
    document = json.loads(sans.read_text(encoding="utf-8"))
    une_seule = json.loads(json.dumps(document))
    for pi in ("0.0", "0.02"):
        une_seule["bancs"]["socle complet"][pi]["variables"] = "0" * 64
    sans.write_text(json.dumps(une_seule), encoding="utf-8")
    capsys.readouterr()
    assert _comparer(emp, sans, EXCLUES) == 2
    err = capsys.readouterr().err
    assert "présentes dans la référence" in err and "socle complet, π* = 0.1" in err
    assert "π* = 0.02" not in err
    for valeurs in document["bancs"]["socle complet"].values():
        valeurs["variables"] = "0" * 64
    sans.write_text(json.dumps(document), encoding="utf-8")
    assert _comparer(emp, sans, EXCLUES) == 1
    err = capsys.readouterr().err
    assert "socle complet, π* = 0.1, variables" in err
    assert err.count("absence dans la référence non établie") == 3
    # En-tête : écarts de trajectoire, grandeurs et absences non établies, tous décomptés.
    entete, = (ligne for ligne in err.splitlines() if ligne.startswith("ÉCART"))
    assert entete.endswith(f"({sum(ligne.startswith('  ') for ligne in err.splitlines())}) :")


def test_exclusions_symetriques_masqueraient_un_ecart_refus(emp, racine, tmp_path, monkeypatch,
                                                            capsys):
    """M1 de l'audit : une variable exclue présente dans la référence et altérée (iB_BH + 1)
    laisse égaux les documents mesurés avec les mêmes exclusions (l'écart serait masqué) ; la
    comparaison à une référence mesurée avec exclusion est donc refusée (code 2)."""
    reference = _ecrire(emp, tmp_path, "avec.json", EXCLUES)
    relever = emp.Hacheur.relever

    def relever_altere(self, e):
        if type(e) is racine.fin_de_pas:
            e = dataclasses.replace(e, variables_du_pas=tuple(
                (nom, v + 1.0 if nom == "iB_BH" else v) for nom, v in e.variables_du_pas))
        relever(self, e)
    monkeypatch.setattr(emp.Hacheur, "relever", relever_altere)
    altere = tmp_path / "altere.json"
    assert emp.main(["--bancs", *BANCS_COURTS, "--pas", "2", "--ecrire", str(altere),
                     "--exclure-variables", *EXCLUES]) == 0
    un, deux = (json.loads(f.read_text(encoding="utf-8")) for f in (reference, altere))
    assert emp.comparer(deux, un) == []  # masquage, sans la règle de refus
    assert deux["bancs"]["socle complet"]["0.02"]["variables_sans_exclusion"] != (
        un["bancs"]["socle complet"]["0.02"]["variables_sans_exclusion"])
    capsys.readouterr()
    assert _comparer(emp, reference, EXCLUES) == 2
    assert "P187 non jugeable" in capsys.readouterr().err


def test_banc_arrete_nom_exclu_non_conclu_inconnu(emp, racine, monkeypatch, capsys):
    """m1 de l'audit : un banc arrêté garde les noms exclus relevés jusqu'à l'arrêt ; un nom
    non relevé parce que le seul banc qui le porte s'est arrêté n'est pas conclu inconnu :
    code 1 (arrêt), jamais un refus (code 2)."""
    executer = racine.ordo.executer_pas

    class DefautFabrique(Exception):
        pass

    def arreter_au_pas(t_arret):
        def executer_puis_arreter(etat, *args, **kwargs):
            if etat.t == t_arret:
                raise DefautFabrique("arrêt fabriqué")
            return executer(etat, *args, **kwargs)
        return executer_puis_arreter
    monkeypatch.setattr(racine.ordo, "executer_pas", arreter_au_pas(3))
    v = emp.empreinte_du_banc(racine, emp.SOCLE_COMPLET, 0.02, 5, EXCLUES)
    assert v["arret"]["pas"] == 3 and v["exclues_presentes"] == sorted(EXCLUES)
    capsys.readouterr()
    assert emp.main(["--bancs", "socle complet", "--pas", "5", "--exclure-variables",
                     *EXCLUES]) == 1
    err = capsys.readouterr().err
    assert "socle complet, π* = 0.02 : arrêt au pas 3, DefautFabrique" in err
    assert "refus" not in err
    monkeypatch.setattr(racine.ordo, "executer_pas", arreter_au_pas(0))
    assert emp.main(["--bancs", "socle complet", "--pas", "5", "--exclure-variables",
                     *EXCLUES]) == 1
    err = capsys.readouterr().err
    assert "arrêt au pas 0" in err and "inconnues non établies" in err
    assert "refus" not in err
