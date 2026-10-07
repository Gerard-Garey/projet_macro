"""Sauvegarde et reprise exactes de l'état d'un monde (ADR 0012, D3 et D4).

Format : un document **JSON texte, UTF-8**, `{"version": <entier>, "pays":
[<EtatPays>…]}`, les pays dans l'ordre canonique (identifiant croissant), les
clés de chaque pays dans l'ordre des champs du schéma. Les entiers sont écrits
en entiers, les flottants par le **`repr` de `float`** (le plus court texte qui
se relit bit à bit, −0,0 compris), le registre en liste. Un état qui contient
un `inf` ou un `NaN` n'est pas sauvegardable (défaut en amont). Aucun
paramètre, aucun levier, aucune série : la reprise exacte vaut à paramètres et
entrées identiques.

`charger` refuse avec diagnostic (`SauvegardeRefusee`) : un document qui n'est
pas du JSON UTF-8 strict (clé en double, `NaN` ou `Infinity` compris) ; un
flottant non fini, y compris un nombre qui déborde (`1e400`) ; un entier
au-delà de la limite de conversion de Python ; une imbrication qui épuise la
pile ; une version différente de `VERSION_SCHEMA` (aucune migration au J2) ;
un champ manquant ou inconnu ; un type qui ne correspond pas exactement au
schéma (un entier pour un flottant compris) ; un champ d'identité hors de son
domaine (identifiant vide, graine négative) ; un pays en double ou hors de
l'ordre canonique (identifiants comparés par point de code Unicode). L'aller-retour `sauvegarder(charger(document))` rend les mêmes
octets qu'un document écrit par `sauvegarder`.
"""

from __future__ import annotations

import itertools
import json
import math
from collections.abc import Sequence

from nations.etat.schema import (
    CHAMPS,
    CHAMPS_D_IDENTITE,
    VARIABLE,
    VERSION_SCHEMA,
    EtatPays,
    defaut_d_identite,
)

_CLES_DU_DOCUMENT = ("version", "pays")
_TYPE_D_IDENTITE = dict(CHAMPS_D_IDENTITE)


class SauvegardeRefusee(Exception):
    """Sauvegarde ou reprise refusée, avec le pays (identifiant ou rang) et le champ en cause."""

    def __init__(self, message: str, *, pays: str | int | None = None,
                 champ: str | None = None) -> None:
        self.pays = pays
        self.champ = champ
        self.message = message
        details = []
        if pays is not None:
            details.append(f"pays {pays!r}")
        if champ is not None:
            details.append(f"champ {champ}")
        super().__init__(f"{message} ({' ; '.join(details)})" if details else message)


def _verifier_ordre(identifiants: Sequence[str]) -> None:
    """Identifiants strictement croissants par point de code Unicode : ni double, ni autre ordre."""
    for precedent, courant in itertools.pairwise(identifiants):
        if courant == precedent:
            raise SauvegardeRefusee("pays en double", pays=courant)
        if courant < precedent:
            raise SauvegardeRefusee("pays hors de l'ordre canonique (identifiant croissant)",
                                    pays=courant)


def sauvegarder(etats: Sequence[EtatPays]) -> bytes:
    """Document de sauvegarde de l'état d'un monde, en octets UTF-8."""
    pays = []
    for etat in etats:
        if type(etat) is not EtatPays:
            raise SauvegardeRefusee(f"EtatPays attendu, {type(etat).__name__} reçu")
        champs = {}
        for nom in CHAMPS:
            valeur = getattr(etat, nom)
            scalaires = valeur if type(valeur) is tuple else (valeur,)
            for x in scalaires:
                if type(x) is float and not math.isfinite(x):
                    raise SauvegardeRefusee(f"valeur non finie {x!r} : état non sauvegardable",
                                            pays=etat.identifiant, champ=nom)
            champs[nom] = list(valeur) if type(valeur) is tuple else valeur
        pays.append(champs)
    _verifier_ordre([p["identifiant"] for p in pays])
    document = json.dumps({"version": VERSION_SCHEMA, "pays": pays}, ensure_ascii=False,
                          allow_nan=False, indent=1)
    return (document + "\n").encode("utf-8")


def _objet_sans_cle_double(paires: list[tuple[str, object]]) -> dict[str, object]:
    objet = {}
    for cle, valeur in paires:
        if cle in objet:
            raise SauvegardeRefusee("clé en double dans le document", champ=cle)
        objet[cle] = valeur
    return objet


def _constante_refusee(nom: str) -> float:
    raise SauvegardeRefusee(f"constante {nom} : une valeur non finie n'est pas sauvegardable")


def _flottant_fini(texte: str) -> float:
    """Flottant lu, refusé s'il n'est pas fini (un nombre qui déborde, `1e400`, donne `inf`)."""
    valeur = float(texte)
    if not math.isfinite(valeur):
        raise SauvegardeRefusee(f"nombre {texte[:40]!r} lu comme {valeur!r} : une valeur non "
                                "finie n'est pas sauvegardable")
    return valeur


def _entier(texte: str) -> int:
    """Entier lu, refusé au-delà de la limite de conversion de Python (`ValueError`)."""
    try:
        return int(texte)
    except ValueError as erreur:
        raise SauvegardeRefusee(f"entier de {len(texte)} caractères illisible : {erreur}") from None


def _champs_attendus(objet: object, attendus: Sequence[str], pays: str | int | None) -> dict:
    """Objet JSON aux clés exactement attendues : champ manquant ou inconnu refusé."""
    if type(objet) is not dict:
        raise SauvegardeRefusee("objet JSON attendu", pays=pays)
    for nom in attendus:
        if nom not in objet:
            raise SauvegardeRefusee("champ manquant", pays=pays, champ=nom)
    for nom in objet:
        if nom not in attendus:
            raise SauvegardeRefusee("champ inconnu du schéma", pays=pays, champ=nom)
    return objet


def charger(document: bytes) -> tuple[EtatPays, ...]:
    """État d'un monde relu d'un document de sauvegarde, ou refus avec diagnostic."""
    if type(document) is not bytes:
        raise SauvegardeRefusee(f"document en octets attendu, {type(document).__name__} reçu")
    try:
        texte = document.decode("utf-8")
    except UnicodeDecodeError as erreur:
        raise SauvegardeRefusee(f"document non UTF-8 : {erreur}") from None
    try:
        racine = json.loads(texte, object_pairs_hook=_objet_sans_cle_double,
                            parse_float=_flottant_fini, parse_int=_entier,
                            parse_constant=_constante_refusee)
    except json.JSONDecodeError as erreur:
        raise SauvegardeRefusee(f"document JSON invalide : {erreur}") from None
    except RecursionError:
        raise SauvegardeRefusee("document JSON trop profondément imbriqué : pile épuisée "
                                "à la lecture") from None
    if type(racine) is not dict:
        raise SauvegardeRefusee("objet JSON attendu à la racine")
    # La version d'abord : une sauvegarde d'une autre version est refusée comme
    # telle, avant tout diagnostic de champ.
    if "version" not in racine:
        raise SauvegardeRefusee("champ manquant", champ="version")
    version = racine["version"]
    if type(version) is not int or version != VERSION_SCHEMA:
        raise SauvegardeRefusee(f"version du schéma {version!r} : seule la version "
                                f"{VERSION_SCHEMA} est admise (aucune migration)",
                                champ="version")
    _champs_attendus(racine, _CLES_DU_DOCUMENT, None)
    if type(racine["pays"]) is not list:
        raise SauvegardeRefusee("liste des pays attendue", champ="pays")
    etats = []
    for rang, objet in enumerate(racine["pays"]):
        # Le pays est nommé par son identifiant s'il est une chaîne non vide, sinon par son rang.
        pays = rang
        if type(objet) is dict and type(objet.get("identifiant")) is str and objet["identifiant"]:
            pays = objet["identifiant"]
        champs = _champs_attendus(objet, CHAMPS, pays)
        valeurs = {}
        for nom in CHAMPS:
            valeur = champs[nom]
            if nom in _TYPE_D_IDENTITE:
                admis = type(valeur) is _TYPE_D_IDENTITE[nom]
            else:
                variable = VARIABLE[nom]
                if variable.type is tuple and type(valeur) is list:
                    valeur = tuple(valeur)
                admis = variable.admet(valeur)
            if not admis:
                attendu = (_TYPE_D_IDENTITE[nom].__name__ if nom in _TYPE_D_IDENTITE
                           else VARIABLE[nom].description_du_type())
                raise SauvegardeRefusee(f"type faux : {attendu} attendu, {valeur!r} lu",
                                        pays=pays, champ=nom)
            motif = defaut_d_identite(nom, valeur) if nom in _TYPE_D_IDENTITE else None
            if motif is not None:
                raise SauvegardeRefusee(f"hors domaine : {motif}", pays=pays, champ=nom)
            valeurs[nom] = valeur
        etats.append(EtatPays(**valeurs))
    _verifier_ordre([e.identifiant for e in etats])
    return tuple(etats)
