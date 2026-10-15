"""Catalogue du noyau comparé à la spécification (issue #95, critères 5, 8 et 9).

Contrat : ADR 0012, A1, A2 et A4. Le catalogue (`nations.noyau.catalogue`) est
comparé terme à terme à `tab:matrice-flux`, `tab:portes-monnaie` et
`tab:phases`, lues dans la spécification par le lecteur de
`outils/verifier_matrices.py` (fixture `matrices`). Les signatures (ΔM, ΔH) ne
sont pas saisies : elles sont dérivées du règlement par l'arbre des comptes,
et c'est la dérivation qui est comparée à la table.
"""

import re
from collections import Counter
from pathlib import Path

import pytest

from nations.noyau import catalogue as cat

RACINE = Path(__file__).resolve().parents[2]
SPEC = RACINE / "docs" / "specification" / "nations_et_marches.tex"

# Libellés de la colonne « Écrivent » de `tab:phases` → radicaux des blocs
# (ADR 0012, B1 : table de correspondance unique radical ↔ libellé).
RADICAUX = {
    "production": "production", "travail": "travail", "prix": "prix",
    "ménages": "menages", "investissement": "investissement", "banque": "banque",
    "banque centrale": "banque_centrale", "État": "finances_publiques",
}


@pytest.fixture(scope="module")
def tables(matrices):
    """Les trois tables lues dans la spécification, sans écart de lecture."""
    texte = matrices.preparer_tex(SPEC.read_text(encoding="utf-8"))
    lues = {}
    for label in (matrices.LABEL_FLUX, matrices.LABEL_PORTES, "tab:phases"):
        table, ecarts = matrices.lire_table(texte, label, "spec")
        assert table is not None and ecarts == [], (label, ecarts)
        lues[label] = table
    ecarts = []
    matrices.lire_termes(lues[matrices.LABEL_FLUX], ecarts)
    assert ecarts == []
    return lues


def termes_du_catalogue(matrices, ligne):
    """Cellules d'une ligne du catalogue : colonne → Counter de (signe, terme normalisé)."""
    cellules = {c: Counter() for c in cat.COLONNES}
    for terme in ligne.termes:
        cle = matrices.normaliser_terme(terme.ecriture)
        cellules[terme.colonne_plus][(1, cle)] += 1
        cellules[terme.colonne_moins][(-1, cle)] += 1
    return cellules


def test_vingt_huit_lignes_onze_postes_six_colonnes():
    assert len(cat.LIGNES) == 28
    assert len(set(cat.IDENTIFIANTS)) == 28
    assert len(cat.POSTES) == 11
    assert len(cat.COLONNES) == 6
    assert [ligne.identifiant for ligne in cat.CONTREPARTIES] == ["17", "20", "22"]


def test_catalogue_egal_a_la_matrice_des_flux(matrices, tables):
    """Terme à terme, ligne par ligne et colonne par colonne, dans l'ordre de la table."""
    flux = tables[matrices.LABEL_FLUX]
    entetes = [c.cle for c in flux.colonnes]
    assert entetes == ["menages", "entr. courant", "entr. capital", "banque", "bc", "etat"]
    assert [ligne.identifiant for ligne in flux.lignes] == list(cat.IDENTIFIANTS)
    for lue, ligne in zip(flux.lignes, cat.LIGNES, strict=True):
        attendues = termes_du_catalogue(matrices, ligne)
        for colonne, cellule in zip(cat.COLONNES, lue.cellules, strict=True):
            dans_la_table = Counter((t.signe, t.nom) for t in cellule.termes)
            assert dans_la_table == attendues[colonne], (ligne.identifiant, colonne)


def test_signatures_derivees_egales_aux_portes(matrices, tables):
    """Signatures (ΔM, ΔH) dérivées du règlement = `tab:portes-monnaie` ; montants = termes positifs."""
    portes = tables[matrices.LABEL_PORTES]
    assert [ligne.identifiant for ligne in portes.lignes] == list(cat.IDENTIFIANTS)
    for lue, ligne in zip(portes.lignes, cat.LIGNES, strict=True):
        montant, signe_m, signe_h = lue.cellules
        termes, erreur = matrices.lire_cellule(montant.texte)
        assert erreur is None
        assert Counter(cle for _, cle, _ in termes) == Counter(
            matrices.normaliser_terme(t.ecriture) for t in ligne.termes), ligne.identifiant
        assert all(signe == 1 for signe, _, _ in termes)
        sm, _ = matrices.lire_signe(signe_m.texte)
        sh, _ = matrices.lire_signe(signe_h.texte)
        if ligne.signature is None:
            assert (sm, sh) == (None, None), ligne.identifiant
        else:
            assert (sm, sh) == ligne.signature, ligne.identifiant


def lignes_de_la_cellule(texte):
    """Identifiants du catalogue désignés par une cellule « Lignes » de `tab:phases`."""
    texte = re.sub(r"au jalon J\d", "", texte)
    if texte.strip() == "aucune":
        return []
    bases = [i.split("-")[0] for i in cat.IDENTIFIANTS]
    trouves = []
    for morceau in re.split(r"[,;]", texte):
        morceau = morceau.strip()
        if not morceau:
            continue
        if " à " in morceau:
            debut, fin = (m.strip() for m in morceau.split(" à "))
            i, j = bases.index(debut), len(bases) - 1 - bases[::-1].index(fin)
            trouves.extend(cat.IDENTIFIANTS[i:j + 1])
        else:
            trouves.extend(i for i, b in zip(cat.IDENTIFIANTS, bases, strict=True) if b == morceau)
    return trouves


def phases_lues(matrices, tables):
    """Ligne → clôture, d'après la colonne « Lignes » de `tab:phases`."""
    table = tables["tab:phases"]
    colonnes = [c.cle for c in table.colonnes]
    rang = colonnes.index("lignes")
    phases = {}
    for lue in table.lignes:
        numero = lue.identifiant
        cellule = matrices.texte_simple(lue.cellules[rang].texte)
        if numero == "8":
            for sous, partie in zip("abc", cellule.split("puis"), strict=True):
                for identifiant in lignes_de_la_cellule(partie):
                    phases[identifiant] = "8" + sous
        else:
            for identifiant in lignes_de_la_cellule(cellule):
                phases[identifiant] = numero
    return phases


def test_phase_de_chaque_ligne_egale_a_tab_phases(matrices, tables):
    """Critère 5 : la colonne « phase » du catalogue est celle de `tab:phases`."""
    lues = phases_lues(matrices, tables)
    attendues = {ligne.identifiant: ligne.phase for ligne in cat.LIGNES if not ligne.contrepartie}
    assert lues == attendues
    # Les phases 1, 2 et 9 n'exécutent aucune ligne.
    for phase in ("1", "2", "9"):
        assert cat.LIGNES_DE_LA_PHASE[phase] == ()
    assert [p for p in cat.PHASES] == ["1", "2", "3", "4", "5", "6", "7", "8a", "8b", "8c", "9"]


def test_proposant_siege_dans_la_phase_de_sa_ligne(matrices, tables):
    """Le proposant au socle de chaque ligne est un écrivain de sa phase (`tab:phases`)."""
    table = tables["tab:phases"]
    rang = [c.cle for c in table.colonnes].index("ecrivent")
    ecrivains = {}
    for lue in table.lignes:
        cellule = matrices.texte_simple(lue.cellules[rang].texte)
        noms = set()
        for libelle, radical in RADICAUX.items():
            if re.search(r"(^|[ ,(])" + re.escape(libelle) + r"($|[ ,()])", cellule):
                noms.add(radical)
        ecrivains[lue.identifiant] = noms
    for ligne in cat.LIGNES:
        if ligne.proposant is None:
            continue
        assert ligne.proposant in ecrivains[ligne.phase[0]], ligne.identifiant


def test_contreparties_et_lignes_sans_proposant():
    """Critères 5 et 8 : 17, 20, 22 dérivées par le noyau ; 19b sans proposant au socle."""
    for ligne in cat.LIGNES:
        if ligne.identifiant in ("17", "20", "22"):
            assert ligne.contrepartie and ligne.phase is None and ligne.proposant is None
            assert all(t.poste_regle is not None and t.reglement == () for t in ligne.termes)
        else:
            assert not ligne.contrepartie
            assert all(t.poste_regle is None for t in ligne.termes)
        if ligne.identifiant.startswith("19b"):
            assert ligne.proposant is None and ligne.phase == "7"
    assert {i for i, ligne in cat.LIGNE.items() if ligne.resultat} == set(
        cat.IDENTIFIANTS[:cat.IDENTIFIANTS.index("16") + 1])


@pytest.mark.parametrize("payeur, beneficiaire, attendu", [
    ("menages", "etat", (("D_H", -1.0), ("Res", -1.0), ("M_G", 1.0))),
    ("etat", "entreprises", (("M_G", -1.0), ("Res", 1.0), ("D_F", 1.0))),
    ("banque", "etat", (("Res", -1.0), ("M_G", 1.0))),
    ("banque_centrale", "banque", (("Res", 1.0),)),
    ("banque_centrale", "menages", (("Res", 1.0), ("D_H", 1.0))),
    ("banque_centrale", "etat", (("M_G", 1.0),)),
    ("banque", "entreprises", (("D_F", 1.0),)),
    ("menages", "entreprises", (("D_H", -1.0), ("D_F", 1.0))),
    ("entreprises", "entreprises", ()),
])
def test_arbre_des_comptes(payeur, beneficiaire, attendu):
    """A4 : un paiement parcourt l'arbre des comptes (ADR 0012, exemples de A4)."""
    assert cat.chemin_de_reglement(payeur, beneficiaire) == attendu


def test_variations_d_instrument_coherentes_avec_les_signes():
    """Variation d'un actif détenu −, d'un passif émis + : coefficient opposé au signe du détenteur."""
    def colonne_de(secteur):
        # Les entreprises portent leurs variations de postes en sous-colonne capital.
        return "entreprises_capital" if secteur == "entreprises" else secteur

    verifiees = 0
    for ligne in cat.LIGNES:
        for terme in ligne.termes:
            cellules = {terme.colonne_plus: 1.0, terme.colonne_moins: -1.0}
            for poste, coef in terme.variations:
                p = cat.POSTE[poste]
                if colonne_de(p.detenteur) in cellules:
                    assert coef == -cellules[colonne_de(p.detenteur)], (ligne.identifiant, poste)
                else:
                    assert coef == cellules[colonne_de(p.emetteur)], (ligne.identifiant, poste)
                verifiees += 1
    # 3, 4, 8, 18 et 21 : un poste chacune ; 19a : trois lignes d'un poste ;
    # 19b : deux lignes de deux postes (titres cédés, titres acquis).
    assert verifiees == 12


@pytest.mark.parametrize("identifiant", [i for i in cat.IDENTIFIANTS
                                         if not cat.LIGNE[i].contrepartie])
@pytest.mark.parametrize("x", [-7.25, 3.5])
def test_portes_signees_par_ligne(identifiant, x):
    """Critère 9 : ΔM = Δ(D_H + D_F) et ΔH = ΔRes par ligne, montant signé, négatif compris.

    Le montant de la ligne est la somme signée de ses termes ; pour une ligne
    à un terme de valeur x < 0 (16, 18, 19a, 19b, 21 négatives), le
    règlement dérivé redonne la signature fois x, avec son signe.
    """
    ligne = cat.LIGNE[identifiant]
    montant = 0.0
    delta_m = 0.0
    delta_h = 0.0
    for terme in ligne.termes:
        montant += x
        for poste, coef in terme.reglement:
            if poste in cat.POSTES_MONNAIE:
                delta_m += coef * x
            if poste in cat.POSTES_MONNAIE_CENTRALE:
                delta_h += coef * x
    assert delta_m == ligne.signature[0] * montant
    assert delta_h == ligne.signature[1] * montant


def test_couples_du_montant_couvert():
    """A3.2 : liste fermée réduite à (16, finances_publiques), ligne à un terme."""
    assert cat.COUPLES_MONTANT_COUVERT == {("16", "finances_publiques")}
    for identifiant, _ in cat.COUPLES_MONTANT_COUVERT:
        assert len(cat.LIGNE[identifiant].termes) == 1
        assert cat.LIGNE[identifiant].phase == "8b"


def test_lignes_qui_admettent_un_negatif():
    """Liste fermée (ADR 0012, annotation du 07/10/2026, point 1), ligne 7 comprise, par ligne."""
    decidees = {i for i, ligne in cat.LIGNE.items() if ligne.admet_negatif and not ligne.contrepartie}
    assert decidees == {
        "4", "7", "9", "10", "11a", "11b", "11c", "12", "13", "16", "18",
        "19a-ménages", "19a-banque", "19a-BC", "19b-ménages", "19b-banque", "21"}
    assert {i for i, ligne in cat.LIGNE.items() if not ligne.admet_negatif} == {
        "1", "2", "3", "5", "6", "8", "14", "15"}


def test_signature_des_moyens_de_paiement_et_montant_couvert():
    """Lecture « poste » des contreparties : D_H, D_F font M ; Res fait H ; M^G ni l'un ni l'autre."""
    assert cat.SIGNATURE_DU_MOYEN == {"D_H": (1, 0), "D_F": (1, 0), "Res": (0, 1), "M_G": (0, 0)}
    assert cat.LIGNES_A_MONTANT_COUVERT == {"16"}
