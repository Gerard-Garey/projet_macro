"""Tests du banc d'empreintes `outils/empreintes_des_bancs.py` (#144, P173).

Bancs courts (`NB_PAS_COURT` pas) : le critère « identiques au bit » sur 720 pas se mesure par
le script lui-même, pas ici. Vérifiés : encodage sans ambiguïté, déterminisme (deux appels,
même empreinte), sensibilité à un écart d'un ulp (état, montant de clôture, variable du pas ;
grandeurs d'ouverture hors empreinte), refus bruyant d'un bloc manquant (en appel direct et sur
une racine extraite sans un module de bloc), arrêt du moteur consigné comme écart (code 1),
écart signalé par `--comparer` (code 1).
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
