"""Ensemble immuable des tables de paramètres, passé à `assembler` et lu par la vue.

Contrat : ADR 0012, annotation du 13/11/2026, point 3.5 (décision du
mainteneur du 13/11/2026, P69). L'objet `parametres` passé à `assembler`
(signature inchangée) est un `EnsembleDesParametres` : un champ par table,
`cadre`, `production`, `travail`, `prix`, `menages`, `investissement`, puis `banque` et
`banque_centrale` (ADR 0013, annotation du 14/11/2026, point 6 ; H3.5 ; `menages` entre
`prix` et `investissement` : annotation du 14/11/2026 (rang 1b de J3-d1), point 2). Les blocs le
lisent par la vue (`vue.parametres.<radical>.<nom>`), jamais en important un
module de table, ce qui lirait la valeur indicative au lieu de celle du
scénario ; `executer_pas` passe `parametres.cadre` à `ouvrir_pas` (lettre de
A3.1). Module à part de `nations.moteur.parametres`, pour éviter le cycle avec
`__init__`.

**Condition jointe entre tables** (annotation du 14/11/2026 (rang 1b de J3-d1), point 2 ;
`sec:menages-conditions`) : le coefficient de richesse λ_H/n_a + ν_H λ_H π^{∗,pas} > γ^e,
qui lit les tables des ménages, de la production, du travail et de la banque centrale, est
contrôlé à toute construction de l'ensemble, sur le paramètre π* (valeur initiale de la cible,
BC4 à levier fermé) ; les facteurs passent par `facteur_par_pas` et λ_H par `par_pas` (F2,
conversion unique), sous la forme de Γ^e du moteur, f(g_pr) f(g_N) f(π*). Refus
(`DefautDeDeclaration`), jamais écrêtage. Au J4, le domaine du levier de cible prend le relais
(G4).

`PARAMETRES_DE_REFERENCE` porte les tables de référence (valeurs
indicatives) ; une variation passe par `dataclasses.replace` sur l'ensemble et
par `nations.moteur.parametres.varier` sur une table, l'une et l'autre
contrôlées à la construction.
"""

from __future__ import annotations

from dataclasses import dataclass

from nations.moteur.conversions import facteur_par_pas, par_pas
from nations.moteur.diagnostics import DefautDeDeclaration
from nations.moteur.parametres.banque import BANQUE, TableBanque
from nations.moteur.parametres.banque_centrale import (
    BANQUE_CENTRALE,
    TableBanqueCentrale,
)
from nations.moteur.parametres.cadre import CADRE, Cadre
from nations.moteur.parametres.investissement import INVESTISSEMENT, TableInvestissement
from nations.moteur.parametres.menages import MENAGES, TableMenages
from nations.moteur.parametres.prix import PRIX, TablePrix
from nations.moteur.parametres.production import PRODUCTION, TableProduction
from nations.moteur.parametres.travail import TRAVAIL, TableTravail


@dataclass(frozen=True, slots=True)
class EnsembleDesParametres:
    """Les tables de paramètres du moteur, une par champ, chacune de son type exact."""

    cadre: Cadre
    production: TableProduction
    travail: TableTravail
    prix: TablePrix
    menages: TableMenages
    investissement: TableInvestissement
    banque: TableBanque
    banque_centrale: TableBanqueCentrale

    def __post_init__(self) -> None:
        for nom, attendu in (("cadre", Cadre), ("production", TableProduction),
                             ("travail", TableTravail), ("prix", TablePrix),
                             ("menages", TableMenages),
                             ("investissement", TableInvestissement), ("banque", TableBanque),
                             ("banque_centrale", TableBanqueCentrale)):
            valeur = getattr(self, nom)
            if type(valeur) is not attendu:
                raise DefautDeDeclaration(f"table {type(valeur).__name__} : {attendu.__name__} "
                                          "attendue", nom=nom)
        coefficient = coefficient_de_richesse(self)
        if not coefficient > 0.0:
            raise DefautDeDeclaration(
                f"coefficient de richesse λ_H/n_a + ν_H λ_H π^{{∗,pas}} − γ^e = {coefficient!r} : "
                "> 0 attendu (sec:menages-conditions ; C^règle ≥ 0 quand YD^e ≥ 0) : refusé, "
                "jamais écrêté", nom="lambda_H")


def coefficient_de_richesse(parametres: EnsembleDesParametres) -> float:
    """λ_H/n_a + ν_H λ_H π^{∗,pas} − γ^e, par pas, sans dimension, sur le paramètre π* de la
    table du bloc 8 (`sec:menages-conditions`) : π^{∗,pas} = f(π*) − 1 et
    γ^e = f(g_pr) f(g_N) f(π*) − 1, f = `facteur_par_pas`, forme de Γ^e du moteur ; positif
    dans le domaine."""
    menages = parametres.menages
    facteur_cible = facteur_par_pas(parametres.banque_centrale.pi_etoile)
    gamma_e = (facteur_par_pas(parametres.production.g_pr)
               * facteur_par_pas(parametres.travail.g_N) * facteur_cible - 1.0)
    lambda_H_pas = par_pas(menages.lambda_H)
    return (lambda_H_pas + menages.nu_H * menages.lambda_H.valeur * (facteur_cible - 1.0)
            - gamma_e)


PARAMETRES_DE_REFERENCE = EnsembleDesParametres(CADRE, PRODUCTION, TRAVAIL, PRIX, MENAGES,
                                                INVESTISSEMENT, BANQUE, BANQUE_CENTRALE)
