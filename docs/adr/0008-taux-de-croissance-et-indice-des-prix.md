---
status: proposed
date: 2026-10-03
---

# Taux de croissance et d'inflation convertis géométriquement ; indice des prix égal au prix du tour, lu au tour suivant, dans un registre de 13 niveaux

> Statut « proposé » : rédigé par `architect-approfondi` (Opus, effort `high` ; aucune consultation Fable) le 03/10/2026, sur les décisions M25, lecture (b), et M26, question 1, du mainteneur (fiches `docs/blocs/travail.md` § 8 et `docs/blocs/prix.md` § 8, commit `de91847` ; issues #39, #40 et #24). Il passe à « accepté » sur accord du mainteneur, à la date de cet accord.
>
> Il **révise partiellement l'ADR 0005** (points 4, 16 et 17, et § Conséquences) sans réécrire sa décision ; l'ADR 0005 reçoit une annotation datée qui renvoie ici. Il porte les deux contrats partagés que touchent M25 et M26, et eux seuls : la conversion des taux annuels (partie I) et la phase de l'indice des prix (partie II). Les choix d'option (C et SN pour la fiche 3, M pour la fiche 4) et les autres lectures ne touchent aucun contrat partagé ; ils restent consignés dans les fiches.
>
> **Un seul ADR plutôt que deux**, pour trois motifs :
> - les deux parties répondent aux deux volets de la même issue (#24) ;
> - elles forment une seule chaîne de mesure de l'inflation : la partie I met la cible, l'anticipation et le glissement sur la même échelle, la partie II fixe la date à laquelle ce glissement est lu ;
> - elles ont été décidées le même jour, par paire.
>
> Elles sont numérotées séparément : une réouverture de la partie II (point II.7) la remplacerait par un nouvel ADR sans toucher la partie I.

## Contexte

- **Deux contrats partagés hérités de M22.**
  - *La conversion.* L'ADR 0005 fixe une règle de conversion linéaire unique, x/n_a, « pour les trois natures — taux d'intérêt, flux annuel, vitesse d'ajustement » (pt 4). `sec:cadre-calendrier` en dit deux choses (`nations_et_marches.tex` l. 188) : « c'est la seule conversion du moteur » ; un ratio stationnaire écrit en base annuelle « ne dépend pas de n_a, pourvu que les taux de croissance soient eux aussi écrits en base annuelle linéaire ».
  - *L'empreinte calendaire.* Il fixe aussi une empreinte de 13 variables : l'indice t et un registre de 12 valeurs de l'indice des prix, révisé en phase 1 (pt 16 ; `tab:phases`, l. 504 et 512).
  - Ces deux objets sont des contrats partagés au sens de `docs/agents/routage.md` § 4.2 (la règle de conversion, les phases, le schéma d'état).
- **Les taux de croissance et d'inflation : une nature non classée, puis un état mixte.**
  - M22 ne classe pas ces taux. `sec:cadre-calendrier` le dit (l. 195) et renvoie le traitement des cibles aux fiches « prix » et « banque centrale et anticipations » (issue #24).
  - M24 (f) convertit ensuite linéairement la croissance de productivité : g_pr/n_a par pas, croissance effective publiée de 2,0184 % pour 2 % (`sec:production`, l. 591, 616, 741 et 783).
  - Le visa du mainteneur du 03/10/2026 sur la fiche 2 lit au contraire π̄ comme un glissement annuel : les prix montent de (1 + π̄)^{1/n_a} − 1 par pas (l. 678, 722, 731, 734).
  - La spécification mêle donc déjà une croissance des volumes linéaire et une croissance des prix géométrique.
- **Ce que les fiches 3 et 4 ont établi.** La règle de salaire SN retenue par M25 n'est exacte et indépendante des vitesses que si la productivité, la population active et l'anticipation sont converties de la même façon (fiche 3, § 3.N-4). Le mainteneur a exclu la forme mixte (productivité linéaire, anticipation géométrique) avant la fin de l'instruction. Restaient deux lectures communes aux fiches 3, 4 et 8 : (L), linéaire pour tous les taux, et (G), géométrique pour les taux de croissance et d'inflation. Les mesures ci-dessous viennent de la fiche (§ 3.N-4) et de l'avis de `monnaie` (§ 6.1, Q3) ; `architect` les a remesurées le 03/10/2026 (commande au § Conséquences).
  - *Sous (L)* :
    - une cible de 2 % donne un glissement effectif de 2,0151 / 2,0184 / 2,0197 % à n_a = 4 / 12 / 52 ;
    - l'anticipation stationnaire exacte de SN vaut n_a[(1 + π̄)^{1/n_a} − 1], soit 1,9819 % à n_a = 12, et non π̄ ;
    - le critère 9 (a) de la fiche 3 devrait être transposé. La fiche 8 devrait former une anticipation en taux linéaire, ou convertir le glissement, qui est « mesuré, jamais converti ».
  - *Sous (G)* :
    - la cible, l'anticipation et le glissement sont sur la même échelle : « 2 % » veut dire 2 % ;
    - les critères 3 (b) et 9 (a) de la fiche 3 sont tenus tels qu'ils sont écrits ;
    - en revanche, un ratio stationnaire qui combine un taux de flux linéaire et une croissance géométrique dépend légèrement de n_a. Exemple : K/(n_a I) = 1/(n_a[(1 + g)^{1/n_a} − 1] + δ) vaut 14,3160 / 14,3228 / 14,3253 à n_a = 4 / 12 / 52 (g = 2 %, δ = 5 %), contre 14,2857 pour tout n_a sous (L).
- **La phase de P_t.** Sous M24, le bloc 4 écrit le prix p_t en phase 5 ; sous le contrat de l'ADR 0005, l'indice est révisé en phase 1. La fiche 4 (§ 1.5, Q1 ; § 3.N-1) a instruit trois lectures :
  - (a) P_t ≡ p_{t−1}, arrêté en phase 1 : aucun texte révisé, mais l'indice a un tour de retard sur son prix ;
  - (b) p_t fixé en phase 1, P_t ≡ p_t : délai nul pour la règle de taux, au prix d'une révision de M24 et de `tab:phases` ;
  - (c) P_t ≡ p_t, arrêté avec le prix du tour et lu en phase 1 du tour suivant.

  (a) et (c) donnent des trajectoires identiques (constat 1 du § 3.N-1) : elles ne diffèrent que par l'étiquette de l'indice et sa restitution. Sous (c), la règle de taux lit le glissement du tour précédent, π_{n−1} = p_{n−1}/p_{n−13} − 1. Il faut donc **13 niveaux de prix**, un de plus que le registre de l'ADR 0005, ou 12 niveaux plus le glissement porté en variable d'état. Les deux experts se sont exprimés sur cette forme :
  - `macro` décrit (c) avec π_t en état (fiche 4, § 3.N-1 et § 5) ;
  - `monnaie` exprime une préférence faible pour un registre de 13 niveaux, « une seule source nominale […] d'où se recalculent le glissement et la variation sur le tour », et laisse la forme à `architect` (fiche 4, § 6.1, Q1, point 5).
- **Pourquoi maintenant.** Plusieurs travaux en dépendent :
  - les sections `sec:travail` et `sec:prix` (jalons 4 de #39 et #40) placent chaque équation dans sa phase et écrivent leurs conversions ;
  - la fiche 6 (#42) doit recalculer ρ̄_K ;
  - la fiche 8 (branche n° 4) part de la lecture (G) (condition C4) et de la phase de lecture (conditions C9, C10 et C12).

  Le moteur v3 n'exécute encore rien : aucune de ces décisions ne change un résultat.

## Décision

**M25, lecture (b), et M26, question 1, arrêtées par le mainteneur le 03/10/2026** (fiches `docs/blocs/travail.md` § 8 et `docs/blocs/prix.md` § 8, commit `de91847`). Ce sont des décisions citant M22 et M24. La **forme** du point II.3 (registre de 13 niveaux) est proposée par `architect` ; elle prend effet avec l'acceptation de cet ADR. Statut de tous les points : **choix de conception**.

### Partie I — Conversion des taux de croissance et d'inflation (lecture (G), commune aux fiches 3, 4 et 8)

**I.1. Deux conversions, selon la nature du taux.**
- Les taux d'intérêt, les flux annuels et les vitesses d'ajustement restent convertis par la règle linéaire de M22, x/n_a par pas (`eq:moteur-conversion-taux` ; ADR 0005, pt 4, inchangé).
- Les **taux de croissance et d'inflation** sont convertis **géométriquement**. Ce sont les taux annuels d'évolution d'un niveau (volume, productivité, population active, prix), qu'ils soient tendanciels, stationnaires, anticipés ou visés : g_pr, g_N, g, π̄, π^e, π\*. Un taux annuel x donne le facteur par pas (1 + x)^{1/n_a} : un niveau qui croît au taux x croît exactement de x en n_a pas.
- L'écriture logarithmique, ln(1 + x)/n_a par pas, est équivalente et admise. Aucune autre écriture n'est admise pour un taux de croissance ou d'inflation, en particulier ni x/n_a ni 1 + x/n_a.

**I.2. Critère de nature.**
- Un taux appliqué à un encours pour produire un flux du pas (intérêt, amortissement δ, taux de prélèvement) est un taux de flux : il se convertit linéairement.
- Un taux qui décrit l'évolution d'un niveau d'un pas à l'autre est un taux de croissance : il se convertit géométriquement.
- Chaque fiche classe et déclare les taux annuels de ses équations selon ce critère. Un cas douteux est soumis au mainteneur avec la fiche, jamais tranché dans le code.

**I.3. Une seule écriture de chaque conversion.**
- La conversion géométrique est écrite une fois dans `sec:cadre-calendrier`, par une équation propre, et n'est recalculée nulle part ailleurs. Label proposé : `eq:moteur-conversion-croissance`, posé au J2 avec sa balise, comme `eq:moteur-conversion-taux`.
- Dans `moteur/` (ADR 0002, couche 3), la nature d'un taux est portée par le **type** du paramètre, c'est-à-dire par son unité déclarée (« par an, taux de croissance » ou « par an, taux de flux »). La conversion appliquée se déduit de ce type, jamais du site d'appel.
- Aucune fonction de conversion ne prend la nature en argument : ce serait un drapeau de mode au sens de l'ADR 0002.

**I.4. Mesures et restitution.**
- Le glissement annuel π_t est mesuré, jamais converti (inchangé).
- Toute annualisation d'une variation par pas d'un niveau, qu'elle soit restituée au joueur ou comparée à un taux annuel, est géométrique : (1 + v)^{n_a} − 1, inverse du point I.1.
- Le taux réel restitué et testé reste r = i − π (ADR 0005, pt 5, conditions de `monnaie`).

**I.5. Révision de M24 (f).**
- La croissance de productivité est convertie selon le point I.1 : pr_{t+1} = pr_t (1 + g_pr)^{1/n_a}.
- La croissance tendancielle s'écrit g = (1 + g_pr)(1 + g_N) − 1.
- La croissance effective de 2,0184 % pour g_pr = 2 % n'existe plus ; elle n'est plus publiée.
- Les autres lectures de M24 sont inchangées.

**I.6. Dépendance à n_a, déclarée.**
- Sous (G), un ratio stationnaire qui combine un taux de flux linéaire et une croissance géométrique dépend de n_a. Exemple du Contexte : K/(n_a I) varie de 14,3160 à 14,3253 entre n_a = 4 et n_a = 52.
- Ces ratios restent indépendants des vitesses.
- n_a est fixé à 12 par M22 (ADR 0005, pt 18). Cette dépendance est donc une propriété déclarée et chiffrée du cadre, non une dérive.
- Elle s'ajoute aux deux grandeurs déjà déclarées de `sec:cadre-calendrier`. Contrairement à elles, elle touche l'état d'arrivée, par la durée du pas, jamais par une vitesse.

### Partie II — Phase de l'indice des prix (lecture (c) de la question 1 de la fiche 4)

**II.1. L'indice est le prix du tour.**
- Sous J = 1, P_t ≡ p_t, le prix que le bloc 4 écrit en phase 5 du pas t (M24, M26).
- Le bloc 4 n'écrit rien en phase 1.
- À J ≥ 2, P_t sera un agrégat des p_{j,t}, dont la définition reste à fixer (fiche 4, critère 9 (c)). Elle ne changera pas la phase.

**II.2. Les règles le lisent au tour suivant.**
- En phase 1 du pas t, les règles (salaires, anticipations, règle de taux) lisent l'état d'ouverture : le dernier prix connu P_{t−1} et le glissement du tour précédent, π_{t−1} = P_{t−1}/P_{t−1−n_a} − 1.
- Le délai entre un mouvement du prix et sa lecture par une règle est d'**un tour**. Au moment de décider, la règle a la même information que le joueur (condition C9 de la fiche 4).
- La définition du glissement, π_t = P_t/P_{t−n_a} − 1, est inchangée. Le glissement du tour t est calculable dès la phase 5 du pas t, pour la restitution.

**II.3. Forme : un registre de n_a + 1 = 13 niveaux.**
- À l'ouverture du pas t, le registre de l'indice des prix tient les 13 niveaux P_{t−1}, …, P_{t−13}.
- Il est avancé en phase 9 : P_t y entre, P_{t−13} en sort. C'est la clôture, où `tab:phases` place déjà la « mise à jour du registre ».
- Le glissement, la variation sur le tour et toute mesure de l'inflation sur une fenêtre d'au plus n_a tours sont des **fonctions du registre**, calculées à la lecture. Aucune n'est une variable d'état.
- Valeur stationnaire explicite : P_{t−u} = P_t (1 + π̄)^{−u/n_a}, u = 1, …, n_a + 1.

**II.4. Empreinte calendaire de l'état : 14 variables**, l'indice t et 13 niveaux, au lieu de 13 (ADR 0005, pt 16). Le registre reste une variable d'état retardée de longueur fixe, jamais un historique ; aucun compteur caché.

**II.5. Phases.**
- La phase 1 lit le registre et ne révise plus l'indice.
- La phase 5 écrit le prix du tour, qui est l'indice.
- La phase 9 avance le registre.
- Le bloc 4 n'écrit pas en phase 1. Au titre de l'indice, l'ordre interne de la phase 1 ne contraint donc ni le bloc 3 ni le bloc 8 (fiche 4, § 3.N-1, « Ordre interne de la phase 1 »).
- La date de formation de π^e (condition C12) reste à la fiche 8.

**II.6. Dernier prix connu.**
- Toute règle qui lit un niveau de prix en phase 1 lit P_{t−1}, première entrée du registre : c'est le cas de la règle de salaire de la fiche 3 (constat T2 de la fiche 4, § 6.1, Q6).
- Lire P_{t−2} à la place serait un défaut : U* se déplacerait de −ln(1 + π̄)/(n_a β).

**II.7. Clause de réouverture vers (b)** (avis de `monnaie`, fiche 4, § 6.1, Q1, point 4 ; M26).
- *Condition.* La question 1 est rouverte vers (b) si l'analyse de stabilité de la fiche 8 (condition C10) montre que le délai d'un tour est déterminant à la calibration retenue. Le critère est écrit dans la fiche 8 avant l'essai.
- *Forme.* La réouverture est une décision citant M26, M24 et M22. Un nouvel ADR remplace alors la partie II. Il révise aussi le contrat de M24 : p_t (phase 5) et UC (phase 2) passent en phase 1, et le registre revient à n_a niveaux.
- *Coût.* Sous M, ce passage ne serait qu'un réordonnancement, puisque p_t ne lit que l'ouverture (fiche 4, § 6.1, Q1, point 4).

## Options écartées

### Partie I

- **(L), linéaire pour tous les taux** (conforme à M22 et à M24 (f)). Elle garde les ratios stationnaires indépendants de n_a. Mais l'inflation et la croissance effectives dépendent alors de n_a et diffèrent des taux affichés, avec quatre conséquences :
  - le joueur verrait un glissement de 2,0184 % pour une cible de 2 % (10,4713 % pour 10 %) ;
  - toute loi de crédibilité qui compare le glissement à la cible sanctionnerait un écart permanent, de 0,47 point à 10 % (`monnaie`, fiche 3, § 6.1, Q3) ;
  - la fiche 8 devrait apprendre soit sur un glissement converti géométriquement (la formule géométrique serait déplacée, non supprimée), soit sur une variation mensuelle bruitée ;
  - le critère 9 (a) de la fiche 3 devrait être transposé après l'instruction.

  Le jeu affiche l'inflation et la croissance au joueur, et n_a est fixé : l'arbitrage favorise (G). Sous (G), la dépendance à n_a quitte les grandeurs restituées pour les ratios du test zéro, où elle est déclarée et invisible pour le joueur.
- **Forme mixte** (productivité linéaire, anticipation géométrique). SN y échoue au critère 4 de la fiche 3 (U* fonction de λ_w). Exclue par le mainteneur avant la fin de l'instruction (fiche 3, § 3.N-4).
- **Conversion géométrique de tous les taux, intérêts compris** (la « conversion composée » des options écartées de l'ADR 0005). Non rouverte : les intérêts versés dans l'année deviendraient inexacts (3,9285 % pour 4 % à 12 pas, ADR 0005, Contexte), et une vitesse λ ≥ 1 par an n'aurait pas d'équivalent. La partie I ne vise que les taux que M22 n'avait pas classés ; M24 (f), qui en avait classé un, est révisée.
- **Une seule fonction de conversion avec un argument de nature.** La classification se ferait au site d'appel, et un argument choisirait entre deux comportements : c'est un drapeau de mode (ADR 0002). Le type du paramètre porte la nature une fois pour toutes (point I.3).

### Partie II

- **(a) P_t ≡ p_{t−1}, arrêté en phase 1** (repli de `macro` et de `monnaie`). Ses trajectoires sont identiques à celles de (c) et aucun texte n'est révisé. Mais elle n'a que des inconvénients en échange :
  - l'indice restitué au tour n est le prix du tour n − 1 ;
  - l'empreinte est la même, puisque le prix p_{t−1} doit être tenu en état ;
  - elle tend le piège T2 : une règle qui lit P_{t−1} au lieu de P_t déplace U*, et ce déplacement dépend de n_a.
- **(b) p_t fixé en phase 1, P_t ≡ p_t.** Le délai est nul pour la règle de taux, mais elle cumule les coûts :
  - elle révise M24 (p_t en phase 5), `tab:phases` et la phase de UC ;
  - la règle de taux lirait une inflation que le joueur ne voit pas avant de décider : en multijoueur, cette asymétrie profiterait à un pays non joué ;
  - elle exclut toute règle de prix qui lit les phases 2 à 4.

  Ni `monnaie` ni `macro` ne la demandent. Elle reste la destination de la clause II.7.
- **(c) avec le glissement π_t porté en variable d'état** (12 niveaux plus π_t ; forme décrite par `macro`, fiche 4, § 3.N-1). Même empreinte (14 variables), mêmes trajectoires. Écartée pour la forme, pour trois motifs :
  - *Une grandeur dérivée invérifiable.* Elle stocke une grandeur dérivée dont la cohérence avec le registre ne se vérifie pas depuis l'état, puisque le niveau P_{t−13} qui la définit en est sorti. Une sauvegarde porterait un π_t que rien ne permet de recontrôler. Sous II.3, toute mesure se recalcule depuis une seule source nominale.
  - *Une contrainte d'ordre qui fuit.* Elle impose un ordre dans la clôture : calculer π_t avant d'avancer le registre. Cette contrainte d'indexation sort du registre ; c'est précisément la classe d'erreur d'un tour que décrit T2. Sous II.3, la lecture du glissement est une fonction du registre, écrite en un seul endroit (localité).
  - *Une mesure figée.* L'analyse C10 de la fiche 8 peut retenir une autre mesure que le glissement de 12 tours : la variation sur le tour annualisée stabilise des cas où le glissement explose (fiche 4, § 6.1, Q1, point 4). Le registre de 13 niveaux fournit toute mesure de fenêtre ≤ n_a sans variable d'état nouvelle ; la forme à π_t stocké demanderait de la remplacer.

  `monnaie` a exprimé une préférence faible pour le registre de 13 niveaux ; `macro` n'a pas motivé la forme à π_t contre elle, il la décrit comme l'empreinte de (c). Le désaccord porte sur la forme, non sur le fond, puisque les trajectoires sont les mêmes. Le mainteneur peut retenir π_t en état en refusant le point II.3 lors de l'acceptation.

## Conséquences

- **Pour `sec:cadre-calendrier`.** Rédaction par `docwriter` dans les sections de #39 et de #40 (décision citant M22), en un commit `docs:` propre au cadre si la session préfère isoler le contrat :
  - paragraphe « Règle de conversion linéaire unique » (l. 184 à 188) :
    - titre et texte ramenés aux deux conversions du point I.1 ;
    - « c'est la seule conversion du moteur » devient « c'est la seule conversion des taux de flux et des vitesses » ;
    - la phrase « un ratio stationnaire écrit en base annuelle ne dépend pas de n_a, pourvu que les taux de croissance soient eux aussi écrits en base annuelle linéaire » est retirée ;
  - paragraphe sur les taux de croissance (l. 195) : remplacé par l'énoncé de la conversion géométrique (`eq:moteur-conversion-croissance`, sans label avant le J2) ; le chiffre de 2,0184 % est retiré ;
  - « Deux grandeurs qui dépendent de n_a » (l. 190 à 194) : une troisième s'y ajoute, la dépendance des ratios mixtes (point I.6), chiffrée par l'exemple K/(n_a I) ;
  - « Date de décision » (l. 182) : l'indice des prix n'est plus révisé en phase 1 ; les règles y lisent le glissement du tour précédent (points II.2 et II.5) ;
  - « Empreinte calendaire de l'état » (l. 199 à 203) : registre de 13 niveaux P_{t−1}, …, P_{t−13}, soit 1 + 13 = 14 variables ; valeur stationnaire pour u = 1, …, n_a + 1 ; glissement lu en phase 1 sur π_{t−1} ;
  - « Ratio stationnaire au PIB annuel » (l. 205 à 209) : le facteur s'écrit avec (1 + g)^{1/n_a} au lieu de 1 + g/n_a. Il vaut **1,0108** au lieu de 1,0109 pour g = 2 % (remesuré : 1,010768 sous (G), 1,010866 sous (L)) ;
  - `tab:phases` (l. 504 et 512) : en ligne 1, « indice des prix et glissement annuel (registre) » devient une lecture du registre ; en ligne 5, le bloc prix écrit le prix du tour, qui est l'indice ; la ligne 9 est inchangée ;
  - `tab:symboles` (l. 1147) : P_t, « le registre en tient les n_a + 1 valeurs précédentes » ;
  - « Provenance » du paragraphe : M22, M25 et M26.
- **Pour `sec:production`** (révision de M24 (f)). `docwriter` intervient après le recalcul de `macro`, mené en parallèle :
  - chiffres à retirer :
    - l. 591 : conversion linéaire de g_pr et 2,0184 % ;
    - l. 616 : forme de g ;
    - l. 741 : paragraphe « Croissance », d'où 2,0184 % et 1,9819 % sont retirés ;
    - l. 783 : glissement de 2,0184 % de la production ;
  - formes fermées et récurrences écrites avec g/n_a, à recalculer sous (G) :
    - l. 617 ;
    - l. 676 à 678 (ρ̄_K) ;
    - l. 722 à 734 (y/v, ρ̄_IN, ΔIN) ;
    - l. 757 (valeur propre) ;
  - **ρ̄_K = 0,7791**, transmis à la fiche 6 et visé par le mainteneur le 03/10/2026, est à recalculer. Une valeur qui change est reportée avec son tableau avant / après dans la fiche 2 (§ 9) et soumise au visa : une fiche décidée ne se réécrit pas sans lui ;
  - phase de UC (M26, Q2) : phase 2, à reporter dans `sec:production-phases`.
- **Pour `CONVENTIONS.md`** (`docwriter`) :
  - § 5.2, « Taux » : la conversion au pas est donnée par deux équations de `sec:cadre`, `eq:moteur-conversion-taux` et `eq:moteur-conversion-croissance`, jamais recalculées localement ;
  - § 6 :
    - la « seule règle linéaire » est limitée aux taux d'intérêt, aux flux et aux vitesses ;
    - la conversion géométrique des taux de croissance et d'inflation (M25) est ajoutée ;
    - la phrase finale devient « changer n_a, n_m ou une règle de conversion demande une décision M-m citant M22 ».
- **Pour l'ADR 0005.** Une annotation datée du 03/10/2026 renvoie au présent ADR, sans réécrire la décision. Elle porte sur les points 4, 16 et 17 et sur deux phrases du § Conséquences : « `eq:moteur-conversion-taux` est la seule conversion » et « le schéma porte t et le registre de 12 valeurs ». Le point 5 reste exact pour les deux grandeurs qu'il nomme.
- **Pour `docs/agents/routage.md` § 4.2** (hors du périmètre d'écriture d'`architect` ; commit `docs:` de la session principale) :
  - la liste des contrats partagés nomme la règle de conversion `eq:moteur-conversion-taux` ; y ajouter la conversion géométrique `eq:moteur-conversion-croissance` (M25) ;
  - préciser le registre de l'indice des prix (13 niveaux, ADR 0008) au titre du schéma d'état.
- **Pour `moteur/` et `etat/`** (J2) :
  - deux fonctions de conversion, chacune balisée ;
  - des paramètres typés dont l'unité porte la nature du taux (point I.3) ;
  - le registre est un objet d'état de 13 niveaux, avancé en phase 9. Ses lectures (dernier prix, glissement, variation sur le tour) sont les seules fonctions qui l'indexent ;
  - le test d'invariant de la reprise à la frontière de tour est inchangé ;
  - le test d'invariance d'unité sous ×100 (ADR 0005, pt 19) est étendu au registre : glissement identique à 1e−10 près en relatif.
- **Pour les fiches suivantes.**
  - Fiche 8 : elle part de (G) (condition C4 : cible comparée au glissement, π^e en glissement anticipé, stockage éventuel de ln(1 + π^e)) et de la lecture à un tour (C9, C10, C12). Elle écrit avant l'essai le critère de la clause II.7.
  - Fiches 5, 6, 7 et 9 : chacune classe les taux annuels de ses équations selon le point I.2. La fiche 6 reçoit ρ̄_K recalculé.
  - Fiche 3 : la population active croît de (1 + g_N)^{1/n_a} par pas (M25 (d)).
- **Fichiers** :
  - `docs/feuille-de-route.md` § 4 (lignes M25 et M26) ;
  - `docs/blocs/README.md` : fiches 3 et 4 « décidées » ; fiches 1 et 2, contrat révisé ;
  - `CONTEXT.md` : « Règle de conversion », « Date de décision », « Registre de l'indice des prix », « Empreinte calendaire de l'état » ;
  - `CLAUDE.md` : inchangé.
- **Effet sur les résultats.** Aucun : le moteur v3 n'exécute rien.
  - Certains chiffres publiés de la spécification changent : 2,0184 %, 1,0109, ρ̄_K et les formes de la fiche 2. Ce sont des formes fermées de sections proposées ; `macro` les recalcule, et ils sont visés comme le prévoit `CLAUDE.md` pour un état stationnaire de référence.
  - Aucune table de flux ni de bilans n'est touchée : la sortie de `verifier_matrices.py --strict` ne doit pas changer.
- **Mesures citées.** `uv run python -`, exécuté le 03/10/2026 par `architect`, pour g = 2 % et δ = 5 % :

  | Grandeur | Lecture | n_a = 4 | n_a = 12 | n_a = 52 |
  |---|---|---|---|---|
  | K/(n_a I) | (G) | 14,3160 | 14,3228 | 14,3253 |
  | K/(n_a I) | (L) | 14,2857 | 14,2857 | 14,2857 |
  | Facteur du ratio restitué | (G) | 1,012438 | 1,010768 | 1,010126 |
  | Facteur du ratio restitué | (L) | 1,012531 | 1,010866 | 1,010226 |
  | Croissance effective pour 2 % | (L) | 2,0151 % | 2,0184 % | 2,0197 % |

  Hausse par pas pour 2 % sous (G), à n_a = 12 : 0,16516 %.
- **Ce que l'ADR ne règle pas** :
  - la loi de formation de π^e, la règle de taux, la mesure d'inflation qu'elle lit et la date de formation de π^e (fiche 8, conditions C1 à C13) ;
  - la définition de P_t à J ≥ 2 ;
  - la classification des taux des fiches 5 à 9 (point I.2), faite par chaque fiche ;
  - la variable de fermeture du niveau d'activité (#44).
- **Conditions de réouverture.**
  - Partie II : clause II.7.
  - Partie I : une décision M-m citant M25, M24 et M22, dans deux cas : une fiche établit, par une mesure, qu'une grandeur restituée ou un critère du test zéro dépend de n_a d'une façon que le point I.6 ne couvre pas ; ou n_a change (décision citant M22), et les dépendances déclarées doivent alors être remesurées.

Issues : #24 (les deux volets : le volet « prix » est tranché ici, le volet « banque centrale » reste à la branche n° 4), #39 (M25), #40 (M26), #17 (ADR 0005, révisé en partie), #34 (M24 (f), révisée).
