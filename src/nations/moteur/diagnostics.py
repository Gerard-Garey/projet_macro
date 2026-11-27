"""Diagnostics d'arrêt du moteur : des exceptions typées, à champs structurés.

Contrat : ADR 0012, B3, B4 et F1 ; même forme que les diagnostics du noyau
(`nations.noyau.diagnostics`, A6). Deux familles, dérivées de `ArretMoteur` :

- `DefautDeDeclaration`, levée **avant le premier pas** : déclaration d'un
  paramètre hors de son domaine ou de son vocabulaire (F1, F2), déclaration
  de bloc refusée par le contrôle statique de l'assemblage (B3) ;
- `RefusDuMoteur`, levée **au moment de l'appel**, pendant un pas : écriture
  d'une variable du pas non déclarée ou déjà écrite, lecture d'une variable
  non déclarée ou non encore écrite, lecture du montant exécuté d'une ligne
  non déclarée (#100), écriture d'une variable d'état hors de
  son propriétaire, de sa phase ou de son type, variable d'état non écrite à
  la couche moteur de la phase 9, entrées du tour non déclarées (B4, C2, B5) ;
  sa dérivée `PlanHorsDomaine` refuse un plan écrit hors de son domaine
  (`DOMAINES_DU_PAS` de l'ordonnanceur ; ADR 0013, annotation du 14/11/2026
  (J3-d1), point 4 ; P120, P129, #124) ; sa dérivée `EntreeHorsDomaine` refuse une entrée de
  scénario publiée hors de son domaine (`DOMAINES_DES_ENTREES` ; P138) ; sa dérivée
  `DepassementNumerique` traduit le dépassement de la double précision d'une règle de bloc
  (`OverflowError` de `math.exp`, S2, S3 et S6 du bloc 6 ; P139) ; sa dérivée `DivisionParZero`
  traduit une division par un zéro de la double précision (`ZeroDivisionError` ; ADR 0016,
  point 10.1 ; #158). Ces deux traductions forment une liste fermée : aucune autre exception
  n'est traduite.

Le moteur ne rattrape jamais un arrêt pour continuer, ni du noyau ni le sien :
l'état d'ouverture reste intact (gelé), et aucun état t + 1 n'est rendu.
"""

from __future__ import annotations


class ArretMoteur(Exception):
    """Arrêt du moteur, avec ses champs structurés.

    Champs : pas `t` ; `etape` (phase ou sous-phase : `"8b"`) ; `bloc`
    (radical de l'écrivain, `moteur` compris) ; `nom` (variable, paramètre,
    ligne ou lecture en cause). Un champ sans objet vaut `None`.
    """

    def __init__(
        self,
        message: str,
        *,
        t: int | None = None,
        etape: str | None = None,
        bloc: str | None = None,
        nom: str | None = None,
    ) -> None:
        self.t = t
        self.etape = etape
        self.bloc = bloc
        self.nom = nom
        self.message = message
        super().__init__(self._composer())

    def _composer(self) -> str:
        """Message en français qui nomme le pas, l'étape, le bloc et le nom renseignés."""
        parties = []
        if self.t is not None:
            parties.append(f"pas {self.t}")
        if self.etape is not None:
            parties.append(f"phase {self.etape}")
        if self.bloc is not None:
            parties.append(f"bloc {self.bloc}")
        if self.nom is not None:
            parties.append(f"« {self.nom} »")
        tete = ", ".join(parties)
        return f"{tete} : {self.message}" if tete else self.message


class DefautDeDeclaration(ArretMoteur):
    """Déclaration refusée avant le premier pas : paramètre (F1) ou assemblage (B3)."""


class RefusDuMoteur(ArretMoteur):
    """Refus levé au moment de l'appel, pendant un pas (B4, C2, B5)."""


class PlanHorsDomaine(RefusDuMoteur):
    """Plan d'un acheteur (`C_plan`, `I_plan`, `G_plan`) écrit hors de son domaine : non fini
    (NaN, ±∞) ou négatif ; −0,0 est admis (ADR 0013, annotation du 14/11/2026 (J3-d1),
    point 4 ; P120, P129, #124).

    Levé par l'espace du pas à l'écriture, quel que soit l'écrivain, avant le refus générique
    de finitude ; jamais d'écrêtage. Champs : pas, étape et bloc écrivain (passés par tout
    appelant de `VariablesDuPas.ecrire`, où ils sont obligatoires : la vue pour un bloc, le
    moteur pour lui-même ; #137), nom du plan ; la valeur et la condition sont dans le message.
    """


class EntreeHorsDomaine(RefusDuMoteur):
    """Entrée de scénario du tour (ς_{L,t}) publiée hors de son domaine, [0 ; 1] pour une part
    refusée : NaN, ±∞ compris (P138, sur le modèle de `PlanHorsDomaine`, P129).

    Levé par le moteur à la publication en phase 0, avant le refus générique de finitude ;
    jamais d'écrêtage. Champs : pas, étape « 0 », bloc « moteur », nom de l'entrée ; la valeur
    et la condition sont dans le message. Dérivée de `RefusDuMoteur` : le refus a lieu au
    moment de l'appel, pendant un pas (contrat « refus à l'appel » inchangé), et le type
    distinct permet au test et au diagnostic de le séparer d'une entrée non déclarée.
    """


class DepassementNumerique(RefusDuMoteur):
    """Dépassement de la double précision dans une méthode d'étape d'un bloc
    (`OverflowError`, levée par `math.exp` au-delà d'un argument d'environ 709 ; S2, S3 et S6 du
    bloc 6 ; P139).

    Levé par le moteur, qui traduit l'exception de l'arithmétique en refus typé à l'appel du
    bloc : champs pas, étape, bloc (radical de la méthode appelée) ; l'exception d'origine est
    chaînée. Ce n'est pas un rattrapage : le pas s'arrête comme pour tout `RefusDuMoteur`.
    """


class DivisionParZero(RefusDuMoteur):
    """Division par un zéro de la double précision dans une méthode d'étape d'un bloc
    (`ZeroDivisionError`) : refus de division (ADR 0016, point 10.1 ; décision du mainteneur du
    27/11/2026, point 2 ; P299 ; #158).

    Levé par le moteur, qui traduit l'exception de l'arithmétique en refus typé à l'appel du
    bloc, sur le modèle de `DepassementNumerique` : champs pas, étape, bloc (radical de la
    méthode appelée), `nom = None` (l'arithmétique ne connaît pas la variable) ; l'exception
    d'origine est chaînée. Le filet couvre tout ce que la méthode d'étape appelle, vue et noyau
    compris : le code du moteur et du noyau atteignable depuis une vue ne divise par aucune
    grandeur qui puisse être nulle (ADR 0016, point 10.4). Ce n'est pas un rattrapage : le pas
    s'arrête comme pour tout `RefusDuMoteur`.
    """
