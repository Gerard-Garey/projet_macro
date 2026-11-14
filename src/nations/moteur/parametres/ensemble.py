"""Ensemble immuable des tables de paramètres, passé à `assembler` et lu par la vue.

Contrat : ADR 0012, annotation du 13/11/2026, point 3.5 (décision du
mainteneur du 13/11/2026, P69). L'objet `parametres` passé à `assembler`
(signature inchangée) est un `EnsembleDesParametres` : un champ par table,
`cadre`, `production`, `travail`, `prix`, `investissement`, puis `banque` et
`banque_centrale` (ADR 0013, annotation du 14/11/2026, point 6 ; H3.5). Les blocs le
lisent par la vue (`vue.parametres.<radical>.<nom>`), jamais en important un
module de table, ce qui lirait la valeur indicative au lieu de celle du
scénario ; `executer_pas` passe `parametres.cadre` à `ouvrir_pas` (lettre de
A3.1). Module à part de `nations.moteur.parametres`, pour éviter le cycle avec
`__init__`.

`PARAMETRES_DE_REFERENCE` porte les tables de référence (valeurs
indicatives) ; une variation passe par `dataclasses.replace` sur l'ensemble et
par `nations.moteur.parametres.varier` sur une table, l'une et l'autre
contrôlées à la construction.
"""

from __future__ import annotations

from dataclasses import dataclass

from nations.moteur.diagnostics import DefautDeDeclaration
from nations.moteur.parametres.banque import BANQUE, TableBanque
from nations.moteur.parametres.banque_centrale import BANQUE_CENTRALE, TableBanqueCentrale
from nations.moteur.parametres.cadre import CADRE, Cadre
from nations.moteur.parametres.investissement import INVESTISSEMENT, TableInvestissement
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
    investissement: TableInvestissement
    banque: TableBanque
    banque_centrale: TableBanqueCentrale

    def __post_init__(self) -> None:
        for nom, attendu in (("cadre", Cadre), ("production", TableProduction),
                             ("travail", TableTravail), ("prix", TablePrix),
                             ("investissement", TableInvestissement), ("banque", TableBanque),
                             ("banque_centrale", TableBanqueCentrale)):
            valeur = getattr(self, nom)
            if type(valeur) is not attendu:
                raise DefautDeDeclaration(f"table {type(valeur).__name__} : {attendu.__name__} "
                                          "attendue", nom=nom)


PARAMETRES_DE_REFERENCE = EnsembleDesParametres(CADRE, PRODUCTION, TRAVAIL, PRIX, INVESTISSEMENT,
                                                BANQUE, BANQUE_CENTRALE)
