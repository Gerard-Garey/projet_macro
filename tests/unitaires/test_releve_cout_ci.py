"""Tests du relevé du coût du noyau seul dans les journaux de la CI (#105).

Les journaux sont synthétiques et minimaux : les seules lignes que le script
lit (checkout, image, C), avec l'horodatage de GitHub Actions en tête.
"""

import json

import pytest

SHA = "2e643a2d1b43f15929a661b53a6b309129e34129"
AUTRE_SHA = "156564b" + "0" * 33
H = "2026-10-15T05:54:20.7841312Z "


def journal(c=None, reps=None, image="20261012.334.1", sha=SHA, fetch_seul=False):
    """Texte d'un journal fabriqué ; `None` omet la ligne correspondante."""
    lignes = [f"{H}##[group]Run actions/checkout@v4"]
    if sha is not None:
        lignes.append(
            f"{H}[command]/usr/bin/git -c protocol.version=2 fetch --no-tags --depth=1 origin "
            f"+{sha}:refs/remotes/origin/main"
        )
        if not fetch_seul:
            lignes += [f"{H}[command]/usr/bin/git log -1 --format=%H", f"{H}{sha}"]
    lignes.append(f'{H}\x1b[36;1mecho "ImageOS=${{ImageOS:-?}} ImageVersion=${{ImageVersion:-?}}"\x1b[0m')
    if image is not None:
        lignes.append(f"{H}ImageOS=ubuntu24 ImageVersion={image}")
    if c is not None:
        reps = reps or [c + 0.01, c, c + 0.002, c + 0.003, c + 0.004]
        texte_reps = ", ".join(f"{r:.4f}" for r in reps)
        lignes.append(f"{H}  C = {c:.4f} ms par pas (répétitions : {texte_reps})")
        lignes.append(f"{H}  seuil 0.5 ms : marge 0.1 ms, rapport seuil / C = 1.38")
    return "\n".join(lignes) + "\n"


def ecrire(dossier, nom, contenu):
    chemin = dossier / nom
    chemin.write_text(contenu, encoding="utf-8")
    return chemin


def test_extraction_exacte(releve_cout, tmp_path):
    chemin = ecrire(tmp_path, "run_38689324771_job_116271332120.txt",
                    journal(0.3622, [0.3700, 0.3739, 0.3642, 0.3623, 0.3622]))
    r = releve_cout.lire_journal(chemin)
    assert r.run == 38689324771
    assert r.commit == SHA and r.commit_source == "journal"
    assert r.image == "ubuntu24 20261012.334.1"
    assert r.c_ms == 0.3622
    assert r.repetitions_ms == (0.3700, 0.3739, 0.3642, 0.3623, 0.3622)


def test_commit_de_git_log_prefere_a_celui_du_fetch(releve_cout, tmp_path):
    texte = journal(0.3, sha=AUTRE_SHA, fetch_seul=True)
    texte += f"{H}[command]/usr/bin/git log -1 --format=%H\n{H}{SHA}\n"
    assert releve_cout.lire_journal(ecrire(tmp_path, "run_1.txt", texte)).commit == SHA


def test_commit_lu_dans_la_ligne_de_fetch_a_defaut(releve_cout, tmp_path):
    chemin = ecrire(tmp_path, "run_1.txt", journal(0.3, fetch_seul=True))
    assert releve_cout.lire_journal(chemin).commit == SHA


def test_run_absent_du_nom(releve_cout, tmp_path):
    assert releve_cout.lire_journal(ecrire(tmp_path, "journal.txt", journal(0.3))).run is None


def test_statistiques(releve_cout, tmp_path):
    valeurs = {1: (0.27, "A"), 2: (0.42, "B"), 3: (0.43, "B"), 4: (0.36, "B")}
    for run, (c, image) in valeurs.items():
        ecrire(tmp_path, f"run_{run}_job_9.txt", journal(c, image=image))
    resultat = releve_cout.synthese(releve_cout.relever([tmp_path]))
    ens = resultat["ensemble"]
    assert ens["n"] == 4
    assert ens["minimum_ms"] == 0.27 and ens["maximum_ms"] == 0.43
    # Effectif pair : moyenne des deux valeurs centrales, (0.36 + 0.42) / 2.
    assert ens["mediane_ms"] == pytest.approx(0.39)
    assert ens["rapport_max_min"] == pytest.approx(0.43 / 0.27)
    assert list(resultat["par_image"]) == ["ubuntu24 A", "ubuntu24 B"]
    assert resultat["par_image"]["ubuntu24 A"]["n"] == 1
    assert resultat["par_image"]["ubuntu24 A"]["rapport_max_min"] == pytest.approx(1.0)
    assert resultat["par_image"]["ubuntu24 B"]["mediane_ms"] == pytest.approx(0.42)


@pytest.mark.parametrize("champs", [{"c": None}, {"image": None}])
def test_refus_d_un_journal_incomplet(releve_cout, tmp_path, champs, capsys):
    ecrire(tmp_path, "run_1.txt", journal(0.3))
    ecrire(tmp_path, "run_2.txt", journal(**({"c": 0.3} | champs)))
    with pytest.raises(releve_cout.JournalRefuse):
        releve_cout.relever([tmp_path])
    assert releve_cout.main([str(tmp_path)]) != 0
    assert "run_2.txt" in capsys.readouterr().err


def test_refus_de_c_qui_n_est_pas_la_meilleure_repetition(releve_cout, tmp_path):
    chemin = ecrire(tmp_path, "run_1.txt", journal(0.3, [0.31, 0.29, 0.32, 0.33, 0.34]))
    with pytest.raises(releve_cout.JournalRefuse, match="minimum"):
        releve_cout.lire_journal(chemin)


@pytest.mark.parametrize(
    "ajout, motif",
    [
        (f"{H}  C = 0.3000 ms par pas (répétitions : 0.3000)\n", "lignes C"),
        (f"{H}ImageOS=ubuntu24 ImageVersion=20261004.327.1\n", "plusieurs images"),
        # Ligne d'image répétée à l'identique : refusée comme une ligne C répétée (docstring du script).
        (f"{H}ImageOS=ubuntu24 ImageVersion=20261012.334.1\n", "plusieurs images"),
    ],
    ids=["deux_lignes_C", "deux_images", "deux_images_identiques"],
)
def test_refus_d_un_journal_ambigu(releve_cout, tmp_path, ajout, motif):
    chemin = ecrire(tmp_path, "run_1.txt", journal(0.3) + ajout)
    with pytest.raises(releve_cout.JournalRefuse, match=motif):
        releve_cout.lire_journal(chemin)


def test_refus_de_deux_journaux_au_meme_run(releve_cout, tmp_path):
    ecrire(tmp_path, "run_1_job_a.txt", journal(0.3))
    ecrire(tmp_path, "run_1_job_b.txt", journal(0.3))
    with pytest.raises(releve_cout.JournalRefuse, match="même run"):
        releve_cout.relever([tmp_path])


def test_refus_d_un_journal_donne_deux_fois(releve_cout, tmp_path):
    # Sans numéro de run, seul le chemin résolu distingue le doublon.
    chemin = ecrire(tmp_path, "journal.txt", journal(0.3))
    for chemins in ([chemin, chemin], [tmp_path, tmp_path / "." / "journal.txt"]):
        with pytest.raises(releve_cout.JournalRefuse, match="deux fois"):
            releve_cout.relever(chemins)


def test_refus_de_commits_differents(releve_cout, tmp_path, capsys):
    ecrire(tmp_path, "run_1.txt", journal(0.3))
    ecrire(tmp_path, "run_2.txt", journal(0.3, sha=AUTRE_SHA))
    assert releve_cout.main([str(tmp_path)]) != 0
    assert "commits différents" in capsys.readouterr().err


def test_commit_declare(releve_cout, tmp_path):
    ecrire(tmp_path, "run_1.txt", journal(0.3))
    ecrire(tmp_path, "run_2.txt", journal(0.3, sha=None))
    # Sans --commit, le journal sans commit est refusé.
    with pytest.raises(releve_cout.JournalRefuse, match="--commit"):
        releve_cout.relever([tmp_path])
    releves = releve_cout.relever([tmp_path], "2E643A2")
    assert [r.commit_source for r in releves] == ["journal", "--commit"]
    # Un commit lu qui ne commence pas par le commit déclaré est refusé.
    with pytest.raises(releve_cout.JournalRefuse, match="déclaré"):
        releve_cout.relever([tmp_path], "156564b")


def test_un_seul_commit_affiche_avec_commit_court(releve_cout, tmp_path, capsys):
    # --commit court et commit complet lu ailleurs : le lu, complet, est le seul affiché.
    ecrire(tmp_path, "run_1.txt", journal(0.3))
    ecrire(tmp_path, "run_2.txt", journal(0.3, sha=None))
    assert releve_cout.synthese(releve_cout.relever([tmp_path], "2e643a2"))["commit"] == SHA
    assert releve_cout.main([str(tmp_path), "--commit", "2e643a2"]) == 0
    assert f"Commit : {SHA}\n" in capsys.readouterr().out
    # Sans commit lu, le commit déclaré est affiché.
    (tmp_path / "run_1.txt").unlink()
    assert releve_cout.synthese(releve_cout.relever([tmp_path], "2e643a2"))["commit"] == "2e643a2"


def test_ordre_deterministe(releve_cout, tmp_path, capsys):
    for run, c in ((300, 0.30), (20, 0.20), (1000, 0.10)):
        ecrire(tmp_path, f"run_{run}_job_1.txt", journal(c))
    ecrire(tmp_path, "sans_run.txt", journal(0.4))
    runs = [r.run for r in releve_cout.relever([tmp_path])]
    assert runs == [20, 300, 1000, None]
    # Même sortie quel que soit l'ordre des chemins donnés.
    fichiers = sorted(tmp_path.glob("*.txt"))
    assert releve_cout.main(["--json", *map(str, fichiers)]) == 0
    direct = capsys.readouterr().out
    assert releve_cout.main(["--json", *map(str, reversed(fichiers))]) == 0
    assert capsys.readouterr().out == direct
    assert [e["run"] for e in json.loads(direct)["executions"]] == runs


def test_refus_sans_journal(releve_cout, tmp_path):
    assert releve_cout.main([str(tmp_path)]) != 0
