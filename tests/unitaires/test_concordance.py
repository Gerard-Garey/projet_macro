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


# Tableau des décisions de la feuille de route (règle 4) : M3 et M16 existent.
FEUILLE_DE_ROUTE = """# Feuille de route

## 4. Décisions du mainteneur

| N° | Date | Décision | Trace |
|---|---|---|---|
| M3 | 29/09/2026 | Décision fabriquée. | ADR |
| M16 | 29/09/2026 | Décision fabriquée. | ADR |
"""


def fabriquer(racine, corps_tex=EQUATION, fichiers=None):
    """Crée un dépôt minimal sous `racine` et rend le chemin du `.tex`."""
    code = {
        "src/nations/__init__.py": '"""Paquet."""\n',
        "src/nations/blocs/__init__.py": '"""Blocs."""\n',
        "src/nations/blocs/prix.py": PRIX,
        "src/nations/moteur/__init__.py": '"""Moteur."""\n',
        "src/nations/moteur/parametres.py": "taux_marge = 0.2\n",
        "outils/outil.py": "def f():\n    return 1\n",
        "docs/feuille-de-route.md": FEUILLE_DE_ROUTE,
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
    # Le module qui contient la balise est admis, écrit en nom nu.
    corps = EQUATION.replace("{nations.blocs.prix.cout_unitaire}", "{nations.blocs.prix}")
    tex = fabriquer(tmp_path, corps_tex=corps)
    assert verifier(concordance, tmp_path, tex).ecarts == []


def test_tracabilite_avec_code_refusee(concordance, tmp_path):
    # \tracabilite enveloppe déjà son troisième argument dans \code.
    corps = EQUATION.replace("{nations.blocs.prix.cout_unitaire}", "{\\code{nations.blocs.prix}}")
    tex = fabriquer(tmp_path, corps_tex=corps)
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [5]
    assert len(rapport.ecarts) == 1
    assert "enveloppe déjà son troisième argument dans \\code" in rapport.ecarts[0].message


@pytest.mark.parametrize(
    "provenance",
    ["v1.5 ; décision~M-3", "choix du mainteneur (M16)", "(M-3)", "Décision M3 et décision M16"],
)
def test_decision_existante_admise(concordance, tmp_path, provenance):
    tex = fabriquer(tmp_path, corps_tex=EQUATION.replace("v1.5, éq. (21), § 6.2 ; décision M-3", provenance))
    assert verifier(concordance, tmp_path, tex).ecarts == []


@pytest.mark.parametrize(
    ("provenance", "fragment"),
    [
        # Mention nue d'un numéro existant : pas une décision citée.
        ("agrégat M2 de la v1.5", "aucune décision citée"),
        ("agrégat M3 de la v1.5", "aucune décision citée"),
        # Forme reconnue, numéro absent du tableau des décisions.
        ("décision M-99", "M99 absente"),
        ("(M2)", "M2 absente"),
    ],
)
def test_decision_absente_ou_mal_citee_relevee(concordance, tmp_path, provenance, fragment):
    tex = fabriquer(tmp_path, corps_tex=EQUATION.replace("v1.5, éq. (21), § 6.2 ; décision M-3", provenance))
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [4]
    assert len(rapport.ecarts) == 1 and fragment in rapport.ecarts[0].message


def test_feuille_de_route_absente_relevee(concordance, tmp_path):
    tex = fabriquer(tmp_path, fichiers={"docs/feuille-de-route.md": None})
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [4]
    assert len(rapport.ecarts) == 1 and "feuille de route introuvable" in rapport.ecarts[0].message


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


def test_exposant_et_indice_exemptes_mais_pas_une_accolade_seule(concordance, tmp_path):
    phrase = "Dérivée f^(2), g_(3), h^{(4)}, k_{(5)} ; mais \\textbf{(6)} et \\emph{(7)} relevés."
    assert numeros_releves(concordance, tmp_path, phrase) == ["(6)", "(7)"]


def test_numero_en_mode_mathematique_ignore(concordance, tmp_path):
    phrase = textwrap.dedent(r"""
        On a $f(2) = K(0)$, $$g(3)$$, \(h(4)\) et \[k(5)\].
        \begin{align*} x(6) \\ y(7) \end{align*}
        \begin{equation*} z(8) \end{equation*}
        Hors mode mathématique : 10\$ (9) \$ puis (10), et \\[2pt] (11).
        """)
    assert numeros_releves(concordance, tmp_path, phrase) == ["(9)", "(10)", "(11)"]


def test_multline_porte_un_seul_label(concordance, tmp_path):
    multline = textwrap.dedent(r"""
        \begin{multline}\label{eq:prix-cout-unitaire}
          c = w \\
            + y \\
            + z
        \end{multline}""")
    corps = EQUATION.replace(EQUATION_SIMPLE, multline)
    tex = fabriquer(tmp_path, corps_tex=corps)
    assert verifier(concordance, tmp_path, tex).ecarts == []
    # Sans label, un seul écart, quel que soit le nombre de lignes.
    sans_label = EQUATION + multline.replace("\\label{eq:prix-cout-unitaire}", "")
    rapport = verifier(concordance, tmp_path, fabriquer(tmp_path, corps_tex=sans_label))
    assert regles(rapport) == [3]
    assert len(rapport.ecarts) == 1
    assert "0 label(s) pour 1 ligne(s)" in rapport.ecarts[0].message


@pytest.mark.parametrize("marque", ["\\nonumber", "\\notag"])
@pytest.mark.parametrize("nom", ["equation", "multline"])
def test_equation_non_numerotee_sans_label_admise(concordance, tmp_path, marque, nom):
    corps = EQUATION + f"\n\\begin{{{nom}}}\n  x = 1 {marque}\n\\end{{{nom}}}\n"
    tex = fabriquer(tmp_path, corps_tex=corps)
    assert verifier(concordance, tmp_path, tex).ecarts == []


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


def ecarts_de_regle_3(concordance, racine, corps):
    """Écarts de règle 3 relevés sur une spécification fabriquée."""
    rapport = verifier(concordance, racine, fabriquer(racine, corps_tex=corps))
    return [e for e in rapport.ecarts if e.regle == 3]


@pytest.mark.parametrize("marque", ["\\nonumber", "\\notag"])
def test_label_sur_equation_non_numerotee_releve(concordance, tmp_path, marque):
    # Issue #12, premier cas : le label pointe sur un autre compteur.
    equation = EQUATION_SIMPLE.replace("c = w / y", f"c = w / y {marque}")
    ecarts = ecarts_de_regle_3(concordance, tmp_path, EQUATION.replace(EQUATION_SIMPLE, equation))
    assert len(ecarts) == 1
    assert "eq:prix-cout-unitaire sur une ligne non numérotée (equation" in ecarts[0].message


def test_label_sur_ligne_d_align_non_numerotee_releve(concordance, tmp_path):
    # Issue #12, deuxième cas : une ligne numérotée, deux labels dont l'un
    # sur la ligne marquée \notag.
    align = textwrap.dedent(r"""
        \begin{align}
          c &= w \label{eq:prix-cout-unitaire} \\
          d &= y \notag \label{eq:prix-marge}
        \end{align}""")
    prix = PRIX + "\n\ndef marge():\n    # eq:prix-marge\n    return 0\n"
    tex = fabriquer(tmp_path, corps_tex=EQUATION.replace(EQUATION_SIMPLE, align),
                    fichiers={"src/nations/blocs/prix.py": prix})
    ecarts = [e for e in verifier(concordance, tmp_path, tex).ecarts if e.regle == 3]
    assert len(ecarts) == 1
    assert "eq:prix-marge sur une ligne non numérotée (align" in ecarts[0].message


def test_label_deplace_sur_la_ligne_non_numerotee_releve(concordance, tmp_path):
    # Issue #12, constat d'audit : autant de labels que de lignes numérotées,
    # mais le label est sur la ligne \notag et la ligne numérotée n'en a pas.
    # La comparaison des totaux ne le voit pas ; le contrôle ligne par ligne
    # relève l'écart et le manque.
    align = textwrap.dedent(r"""
        \begin{align}
          c &= w \\
          d &= y \notag \label{eq:prix-cout-unitaire}
        \end{align}""")
    ecarts = ecarts_de_regle_3(concordance, tmp_path, EQUATION.replace(EQUATION_SIMPLE, align))
    messages = [e.message for e in ecarts]
    assert len(messages) == 2
    assert any("eq:prix-cout-unitaire sur une ligne non numérotée (align" in m for m in messages)
    assert any("sans label eq: (0 label(s) pour 1 ligne(s)" in m for m in messages)


def test_second_label_sur_une_ligne_d_align_releve(concordance, tmp_path):
    align = textwrap.dedent(r"""
        \begin{align}
          c &= w \label{eq:prix-cout-unitaire}\label{eq:prix-marge}
        \end{align}""")
    prix = PRIX + "\n\ndef marge():\n    # eq:prix-marge\n    return 0\n"
    tex = fabriquer(tmp_path, corps_tex=EQUATION.replace(EQUATION_SIMPLE, align),
                    fichiers={"src/nations/blocs/prix.py": prix})
    ecarts = [e for e in verifier(concordance, tmp_path, tex).ecarts if e.regle == 3]
    assert len(ecarts) == 1
    assert "eq:prix-marge en excès" in ecarts[0].message


def test_second_label_dans_une_equation_releve(concordance, tmp_path):
    # Issue #12, troisième cas : deux labels pour un seul numéro.
    equation = EQUATION_SIMPLE.replace(
        "\\label{eq:prix-cout-unitaire}", "\\label{eq:prix-cout-unitaire}\\label{eq:prix-marge}",
    )
    ecarts = ecarts_de_regle_3(concordance, tmp_path, EQUATION.replace(EQUATION_SIMPLE, equation))
    assert len(ecarts) == 1
    assert "eq:prix-marge en excès" in ecarts[0].message


def test_equation_labellisee_sans_lecture(concordance, tmp_path):
    # Deux équations labellisées, un seul encadré, placé après la seconde.
    premiere = "\n\\begin{equation}\\label{eq:prix-marge}\n  m = 0\n\\end{equation}\n"
    prix = PRIX + "\n\ndef marge():\n    # eq:prix-marge\n    return 0\n"
    tex = fabriquer(tmp_path, corps_tex=premiere + EQUATION,
                    fichiers={"src/nations/blocs/prix.py": prix})
    rapport = verifier(concordance, tmp_path, tex)
    assert regles(rapport) == [8]
    assert rapport.ecarts[0].emplacement.endswith(":6")


# Issue #8 : faux négatifs de la préparation du texte. Chaque cas place, après
# le passage à effacer, un numéro en dur (15) que la règle 6 doit relever :
# s'il ne l'est pas, la suite du document a été effacée sans écart.


def releves(rapport):
    """Numéros en dur relevés par la règle 6."""
    return sorted(re.findall(r"\(\d+\)", " ".join(
        e.message for e in rapport.ecarts if e.regle == 6)))


def test_iffalse_ignore_les_conditions_etoolbox(concordance, tmp_path):
    # \ifbool et \iftoggle (etoolbox) sont des commandes, pas des conditions :
    # le \fi qui suit ferme le \iffalse.
    corps = EQUATION + textwrap.dedent(r"""
        \iffalse
        \ifbool{brouillon}{(12)}{} \iftoggle{notes}{(13)}{}
        \fi
        Après le bloc, (15) est relevé.
        """)
    rapport = verifier(concordance, tmp_path, fabriquer(tmp_path, corps_tex=corps))
    assert regles(rapport) == [6] and releves(rapport) == ["(15)"]


def test_iffalse_ignore_ifdef_et_ifstrequal(concordance, tmp_path):
    corps = EQUATION + textwrap.dedent(r"""
        \iffalse
        \ifdef{\brouillon}{(12)}{} \ifdefmacro{\a}{}{} \ifstrequal{a}{b}{(13)}{}
        \fi
        Après le bloc, (15) est relevé.
        """)
    rapport = verifier(concordance, tmp_path, fabriquer(tmp_path, corps_tex=corps))
    assert regles(rapport) == [6] and releves(rapport) == ["(15)"]


def test_iffalse_newif_dans_le_bloc_ne_declare_rien(concordance, tmp_path):
    # Dans un bloc sauté, \newif n'est pas exécuté : \ifbrouillon n'est pas
    # une condition, et le \fi ferme le \iffalse.
    corps = EQUATION + textwrap.dedent(r"""
        \iffalse
        \newif\ifbrouillon (12)
        \fi
        Après le bloc, (15) est relevé.
        """)
    rapport = verifier(concordance, tmp_path, fabriquer(tmp_path, corps_tex=corps))
    assert regles(rapport) == [6] and releves(rapport) == ["(15)"]


def test_iffalse_condition_declaree_par_newif_comptee(concordance, tmp_path):
    # Déclarée hors du bloc, \ifbrouillon est une condition : son \fi ne ferme
    # pas le \iffalse, et (14) reste dans le bloc.
    corps = EQUATION + textwrap.dedent(r"""
        \newif\ifbrouillon
        \iffalse
        \ifbrouillon (13) \fi (14) \ifnum1=1 \fi
        \fi
        Après le bloc, (15) est relevé.
        """)
    rapport = verifier(concordance, tmp_path, fabriquer(tmp_path, corps_tex=corps))
    assert regles(rapport) == [6] and releves(rapport) == ["(15)"]


def test_iffalse_non_referme_est_un_ecart(concordance, tmp_path):
    corps = EQUATION + textwrap.dedent(r"""
        \iffalse
        \ifx\a\b (14) \fi
        Plus loin, (15) est relevé.
        """)
    rapport = verifier(concordance, tmp_path, fabriquer(tmp_path, corps_tex=corps))
    # Rien n'est effacé : la suite est analysée.
    assert regles(rapport) == [0, 6] and releves(rapport) == ["(14)", "(15)"]
    ecart = next(e for e in rapport.ecarts if e.regle == 0)
    assert "\\iffalse non refermé" in ecart.message
    attendu = (PREAMBULE + corps).split("\n").index("\\iffalse") + 1
    assert ecart.emplacement.endswith(f":{attendu}")


def test_saut_de_ligne_suivi_de_iffalse_n_ouvre_rien(concordance, tmp_path):
    # `\\iffalse` est un saut de ligne suivi du mot « iffalse » : aucun bloc
    # n'est ouvert, donc aucun écart de règle 0, et (15) est analysé.
    corps = EQUATION + textwrap.dedent(r"""
        Une ligne\\iffalse puis la suite : (15) est relevé.
        """)
    rapport = verifier(concordance, tmp_path, fabriquer(tmp_path, corps_tex=corps))
    assert regles(rapport) == [6] and releves(rapport) == ["(15)"]


def test_saut_de_ligne_suivi_de_fi_ne_ferme_pas_le_bloc(concordance, tmp_path):
    # Dans un bloc, `A\\fi B` est un saut de ligne suivi du mot « fi » : le
    # bloc reste ouvert jusqu'au vrai \fi, et (14) est effacé. Avec un nombre
    # impair de barres, `\\\fi` est un saut de ligne suivi de \fi.
    corps = EQUATION + textwrap.dedent(r"""
        \iffalse
        A\\fi B (14)
        \fi
        Après le bloc, (15) est relevé.
        \iffalse (16) \\\fi
        Après le second bloc, (17) est relevé.
        """)
    rapport = verifier(concordance, tmp_path, fabriquer(tmp_path, corps_tex=corps))
    assert regles(rapport) == [6] and releves(rapport) == ["(15)", "(17)"]


def test_iffalse_condition_declaree_par_newif_entre_accolades(concordance, tmp_path):
    # `\newif{\ifbrouillon}` déclare la condition comme `\newif\ifbrouillon` :
    # son \fi ne ferme pas le \iffalse, et (14) reste dans le bloc.
    corps = EQUATION + textwrap.dedent(r"""
        \newif{\ifbrouillon}
        \iffalse
        \ifbrouillon (13) \fi (14)
        \fi
        Après le bloc, (15) est relevé.
        """)
    rapport = verifier(concordance, tmp_path, fabriquer(tmp_path, corps_tex=corps))
    assert regles(rapport) == [6] and releves(rapport) == ["(15)"]


def test_iffalse_branche_else_composee(concordance, tmp_path):
    # Issue #32, cas 1 : TeX compose la branche \else d'un \iffalse. Seul le
    # texte jusqu'au \else est effacé ; un \else d'une condition imbriquée
    # (\ifnum) reste dans le bloc. La branche \else est relue au niveau
    # supérieur : un \iffalse qu'elle contient ouvre un bloc.
    corps = EQUATION + textwrap.dedent(r"""
        \iffalse (12) \ifnum1=1 (13) \else (14) \fi \else Composé : (15). \fi
        \iffalse (16) \else (17) \iffalse (18) \fi \fi
        Après les blocs, (19) est relevé.
        """)
    rapport = verifier(concordance, tmp_path, fabriquer(tmp_path, corps_tex=corps))
    assert regles(rapport) == [6] and releves(rapport) == ["(15)", "(17)", "(19)"]


def test_iffalse_cite_par_let_n_ouvre_rien(concordance, tmp_path):
    # Issue #32, cas 2 : `\let\ifbrouillon\iffalse` ne fait que copier le
    # jeton \iffalse ; il n'ouvre pas de bloc jusqu'au \fi suivant. Le signe
    # `=` et les espaces sont admis, et `\global\let` est un \let.
    corps = EQUATION + textwrap.dedent(r"""
        \let\ifbrouillon\iffalse
        Entre les deux, (13) est relevé.
        \ifbrouillon Y\fi
        \let\ifnotes = \iffalse \global\let\ifannexe\iffalse
        Plus loin, (15) est relevé. \ifnotes Z\fi
        """)
    rapport = verifier(concordance, tmp_path, fabriquer(tmp_path, corps_tex=corps))
    assert regles(rapport) == [6] and releves(rapport) == ["(13)", "(15)"]


def test_iffalse_dans_une_definition_n_ouvre_rien(concordance, tmp_path):
    # Issue #32, cas 2 : le corps d'une définition n'est pas exécuté quand
    # elle est lue ; un \iffalse qu'il contient n'ouvre pas de bloc.
    corps = EQUATION + textwrap.dedent(r"""
        \newcommand{\debutcache}{\iffalse}
        Après \newcommand, (12) est relevé.
        \renewcommand*\debutcache[1][x]{\iffalse #1}
        Après \renewcommand, (13) est relevé.
        \providecommand{\autre}{\iffalse}
        Après \providecommand, (14) est relevé.
        \def\cacher#1{\iffalse #1} \gdef\cachertout{\iffalse}
        Après \def et \gdef, (15) est relevé.
        \newcommand{\fincache}{\fi}
        \iffalse (16) \fi
        Après le bloc qui suit les définitions, (17) est relevé.
        """)
    rapport = verifier(concordance, tmp_path, fabriquer(tmp_path, corps_tex=corps))
    assert regles(rapport) == [6]
    assert releves(rapport) == ["(12)", "(13)", "(14)", "(15)", "(17)"]


def test_retirer_iffalse_cas_de_l_issue_32(concordance):
    # Cas mesurés dans l'issue #32 (appel direct) : le label reste visible.
    for texte in (r"A \iffalse X \else \label{eq:b} \fi C",
                  "\\let\\ifbrouillon\\iffalse\n\\label{eq:b}\n\\ifbrouillon Y\\fi",
                  "\\newcommand{\\debut}{\\iffalse}\n\\label{eq:b}\n\\newcommand{\\fin}{\\fi}"):
        rendu, anomalies = concordance.retirer_iffalse(texte)
        assert "\\label{eq:b}" in rendu and anomalies == []
        assert rendu.count("\n") == texte.count("\n")
    rendu, _ = concordance.retirer_iffalse(r"A \iffalse X \else \label{eq:b} \fi C")
    assert "X" not in rendu


def test_copie_de_iffalse_par_let_compte_dans_un_bloc(concordance):
    # Comme TeX, `\let\ifbrouillon\iffalse` fait de \ifbrouillon une
    # condition : dans un bloc, son \else ne ferme pas le bloc et son \fi
    # est apparié ; le \fi suivant ferme le bloc.
    texte = (r"\let\ifbrouillon\iffalse \iffalse \ifbrouillon A \else B=\label{eq:b} "
             r"\fi C=\label{eq:c} \fi D")
    rendu, anomalies = concordance.retirer_iffalse(texte)
    assert rendu.split() == [r"\let\ifbrouillon\iffalse", "D"] and anomalies == []


def test_copie_de_iffalse_par_let_ouvre_un_bloc(concordance):
    # La copie ouvre un bloc comme \iffalse ; le \iffalse cité par \let,
    # lui, n'en ouvre pas. Une copie de copie et une condition déclarée
    # (\newif) copiée par \let se comportent comme leur cible, et un \let
    # vers une commande ordinaire retire la nature de condition.
    texte = "\n".join([
        r"\let\ifbrouillon\iffalse \ifbrouillon \label{eq:cache}\fi D",
        r"\let\ifnotes=\ifbrouillon \ifnotes \label{eq:cache2}\fi E",
        r"\newif\ifannexe \let\ifcopie\ifannexe \iffalse \ifcopie\fi \label{eq:cache3}\fi F",
        r"\let\ifnotes\relax \ifnotes \label{eq:vu}\fi G",
    ])
    rendu, anomalies = concordance.retirer_iffalse(texte)
    assert "cache" not in rendu and anomalies == []
    assert r"\label{eq:vu}" in rendu
    assert [m for m in "DEFG" if m in rendu.split()] == list("DEFG")
    assert rendu.count("\n") == texte.count("\n")


def test_iffalse_dans_un_environnement_n_ouvre_rien(concordance):
    # Les deux corps de \newenvironment et \renewenvironment (étoilés ou
    # non, arguments optionnels) ne sont pas exécutés à la lecture.
    for texte in ("\\newenvironment{cache}{\\iffalse}{}\n\\label{eq:b}\n\\fi",
                  "\\renewenvironment*{cache}[1][x]{\\iffalse #1}{\\iffalse}\n\\label{eq:b}\n\\fi",
                  "\\newenvironment{cache}{}{\\iffalse}\n\\label{eq:b}\n\\fi"):
        rendu, anomalies = concordance.retirer_iffalse(texte)
        assert "\\label{eq:b}" in rendu and anomalies == [], texte


def test_branche_else_sans_fi_est_un_ecart(concordance, tmp_path):
    # La branche \else d'un \iffalse attend son \fi : sans lui, le bloc
    # n'est pas refermé, rien n'est effacé et c'est un écart (règle 0).
    rendu, anomalies = concordance.retirer_iffalse(r"A \iffalse X \else Y")
    assert rendu == r"A \iffalse X \else Y"
    assert anomalies == [(2, "\\iffalse non refermé (aucun \\fi apparié) : "
                             "la suite est analysée")]
    # Le \fi d'une condition composée dans la branche ne la ferme pas.
    _, anomalies = concordance.retirer_iffalse(r"\iffalse X \else \ifnum1=1 Y\fi")
    assert len(anomalies) == 1
    corps = EQUATION + textwrap.dedent(r"""
        \iffalse (14) \else
        Plus loin, (15) est relevé.
        """)
    rapport = verifier(concordance, tmp_path, fabriquer(tmp_path, corps_tex=corps))
    assert regles(rapport) == [0, 6] and releves(rapport) == ["(14)", "(15)"]


def test_verbatim_cite_en_commentaire(concordance, tmp_path):
    # Le commentaire est ouvert avant le \begin{verbatim} qu'il cite : il
    # n'ouvre rien, et le texte jusqu'au vrai verbatim reste analysé.
    corps = EQUATION + textwrap.dedent(r"""
        % Exemple : \begin{verbatim} ouvre un verbatim.
        Entre les deux, (15) est relevé.
        \begin{verbatim}
        (16) % \end{verbatim} n'est pas un commentaire
        \end{verbatim}
        Ni \verb|%| ni \% n'ouvre de commentaire : (17) est relevé.
        """)
    rapport = verifier(concordance, tmp_path, fabriquer(tmp_path, corps_tex=corps))
    assert regles(rapport) == [6] and releves(rapport) == ["(15)", "(17)"]
