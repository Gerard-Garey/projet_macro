"""Tests du script de concordance sur des dépôts fabriqués.

Chaque test construit, dans un dossier temporaire, une spécification et un
code minimaux, puis vérifie qu'un écart fabriqué est relevé par la règle
attendue du contrat (`docs/specification/CONVENTIONS.md`, § 9), et qu'un cas
conforme n'en relève aucun.
"""

import re
import textwrap

import pytest

PREAMBULE = r"""\documentclass{article}
\newcommand{\code}[1]{\texttt{\detokenize{#1}}}
\newcommand{\tracabilite}[3]{#1 #2 #3}
\begin{document}
"""

EQUATION = r"""
\begin{equation}\label{eq:prix-cout-unitaire}
  c = w / y
\end{equation}
\begin{lecture}[coût unitaire]
\variables $c$ : coût unitaire.
\sens Le coût unitaire rapporte le salaire à la production.
\hyp Rendements constants.
\limites Aucune.
\tracabilite{dérivée}{v1.5, éq. (21), § 6.2 ; décision M-3}{nations.blocs.prix.cout_unitaire}
\end{lecture}
Voir \code{nations.blocs.prix} et \code{outils/outil.py}.
"""

# Équation de EQUATION, sans son encadré (pour la remplacer par une autre forme).
EQUATION_SIMPLE = "\n\\begin{equation}\\label{eq:prix-cout-unitaire}\n  c = w / y\n\\end{equation}"
assert EQUATION_SIMPLE in EQUATION

PRIX = '''\
"""Bloc prix (fabriqué pour les tests)."""


def cout_unitaire(w, y):
    """Coût unitaire."""
    # eq:prix-cout-unitaire
    return w / y
'''


def fabriquer(racine, corps_tex=EQUATION, fichiers=None):
    """Crée un dépôt minimal sous `racine` et rend le chemin du `.tex`."""
    code = {
        "src/nations/__init__.py": '"""Paquet."""\n',
        "src/nations/blocs/__init__.py": '"""Blocs."""\n',
        "src/nations/blocs/prix.py": PRIX,
        "src/nations/moteur/__init__.py": '"""Moteur."""\n',
        "src/nations/moteur/parametres.py": "taux_marge = 0.2\n",
        "outils/outil.py": "def f():\n    return 1\n",
    }
    code.update(fichiers or {})
    for relatif, contenu in code.items():
        chemin = racine / relatif
        chemin.parent.mkdir(parents=True, exist_ok=True)
        if contenu is None:
            chemin.unlink(missing_ok=True)
        else:
            chemin.write_text(contenu, encoding="utf-8")
    tex = racine / "spec.tex"
    tex.write_text(PREAMBULE + corps_tex + "\n\\end{document}\n", encoding="utf-8")
    return tex


def verifier(concordance, racine, tex):
    return concordance.verifier(tex, racine, racine / "src", racine / "outils")


def regles(rapport):
    return sorted({e.regle for e in rapport.ecarts})


def test_cas_conforme_sans_ecart(concordance, tmp_path):
    tex = fabriquer(tmp_path)
    rapport = verifier(concordance, tmp_path, tex)
    assert rapport.ecarts == []
    assert (rapport.nb_labels, rapport.nb_balises, rapport.nb_lectures) == (1, 1, 1)


def test_depot_vide_sans_ecart(concordance, tmp_path):
    # État du squelette : aucune équation, aucune balise.
    tex = fabriquer(tmp_path, corps_tex="Squelette.", fichiers={"src/nations/blocs/prix.py": None})
    rapport = verifier(concordance, tmp_path, tex)
    assert rapport.ecarts == []
    assert (rapport.nb_labels, rapport.nb_balises) == (0, 0)


def test_label_sans_balise(concordance, tmp_path):
    prix = PRIX.replace("    # eq:prix-cout-unitaire\n", "")
    tex = fabriquer(tmp_path, fichiers={"src/nations/blocs/prix.py": prix})
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [1]
    assert "aucune balise" in rapport.ecarts[0].message


def test_balise_sans_label(concordance, tmp_path):
    prix = PRIX + "\n\ndef marge():\n    # eq:prix-marge\n    return 0.2\n"
    tex = fabriquer(tmp_path, fichiers={"src/nations/blocs/prix.py": prix})
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [1]
    assert "eq:prix-marge" in rapport.ecarts[0].message
    assert "sans label" in rapport.ecarts[0].message


def test_balise_en_double(concordance, tmp_path):
    prix = PRIX + "\n\ndef autre():\n    # eq:prix-cout-unitaire\n    return 1\n"
    tex = fabriquer(tmp_path, fichiers={"src/nations/blocs/prix.py": prix})
    rapport = verifier(concordance, tmp_path, tex)
    # La seconde balise est aussi hors de la fonction citée par \tracabilite
    # (règle 5).
    assert regles(rapport) == [1, 5]
    assert any("2 fois dans src/" in e.message for e in rapport.ecarts if e.regle == 1)


def test_label_en_double(concordance, tmp_path):
    double = EQUATION + "\n\\begin{equation}\\label{eq:prix-cout-unitaire}\n  x\n\\end{equation}\n"
    tex = fabriquer(tmp_path, corps_tex=double)
    rapport = verifier(concordance, tmp_path, tex)
    assert 1 in regles(rapport)
    assert any("2 fois dans la spécification" in e.message for e in rapport.ecarts)


def test_code_inexistant(concordance, tmp_path):
    corps = EQUATION + "\nVoir \\code{nations.blocs.prix.fonction_absente}.\n"
    tex = fabriquer(tmp_path, corps_tex=corps)
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [5]
    assert "fonction_absente" in rapport.ecarts[0].message


@pytest.mark.parametrize(
    "nom",
    [
        "nations.moteur.parametres.taux_marge",
        "nations.blocs.prix.cout_unitaire",
        "nations.blocs",
        "outils/outil.py",
        "outils.outil.f",
    ],
)
def test_code_existant(concordance, tmp_path, nom):
    tex = fabriquer(tmp_path, corps_tex=EQUATION + f"\n\\code{{{nom}}}\n")
    assert verifier(concordance, tmp_path, tex).ecarts == []


def test_code_hors_de_src_et_outils(concordance, tmp_path):
    tex = fabriquer(tmp_path, corps_tex=EQUATION + "\n\\code{spec.tex}\n\\code{spec/../spec.tex}\n")
    assert regles(verifier(concordance, tmp_path, tex)) == [5]


def test_format_de_label_invalide(concordance, tmp_path):
    corps = EQUATION.replace("eq:prix-cout-unitaire", "eq:prix_cout")
    prix = PRIX.replace("eq:prix-cout-unitaire", "eq:prix_cout")
    tex = fabriquer(tmp_path, corps_tex=corps, fichiers={"src/nations/blocs/prix.py": prix})
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [2]
    assert all("format invalide" in e.message for e in rapport.ecarts)


def test_radical_sans_module(concordance, tmp_path):
    corps = EQUATION.replace("eq:prix-cout-unitaire", "eq:salaires-cout-unitaire")
    prix = PRIX.replace("eq:prix-cout-unitaire", "eq:salaires-cout-unitaire")
    tex = fabriquer(tmp_path, corps_tex=corps, fichiers={"src/nations/blocs/prix.py": prix})
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [2]
    assert all("radical" in e.message for e in rapport.ecarts)


def test_equation_numerotee_sans_label(concordance, tmp_path):
    corps = EQUATION + "\n\\begin{equation}\n  x = 1\n\\end{equation}\n\\begin{equation*}\n  y\n\\end{equation*}\n"
    tex = fabriquer(tmp_path, corps_tex=corps)
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [3]
    assert len(rapport.ecarts) == 1


def test_rubriques_de_lecture_dans_le_desordre(concordance, tmp_path):
    # \hyp avant \sens.
    corps = EQUATION.replace("\\sens Le coût", "\\hyp Le coût").replace("\\hyp Rendements", "\\sens Rendements")
    tex = fabriquer(tmp_path, corps_tex=corps)
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [3]
    assert any("ordre" in e.message for e in rapport.ecarts)


def test_rubrique_de_lecture_absente(concordance, tmp_path):
    tex = fabriquer(tmp_path, corps_tex=EQUATION.replace("\\limites Aucune.\n", ""))
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [3]
    assert "\\limites présent 0 fois" in rapport.ecarts[0].message


def test_statut_et_decision_de_tracabilite(concordance, tmp_path):
    corps = EQUATION.replace("{dérivée}", "{probable}").replace("décision M-3", "sans décision")
    tex = fabriquer(tmp_path, corps_tex=corps)
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [4]
    assert len(rapport.ecarts) == 2


def test_decision_sans_tiret_admise(concordance, tmp_path):
    # La feuille de route numérote les décisions M1, M2… : forme admise.
    tex = fabriquer(tmp_path, corps_tex=EQUATION.replace("M-3", "M16"))
    assert verifier(concordance, tmp_path, tex).ecarts == []


def test_tracabilite_qui_ne_porte_pas_la_balise(concordance, tmp_path):
    corps = EQUATION.replace("{nations.blocs.prix.cout_unitaire}", "{nations.moteur.parametres}")
    tex = fabriquer(tmp_path, corps_tex=corps)
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [5]
    assert "ne contient pas la balise" in rapport.ecarts[0].message


def test_tracabilite_au_module_admise(concordance, tmp_path):
    corps = EQUATION.replace("{nations.blocs.prix.cout_unitaire}", "{\\code{nations.blocs.prix}}")
    tex = fabriquer(tmp_path, corps_tex=corps)
    assert verifier(concordance, tmp_path, tex).ecarts == []


def numeros_releves(concordance, tmp_path, phrase):
    tex = fabriquer(tmp_path, corps_tex=EQUATION + "\n" + phrase + "\n")
    rapport = verifier(concordance, tmp_path, tex)
    assert set(regles(rapport)) <= {6}
    return [re.search(r"\(\d+\)", e.message).group(0) for e in rapport.ecarts]


def test_numero_en_dur(concordance, tmp_path):
    assert numeros_releves(concordance, tmp_path, "D'après (12), on a $f^{(2)}$.") == ["(12)"]


def test_enumeration_entre_parentheses_relevee(concordance, tmp_path):
    # Une énumération s'écrit avec enumerate, pas en dur.
    assert numeros_releves(concordance, tmp_path, "(1) épargner ; (2) investir.") == ["(1)", "(2)"]


def test_annee_de_citation_admise(concordance, tmp_path):
    phrase = "Godley et Lavoie (2007) ; Tobin (1969) ; mais (2100) et (999) relevés."
    assert numeros_releves(concordance, tmp_path, phrase) == ["(2100)", "(999)"]


def test_citation_archivee_exemptee(concordance, tmp_path):
    phrase = "Voir v1.5, éq. (41) et (43), v1.5, éq.~(35), § 8.1, et v2.0, éq. (7)."
    assert numeros_releves(concordance, tmp_path, phrase) == []


def test_mention_d_archive_sans_citation_exacte_relevee(concordance, tmp_path):
    phrase = "Comme en v2.0, la règle (12) s'applique ; v1.5 (3)."
    assert numeros_releves(concordance, tmp_path, phrase) == ["(12)", "(3)"]


def test_parametre_de_calibration_hors_moteur(concordance, tmp_path):
    table = textwrap.dedent(r"""
        \begin{longtable}{ll}
        \label{tab:calibration}
        \code{nations.moteur.parametres.taux_marge} & 0,2 \\
        \code{nations.blocs.prix.cout_unitaire} & 1 \\
        \end{longtable}
        """)
    tex = fabriquer(tmp_path, corps_tex=EQUATION + table)
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [7]
    assert len(rapport.ecarts) == 1


def test_commentaires_et_docstrings_ignores(concordance, tmp_path):
    # Un label en commentaire LaTeX n'est pas un label ; une mention de
    # « # eq: » dans une docstring n'est pas une balise.
    corps = EQUATION + "\n% \\label{eq:prix-fantome} \\code{absent}\n50\\% de (7) % (8)\n"
    prix = PRIX.replace('"""Coût unitaire."""', '"""Porte la balise # eq:prix-fantome."""')
    tex = fabriquer(tmp_path, corps_tex=corps, fichiers={"src/nations/blocs/prix.py": prix})
    rapport = verifier(concordance, tmp_path, tex)
    # Seul « (7) », hors commentaire, est relevé.
    assert regles(rapport) == [6]
    assert len(rapport.ecarts) == 1


def test_specification_introuvable(concordance, tmp_path):
    fabriquer(tmp_path)
    rapport = verifier(concordance, tmp_path, tmp_path / "absent.tex")
    assert any("introuvable" in e.message for e in rapport.ecarts)


def test_code_de_sortie(concordance, tmp_path, capsys):
    tex = fabriquer(tmp_path)
    options = ["--tex", str(tex), "--racine", str(tmp_path)]
    assert concordance.main(options + ["--strict"]) == 0
    (tmp_path / "src/nations/blocs/prix.py").write_text(PRIX.replace("# eq:", "# "), encoding="utf-8")
    assert concordance.main(options) == 0
    assert concordance.main(options + ["--strict"]) == 1
    assert "aucune balise" in capsys.readouterr().out


def test_balise_a_plusieurs_dieses_comptee(concordance, tmp_path):
    prix = PRIX.replace("    # eq:prix-cout-unitaire", "    ## eq:prix-cout-unitaire")
    tex = fabriquer(tmp_path, fichiers={"src/nations/blocs/prix.py": prix})
    rapport = verifier(concordance, tmp_path, tex)
    assert rapport.ecarts == [] and rapport.nb_balises == 1
    # Comptée pour l'unicité : une seconde balise fait un doublon.
    prix += "\n\ndef marge():\n    #eq:prix-cout-unitaire\n    return 1\n"
    tex = fabriquer(tmp_path, fichiers={"src/nations/blocs/prix.py": prix})
    rapport = verifier(concordance, tmp_path, tex)
    assert any("2 fois dans src/" in e.message for e in rapport.ecarts)


def test_balise_en_fin_de_ligne_relevee(concordance, tmp_path):
    prix = PRIX.replace("    # eq:prix-cout-unitaire\n    return w / y",
                        "    return w / y  # eq:prix-cout-unitaire")
    tex = fabriquer(tmp_path, fichiers={"src/nations/blocs/prix.py": prix})
    rapport = verifier(concordance, tmp_path, tex)
    assert rapport.nb_balises == 1
    assert regles(rapport) == [1]
    assert "fin de ligne" in rapport.ecarts[0].message


def test_verbatim_et_iffalse_ignores(concordance, tmp_path):
    corps = EQUATION + textwrap.dedent(r"""
        \begin{verbatim}
        \label{eq:prix-fantome} \code{absent} (12)
        \end{verbatim}
        \verb|\code{absent2}| et \verb+(13)+
        \iffalse
        \label{eq:prix-fantome2} \ifx\a\b (14) \fi \code{absent3}
        \fi
        Après le bloc, (15) est relevé.
        """)
    tex = fabriquer(tmp_path, corps_tex=corps)
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [6]
    assert len(rapport.ecarts) == 1 and "(15)" in rapport.ecarts[0].message
    # Les numéros de ligne sont conservés après effacement.
    attendu = (PREAMBULE + corps).split("\n").index("Après le bloc, (15) est relevé.") + 1
    assert rapport.ecarts[0].emplacement.endswith(f":{attendu}")


def test_align_ne_compte_que_les_lignes_de_niveau_superieur(concordance, tmp_path):
    align = textwrap.dedent(r"""
        \begin{align}\label{eq:prix-cout-unitaire}
          c &= \begin{cases} a & \text{si } x \\ b & \text{sinon} \end{cases}
             + \begin{pmatrix} 1 \\ 2 \end{pmatrix} + {x \\ y}
        \end{align}""")
    corps = EQUATION.replace(EQUATION_SIMPLE, align)
    tex = fabriquer(tmp_path, corps_tex=corps)
    assert verifier(concordance, tmp_path, tex).ecarts == []


def test_align_a_deux_lignes_et_un_label(concordance, tmp_path):
    align = textwrap.dedent(r"""
        \begin{align}\label{eq:prix-cout-unitaire}
          c &= w \\
          d &= y \notag \\
          e &= z
        \end{align}""")
    corps = EQUATION.replace(EQUATION_SIMPLE, align)
    tex = fabriquer(tmp_path, corps_tex=corps)
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [3]
    assert "1 label(s) pour 2 ligne(s)" in rapport.ecarts[0].message


def test_equation_labellisee_sans_lecture(concordance, tmp_path):
    # Deux équations labellisées, un seul encadré, placé après la seconde.
    premiere = "\n\\begin{equation}\\label{eq:prix-marge}\n  m = 0\n\\end{equation}\n"
    prix = PRIX + "\n\ndef marge():\n    # eq:prix-marge\n    return 0\n"
    tex = fabriquer(tmp_path, corps_tex=premiere + EQUATION,
                    fichiers={"src/nations/blocs/prix.py": prix})
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [8]
    assert rapport.ecarts[0].emplacement.endswith(":6")
