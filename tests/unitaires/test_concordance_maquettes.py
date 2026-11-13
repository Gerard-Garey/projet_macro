"""Concordance des deux écritures des variantes de F : maquette conjointe (#65) et contre-épreuve (#66).

`outils/maquette_conjointe.py` (`variantes_F`) et
`outils/contre_epreuve_financement.py` (`calculer`, lignes « conjoint ») sont
deux écritures indépendantes de la boucle conjointe sous F retenue et sous
ses variantes écartées (fiche 6, § 3.N ; `sec:ecartees`). L'indépendance
porte sur l'écriture des outils (chacun a son test qui lui interdit de citer
l'autre) ; ce fichier est le seul autorisé à importer les deux, pour les
comparer.

Appariement : configuration (« fiche », « socle »), λ_ti, règle de taux
(« exogene » et « regle », mêmes noms dans les deux outils), régime de T4,
écriture du levier et cible de dépôts. Le module de la racine retenue de
#65 (lecture (c)) doit égaler celui de #66 à `TOL_MODULE` près pour chaque
paire, et chaque ligne de #66 doit avoir son homologue. Lignes de #65
exclues, déclarées (`exclue`) : la branche « plancher » de B6 en
configuration « fiche » (#66 mesure la branche où l'argument de B6 est versé),
le taux « exogene_ancre » et le taux « regle » en configuration « fiche »,
que #66 ne mesure pas.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[2]
TOL_MODULE = 1e-7  # |écart| admis sur le module de la racine retenue ; mesuré ≤ 2,6e-9, 84 paires (pas rel. 1e-6)

# Financement de #65 pour (crédit, dépôts) de #66.
CREDIT_66 = {"pK_phat_ouv": "levier_pK.p_hat.ouverture", "pK_phat_apres": "levier_pK.p_hat.apres",
             "pK_pm1_ouv": "levier_pK.p_prec.ouverture", "pK_pm1_apres": "levier_pK.p_prec.apres"}


def _charger(nom: str):
    spec = importlib.util.spec_from_file_location(f"{nom}_concordance", RACINE / "outils" / f"{nom}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def financement_65(credit: str, depots: str, maquette) -> str:
    """Nom de la variante de #65 pour le crédit et les dépôts de #66."""
    if depots == "ve":
        return "F" if credit == "comptable" else CREDIT_66[credit]
    assert depots == "ventes_du_pas", depots
    if credit == "comptable":
        return "depots_ventes"
    assert credit == "pK_phat_ouv", credit  # seule combinaison publiée (fiche 6, § 3.N)
    return maquette.LEVIER_PK_DEPOTS_VENTES


def exclue(ligne) -> bool:
    """Lignes de #65 sans homologue déclaré dans #66."""
    return (ligne["B6"] == "plancher" or ligne["taux"] == "exogene_ancre"
            or (ligne["configuration"] == "fiche" and ligne["taux"] == "regle"))


def cle(configuration, lambda_ti, taux, financement, regime):
    return configuration, round(lambda_ti, 9), taux, financement, regime


@pytest.fixture(scope="module")
def paires():
    maquette, contre = _charger("maquette_conjointe"), _charger("contre_epreuve_financement")
    lignes_65 = {cle(v["configuration"], v["lambda_ti"], v["taux"], v["financement"], v["regime"]): v
                 for v in maquette.variantes_F() if not exclue(v)}
    lignes_66 = contre.calculer()["conjoint"]
    sortie, sans_homologue = [], []
    for x in lignes_66:
        k = cle(x["configuration"], x["lambda_ti"], x["taux"], financement_65(x["credit"], x["depots"], maquette),
                x["regime"])
        if k in lignes_65:
            sortie.append((k, lignes_65[k], x))
        else:
            sans_homologue.append(k)
    return maquette, lignes_65, sortie, sans_homologue


def test_chaque_ligne_a_son_homologue(paires):
    """Bijection : chaque ligne de #66 a son homologue dans #65 et chaque ligne non exclue de #65 est appariée."""
    maquette, lignes_65, sortie, sans_homologue = paires
    assert sans_homologue == []
    assert sorted(k for k, _, _ in sortie) == sorted(lignes_65)
    # Chaque variante de #65 et chaque configuration sont comparées, la combinaison comprise.
    assert {k[3] for k, _, _ in sortie} == set(maquette.FINANCEMENTS)
    assert {k[0] for k, _, _ in sortie} == set(maquette.CONFIGURATIONS_F)
    assert {k[2] for k, _, _ in sortie} == {"exogene", "regle"}
    # En configuration « fiche », la seule branche de B6 comparée est « verse ».
    assert {v["B6"] for k, v, _ in sortie if k[0] == "fiche"} == {"verse"}


def test_modules_concordent(paires):
    _, _, sortie, _ = paires
    ecarts = [(k, v["rayon"], x["rayon"]) for k, v, x in sortie if not abs(v["rayon"] - x["rayon"]) < TOL_MODULE]
    assert ecarts == []
