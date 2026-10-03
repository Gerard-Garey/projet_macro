"""Tests du script de vérification des matrices (issue #19).

Contrat : convention d'écriture des matrices, `docs/blocs/temps_comptabilite.md`
§ 9.7. La fixture `donnees/matrices_conformes.tex` écrit les trois tables selon
la convention complète (lignes 11, 19a et 19b scindées, colonne « Réel »,
valeurs nettes développées, `tab:portes-monnaie`) ; chaque test y fabrique un
écart et vérifie qu'il est relevé, avec son point, son `fichier:ligne` et le
code de sortie attendu, ou qu'un cas conforme n'en relève aucun.
"""

from pathlib import Path

import pytest

DONNEES = Path(__file__).resolve().parent / "donnees"
CONFORME = (DONNEES / "matrices_conformes.tex").read_text(encoding="utf-8")


def ecrire(tmp_path, texte, nom="spec.tex"):
    chemin = tmp_path / nom
    chemin.write_text(texte, encoding="utf-8")
    return chemin


def muter(avant, apres):
    """Fixture conforme où `avant` (présent une seule fois) devient `apres`."""
    assert CONFORME.count(avant) == 1, avant
    return CONFORME.replace(avant, apres)


def ligne_de(texte, extrait):
    """Numéro de ligne (à partir de 1) de la première occurrence d'`extrait`."""
    return texte[:texte.index(extrait)].count("\n") + 1


def executer(matrices, chemin, capsys, strict=True):
    code = matrices.main((["--strict"] if strict else []) + [str(chemin)])
    return code, capsys.readouterr().out


# --------------------------------------------------------------------------
# Cas conformes
# --------------------------------------------------------------------------


def test_fixture_conforme_sans_ecart(matrices, tmp_path, capsys):
    code, sortie = executer(matrices, ecrire(tmp_path, CONFORME), capsys)
    assert code == 0, sortie
    assert "Aucun écart." in sortie
    # Décomptes : lignes, colonnes hors étiquette, termes.
    assert "tab:matrice-bilans : 9 lignes, 6 colonnes" in sortie
    assert "tab:matrice-flux : 28 lignes, 6 colonnes" in sortie
    assert "tab:portes-monnaie : 28 lignes, 3 colonnes" in sortie


def test_identite_delta_res_banque_et_banque_centrale(matrices, tmp_path):
    """Point (c) : ΔRes tiré de la colonne banque = ΔRes tiré de la colonne BC."""
    texte = matrices.preparer_tex(CONFORME)
    flux, ecarts = matrices.lire_table(texte, matrices.LABEL_FLUX, "spec.tex")
    matrices.lire_termes(flux, ecarts)
    reglement = matrices.postes_de_reglement(flux, ecarts)
    assert ecarts == []
    assert reglement["banque"] == reglement["banque_centrale"]
    # Le paiement de l'État à la banque (ligne 2) crée des réserves ; le
    # versement du résultat de la BC (ligne 16) n'y figure pas.
    assert reglement["banque"]["G"] == 1
    assert "\\Pi^{CB}" not in reglement["banque"]


def test_normalisation_des_termes(matrices):
    n = matrices.normaliser_terme
    assert n("B_{H}") == n("B_H")
    assert n(r"\Delta\, \mathit{Res}") == n(r"\Delta Res") == n(r"\Delta \mathrm{Res}")
    assert n("i_{D} D_{H}") == n("i_D D_H")
    assert n("B_{Bk}") != n("B_{CB}")


def test_aucune_matrice_trouvee(matrices, tmp_path, capsys):
    tex = ecrire(tmp_path, "\\documentclass{article}\n\\begin{document}\nTexte.\n\\end{document}\n")
    code, sortie = executer(matrices, tex, capsys)
    assert code == 0
    assert "aucune matrice trouvée" in sortie


def test_specification_reelle(matrices, capsys):
    """La spécification passe en `--strict`.

    Avant #18, elle ne contient pas les tables : le script le dit (« aucune
    matrice trouvée ») sans échouer.
    """
    code, sortie = executer(matrices, matrices.TEX_DEFAUT, capsys)
    assert code == 0, sortie
    assert "aucune matrice trouvée" in sortie or "Aucun écart." in sortie


def test_specification_reelle_porte_les_trois_tables(matrices, capsys):
    """La spécification contient les trois tables et passe en `--strict`."""
    texte = matrices.TEX_DEFAUT.read_text(encoding="utf-8")
    for label in matrices.LABELS:
        assert f"\\label{{{label}}}" in texte, label
    code, sortie = executer(matrices, matrices.TEX_DEFAUT, capsys)
    assert code == 0, sortie
    assert "Aucun écart." in sortie


def test_pieds_de_page_ignores(matrices, tmp_path, capsys):
    """Les zones `\\endfoot` et `\\endlastfoot` ne sont ni données ni en-tête."""
    assert "\\endfoot" in CONFORME and "\\endlastfoot" in CONFORME
    code, sortie = executer(matrices, ecrire(tmp_path, CONFORME), capsys)
    assert code == 0, sortie
    # Pied à cellules (`&`), sous `\\endlastfoot` seul : ignoré lui aussi.
    texte = muter("\\bottomrule\n\\endlastfoot",
                  "\\midrule\nFin & & & & & & \\\\\n\\bottomrule\n\\endlastfoot")
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys)
    assert code == 0, sortie
    assert "tab:matrice-flux : 28 lignes, 6 colonnes" in sortie


def test_note_de_tete_repetee_ignoree(matrices, tmp_path, capsys):
    """Tête répétée précédée d'une note d'une cellule : note ignorée, en-tête comparé."""
    note = "\\endfirsthead\n\\multicolumn{7}{l}{\\emph{Suite de la page précédente}}\\\\\n"
    assert CONFORME.count(note) == 1
    code, sortie = executer(matrices, ecrire(tmp_path, CONFORME), capsys)
    assert code == 0, sortie
    assert "en-tête répété" not in sortie
    # Une ligne à plusieurs cellules différente du premier en-tête reste relevée.
    avant = note + "\\toprule\n\\textbf{Poste} & \\textbf{Ménages}"
    texte = muter(avant, avant.replace("\\textbf{Ménages}", "\\textbf{Foyers}"))
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys)
    assert code == 1
    ligne = ligne_de(texte, "\\textbf{Poste} & \\textbf{Foyers}")
    assert (f"[structure] {tmp_path / 'spec.tex'}:{ligne} : tab:matrice-bilans : en-tête "
            "répété différent du premier en-tête") in sortie
    assert "1 écart(s)" in sortie


# --------------------------------------------------------------------------
# Écarts
# --------------------------------------------------------------------------


def test_ligne_desequilibree(matrices, tmp_path, capsys):
    avant = r"Réserves & & & $+\mathit{Res}$ & $-\mathit{Res}$"
    texte = muter(avant, r"Réserves & & & $+\mathit{Res}$ & $+\mathit{Res}$")
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys)
    assert code == 1
    ligne = ligne_de(texte, "Réserves &")
    assert f"[a] {tmp_path / 'spec.tex'}:{ligne} : tab:matrice-bilans, ligne « Réserves »" in sortie
    assert "2 fois en +, 0 fois en −" in sortie
    # La colonne de la banque centrale n'est plus nulle non plus (point (b)).
    assert "[b]" in sortie and "colonne « Banque centrale »" in sortie


def test_sans_strict_code_0(matrices, tmp_path, capsys):
    texte = muter(r"$-\mathit{Res}$ & & \\", r"$+\mathit{Res}$ & & \\")
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys, strict=False)
    assert code == 0
    assert "écart(s)" in sortie


def test_cellule_mal_formee(matrices, tmp_path, capsys):
    """Une somme factorisée est refusée : la cellule doit être développée."""
    texte = muter(r"& $-\Delta B_H^{\mathrm{sec}}$ & \\", r"& $-(\Delta B_H^{\mathrm{sec}})$ & \\")
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys)
    assert code == 1
    ligne = ligne_de(texte, "19b-ménages Achats")
    assert f"[format] {tmp_path / 'spec.tex'}:{ligne} : tab:matrice-flux, ligne « 19b-ménages" in sortie
    assert "« ( » interdit" in sortie
    assert "non vérifié : (c) et (d)" in sortie


def test_terme_sans_signe(matrices, tmp_path, capsys):
    texte = muter("1 Consommation & $-C$", "1 Consommation & $C$")
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys)
    assert code == 1
    assert f"[format] {tmp_path / 'spec.tex'}:{ligne_de(texte, '1 Consommation')}" in sortie
    assert "terme sans signe explicite" in sortie


def test_cellule_hors_mode_mathematique(matrices, tmp_path, capsys):
    texte = muter("1 Consommation & $-C$", "1 Consommation & -C")
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys)
    assert code == 1
    assert "hors du mode mathématique" in sortie


def test_agregat_dans_une_cellule(matrices, tmp_path, capsys):
    """ΔD au lieu de ΔD_H + ΔD_F : la ligne 17 n'est plus nulle terme à terme."""
    texte = muter(r"$+\Delta D_H + \Delta D_F$ & & \\", r"$+\Delta D$ & & \\")
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys)
    assert code == 1
    ligne = ligne_de(texte, "17 $\\Delta$ Dépôts")
    assert f"[a] {tmp_path / 'spec.tex'}:{ligne} : tab:matrice-flux, ligne « 17 Δ Dépôts »" in sortie
    assert "non vérifié : (c) et (d) : lignes non nulles" in sortie


def test_poste_de_reglement_hors_de_sa_colonne(matrices, tmp_path, capsys):
    """ΔRes porté par l'État au lieu de la banque : ligne nulle, mais point (c)."""
    avant = r"20 $\Delta$ Réserves & & & & $-\Delta \mathit{Res}$ & $+\Delta \mathit{Res}$ & \\"
    apres = r"20 $\Delta$ Réserves & & & & & $+\Delta \mathit{Res}$ & $-\Delta \mathit{Res}$\\"
    code, sortie = executer(matrices, ecrire(tmp_path, muter(avant, apres)), capsys)
    assert code == 1
    assert "[c]" in sortie
    assert "colonne banque : le poste de règlement \\Delta Res y apparaît 0 fois" in sortie
    assert "[a]" not in sortie


def test_signature_fausse(matrices, tmp_path, capsys):
    """Ligne 9 déclarée + dans ΔM : ΔM recomposé ≠ ΔD_H + ΔD_F (point (d))."""
    texte = muter("9 & $+i_L L$ & $-$ & 0", "9 & $+i_L L$ & $+$ & 0")
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys)
    assert code == 1
    assert "[d]" in sortie and "ΔM ; terme « i_L L » : coefficient +1 dans ΔM recomposé" in sortie


def test_sens_de_ligne_inverse_releve_par_les_portes(matrices, tmp_path, capsys):
    """Ligne 12 inversée : lignes et ΔRes restent cohérents, seul (d) la relève."""
    avant = r"$+i_{res} \mathit{Res}$ & $-i_{res} \mathit{Res}$"
    apres = r"$-i_{res} \mathit{Res}$ & $+i_{res} \mathit{Res}$"
    code, sortie = executer(matrices, ecrire(tmp_path, muter(avant, apres)), capsys)
    assert code == 1
    assert "1 écart(s)" in sortie
    assert "[d]" in sortie and "ΔH ; terme « i_{res} \\mathit{Res} »" in sortie


def test_montant_faux(matrices, tmp_path, capsys):
    texte = muter("7 & $+T_H + T_F$", "7 & $+T_H$")
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys)
    assert code == 1
    ligne = ligne_de(texte, "7 & $+T_H$")
    assert f"[d] {tmp_path / 'spec.tex'}:{ligne} : tab:portes-monnaie, ligne « 7 » : le montant" in sortie


def test_ligne_absente_des_portes(matrices, tmp_path, capsys):
    texte = muter("16 & $+\\Pi^{CB}$ & 0 & 0\\\\\n", "")
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys)
    assert code == 1
    assert "ligne « 16 » absente de tab:portes-monnaie" in sortie


def test_colonne_sigma_refusee(matrices, tmp_path, capsys):
    avant = "& \\textbf{État}\\\\\n\\midrule\n\\endfirsthead\n\\toprule\n\\textbf{Ligne}"
    apres = "& \\textbf{État} & $\\Sigma$\\\\\n\\midrule\n\\endfirsthead\n\\toprule\n\\textbf{Ligne}"
    code, sortie = executer(matrices, ecrire(tmp_path, muter(avant, apres)), capsys)
    assert code == 1
    assert "les colonnes Σ sont supprimées" in sortie


def test_table_partielle(matrices, tmp_path, capsys):
    """Une table présente sans les deux autres : les absentes sont des écarts."""
    debut = CONFORME.index("\\begin{longtable}{lllllll}\n\\caption{Matrice des flux")
    fin = CONFORME.index("\\end{document}")
    code, sortie = executer(matrices, ecrire(tmp_path, CONFORME[:debut] + CONFORME[fin:]), capsys)
    assert code == 1
    assert "table tab:matrice-flux absente" in sortie
    assert "table tab:portes-monnaie absente" in sortie


@pytest.mark.parametrize("cellule", ["$+D_H +$", "$+D_H = B$", "$+\\frac{D}{2}$"])
def test_cellules_refusees(matrices, cellule):
    termes, erreur = matrices.lire_cellule(cellule)
    assert termes == [] and erreur is not None


@pytest.mark.parametrize("cellule", ["$+x^-1$", "$+x_-1$", "$+x^ - 1$", "$+i_{res}^+R$"])
def test_exposant_signe_sans_accolades(matrices, cellule):
    """`x^-1` se lirait comme deux termes `+x^` et `-1` : refusé."""
    termes, erreur = matrices.lire_cellule(cellule)
    assert termes == []
    assert erreur is not None and "exposant ou indice signé sans accolades" in erreur


def test_exposant_signe_entre_accolades(matrices):
    termes, erreur = matrices.lire_cellule("$+x^{-1} - B_{H}$")
    assert erreur is None
    assert [(s, n) for s, n, _ in termes] == [(1, "x^{-1}"), (-1, "B_H")]


def test_poste_hors_des_lignes_17_et_20(matrices, tmp_path, capsys):
    texte = muter("9 & $+i_L L$ & $-$ & 0", "9 & $+i_L L$ & poste & 0")
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys)
    assert code == 1
    ligne = ligne_de(texte, "9 & $+i_L L$")
    assert (f"[format] {tmp_path / 'spec.tex'}:{ligne} : tab:portes-monnaie, ligne « 9 » : "
            "« poste » réservé aux lignes 17 et 20") in sortie


@pytest.mark.parametrize("ident, avant", [
    ("17", "17 & $+\\Delta D_H + \\Delta D_F$ & poste"),
    ("20", "20 & $+\\Delta \\mathit{Res}$ & poste"),
])
def test_poste_montant_vide_refuse(matrices, tmp_path, capsys, ident, avant):
    """Le montant s'écrit toujours, lignes « poste » comprises."""
    texte = muter(avant, f"{ident} & & poste")
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys)
    assert code == 1
    ligne = ligne_de(texte, f"{ident} & & poste")
    assert (f"[d] {tmp_path / 'spec.tex'}:{ligne} : tab:portes-monnaie, ligne « {ident} » : "
            "montant vide") in sortie
    assert "1 écart(s)" in sortie


def test_montant_vide_refuse(matrices, tmp_path, capsys):
    texte = muter("9 & $+i_L L$ & $-$ & 0", "9 & & $-$ & 0")
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys)
    assert code == 1
    assert "ligne « 9 » : montant vide" in sortie


def test_poste_montant_ecrit_verifie(matrices, tmp_path, capsys):
    texte = muter("20 & $+\\Delta \\mathit{Res}$ & poste", "20 & $+\\Delta L$ & poste")
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys)
    assert code == 1
    ligne = ligne_de(texte, "20 & $+\\Delta L$")
    assert (f"[d] {tmp_path / 'spec.tex'}:{ligne} : tab:portes-monnaie, ligne « 20 » : "
            "le montant n'est pas") in sortie


@pytest.mark.parametrize("ident, avant, apres, colonne", [
    ("17", "17 & $+\\Delta D_H + \\Delta D_F$ & poste & poste",
     "17 & $+\\Delta D_H + \\Delta D_F$ & poste & $+$", "$+$"),
    ("17", "17 & $+\\Delta D_H + \\Delta D_F$ & poste & poste",
     "17 & $+\\Delta D_H + \\Delta D_F$ & 0 & poste", "0"),
    ("20", "20 & $+\\Delta \\mathit{Res}$ & poste & poste",
     "20 & $+\\Delta \\mathit{Res}$ & poste & 0", "0"),
])
def test_poste_exige_sur_les_lignes_17_et_20(matrices, tmp_path, capsys, ident, avant,
                                            apres, colonne):
    """Lignes 17 et 20 : les deux signes sont « poste » (§ 9.7, point 5)."""
    texte = muter(avant, apres)
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys)
    assert code == 1
    ligne = ligne_de(texte, apres)
    assert (f"[format] {tmp_path / 'spec.tex'}:{ligne} : tab:portes-monnaie, ligne « {ident} » : "
            f"« poste » exigé sur les lignes 17 et 20 (postes de règlement), lu « {colonne} »"
            ) in sortie
    assert "1 écart(s)" in sortie


def test_iffalse_non_referme_est_un_ecart_sans_effacer_les_tables(matrices, tmp_path, capsys):
    """Issue #8 : un `\\iffalse` sans `\\fi` apparié est un écart et n'efface plus la suite.

    `\\ifx` est une condition primitive : le `\\fi` lui revient, le `\\iffalse` reste ouvert.
    """
    texte = muter("\\begin{document}", "\\begin{document}\n\\iffalse \\ifx\\a\\b \\fi")
    code, sortie = executer(matrices, ecrire(tmp_path, texte), capsys)
    assert code == 1
    ligne = ligne_de(texte, "\\iffalse")
    assert (f"1. [structure] {tmp_path / 'spec.tex'}:{ligne} : \\iffalse non refermé "
            "(aucun \\fi apparié) : la suite est analysée") in sortie
    assert "1 écart(s)" in sortie
    # Les tables qui suivent sont lues.
    assert "tab:matrice-bilans : 9 lignes, 6 colonnes" in sortie
    assert "tab:portes-monnaie : 28 lignes, 3 colonnes" in sortie
