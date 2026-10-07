"""Schéma d'état, sauvegarde et reprise (issue #96).

Contrat : ADR 0012, C1, D1 à D4 ; critères de #96 et leur complément du rang
1b (V^flux dans l'état, S hors de l'état, sauvegarde JSON à `repr`, refus,
aller-retour aux mêmes octets). Chaque test énonce une propriété (décompte,
refus, égalité bit à bit), jamais une valeur à reproduire.
"""

import dataclasses
import json
import math
import struct
import subprocess
import sys

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


@dataclasses.dataclass(frozen=True)
class CadreDouble:
    """Double des paramètres du cadre (#97) : les deux tolérances, sans dimension."""

    tolerance_identite_pas: float = EPS
    tolerance_identite_cumulee: float = EPS


def etat_pays(identifiant="A", graine=1, t=0, registre=None, **positions):
    """État d'essai : V^flux = V^stock, registre stationnaire à π̄ = 2 % (ADR 0008, II.3)."""
    p = dict(OUVERTURE)
    p.update(positions)
    v = {cat.VALEUR_NETTE_FLUX[s]: idt.valeur_nette_stock(p, s) for s in cat.SECTEURS}
    if registre is None:
        registre = tuple(1.02 ** (-u / 12) for u in range(1, 14))
    return EtatPays(identifiant=identifiant, graine=graine, t=t, registre_prix=registre, **p, **v)


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

    etats = []
    for k in range(n):
        champs = {v.nom: (tuple(tirage() for _ in range(v.longueur)) if v.type is tuple
                          else int(rng.integers(0, 10**6)) if v.type is int else tirage())
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
    assert VERSION_SCHEMA == 1


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
    """ADR 0012, F2 et annotation du 07/10/2026 (point 2) : F2 complété de quatre unités, sans double."""
    f2 = ("pas par an", "pas par tour", "sans dimension", "u.m.", "u.m. par pas",
          "par an, taux de flux", "par an, taux de croissance", "années", "personnes", "fraction")
    complements = ("pas", "u.v.", "u.v. par pas", "u.m. par u.v.")
    assert unites.UNITES == f2 + complements
    assert len(set(unites.UNITES)) == len(unites.UNITES)
    assert {v.unite for v in VARIABLES} <= set(unites.UNITES)
    # Un seul vocabulaire : le schéma utilise celui de `unites`, il n'en a pas de copie.
    assert schema.UNITES is unites.UNITES


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
    # Décompte de l'état : 14 (empreinte) + 11 + 5 scalaires, aucun autre propriétaire au J2.
    assert {v.proprietaire for v in VARIABLES} == {"moteur", "noyau"}
    assert sum(v.longueur for v in VARIABLES) == 30


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


# Champs hors de leur domaine (B-5 ; décision du mainteneur du 07/10/2026,
# constats N-1 et N-2) : mêmes refus à la construction et à la reprise.
HORS_DOMAINE = [
    ("graine", -1, "graine négative"), ("graine", -(2**70), "graine négative"),
    ("graine", schema.GRAINE_EXCLUE, "≥ 2\\^64"), ("graine", 2**70, "≥ 2\\^64"),
    ("t", -1, "t négatif"), ("t", -(2**70), "t négatif"),
    ("identifiant", "", "identifiant vide"),
    ("identifiant", "\ud800", "UTF-8"), ("identifiant", "A\udfff", "UTF-8"),
    ("identifiant", "\x00", "contrôle"), ("identifiant", "A\x7fB", "contrôle"),
    ("identifiant", "A\x85", "contrôle"), ("identifiant", "\t", "contrôle"),
    ("identifiant", " A", "espace de bord"), ("identifiant", "A ", "espace de bord"),
    ("identifiant", "\u00a0A", "espace de bord"), ("identifiant", "A\u2028", "espace de bord"),
]


@pytest.mark.parametrize("champ, valeur, motif", HORS_DOMAINE)
def test_hors_domaine_refuse_a_la_construction(champ, valeur, motif):
    """Graine dans [0 ; 2^64[, t ≥ 0, identifiant non vide, UTF-8, sans contrôle ni espace de bord."""
    with pytest.raises(ValueError, match=f"EtatPays.{champ} : .*{motif}"):
        dataclasses.replace(etat_pays(), **{champ: valeur})


@pytest.mark.parametrize("champs", [
    {"graine": 0}, {"graine": schema.GRAINE_EXCLUE - 1}, {"graine": 2**63},
    {"t": 0}, {"t": 10**6},
    {"identifiant": "x"}, {"identifiant": "État-α"}, {"identifiant": "A B"},
    {"identifiant": "\U0001F30D"},
])
def test_valeurs_aux_bornes_du_domaine_admises(champs):
    """Les bornes incluses (0, 2^64 − 1) et les identifiants Unicode réguliers passent l'aller-retour."""
    e = dataclasses.replace(etat_pays(), **champs)
    assert all(getattr(e, nom) == valeur for nom, valeur in champs.items())
    assert charger(sauvegarder([e])) == (e,)


def test_bornes_declarees():
    """Bornes nommées : graine dans [0 ; 2^64[, t ≥ 0."""
    assert (schema.GRAINE_MINIMALE, schema.GRAINE_EXCLUE, schema.T_MINIMAL) == (0, 2**64, 0)


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
        e = dataclasses.replace(etat_pays(identifiant="B"), **{champ: valeur})
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
    assert lignes[:5] == ["{", ' "version": 1,', ' "pays": [', "  {", '   "identifiant": "État-α",']
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


@pytest.mark.parametrize("version", [0, 2, "1", 1.0, True, None])
def test_version_differente_refusee(version):
    with pytest.raises(SauvegardeRefusee, match="version") as refus:
        charger(document_modifie(remplacer("version", version)))
    assert refus.value.champ == "version"


def test_version_refusee_avant_tout_diagnostic_de_champ():
    """Une sauvegarde d'une autre version est refusée comme telle, même si ses champs diffèrent."""
    def modifier(racine):
        racine["version"] = 2
        racine["pays"][0]["champ_futur"] = 1.0
    with pytest.raises(SauvegardeRefusee, match="version"):
        charger(document_modifie(modifier))


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
    (b'{"version": 1}', "champ manquant"),
    (b'{"pays": []}', "champ manquant"),
    (b'{"version": 1, "pays": {}}', "liste des pays"),
    (b'{"version": 1, "pays": [3]}', "objet JSON"),
    (b'{"version": 1, "version": 1, "pays": []}', "clé en double"),
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
