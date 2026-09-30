# Faits mesurés en sessions G à K sur le moteur v2.0

Synthèse rédigée le 29/09/2026 pour l'issue #5, à partir des rapports des sessions G à K (rapports datés du 17 au 19/09/2026) et de leurs audits de reproduction (17 au 20/09/2026). Elle sert de source historique aux fiches comparatives du moteur v3 (`docs/blocs/`) ; elle n'est pas une référence pour le moteur v3.

## 1. Contexte commun et statuts

### 1.1 Moteur, état, profil

- **Moteur** : v2.0, profil « W10 + P1 + R3 », version d'état `2.5-claude-w10-20260914`. Le code versé dans `archive/v2.0/prototype/` est celui de l'archive d'exécution K ; l'audit K établit qu'il est identique fichier par fichier à celui de J (`RAPPORT_AUDIT_K_OPUS_20260920.md` § 1.1). Il contient la seule ligne moteur modifiée pendant G–K : le diagnostic `_diag_cu['dY']` (diff H0, `model.py` l. 1079), sans effet sur la trajectoire (audit H § 1.2). **Aucune équation économique n'a été modifiée de G à K.**
- **État de départ** : D1 (`reference/D1_prepare150.json`), t = 20 280 semaines, obtenu après **150 ans de préparation**. Il **n'est pas versé** (72 Mo, décision M6) : aucun fait ci-dessous ne peut être rejoué depuis ce dépôt.
- **Profil lu dans l'état D1** (`G/RAPPORT_SESSION_G_20260917.md`, § Périmètre ; confirmé par `RAPPORT_AUDIT_G_OPUS_20260917.md` § 1.1) : `price_mode='markup'`, `price_basis='average'`, `pricing_cost_mode='legacy'`, `mu_fast=0,15`, `money_norm=True`, `investment_mode='legacy_q'`, `ups=0,05`, `xi_M=0,005`, R3 actif (`price_demand_feedback=True`, `kappa_p=0,1`, `kappa_bar=0,05`), P1 (`payout_mode='leverage_target'`, `ell_star=0,3`, `lam_ell=0,1`), `rstar_mode='anchored'` (`rstar_anchor='deposit_wedge'`, `rstar_band=0,01`), `rho_i=0,7`, `portfolio_mode='joint_equity'` (`K/resultats/K1/k1_cred_initial_1/resultat.json`). Autres correctifs actifs lus par l'audit G : `tax_rule=True`, `build_norm=True`, `adv_interest=True`, `treasury_redeem_all=True`, `residual_tolerance='stock_aware'` ; `fiscal_rule=False`.
- **Calendrier** : 52 semaines par an, une décision de politique toutes les 4 semaines (`DECISION_WEEKS = 4`, `model.py` l. 37), soit 13 décisions par an.
- **Appariement** : chaque branche d'un essai repart du même D1 sérialisé et du même état PCG64 (empreinte `97710307…e3fd` en I, J et K). Les écarts publiés sont des **effets totaux appariés** (branche − contrôle), pas des attributions à un canal.

### 1.2 Statuts

| Statut | Sens |
|---|---|
| **S+O** | mesuré par Sol (exécutant) et reproduit par Opus (vérificateur) par exécution, bit à bit sauf mention |
| **O** | mesuré par Opus seul, par post-traitement des trajectoires livrées ou lecture du code, non contre-vérifié |
| **R** | rapporté, non reproduit pendant G–K |
| **L** | lu dans le code versé (`archive/v2.0/prototype/`), numéro de ligne vérifié le 29/09/2026 |

Les sources sont citées relativement à `sessions_sol/` (rapports et JSON de Sol) ou `audits_opus/` (rapports et fiches d'Opus) du dossier de lancement, qui n'est pas versé. Un fait sans JSON cité ne se vérifie que dans le rapport.

### 1.3 Définitions récurrentes

- **Inflation moyenne (G)** : moyenne des 260 glissements annuels hebdomadaires de l'IPC, fraction annuelle. Les 51 premiers glissements recouvrent des prix antérieurs à la branche.
- **d_b(t)** (I, J, K) : `100 × log[(P_b,t / P_b,t−52) / (P_0,t / P_0,t−52)]`, en points de log, avec `P = hist['P']` de fin de semaine ; écart de **rythme** d'inflation entre branche b et contrôle 0.
- **E(t)** (J, K) : écart en points de log du glissement annuel de l'IPC à la cible propre de la branche.
- **Verdict « écart de rythme soutenu, signe attendu »** (J, K) : au moins 209 des 261 semaines de la fenêtre terminale avec |d| ≥ 0,3 point du signe attendu (`audits_opus/RAPPORT_AUDIT_J_OPUS_20260918.md` § 1.3).
- **B_close** (H, I, J, K) : échelle du bilan par pays et semaine, `|D_tot| + |L_cb| + |E_bank| + Σ|Loans_j| + |B_bank| + Σ|LZ_h| + |LE|`, unité monétaire commune ; le dénominateur des soldes est `max(B_close_a, B_close_b)`.
- **R(t)** : ratio `|écart L_cb| / B_close` maximal à la semaine t.

## 2. Référence

### G1 — contrôle sur 260 semaines depuis D1 (S+O)

Source : `G/RAPPORT_SESSION_G_20260917.md` § G1 ; `G/resultats/G1_comparaison.json` (`branch_stats.control`) ; reproduit bit à bit (`audits_opus/RAPPORT_AUDIT_G_OPUS_20260917.md` § 1.3). Fenêtre : semaines 1 à 260 depuis t = 20 280.

| Grandeur (définition, unité) | Valeur |
|---|---:|
| Inflation moyenne (§ 1.3), fraction annuelle | 4,048 % (plage 3,936–4,195 %, finale 3,943 %) |
| Inflation en croissance annualisée du log de l'IPC entre première et dernière décision (O, `audits_opus/FICHE_REPRISE_AUDIT_G_20260917.md`) | 3,977 %/an |
| Inflation anticipée finale `pi_e`, fraction annuelle | 4,015 % |
| Taux directeur `i_cb`, première → dernière semaine | 9,117 % → 9,265 % |
| Cible de taux moyenne aux 65 décisions | 9,225 % |
| PIB réel, variation première → dernière semaine | +11,53 % |
| Chômage final, fraction de la population active | 5,185 % |
| Salaires / coûts unitaires, variation sur 5 ans | +36,19 % / +22,77 % |
| Semaines de contrainte budgétaire d'un groupe de ménages | 0 |

Aucune branche G1 ne déclenche `collapsed`, `depressed`, borne de prix, borne de correction monétaire, rationnement public, défaut de paiement ni fermeture du crédit.

### G1 — trois ablations sur 260 semaines (S+O)

Même source et fenêtre. Écarts de PIB au contrôle : PIB réel final branche / contrôle − 1.

| Branche | Inflation moyenne | PIB final vs contrôle | Chômage final | Contrainte ménages |
|---|---:|---:|---:|---:|
| `ups=0` (terme monétaire des anticipations retiré) | 4,046 % | +0,051 % | 5,151 % | 0 sem. |
| `xi_M=0` (correction d'encaisses sur les prix retirée) | 4,019 % | +0,006 % | 5,127 % | 0 sem. |
| R3 désactivé (`price_demand_feedback=False`) | 4,839 % (plage −0,339 à 16,103 %) | **−13,803 %** | **16,438 %** | 145 sem., 232 groupe-sem. |

- **G1a — identités d'effet direct** à la première décision : résidus 1,70e−18 (`ups`), 0 (`xi_M`, facteur contrôle/ablation 1,0007089876 dans les 4 secteurs), 2,71e−20 (R3). Les trois termes sont actifs avec les coefficients lus. `ups=0` retire à la fois `ups·(gM−gY)` et `−ups·pi_e` (`model.py` l. 1300) : il n'isole pas le signal monétaire.
- **G1b — R3 désactivé** : prix final de l'équipement +65,86 % vs contrôle, coût unitaire +59,62 %, salaire +17,77 %, crédit nouveau nominal moyen +77,94 %. Trajectoire instable sans signal binaire de crise : les indicateurs `collapsed`/`depressed` ne suffisent pas à qualifier une trajectoire.
- **G1c — la définition de l'inflation change le signe** (O, `audits_opus/RAPPORT_AUDIT_G_OPUS_20260917.md` § 1.4) : écart au contrôle en moyenne des glissements / en croissance log de l'IPC : `ups=0` −0,0026 / +0,0024 pt ; `xi_M=0` −0,029 / −0,022 pt ; R3 désactivé +0,79 / −0,33 pt. Un écart de moins d'un point sur cinq ans ne se publie pas sans sa définition.

### D1 sur 60 ans (R)

Source : cadre du projet, `CONTEXTE_PROJET_20260917_version_projet.md` § 2 (mesures antérieures à G, non reproduites en G–K). Test de 60 ans (3 120 semaines) depuis D1, par blocs de 5 ans : 7 critères sur 8.

| Grandeur | Valeur rapportée |
|---|---:|
| Dérive K/Y (bloc vs bloc 5–10 ans) | 3,41 % |
| Dérive M/Y | 1,66 % |
| Dérive de la part salariale | 0,147 pt |
| Chômage | 5,18 % (12 blocs sur 12 dans 4–8 %) |
| q̄ | 1,111 |
| Prix équipement / consommation : dérive ; épisode | 12,8 % ; 13,6 % |
| **Taux réel directeur** (seul critère en échec, bande 1,5–3 %) | **5,12 %** |
| **Inflation** (critère prospectif du 16/09, 2 ± 1 pt) | **4,07 %** |

Décomposition rapportée du taux réel : ancre 1,919 + (proxy − ancre) 0,514 + terme d'inflation 2,868 − activité 0,170 = 5,117 %. Les ratios de stocks sont stables depuis D1, mais **D1 n'est pas un état initial résolu** : la préparation de 150 ans fait passer la dérive K/Y de 11,2 % à 3,41 % et M/Y de 22,0 % à 1,66 % (même source, § 3).

Crédibilité du contrôle : 0 sur 3 120 semaines (O, `audits_opus/RAPPORT_AUDIT_J_OPUS_20260918.md` § 2.3 ; cohérent avec un écart de crédibilité J1a − contrôle nul sur 3 120 semaines, `J/resultats/J1/synthese_J1.json`).

## 3. Transmission, prix et salaires

### G-T — chemin actif de la transmission monétaire (S+O ; chemin lu par Sol)

Source : `G/RAPPORT_SESSION_G_20260917.md` § Transmission. Fenêtre : contrôle G1, 65 décisions.

- Cible de taux = taux naturel estimé 2,417 + anticipation 4,007 + contribution d'inflation 2,953 − activité 0,153 = **9,225 %** (reproduit : 9,2248 %). La règle ajoute l'anticipation séparément : c'est `a_pi` = 1,5 entier qui pèse sur le taux réel.
- Taux apparent d'emprunt 13,220 % → 13,342 % ; dépôt 8,177 % → 8,265 % ; rendement réel net moyen des ménages 2,086 % ; taux réel long de l'investissement 5,948 % → 6,009 % ; `q` moyen 1,097–1,109 selon le secteur.
- **Aucune élasticité causale** de la demande au taux n'est identifiée par G (pas de choc exogène).

### G-P — les prix suivent les coûts unitaires (O)

Source : `audits_opus/RAPPORT_AUDIT_G_OPUS_20260917.md` § 1.5. Grandeur : croissance du log du prix sectoriel sur 260 semaines / 5, points par an ; résidu de décomposition < 1e−15.

- Dans les trois branches stables (contrôle, `ups=0`, `xi_M=0`), la croissance du prix de chaque secteur égale celle de son coût unitaire **à 0,04 point par an près**.
- `xi_M` pèse directement 0,935 point par an sur tous les prix (environ 23 % de leur croissance) ; son retrait est compensé par un rappel au coût plus fort (environ +0,9 point par an). L'équation de prix répartit la hausse, elle n'en fixe pas le rythme.

### G-W — bloc salarial actif `wsps2` (O, coefficients lus dans D1)

Source : `audits_opus/RAPPORT_AUDIT_G_OPUS_20260917.md` § 1.5.

- Croissance salariale annuelle = `idx_u · varpi_w · max(pi_e, pi) + lam_w · log(W*/W) + gamma_A · g_prod`, avec `varpi_w=1`, `gamma_A=1`, `lam_w=1`, `beta_u=2`, `cred=0` dans le bloc, `idx_catchup=0`, `wage_indexation_mode='legacy_asymmetric'`, `idx_u = clip(1 − 2·max(u − u_n, 0), 0, 1)`.
- Contrôle G1 : croissance salariale moyenne sectorielle mesurée 6,19 %/an ; terme prédit 4,05 % (inflation) + 2,17 % (`g_prod`) = 6,22 %.
- L'indexation sur `max(pi_e, pi)` fait cliquet à la baisse.
- **H0** (S+O, `H/RAPPORT_SESSION_H_20260917.md` § 1.3 ; `audits_opus/RAPPORT_AUDIT_H_OPUS_20260917.md` § 1.4) : les champs exportés reconstituent la croissance salariale exécutée (résidu 1,1e−16) et la variation de `pi_e` (résidu 3,4e−18) ; sur 7 décisions (26 semaines), aucune borne salariale ni branche `unprof` sur 28 observations secteur-décision, branche marginale de la cible d'équipement 7/7, `u_n` hystérétique 5,125137–5,125414 % contre `p.u_n` = 5 %.

## 4. Politique monétaire et crédibilité

Tous les essais : branches appariées depuis D1, continuation unique sans redémarrage, filtres « aucun effondrement, aucune dépression, aucune contrainte prévisionnelle d'un groupe de ménages de plus de 26 semaines consécutives » tous satisfaits.

### I1 — choc de taux temporaire ±0,01 pendant 104 semaines (S+O)

Source : `I/RAPPORT_SESSION_I_20260917.md` § 4 ; `I/resultats/I1/synthese_I1.json` ; reproduit bit à bit (`audits_opus/RAPPORT_AUDIT_I_OPUS_20260917.md` § 1.2). Choc `shock_i` additif dans la cible avant lissage, appels 1 à 104 (26 décisions), nul ensuite ; horizon 3 120 semaines.

| Branche | d(260), pt log | d(3120), pt log | Extrémum signé de d, semaine |
|---|---:|---:|---:|
| Hausse +0,01 | +0,381750 | +0,022703 | −1,133865, sem. 37 |
| Baisse −0,01 | +0,070968 | −0,070579 | +0,910925, sem. 41 |

- Premier pas de `i_cb` : ±0,003 exactement, soit `(1 − rho_i)·s`. Aucune borne active, `pol_override` inactif.
- **I1a — asymétrie** : ratio des extrémums 1,133865 / 0,910925 = **1,245** (lecture robuste, `J/RAPPORT_SESSION_J_20260917.md` § J3). Le ratio terminal |d_hausse(260)| / |d_baisse(260)| = 5,379207 **n'a pas d'information** : dénominateur juste au-dessus de son plancher de 0,05 et série qui change douze fois de signe avant la semaine 1 040 (audit I § 2). Le verdict « indéterminé » de la hausse à 260 semaines traduit une oscillation.
- **I1b — le choc déplace le niveau des prix, pas le rythme** (O, `audits_opus/FICHE_REPRISE_AUDIT_I_20260917.md`) : hausse, écart permanent de −1,24 point de log du niveau de l'IPC (−1,26 en fin de choc) ; baisse, +2,21. Coût réel de la hausse : écart de chômage maximal +0,55 point (semaine 42), +0,31 point en moyenne pendant le choc.
- **I1c — transmission salariale** (O, même source) : pendant les 26 décisions choquées (hausse), croissance salariale inférieure de 0,495 point par an au contrôle, dont −0,200 par l'indexation, −0,319 par le terme de niveau `log(W*/W)`, +0,023 par la productivité ; les trois termes reviennent sous 0,03 point sur les années 6 à 60. La transmission n'est pas faible, elle est **temporaire** : aucun terme du bloc actif ne retient un changement de rythme.

### J1a — cible d'inflation 2 % → 3 %, maintenue 3 120 semaines (S+O)

Source : `J/RAPPORT_SESSION_J_20260917.md` § J1 ; `J/resultats/J1/synthese_J1.json` ; reproduit bit à bit (audit J § 1.2).

| Horizon | d(T), pt log | Gain de cible G | E(T) J1a − 3 % | E(T) contrôle − 2 % |
|---:|---:|---:|---:|---:|
| 1 560 | +0,886437 | 0,886 | 1,940709 | 2,054272 |
| 3 120 | +0,975314 | 0,975 | 1,964654 | 1,989340 |

- Verdict « écart de rythme soutenu, signe attendu » aux deux horizons (261/261 semaines). Réponse du rythme presque unitaire, **mais même biais d'environ 2 points au-dessus de la cible propre** : la cible est suivie, pas atteinte.
- Écart de chômage (moyenne mobile, J1a − contrôle) : maximum 0,239 point ; aucun épisode de stagnation (seuil 2 points). Écart de crédibilité au contrôle : 0 sur 3 120 semaines.

### J1b — choc de taux +2 points maintenu 3 120 semaines (S+O)

Même source.

- d(1560) = −0,987358 ; d(3120) = −0,396659 ; verdict « écart de rythme soutenu, signe attendu » aux deux horizons.
- Écarts au contrôle à 3 120 semaines (fractions annuelles) : taux appliqué −0,031174, taux réel déflaté −0,025890, `rstar` appliqué −0,009697. **Le resserrement permanent finit avec un taux plus bas** que le contrôle.
- **J1c — bascule de crédibilité** : écart de crédibilité au contrôle terminal 0,99889, moyen 0,90766 sur 3 120 semaines ; anticipation d'inflation terminale −1,99 point, moyenne −1,84 point (`synthese_J1.json`, `measure_summaries_as_gap_to_control`). Date de la bascule de 0 à 1 « vers la semaine 305 » : rapportée par Opus (audit J § 2.3), **non vérifiable** dans les JSON versés au dossier (trajectoires hebdomadaires non disponibles).
- Chômage : écart moyen +0,577 point sur 3 120 semaines (JSON : `mean_gap` 0,005772), maximum de la moyenne mobile 0,763 point.

### K1 — crédibilité initiale fixée à 1, une seule fois, 1 560 semaines (S+O)

Source : `K/RAPPORT_SESSION_K_20260919.md` § 2 ; `K/resultats/K1/synthese_K1.json` ; `K/resultats/K1/k1_cred_initial_1/resultat.json` (crédibilité 0 avant affectation, 1 après, aucun maintien forcé) ; reproduit bit à bit (audit K § 1.2). Fenêtre `[0, T]`, semaine 0 = D1 (d(0) = 0 par construction).

| Grandeur | T = 260 | T = 1 560 |
|---|---:|---:|
| d(T), pt log | −0,37353 | −0,31228 |
| Semaines au seuil de signe attendu | 240/261 | 173/261 |
| Verdict | soutenu, signe attendu | indéterminé (transition inachevée) |
| E(T), pt log | 1,49324 | 1,74199 |
| Semaines dans |E| ≤ 0,3 | 0/261 | 0/261 |
| Crédibilité terminale | 0,962896 | 0,768763 |

- Écarts au contrôle (rapport K) : chômage terminal −0,60 puis −0,15 point ; anticipation terminale −1,71 puis −1,67 point ; prime de dette −3,04 puis −2,46 points.
- La crédibilité quitte 1 dès la première clôture, n'y revient jamais, n'atteint jamais 0.

### K1a — loi de crédibilité (L, et O pour sa vérification)

Lu dans `archive/v2.0/prototype/model.py` **l. 1305** (bloc mensuel ouvert l. 1289), à chaque décision :

```
raw_credibility = cred + nu1·1[|pi − pi_star| < eps_bar] − nu2·|pi − pi_star|/13 − nu3·1[monetize > 0]/13
cred = clip(raw_credibility, 0, max(1 − nu9·M_hist, cred_floor))      # l. 1306 et 1308
```

- Valeurs par défaut de `Params` (l. 229) : `nu1 = 0,01`, `nu2 = 0,5`, `nu3 = 0,2`, `eps_bar = 0,01` (1 point) ; l. 303 : `nu9 = 0,12`, `cred_floor = 0,05`. Les valeurs de D1 ne sont pas vérifiables depuis ce dépôt (D1 absent) ; l'audit K les donne égales (`nu1 = 0,01`, `nu2 = 0,5`, `eps_bar = 1` point).
- **Seuil de déclenchement** : le bonus (+0,01 par décision, soit +0,13 par an au plus) ne joue que si l'écart d'inflation à la cible est inférieur à `eps_bar`. Au-delà, seule la pénalité agit : −`nu2`·|écart| par an.
- **Vérification (O, audit K § 3)** : sur les 1 560 semaines de K1, l'écart ne passe jamais sous 1 point ; avec un écart moyen de 1,48 point sur 5 ans et 1,54 point sur 30 ans, la loi prédit 0,962896 et 0,768763, **exactement** les valeurs mesurées. Calcul : 1 − 5 × 0,5 × 0,0148 = 0,963 ; 1 − 30 × 0,5 × 0,0154 = 0,769 ; la crédibilité se vide d'environ 0,0075 par an.
- **Conséquence** : la crédibilité est une variable asservie à l'écart d'inflation qu'elle est censée refermer. Sur le critère préenregistré par Opus (fiche J), l'inflation ne rejoint pas la cible : **la crédibilité est un relais, pas le verrou**. Aucun des trois leviers essayés séparément (cible, taux maintenu, crédibilité initiale) ne referme les deux points d'écart à la cible. L'essai proposé (`eps_bar` élargi) n'a pas été exécuté.

## 5. Invariance multijoueur

Seuils prospectifs (fixés en H avant essai) : écart relatif `|a − b|/|b|` ≤ 1e−10 sur huit champs économiques (PIB réel, chômage, prix sectoriels, salaires, capital, prêts, `pi_e`, `i_cb`) ; `|écart Res ou L_cb| / B_close` ≤ 1e−12. Fixtures : unité monétaire du pays A ×100 (nominaux convertis, 23 403 cohortes hypothécaires, identifiants inchangés) ; permutation de l'ordre des pays A-B-C.

### G2 — tolérances héritées (S+O)

`G/resultats/G2/localisation.json`. Aux tolérances héritées (`rtol = 1e−10`, `atol = 1e−8`), trois contrôles échouent : pays seul contre `World([pays])`, `Res` semaine 5 (écart 2,44e−4, 25 %) ; unité ×100, `L_cb` semaine 1 (écart 8,58e−5) ; permutation, `L_cb` semaine 1 (écart 1,22e−4). Lecture d'Opus (O, audit G § 1.4) : `Res` est un solde dérivé du bilan bancaire et sa partie négative est reportée sur `L_cb` (`model.py` l. 1280–1283, L) ; les écarts sont des fractions dyadiques de l'ordre du pas flottant d'un bilan d'environ 6,6e11 ; les grandeurs économiques restent ≤ 1,7e−14 sur 13 semaines et ≤ 5,9e−13 sur 260 semaines (pays seul). Le verdict « échec » aux tolérances héritées est conservé ; le critère est mal posé pour des soldes résiduels.

### H2 — 260 semaines (S+O)

`H/resultats/H2/invariance_260_semaines.json` ; 44 valeurs retrouvées bit à bit par un script indépendant (audit H § 1.3).

| Fixture | Écart relatif économique max | Champ | `L_cb` / B_close max | `Res` / B_close max |
|---|---:|---|---:|---:|
| Unité ×100 | 3,913e−13 | chômage | 7,288e−14 | 4,387e−15 |
| Permutation | 2,717e−13 | taux directeur | 1,449e−13 | 8,232e−15 |

Les deux critères prospectifs passent sur 260 semaines. I2 (`I/resultats/I2/synthese_I2.json`) redonne les mêmes maxima ; R(260) = 6,694873e−14 (unité) et 1,449120e−13 (permutation), pente 209–260 de −1,09e−16 et +9,08e−16 par semaine.

### J2 et K2b — permutation sur 3 120 semaines (S ; O jusqu'à 920)

`J/resultats/J2/country_permutation/synthese.json` ; `K/resultats/K2b/synthese_K2b.json`.

- Champs économiques : écart relatif max 2,97e−12 sur 3 120 semaines (taux directeur), sous le seuil 1e−10 ; 2,16e−12 à 920 semaines (audit K).
- **`Res`** : premier franchissement semaine **910**, pays B, écart absolu 4,26654 pour B_close 4,2647e12, ratio 1,000426e−12 ; 2 211 semaines en échec sur 3 120 ; ratio max 3,30e−12.
- **`L_cb`** : premier franchissement semaine **1 154**, pays A, ratio 1,000092e−12 ; 536 semaines en échec ; ratio max 1,667e−12 ; R(3120) = 1,664e−12. À 920 semaines : aucun échec, ratio max 9,246e−13.
- Statut : la trajectoire J2 à 3 120 semaines a été poursuivie par reprises de sauvegarde tous les 260 semaines (transparence reprise/continu testée sur 16 semaines seulement) et **n'est pas reproduite par Opus** au-delà de 920 ; K2b (Sol, d'une traite) et l'audit K (exécution indépendante) reproduisent le premier échec `Res` en semaine 910 à la dernière décimale.
- L'extrapolation linéaire de l'audit I (franchissement vers la semaine 1 692) était fausse : la croissance du ratio est plus rapide que linéaire.

### J2 et K2c — redénomination ×100 : arrêt en semaine 824 (S+O)

`J/resultats/J2/J2_EXECUTION_INTERRUPTION.json` ; `K/resultats/K2c/observation_paiement_rejete.json`.

- Le monde redénominé s'arrête en semaine 824 (823 semaines accomplies) sur `AssertionError: Paiement international non financé` ; le monde de référence traverse 830 semaines sans erreur (O, audit J § 2.1). R(260) = 6,694873e−14.
- Paiement rejeté unique : `World._clear.<locals>.pay`, pays A, `FX → G` ; demandé −1,862645e−9, payé 0 (unité locale) ; dépôt avant débit 5 716 572,39 ; cours local / commun 0,01 ; seuil 1e−9.
- Mécanisme (L) : `Ledger.transfer` renvoie 0 pour tout montant ≤ 0 (`model.py` l. 52), puis `World.pay` teste `abs(paid − amount) > 1e−9*max(1., amount)` (`worldn.py` l. 166). **Tolérance absolue sous 1, relative au-dessus, évaluée en unité locale : elle ne suit pas un changement d'unité.** Même seuil non homogène dans `Ledger.transfer` pour l'enregistrement des défauts de paiement (`model.py` l. 55).
- Origine du résidu négatif : non recherchée. Un correctif d'Opus (deux blocs de `worldn.py`) a été déposé après K ; ses rejeux à 3 120 semaines n'ont pas été exécutés par Sol. Le code versé ne le contient pas.

### Non-interférence des exports (S+O)

G0, H0, I0, J0 : sur 26 semaines, charge utile complète de l'état, état PCG64, grand livre et diagnostics comptables identiques bit à bit avec et sans export. Le contrôle J est identique bit à bit au contrôle I sur 3 120 semaines pour les 104 champs communs (O, audit J § 1.2). `_diag_cu` est sérialisé dans l'état (audit H § 1.2).

## 6. Instabilités connues — ne pas réintroduire

Source : `CONTEXTE_PROJET_20260917_version_projet.md` § 5 (R), complété par G–K.

1. Construction répondant au niveau de p_Z/p_K : cycle de 3,5 ans.
2. Avances au Trésor sans intérêt.
3. Coupon de consolidation au taux du moment.
4. Estimateur de r* sans ancre ni bande.
5. Dividende de trésorerie sans règle fiscale.
6. Effet richesse normé par défaut.
7. Ancrage salarial fort sur la productivité marginale.
8. Buffer-stock calibré sur un risque iid sans persistance.
9. Mode de prix `normal_average` seul : prix de l'équipement ×4,8 en 60 ans.
10. N1, dépréciation au prix lissé : ×2,9.
11. N5, dépréciation indexée.
12. N6, correction de marge par le gain.
13. R1, élasticité à référence mobile.
14. **Règle de prix sans terme de demande (R3 retiré)** : G1b ci-dessus (S+O) ; et, rapporté (R, contexte § 3), production d'équipement nulle en semaine 736 sur 60 ans.
15. **Un plafond produit un cycle** (R, contexte § 3).
16. **Tolérances absolues sur des soldes résiduels ou des montants en unité locale** : G2, J2, K2c (§ 5).

## 7. Hypothèses réfutées — ne pas y revenir sans fait nouveau

Source : `CONTEXTE_PROJET_20260917_version_projet.md` § 4 (R), complété par les audits G–K (O). Cause commune : raisonner sur une équation sans vérifier qu'elle est active dans le profil, ni avec quels coefficients.

1. **Prix de l'équipement auto-référent « à gain 1 »** : le gain comparait deux définitions (avec et sans intrants externes) ; à définition égale, les deux moteurs sont au même niveau.
2. **Dérive du prix relatif en v1.7** : mesurée contre l'énergie (+55 % en 200 ans) ; contre la consommation, +2,5 %. Erreur de dénominateur.
3. **Élasticité de la consommation au taux comme mécanisme manquant** : étendue à H0 et H1, chômage 9,02 % → 8,88 % pour η de 0 à 2.
4. **Blocage de l'investissement en v1.7** : capital +12,7 à 13,3 % en cinq ans, aucune borne ne lie, rationnement de livraison 3,55 %.
5. **Ancre du taux naturel à 4 %** : mesurée à 1,997 %.
6. **Formule de Taylor en (a_π − 1)** : la règle ajoute l'anticipation séparément, c'est a_π = 1,5 entier qui pèse.
7. **`u_n` hérité dans l'écart d'activité** : inactif sous `wsps2`, la règle utilise le paramètre structurel à 5 %.
8. **Piège de crédibilité immédiat hérité de l'état** : pendant la préparation, la crédibilité monte à 1, passe 580 semaines dans la bande et ne tombe à zéro qu'après 134 ans ; la remise de `cred`, `pi_e`, `u_n` à leur valeur de construction (F1c) laisse inflation et taux réel inchangés à la quatrième décimale.
9. **Canal d'inflation désigné par `ups`, `xi_M` ou R3** (G1, S+O) : aucune des trois ablations ne désigne de canal ; la comptabilité renvoie au coût unitaire et au bloc salarial (G-P).
10. **Salaires insensibles au chômage hors `idx_u`** (hypothèse d'Opus, fiche G, réfutée sur son propre critère, fiche I) : pente prédite ≈ −0,08 point de croissance salariale par point de chômage ; mesurée ≈ −0,50 point par an pour +0,31 point de chômage, surtout par le terme de niveau (I1c).
11. **Crédibilité comme verrou du régime à 4 %** (fiche J, réfutée en K) : K1a.
12. **Franchissement linéaire du seuil d'invariance** (audit I) : observé en semaine 910, pas 1 692.

Question ouverte au terme de K : **ce qui fixe le rythme d'inflation à environ 4 %** n'est pas établi. Un régime attractif est compatible avec les faits ; son unicité et son étendue ne le sont pas.

## 8. Acquis à conserver

Source : `CONTEXTE_PROJET_20260917_version_projet.md` § 3 (R) sauf mention ; aucun n'a été remesuré pendant G–K hors R3 et WS-PS.

- **P1, cible de levier des firmes** : rétention = (1 − ℓ*)·p_K·I + (λ_ℓ/52)·(prêts − ℓ*·p_K·K), dividende résiduel, demande de crédit vers la cible et remboursement limité à l'excès de levier. Sans les deux derniers termes, le levier tend vers zéro dans les deux moteurs. A stabilisé les stocks financiers partout où il a été essayé. Paramètres D1 : `ell_star = 0,3`, `lam_ell = 0,1` (audit G).
- **R3, terme de demande dans la règle de prix** : `adj += clip(kappa_p·flex·z, ±kappa_bar·flex)` (audit G § 1.4) ; expérience causale la plus nette du projet (G1b, S+O).
- **WS-PS (bloc salarial `wsps2`)** : donne le bon partage de la valeur ajoutée (dérive de la part salariale 0,147 pt sur 60 ans, R) ; sa forme active et sa vérification numérique sont en G-W (O).
- **Formule d'état stationnaire du capital** : K/Y = part du capital / (q*·(r_L + ρ_E + δ)), q* = 1 + g/(ι·Γ), corrigée du taux de livraison ; l'épargne n'y entre pas (bouclage wicksellien).
- **La propension à consommer ne fixe pas la dépense** (résultat stock-flux) ; taux d'épargne stationnaire = g × richesse/revenu.
- **La préparation de l'état est décisive** : un état qui n'est pas un équilibre des règles en vigueur produit des dérives (§ 2, D1). D'où l'exigence v3 d'un état initial résolu.
- **Les tâtonnements de prix et l'emploi au profit nul étaient les stabilisateurs cachés de la v1** ; les retirer donne le bon partage et déplace le problème vers la fermeture du niveau d'activité.
- **La politique monétaire peut agir à l'envers** (canal rentier).
- **Coût de la monétisation (H7, F3)** (R ; non reproduit par l'audit G, état F3 absent) : barèmes figés (`tax_adjust_speed = 0`), niveau de vie final −27,2053 %, PIB final −5,6468 %, dette publique nette 293,0506 % du PIB contre 62,4225 %, paiements publics rationnés à ρ_G = 0,58, consommation H0/H1 −19,5407 %/−19,1948 %, H2 +15,7694 % (`G/RAPPORT_SESSION_G_20260917.md` § G3). La monétisation n'est pas gratuite ; son équilibre ludique n'est pas établi, et F3 ne sépare pas l'effet des avances de celui des transferts.
- **Méthode** : une grandeur porte définition, unité, dénominateur et fenêtre (G1c, I1a montrent le coût d'un oubli) ; critères préenregistrés, verdicts historiques conservés ; appariement depuis un même état et une même graine ; contrôles de non-interférence des observateurs.
