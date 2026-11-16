"""Schéma d'état, sauvegarde et reprise (issue #96).

Contrat : ADR 0012, C1, D1 à D4 ; critères de #96 et leur complément du rang
1b (V^flux dans l'état, S hors de l'état, sauvegarde JSON à `repr`, refus,
aller-retour aux mêmes octets). Chaque test énonce une propriété (décompte,
refus, égalité bit à bit), jamais une valeur à reproduire.
"""

import ast
import dataclasses
import inspect
import json
import math
import struct
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from nations.etat import schema, unites
from nations.etat.sauvegarde import SauvegardeRefusee, charger, sauvegarder
from nations.etat.schema import (
    CHAMPS,
    CHAMPS_D_IDENTITE,
    VARIABLES,
    VERSION_SCHEMA,
    EtatPays,
    Invariance,
    VariableEtat,
)
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.grand_livre import FluxPropose, ouvrir_pas

EPS = 1e-12

# Positions d'ouverture d'essai, en u.m. (celles des tests du grand livre).
OUVERTURE = {"D_H": 600.0, "D_F": 400.0, "L": 500.0, "B_H": 200.0, "B_Bk": 300.0,
             "B_CB": 100.0, "Res": 50.0, "L_CB": 20.0, "M_G": 150.0, "K": 900.0, "IN": 100.0}

# Variables d'état des blocs (schéma v4, YD_m1 au rang 3, ti, y_m1, T_F_m1, varrho_bar_L au
# rang 4 de J3-d1 ; schéma v5, Y_HS_m1, #132), valeurs d'essai dans leurs domaines.
VARIABLES_DES_BLOCS = {"v_e": 1.0, "IN_vol": 1.4, "pr": 1.0, "K_vol": 24.0, "W": 0.8,
                       "U": 0.05, "N": 0.95, "N_pa": 1.0, "mu_tilde": 0.22314355131420976,
                       "YD_m1": 0.7, "ti": 0.14, "y_m1": 1.0, "T_F_m1": 0.0,
                       "varrho_bar_L": 0.0296, "i_L": 0.0502, "i_D": 0.0202, "pi_e": 0.02,
                       "r_hat_etoile": 0.01, "pi_etoile": 0.02, "Y_HS_m1": 0.8}


@dataclasses.dataclass(frozen=True)
class CadreDouble:
    """Double des paramètres du cadre (#97) : les deux tolérances, sans dimension."""

    tolerance_identite_pas: float = EPS
    tolerance_identite_cumulee: float = EPS


def etat_pays(identifiant="A", graine=1, t=0, registre=None, **positions):
    """État d'essai : V^flux = V^stock, registre stationnaire à π̄ = 2 % (ADR 0008, II.3),
    variables des blocs à leurs valeurs d'essai."""
    p = dict(OUVERTURE)
    p.update(positions)
    v = {cat.VALEUR_NETTE_FLUX[s]: idt.valeur_nette_stock(p, s) for s in cat.SECTEURS}
    if registre is None:
        registre = tuple(1.02 ** (-u / 12) for u in range(1, 14))
    return EtatPays(identifiant=identifiant, graine=graine, t=t, registre_prix=registre, **p, **v,
                    **VARIABLES_DES_BLOCS)


def bits(etat):
    """Empreinte bit à bit d'un état : chaque flottant par son motif binaire (−0,0 ≠ 0,0)."""
    def motif(x):
        if type(x) is float:
            return struct.pack("<d", x).hex()
        if type(x) is tuple:
            return tuple(motif(y) for y in x)
        return (type(x).__name__, x)
    return tuple((f.name, motif(getattr(etat, f.name))) for f in dataclasses.fields(etat))


def etats_tires(rng, n=3):
    """n pays aux flottants tirés sur 600 ordres de grandeur, −0,0 et sous-normaux compris."""
    def tirage():
        choix = rng.integers(0, 6)
        if choix == 0:
            return -0.0
        if choix == 1:
            return math.ulp(0.0) * float(rng.integers(1, 1000))
        signe = -1.0 if rng.integers(0, 2) else 1.0
        return signe * float(rng.uniform(1.0, 2.0)) * 2.0 ** float(rng.integers(-1000, 1000))

    def tirage_positif():
        # Niveau du registre : float fini > 0 (domaine de `registre_prix`).
        if rng.integers(0, 6) == 0:
            return math.ulp(0.0) * float(rng.integers(1, 1000))
        return float(rng.uniform(1.0, 2.0)) * 2.0 ** float(rng.integers(-1000, 1000))

    def tirage_du_domaine(nom):
        # Variables des blocs : tirage dans le domaine du schéma v2 (annotation du
        # 13/11/2026, points 1.6 et 1.7), bornes comprises quand elles sont admises.
        if nom == "U":
            return (0.0, 1.0, float(rng.uniform(0.0, 1.0)))[int(rng.integers(0, 3))]
        if nom == "pi_e":
            return float(rng.uniform(-0.999, 10.0))
        if nom in ("IN_vol", "N") and rng.integers(0, 4) == 0:
            return (0.0, -0.0)[int(rng.integers(0, 2))]
        if nom in schema.DOMAINES_DES_BLOCS:
            return tirage_positif()
        return tirage()

    etats = []
    for k in range(n):
        champs = {v.nom: (tuple(tirage_positif() for _ in range(v.longueur)) if v.type is tuple
                          else int(rng.integers(0, 10**6)) if v.type is int
                          else tirage_du_domaine(v.nom))
                  for v in VARIABLES}
        etats.append(EtatPays(identifiant=f"pays-{k:02d}", graine=int(rng.integers(0, 2**63)),
                              **champs))
    return tuple(etats)


# --------------------------------------------------------------------------
# Schéma : champs engendrés des déclarations, empreinte calendaire, S hors de l'état
# --------------------------------------------------------------------------


def test_champs_engendres_des_declarations():
    """D1 : champs de EtatPays = champs d'identité + variables déclarées, dans cet ordre."""
    assert CHAMPS == tuple(n for n, _ in CHAMPS_D_IDENTITE) + tuple(v.nom for v in VARIABLES)
    assert [f.name for f in dataclasses.fields(EtatPays)] == list(CHAMPS)
    for f in dataclasses.fields(EtatPays):
        assert f.default is dataclasses.MISSING and f.default_factory is dataclasses.MISSING
    # Schéma v5 (ADR 0013, annotation du 15/11/2026 (rang 1b de J3-d2), point 2 ; #132).
    assert VERSION_SCHEMA == 5


def test_empreinte_calendaire_de_14_variables():
    """ADR 0008, II.4 : t et les 13 niveaux du registre, propriétaire le moteur."""
    calendaires = [v for v in VARIABLES if v.proprietaire == "moteur"]
    assert [v.nom for v in calendaires] == ["t", "registre_prix"]
    assert sum(v.longueur for v in calendaires) == 14
    assert schema.VARIABLE["t"].type is int
    registre = schema.VARIABLE["registre_prix"]
    assert (registre.type, registre.longueur, registre.invariance) == (tuple, 13, Invariance.INDICE)
    # P_t est en u.m. par u.v. (spécification, P4) ; t en pas.
    assert registre.unite == "u.m. par u.v."
    assert schema.VARIABLE["t"].unite == "pas"


def test_vocabulaire_unique_des_unites():
    """ADR 0012, F2, annotations du 07/10/2026 (point 2) et du 13/11/2026 (#104, P65) : F2
    complété de quatre unités, puis de deux unités par personne et par pas, sans double."""
    f2 = ("pas par an", "pas par tour", "sans dimension", "u.m.", "u.m. par pas",
          "par an, taux de flux", "par an, taux de croissance", "années", "personnes", "fraction")
    complements = ("pas", "u.v.", "u.v. par pas", "u.m. par u.v.")
    complements_j3 = ("u.m. par personne et par pas", "u.v. par personne et par pas")
    assert unites.UNITES == f2 + complements + complements_j3
    assert len(set(unites.UNITES)) == len(unites.UNITES)
    assert {v.unite for v in VARIABLES} <= set(unites.UNITES)
    # Un seul vocabulaire : la déclaration d'une variable d'état (module feuille `variables`,
    # depuis le schéma v2) utilise celui de `unites`, elle n'en a pas de copie.
    from nations.etat import variables
    assert variables.UNITES is unites.UNITES


def test_unites_ne_charge_aucun_autre_module_de_nations():
    """`nations.etat.unites` s'importe sans charger le noyau ni le schéma (moteur/parametres, #97)."""
    code = ("import sys, nations.etat.unites\n"
            "print(sorted(m for m in sys.modules if m == 'nations' or m.startswith('nations.')))")
    sortie = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                            check=True)
    assert sortie.stdout.strip() == str(["nations", "nations.etat", "nations.etat.unites"])


def test_variables_du_noyau_positions_et_v_flux():
    """C1 et C96-1 : onze positions et cinq V^flux, propriétaire le noyau, nominales, phase 9."""
    noyau = [v for v in VARIABLES if v.proprietaire == "noyau"]
    assert [v.nom for v in noyau] == list(cat.NOMS_POSTES) + [
        cat.VALEUR_NETTE_FLUX[s] for s in cat.SECTEURS]
    for v in noyau:
        assert (v.phase_ecriture, v.unite, v.type, v.invariance) == (
            "9", "u.m.", float, Invariance.NOMINAL)
    # Décompte de l'état : 14 (empreinte) + 11 + 5 scalaires, plus les dix variables des
    # blocs du schéma v2, π*, r̂*, i_L et i_D (schéma v3, rangs 3 à 5 de J3-c, #61, #91, #90),
    # YD_{t−1} (schéma v4, rang 3 de J3-d1, #60), ti, y_{t−1}, T_{F,t−1} et ϱ̄_L (schéma v4,
    # rang 4 de J3-d1, #67), Y^HS_{t−1} (schéma v5, rang 3 de J3-d2, #132).
    assert {v.proprietaire for v in VARIABLES} == {
        "moteur", "noyau", "production", "travail", "prix", "menages", "investissement",
        "banque", "banque_centrale", "finances_publiques"}
    assert sum(v.longueur for v in VARIABLES) == 50


def test_variables_des_blocs_du_schema_v5():
    """ADR 0012, annotation du 13/11/2026, point 1.2 : nom, propriétaire, phase d'écriture,
    unité et invariance des dix variables du schéma v2, à la suite de celles du noyau, par
    radical dans l'ordre des blocs puis dans l'ordre de la table ; ADR 0013, annotation du
    14/11/2026, point 3 (P96 ; #61, #91, #90) : i_L puis i_D, avant π^e, propriétaire
    `banque`, écrites en phase 8 (c), par an, taux de flux, sans dimension ; r̂* puis π*, après
    π^e, propriétaire `banque_centrale`, écrites en phase 1, par an, taux de croissance, sans
    dimension ; annotation du 14/11/2026 (rang 1b de J3-d1), point 1 (P127 ; #60) : YD_{t−1}
    (`YD_m1`), propriétaire `menages`, entre `prix` et `banque`, écrite en phase 9, u.m. par
    pas, nominale ; (#67, P127, P128) ti (phase 5, fraction), y_{t−1} (`y_m1`, phase 5, u.v.
    par pas, volume), T_{F,t−1} (`T_F_m1`, phase 9, u.m. par pas, nominale) et ϱ̄_L
    (`varrho_bar_L`, phase 2, par an, taux de croissance), propriétaire `investissement`,
    entre `menages` et `banque` ; annotation du 15/11/2026 (rang 1b de J3-d2), point 2 (#132) :
    Y^HS_{t−1} (`Y_HS_m1`), propriétaire `finances_publiques`, dernier radical, écrite en
    phase 7, u.m. par pas, nominale."""
    blocs = [(v.nom, v.proprietaire, v.phase_ecriture, v.unite, v.type, v.longueur,
              v.invariance) for v in VARIABLES if v.proprietaire not in ("moteur", "noyau")]
    assert blocs == [
        ("v_e", "production", "5", "u.v. par pas", float, 1, Invariance.VOLUME),
        ("IN_vol", "production", "5", "u.v.", float, 1, Invariance.VOLUME),
        ("pr", "production", "5", "u.v. par personne et par pas", float, 1, Invariance.VOLUME),
        ("K_vol", "production", "5", "u.v.", float, 1, Invariance.VOLUME),
        ("W", "travail", "1", "u.m. par personne et par pas", float, 1, Invariance.NOMINAL),
        ("U", "travail", "4", "fraction", float, 1, Invariance.SANS_DIMENSION),
        ("N", "travail", "4", "personnes", float, 1, Invariance.VOLUME),
        ("N_pa", "travail", "4", "personnes", float, 1, Invariance.VOLUME),
        ("mu_tilde", "prix", "5", "sans dimension", float, 1, Invariance.SANS_DIMENSION),
        ("YD_m1", "menages", "9", "u.m. par pas", float, 1, Invariance.NOMINAL),
        ("ti", "investissement", "5", "fraction", float, 1, Invariance.SANS_DIMENSION),
        ("y_m1", "investissement", "5", "u.v. par pas", float, 1, Invariance.VOLUME),
        ("T_F_m1", "investissement", "9", "u.m. par pas", float, 1, Invariance.NOMINAL),
        ("varrho_bar_L", "investissement", "2", "par an, taux de croissance", float, 1,
         Invariance.SANS_DIMENSION),
        ("i_L", "banque", "8c", "par an, taux de flux", float, 1, Invariance.SANS_DIMENSION),
        ("i_D", "banque", "8c", "par an, taux de flux", float, 1, Invariance.SANS_DIMENSION),
        ("pi_e", "banque_centrale", "1", "par an, taux de croissance", float, 1,
         Invariance.SANS_DIMENSION),
        ("r_hat_etoile", "banque_centrale", "1", "par an, taux de croissance", float, 1,
         Invariance.SANS_DIMENSION),
        ("pi_etoile", "banque_centrale", "1", "par an, taux de croissance", float, 1,
         Invariance.SANS_DIMENSION),
        ("Y_HS_m1", "finances_publiques", "7", "u.m. par pas", float, 1, Invariance.NOMINAL),
    ]
    assert CHAMPS[-20:] == tuple(nom for nom, *_ in blocs)
    # W (point 1.3), YD_{t−1} et T_{F,t−1} (schéma v4), Y^HS_{t−1} (schéma v5) sont les variables
    # nominales des blocs.
    assert [nom for nom, *_, inv in blocs if inv is Invariance.NOMINAL] == [
        "W", "YD_m1", "T_F_m1", "Y_HS_m1"]
    # Un module de déclarations par radical (G1 (a)), assemblé par `schema` seul, `menages` puis
    # `investissement` avant `banque` (ordre des blocs, H1.5).
    from nations.etat import (
        banque,
        banque_centrale,
        finances_publiques,
        investissement,
        menages,
        prix,
        production,
        travail,
    )
    assert schema.VARIABLES_DES_BLOCS == (production.VARIABLES + travail.VARIABLES
                                          + prix.VARIABLES + menages.VARIABLES
                                          + investissement.VARIABLES
                                          + banque.VARIABLES + banque_centrale.VARIABLES
                                          + finances_publiques.VARIABLES)
    # μ̃, r̂*, i_L, i_D, YD_{t−1}, T_{F,t−1} et ϱ̄_L : finitude seule, sans domaine propre (point
    # 1.4 de l'annotation du 13/11/2026 ; ADR 0013, annotation du 14/11/2026, point 4 ;
    # annotation du 14/11/2026 (rang 1b de J3-d1), point 1).
    assert set(schema.DOMAINES_DES_BLOCS) == {v[0] for v in blocs} - {
        "mu_tilde", "r_hat_etoile", "i_L", "i_D", "YD_m1", "T_F_m1", "varrho_bar_L", "Y_HS_m1"}


def test_cloture_du_noyau_couvre_exactement_ses_variables_d_etat():
    """Le grand livre rend, à `clore_pas`, exactement les variables d'état dont le noyau est propriétaire."""
    gl = ouvrir_pas(etat_pays(), CadreDouble())
    for phase in cat.PHASES:
        for ligne in cat.LIGNES_DE_LA_PHASE[phase]:
            if ligne.proposant is not None:
                gl.proposer(FluxPropose(ligne.identifiant, {t.nom: 0.0 for t in ligne.termes},
                                        ligne.proposant))
        gl.clore_phase(phase)
    fin = gl.clore_pas()
    assert set(fin.variables) == {v.nom for v in VARIABLES if v.proprietaire == "noyau"}


def test_aucune_variable_hors_du_schema():
    """Ni attribut créé à la volée, ni champ manquant ou en trop, ni affectation."""
    e = etat_pays()
    assert not hasattr(e, "__dict__")
    with pytest.raises(dataclasses.FrozenInstanceError):
        e.D_H = 1.0
    with pytest.raises((dataclasses.FrozenInstanceError, AttributeError, TypeError)):
        e.echelle_banque = 1.0
    champs = {f.name: getattr(e, f.name) for f in dataclasses.fields(e)}
    with pytest.raises(TypeError):
        EtatPays(**champs, S_banque=1.0)
    for nom in CHAMPS:
        with pytest.raises(TypeError):
            EtatPays(**{k: v for k, v in champs.items() if k != nom})


def test_echelle_hors_de_l_etat_recalculee_a_la_reprise():
    """C96-2 : S n'est pas un champ ; elle se recalcule à l'ouverture, identique bit à bit après reprise."""
    noms = {n.lower() for n in CHAMPS}
    assert not any("echelle" in n or n.startswith("s_") for n in noms)
    e = etat_pays()
    repris, = charger(sauvegarder([e]))
    avant, apres = ouvrir_pas(e, CadreDouble()), ouvrir_pas(repris, CadreDouble())
    for s in cat.SECTEURS:
        assert struct.pack("<d", avant.echelle(s)) == struct.pack("<d", apres.echelle(s))


def test_etat_pays_satisfait_l_etat_d_ouverture_du_noyau():
    """Le noyau ouvre un pas sur le vrai schéma : t entier, positions et V^flux en float."""
    # V^flux décalées de quelques ulp de V^stock (sous ε_V) : le noyau les lit
    # dans l'état, il ne les recalcule pas des positions.
    base = etat_pays(t=5)
    decalees = {}
    for k, s in enumerate(cat.SECTEURS, start=1):
        nom = cat.VALEUR_NETTE_FLUX[s]
        v = getattr(base, nom)
        decalees[nom] = v + 2 * k * math.ulp(max(abs(v), 1.0))
    e = dataclasses.replace(base, **decalees)
    gl = ouvrir_pas(e, CadreDouble())
    assert gl.phase_courante() == "1"
    for nom in cat.NOMS_POSTES:
        assert gl.ouverture(nom) == getattr(e, nom)
    # Un pas sans flux : V^flux_{t+1} = V^flux_t, bit à bit, pour les cinq secteurs.
    for phase in cat.PHASES:
        for ligne in cat.LIGNES_DE_LA_PHASE[phase]:
            if ligne.proposant is not None:
                gl.proposer(FluxPropose(ligne.identifiant, {t.nom: 0.0 for t in ligne.termes},
                                        ligne.proposant))
        gl.clore_phase(phase)
    for s in cat.SECTEURS:
        nom = cat.VALEUR_NETTE_FLUX[s]
        assert struct.pack("<d", gl.valeur_nette_flux(s)) == struct.pack("<d", getattr(e, nom))
        assert getattr(e, nom) != getattr(base, nom)


@pytest.mark.parametrize("champ, valeur", [
    ("identifiant", 3), ("graine", 1.0), ("graine", True), ("t", 0.0), ("t", True),
    ("t", np.int64(0)), ("D_H", 600), ("D_H", np.float64(600.0)), ("V_flux_banque", None),
    ("registre_prix", [1.0] * 13), ("registre_prix", (1.0,) * 12), ("registre_prix", (1.0,) * 14),
    ("registre_prix", (1,) + (1.0,) * 12),
])
def test_type_faux_refuse_a_la_construction(champ, valeur):
    with pytest.raises(TypeError, match=champ):
        dataclasses.replace(etat_pays(), **{champ: valeur})


# Champs hors de leur domaine (B-5 ; décisions du mainteneur du 07/10/2026,
# constats N-1, N-2 et C-1, catégories Cf, Zl, Zp et forme NFC de l'identifiant) :
# mêmes refus à la construction et à la reprise.
HORS_DOMAINE = [
    ("graine", -1, "graine négative"), ("graine", -(2**70), "graine négative"),
    ("graine", schema.GRAINE_EXCLUE, "≥ 2\\^64"), ("graine", 2**70, "≥ 2\\^64"),
    ("t", -1, "t négatif"), ("t", -(2**70), "t négatif"),
    ("t", schema.T_EXCLU, "≥ 2\\^63"), ("t", 2**64, "≥ 2\\^63"),
    ("identifiant", "", "identifiant vide"),
    ("identifiant", "\ud800", "UTF-8"), ("identifiant", "A\udfff", "UTF-8"),
    ("identifiant", "\x00", "contrôle"), ("identifiant", "A\x7fB", "contrôle"),
    ("identifiant", "A\x85", "contrôle"), ("identifiant", "\t", "contrôle"),
    ("identifiant", " A", "espace de bord"), ("identifiant", "A ", "espace de bord"),
    ("identifiant", "\u00a0A", "espace de bord"),
    ("identifiant", "A\u202eB", "de format \\(U\\+202E, Cf\\)"),
    ("identifiant", "A\u200b", "de format \\(U\\+200B, Cf\\)"),
    ("identifiant", "\ufeffA", "de format \\(U\\+FEFF, Cf\\)"),
    ("identifiant", "A\u2028B", "séparateur de ligne \\(U\\+2028, Zl\\)"),
    ("identifiant", "A\u2028", "séparateur de ligne"),
    ("identifiant", "A\u2029B", "séparateur de paragraphe \\(U\\+2029, Zp\\)"),
    ("identifiant", "e\u0301", "NFC"), ("identifiant", "\u212b", "NFC"),
    # Variables des blocs (schéma v2 ; annotation du 13/11/2026, points 1.6 et 1.7).
    ("v_e", 0.0, "hors du domaine v\\^e > 0"), ("v_e", -1.0, "v\\^e > 0"),
    ("IN_vol", -1e-300, "hors du domaine IN\\^vol ≥ 0"),
    ("pr", 0.0, "hors du domaine pr > 0"), ("K_vol", -0.0, "hors du domaine K\\^vol > 0"),
    ("W", 0.0, "hors du domaine W > 0"), ("W", -2.5, "W > 0"),
    ("U", -1e-300, "hors du domaine 0 ≤ U ≤ 1"), ("U", 1.0000000000000002, "0 ≤ U ≤ 1"),
    ("N", -1.0, "hors du domaine N ≥ 0"), ("N_pa", 0.0, "hors du domaine N\\^pa > 0"),
    ("pi_e", -1.0, "hors du domaine 1 \\+ π\\^e > 0"), ("pi_e", -2.0, "1 \\+ π\\^e > 0"),
    # Schéma v3 (ADR 0013, annotation du 14/11/2026, point 4 ; #61).
    ("pi_etoile", -1.0, "hors du domaine 1 \\+ π\\* > 0"),
    ("pi_etoile", -1.5, "1 \\+ π\\* > 0"),
]

# Valeurs non finies des variables des blocs : refusées à la construction par le domaine
# (forme « <valeur> hors du domaine <condition> ») ; à la reprise, le JSON strict les
# refuse avant le domaine.
HORS_DOMAINE_NON_FINIS = [
    (nom, x, "hors du domaine") for nom in schema.DOMAINES_DES_BLOCS
    for x in (float("nan"), float("-inf"))
] + [("pi_e", float("nan"), "1 \\+ π\\^e > 0"), ("U", float("inf"), "0 ≤ U ≤ 1")]


@pytest.mark.parametrize("champ, valeur, motif", HORS_DOMAINE + HORS_DOMAINE_NON_FINIS)
def test_hors_domaine_refuse_a_la_construction(champ, valeur, motif):
    """Graine dans [0 ; 2^64[, t dans [0 ; 2^63[, identifiant non vide, UTF-8, NFC, sans
    caractère Cc, Cf, Zl ou Zp ni espace de bord."""
    with pytest.raises(ValueError, match=f"EtatPays.{champ} : .*{motif}"):
        dataclasses.replace(etat_pays(), **{champ: valeur})


# Finitude de toute variable `float` (décision du mainteneur du 13/11/2026, point Q2 de
# l'audit de #112) : positions, V^flux et variables des blocs, `inf`, `-inf` et `NaN`.
VARIABLES_FLOTTANTES = [v.nom for v in schema.VARIABLES if v.type is float]
NON_FINIS = (math.inf, -math.inf, math.nan)


def test_toutes_les_variables_flottantes_sont_couvertes():
    """Les variables `float` du schéma v5 : onze positions, cinq V^flux, vingt variables des
    blocs (i_L, i_D, r̂*, π*, YD_{t−1}, ti, y_{t−1}, T_{F,t−1}, ϱ̄_L et Y^HS_{t−1} comprises) ;
    aucune autre variable numérique que `t` (entier) et le registre (n-uplet)."""
    assert len(VARIABLES_FLOTTANTES) == 36
    assert set(VARIABLES_FLOTTANTES) == (set(cat.NOMS_POSTES) | set(cat.VALEUR_NETTE_FLUX.values())
                                         | {v.nom for v in schema.VARIABLES_DES_BLOCS})
    assert {v.nom for v in schema.VARIABLES if v.type is not float} == {"t", "registre_prix"}


@pytest.mark.parametrize("nom", VARIABLES_FLOTTANTES)
def test_defaut_de_domaine_refuse_toute_valeur_non_finie(nom):
    """Appel direct : `defaut_de_domaine` rend un motif pour `inf`, `-inf` et `NaN` de toute
    variable `float` ; « non fini » quand aucun domaine propre ne la refuse avant (positions,
    V^flux, μ̃, v^e = +inf…)."""
    for x in NON_FINIS:
        motif = schema.defaut_de_domaine(nom, x)
        assert motif is not None, (nom, x)
        if nom not in schema.DOMAINES_DES_BLOCS:
            assert motif == f"{x!r} non fini : float fini attendu"
    # Une valeur finie quelconque d'une position ou d'une V^flux reste sans motif.
    if nom not in schema.DOMAINES_DES_BLOCS:
        for x in (0.0, -1e300, 1e300, 5e-324):
            assert schema.defaut_de_domaine(nom, x) is None


@pytest.mark.parametrize("nom", VARIABLES_FLOTTANTES)
def test_etat_non_fini_refuse_a_la_construction(nom):
    """`EtatPays` refuse à la construction toute variable `float` non finie, le diagnostic
    nommant le champ (état initial, état de clôture de chaque pas, reprise)."""
    for x in NON_FINIS:
        with pytest.raises(ValueError, match=f"EtatPays.{nom} : "):
            dataclasses.replace(etat_pays(), **{nom: x})


def test_plus_l_infini_d_une_variable_a_domaine_ouvert_est_non_fini():
    """v^e > 0, K^vol > 0, W > 0 admettaient `+inf` avant le contrôle de finitude ; μ̃, sans
    domaine propre, admettait `NaN` : refusés désormais sous le motif « non fini »."""
    for nom in ("v_e", "K_vol", "W", "IN_vol", "N"):
        with pytest.raises(ValueError, match=f"EtatPays.{nom} : inf non fini"):
            dataclasses.replace(etat_pays(), **{nom: math.inf})
    with pytest.raises(ValueError, match="EtatPays.mu_tilde : nan non fini"):
        dataclasses.replace(etat_pays(), mu_tilde=math.nan)


def _registre_avec(u, niveau):
    """Registre stationnaire d'essai dont le niveau u (P_{t−u}) est remplacé."""
    registre = [1.02 ** (-k / 12) for k in range(1, 14)]
    registre[u - 1] = niveau
    return tuple(registre)


# Niveaux du registre hors de leur domaine, float fini > 0 (spécification, lecture
# de `eq:moteur-registre-prix` : « Un indice non fini ou non positif est refusé »).
REGISTRE_HORS_DOMAINE = [
    (1, float("nan")), (13, float("nan")), (1, 0.0), (13, 0.0), (7, -0.0),
    (1, -1.0), (13, -1e-300), (1, float("inf")), (13, float("-inf")),
]


@pytest.mark.parametrize("u, niveau", REGISTRE_HORS_DOMAINE)
def test_registre_hors_domaine_refuse_a_la_construction(u, niveau):
    """Un niveau du registre non fini ou non positif est refusé ; le diagnostic nomme le
    champ et le niveau."""
    with pytest.raises(ValueError,
                       match=f"EtatPays.registre_prix : niveau {u} .*float fini > 0 attendu"):
        etat_pays(registre=_registre_avec(u, niveau))


@pytest.mark.parametrize("champs", [
    {"graine": 0}, {"graine": schema.GRAINE_EXCLUE - 1}, {"graine": 2**63},
    {"t": 0}, {"t": 10**6}, {"t": schema.T_EXCLU - 1},
    {"identifiant": "x"}, {"identifiant": "État-α"}, {"identifiant": "A B"},
    {"identifiant": "\U0001F30D"}, {"identifiant": "\u00e9"},
    {"U": 0.0}, {"U": 1.0}, {"U": -0.0}, {"IN_vol": 0.0}, {"N": 0.0}, {"pi_e": -0.999},
    {"mu_tilde": -3.0}, {"mu_tilde": 0.0}, {"W": 5e-324}, {"v_e": 1e300},
    {"pi_etoile": -0.999}, {"pi_etoile": 0.0}, {"pi_etoile": -0.05},
    # r̂* : finitude seule, sans condition de signe (ADR 0013, annotation du 14/11/2026,
    # point 4 ; #91).
    {"r_hat_etoile": -0.5}, {"r_hat_etoile": -5.0}, {"r_hat_etoile": 0.0},
    # i_L et i_D : finitude seule, sans condition de signe (i_D négatif sans plancher ; ADR
    # 0013, annotation du 14/11/2026, point 4 ; #90).
    {"i_D": -0.01}, {"i_D": -2.0}, {"i_L": -0.5}, {"i_L": 0.0}, {"i_D": 0.0},
])
def test_valeurs_aux_bornes_du_domaine_admises(champs):
    """Les bornes incluses (0, 2^64 − 1, 2^63 − 1), les identifiants Unicode réguliers
    (« é » en NFC compris) et les variables des blocs aux bornes admises de leur domaine
    (U = 0 et U = 1, IN^vol = 0, N = 0 ; μ̃ de signe quelconque) passent l'aller-retour."""
    e = dataclasses.replace(etat_pays(), **champs)
    assert all(getattr(e, nom) == valeur for nom, valeur in champs.items())
    assert charger(sauvegarder([e])) == (e,)


def test_bornes_declarees():
    """Bornes nommées : graine dans [0 ; 2^64[, t dans [0 ; 2^63[."""
    assert (schema.GRAINE_MINIMALE, schema.GRAINE_EXCLUE, schema.T_MINIMAL, schema.T_EXCLU) == (
        0, 2**64, 0, 2**63)


@pytest.mark.parametrize("champ, valeur, description", [
    ("identifiant", 10**5000, "str attendu, entier de 16610 bits reçu"),
    ("registre_prix", (10**5000,) * 13, "entier de 16610 bits, " * 12 + "entier de 16610 bits\\)"),
    ("registre_prix", [-(10**5000)] * 13, "\\[-entier de 16610 bits"),
    ("t", (10**5000,), "\\(entier de 16610 bits,\\) reçu"),
], ids=["identifiant", "registre-tuple", "registre-liste", "t-tuple"])
def test_type_faux_d_entier_geant_diagnostique_sans_repr(champ, valeur, description):
    """C-2 : le diagnostic de type faux décrit un entier géant par sa taille, sans son `repr`
    (qui lèverait `ValueError` au-delà de 4 300 chiffres)."""
    with pytest.raises(TypeError, match=f"EtatPays.{champ} : .*{description}") as refus:
        dataclasses.replace(etat_pays(), **{champ: valeur})
    assert len(str(refus.value)) < 1000


def _liste_autoreferente():
    liste = []
    liste.append(liste)
    return liste


def _tuple_imbrique(profondeur, fond=()):
    valeur = fond
    for _ in range(profondeur):
        valeur = (valeur,)
    return valeur


def _liste_autoreferente_a_entier_geant():
    liste = [10**5000]
    liste.append(liste)
    return liste


def _liste_large_autoreferente():
    """100 000 références à la liste elle-même, puis un entier géant au-delà des éléments écrits."""
    liste = []
    liste.extend([liste] * 100_000)
    liste.append(10**5000)
    return liste


@pytest.mark.parametrize("champ, valeur, description", [
    ("registre_prix", _liste_autoreferente(), "\\[\\[\\.\\.\\.\\]\\] reçu"),
    ("registre_prix", _tuple_imbrique(500), "\\(\\(\\(\\(\\(.*\\),\\),\\) reçu"),
    ("registre_prix", _tuple_imbrique(100_000), "\\(<tuple de longueur 1>,\\) reçu"),
    ("t", {1: 10**5000}, "<dict de longueur 1> reçu"),
    ("t", {10**5000}, "<set de longueur 1> reçu"),
    ("registre_prix", frozenset({10**5000}), "<frozenset de longueur 1> reçu"),
    ("registre_prix", _liste_autoreferente_a_entier_geant(),
     "\\[entier de 16610 bits, <list de longueur 2>\\] reçu"),
    ("registre_prix", _tuple_imbrique(500, 10**5000), "\\(<tuple de longueur 1>,\\) reçu"),
    ("registre_prix", _liste_large_autoreferente(),
     "\\[(<list de longueur 100001>, ){32}… 99969 autres éléments\\] reçu"),
    ("registre_prix", [1.5, np.array([10**5000], dtype=object)],
     "\\[1.5, <ndarray de longueur 1>\\] reçu"),
    ("registre_prix", [10**5000, (1.0, 2.0)], "\\[entier de 16610 bits, <tuple de longueur 2>\\] reçu"),
], ids=["liste-autoreferente", "tuple-profondeur-500", "tuple-profondeur-100000", "dict-geant",
        "set-geant", "frozenset-geant", "liste-autoreferente-geant", "geant-a-profondeur-500",
        "liste-large-autoreferente", "element-a-repr-en-echec", "element-conteneur-decrit"])
def test_type_faux_cyclique_profond_ou_ensembliste_diagnostique(champ, valeur, description):
    """M-1 et M-2 (audit de b9c3fe8, #96) : une structure autoréférente, très profonde, ou un
    dictionnaire ou ensemble contenant un entier géant lève le `TypeError` du type faux, avec
    son diagnostic, sans `RecursionError` ni `ValueError`. Une valeur dont le `repr` échoue
    est décrite par son type et sa longueur, sans être parcourue ; un tuple ou une liste
    n'est écrit que sur un niveau et ses `_ELEMENTS_ECRITS` premiers éléments."""
    with pytest.raises(TypeError, match=f"EtatPays.{champ} : .*{description}") as refus:
        dataclasses.replace(etat_pays(), **{champ: valeur})
    assert len(str(refus.value)) < 5000


@pytest.mark.parametrize("signe", [1, -1])
def test_graine_de_4301_chiffres_refusee_avant_la_sauvegarde(signe):
    """N-2 : la construction refuse, avec un diagnostic qui n'écrit pas l'entier (son repr échouerait)."""
    graine = signe * 10**4300  # 4 301 chiffres, au-delà de la limite de conversion (4 300)
    assert sys.get_int_max_str_digits() == 4300
    with pytest.raises(ValueError, match="EtatPays.graine : .*entier de 14285 bits") as refus:
        dataclasses.replace(etat_pays(), graine=graine)
    assert len(str(refus.value)) < 200


@pytest.mark.parametrize("modification, motif", [
    ({"proprietaire": ""}, "sans propriétaire"),
    ({"phase_ecriture": "10"}, "phase d'écriture"),
    ({"unite": "euros"}, "unité"),
    ({"type": str}, "type"),
    ({"longueur": 2}, "longueur"),
    ({"type": tuple, "longueur": 0}, "longueur"),
    ({"nom": "é"}, "nom"),
    ({"invariance": "nominal"}, "invariance"),
])
def test_declaration_invalide_refusee(modification, motif):
    base = {"nom": "x", "proprietaire": "noyau", "phase_ecriture": "9", "unite": "u.m.",
            "type": float, "longueur": 1, "valeur_stationnaire": "0", "invariance": Invariance.NOMINAL}
    with pytest.raises(ValueError, match=motif):
        VariableEtat(**(base | modification))


# --------------------------------------------------------------------------
# Sauvegarde : JSON à repr, aller-retour aux mêmes octets, état égal bit à bit
# --------------------------------------------------------------------------


@pytest.mark.parametrize("graine", [1, 2, 3])
def test_aller_retour_bit_a_bit_et_memes_octets(graine):
    """D4 : sauvegarde → chargement → sauvegarde rend les mêmes octets ; état égal bit à bit."""
    etats = etats_tires(np.random.default_rng(graine))
    document = sauvegarder(etats)
    repris = charger(document)
    assert [bits(e) for e in repris] == [bits(e) for e in etats]
    assert sauvegarder(repris) == document
    assert all(type(e) is EtatPays for e in repris)


def test_flottants_ecrits_par_repr():
    """D3 : chaque flottant du document est le `repr` de sa valeur ; les entiers restent entiers."""
    etats = etats_tires(np.random.default_rng(4))
    document = sauvegarder(etats)
    textes = json.loads(document.decode("utf-8"), parse_float=lambda s: ("float", s))
    assert textes["version"] == VERSION_SCHEMA
    for etat, champs in zip(etats, textes["pays"], strict=True):
        assert list(champs) == list(CHAMPS)
        for v in VARIABLES:
            valeur = getattr(etat, v.nom)
            if v.type is int:
                assert champs[v.nom] == valeur
            else:
                ecrits = champs[v.nom] if v.type is tuple else [champs[v.nom]]
                attendus = valeur if v.type is tuple else (valeur,)
                assert ecrits == [("float", repr(x)) for x in attendus]
    assert document.endswith(b"\n")
    document.decode("utf-8", errors="strict")


def test_sauvegarde_refuse_un_etat_non_fini():
    """D3 : un état qui contient inf ou NaN n'est pas sauvegardable, et le diagnostic nomme le champ."""
    for champ, valeur in (("K", math.inf), ("V_flux_etat", math.nan),
                          ("registre_prix", (math.nan,) + (1.0,) * 12)):
        e = etat_pays(identifiant="B")
        # Le registre non fini est refusé dès la construction (domaine de
        # `registre_prix`) : il est forcé ici pour éprouver la défense de `sauvegarder`.
        object.__setattr__(e, champ, valeur)
        with pytest.raises(SauvegardeRefusee, match="non sauvegardable") as refus:
            sauvegarder([e])
        assert (refus.value.pays, refus.value.champ) == ("B", champ)


def test_document_utf8_non_echappe_et_un_champ_par_ligne():
    """D3 : identifiant non ASCII écrit tel quel (`ensure_ascii=False`), indentation d'un espace par niveau."""
    e = etat_pays(identifiant="État-α")
    document = sauvegarder([e])
    assert "État-α".encode() in document
    assert b"\\u" not in document
    lignes = document.decode("utf-8").splitlines()
    assert lignes[:5] == ["{", ' "version": 5,', ' "pays": [', "  {", '   "identifiant": "État-α",']
    # Un champ par ligne, trois espaces devant (profondeur 3), et un niveau du registre par ligne.
    for nom in CHAMPS:
        assert sum(1 for ligne in lignes if ligne.startswith(f'   "{nom}": ')) == 1
    assert [ligne for ligne in lignes if ligne.startswith("    ")] == [
        "    " + repr(x) + ("," if u < 12 else "") for u, x in enumerate(e.registre_prix)]


@pytest.mark.parametrize("ordre", [("B", "a"), ("Z", "É"), ("a", "é"), ("A", "AA")])
def test_ordre_canonique_par_point_de_code(ordre):
    """Les identifiants se comparent par point de code Unicode (« B » < « a »), sans locale."""
    etats = [etat_pays(identifiant=i) for i in ordre]
    assert [e.identifiant for e in charger(sauvegarder(etats))] == list(ordre)
    with pytest.raises(SauvegardeRefusee, match="ordre"):
        sauvegarder(etats[::-1])


@pytest.mark.parametrize("identifiants, motif", [(["B", "A"], "ordre"), (["A", "A"], "double")])
def test_sauvegarde_refuse_un_monde_hors_ordre(identifiants, motif):
    with pytest.raises(SauvegardeRefusee, match=motif):
        sauvegarder([etat_pays(identifiant=i) for i in identifiants])


def test_sauvegarde_refuse_un_objet_autre_qu_un_etat_pays():
    with pytest.raises(SauvegardeRefusee, match="EtatPays attendu"):
        sauvegarder([{"identifiant": "A"}])


# --------------------------------------------------------------------------
# Reprise : refus avec diagnostic
# --------------------------------------------------------------------------


def document_modifie(modifier):
    """Document valide de deux pays, modifié sur son arbre JSON puis réécrit.

    Réécrit en échappements ASCII : un substitut isolé ne peut entrer dans un
    document UTF-8 que par un échappement JSON (`"\\ud800"`).
    """
    racine = json.loads(sauvegarder([etat_pays("A"), etat_pays("B")]).decode("utf-8"))
    modifier(racine)
    return json.dumps(racine, ensure_ascii=True, indent=1).encode("utf-8")


def remplacer(cle, valeur):
    def modifier(racine):
        racine[cle] = valeur
    return modifier


def remplacer_champ(champ, valeur):
    def modifier(racine):
        racine["pays"][1][champ] = valeur
    return modifier


def retirer_champ(champ):
    def modifier(racine):
        del racine["pays"][1][champ]
    return modifier


@pytest.mark.parametrize("version", [0, 1, 2, 3, 4, 6, "5", 5.0, True, None])
def test_version_differente_refusee(version):
    with pytest.raises(SauvegardeRefusee, match="version") as refus:
        charger(document_modifie(remplacer("version", version)))
    assert refus.value.champ == "version"


def test_version_refusee_avant_tout_diagnostic_de_champ():
    """Une sauvegarde d'une autre version est refusée comme telle, même si ses champs diffèrent."""
    def modifier(racine):
        racine["version"] = 6
        racine["pays"][0]["champ_futur"] = 1.0
    with pytest.raises(SauvegardeRefusee, match="version"):
        charger(document_modifie(modifier))


def test_sauvegarde_v1_refusee_avec_diagnostic():
    """ADR 0012, D4 et annotation du 13/11/2026, point 1.5 : une sauvegarde au format v1
    (version 1, sans les variables des blocs) est refusée sous le schéma v5, avec un
    diagnostic qui nomme la version lue et la seule admise, sans migration."""
    def en_v1(racine):
        racine["version"] = 1
        for pays in racine["pays"]:
            for v in schema.VARIABLES_DES_BLOCS:
                del pays[v.nom]
    with pytest.raises(SauvegardeRefusee,
                       match="version du schéma 1 : seule la version 5 est admise "
                             "\\(aucune migration\\)") as refus:
        charger(document_modifie(en_v1))
    assert refus.value.champ == "version"


def test_sauvegarde_v2_refusee_avec_diagnostic():
    """ADR 0012, D4 ; ADR 0013, annotation du 14/11/2026, point 3 (critère de #61) : une
    sauvegarde au format v2 (version 2, sans π*) est refusée sous le schéma v5, avec un
    diagnostic qui nomme la version lue et la seule admise, sans migration ; la même, au seul
    numéro de version près, l'est encore (le champ manquant n'est pas le motif)."""
    def en_v2(racine):
        racine["version"] = 2
        for pays in racine["pays"]:
            del pays["pi_etoile"]
    with pytest.raises(SauvegardeRefusee,
                       match="version du schéma 2 : seule la version 5 est admise "
                             "\\(aucune migration\\)") as refus:
        charger(document_modifie(en_v2))
    assert refus.value.champ == "version"
    with pytest.raises(SauvegardeRefusee, match="version du schéma 2") as refus:
        charger(document_modifie(remplacer("version", 2)))
    assert refus.value.champ == "version"


def test_sauvegarde_v3_refusee_avec_diagnostic():
    """ADR 0012, D4 ; ADR 0013, annotation du 14/11/2026 (rang 1b de J3-d1), point 1 (critère
    de #60) : une sauvegarde au format v3 (version 3, sans YD_{t−1}) est refusée sous le schéma
    v5, avec un diagnostic qui nomme la version lue et la seule admise, sans migration ; la
    même, au seul numéro de version près, l'est encore (le champ manquant n'est pas le
    motif)."""
    def en_v3(racine):
        racine["version"] = 3
        for pays in racine["pays"]:
            del pays["YD_m1"]
    with pytest.raises(SauvegardeRefusee,
                       match="version du schéma 3 : seule la version 5 est admise "
                             "\\(aucune migration\\)") as refus:
        charger(document_modifie(en_v3))
    assert refus.value.champ == "version"
    with pytest.raises(SauvegardeRefusee, match="version du schéma 3") as refus:
        charger(document_modifie(remplacer("version", 3)))
    assert refus.value.champ == "version"


def test_sauvegarde_v4_refusee_avec_diagnostic():
    """ADR 0012, D4 ; ADR 0013, annotation du 15/11/2026 (rang 1b de J3-d2), point 2 (#132) :
    une sauvegarde au format v4 (version 4, sans Y^HS_{t−1}) est refusée sous le schéma v5, avec
    un diagnostic qui nomme la version lue et la seule admise, sans migration ; la même, au seul
    numéro de version près, l'est encore (le champ manquant n'est pas le motif)."""
    def en_v4(racine):
        racine["version"] = 4
        for pays in racine["pays"]:
            del pays["Y_HS_m1"]
    with pytest.raises(SauvegardeRefusee,
                       match="version du schéma 4 : seule la version 5 est admise "
                             "\\(aucune migration\\)") as refus:
        charger(document_modifie(en_v4))
    assert refus.value.champ == "version"
    with pytest.raises(SauvegardeRefusee, match="version du schéma 4") as refus:
        charger(document_modifie(remplacer("version", 4)))
    assert refus.value.champ == "version"


@pytest.mark.parametrize("champ", CHAMPS)
def test_champ_manquant_refuse(champ):
    with pytest.raises(SauvegardeRefusee, match="champ manquant") as refus:
        charger(document_modifie(retirer_champ(champ)))
    assert refus.value.champ == champ


@pytest.mark.parametrize("modifier, champ", [
    (remplacer_champ("S_banque", 1.0), "S_banque"),
    (remplacer_champ("historique_prix", [1.0, 1.0]), "historique_prix"),
    (remplacer("parametres", {}), "parametres"),
])
def test_champ_inconnu_refuse(modifier, champ):
    with pytest.raises(SauvegardeRefusee, match="champ inconnu") as refus:
        charger(document_modifie(modifier))
    assert refus.value.champ == champ


@pytest.mark.parametrize("champ, valeur", [
    ("D_H", 600), ("D_H", "600.0"), ("D_H", None), ("D_H", [600.0]), ("t", 0.0), ("t", True),
    ("graine", 1.5), ("identifiant", 7), ("registre_prix", [1.0] * 12),
    ("registre_prix", [1.0] * 14), ("registre_prix", [1] + [1.0] * 12),
    ("registre_prix", 1.0), ("V_flux_menages", False),
])
def test_type_faux_refuse(champ, valeur):
    with pytest.raises(SauvegardeRefusee, match="type faux") as refus:
        charger(document_modifie(remplacer_champ(champ, valeur)))
    # Le pays est nommé par son identifiant, ou par son rang si l'identifiant est en cause.
    assert (refus.value.pays, refus.value.champ) == (1 if champ == "identifiant" else "B", champ)


@pytest.mark.parametrize("champ, valeur, motif", HORS_DOMAINE)
def test_hors_domaine_refuse_a_la_reprise(champ, valeur, motif):
    """Mêmes refus qu'à la construction ; le pays est nommé par son rang si l'identifiant est en cause."""
    with pytest.raises(SauvegardeRefusee, match=f"hors domaine : .*{motif}") as refus:
        charger(document_modifie(remplacer_champ(champ, valeur)))
    assert (refus.value.pays, refus.value.champ) == (1 if champ == "identifiant" else "B", champ)


@pytest.mark.parametrize("u, niveau", [(u, x) for u, x in REGISTRE_HORS_DOMAINE
                                         if math.isfinite(x)])
def test_registre_non_positif_refuse_a_la_reprise(u, niveau):
    """Mêmes refus qu'à la construction, le pays et le champ nommés."""
    def modifier(racine):
        racine["pays"][1]["registre_prix"][u - 1] = niveau
    with pytest.raises(SauvegardeRefusee, match=f"hors domaine : niveau {u} .*float fini > 0"
                       ) as refus:
        charger(document_modifie(modifier))
    assert (refus.value.pays, refus.value.champ) == ("B", "registre_prix")


@pytest.mark.parametrize("constante", ["NaN", "Infinity", "-Infinity", "1e400"])
def test_registre_non_fini_refuse_a_la_reprise(constante):
    """Un niveau non fini est refusé dès la lecture JSON (B-1), avant le domaine du champ."""
    texte = sauvegarder([etat_pays()]).decode("utf-8")
    debut = texte.index('"registre_prix": [')
    fin = texte.index(",", debut)
    texte = texte[:debut] + '"registre_prix": [' + constante + texte[fin:]
    assert f"[{constante}," in texte
    with pytest.raises(SauvegardeRefusee, match="non finie"):
        charger(texte.encode("utf-8"))


def test_graine_de_4300_chiffres_refusee_a_la_reprise_avec_diagnostic():
    """Une graine lisible (4 300 chiffres, à la limite de conversion) mais hors borne : refus nommé."""
    texte = sauvegarder([etat_pays("B")]).decode("utf-8")
    assert texte.count('"graine": 1') == 1
    with pytest.raises(SauvegardeRefusee, match="hors domaine : .*entier de 14285 bits") as refus:
        charger(texte.replace('"graine": 1', '"graine": ' + "9" * 4300).encode("utf-8"))
    assert (refus.value.pays, refus.value.champ) == ("B", "graine")


@pytest.mark.parametrize("identifiants, motif", [(["B", "A"], "ordre"), (["A", "A"], "double")])
def test_pays_hors_ordre_ou_en_double_refuse(identifiants, motif):
    def modifier(racine):
        for pays, identifiant in zip(racine["pays"], identifiants, strict=True):
            pays["identifiant"] = identifiant
    with pytest.raises(SauvegardeRefusee, match=motif):
        charger(document_modifie(modifier))


@pytest.mark.parametrize("document, motif", [
    (b"", "JSON invalide"),
    (b"[]", "racine"),
    (b'{"version": 5}', "champ manquant"),
    (b'{"pays": []}', "champ manquant"),
    (b'{"version": 5, "pays": {}}', "liste des pays"),
    (b'{"version": 5, "pays": [4]}', "objet JSON"),
    (b'{"version": 5, "version": 5, "pays": []}', "clé en double"),
    (b"\xff\xfe", "UTF-8"),
])
def test_document_mal_forme_refuse(document, motif):
    with pytest.raises(SauvegardeRefusee, match=motif):
        charger(document)


@pytest.mark.parametrize("constante", ["NaN", "Infinity", "-Infinity", "1e400", "-1e400",
                                       "1.5E309", "-0.1e310"])
def test_constante_non_finie_refusee_a_la_reprise(constante):
    """Constante non finie, ou nombre qui déborde en ±inf à la lecture (B-1) : refus."""
    texte = sauvegarder([etat_pays()]).decode("utf-8")
    texte = texte.replace('"K": 900.0', f'"K": {constante}')
    assert constante in texte
    with pytest.raises(SauvegardeRefusee, match="non finie"):
        charger(texte.encode("utf-8"))


@pytest.mark.parametrize("remplacement, motif", [
    (('"t": 0', '"t": ' + "9" * 5000), "entier de 5000 caractères"),
    (('"graine": 1', '"graine": -' + "1" * 5000), "entier de 5001 caractères"),
    (('"graine": 1', '"graine": 1' + "0" * 4300), "entier de 4301 caractères"),
    (('"K": 900.0', '"K": ' + "[" * 100_000 + "]" * 100_000), "imbriqué"),
])
def test_entier_illisible_ou_imbrication_profonde_refuse(remplacement, motif):
    """B-2 : `ValueError` (limite de conversion des entiers) et `RecursionError` deviennent des refus."""
    texte = sauvegarder([etat_pays()]).decode("utf-8")
    ancien, nouveau = remplacement
    assert texte.count(ancien) == 1
    with pytest.raises(SauvegardeRefusee, match=motif):
        charger(texte.replace(ancien, nouveau).encode("utf-8"))


def test_document_en_texte_refuse():
    with pytest.raises(SauvegardeRefusee, match="octets"):
        charger(sauvegarder([etat_pays()]).decode("utf-8"))


def test_monde_vide_aller_retour():
    assert charger(sauvegarder([])) == ()
    assert sauvegarder(charger(sauvegarder([]))) == sauvegarder([])


# --------------------------------------------------------------------------
# Construction de clôture (#144, point 1 ; ADR 0013, annotation du 16/11/2026, point 1)
# --------------------------------------------------------------------------

SOURCE = Path(__file__).resolve().parents[2] / "src"


def _champs(etat):
    return {nom: getattr(etat, nom) for nom in CHAMPS}


def test_etat_de_cloture_egal_au_constructeur_au_bit():
    """Même objet que `EtatPays(**champs)` : type, égalité, hachage, bits, gel."""
    etat = etat_pays()
    cloture = schema.etat_de_cloture(_champs(etat))
    assert type(cloture) is EtatPays
    assert cloture == etat and hash(cloture) == hash(etat) and bits(cloture) == bits(etat)
    with pytest.raises(dataclasses.FrozenInstanceError):
        cloture.t = 1


@pytest.mark.parametrize("nom, valeur", [
    ("identifiant", ""), ("graine", -1), ("t", -1), ("t", 2**63),
    ("registre_prix", (0.0,) * 13), ("D_H", float("nan")), ("V_flux_etat", float("inf")),
])
def test_etat_de_cloture_refuse_un_champ_hors_bloc_hors_domaine(nom, valeur):
    """Le domaine des champs autres que les variables des blocs (identité, t, registre,
    positions, V^flux) reste contrôlé à la clôture, avec le refus de `EtatPays`."""
    champs = _champs(etat_pays())
    assert nom in champs
    champs[nom] = valeur
    with pytest.raises(ValueError, match=f"EtatPays.{nom} : "):
        schema.etat_de_cloture(champs)
    with pytest.raises(ValueError, match=f"EtatPays.{nom} : "):
        EtatPays(**champs)


@pytest.mark.parametrize("nom, valeur", [
    ("identifiant", 1), ("t", 0.0), ("registre_prix", (1.0,) * 12), ("D_H", 1),
    ("U", 1), ("pi_e", np.float64(0.02)), ("mu_tilde", True),
])
def test_etat_de_cloture_controle_le_type_de_tous_les_champs(nom, valeur):
    """Le type de tous les champs, variables des blocs comprises, est contrôlé à la clôture."""
    champs = _champs(etat_pays())
    champs[nom] = valeur
    with pytest.raises(TypeError, match=f"EtatPays.{nom} : "):
        schema.etat_de_cloture(champs)


def test_etat_de_cloture_ne_recontrole_pas_le_domaine_des_variables_des_blocs():
    """Le domaine d'une variable d'état d'un bloc n'est contrôlé qu'à l'écriture
    (`Vue.ecrire_etat`) : appelée directement, `etat_de_cloture` ne le refait pas, quand le
    constructeur, `dataclasses.replace` et la reprise le contrôlent toujours."""
    champs = _champs(etat_pays())
    champs["U"] = 1.2
    cloture = schema.etat_de_cloture(champs)
    assert cloture.U == 1.2
    with pytest.raises(ValueError, match="EtatPays.U : 1.2 hors du domaine"):
        EtatPays(**champs)
    with pytest.raises(ValueError, match="EtatPays.U : 1.2 hors du domaine"):
        dataclasses.replace(cloture, t=1)
    with pytest.raises(SauvegardeRefusee):
        charger(sauvegarder([cloture]))


def test_etat_de_cloture_refuse_un_champ_manquant_ou_en_trop():
    champs = _champs(etat_pays())
    with pytest.raises(TypeError, match="champs manquants \\['U'\\]"):
        schema.etat_de_cloture({k: v for k, v in champs.items() if k != "U"})
    with pytest.raises(TypeError, match="champs non déclarés \\['S_banque'\\]"):
        schema.etat_de_cloture({**champs, "S_banque": 1.0})


def test_post_init_d_etat_pays_sans_argument_ni_champ_qui_le_module():
    """Ni argument, ni `InitVar`, ni valeur par défaut ne module `EtatPays.__post_init__` : le
    contrôle complet est celui de toute construction par le constructeur."""
    assert EtatPays.__post_init__ is schema._verifier_types
    assert tuple(inspect.signature(schema._verifier_types).parameters) == ("etat",)
    assert tuple(EtatPays.__dataclass_fields__) == CHAMPS
    for champ in EtatPays.__dataclass_fields__.values():
        assert champ._field_type is dataclasses._FIELD
        assert champ.default is dataclasses.MISSING
        assert champ.default_factory is dataclasses.MISSING


def _fonctions(arbre):
    """(nom qualifié, nœud) de chaque fonction d'un module, méthodes comprises."""
    for noeud in arbre.body:
        if isinstance(noeud, ast.FunctionDef):
            yield noeud.name, noeud
        elif isinstance(noeud, ast.ClassDef):
            for sous in noeud.body:
                if isinstance(sous, ast.FunctionDef):
                    yield f"{noeud.name}.{sous.name}", sous


def _sites(predicat):
    """(fichier relatif, fonction) de chaque nœud de `src/` qui vérifie `predicat`, hors de toute
    fonction compris (« <module> »)."""
    sites = set()
    for chemin in sorted(SOURCE.rglob("*.py")):
        arbre = ast.parse(chemin.read_text(encoding="utf-8"))
        dans_une_fonction = set()
        for nom, fonction in _fonctions(arbre):
            for n in ast.walk(fonction):
                dans_une_fonction.add(id(n))
                if predicat(n):
                    sites.add((chemin.relative_to(SOURCE).as_posix(), nom))
        for n in ast.walk(arbre):
            if id(n) not in dans_une_fonction and predicat(n):
                sites.add((chemin.relative_to(SOURCE).as_posix(), "<module>"))
    return sites


def _noeuds_de_src():
    """(fichier relatif, fonction, nœud, parent) de chaque nœud de chaque module de `src/`, module
    entier (niveau module et classes imbriquées compris, « <module> » hors des fonctions de
    `_fonctions`) ; parent : nœud qui le contient, None pour le module (réserve r2 de l'audit du
    rang 3)."""
    for chemin in sorted(SOURCE.rglob("*.py")):
        arbre = ast.parse(chemin.read_text(encoding="utf-8"))
        parents = {id(e): p for p in ast.walk(arbre) for e in ast.iter_child_nodes(p)}
        fonctions = {id(n): nom for nom, f in _fonctions(arbre) for n in ast.walk(f)}
        fichier = chemin.relative_to(SOURCE).as_posix()
        for n in ast.walk(arbre):
            yield fichier, fonctions.get(id(n), "<module>"), n, parents.get(id(n))


def _nomme(n, nom):
    return (isinstance(n, ast.Name) and n.id == nom) or (
        isinstance(n, ast.Attribute) and n.attr == nom)


def test_executer_pas_seul_appelant_de_etat_de_cloture():
    """Test textuel (condition 1 de l'annotation) : dans `src/`, seul `executer_pas` nomme
    `etat_de_cloture` hors de sa définition."""
    sites = _sites(lambda n: _nomme(n, "etat_de_cloture"))
    assert sites == {("nations/moteur/ordonnanceur.py", "executer_pas")}


# Accès dynamiques aux attributs dans `src/` (`getattr`, `setattr`, `delattr`, `attrgetter`,
# `getattr_static`, `__getattribute__`, `__setattr__`) dont le nom d'attribut n'est pas une chaîne
# littérale : liste fermée des sites, mesurée le 16/11/2026 (M1 de l'audit du rang 2 : un
# `getattr` à nom calculé sur le contexte du pas contournerait les tests textuels de
# `etat_suivant`).
ACCES_DYNAMIQUES_ADMIS = {
    ("nations/etat/sauvegarde.py", "sauvegarder"),
    ("nations/etat/schema.py", "_verifier_types"),
    ("nations/etat/schema.py", "etat_de_cloture"),
    ("nations/moteur/ordonnanceur.py", "assembler"),
    ("nations/moteur/parametres/__init__.py", "valider_table"),
    ("nations/moteur/parametres/ensemble.py", "EnsembleDesParametres.__post_init__"),
    ("nations/noyau/grand_livre.py", "ouvrir_pas"),
}
_ACCES_DYNAMIQUES = {"getattr", "setattr", "delattr", "attrgetter", "getattr_static",
                     "__getattribute__", "__setattr__", "__delattr__"}
# Références à un accès dynamique qui ne sont pas appelées directement (alias, argument, valeur
# rendue ; réserve r1 de l'audit du rang 2) : (fichier, fonction, instruction), liste fermée.
# Seule admise : `poser = object.__setattr__` dans `_construire`, constructeur privé de
# `GrandLivre` (appelé par `ouvrir_pas` seul), où `poser` ne sert qu'à poser, sur l'objet neuf
# `livre`, des attributs privés nommés par un littéral (contrôlé par le test).
REFERENCES_DYNAMIQUES_ADMISES = {
    ("nations/noyau/grand_livre.py", "_construire", "poser = object.__setattr__"),
}


def _acces_dynamique(n):
    """Appel d'accès dynamique à un attribut (`getattr`, `object.__setattr__`,
    `inspect.getattr_static`…)."""
    if not isinstance(n, ast.Call):
        return False
    f = n.func
    nom = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else None
    return nom in _ACCES_DYNAMIQUES


def _reference_dynamique(n, parent):
    """Référence (Load) à un accès dynamique qui n'est pas la fonction d'un appel direct
    (`lire = getattr`, `poser = object.__setattr__`, `map(getattr, …)`), ou importation renommée
    (`from inspect import getattr_static as lire`) : l'appel passe alors par un autre nom, que
    `_acces_dynamique` ne voit pas."""
    if isinstance(n, ast.alias):
        return n.name.rsplit(".", 1)[-1] in _ACCES_DYNAMIQUES and n.asname not in (None, n.name)
    nom = (n.id if isinstance(n, ast.Name) else n.attr if isinstance(n, ast.Attribute)
           else None)
    return (nom in _ACCES_DYNAMIQUES and isinstance(n.ctx, ast.Load)
            and not (isinstance(parent, ast.Call) and parent.func is n))


def _nom_litteral(n):
    arguments = n.args[1:2] if not (isinstance(n.func, ast.Name)
                                    and n.func.id == "attrgetter") else n.args[:1]
    return (arguments[0].value if arguments and isinstance(arguments[0], ast.Constant)
            and type(arguments[0].value) is str else None)


def test_acces_dynamiques_aux_attributs_liste_fermee():
    """M1 de l'audit du rang 2 (#144, point 1) : un accès dynamique à nom calculé n'existe que
    sur une liste fermée de sites, sans `_Pas` ; un nom littéral `etat_suivant` ou `_pas` n'est
    jamais lu dynamiquement. Réserve r1 (#144) : `getattr_static` est un accès dynamique, et toute
    référence à un accès dynamique qui n'est pas appelée directement (alias) est sur une liste
    fermée, `poser` de `_construire`, dont chaque appel nomme par un littéral un attribut privé
    de l'objet neuf `livre`."""
    assert _sites(lambda n: _acces_dynamique(n) and _nom_litteral(n) is None) == (
        ACCES_DYNAMIQUES_ADMIS)
    assert _sites(lambda n: _acces_dynamique(n)
                  and _nom_litteral(n) in ("etat_suivant", "_pas")) == set()
    references = {(fichier, nom, ast.unparse(parent))
                  for fichier, nom, n, parent in _noeuds_de_src()
                  if _reference_dynamique(n, parent)}
    assert references == REFERENCES_DYNAMIQUES_ADMISES
    arbre = ast.parse((SOURCE / "nations" / "noyau" / "grand_livre.py").read_text(
        encoding="utf-8"))
    construire = dict(_fonctions(arbre))["_construire"]
    appels = [n for n in ast.walk(construire) if isinstance(n, ast.Call) and _nomme(n.func, "poser")]
    assert appels and all(
        isinstance(n.func, ast.Name) and len(n.args) == 3 and not n.keywords
        and _nomme(n.args[0], "livre") and isinstance(n.args[1], ast.Constant)
        and type(n.args[1].value) is str and n.args[1].value.startswith("_")
        and n.args[1].value != "_pas" for n in appels), [ast.unparse(n) for n in appels]
    assert [ast.unparse(n) for n in ast.walk(construire)
            if _nomme(n, "poser") and isinstance(n.ctx, ast.Load)] == ["poser"] * len(appels)


def test_vue_ecrire_etat_seul_site_qui_remplit_etat_suivant():
    """Test textuel (condition 2 de l'annotation) : dans `src/`, `etat_suivant` n'est rempli
    (affectation indicée, méthode de mutation) que par `Vue.ecrire_etat`, après son contrôle de
    domaine ; il n'est lié qu'à un dictionnaire vide dans `_Pas.__init__`, et n'est jamais
    passé à une fonction."""
    def rempli(n):
        if isinstance(n, (ast.Assign, ast.AugAssign, ast.AnnAssign, ast.Delete)):
            cibles = n.targets if isinstance(n, (ast.Assign, ast.Delete)) else [n.target]
            return any(isinstance(c, ast.Subscript) and _nomme(c.value, "etat_suivant")
                       for c in cibles)
        return (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and _nomme(n.func.value, "etat_suivant"))
    assert _sites(rempli) == {("nations/moteur/ordonnanceur.py", "Vue.ecrire_etat")}

    def passe(n):
        return isinstance(n, ast.Call) and any(
            _nomme(a, "etat_suivant") for a in (*n.args, *(k.value for k in n.keywords)))
    assert _sites(passe) == set()

    def lie(n):
        return isinstance(n, (ast.Assign, ast.AnnAssign)) and any(
            isinstance(c, ast.Attribute) and c.attr == "etat_suivant"
            for c in (n.targets if isinstance(n, ast.Assign) else [n.target]))
    assert _sites(lie) == {("nations/moteur/ordonnanceur.py", "_Pas.__init__")}
    # Lecture de l'attribut (M1 de l'audit du rang 2 : alias) : seulement dans `ecrire_etat`
    # et `executer_pas`, et seulement pour lier le nom local `etat_suivant`, qui n'est lu que
    # dans un test d'appartenance ou un indice (jamais rendu à un autre nom, ni passé).
    # Module entier (réserve r2 de l'audit du rang 2) : niveau module et classes imbriquées
    # compris, « <module> » hors des fonctions et méthodes de premier niveau.
    lus, lus_hors_liaison, noms_detournes = set(), set(), set()
    for fichier, nom, n, parent in _noeuds_de_src():
        if (isinstance(n, ast.Attribute) and n.attr == "etat_suivant"
                and isinstance(n.ctx, ast.Load)):
            lus.add((fichier, nom))
            if not (isinstance(parent, ast.Assign) and parent.value is n
                    and [ast.unparse(c) for c in parent.targets] == ["etat_suivant"]):
                lus_hors_liaison.add((fichier, nom, ast.unparse(parent)))
        if (isinstance(n, ast.Name) and n.id == "etat_suivant"
                and isinstance(n.ctx, ast.Load)
                and not isinstance(parent, (ast.Compare, ast.Subscript))):
            noms_detournes.add((fichier, nom, ast.unparse(parent)))
    assert lus == {("nations/moteur/ordonnanceur.py", "Vue.ecrire_etat"),
                   ("nations/moteur/ordonnanceur.py", "executer_pas")}
    assert lus_hors_liaison == set()
    assert noms_detournes == set()
    # Dans `Vue.ecrire_etat`, l'enregistrement suit le contrôle de domaine.
    arbre = ast.parse((SOURCE / "nations" / "moteur" / "ordonnanceur.py").read_text(
        encoding="utf-8"))
    ecrire_etat = dict(_fonctions(arbre))["Vue.ecrire_etat"]
    controle = min(n.lineno for n in ast.walk(ecrire_etat) if _nomme(n, "defaut_de_domaine"))
    enregistrement = max(n.lineno for n in ast.walk(ecrire_etat) if rempli(n))
    assert controle < enregistrement
