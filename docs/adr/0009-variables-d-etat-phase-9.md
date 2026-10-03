---
status: accepted
date: 2026-10-03
---

# Variables d'état du pas suivant assises sur les flux du pas : les blocs déclarés les écrivent en phase 9, sans flux, après les identités du noyau et avant le passage au pas suivant

> Statut « accepté » : décision M29 du mainteneur du 03/10/2026, acceptée sur le fond (fiches `docs/blocs/menages.md` et `docs/blocs/investissement.md` § 9.10, commit `efb6bcd`), prenant effet avec la présente rédaction. Rédigé par `architect` (Opus) le 03/10/2026 sur le constat 1 de la fiche « investissement et financement » (§ 9.8, point 2 (b)) et sur le contrat 1 de la fiche « ménages » (§ 9.8) ; relu et amendé le même jour par `architect-approfondi` (Fable, consultation 1 sur 3 de la branche n° 3b, accord du mainteneur du 03/10/2026 ; `docs/agents/routage.md` § 4.1, point 3 : ADR d'architecture). Il **complète l'ADR 0005 (point 15) sans le réécrire**, **précise l'ADR 0002** (couche 2, interface bloc → noyau) et laisse inchangés l'ADR 0007 et l'ADR 0008 (partie II). Forme retenue : un ADR nouveau plutôt qu'une annotation de l'ADR 0005, pour le motif de l'ADR 0007 : un contrat partagé (les phases de l'ordonnanceur) reçoit un point nouveau, avec ses options écartées et ses conséquences pour le jalon J2.

## Contexte

- **Le contrat des phases.** M22 (ADR 0005, point 15) fixe neuf phases triangulaires. La phase 9, « clôture », n'a pour écrivains que le noyau (identités par pas et cumulée, double calcul des valeurs nettes, Res ≥ 0) et le moteur (mise à jour du registre, passage à t + 1) : `tab:phases`, ligne 9 (`docs/specification/nations_et_marches.tex`, l. 512). Un bloc ne lit que l'état d'ouverture, des variables d'une phase antérieure du même pas ou, dans sa propre phase, des variables produites avant lui dans l'ordre d'exécution déclaré (l. 487 ; ADR 0007).
- **Le fait nouveau (M28).** La règle de financement F anticipe l'impôt des entreprises : T̂_{F,t} = Γ·T_{F,t−1} (F4, `eq:investissement-impot-anticipe`, label prévu au J3 ; fiche 6 § 9.1). T_{F,t−1} est une variable d'état du bloc 6 (§ 9.4). T_{F,t}, ligne 7 de `tab:matrice-flux`, colonne des entreprises (l. 324), est exécutée en phase 6 sur la proposition du bloc 9 (`tab:phases`, ligne 6). Or le bloc 6 ne siège après le bloc 9 dans aucune phase :
  - la phase 6 n'a pas d'ordre interne, et F3 ne doit pas y lire T_F du pas (fiche 6, critère 3 (d) ; § 9.4, « Triangularité ») ;
  - le bloc 6 n'écrit dans aucune phase postérieure à la phase 6 ;
  - la phase 9 n'a pas d'écrivain de type bloc.
- **Le même besoin ailleurs.**
  - YD_t (H7, `eq:menages-revenu-disponible`, M27) : somme des montants exécutés des lignes 5, 6, 7, 10, 11a, 14 et 15 de la colonne des ménages, « lus au grand livre, jamais recalculés » (fiche 5 § 9.1). La fiche 5 le plaçait en phase 7 (§ 9.4), où les ménages ne proposent plus aucune ligne sous B_H ≡ 0 (M27) et où l'ordre C25 (État, puis banque centrale, puis banque) ne les contient pas.
  - i_L et i_D du bloc 7, « écrits en phase 8 (c) ou à la clôture, publiés à l'ouverture » (C27 ; fiche 6 § 9.4).
- **Ce qu'en disent les experts.** `macro` recommande la lecture (i), « une seule déclaration pour tous les blocs, sans ordre nouveau » (fiche 6 § 9.8, point 2 (b)) ; `jeu` n'est pas consulté (aucun mécanisme visible par le joueur : les trois lectures donnent les mêmes trajectoires au socle).
- **Pourquoi maintenant.** Les sections `sec:menages` et `sec:investissement` (jalons 4 de #41 et #42) placent chaque équation dans sa phase, et `docwriter` ne passe qu'une fois par branche (règle 9). L'ordonnanceur (J2) n'existe pas : la décision ne change aucun code.

## Décision

**M29, arrêtée par le mainteneur le 03/10/2026** (fiches 5 et 6, § 9.10, commit `efb6bcd`), décision citant M22, M27 et M28. Statut de tous les points : **choix de conception**.

1. **État d'ouverture figé, propriétaire unique, écriture unique.**
   - L'**état d'ouverture** du pas t est une lecture figée : il n'est jamais modifié pendant le pas. Il se distingue des **positions courantes** du grand livre (clôture = ouverture + lignes exécutées, phase après phase ; ADR 0005, points 8 et 10), tenues par le noyau, qui ne sont pas l'état d'ouverture.
   - Chaque variable d'état a **un propriétaire déclaré** : le **noyau** pour les postes des matrices, mis à jour par les seules lignes de flux exécutées ; le **moteur** pour l'empreinte calendaire (indice t, registre de l'indice des prix ; ADR 0008, II.3) ; **un bloc** pour chacune des variables d'état de bloc (ti, y_{t−1}, T_{F,t−1}, YD_{t−1}, v^e, i_L, i_D, …).
   - Une variable d'état de bloc ou du moteur reçoit sa valeur du pas suivant **exactement une fois dans le pas**, de son propriétaire, dans la phase qu'il déclare. Cette valeur est une variable du pas t, lisible par les phases suivantes sous son indice daté **si la fiche du lecteur déclare cette lecture** dans son tableau de phases (exemple : v^e_{t+1}, écrite en phase 5 par le bloc 2, lue en phase 6 par F2) ; à défaut, un bloc lit la valeur d'ouverture (exemple : la cible d'inflation en vigueur, lue à l'ouverture par les blocs 5 et 6, décision du 03/10/2026, ADR 0010).
   - Le moteur assemble l'état du pas t + 1 au passage de la phase 9. C'est une précision de l'ADR 0002, couche 2 (« un bloc lit l'état d'ouverture et rend des flux proposés et des variables nouvelles »).
2. **Groupe de mise à jour de la phase 9.** Un bloc peut écrire en phase 9 ses variables d'état du pas suivant, aux conditions suivantes :
   - il ne propose aucun flux ; un flux proposé en phase 9 est refusé par l'ordonnanceur ;
   - il lit l'ouverture, les variables des phases 1 à 8 et les **montants exécutés** du pas, au grand livre clos par le noyau, en lecture seule ;
   - il ne lit aucune écriture d'un autre bloc dans la phase 9 ;
   - il n'écrit rien d'autre que des variables du schéma d'état.
   La phase 9 s'exécute dans l'ordre suivant, entre couches : **noyau** (identités par pas et cumulée, double calcul des valeurs nettes, Res_{t+1} ≥ 0), **puis blocs** (groupe sans lecture mutuelle, appelés dans l'ordre déclaré), **puis moteur** (avancée du registre, ADR 0008, II.3, puis passage à t + 1). Un bloc qui lit le registre en phase 9 lit donc celui d'ouverture.
3. **Déclaration statique.** Chaque fiche déclare dans son tableau de phases les variables qu'elle écrit en phase 9 ; `tab:phases` liste les blocs du groupe dans la cellule « Écrivent » de la ligne 9, et l'ordonnanceur lit cette déclaration comme celle des phases 1, 4, 5 et 7 (ADR 0007, point 4). Le groupe ne dépend ni des données du pas ni de l'ordre des joueurs.
4. **Où écrire une variable d'état.** Un bloc écrit la valeur suivante d'une variable d'état dans une phase où il siège **après toutes ses entrées** : c'est le cas de ti_{t+1} (S6) et de y_t retenu comme y_{t−1} (bloc 6, phase 5), de v^e_{t+1} (bloc 2, phase 5), de la cible en vigueur (bloc 8, phase 1 ; ADR 0010). Si aucune de ses phases ne convient, il l'écrit en phase 9. Une variable assise sur un **montant exécuté** se lit au grand livre, après l'exécution, jamais sur la proposition d'un bloc.
5. **Application aux fiches décidées.**
   - Fiche 6 (M28) : en phase 9, le bloc 6 retient T_{F,t}, montant exécuté de la ligne 7, colonne des entreprises, comme T_{F,t−1} du pas suivant. F4 reste en phase 6 et lit l'ouverture (fiche 6 § 9.10).
   - Fiche 5 (M27) : H7 s'exécute en phase 9, sur les montants exécutés du pas, au lieu de la phase 7 (fiche 5 § 9.10). **Les ménages sortent des écrivains de la phase 7 au socle** (B_H ≡ 0) ; les lignes 19a-ménages et 19b-ménages restent à montant nul, sans retrait (fiche 5 § 9.8, point 4).
   - Fiche 7 (branche n° 4) : elle déclare la phase de i_L et i_D selon le point 4 ; la phase 8 (c), où le bloc 7 siège après i_CB du pas, est désignée si toutes ses entrées la précèdent ; sinon la phase 9 (C27).
6. **Inchangé.** La numérotation et le contenu des phases 0 à 8 ; les lignes de flux et leurs phases ; `tab:matrice-bilans`, `tab:matrice-flux` et `tab:portes-monnaie` ; l'empreinte d'état des blocs 5 et 6 (une et trois variables) ; le point 3 de l'ADR 0005 (frontière de tour).

## Options écartées

- **(ii) Ajouter le bloc 6 (et garder le bloc 5) aux écrivains de la phase 7.** Écartée pour la localité et la lisibilité du contrat :
  - un bloc deviendrait écrivain d'une phase (« titres publics ») où il ne propose aucun flux ;
  - chaque besoin futur ajouterait un bloc à une phase sans rapport avec lui ;
  - sous B_H ≡ 0, l'ordre C25 de la phase 7 ne contient plus les ménages ;
  - une ligne exécutée après la phase 7, si le J5 ou le J6 en ajoute une dans la colonne des ménages, échapperait à H7.
- **(iii) T_{F,t−1} tenu par le bloc 9 et lu à l'ouverture par le bloc 6.** Écartée pour trois raisons :
  - dans sa phase, le bloc 9 ne connaît que sa proposition, pas le montant exécuté ; au socle ils coïncident (aucune ligne nommée de part non payée, D_F ≥ 0 inactive), mais une ligne nommée de part non payée (J6, #57) les ferait diverger en silence ;
  - l'ensemble d'information de l'anticipation F4 appartient au bloc 6 : toute révision de cette anticipation (lissage, forme adaptative) toucherait le bloc 9 ;
  - elle ne couvre pas un agrégat que le lecteur doit calculer (YD_t).
- **Ordre interne de la phase 6 (État, banque, puis investissement).** Il permettrait à F3 de lire T_F du pas, ce qui rouvrirait le fond de M28 (critère 3 (d)) ; il ne sert ni YD_t ni i_L, i_D.
- **Registre des flux du pas précédent tenu par le noyau** (les 62 termes de `tab:matrice-flux`, avancés en phase 9). Forme parente du registre des prix, mais elle porte dans l'état tous les flux pour deux usages et les rend lisibles par tous les blocs : l'interface s'élargit sans motif ; elle ne sert pas non plus i_L, i_D.
- **Mise à jour par le moteur au passage à t + 1**, d'après une table « variable du pas → variable d'état » tenue dans `moteur/`. La règle de mise à jour d'un bloc sortirait de son module, et une équation de la spécification (H7) serait exécutée hors de son bloc.
- **Règle stricte « une valeur du pas suivant n'est lisible qu'au pas suivant ».** Elle interdirait F2 (v^e_{t+1} lue en phase 6, fiche 6 § 3.N) et obligerait à dédoubler toute variable écrite en cours de pas en une variable du pas et une variable d'état. Le point 1 retient la lecture déclarée par la fiche du lecteur.
- **Une phase 10 « mise à jour des états ».** Elle renuméroterait la phase 9 de M22 (ADR 0005, point 15), `CONTEXT.md` et les fiches, pour exprimer ce qu'un groupe déclaré dans la phase 9 exprime déjà (motif de l'ADR 0007, « scinder la phase 4 »).
- **Sous-phases 9 (a), (b), (c)** (noyau, blocs, moteur). Les sous-phases de la phase 8 ordonnent des **lignes de flux** (12, 13, puis 16, puis 21) ; la phase 9 n'en exécute aucune. L'ordre « noyau, puis blocs, puis moteur » est un ordre entre couches, écrit par « puis » dans la cellule, comme l'ordre des blocs de la phase 4 (ADR 0007, annotation du 03/10/2026).
- **Lecture du flux du pas précédent dans `observation/`.** Interdite par l'ADR 0002 (couche 5 : séries hors de l'état, sans effet sur la trajectoire ; test de suppression) ; un bloc qui lirait une série ferait dépendre la trajectoire de l'observation.

## Conséquences

- **Pour `noyau/` (ADR 0002, couche 1 ; ADR 0005, § Conséquences).** L'interface étroite reçoit une opération de **lecture seule** : le montant exécuté d'une ligne ℓ de `tab:matrice-flux`, pour une colonne s, dans le pas courant, disponible après la clôture de la phase qui exécute la ligne. Le grand livre reste le seul lieu d'exécution ; aucun bloc n'y écrit. Cette lecture est celle de H7 (fiche 5 § 9.1) et du point 5 ; elle précise le contrat « état d'ouverture lu, flux proposés rendus » de `docs/agents/routage.md` § 4.2.
- **Pour `moteur/` (ordonnanceur, J2 ; ADR 0002, couche 3).**
  - La déclaration phase → séquence ordonnée de blocs (ADR 0007) comprend le groupe de la phase 9, placé entre le noyau et le moteur.
  - L'interface du bloc distingue, pour la phase 9, les variables du schéma d'état écrites ; un flux proposé en phase 9 est refusé.
  - Au passage à t + 1, l'ordonnanceur **vérifie à l'exécution** que chaque variable d'état de bloc et du moteur a reçu exactement une écriture dans le pas, de son propriétaire déclaré (ADR 0002 : aucun état caché).
  - Tests de J2, sur un **bloc d'essai** (aucun bloc n'existe au J2) :
    - (1) écriture unique : chaque variable d'état de bloc reçoit sa valeur suivante une fois par pas, du bloc déclarant, dans la phase déclarée ; une seconde écriture, ou une écriture par un autre bloc, est refusée ;
    - (2) le test de triangularité couvre la phase 9 : aucune lecture mutuelle dans le groupe ;
    - (3) une permutation de l'appel des blocs du groupe de la phase 9 laisse l'état du pas t + 1 identique bit à bit ;
    - (4) l'état d'ouverture du pas t est identique (empreinte) avant la phase 1 et après la phase 9 ;
    - (5) un flux proposé en phase 9 est refusé ;
    - (6) la reprise à la frontière de tour (test existant, ADR 0005, point 19) couvre une variable écrite en phase 9.
- **Pour `etat/` (J2) et la reprise.** La frontière de tour suit la phase 9 entière (ADR 0005, point 3) : les écritures de la phase 9 sont dans l'état sauvegardé, et la reprise exacte les couvre ; une sauvegarde prise en cours de pas, phase 9 comprise, n'est pas un point de reprise. Le schéma déclare chaque variable avec son propriétaire, sa phase d'écriture, son unité et sa valeur stationnaire (ADR 0002). Empreinte inchangée : bloc 6, trois variables (ti, y_{t−1}, T_{F,t−1}) ; bloc 5, une (YD_{t−1}) ; valeurs initiales fournies par l'état résolu (fiches § 9.7).
- **Pour le déterminisme et le budget (ADR 0002, invariants 10 et 11).** Ordre statique, aucune lecture mutuelle, aucune agrégation entre pays, aucun tirage. Coût d'une copie ou d'une somme de quelques termes par pas. Les barrières entre pays (J5) restent à décider ; comme l'ADR 0007, celui-ci n'exige d'une barrière que de ne pas couper une phase en deux : la phase 9 n'est pas coupée entre le groupe des blocs et le passage à t + 1.
- **Pour la spécification (`docwriter`, branche n° 3b, jalons 4 de #41 et #42 ; commit `docs:` propre au cadre si la session préfère isoler le contrat).**
  - `sec:cadre-phases`, l. 487, après « … décision M24, ADR 0007) » : « ; en phase 9, après les identités du noyau et avant l'avancée du registre et le passage au pas suivant, les blocs déclarés écrivent leurs variables d'état du pas suivant, sans proposer de flux et sans se lire entre eux, les montants exécutés du pas se lisant au grand livre (décision M29, ADR 0009) ».
  - `tab:phases`, ligne 9 : colonne « Contenu » : « identités par pas et cumulée ; double calcul des valeurs nettes ; Res_{t+1} ≥ 0 ; variables d'état du pas suivant des blocs déclarés (sans flux) ; mise à jour du registre ; passage à t + 1 » ; colonne « Écrivent » : « noyau, puis ménages, investissement, puis moteur » ; colonne « Lisent » : « tout, dont les montants exécutés du pas ».
  - `tab:phases`, ligne 7, colonne « Écrivent » : « État, banque, banque centrale » (ordre à fixer par les fiches 7 à 9) ; colonne « Lignes » inchangée (19a, 19b).
  - Provenance de `sec:cadre-phases` : ajouter « décision M29, citant M22 (ADR 0009) ».
  - Recommandation de forme de la fiche 6 (§ 9.8, point 2 (a)), hors décision : légende de `tab:phases`, « toute phase lit aussi l'état d'ouverture ».
  - `sec:menages` : H7 en phase 9 ; `sec:investissement` : tenue de T_{F,t} en phase 9, F4 en phase 6 sur l'ouverture.
  - `verifier_matrices.py --strict` : sortie identique (aucune table de flux ni de bilans ne change).
- **Pour les fiches.** Les § 9.10 des fiches 5 et 6 consignent déjà la décision (commit `efb6bcd`) et s'imposent à la lecture de leurs § 9.4 (fiche 6 : dernière ligne du tableau des phases, « phase 9 » ; fiche 5 : H7 en phase 9, ligne « 7 » sans écriture) : aucune retouche des tableaux n'est due avant le passage de `docwriter`. Fiche 7 (branche n° 4) : déclare la phase de i_L, i_D (point 5). Fiche 9 : aucune obligation d'état pour T_F.
- **Pour l'ADR 0005.** Annotation datée d'une phrase au point 15, renvoyant ici (la décision M22 est inchangée) : la phase 9 reçoit un groupe de blocs écrivant leurs variables d'état, sans flux. À faire par `architect` si le mainteneur retient cette forme ; l'ADR 0007 n'avait pas annoté l'ADR 0005, l'ADR 0008 l'a fait.
- **Pour `docs/agents/routage.md` § 4.2** (hors du périmètre d'écriture d'`architect` ; commit `docs:` de la session principale) : préciser « les phases numérotées de l'ordonnanceur, dont le groupe de la phase 9 (ADR 0009) » et « l'interface bloc → noyau (état d'ouverture lu, flux proposés rendus, montants exécutés lus en lecture seule : ADR 0009) ».
- **Fichiers.** `docs/feuille-de-route.md` § 4 (ligne M29 du tableau, aujourd'hui en prose l. 192) ; `CONTEXT.md` (entrées « Phase », « Ordre interne », « État d'ouverture / état de clôture », « Variable d'état retardée », nouvelle entrée « Montant exécuté ») ; `docs/blocs/README.md` (ligne de la fiche 1 : la phase 9 reçoit un groupe de blocs, ADR 0009 ; lignes des fiches 5 et 6 : M29) ; `CLAUDE.md` inchangé (« phases numérotées d'un pas, identiques à celles de la spécification » reste vrai).
- **Effet sur les résultats.** Aucun : le moteur v3 n'exécute rien, et les lectures (i), (ii), (iii) donnent la même valeur T_{F,t} et YD_t au pas t + 1 au socle, puisqu'aucune ligne des phases 7 et 8 (19a, 19b ; 12, 13, 16, 21) ne touche la colonne des ménages ou des entreprises hors des lignes à montant nul (`tab:matrice-flux`, l. 331 à 345).
- **Ce que l'ADR ne règle pas.** Le fond de F3, F4 et H7 (M27, M28) ; la règle de i_L, i_D (fiche 7) ; l'ordre de la phase 7 (fiches 7 à 9) ; les barrières entre pays (J5) ; la ligne nommée de part non payée (J6, #57) ; la cible d'inflation en vigueur et le facteur Γ^e, qui relèvent de l'ADR 0010 (proposé) et de l'issue #61.
- **Conditions de réouverture.** Une décision citant M29 et M22, dans quatre cas :
  - un bloc doit lire en phase 9 l'écriture d'un autre bloc (le groupe devient ordonné) ;
  - l'ordonnanceur de J2 montre qu'une déclaration unique par phase ne suffit pas ;
  - une variable d'état de bloc doit recevoir deux écritures dans le pas ;
  - une barrière entre pays (J5) doit s'intercaler entre le groupe des blocs et le passage à t + 1.

Issues : #42 (constat 1, § 9.8 ; cet ADR répond à l'issue proposée n° 1 du § 9.9, non créée, fiche 6 § 9.10) ; #41 (H7, § 9.8, contrat 1) ; #60 (`menages.py`, J3 : H7 en phase 9) ; #61 (ADR 0010) ; #17 (ADR 0005 complété) ; #57 (montants exécutés au J6) ; issue « noyau » de la branche n° 5 (tests de J2, à créer).
