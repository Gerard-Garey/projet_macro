"""Test fumée : le paquet et ses sous-paquets se chargent et fixent leur rôle."""

import importlib

import pytest

SOUS_PAQUETS = ("noyau", "blocs", "moteur", "etat", "scenarios", "leviers", "observation")


def test_paquet_se_charge():
    import nations

    assert nations.__doc__ and nations.__doc__.strip()


@pytest.mark.parametrize("nom", SOUS_PAQUETS)
def test_sous_paquet_se_charge_avec_son_role(nom):
    module = importlib.import_module(f"nations.{nom}")
    # Chaque sous-paquet porte une docstring qui fixe son rôle (CLAUDE.md,
    # « Architecture »).
    assert module.__doc__ and module.__doc__.strip()
