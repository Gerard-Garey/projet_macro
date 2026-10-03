---
status: accepted
date: 2026-10-03
---

# Cible d'inflation en vigueur : une variable d'état par pays, lue à l'ouverture par les blocs (délai d'un tour), écrite en phase 1 ; facteur de croissance nominale attendue Γ^e calculé une seule fois par le moteur

> Statut « accepté » : **accepté par le mainteneur le 03/10/2026, avec ses points de forme 3, 4 et 6 (décision M30)**. Rédigé par `architect-approfondi` (Fable, dans la consultation 1 sur 3 de la branche n° 3b, accord du mainteneur du 03/10/2026) sur la décision du mainteneur du 03/10/2026 (fiches `docs/blocs/menages.md` et `docs/blocs/investissement.md` § 9.10, commit `efb6bcd` ; issue #61), décision citant M27 et M28, recommandation concordante de `macro` et `monnaie`. Le fond (délai d'un tour ; Γ^e au moteur ; π\* paramètre au J3 initialisant une variable d'état) est décidé ; les points de **forme** 3, 4 et 6 ci-dessous, proposés par `architect`, ont pris effet avec l'acceptation. Il porte les deux contrats partagés que touche cette décision — le schéma d'état et les grandeurs typées du moteur — et eux seuls ; il applique le point 4 de l'ADR 0009 et le point I.3 de l'ADR 0008. La règle de formation de π\*, ses régimes (B, D, E) et le levier du bloc 8 restent à la fiche 8.

## Contexte

- **Deux blocs lisent la cible déclarée.** M27 (fiche 5, Q10, lecture (c)) : les ménages lisent π\*, jamais π̄ ni le registre (facteur Γ^e = [(1 + g)(1 + π\*)]^{1/n_a}, H1 à H3). M28 (fiche 6) : le taux réel du crédit anticipé ϱ_L = (1 + i_L)/(1 + π\*) − 1 (S1), le prix anticipé de F1 et l'impôt anticipé F4 lisent π\* ; la fiche 6 notait le même facteur Γ̂.
- **Deux questions laissées ouvertes par les fiches** (fiche 5 § 9.8, contrats 2 et 3 ; fiche 6 § 9.8, point 5) : la **date** de lecture (π\* du tour, lue en phase 1, délai 0 ; ou π\* en vigueur à l'ouverture, délai 1) et le **propriétaire** du facteur (un symbole, un calcul).
- **Décision du mainteneur du 03/10/2026** (§ 9.10 des deux fiches ; #61) : délai 1 ; Γ^e grandeur du moteur calculée une seule fois (`eq:moteur-croissance-nominale-attendue` proposé), Γ̂ disparaît ; au J3, π\* est un paramètre typé à source unique de `moteur/` qui initialise une variable d'état « cible en vigueur » ; à la fiche 8, cette variable est écrite par le levier du bloc 8, sans changer l'interface de lecture des blocs 5 et 6. Motifs de `monnaie` (fiche 6 § 9.10) : numérateur et dénominateur de ϱ_L à la même date (sous le délai 0, un changement de cible sans changement de taux produirait un faux saut du taux réel perçu pendant un tour) ; délai uniforme des deux leviers de la banque centrale (i_L lu à l'ouverture, C27). Motif de `macro` (fiche 5 § 9.8) : la grammaire des délais des fiches 3 et 4 (« une décision du tour n agit sur le secteur privé au tour n + 1 au plus tôt ») et la phrase de `jeu` (« une annonce ne déplace pas l'épargne le tour même »).
- **Fait d'architecture.** La phase 2 n'a pas d'ordre interne déclaré (ADR 0007, § « ne règle pas ») ; les blocs 5 et 6 y écrivent tous deux leurs plans. Un facteur tenu par l'un et lu par l'autre en phase 2 exigerait un ordre interne, donc une décision citant M22.
- **Pourquoi maintenant.** Les sections `sec:menages` et `sec:investissement` (jalons 4 de #41 et #42) écrivent H1, S1, F1 et F4 avec leur date de lecture ; l'issue #61 demande la forme du paramètre et de la variable d'état. Aucun code n'existe.

## Décision

**M30, décision du mainteneur du 03/10/2026** (fiches 5 et 6, § 9.10 ; #61), citant M27 et M28 ; forme des points 3, 4 et 6 proposée par `architect` et retenue à l'acceptation. Statut : **choix de conception**.

1. **Une variable d'état « cible d'inflation en vigueur », π\*_t, par pays**, dans le schéma d'état (`etat/`), unité « par an, taux de croissance » (ADR 0008, I.2 : taux d'inflation, converti géométriquement), valeur stationnaire π\* (la cible déclarée de l'état résolu).
2. **Lecture à l'ouverture, délai d'un tour.** Tout bloc qui lit la cible lit π\*_t, valeur d'ouverture du pas, jamais la valeur écrite dans le pas. Un changement de cible décidé au tour n est lu au tour n + 1 ; les plans du tour n sont inchangés (fiche 6 § 9.10, test « Délais »). Cette lecture est la lecture par défaut du point 1 de l'ADR 0009.
3. **Écriture en phase 1, une fois par pas** (ADR 0009, points 1 et 4). La valeur du pas suivant, π\*_{t+1}, est écrite en phase 1 par son propriétaire :
   - **au J3**, le **moteur**, propriétaire provisoire déclaré : il reconduit la valeur en vigueur (π\*_{t+1} = π\*_t), la valeur initiale étant celle du paramètre typé π\* à source unique de `moteur/` ; la trajectoire est constante ;
   - **à partir de la fiche 8**, le **bloc 8**, qui siège déjà en phase 1 (`tab:phases`, ligne 1), l'écrit depuis son levier lu en phase 1 (ADR 0005, point 2) ; l'interface de lecture des blocs 5 et 6 ne change pas, et `tab:phases` non plus.
4. **Γ^e, grandeur du moteur, calculée une seule fois par pas** à partir de la cible d'ouverture et des paramètres de croissance : Γ^e_t = [(1 + g)(1 + π\*_t)]^{1/n_a}, avec g = (1 + g_pr)(1 + g_N) − 1 (ADR 0008, I.5). Ses dérivées γ^e_t = Γ^e_t − 1 et π^{∗,pas}_t = (1 + π\*_t)^{1/n_a} − 1 sont des fonctions du moteur ; aucune n'est une variable d'état, aucune n'est recalculée dans un bloc (ADR 0008, I.3). Label unique : `eq:moteur-croissance-nominale-attendue` (radical `moteur`), posé au J2 ou au J3 avec sa balise ; le symbole Γ̂ de la fiche 6 disparaît.
5. **Γ^e n'est pas le facteur réalisé Γ** = [(1 + g)(1 + π̄)]^{1/n_a} : hors cible, ils diffèrent (T̂_F/T_F = 0,99373 à π̄ = 10 %, π\* = 2 %, fiche 6 § 9.7 (a), chiffre de la fiche, non remesuré ici). Γ est une grandeur de l'état stationnaire résolu, non du moteur.
6. **Phases.** Phase 1 : écriture de π\*_{t+1} (moteur, puis bloc 8) ; phase 2 : les blocs 5 et 6 lisent π\*_t et Γ^e_t. `tab:phases` est inchangée : la ligne 1 écrit déjà « moteur (leviers) » et « banque centrale », et la ligne 2 lit la phase 1 et l'ouverture.

## Options écartées

- **Délai 0 : π\* du tour, lue en phase 1 par les blocs 5 et 6** (lecture implicite des § 3.N-5 et 6.5 de la fiche 5). Écartée par le mainteneur : faux saut du taux réel perçu ϱ_L pendant un tour quand la cible change sans le taux ; délai non uniforme entre les deux leviers de la banque centrale ; dérogation à la grammaire des délais des fiches 3 et 4. Aucun effet stationnaire (fiche 5 § 9.8).
- **π\* paramètre pur au J3, variable d'état seulement à la fiche 8.** Écartée : l'interface de lecture des blocs 5 et 6 changerait à la fiche 8 (deux formes successives du même contrat), et la reprise exacte d'une partie où la cible a changé exige de toute façon la valeur en vigueur dans l'état. La variable existe dès le J3 ; seul son propriétaire change (point 3).
- **Γ^e tenu par le bloc 5 et lu par le bloc 6 en phase 2** (ou l'inverse). Écartée : la phase 2 n'a pas d'ordre interne (ADR 0007) ; en déclarer un pour une grandeur dérivée serait une décision citant M22 sans contenu économique ; une révision du facteur toucherait deux blocs.
- **Deux symboles, deux calculs** (Γ^e au bloc 5, Γ̂ au bloc 6). Écartée : contraire à l'ADR 0008, I.3 (une conversion écrite une fois, jamais recalculée) ; deux équations de la spécification pour une grandeur, et une divergence silencieuse possible.
- **Γ^e en variable d'état.** Écartée : grandeur dérivée, recalculable depuis π\*_t et les paramètres ; même motif que le glissement π_t écarté de l'état par l'ADR 0008 (partie II).
- **Facteur réalisé Γ (sur π̄) à la place de Γ^e.** Question de fond tranchée par M27 (lecture (c) : jamais π̄) ; hors de cet ADR.

## Conséquences

- **Pour `moteur/` (J2, J3).** Paramètre typé π\* (« par an, taux de croissance », source : M27, M28, décision du 03/10/2026 ; présent dans au moins un test) ; fonction Γ^e balisée `eq:moteur-croissance-nominale-attendue`, ses dérivées sans label propre ; en phase 1, la reconduction de la cible par le moteur jusqu'à la fiche 8.
- **Pour `etat/` (J2, J3).** Une variable par pays, π\*_t, avec propriétaire, phase d'écriture (1), unité et valeur stationnaire ; la reprise exacte la couvre ; l'invariance d'unité (×100) la laisse inchangée (sans dimension).
- **Tests (J3, fiches 5 et 6, § 9.6, à compléter).** (1) Délai : une cible modifiée au tour n laisse les plans des blocs 5 et 6 du tour n identiques au contrôle apparié et modifie ceux du tour n + 1 (fiche 6 § 9.10, test « Délais » ; fiche 5, levier « Cible π\* ») ; (2) ϱ_L recalculé avec i_L et π\* d'ouverture ; (3) Γ^e identique dans les blocs 5 et 6 (une seule source) ; (4) à cible constante, π\*_t est constante et la trajectoire est celle de l'état résolu.
- **Pour la spécification (`docwriter`, jalons 4 de #41 et #42).** `sec:cadre-calendrier` ou `sec:cadre-phases` : paragraphe « cible d'inflation en vigueur » (variable d'état, lue à l'ouverture, écrite en phase 1) et équation de Γ^e en `equation*` sans label (section proposée) ; `tab:symboles` : π\*_t, Γ^e, γ^e, π^{∗,pas} ; `sec:menages` et `sec:investissement` : « ouverture : π\* » au lieu de « phase 1 : π\* » (fiche 6 § 9.10), délai 1 dans les encadrés `joueur` ; `tab:phases` inchangée.
- **Pour les fiches.** Fiche 8 (branche n° 4) : règle de formation ou levier de la cible, écrit en phase 1 ; quelle cible lisent les ménages dans les régimes B, D et E (J5) ; condition C26 (réouverture de Q10). Fiche 5 : H1 devient une lecture de Γ^e (couche `moteur/`) ; empreinte inchangée (YD_{t−1}). Fiche 6 : Γ̂ remplacé par Γ^e ; empreinte inchangée.
- **Pour `docs/agents/routage.md` § 4.2** (session principale) : le schéma d'état compte la cible en vigueur (ADR 0010).
- **Fichiers.** `docs/feuille-de-route.md` § 4 (ligne M30) ; `CONTEXT.md` : entrée « Cible d'inflation en vigueur (π\*_t) » ; `docs/blocs/README.md` : fiches 5, 6 et 8.
- **Effet sur les résultats.** Aucun : aucun code n'existe ; à cible constante, les trois formes donnent la même trajectoire.
- **Ce que l'ADR ne règle pas.** La loi de π\* et son levier (fiche 8, C1 à C13) ; les régimes de souveraineté (J5) ; le domaine de π\* (coefficient de richesse positif, fiche 5 § 9.2) ; la mesure de l'impulsion et du frein de Fisher au même tour (#54) ; le taux réel sous (G) (#49).
- **Conditions de réouverture.** Une décision citant cette décision, M27 et M28 : si la fiche 8 établit, par une mesure, que le délai d'un tour sur la cible est déterminant pour la stabilité (analogue de la clause II.7 de l'ADR 0008) ; ou si un régime (J5) exige que deux cibles coexistent pour un pays.

Issues : #61 (décision) ; #41, #42 (jalons 4) ; #54 (mesure) ; #24 (volet « banque centrale », fiche 8).
