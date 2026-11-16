---
status: accepted
date: 2026-11-14
---

# Document de lecture de l'ADR 0012 : état en vigueur au 14/11/2026 des interfaces du noyau, de l'ordonnanceur et du schéma d'état, consolidé sans décision nouvelle ; les annotations futures vont ici

> **Statut « accepté » le 14/11/2026, par décision du mainteneur** (P76, option (b), #119), sans Fable (seuil § 4.3 de `docs/agents/routage.md` atteint, consultation déclinée). Rédigé par `architect-approfondi` (Opus, effort `high`) au rang 1b de J3-c (`claude/j3-monnaie`, PR #129, tête `d246c28`).

## Contexte

L'ADR 0012 (rédigé sous P31 (a), accepté le 07/10/2026) fixe les trois contrats partagés de J2 : noyau, interface bloc → noyau, schéma d'état, sous les critères de J2 (M19). Huit annotations datées l'ont précisé jusqu'au 13/11/2026 ; il compte 157 184 octets et 449 lignes (`wc -c`, tête `d246c28`) et presque chaque agent le lit. #119 rattache à la taille des documents lus deux arrêts d'agents à 40 tours au J2 (P48). P76 (b) : un ADR de consolidation **sans décision nouvelle**, de 40 ko au plus ; l'ADR 0012 reste intact ; les annotations futures vont à l'ADR 0013.

## Décision

1. **Rôle.** Ce document rassemble, contrat par contrat, la règle **en vigueur** de l'ADR 0012 et de ses annotations, chacune avec son origine, sous les étiquettes de l'ADR 0012 (A1 à G5, points soumis 1 à 11) ; l'annotation du 13/11/2026 est rangée sous **H1 à H6** (ses §§ 1 à 6). Un renvoi existant « ADR 0012, A3.2 » (`CONTEXT.md`, code, spécification) se lit ici sous la même étiquette.
2. **Ce qui fait foi.** L'ADR 0012 annoté reste la source des règles consolidées ici, avec leurs motifs, mesures et options écartées. Ce document n'ajoute, ne retire ni ne modifie aucune règle ; un écart entre les deux est un défaut de ce document, corrigé par annotation datée ci-dessous.
3. **Annotations futures.** Toute précision de ces contrats est une **annotation datée de l'ADR 0013**, en fin de fichier ; pour le point qu'elle touche, elle l'emporte sur l'état consolidé (convention de l'ADR 0012 : « là où il diverge, l'annotation l'emporte », a95, a97). L'ADR 0012 ne reçoit plus d'annotation. Modifier un contrat au-delà d'une précision demande un nouvel ADR (point 6).
4. **Sigles d'origine.** **Acc** : texte accepté, décision du mainteneur du 07/10/2026, et ses points soumis (« pt n ») ; **a95**, **a96**, **a97** : annotations du 07/10/2026 (questions de `coder` sur #95, #96 avec ses compléments, #97 avec R1 à R3) ; **a98** : annotation du 14/10/2026 ; **c14** : second complément du 14/10/2026 ; **g15** : annotation du 15/10/2026, G1 tranchée (P40 (a)) ; **a100** : annotation du 15/10/2026 (#100) ; **a13** : annotation du 13/11/2026 (rang 1b de J3-b), avec ses mentions datées du rang 10. « a95.2 » : point 2 de a95. M1 à M8 : mesures de l'instruction du point 8 (Contexte de l'ADR 0012) ; M95-n : propositions de `monnaie` ; C95-n, C97-n : de `macro`.
5. **État en vigueur** : sections A à H. Toutes les règles sont des **choix de conception**, sauf les identités (dérivées, ADR 0005) ; l'ADR 0012 applique les ADR 0002 et 0005 et met en forme les ADR 0007 à 0011 sans les rouvrir ; un nom de code peut changer s'il est signalé, jamais une signature, unité, propriétaire, phase, lecture ni règle de refus (Acc ; a13).
6. **Conditions de réouverture** (Acc, Conséquences, avec l'ajout du pt 8) : nouvel ADR citant l'ADR 0012, M22 et M29 si un bloc ne peut pas exprimer un flux par les termes d'une ligne du catalogue (rouvrir la matrice, citant M22) ; si le contrôle statique de B3 ne garantit pas la triangularité ; si le coût du noyau seul dépasse 0,5 ms sur la plateforme de référence sous A7 (mesure d'abord) ; si une barrière (J5) doit lire ou écrire le grand livre d'un autre pays ; si une sauvegarde doit être relue par une version antérieure ; si une règle de bloc ne peut pas tenir Res_{t+1} ≥ 0 sous forme exacte (alors (ii) pour Res, citant M22) ; si une saturation à une ligne n'admet pas d'écriture en min/max (A8.1) ; si la poussière de la lecture nette devient perceptible dans la restitution (J4, avis de `jeu`).

### A. Noyau (#95)

**A1. Catalogue** (`nations.noyau.catalogue`, seule source des lignes ; Acc A1, pt 2). **28 lignes** (1 à 10, 11a à 11c, 12 à 18, 19a-ménages, 19a-banque, 19a-BC, 19b-ménages, 19b-banque, 20 à 22), **six colonnes** dans l'ordre de `tab:matrice-flux`, **onze positions** : D_H, D_F, L, B_H, B_Bk, B_CB, Res, L^CB, M^G, K, IN. Chaque ligne est décrite par ses **termes simples** ; chaque cellule a une nature : revenu, actif réel (K : lignes 3, 8 ; IN : ligne 4) ou variation d'instrument. Phase : 18 en 3 ; 5 en 4 ; 1 à 4 en 5 ; 6 à 10, 11a à 11c, 14, 15 en 6 ; 19a en 7 ; 12, 13 en 8a ; 16 en 8b ; 21 en 8c ; 19b au J6. Pas de proposant au socle pour 19b-ménages et 19b-banque (ADR 0011, lecture (i)). **17, 20, 22** : contreparties de règlement, non proposables (A4). Signatures (ΔM, ΔH), cellules 17, 20, 22 et sommes de colonnes **dérivées**, comparées par test à `tab:portes-monnaie` et `tab:matrice-flux` (`lire_table` d'`outils/verifier_matrices.py` ; M95-1).

**A2. Flux proposé** (Acc A2, pt 1 (b)). `FluxPropose` immuable : ligne ; montant de chaque terme (u.m. par pas) ; **proposant apposé par la vue** (M95-10 (a)). Le noyau développe les termes : somme nulle **par construction**. **Montant négatif admis** pour les lignes 4, 7, 9, 10, 11a à 11c, 12, 13, 16, 18, 19a, 19b, 21 seulement, la ligne 7 par ligne (liste fermée, a95.1). Montant de la ligne : somme **signée** des cellules à terme symbolique positif (M95-2). Ni date ni phase.

**A3. Grand livre** (`nations.noyau.grand_livre`, `GrandLivre`, un par pays).
1. **`ouvrir_pas(etat_ouverture, parametres_cadre)`**, seul constructeur (a95.5) : copie les onze positions (ADR 0009, pt 1), remet à zéro les montants exécutés, évalue **une échelle S par secteur à l'ouverture** (`eq:noyau-echelle-bilan`, |Res| et |E| compris ; P33 (a)), valable pour tous les contrôles du pas, phase 9 comprise. **Domaines à l'ouverture** (défaut avec diagnostic, jamais repli ni `max(·)`) : S **finie et > 0** (pt 11 ; a95.5) ; **Res ≥ 0 strict** ; D_H, D_F, M^G ≥ −ε × S_payeur (M95-13) ; **IN ≥ 0 strict**, règle `STOCKS_OUVERTURE` (P72 ; H1.8) ; `t` entier. `executer_pas` passe `parametres.cadre` (P69).
2. **`proposer(flux)`**. `RefusDeProposition` si : ligne hors catalogue ; contrepartie ; phase autre que celle de la ligne, ou phase 9 (ADR 0009, pt 2) ; terme manquant ou en trop ; seconde proposition ; ligne sans proposant au socle ; signe non admis. Une ligne à proposant reçoit **exactement une** proposition, nulle comprise ; une ligne oubliée est refusée à la clôture, jamais un zéro implicite. Unicité : **critère d'interface, non identité** (C95-10).
   **Montant couvert** (pt 3 amendé par le pt 8 (4) ; applique l'ADR 0011, P1 ; QM2 (a)). `declarer_montant_couvert(ligne, montant)`, réservée au **bloc payeur**, apposé par la vue ; couples admis : **{(16, `finances_publiques`)}**, en 8b (ligne 7 et 19a-banque exclues, ADR 0011, P4). **Obligatoire dès que Π < 0 strict**, sinon refus à la clôture de 8b (a95.2). c = min(|Π| ; max(0 ; M^{G,8a})), **0 ≤ c ≤ |Π|** vérifié par `controle_de_signe` sous règle stricte ; hors liste ou hors domaine (ligne 16 positive, autre bloc, c < 0, c > |Π|, sans proposition, seconde déclaration) : refus, **jamais écrêtage**. Le noyau **exécute −c**, sans rien calculer ; c = 0 admis. **u = |Π| − c** est enregistrée par le bloc 9 (E13) en variable du pas ; « **exécuté − proposé = u** » au bit (a95.2 ; M3). M^G après 8b = fl(M^{G,8a} − c) ≥ 0 **si M^{G,8a} ≥ 0**, sinon c = 0 et M^G reste une poussière admise à −ε × S_G (a98.1). **Ligne 6** : proposition nette par le bloc 9 (payeur), part non versée enregistrée en variable du pas ; liste des couples inchangée (pt 10).
3. **`clore_phase(phase) → ClotureDePhase`**. Exécution **dans l'ordre canonique du catalogue** (lignes, puis colonnes), quel que soit l'ordre d'appel (M95-3) ; permuter les blocs d'une cellule à virgule (phase 2, dernier groupe de la 5, phase 6, 8b avec le montant couvert, groupe de la 9) laisse la clôture **identique bit à bit** (C95-9, C97-4). Règlements (A4), positions (`eq:noyau-cloture-poste`), identités (A5) ; rend une valeur immuable (phase, résidus/S, montants exécutés), le noyau n'en garde rien. **Onze clôtures** : 1 à 7, 8a, 8b, 8c, 9 (pt 7 ; M95-5) ; en 8c, la banque lit le flottant même des réserves après 8b (M95-7) ; ouverture figée et position courante sont deux lectures (M95-6). Une clôture **sans ligne exécutée** saute ses contrôles (égalité testée), jamais la couche noyau de la phase 9 (a95.6). L'identifiant « 8c » est **exposé par le noyau**, lu par l'ordonnanceur sans copie (c14.2).
   **Lectures seules**, aucune méthode d'affectation : `montant_execute(ligne, colonne)`, `montant_execute_ligne(ligne)` après clôture de la phase de la ligne, sinon refus, jamais 0 ; `position`, `ouverture`, `echelle` ; `valeur_nette_stock`, `valeur_nette_flux` ; `clore_pas()` rend les onze positions de clôture ; le grand livre ne survit pas au pas.

**A4. Règlement dérivé** (Acc A4, pt 2). Moyens de paiement : D_H, D_F (comptes à la banque), Res, M^G (comptes à la banque centrale) ; la banque centrale paie au compte de la contrepartie chez elle. 17, 20, 22 **routées ligne par ligne**, jamais en reste de colonne (M95-1, M95-4) ; `eq:noyau-somme-colonne` reste un contrôle qui peut échouer. Caisse : **colonne payeuse**, quel que soit le proposant (ADR 0011). Le noyau ne convertit aucun taux et ne lit pas n_a.

**A5. Identités** (Acc A5 ; pts 8, 9 ; a95.4, a95.7). Tolérances **relatives** ε × S, ε_V × S, S à l'ouverture, ε et ε_V paramètres typés ; forme |r| ≤ ε × S. **À chaque clôture** : `eq:noyau-somme-ligne` (exacte sous A2) ; `eq:noyau-somme-colonne` (ε × S_s, sous-colonnes des entreprises réunies) ; `eq:noyau-cloture-poste` dans **chacun des deux bilans**, à son échelle ; **portes ligne par ligne**, contreparties comprises (a95.7 ; M95-2), à ε × S_ℓ, **S_ℓ = plus petit S_s des secteurs à montant non nul** (pt 9 (α) ; M95-12) ; **caisse nette** `eq:noyau-caisse-nette` (`verifier_caisse` ; a95.4) pour D_H, D_F, M^G seuls (banque et banque centrale exclues ; M95-8) : **x + ε × S_payeur ≥ 0**, S à l'ouverture (pt 8 (2)), position jamais ramenée à zéro. **Phase 9, couche noyau** (ADR 0009, pt 2) : `eq:noyau-valeur-nette-stock` et `eq:noyau-valeur-nette-flux`, V^flux_{t+1} = V^flux_t + Σ lignes 1 à 16 de la colonne (sous-colonne courante des entreprises), V^flux variable d'état du noyau, initialisée à V^stock_0 (ADR 0005, pt 8) ; `eq:noyau-tolerance-cumulee` (ε_V × S_{s,t}) ; `eq:noyau-reserves-cloture`, **Res_{t+1} ≥ 0 strict**, sans tolérance (pt 8 (1)) ; `eq:noyau-variation-monnaie` (ε × S^Bk) et `eq:noyau-variation-monnaie-centrale` (ε × S^CB), une fonction chacune (a95.4) ; `eq:noyau-tolerance-pas`, forme commune. Res n'est pas contrôlé entre les phases (découvert intra-pas). Σ V^stock = K + IN : **retirée du moteur, gardée en test** (a95.4). **Douze** labels `eq:noyau-*` (a95.4).
**Contrôle de signe** (pt 8 (3)) : **une seule fonction**, `controle_de_signe` (`nations.noyau.identites`), sans label propre (labels portés par ses appelants : caisse nette, réserves de clôture, domaine du montant couvert ; a95.4) ; aucune autre comparaison de signe dans `src/nations/noyau/` (test textuel). Domaine **déclaré par identité** selon sa structure (nombre de lignes qui touchent la position dans la phase) : *strict* (Res_{t+1}) ou *relatif au payeur* (D_H, D_F, M^G) ; pas un drapeau de mode, son changement est une décision. Mêmes domaines pour l'**état chargé** avant la phase 1 (M95-13). Statut : précision de M22, lecture (B), annotation du 07/10/2026 de l'ADR 0005, pt 10.

**A6. Diagnostics** (pt 6). Exceptions dérivées d'`ArretNoyau` (`nations.noyau.diagnostics`) : `RefusDeProposition` à l'appel, `DefautComptable` à la clôture ; champs structurés (pas, étape, identité ou règle, secteur ou payeur, ligne, terme, résidu, S, résidu/S, tolérance), message en français. Jamais rattrapées par le moteur ; état d'ouverture intact ; aucune tolérance élargie (ADR 0005, pt 14).

**A7. Représentation** (Acc A7 ; P37 (a)). `float` Python dans des structures à champs fixes ; **aucun NumPy** dans le grand livre d'un pays ni dans l'état, **aucun `Decimal`** ; NumPy admis dans `observation/` et, sur mesure, pour l'agrégation du J5.

**A8. Saturations exactes et contrat de poussière** (pt 8 (5)).
1. **Saturation à une ligne : forme exacte**, en **min/max sur la position lue** au grand livre. Cas : **B7, ΔL^CB = −min(Res^{8b} ; L^CB)**, d'où **Res_{t+1} · L^CB_{t+1} = 0 exactement**, critère de #90 sans tolérance (M1) ; E13 par le montant couvert (M3) ; E1 et H5, exactes par construction (M7, M8) ; N8, ΔIN = cm · IN^vol_{t+1} − IN_t, qui n'est pas un solde résiduel au sens de l'ADR 0005, pt 8 (P72). Une poussière laissée par une telle saturation est un **défaut du bloc**.
2. **Contrat de poussière** : D_H, D_F, M^G peuvent valoir jusqu'à −ε × S de leur détenteur sans défaut (cas réel : E6 saturée, τ_F = 0, M6) ; toute règle qui les **lit** écrit **max(0 ; ·)**, borne déclarée, testée à −1 ulp et à −0,5 ε × S. Les réserves n'en relèvent pas (Res ≥ 0 strict à l'ouverture, découvert intra-pas lu tel quel par B7).

### B. Ordonnanceur (#97)

**B1. `PHASES`** (`nations.moteur.phases`, unique transcription de `tab:phases` ; Acc B1). Pour chaque phase : écrivains en **séquence de groupes** (virgule : sans lecture mutuelle ; « puis » : ordre), lignes, phases lues. 0 : `moteur` ; 1 : `(moteur) puis (travail, banque_centrale)` ; 2 : `(production, menages, investissement, finances_publiques)` ; 3 : `(investissement)`, ligne 18 ; 4 : `(travail) puis (production)`, ligne 5 ; 5 : `(prix) puis (production) puis (menages, investissement, finances_publiques)`, lignes 1 à 4 ; 6 : `(finances_publiques, banque, investissement)`, lignes 6 à 10, 11a à 11c, 14, 15 ; 7 : `(finances_publiques)`, sans ordre interne (ADR 0011), lignes 19a ; 8 : (a) `(banque_centrale)`, lignes 12, 13 ; (b) `(banque_centrale, finances_publiques)` sans ordre (ADR 0011, P1), ligne 16 ; (c) `(banque)`, ligne 21 ; 9 : `noyau`, puis `(menages, investissement)`, puis `moteur` (ADR 0009). La colonne **« Lisent » est normative** (a97.10) ; les phases 6 et 7 lisent la phase 2 (a97.10, R1). Un test compare `PHASES` à `tab:phases` lue par `lire_table`, colonne « Lisent » comprise. Ordre des radicaux et groupe de la phase 9 indépendants des données et des joueurs (ADR 0007, pt 4 ; ADR 0009, pt 3).

**B2. Contrat de bloc** (`nations.moteur.contrat_bloc`, module feuille ; Acc B2). `DeclarationDeBloc` immuable, suite de **sièges** (bloc × étape) : variables du pas écrites ; lectures (source, nom), source `ouverture`, étape, `grand_livre` ou `registre` ; lignes proposées ; lignes couvertes ; variables d'état (C1, H1). Une méthode par étape, appelée avec une `Vue` qui ne donne que : ouverture figée, paramètres, grandeurs d'ouverture, variables du pas déclarées, grand livre en lecture seule avec `proposer` et `declarer_montant_couvert`, registre, `ecrire_pas` et `ecrire_etat` pour ses variables. `Vue.ecrire_etat` contrôle le domaine dès l'écriture (`RefusDuMoteur`, rien d'enregistré ; a13, mention du rang 10). **Aucun attribut d'instance** : `assembler` refuse un `__dict__` ou des `__slots__` non vides (a97.8) ; test textuel : H5.3.

**B3. Assemblage** (une fois, avant le premier pas ; Acc B3). **`assembler(phases, blocs, parametres, entrees)`** (a97.1), `entrees` une `DeclarationDesEntrees` (entrées de scénario publiées en phase 0, leviers au premier groupe de la phase 1) ; `parametres` exactement un `EnsembleDesParametres` (H3.5). `DefautDeDeclaration` si : écrivain sans implémentation, ou bloc sans siège ; écriture hors phase déclarée, ou ligne proposée hors de sa phase ; ligne à proposant sans exactement un proposant, ou ligne sans proposant qui en a un ; **triangularité** violée (lecture (p', nom) depuis p : p' < p, ou p' = p depuis un groupe antérieur ; montant exécuté : phase de la ligne close avant ; en phase 9, aucune lecture d'un écrivain de la phase 9 ; `ouverture` et `registre` toujours admis) ; **phase source hors de la colonne « Lisent »** (a97.10), montants exécutés compris, leur phase étant celle de la ligne, contreparties en 8c (R2), positions, échelles, ouverture et registre relevant de la seule triangularité (R2), lecture interne à la phase lectrice admise (R3) ; variable d'état à deux propriétaires, propriétaire absent de sa phase d'écriture, ou **bijection** schéma ↔ siège rompue (a97.9 ; g15.1) ; `"P"` non écrite par `prix` en phase 5 (`ECRIVAIN_DE_L_INDICE` ; a97.3) ; attribut d'instance (a97.8).

**B4. Espace des variables du pas** (`VariablesDuPas` ; Acc B4). Noms déclarés, créé à `ouvrir_pas`, détruit à `clore_pas`, distinct de l'état. Refus : nom non déclaré, seconde écriture, lecture d'un nom non écrit (jamais de défaut), valeur non finie (a13, mesures). À l'exécution, seule la présence du nom est vérifiée.

**B5. Pas** (Acc B5). `executer_pas(etat_ouverture, entrees_du_tour, ordonnanceur, observateur) → etat_cloture`, sans état propre. Phase 0 : `ouvrir_pas`, calendrier, grandeurs d'ouverture, entrées de scénario (`EntreesDuTour`, vérifiées contre la déclaration à chaque pas ; a97.1). Phases 1 à 8 : groupes dans l'ordre « puis », blocs dans l'ordre canonique des radicaux, `clore_phase` par étape, `observateur.relever(cloture)`. Phase 9 : `clore_phase("9")`, blocs du groupe, puis couche moteur : avancée du registre avec la variable du pas **`"P"`** (`INDICE_DES_PRIX` ; a97.3), état t + 1 construit par `schema.EtatPays(**champs)`, qui vérifie les domaines (H1.6), contrôle d'**une seule écriture** par variable d'état, `relever(fin_de_pas)`. Les leviers (J4) changent le contenu des déclarations, pas `executer_pas` (a97.1).
**Montants exécutés lus à l'exécution** (a100.1, a100.2, a100.3) : chaque siège a sa `LectureDuGrandLivre` aux droits arrêtés à l'assemblage ; une ligne non déclarée lève `RefusDuMoteur` (pas, étape, bloc, ligne), une ligne hors catalogue garde le refus du noyau. Positions, ouverture, échelles, valeurs nettes ne sont pas filtrées à l'exécution (a100.4) : contrôle statique (H5).

### C. Variables d'état et grandeurs d'ouverture (#96, #97, #61)

**C1. `VariableEtat`** (Acc C1). Nom ; propriétaire (`noyau`, `moteur` ou radical) ; phase d'écriture ; unité (D1) ; type (`float`, `int`, tuple de `float` de longueur déclarée) ; valeur stationnaire ; **invariance** : `nominal` (× 100), `sans_dimension`, `volume` (inchangée, personnes et productivité comprises ; a13 § 1.3), `indice` (× 100, critère relatif du glissement ; a96.2). Sans propriétaire ou sans déclaration : refus.

**C2. Écriture** (Acc C2). Le propriétaire écrit la valeur du pas suivant par `ecrire_etat`, dans sa phase, **une fois par pas** ; elle est lisible dans le pas sous **`<nom>_suivant`**, seul autre nom admis (H1.1, H2.1) ; les autres lisent l'ouverture. Changer de propriétaire change une déclaration, pas l'interface.

**C3. Grandeurs d'ouverture** (`nations.moteur.ouverture.GRANDEURS_OUVERTURE` ; Acc C3 ; forme attendue par #61, P34 (a)). Nom, fonction, label éventuel, unité ; calculées une fois par pas en phase 0, dans l'ordre (triangulaire), lisibles dès la phase 1 (source `0`), **jamais variables d'état ni sauvegardées**. En vigueur : `annee`, `mois`, `date_de_decision`, `g`, `facteur_g` (H4) ; Γ^e_t, avec γ^e_t et π^{∗,pas}_t (`eq:moteur-croissance-nominale-attendue`), s'y ajoute par #61 **après g**, en lisant π\*_t, variable d'état du bloc 8 (ADR 0010, pt 4 et annotation du 04/10/2026). Année, mois et prédicat : « sans dimension », `UNITES` non étendu (a97.6) ; `label` d'`annee` et `mois` : renvoi, non balise (a97.7).

### D. Schéma d'état, version, sauvegarde, reprise (#96)

**D1. `EtatPays`** (`nations.etat.schema` ; Acc D1). Dataclasse **gelée**, champs obligatoires sans défaut : **`CHAMPS_D_IDENTITE`** (`identifiant`, `graine`, écrits par aucune phase) puis **`VARIABLES`** (a96.1) : `t`, `registre_prix` (13 `float`, P_{t−1} à P_{t−13}), onze positions, cinq V^flux, variables des blocs (H1). Champs = déclarations (test) ; empreinte calendaire = 14 ; ni historique, ni série, ni compteur hors de t. Monde : séquence triée par identifiant **par point de code Unicode** (a96.1). Variables d'un bloc déclarées **dans `etat/`, un module par radical**, référencées par sa `DeclarationDeBloc` (G1 (a) : g15.1, P40 (a)) ; `nations.etat.schema` assemble seul `VARIABLES`.
**Domaines** : `schema.defaut_de_domaine`, seule fonction de domaine, appelée à toute construction (état initial, état de clôture de chaque pas) et à la reprise ; refus avec diagnostic, jamais écrêtage (H1.6) : graine entière dans **[0 ; 2^64[** ; `t` entier dans **[0 ; 2^63[** (`T_EXCLU`) ; identifiant non vide, encodable en UTF-8, sans caractère de contrôle ni de catégorie `Cf`, `Zl`, `Zp`, sans espace de bord, en **NFC** (a96.1 et compléments) ; diagnostic de type faux sans entier géant recopié (a96.1, C-2) ; registre **fini et > 0** (c14.1) ; toute variable `float` **finie** (a13 § 1.7, mention du rang 10) ; variables de bloc : H1.6, H1.7.
**Unités** : vocabulaire fermé, **`nations.etat.unites`**, sans importation de `nations` (a96.2) : celui de F2, plus `pas`, `u.v.`, `u.v. par pas`, `u.m. par u.v.` (a96.2), `u.m. par personne et par pas`, `u.v. par personne et par pas` (P65 ; a13 § 1.3).

**D2. Version** (Acc D2). `VERSION_SCHEMA`, incrémentée à tout changement de champ, type, unité ou sémantique, journal dans la docstring. **En vigueur : 2** (a13 § 1.5 ; P53). Une retouche dans une branche ne l'incrémente pas tant qu'aucune sauvegarde de cette version n'est publiée (a96, complément D2 ; a13 § 1.5).

**D3. Sauvegarde** (pt 5). JSON texte UTF-8, `{"version": n, "pays": [...]}` dans l'ordre canonique ; flottants par **`repr`** ; `allow_nan=False` ; clés : champs d'identité puis variables (a96.1). Ni paramètre, ni levier, ni série : reprise exacte **à paramètres et entrées identiques**.

**D4. Reprise** (Acc D4). `charger` refuse (`SauvegardeRefusee`) : autre version (aucune migration, G3) ; champ manquant ou inconnu ; type faux ; pays en double ou hors ordre ; valeur hors domaine. Tests : aller-retour aux mêmes octets ; égalité bit à bit (`struct.pack("<d")`) ; sauvegarde à la frontière de tour qui reproduit la trajectoire ; des **leviers** différents après reprise ne font diverger qu'à partir de la phase 1 (a97.1).

### E. Observation (#96)

**E1. Protocole** (Acc E1). `Observateur.relever(evenement)`, appelé par le moteur seul, avec `ClotureDePhase` et `FinDePas` immuables ; ne rend rien. `FinDePas` : état de clôture, `variables_du_pas`, `grandeurs_ouverture` en n-uplets (nom, valeur) de types de base, dans l'ordre d'inscription, indépendant de l'ordre des blocs passés ; montants exécutés dans les `ClotureDePhase` seulement (a96.4, a97.2). Aucun module de `noyau/`, `moteur/`, `etat/`, `blocs/` n'importe `observation/` hors du protocole ; `ObservateurNul` ; **test de suppression** : sauvegardes identiques à l'octet.

**E2. Résidus** (Acc E2). `ReleveDesResidus` (a96.3) : résidus/S par clôture et |V^stock − V^flux|/S en phase 9 ; grandeur A du jalon (maximum sur secteurs et pas, S à l'ouverture, fenêtre 720 pas) : `accumulation_maximale` (`nations.observation.residus` ; a98.2). Les séries vivent dans `observation/` seulement.

**E3. Coût du noyau seul** (Acc E3). Temps de `ouvrir_pas`, **25 propositions et une déclaration de montant couvert** (a95.8), onze `clore_phase` et `clore_pas` ; propositions pré-générées, `ObservateurNul`, un pays, moyenne sur 720 pas ; relevé par `ReleveDuCout` (`nations.observation.cout` ; a98.2). Seuil **0,5 ms** (ADR 0005, pt 19), affirmé **sur la plateforme de référence seule** (ADR 0003, M16 ; `GITHUB_ACTIONS=true`), saut explicite ailleurs (a98.3).

### F. Paramètres et conversions (#97)

**F1. `Parametre`** (Acc F1, pt 4). Nom, symbole, valeur, unité, source, étiquette, **domaine** (refus, jamais écrêtage ; ADR 0011, pt 2). Cadre : n_a = 12, n_m = 1, ε, ε_V dans `nations.moteur.parametres.cadre` (ADR 0005, pt 18). Tables des blocs : **`nations.moteur.parametres.<radical>`**, valeurs par archétype dans `scenarios/` (H3). Chaque paramètre est dans au moins un test.

**F2. Conversions** (Acc F2). `TauxDeFlux`, `TauxDeCroissance` ; `par_pas` (`eq:moteur-conversion-taux`, x/n_a) et `facteur_par_pas` (`eq:moteur-conversion-croissance`, (1 + x)^{1/n_a}) dans `nations.moteur.conversions`, chacune réservée à son type ; aucune fonction à argument de nature (ADR 0008, I.3). **Annualisation inverse** (1 + v)^{n_a} − 1 (ADR 0008, I.4) : même module, écrite avec son **premier consommateur**, label et test (a97.5). **Test « conversion unique »** sur l'arbre syntaxique (a97.4) : écart = division réelle dont le diviseur est n_a, ou puissance dont l'exposant contient 1/n_a (puis n_a), hors des deux fonctions ; un élément indexé par n_a n'en est pas une ; exemption fermée : `calendrier.date`, `calendrier.est_date_de_decision`. Une durée en années passe par `par_pas(TauxDeFlux(1/κ))` (N11), sans exemption ; construire ces types au site d'appel pour un taux dérivé ou pour π^e est admis (a13 § 3.6, mention du rang 10).

**F3. Registre et calendrier** (Acc F3). Seules fonctions qui indexent le registre (`nations.moteur.registre`) : `dernier_prix`, `glissement`, `variation_sur_le_tour`, `avancer` (`eq:moteur-registre-prix`). `nations.moteur.calendrier` : date affichée (`eq:moteur-calendrier-date`, une balise, dans `calendrier.date` ; t = n − 1, définition du tour, sans balise ; a97.7) et prédicat de date de décision.

### G. Ouvert et à venir

- **G1** : question a96.5 et a97.9, tranchée en (a) le 15/10/2026 (D1 ; g15.1, g15.2) ; échéance « avant le premier module de bloc », sans objet depuis J3-b (g15.3 ; P41 (a)) ; version 2 avec les premières variables de bloc (g15.4 ; D2). **G2** : barrières entre pays (J5), une barrière ne coupant pas une phase (ADR 0007, 0009). **G3** : migrations et paquet de partie, paramètres par référence (J4). **G4** : leviers, déclarés dans `DeclarationDesEntrees` (J4).
- **G5. Générateur de #98** : contrat de bloc sous les huit radicaux ; 23 lignes proposables ; 17, 20, 22 par dérivation ; 19b par un **double du catalogue dans les tests**, jamais en modifiant `catalogue.py` (a95.3) ; B7 en −min et ligne 16 par montant couvert (pt 8) ; critère × 100 **rapporté à S** : |x^{×100} − 100 x| ≤ 1e−10 × 100 S_s, registre et glissement gardant leur critère relatif (ADR 0008 ; M5).
- **Laissés ouverts par l'ADR 0012** : classement des lignes de résultat par secteur (M95-11), à confirmer par `macro` ; agrégat P_t à J ≥ 2 (ADR 0008), qui rouvre l'écrivain unique de `"P"` (a97.3) ; radical de `eq:moteur-ratio-pib-annuel` (E2) ; lectures de paramètres hors contrôle statique (H5.4) ; lecture d'une échelle ou d'une valeur nette par un bloc (H5.3). Issues ouvertes : #120, #121, #122.

### H. Blocs du J3 (a13 ; P53, P54, P58, P59, P63, P65 à P73, dont P67, critère de stationnarité partielle de J3-b)

**H1. Variables d'état du schéma v2** (a13 § 1 ; P53, P54, P65).
1. **Nommage** : transcription ASCII du symbole ; exposant ou indice joint par `_` ; `*` → `_etoile`, `~` → `_tilde` ; grec par son nom ASCII ; indice de secteur (J = 1, M24) et date omis. **Un espace de noms par pays** (variables d'état, du pas, grandeurs d'ouverture).
2. **Table** (toutes `float` ; valeurs stationnaires : a13 § 1.2).

| Nom | Ouverture du pas t | Unité | Invariance | Propriétaire | Phase |
|---|---|---|---|---|---|
| `v_e` | v^e_t | u.v. par pas | `volume` | `production` | 5 |
| `IN_vol` | IN^vol_t | u.v. | `volume` | `production` | 5 |
| `pr` | pr_t | u.v. par personne et par pas | `volume` | `production` | 5 |
| `K_vol` | K^vol_t | u.v. | `volume` | `production` | 5 |
| `W` | W_{t−1} | u.m. par personne et par pas | `nominal` | `travail` | 1 |
| `U` | U_{t−1} | fraction | `sans_dimension` | `travail` | 4 |
| `N` | N_{t−1} | personnes | `volume` | `travail` | 4 |
| `N_pa` | N^pa_t | personnes | `volume` | `travail` | 4 |
| `mu_tilde` | μ̃_{t−1} | sans dimension | `sans_dimension` | `prix` | 5 |
| `pi_e` | π^e_t | par an, taux de croissance | `sans_dimension` | `banque_centrale` | 1 |

3. Seule `W` est nominale (critère relatif à 1e−10, ADR 0005, pt 19).
4. **μ̃** (P54) : écrite par `prix` en phase 5, μ̃_t = ln(p_t/UC_t) ; lue à l'ouverture par `prix` (P2) et `travail` (ω_{t−1} = exp(−μ̃_{t−1}), T2), sans recalcul ni lecture du registre ; |μ̃_t − ln(p_t/UC_t)| ≤ 1e−12 : test de #51.
5. **Ordre** : variables des blocs après celles du noyau, par radical dans l'ordre des blocs, puis dans l'ordre de la table ; `VariableEtat` et `Invariance` peuvent passer dans un module feuille d'`etat/` sans changer de forme ; sauvegarde v1 refusée.
6. **π^e** : refusée si **non (1 + π^e > 0)** ; au fil des pas, π^e > −1 est un invariant de BC3 (0 < λ_e ≤ n_a, P > 0), éprouvé par les tests du bloc 8.
7. **Domaines** (visa de `macro`), forme non (condition) : **W, pr, N^pa > 0** ; **IN^vol, N ≥ 0** ; **v^e > 0** ; **K^vol > 0** ; **0 ≤ U ≤ 1**. Les règles qui les écrivent les tiennent **exactement en double précision** : IN^vol_{t+1} = (IN^vol + y) − v, v = min(d ; IN^vol + y) ; U = 1 − N/N^pa, N ≤ N^pa (critères d'audit de #50, #51). Recommandation de `macro` : test de cohérence de U avec N et N^pa (T5) sur l'état résolu et une sauvegarde rechargée.
8. **Position `IN`** : N8 en ΔIN = cm · IN^vol_{t+1} − IN_t, domaine **IN ≥ 0 strict** dans `ouvrir_pas`, sans ε ni S^F (P72, option (c)) ; critère « Valorisation » de la fiche 2 rapporté à IN_t + UC_t · y_t (P73) ; IN^vol = 0 ⇒ IN = 0 à l'état chargé : #122. Position K : même domaine strict, sans réécriture, « J3-c » se lisant J3-d avec #67 (P80 ; mention datée à porter par l'annotation de J3-c).

**H2. Variables du pas entre blocs** (a13 § 2 ; unités : a13 § 2.2).
1. **Une valeur, un nom** : W_t, N_t, U_t, N^pa_{t+1}, μ̃_t et les quatre variables du bloc 2 s'écrivent une fois par `ecrire_etat` et se lisent sous `<nom>_suivant`.
2. **Table** (étape et groupe de `PHASES`) :

| Nom | Écrivain, étape (groupe) | Lecteurs (bloc, étape) |
|---|---|---|
| `g`, `facteur_g` | moteur, 0 | production (2 : N3 ; 5 : N1) |
| `W_suivant` | `travail`, 1 (2ᵉ) | production (2 : UC) ; travail (4 : WB) |
| `C_plan`, `I_plan`, `G_plan` | `menages`, `investissement`, `finances_publiques`, 2 | production (5 : demande) |
| `y_etoile` | `production`, 2 | production (4 : N5) |
| `IN_vol_etoile` | `production`, 2 | prix (5 : ξ, sans recalcul) |
| `N_etoile` | `production`, 2 | travail (4 : T4) |
| `UC` | `production`, 2 | prix (5 : P2, P3) ; production (5 : ligne 4) |
| `N_suivant` | `travail`, 4 (1ᵉʳ) | production (4, 2ᵉ : N5) |
| `y` | `production`, 4 (2ᵉ) | production (5 : N6, N7) |
| `p` | `prix`, 5 (1ᵉʳ) | production (5, 2ᵉ) ; acheteurs (5, 3ᵉ) |
| `P` | `prix`, 5 (1ᵉʳ) | moteur (9 : registre ; a97.3) |
| `C_vol`, `I_vol`, `G_vol` | `production`, 5 (2ᵉ) | acheteurs (5, 3ᵉ : lignes 1, 3, 2) |
| `v_e_suivant`, `IN_vol_suivant`, `pr_suivant`, `K_vol_suivant` | `production`, 5 (2ᵉ) | lecteur déclaré (ADR 0009, pt 1) |
| `U_suivant`, `N_pa_suivant` ; `y_cap`, `tu` ; `xi`, `mu_tilde_suivant` ; `v` | `travail`, 4 ; `production`, 4 ; `prix`, 5 ; `production`, 5 | observation (P66, P54) |

3. **p et P** : `p`, prix du bien, lu par le bloc 2 et les acheteurs ; `P`, indice, lu par le moteur seul ; sous J = 1, P_t = p_t (`eq:prix-indice`).
4. **La phase 5 ne lit pas W_t** : UC_t (phase 2) le porte ; un besoin contraire modifierait `PHASES` et `tab:phases` (condition d'arrêt) ; confirmé par `macro` (fiche 2, § 9.4).
5. **Lectures d'ouverture fermées par siège** : `travail` 1 : `W`, `U`, `mu_tilde`, `pi_e` (jamais π\*_t ni Γ^e à la place de π^e, ni le registre) ; `travail` 4 : `N`, `N_pa` ; `production` 2 : `v_e`, `IN_vol`, `pr` ; 4 : `pr`, `K_vol` ; 5 : `v_e`, `IN_vol`, `pr`, `K_vol` et la position `IN` (N8) ; `prix` 5 : `IN_vol`, `mu_tilde`, sans registre.

**H3. Tables de paramètres** (a13 § 3 ; P63, P65, P68 à P71).
1. **Forme** : un module par bloc sur le modèle de `cadre`, une déclaration `Parametre` par paramètre et une table immuable aux mêmes noms ; un taux annuel porte **son type** (`taux_du_parametre`), les autres champs sont des `float`.
2. **Domaine vérifié dans `__post_init__`**, toute construction comprise (`dataclasses.replace`, variations de test, archétypes) ; hors domaine : `DefautDeDeclaration`. **0 < λ_v < n_a strict** (P70) ; 0 < λ ≤ n_a pour λ_IN, λ_w, λ_N, λ_μ (P65) ; 1 + x > 0 pour g_pr, g_N ; β > 0 ; ψ_ξ ≥ 0 ; 0 < δ < n_a. *Domaines de définition* (visa de `macro`) : σ > 0 ; κ > 0 et 1/κ fini (a13 § 3.6, mention du rang 10) ; 1 + μ̄ > 0. *Conditions d'existence de l'état stationnaire*, refusées et nommées comme telles (P71) : **0 < U^eq < 1**, **μ̄ > 0**, refusées aussi par `outils/etat_stationnaire.py`.
3. **Une maison par paramètre** : g_pr (production), μ̄ (prix), lus par `travail` sans copie ; valeurs indicatives = défauts du script, **g_N = 0** (P63), égalité testée.
4. **δ** dans `nations.moteur.parametres.investissement` (P68 (b) ; maison de la décision M28), table à compléter avec le bloc 6 (« J3-c » se lit J3-d, P80) ; le bloc 2 la lit par la vue (N10) ; le cadre garde quatre paramètres (ADR 0005, pt 18).
5. **Accès par la vue seulement** (`vue.parametres.<radical>.<nom>`), jamais par importation ; `parametres` est un **`EnsembleDesParametres`** immuable (`cadre`, `production`, `travail`, `prix`, `investissement`), module à part, instance de référence (P69) ; `assembler` refuse tout autre type (mention du rang 10 ; n_a ≠ 12 : #120).

**H4. Croissance tendancielle** (a13 § 4 ; P63). En tête des grandeurs économiques d'ouverture, avant Γ^e : `g` = (1 + g_pr)(1 + g_N) − 1 (label `None`) et `facteur_g` = `facteur_par_pas(TauxDeCroissance(g))` (renvoi `eq:moteur-conversion-croissance`, non balise) ; lues par `Lecture("0", …)`, jamais sauvegardées ni recalculées par un bloc.

**H5. Contrôle statique des lectures** (a13 § 5 ; P58, P59 ; ferme a100.4). Test de `tests/invariants` sur l'arbre syntaxique de chaque module de `src/nations/blocs/` (hors `__init__.py`), **un bloc par module**, nommé par son radical.
1. **Relève**, dans chaque `phase_<étape>` : `vue.ouverture.<champ>` ; `vue.grand_livre.position`, `montant_execute`, `montant_execute_ligne` ; `vue.dernier_prix`, `glissement`, `variation_sur_le_tour` ; `vue.lire`, `ecrire_pas`, `ecrire_etat`, `proposer`, `declarer_montant_couvert`.
2. **Vérifie** : relevé = déclaré, siège par siège et source par source (une lecture déclarée jamais faite est un écart) ; méthode sans siège ou siège sans méthode : écart.
3. **Refuse** : `getattr`, `setattr`, `delattr`, `vars`, `globals`, `locals`, `eval`, `exec`, `__import__`, `__dict__` ; un nom non littéral ; la vue, `vue.ouverture` ou `vue.grand_livre` hors d'un accès relevé ; `vue.grand_livre.ouverture`, `.echelle`, `.valeur_nette_stock`, `.valeur_nette_flux` ; l'importation d'un module de `nations.moteur` autre que `contrat_bloc` et `conversions`, de `tests` ou d'`outils` ; depuis `conversions`, d'autres noms que `par_pas`, `facteur_par_pas`, `TauxDeFlux`, `TauxDeCroissance` (module entier, étoile, formes relatives refusés ; mention du rang 10) ; `global`, `nonlocal`, affectation à un attribut (a97.8). Contournements restants : #121.
4. **Hors contrôle** : `vue.parametres` ; les montants exécutés restent aussi filtrés à l'exécution (a100).
5. **Le test sait échouer** : un module fictif par forme refusée, une déclaration en trop ou en moins.

**H6. Garde-fou** (a13 § 6 ; P52 ; ADR 0002). Blocs d'essai dans `tests/` seulement, sous les radicaux réels, assemblés comme les blocs réels ; aucun module de `src/` n'importe `tests` ni `outils` ; aucun nom ni paramètre de mode dans `src/` ; H5 ne porte que sur `src/nations/blocs/`. Une mesure faite avec un bloc d'essai porte son étiquette (« π^e exogène (bloc d'essai) » en J3-b) et ne vaut pas verdict de boucle conjointe.

## Options écartées

- **P76 (a)**, section « État en vigueur » dans l'ADR 0012 : le fichier lu grossit. **P76 (c)**, document hors ADR : deux maisons à synchroniser.
- Les options écartées par l'ADR 0012 **restent écartées**, motifs et mesures y étant : section « Options écartées » (dont, au pt 8, (i-0), (i-e), (ii) pour Res, (iii-a), (iv), exécution de Π + u (M2, M4), noyau qui exécute −min, position ramenée à zéro) ; a95.3 ; a97.1 ; a97.7 ; g15.2 ; a13 §§ 1.8, 2.4, 3.4 et 4.

## Conséquences

- **Fichiers** : le présent ADR ; une mention en tête de l'ADR 0012 ; `docs/feuille-de-route.md` (§ 1, rang 1b) ; `CONTEXT.md` (entrée « ADR de consolidation »). Ni code, ni test, ni spécification ; labels et balises inchangés. **Effet sur les résultats : aucun.**
- **Relevé de #119** : chaque P-n, M-n, D-n et point d'annotation cité par l'ADR 0012 se retrouve ici (commande et sortie dans la PR #129), hors l'historique pur ci-dessous.
- **Non repris, lus dans l'ADR 0012** : historique de rédaction et d'acceptation (statut « proposé », consultations Fable, compléments du rang 1b de J2) ; positions des experts au point 8 et son instruction ; mesures chiffrées du Contexte et de a13 (un chiffre se remesure) ; numéros de ligne de la spécification à `f021b13` et SHA de réalisation ; tâches par rang de J2 et de J3-b (tests, surfaces documentaires, `CONTEXT.md`, feuille de route), réalisées ; échecs attendus (6, 2) et (7, 2), levés ; réserve M-1 de l'`audit`, corrigée ; mention facultative « interne » de R3 ; mesure publiée de E3 (a98.3) ; effet et surface documentaire de #100 (a100.5).
- **Hors de ce document** : l'annotation de forme de J3-c, ci-dessous, qui attend les avis du rang 1a.

Issues : #119 ; contrats consolidés : #95, #96, #97, #98, #100, #112, #113, #50, #51, #104, #61 ; ouvertes : #120, #121, #122.

## Annotations

### Annotation du 14/11/2026 (rang 1b de J3-c) : nomenclature du schéma v3, tables des blocs 7 et 8, forme de i_res ≡ i_CB, formes d'écriture, mentions datées de P80

Rédigée par `architect-approfondi` (Opus, effort `high`, sans Fable) au rang 1b de J3-c (`claude/j3-monnaie`, PR #129, tête `3aca87b`), en application des décisions du mainteneur du 14/11/2026 (P87 à P99, `docs/feuille-de-route.md` § 4) et des avis du rang 1a (`monnaie-approfondi`, pilote ; `macro-approfondi` ; synthèse en commentaire de la PR #129 du 14/11/2026). **La décision de l'ADR 0012 est inchangée** ; l'annotation précise C1, C3, D1, D2, F1, A8, H1 à H4 et la vue, **avant le code de #61, #91 et #90**. Les noms de code sont des contrats au sens de la Décision, point 5. L'annotation ne change aucun résultat ; P88 en change hors de la référence (point 7).

1. **Règles de lecture confirmées** (P97). La préséance de la Décision, points 2 et 3, est confirmée : l'ADR 0012 annoté fait foi pour l'état consolidé, et l'ADR 0013 se corrige par annotation. Les renvois à P80 de H1.8 et H3.4 sont confirmés (point 11). Le **plafond de 40 ko vaut pour l'état consolidé** (Contexte à Conséquences) ; les annotations s'y ajoutent, et une **reconsolidation par un nouvel ADR** intervient quand elles deviennent lourdes. *Renvoi daté (correction de G, Décision 2)* : le radical du ratio au PIB annuel n'est plus ouvert ; il est fixé à `observation` (P44 (b) ; ADR 0008, annotation du 15/10/2026 ; label `eq:observation-ratio-pib-annuel`, #115), décision que l'ADR 0012 n'enregistrait pas.
2. **Nommage (H1.1 complété).** Chapeau `^` → `_hat`, barre → `_bar` (usage déjà en vigueur : `mu_bar`). Les champs des tables de paramètres ont leur propre espace de noms (`vue.parametres.<radical>`) : un champ de table et une variable peuvent porter le même nom (`theta_CB`, `pi_etoile`).
3. **Schéma v3 : variables d'état des blocs 7 et 8** (toutes `float` ; P96) :

| Nom | Ouverture du pas t | Unité | Invariance | Propriétaire | Phase | Valeur stationnaire |
|---|---|---|---|---|---|---|
| `i_L` | i_{L,t} | par an, taux de flux | `sans_dimension` | `banque` | 8c | i_CB + ϖ_L (`sec:banque-stationnaire`) |
| `i_D` | i_{D,t} | par an, taux de flux | `sans_dimension` | `banque` | 8c | i_CB − ϖ_D (idem) |
| `r_hat_etoile` | r̂\*_t | par an, taux de croissance | `sans_dimension` | `banque_centrale` | 1 | r̄ (`sec:banque_centrale-stationnaire`) |
| `pi_etoile` | π\*_t | par an, taux de croissance | `sans_dimension` | `banque_centrale` | 1 | π\* déclarée (BC4 ; ADR 0010) |

   i_CB vaut (1 + r̄)(1 + π\*) − 1 à l'état stationnaire. Ordre (H1.5) : `i_L`, `i_D` (module nouveau `nations.etat.banque`), puis `pi_e`, `r_hat_etoile`, `pi_etoile` (`nations.etat.banque_centrale`). Les valeurs du pas suivant sont lues sous `<nom>_suivant` par un lecteur qui les déclare ; aucun ne le fait au socle (`sec:banque_centrale-phases`). **`VERSION_SCHEMA` = 3** dès le premier commit qui modifie le schéma (#61, rang 3) et jusqu'à la fusion de J3-c, sans incrément pendant la branche (a13 § 1.5) ; journal : « 3 (14/11/2026, #61, #91, #90 ; ADR 0013, annotation du 14/11/2026 ; P96) : i_L, i_D, r̂\*, π\* ». **Une sauvegarde v2 est refusée** (D4 ; critère de #61).
4. **Domaines** (D1, H1.6 complétés ; `defaut_de_domaine` et `Vue.ecrire_etat`, forme non (condition), sans écrêtage) : `pi_etoile` refusée si **non (1 + π\* > 0)** (domaine du type ; facteur de Fisher de BC1 et f(π\*) de Γ^e) ; `r_hat_etoile`, `i_L`, `i_D` : **finitude seule, déclarée**, sans condition de signe (i_D et i_CB peuvent être négatifs, r̂\* n'a pas de plancher : M31, M32). **Glissement** : `Vue.glissement()` refuse (`RefusDuMoteur` nommant pas, étape, bloc et valeur) un glissement qui n'est pas tel que 1 + π_{t−1} > 0, **y compris −1 exactement**, rendu par `registre.glissement` quand le rapport des prix est inférieur à 2^−54 ; **refus explicite, jamais écrêtage**. C'est la précondition de BC3 (P92), placée dans la vue comme le contrôle de domaine d'`ecrire_etat` (B2) ; `registre.glissement` reste une fonction pure (F3).
5. **Variables du pas (H2 complété)** :

| Nom | Écrivain, étape | Unité | Lecteurs (bloc, étape) |
|---|---|---|---|
| `i_CB` | `banque_centrale`, 1 (2ᵉ groupe) | par an, taux de flux | `banque` (6 : B5 ; 8c : B1, B2) ; `banque_centrale` (8a : BC7, BC8) ; `finances_publiques` (6, 7) |
| `i_regle` | `banque_centrale`, 1 | par an, taux de flux | observation (prescription restituée) |
| `theta_CB` | `banque_centrale`, 1 | fraction | `finances_publiques` (7) |
| `Pi_CB` | `banque_centrale`, 1 | u.m. par pas | `banque_centrale` (8b : BC9) ; `finances_publiques` (7 ; E1 du bloc d'essai 9) |
| `Pi_Bk` | `banque`, 6 | u.m. par pas | observation |

   **Lectures d'ouverture et du grand livre, par siège** (H2.5 complété) : `banque_centrale` 1 : ouverture `pi_etoile`, `r_hat_etoile`, `pi_e`, `B_CB`, `L_CB`, `Res` ; registre : `glissement` ; jamais W_t, p_t ni U_{t−1}. BC6 s'exécute sous sa forme générale, (i_CB B_CB + i_CB L^CB − i_CB Res)/n_a ; la forme « au socle », i_CB (E^CB + M^G)/n_a, est une identité de bilan vérifiée par test, non exécutée (elle lirait une valeur nette, H5.3). 8a : ouverture `Res`, `L_CB` ; pas `i_CB`. 8b : pas `Pi_CB`. `banque` 6 : ouverture `L`, `B_Bk`, `Res`, `L_CB`, `D_H`, `D_F`, `i_L`, `i_D` ; pas `i_CB` ; grand livre : montant exécuté de la ligne 18. E^Bk_t est calculé par le bloc depuis ces six positions (L + B_Bk + Res − D_H − D_F − L^CB), sans lecture de valeur nette (H5.3 reste fermé) ; un test le compare à `valeur_nette_stock` de la banque à l'ouverture, à ε × S^Bk. 8c : grand livre `position("Res")` (après 8b, A3.3) ; ouverture `L_CB` ; pas `i_CB`. Lignes proposées : `banque` 9, 10, 15 (6) et 21 (8c) ; `banque_centrale` 12, 13 (8a) et 16 (8b).
6. **Tables `banque` et `banque_centrale`** (F1, H3 complétés ; P96 ; synthèse du rang 1a, § 6). Valeurs indicatives = défauts du script (H3.3), égalité testée ; aucune unité nouvelle.

| Table | Nom | Symbole | Valeur | Unité | Domaine |
|---|---|---|---|---|---|
| `banque` | `varpi_L` | ϖ_L | 0,02 | par an, taux de flux | fini, sans signe (la condition d'existence du dividende stationnaire le contraint, script) |
| `banque` | `varpi_D` | ϖ_D | 0,01 | par an, taux de flux | idem |
| `banque` | `vartheta` | ϑ | 0,10 | fraction | ϑ > 0 |
| `banque_centrale` | `a_pi` | a_π | 0,5 | sans dimension | 0 < a_π < 1,5 |
| `banque_centrale` | `a_I` | a_I | 0,25 | par an, taux de flux | a_I > 0 |
| `banque_centrale` | `lambda_e` | λ_e | 0,2 | par an, taux de flux | 0 < λ_e ≤ n_a (P65) |
| `banque_centrale` | `theta_CB` | θ_CB | 0 | fraction | 0 ≤ θ_CB ≤ 1 |
| `banque_centrale` | `pi_etoile` | π\* | 0,02 | par an, taux de croissance | 1 + π\* > 0 |
| `banque_centrale` | `r_bar` | r̄ | 0,01 | par an, taux de croissance | r̄ > −5 % (C51 ; contient 1 + r̄ > 0) |

   Le script nomme `pi_cible` et `rbar` ce que les tables nomment `pi_etoile` et `r_bar` ; le test d'égalité porte la correspondance, le script n'est pas renommé. `EnsembleDesParametres` reçoit les champs `banque` et `banque_centrale` (H3.5). La valeur initiale de la variable d'état `pi_etoile` est le paramètre `pi_etoile` (BC4 ; état résolu).
7. **Γ^e et `facteur_g`** (C3, H4 précisés ; P88, #125 point 1). f(x) désigne `facteur_par_pas(TauxDeCroissance(x))`. **`facteur_g` = f(g_pr) · f(g_N)** ; `g` reste publiée comme grandeur de définition (label `None`), mais `facteur_g` n'est plus calculé depuis g. Après `facteur_g`, dans cet ordre : `pi_etoile_pas` = f(π\*_t) − 1, **`Gamma_e` = `facteur_g` · f(π\*_t)**, `gamma_e` = Γ^e − 1, π\*_t lue à l'ouverture (`pi_etoile`) ; une balise `eq:moteur-croissance-nominale-attendue` dans la fonction de `Gamma_e`, renvois pour les deux autres ; aucun bloc ne recalcule Γ^e (contrôle statique, critère de #61). *Mention datée du 14/11/2026 sur H4 (a13 § 4)* : la forme `facteur_par_pas(TauxDeCroissance(g))` est remplacée par le produit. Mesures de `macro` (rang 1a) : trajectoires identiques au bit à la référence sur 720 pas aux trois π\* ; écart au plus 5,6e−14 hors référence ; Γ^e à 4,44e−16 de la forme directe ; tableau avant / après et visa de `macro` dans les commits de #61.
8. **i_res ≡ i_CB et i_B ≡ i_CB** : identités de notation, **aucune variable `i_res` ni `i_B`** ; la ligne 12 (BC7) et BC6 se calculent sur `i_CB`. La **question 2 de la fiche 8 est close** (ADR 0011, P6). Un corridor non nul (J6, décision citant M32) ferait de i_res une variable du pas du bloc 8, écrite en phase 1, sans changer de contrat.
9. **Formes d'écriture déclarées** (A8 précisé ; P92, P93). Une forme d'écriture est algébriquement égale à l'équation de la spécification ; l'équation reste écrite telle quelle, et son encadré déclare la forme exécutée (surface de `docwriter`, rang 7) ; ce n'est ni une borne ni un drapeau. **B7** : ΔL^CB = −min(Res^{8b} ; L^CB) (A8.1, M1). **BC3** : π^e_{t+1} = (1 − c) π^e_t + c π_{t−1}, c = `par_pas(λ_e)` ; la forme littérale rend π^e_{t+1} = −1 dans 13 553 tirages adverses sur 1 954 258, la forme convexe dans aucun (mesure de `monnaie`, non une preuve). Test de l'invariant π^e > −1 (#91) : 10^6 tirages à graine déclarée sous 0 < λ_e ≤ n_a, π^e_t > −1 et la précondition 1 + π_{t−1} > 0 telle que calculée, plus un lot adverse sur les bords ; le contrôle de domaine d'`ecrire_etat` reste en place. `outils/etat_stationnaire.py` est aligné sur les deux formes (P93 ; précédent de P72), avec tableau avant / après (#90, #91).
10. **Concordance** : **57 labels** attendus à la fin de J3-c (40 + 7, B1 à B7 + 9, BC1 à BC9 + 1, `eq:moteur-croissance-nominale-attendue`), décompte du § 1 confirmé ; aucun label pour i_res, γ^e ni π^{∗,pas}. L'annualisation inverse (F2) n'a pas de consommateur dans les blocs 7 et 8 (BC1 à BC3 lisent le glissement annuel) : elle n'est pas écrite en J3-c.
11. **Mentions datées de P80** (14/11/2026). H1.8 : « Position K : même domaine strict en J3-c » se lit **J3-d**, avec #67. H3.4 : « table … complétée en J3-c » se lit **J3-d**, avec #67. Rien de J3-c n'en dépend (mesure de `macro`, rang 1a).

**Effet sur les résultats** : aucun par l'annotation. P88 : identique au bit à la référence, écart au plus 5,6e−14 ailleurs ; P93 : le script change à l'arrondi (Res_1 < 0 dans 5 cas sur 9, de −1,3e−18 à −2,1e−17, avant alignement) ; tableaux avant / après dans les commits concernés. **Surface documentaire** (rang 7, `docwriter`, un commit `docs:` par issue) : unités et domaines des quatre variables d'état et des deux tables (`tab:calibration`, noms `\code{nations.moteur.parametres.<radical>.<NOM>}`) ; formes exécutées de B7 et BC3 ; i_res ≡ i_CB ; Γ^e et `facteur_g` en produit (`sec:cadre-calendrier`) ; refus d'un glissement hors domaine ; BC6 exécutée sous sa forme générale ; mentions de P77.

Issues : #61, #91, #90, #125 (point 1), #119 ; renvoi : `docs/feuille-de-route.md` § 1 (rang 1b de J3-c) et § 4 (P87 à P99).

### Annotation du 14/11/2026 (rang 9 de J3-c, consignation) : H5.3 en liste blanche, lecteurs du pas, E^Bk, R2, A8.2, points 4, 7 et 9 tels qu'exécutés

Rédigée par `architect` (Opus) au rang 9 de J3-c (PR #129, tête `aebbd1d`), d'après les décisions P100 à P110 du 14/11/2026 (`docs/feuille-de-route.md` § 4) et les comptes rendus des rangs 2 à 6 (commentaires de la PR #129). **Aucune décision nouvelle** : elle enregistre l'état exécuté et corrige l'ADR, qui reste la référence. L'état consolidé (Contexte à Conséquences) est inchangé, à 38 865 octets (`head -186 | wc -c`), sous le plafond de 40 ko (P97).

1. **H5.3, état exécuté** (#121, P81, P110 ; `87897bc`). Le refus par liste noire devient une **liste blanche** : importations admises `__future__.annotations`, `contrat_bloc` (`DeclarationDeBloc`, `Siege`, `Lecture`, `OUVERTURE`, `REGISTRE`, `GRAND_LIVRE`) et la liste fermée de `conversions` ; `math` importé entier seulement ; natifs admis `float`, `int`, `str`, `tuple`, `min`, `max`, pris dans une liste figée de **149 noms natifs** (Python 3.12). Tout le reste est refusé, dont l'importation d'un module de `nations` entier et d'un autre bloc. Refusés en outre : noms spéciaux (sauf l'affectation de `__slots__`), attributs privés ou spéciaux, attributs d'introspection (`f_`, `co_`, `gi_`, `cr_`, `ag_`, `tb_`), `format` et `format_map`. **Méthodes `phase_*` verrouillées** : signature exacte `(self, vue)`, liée par un `def` unique sans décorateur dans le corps de la classe. Douze contournements (six de #121, trois relevés par `coder`, trois de l'audit) sont refusés. **La mention « Contournements restants : #121 » est retirée.**
2. **ADR 0012, annotation du 13/11/2026, point 5.3** : la forme `from nations.moteur import contrat_bloc` (module importé entier) **n'est plus admise** ; on importe les noms de `nations.moteur.contrat_bloc`.
3. **Point 5 de l'annotation du rang 1b, compléments** :
   - **reconstruction de Γ^e refusée dans un bloc** : contrôle statique de la reconstruction de f(π\*) (`facteur_par_pas` sur π\*, `**` à exposant non entier, `exp` d'un `log` de π\*, `math.pow` non entier, `sqrt`, `cbrt`), marquage par excès admis si le message nomme la chaîne de dépendance (`c50be3f` ; visa de `monnaie`, rang 4) ;
   - **lecteurs de `Pi_CB` côté `finances_publiques`** : en phase 7 (exigence E3 du bloc d'essai 9) et en 8b (exigence E1, couverture de la ligne 16) ; décision de `monnaie` au rang 4 ; le bloc 9 réel (J3-d) les déclare ;
   - **E^Bk calculé sur les six positions** d'ouverture du bloc 7 (P107), confirmé.
4. **Point 6, R2** : la lecture de `parametres.banque_centrale.pi_etoile` dans un bloc est **refusée statiquement** ; tout bloc lit π\*_t à l'ouverture (ADR 0010 ; `a3702ba`).
5. **A8.2, exception** : « toute règle qui les lit écrit max(0 ; ·) » ne vise pas **E^Bk**, qui lit les positions **brutes** D_H et D_F ; B4 et B5 les lisent en max(0 ; ·). C'est la seule forme qui garde à la fois l'ancre de B6 et C41 (avis de `monnaie`, rang 5 ; `bba1125`).
6. **Points 4 et 9 tels qu'exécutés.** Point 4 : le refus de `Vue.glissement()` couvre aussi un glissement **non fini** (P106). Point 9 : B7 en −min et BC3 en forme convexe exécutées ; `outils/etat_stationnaire.py` aligné (P93) ; **`outils/maquette_conjointe.py` aussi aligné sur B7 en −min**, au-delà de la lettre de P93, parce que `test_carte_du_socle_egale_un_pas` exige que la maquette égale le script (cause mesurée par `macro` : bruit d'arrondi de Res_1 amplifié en 1/h ; visas de `macro` et `monnaie` ; temps de doublement 381,588526 → 381,588529, valeur publiée « 382 » inchangée). Mesures citées des messages de `520dfce` et `2c4de6e`, non remesurées ici : forme littérale de BC3 à −1 dans 40 030 cas d'un lot adverse de 201 090 ; forme littérale de B7 en échec sur 302 911 tirages de 10^6.
7. **Point 7 et « Effet sur les résultats », correction prospective** (réserve R1 de `macro`, `0f4954c`). « Écart au plus 5,6e−14 hors référence » se lit, sur 720 pas à g_N = 0,001 et π\* = 0 ; 2 ; 10 % : variables d'état des blocs 2 à 4, écart relatif à la grandeur elle-même au plus 4,88e−14 ; 5,55e−14 ; 4,88e−14 ; positions, |Δ| rapporté à S du détenteur au plus 6,96e−14 ; 4,61e−14 ; 1,80e−14 ; V^flux, |Δ|/S au plus 6,98e−14 ; 4,59e−14 ; 1,84e−14 ; montants exécutés, |Δ|/max_s S au plus 1,3e−16 ; ξ, nulle à l'état résolu, au plus 9,2e−15 en absolu. L'ancien texte reste publié ci-dessus.

**Effet sur les résultats** : aucun. Issues : #121, #61, #91, #90, #119 ; renvoi : `docs/feuille-de-route.md` § 4 (P100 à P110).

### Annotation du 14/11/2026 (rang 1b de J3-d1) : schéma v4, tables des blocs 5 et 6, domaine strict de K, domaine des plans, exceptions d'identité à A8.2, A8.1 sous la lecture nette, couverture X4, 76 labels

Rédigée par `architect-approfondi` (Opus, effort `high`, sans Fable) au rang 1b de J3-d1 (`claude/j3-menages-investissement`, PR #136, tête `50c55f0`), en application des décisions du mainteneur du 14/11/2026 (P119 à P126, `docs/feuille-de-route.md` § 4), de l'avis du rang 1a de `macro` (pilote) et de celui de `monnaie` (résumé en P124 à P126). **La décision de l'ADR 0012 est inchangée** ; l'annotation précise A3.1, A8, C1, D1, D2, D4, F1, H1, H2 et H3, **avant le code de #124, #60 et #67**. Les noms de code sont des contrats (Décision, point 5). Trois points de forme que les textes ne tranchent pas sont soumis au mainteneur (Q1 à Q3, en fin d'annotation) : la forme recommandée est écrite **sous réserve**, et une mention datée enregistrera la décision. L'annotation ne change aucun résultat.

1. **Schéma v4 : variables d'état des blocs 5 et 6** (C1, D1, H1 complétés). Constat à `50c55f0` : aucune n'existe. `src/nations/etat/` compte cinq modules de bloc (`schema.py:60`, `schema.py:98` : production, travail, prix, banque, banque centrale), `VERSION_SCHEMA = 3` (`schema.py:66`), et le moteur refuse une variable d'état que son propriétaire n'écrit pas dans le pas (`ordonnanceur.py:845-848`). Variables nouvelles, toutes `float` :

| Nom (sous réserve de Q1) | Ouverture du pas t | Unité | Invariance | Propriétaire | Phase | Valeur à l'état initial résolu | Domaine |
|---|---|---|---|---|---|---|---|
| `YD_m1` | YD_{t−1} | u.m. par pas | `nominal` | `menages` | 9 (groupe des blocs ; H7, montants exécutés) | clé `YD_m1` de `ouverture()` du script | finitude seule, déclarée (YD < 0 possible, plancher de H5) |
| `ti` | ti_t | fraction | `sans_dimension` | `investissement` | 5 (S6) | (n_a[(1 + g)^{1/n_a} − 1] + δ) κ/t̄u (`sec:investissement-stationnaire`) | **ti > 0** |
| `y_m1` | y_{t−1} | u.v. par pas | `volume` | `investissement` | 5 (y_t retenue) | y_0/(1 + g)^{1/n_a} (idem) | **y_m1 ≥ 0** |
| `T_F_m1` | T_{F,t−1} | u.m. par pas | `nominal` | `investissement` | 9 (groupe des blocs ; ligne 7 exécutée, colonne des entreprises) | T_{F,0}/Γ̄ (idem) ; nulle au socle (τ_F = 0, M33) | finitude seule, déclarée |
| `varrho_bar_L` | ϱ̄_L | par an, taux de croissance | `sans_dimension` | `investissement` | 2 (sous réserve de Q2) | ϱ_{L,0} = r̄ + ϖ_L/(1 + π\*) (`sec:banque-taux`) | finitude seule, déclarée |

   - **Domaines** : forme non (condition), dans `defaut_de_domaine` et `Vue.ecrire_etat`, refus avec diagnostic, jamais écrêtage (H1.6). ti > 0 et y_m1 ≥ 0 sont la condition de forme qui tient I^plan ≥ 0 par S3 et S4 avec P > 0 (point 4) ; **visa de `macro` au rang 4**, sur le précédent de H1.7. Unité de ϱ̄_L : celle de r̄ et de r̂\* (taux de Fisher, employé en base annuelle sans conversion).
   - **Ordre** (H1.5) : par radical dans l'ordre des blocs, production, travail, prix, **menages**, **investissement**, banque, banque centrale. Deux modules nouveaux, `nations.etat.menages` et `nations.etat.investissement`.
   - **Version** (D2) : **`VERSION_SCHEMA` = 4** dès le premier commit qui modifie le schéma (#60, rang 3, `YD_m1`), et jusqu'à la fusion de J3-d1, sans incrément pendant la branche (précédent du point 3 de l'annotation du rang 1b de J3-c). Journal : « 4 (14/11/2026, #60, #67 ; ADR 0013, annotation du 14/11/2026 (J3-d1)) : YD_{t−1} ; ti, y_{t−1}, T_{F,t−1}, ϱ̄_L ». **Une sauvegarde v3 est refusée** (D4 ; critère de #60). L'insertion des deux radicaux avant `banque` change l'ordre des clés de la sauvegarde ; la version le couvre.
   - **Variables du pas** : `C_plan` et `I_plan` gardent leur nom (H2.2) ; les autres (C^règle, ϱ_L, tu\*, I^{vol,plan}, ΔL^d…) suivent H1.1 et sont listées par `coder` dans le commit qui les crée.
2. **Tables `menages` et `investissement`** (F1, H3 complétés). Module nouveau `nations.moteur.parametres.menages` ; `investissement` est complétée (H3.4, P80) ; `EnsembleDesParametres` reçoit le champ `menages` entre `prix` et `investissement` (H3.5). Valeurs indicatives = défauts de `outils/etat_stationnaire.py` (H3.3), égalité testée ; le script nomme `lv` ce que la table nomme `lv_etoile`, et le test porte la correspondance (précédent de `pi_cible`). Aucune unité nouvelle : η_r et ζ sont `sans dimension`, sur le précédent de β et de a_π, la source gardant « par unité de taux réel annuel, sans conversion ».

| Table | Nom | Symbole | Valeur | Unité | Domaine (`DefautDeDeclaration`) | Source | Étiquettes |
|---|---|---|---|---|---|---|---|
| `menages` | `nu_H` | ν_H | 1,0 | années | ν_H > 0 | `tab:calibration` (indicative) ; M27 ; calibration #62 | `eq:menages-richesse-visee` |
| `menages` | `lambda_H` | λ_H | 0,4 | par an, taux de flux | 0 < λ_H ≤ n_a (P65) | idem | `eq:menages-plan-consommation` |
| `investissement` | `delta` | δ | 0,05 | par an, taux de flux | 0 < δ < n_a (en vigueur) | inchangée | ajouter `eq:investissement-demande-credit` |
| `investissement` | `tu_bar` | t̄u | 0,8 | fraction | t̄u > 0 | M28 ; `tab:calibration` (indicative) | `eq:investissement-utilisation-visee`, `eq:investissement-part-visee` |
| `investissement` | `lambda_ti` | λ_ti | 0,02 | par an, taux de flux | 0 < λ_ti ≤ n_a | M28 ; hypothèse | `eq:investissement-part-visee` |
| `investissement` | `eta_r` | η_r | 2,0 | sans dimension | η_r ≥ 0 | M28 ; hypothèse | `eq:investissement-plan` |
| `investissement` | `zeta` | ζ | 4,0 | sans dimension | ζ ≥ 0 | M28 ; à calibrer (4 à 8), valeur du script | `eq:investissement-utilisation-visee` |
| `investissement` | `lv_etoile` | lv\* | 0,4 | fraction | 0 ≤ lv\* < 1 | M28 ; hypothèse | `eq:investissement-demande-credit` |
| `investissement` | `nu_F` | ν_F | 1/6 | années | ν_F > 0 | M28 ; hypothèse | `eq:investissement-depots-vises` |

   - **Conditions jointes** (`sec:menages-conditions`, « contrôlées au chargement de la table de calibration ») : 0 < ν_H λ_H < 1 dans `__post_init__` de la table `menages` ; **coefficient de richesse** λ_H/n_a + ν_H λ_H π^{∗,pas} > γ^e, qui lit `production`, `travail` et `banque_centrale`, dans `__post_init__` d'`EnsembleDesParametres`, sur le paramètre π\* (valeur initiale de la cible, BC4 à levier fermé) ; les facteurs passent par `facteur_par_pas` (F2, conversion unique). Au J4, le domaine du levier de cible prend le relais (G4).
   - **Hors des tables** : A > 0, taux de distribution dans [0,2 ; 0,9] (#55), η_r ≥ 1,005 (seuil (d1)), λ_ti × 2 dans le domaine de stabilité. Ce sont des contraintes de calibration, contrôlées par le script et les tests, non des refus (fiche 6, § 9.2). Le plafond de H5 n'a pas de champ (décision du 03/10/2026, lecture (i)). ϱ̄_L, π\*, g, Γ^e ne sont pas des paramètres (`sec:investissement-conditions`).
   - Les blocs 5 et 6 lisent π\*_t à l'ouverture, jamais `parametres.banque_centrale.pi_etoile` (R2, refus statique).
3. **Domaine strict de K** (P80 ; H1.8 et H3.4 se lisent J3-d). `ouvrir_pas` refuse **K < 0** à côté de IN (`grand_livre.py:235-239`) : règle `STOCKS_OUVERTURE` étendue à « IN ≥ 0, K ≥ 0 », `controle_de_signe` sans ε ni S^F ; il couvre l'état initial, la reprise et chaque pas (A5, M95-13). **Sans réécriture** : seules les lignes 3 (+I, phase 5) et 8 (−δK/n_a, phase 6) touchent K (`catalogue.py:294`, `catalogue.py:306`), et K_{t+1} = fl(fl(K_t + I_t) − fl(c K_t)) ≥ 0 par monotonie de l'arrondi, si c = `par_pas(δ)` < 1 (domaine de δ), si la ligne 8 porte sur K d'ouverture sous cette forme (S7) et si I_t ≥ 0 (point 4 et N6). *Hypothèse* à éprouver par un lot adverse et des pas enchaînés, sur le précédent de P72 (critère de #67).
4. **Domaine des plans** (P120, #124 ; voie (a)).
   - `C_plan`, `I_plan`, `G_plan` (u.m., phase 2) sont refusés à l'écriture si **non (valeur finie et ≥ 0)** ; NaN et ±∞ compris ; −0,0 admis. Jamais d'écrêtage.
   - **Exception typée** : **`PlanHorsDomaine`**, dérivée de `RefusDuMoteur` (`nations.moteur.diagnostics`), champs t, étape, bloc écrivain (apposé par la vue), nom, valeur dans le message. Dérivée : A6 et le contrat « refus à l'appel » restent tenus ; typée : le test de #124 la distingue. Elle couvre aussi la valeur non finie d'un plan, contrôlée avant le refus générique de l'espace du pas (`ordonnanceur.py:213-215`).
   - **Place** (sous réserve de Q3) : liste fermée `DOMAINES_DU_PAS` du moteur (nom → condition en clair, prédicat), contrôlée par l'espace du pas à l'écriture, quel que soit l'écrivain : blocs réels, blocs d'essai 5, 6 et 9, `chocs_des_plans` des tests. d ≥ 0 (N6) en découle avec p > 0, sans contrôle propre ; le cas d < 0 de #124 tombe à l'écriture du plan.
   - **Conditions**, qui tiennent les plans ≥ 0 par la forme et non par le refus : H5 lit max(0 ; D_H), et H3 et H4 lisent V_H = max(0 ; D_H) + B_H ; E1 lit max(0 ; M^G) (A8.2, déjà prescrit ; code dans #132) ; F3 lit max(0 ; D_F), dans le terme de dépôts et dans les intérêts (comme B4) ; S3 et S4 tiennent I^plan ≥ 0 par ti > 0, y_m1 ≥ 0 et P > 0 (point 1). Chaque lecture en max(0 ; ·) est testée à −1 ulp et à −0,5 ε S (A8.2). Sans elles, une poussière déclencherait `PlanHorsDomaine` : l'arrêt sur l'arrondi qu'a écarté la lecture nette (ADR 0012, option (i-e)).
5. **Exceptions d'identité à A8.2** (P125 ; #103). « Toute règle qui les lit écrit max(0 ; ·) » ne vise pas, outre E^Bk (annotation de consignation, point 5) :
   - **E6** : M^G lu **brut** dans le plafond des transferts, sous le max(0 ; ·) extérieur qui tient Tr_t ≥ 0 (lecture (ii) de `monnaie`) ;
   - **E9** : M^G **brut**. Em_t contient M^{G*}_t − M^G_t : la lecture brute absorbe la poussière à l'émission du pas, alors que max(0 ; ·) la laisserait persister (avis de `macro`, rang 1a, § 5) ;
   - **E4** : assiette B − M^G − E^CB lue **brute**. C'est la dette consolidée d'ouverture, assiette aussi du canal rentier (ligne 15) ; un max(0 ; ·) romprait l'égalité de T^cou et du surcroît de dividende de la banque (`sec:finances_publiques`, couverture réelle).

   La liste est **fermée** : toute autre lecture brute de D_H, D_F ou M^G par un bloc est un défaut. Chaque exception est déclarée au site de lecture (commentaire qui cite ce point) et testée sous une poussière à −1 ulp (E9 l'absorbe ; E4 garde l'identité de bilan ; E6 rend Tr ≥ 0). Code dans #132 (J3-d2). Textes de la spécification (l. ~3194, ~3342, ~3356) réécrits en correction prospective au passage de `docwriter` de J3-d1 (commit `docs:` de #103), ancien texte publié avec sa date.
6. **A8.1, annotée** (P126). « E1 et H5, exactes par construction (M7, M8) » se lit : E1 et H5 bornent **le plan** exactement, G^plan ≤ max(0 ; M^G) et C^plan ≤ max(0 ; D_H). La ligne exécutée (2 ou 1), p·v avec v tiré de N6, peut toutefois dépasser le plan d'un ulp : p·(G^plan/p) ≠ G^plan dans environ 5,7 % des tirages (0,0572 au-dessus, 0,0568 au-dessous sur 10^5 tirages ; mesure de `monnaie` confirmée par la session, P126, non remesurée ici).
   - La poussière laissée ainsi sur M^G et D_H en fin de phase 5 est **admise sous la lecture nette** (A5, −ε × S_payeur), comme pour D_H et D_F jusqu'ici : E1 et H5 sortent de la règle « défaut du bloc » de A8.1 et relèvent de A8.2.
   - Le reste de A8.1 est inchangé (B7, E13 par le montant couvert, N8).
   - Écartée : forme exacte de la ligne 2 et de H5 (P126).
   - La condition de réouverture « si une saturation à une ligne n'admet pas d'écriture en min/max » (Décision, point 6) **n'est pas déclenchée** : la forme exacte existe et a été écartée ; le min porte sur le plan.
   - Les critères « Bornes (d) » de la fiche 5 et de M^G se lisent sous la lecture nette (#103, P125).
7. **Contrat de la couverture X4** (P124 ; code à `coder`, rang 5).
   - **Place** : option de composition `couverture_x4()` dans `tests/invariants/socle_partiel.py`, sur le précédent d'`emission_e3()` (`socle_partiel.py:729`). Elle rend les options du bloc d'essai 9 (déclaration, règle de la ligne 7). Jamais dans `src/` (H6). **Jamais dans le banc de P87** : verdicts de P87 identiques au bit, testés.
   - **Règle** : ligne 7, part des ménages = T_H du sentier + T^cou_t, avec T^cou_t = φ (i_CB,t − i_ref,t) A_t, convertie au pas par `par_pas` (conversion linéaire, F2), φ = 1 et i_ref,t = (1 + r̄)(1 + π\*_t) − 1. Lectures :
     - π\*_t à l'ouverture (`pi_etoile`) ;
     - r̄ du sentier (`sentier.par.rbar`, jamais `parametres.banque_centrale`) ;
     - i_CB en phase 1.
   - **Assiette** : A_t = B_t − M^G_t − E^CB_t, sur les positions d'ouverture, **lue brute** (point 5, E4). E^CB est calculé sur les quatre positions de la banque centrale (B_CB + L^CB − Res − M^G), sans lecture de valeur nette (précédent d'E^Bk, P107).
   - **Lectures déclarées** : ouverture `pi_etoile`, `B_H`, `B_Bk`, `B_CB`, `L_CB`, `Res`, `M_G` ; phase 1 `i_CB`. Variable du pas écrite : `T_cou`.
   - **Grandeur nulle** : T^cou entre dans `GRANDEURS_NULLES` à 1e−12 × S^G, nullité **calculée** (i_CB = i_ref sur le sentier ; P121).
   - **Étiquette** « couverture X4 active » sur toute mesure faite avec l'option (H6).
   - **Composition** : avec `emission_e3()`, déclaration et règles identiques dans les deux ordres (test). Les deux options touchent des sièges et des lignes distincts : X4 la ligne 7 en phase 6, E3 les lignes 19a en phase 7.
   - **Refus sur un bloc 9 réel** : refus typé à l'assemblage, jamais ignoré ; nom au choix de `coder`.
   - **Lignes à choc long** : aucun critère d'arrivée sur 720 pas à π\* = 10 % (demi-vie de 1 799 pas) ; signe et délai seulement.
   - **Nom** : X désigne une exigence du bloc d'essai, distincte d'E1 à E13 de la spécification. #133 renommera E1 à E3 du bloc d'essai dans la même série (X1 à X3, recommandation, décidée dans #133) et gardera X4.
8. **Concordance** : **76 labels** attendus à la fin de J3-d1, soit 57 + 6 (H2 à H7 ; H1 est `eq:moteur-croissance-nominale-attendue`, déjà compté) + 11 (S1 à S7, F1 à F4) + 2 (d et tu, #123). Base remesurée à `50c55f0` : `uv run python outils/concordance_spec_moteur.py --strict` → « labels eq: 57 ; balises # eq: 57 […] Aucun écart ». Aucun label pour la tenue des variables retardées ni pour ϱ̄_L (fiche 6, § 9.1), ni pour X4 (tests).

**Questions au mainteneur** (formes non tranchées par les textes ; recommandations de l'architecte) :
- **Q1. Noms des variables retardées.** H1.1 omet la date, mais `y` est déjà une variable du pas (bloc 2, phase 4) dans le même espace de noms.
  - (i) H1.1 à la lettre, `YD` et `T_F`, et `y_m1` par exception pour la seule collision ;
  - (ii) suffixe `_m1` pour toute variable d'état qui retient une grandeur du pas (`YD_m1`, `y_m1`, `T_F_m1`), H1.1 complété.

  Recommandation : (ii). Une seule règle, sans collision future (T_F, grandeur du bloc 9 en J3-d2), et des noms égaux aux clés d'`ouverture()` du script.
- **Q2. Statut de ϱ̄_L.** Les textes l'excluent des paramètres (`sec:investissement-conditions` ; fiche 6, § 9.2), constante « tenue avec l'état, jamais recalculée » ; ils ne fixent pas la forme.
  - (i) variable d'état d'`investissement`, recopiée de l'ouverture à chaque pas (phase 2) : contrat C2 inchangé, sauvegardée, égalité au bit testée sur 720 pas ;
  - (ii) catégorie nouvelle de champ d'`EtatPays`, « constante résolue », écrite par aucune phase et portée par le moteur, comme les champs d'identité : C1, C2 et D1 modifiés.

  Recommandation : (i). Le contrat est inchangé ; (ii) n'a qu'un usage.
- **Q3. Place du domaine des plans.**
  - (i) liste `DOMAINES_DU_PAS` du moteur, contrôlée à l'écriture pour tout écrivain ;
  - (ii) domaine porté par le siège de chaque écrivain (`DeclarationDeBloc`).

  Recommandation : (i). C'est la précondition du lecteur (N6), tenue en un lieu qui couvre aussi les blocs d'essai et les plans exogènes des tests ; (ii) la répète chez trois écrivains et laisse un bloc d'essai l'omettre.

**Décisions du mainteneur du 14/11/2026** (P127 à P129, `docs/feuille-de-route.md` § 4) : Q1 **(ii)**, suffixe `_m1` (`YD_m1`, `y_m1`, `T_F_m1`) ; Q2 **(i)**, ϱ̄_L variable d'état d'`investissement` ; Q3 **(i)**, `DOMAINES_DU_PAS` du moteur. Les mentions « sous réserve de Q1 à Q3 » de la présente annotation sont levées dans ce sens.

**Effet sur les résultats** : aucun par l'annotation. Pour #124 et K, des refus seulement : les trajectoires de la référence restent identiques au bit (critère de #124).

**Surface documentaire** (rang 6, `docwriter`, un commit `docs:` par issue) :
- noms `\code{nations.moteur.parametres.menages.…}` et `…investissement.…` dans `tab:calibration` ;
- variables d'état des blocs 5 et 6, avec unités et domaines (`sec:menages`, `sec:investissement`) ;
- domaine strict de K, avec IN (`sec:cadre-phases`, chapitre du noyau) ;
- domaine des plans (`sec:production-ventes`) ;
- A8.1 et exceptions E6, E9, E4 (`sec:cadre-caisse`, l. ~689 ; `sec:finances_publiques`, l. ~3194, ~3342, ~3356).

Issues : #124, #60, #67, #123, #103 ; renvois : #132, #133, P80, P119 à P126 (`docs/feuille-de-route.md` § 4).

### Annotation du 15/11/2026 (rang 8 de J3-d1, consignation) : domaine des entrées de scénario (P138), refus du dépassement (P139), bornes (b) restreintes (P145), couverture X4 telle qu'exécutée, liste fermée des lectures brutes, 77 labels

Rédigée par `architect` (Opus) au rang 8 de J3-d1 (PR #136, tête `414a8a4`), d'après les décisions du mainteneur du 15/11/2026 (P142 à P146 ; P138, P139 et P141 confirmées par P144 ; `docs/feuille-de-route.md` § 4). **Aucune décision nouvelle** : elle enregistre l'état exécuté et le contrat partagé étendu par P138. L'état consolidé (Contexte à Conséquences) est inchangé.

1. **Domaine des entrées de scénario** (P138, confirmée ; contrat partagé étendu, B5 et G4 complétés).
   - **Liste fermée `DOMAINES_DES_ENTREES`** du moteur (`src/nations/moteur/ordonnanceur.py:203`), sur le modèle de `DOMAINES_DU_PAS` (P129) : nom → condition en clair et prédicat. Contenu à `f232b70` : `varsigma_L` seule, part refusée 0 ≤ ς_L ≤ 1, finie (contrôlé par `test_moteur_ordonnanceur.py:1220`). Une entrée hors de la liste n'a que le contrôle générique de finitude.
   - **Lieu** : à la publication des entrées en phase 0 (`_verifier_entrees`, `ordonnanceur.py:237-261`), avant le refus générique de finitude ; aucun bloc ne reçoit une part hors de [0 ; 1]. Jamais d'écrêtage.
   - **Exception typée `EntreeHorsDomaine`** (`src/nations/moteur/diagnostics.py:87`), dérivée de `RefusDuMoteur` ; champs : pas, étape « 0 », bloc « moteur », nom de l'entrée ; valeur et condition dans le message. Le contrat « refus à l'appel » (A6) reste tenu.
   - **ς_B** entrera dans la liste avec le bloc 9 réel (#132, engagement 5 du commentaire du 15/11/2026). La colonne « Lisent » de `tab:phases` n'ajoute pas « phase 0 » : l'exemption couvre les grandeurs publiées à l'ouverture, entrées de scénario comprises (`5e5662b`).
2. **Refus du dépassement** (P139, confirmée). Un `OverflowError` levé dans une méthode d'étape d'un bloc devient **`DepassementNumerique`** (`diagnostics.py:99`, traduction à `ordonnanceur.py:903`), dérivée de `RefusDuMoteur`, qui nomme le pas, l'étape et le bloc ; l'exception d'origine est chaînée. La traduction est **limitée à `OverflowError`** : un produit qui déborde sans exception rend ±∞ et s'arrête à son écriture, par `PlanHorsDomaine` pour un plan ou par le refus générique de finitude (#137 ; spécification, `fc48f6e`). Table du point 2 de l'annotation de J3-d1, tel qu'exécuté : η_r et ζ ont le domaine **0 ≤ · ≤ 20** (`src/nations/moteur/parametres/investissement.py:71`, `:79`) ; le script d'état stationnaire refuse le même ensemble (`4792a79`).
3. **Bornes (b) du bloc 6, restreintes** (P145, constat M1 de la revue finale, voie 2). « Pour toute entrée dans le domaine déclaré » (P139) se lit **sur le lot |Δϱ| ≤ 0,1 par an**. Au-delà, S6 composée avec S2 rend ti_{t+1} = 0 en double précision ; le pas est refusé par le domaine de l'état ti > 0 (H1.6 ; point 1 de l'annotation de J3-d1). Frontière publiée sans verdict par `test_frontiere_de_la_double_precision_des_bornes_b` (`tests/invariants/test_investissement.py`) ; remesurée au rang 8 : Δϱ = 3,307756 par an à ζ = 4, 0,661551 à ζ = 20 (`uv run pytest -q -s tests/ -k test_frontiere_de_la_double_precision_des_bornes_b`). Le choix entre une borne de domaine du taux réel et une forme bornée de S2/S6 est renvoyé à #143 ; il touchera ce contrat (domaine d'une entrée ou d'une variable du pas) et passera par une annotation.
4. **Couverture X4, point 7 tel qu'exécuté** (P124 ; `ea2e0da`).
   - **Grandeur nulle** : T^cou n'entre pas dans `GRANDEURS_NULLES` (liste du banc de P87, inchangée) mais dans la liste propre au banc de J3-d1, **`GRANDEURS_NULLES_DE_J3D1`** (`tests/invariants/socle_partiel.py:1071`), avec T_{F,t−1} et le terme T_F de la ligne 7 (P121) ; nullités **calculées** en exact ; `est_nulle` lit les deux listes. Motif : le banc de P87 ne relève pas ces grandeurs, et ses verdicts restent identiques au bit.
   - **Composition** : `composer()` (`socle_partiel.py:882`) assemble X4 et E3 et **refuse** (`OptionsIncompatibles`) deux options qui modifient le même siège d'un radical ou proposent une règle pour la même ligne : le résultat ne dépend pas de l'ordre par construction, ce qui tient la propriété « identiques dans les deux ordres » du point 7.
   - **Refus sur un bloc 9 réel** : `OptionSansBlocDEssai` (`socle_partiel.py:453`), refus à l'assemblage, jamais ignoré.
5. **Liste fermée des lectures brutes** (point 5 de l'annotation de J3-d1, complété ; constat R3 de `monnaie` à la validation du rang 6, `4b8ce65`). La liste s'énonce désormais en entier : **E^Bk** (bloc 7 : D_H et D_F bruts dans les six positions, P107) ; **E6**, **E9** et l'assiette de **E4** (bloc 9 : M^G brut, P125) ; dans `tests/`, l'assiette de X4, qui est celle de E4. Toute autre lecture brute de D_H, D_F ou M^G par un bloc est un défaut. **E5 et E12** lisent D̃_F = max(0 ; D_F) et D̃_H = max(0 ; D_H), comme F3 et la ligne 10 (correction prospective de la spécification du 15/11/2026, `4b8ce65` ; code dans #132), et l'épreuve à −1 ulp et à −0,5 ε S du critère « Lecture nette » du bloc 9 s'y étend (règle générale du point 4 ; engagement 4 sur #132). Notation de la spécification : D̃_H, Ṽ_H = D̃_H + B_H, D̃_F, nommées `D_H_net`, `V_H_net` dans `menages.py` (`046fcde`) ; V_H garde le seul sens de valeur nette du bilan. La localité de ces lectures (max(0 ; ·) calculé hors des fonctions balisées H3, H4, H5 et F3) est l'objet de #142, sans effet sur la trajectoire.
6. **Point 8, concordance** (P142, correction du critère de décompte avant son essai). F1 porte deux labels, `eq:investissement-demande-credit` et **`eq:investissement-credit-servi`** (ligne 18 sous ς_L ; balise dans `credit_servi`, `src/nations/blocs/investissement.py:145` ; `ed4c9c2`). Le décompte attendu est **77 labels** (57 + 6 + 12 + 2), et non 76. Remesuré à `f232b70` : `uv run python outils/concordance_spec_moteur.py --strict` → « labels eq: 77 ; balises # eq: 77 […] Aucun écart ».

**Effet sur les résultats** : aucun par l'annotation. Issues : #124, #60, #67, #123, #103 ; renvois : #132, #137, #142, #143 ; `docs/feuille-de-route.md` § 4 (P138, P139, P141, P142 à P146).

### Annotation du 15/11/2026 (rang 1b de J3-d2) : table du bloc 9, schéma v5 (Y^HS), ς_B dans les entrées à domaine, lectures brutes de M^G, un seul calcul de l'émission par pas, bloc d'essai 9 sous X1 à X4, F3 sur la colonne des entreprises

Rédigée par `architect` (Opus, sans Fable) au rang 1b de J3-d2 (`claude/j3-finances-publiques`, PR #146, tête `69624d5`), en application de P154 (annotation maintenant ; reconsolidation par un ADR nouveau au point d'étape après J3-d2) et des décisions P147 à P164 (`docs/feuille-de-route.md` § 4), **avant le code de #132**. **Aucune décision nouvelle** ; la décision de l'ADR 0012 et l'état consolidé (Contexte à Conséquences) sont inchangés. La spécification fait foi (`sec:finances_publiques-phases`, `tab:finances_publiques-phases`) ; la fiche 9, § 9.1, 9.4 et 9.6, en retard sur elle, est reprise par `docwriter` au rang 6. Constats faits à `69624d5`, commandes citées dans le compte rendu du rang 1b (PR #146).

1. **Table du bloc 9** (`finances_publiques` ; H2 complété ; aucun contrat partagé modifié). Transcription de `tab:finances_publiques-phases` ; la déclaration `PHASES` (`src/nations/moteur/phases.py:91-122`) porte déjà le bloc aux phases 2, 5, 6, 7 et 8 (b), avec les colonnes « Lisent » nécessaires (phase 7 : 1, 2, 4, 5, 6 ; phase 8 : 1 à 7), et l'exclut du groupe de la phase 9 (`menages`, `investissement`) : **`PHASES` ne change pas**.

| Phase | Lit | Écrit, ou propose au noyau | Équations |
|---|---|---|---|
| 0 | rien (exemption de la phase 0 : ς_{B,t} publiée par le moteur, P138) | rien | — |
| 1 | rien (leviers lus par le moteur ; i_CB, θ_CB, Π^CB écrits par `banque_centrale`) | rien | — |
| 2 | ouverture (dont max(0 ; M^G) pour E1, M^G brut pour E6, assiette brute pour E4) ; phase 1 : leviers, i_CB ; moteur : Γ^e, π^{∗,pas} ; paramètres U^eq, r̄ | `G_plan` (E1, `DOMAINES_DU_PAS`) ; Tr^lev, Tr (E6) ; T_H (E3), `T_cou` (E4) | E1, E3, E4, E6 |
| 5 | phase 5 : p, v_G | ligne 2 | E2 |
| 6 | ouverture (D̃_F pour E5) ; phase 1 ; lignes 1 à 5 exécutées ; ses calculs de la phase 2 ; δ | lignes 6, 7 (T_H + T_F), 11a à 11c ; transferts non versés | E5, E6, E7, **E13, première part** |
| 7 | ouverture : M^G **brut** (E9), B, D̃_H (E12) ; phase 0 : ς_B ; phase 1 : i_CB, θ_CB, Π^CB ; lignes 2, 5, 6, 7, 10, 11a à 11c, 14, 15 exécutées ; `T_cou` (phase 2) ; ν_G | M^{G*} (E8), Em (E9) ; lignes 19a-BC, 19a-ménages (E10), 19a-banque (E11) ; **Y^HS_t (E12), variable d'état** (point 2) | E8 à E12 |
| 8 (b) | phase 1 : Π^CB ; max(0 ; M^{G,8a}) au grand livre | montant couvert de la ligne 16 déclaré au noyau (A3.2) ; perte non couverte | **E13, seconde part** |
| 9 | rien | rien | — |

   - **E12 en phase 7** (ADR 0011, P3 ; M29), jamais dans le groupe de la phase 9. **E13 à deux parts** sous **un label** (critère de #132) : transferts non versés en phase 6, perte non couverte en 8 (b) ; les parts non payées sont enregistrées sans ligne nouvelle. **Treize labels** E1 à E13, une balise chacun ; concordance attendue à 90 (91 si #106 pose `eq:moteur-variation-tour`).
   - Noms des variables du pas : H1.1 et point 2 de l'annotation de J3-c ; `G_plan` et `T_cou` sont déjà fixés (P129 ; point 7 de l'annotation de J3-d1) ; les autres sont listés par `coder` dans le commit qui les crée.
2. **Y^HS en variable d'état : schéma v5** (C1, D1, D2 complétés ; **contrat partagé étendu**, dans la forme des annotations de J3-c, point 3, et de J3-d1, point 1). Constat : `VERSION_SCHEMA = 4` (`src/nations/etat/schema.py:79`), sept modules de bloc dans `src/nations/etat/`, aucun pour le bloc 9.

| Nom | Ouverture du pas t | Unité | Invariance | Propriétaire | Phase | Valeur à l'état initial résolu | Domaine |
|---|---|---|---|---|---|---|---|
| `Y_HS_m1` | Y^HS_{t−1} | u.m. par pas | `nominal` | `finances_publiques` | 7 (E12) | Y^HS_0/Γ̄ (`sec:finances_publiques-assiette`, `\limites`) ; clé `Y_HS_m1` d'`ouverture()` du script (`outils/etat_stationnaire.py:563`) | finitude seule, déclarée (T^cou et l'érosion des dépôts admettent Y^HS < 0) |

   - **Nom** : suffixe `_m1` (P127, règle de Q1 (ii)) : la variable retient une grandeur du pas, Y^HS_t, que l'ouverture du pas suivant lit sous Y^HS_{t−1}.
   - **Ordre** (H1.5) : module nouveau `nations.etat.finances_publiques`, dernier radical, après `banque_centrale` (ordre des radicaux, `phases.py:38`).
   - **Version** (D2) : **`VERSION_SCHEMA` = 5** dès le premier commit de #132 qui modifie le schéma, sans incrément pendant la branche (précédents de J3-c et J3-d1). Journal : « 5 (15/11/2026, #132 ; ADR 0013, annotation du 15/11/2026 (J3-d2)) : Y^HS_{t−1} ». **Une sauvegarde v4 est refusée** (D4) ; test à l'image de celui de #60.
   - L'écriture en phase 7 tient C2 (une écriture par pas, du propriétaire, dans une phase où il siège après toutes ses entrées) ; le contrôle d'écriture unique du moteur s'applique tel quel.
3. **ς_B dans `DOMAINES_DES_ENTREES`** (engagement 5 ; P138 ; **contrat partagé étendu**, liste fermée B5 et G4, extension annoncée au point 1 de l'annotation du rang 8 de J3-d1 et dans la docstring de `DeclarationDesEntrees`, `ordonnanceur.py:217-221`). Constat : la liste ne contient que `varsigma_L` (`ordonnanceur.py:203-207`). Entrée `varsigma_B`, même prédicat `_part_dans_l_intervalle_unite` : part dans **[0 ; 1] fermé**, finie ; refus par **`EntreeHorsDomaine`** en phase 0 (`ordonnanceur.py:252-256`), avant le refus générique de finitude ; jamais d'écrêtage ; colonne « Lisent » de `tab:phases` inchangée pour la phase 0. ς_B est déclarée dans `DeclarationDesEntrees.scenario` par l'assemblage du socle complet. **Sous Em < 0** (rachat), ς_B s'applique sous la même forme, (1 − ς_B)(Em − θ_CB Em), sans cas particulier ni second domaine (P159) ; la forme est déclarée en `\limites` de E11 par `docwriter` (rang 6), et les bornes du critère 16 (B_CB + θ_CB Em ≥ 0, B_Bk + ΔB^prim_Bk ≥ 0) se vérifient par appel direct.
4. **Lectures de M^G, liste fermée des lectures brutes** (engagements 2 à 4 ; points 5 des annotations de J3-d1 et du rang 8 ; **aucune extension** : la liste est réaffirmée telle quelle, son contrôle devient un test). Lectures **brutes** admises, et elles seules : **E^Bk** (bloc 7, D_H et D_F, P107) ; **E6** (M^G dans le plafond des transferts, sous le max(0 ; ·) extérieur) ; **E9** (M^G, la poussière est absorbée à l'émission du pas) ; **assiette de E4**, A = B − M^G − E^CB, avec E^CB = B_CB + L^CB − Res − M^G : M^G **s'annule algébriquement**, A = B_H + B_Bk + Res − L^CB ; la lecture brute ne fait que garder l'identité avec le canal rentier (ligne 15) et la poussière n'atteint A qu'à k·ε·S (critère F5) ; dans `tests/`, l'assiette de X4, qui est celle de E4. **Lecture nette partout ailleurs** dans le bloc 9 : E1 lit max(0 ; M^G) ; E5 lit D̃_F ; E12 lit D̃_H (correction prospective du 15/11/2026, `4b8ce65`) ; E13 lit max(0 ; M^{G,8a}). Chaque exception est déclarée au site de lecture par un commentaire qui cite ce point ; un test énumère les lectures brutes du bloc et refuse toute autre (engagement 2). **Localité** : les max(0 ; ·) sont appliqués dans les fonctions balisées du bloc 9, aucun dans ses méthodes de phase (règle que #142 rétablira pour les blocs 5 et 6).
5. **Un seul calcul du besoin d'émission par pas** (rattaché à #132, `docs/feuille-de-route.md` § 1 ; critère de #132 ; **aucun contrat partagé**). Le bloc réel siège une fois en phase 7, seul écrivain : sa méthode de phase calcule E8 et E9 **une fois** et propose les trois lignes 19a (E10, E11) à partir du même Em_t, sans attribut d'instance ni variable d'état (`assembler` refuse déjà l'attribut d'instance). Le double appel du bloc d'essai (`tests/invariants/socle_partiel.py:779`, `:791`), qui ne pouvait garder Em sans état caché, n'est pas repris. Contrôle : test de décompte des appels de la fonction balisée E9 par pas.
6. **Bloc d'essai 9 gardé sous X1 à X4** (P114, #133 ; P124 ; H6 ; **aucun contrat de `src/`**). Il reste dans `tests/invariants/socle_partiel.py` pour deux bancs, aux verdicts **identiques au bit** : le banc de P87 (blocs d'essai 8 et 9) et celui de J3-d1 (blocs 2 à 8 réels, bloc d'essai 9, couverture X4, `GRANDEURS_NULLES_DE_J3D1`). Il est **retiré du banc du socle complet** (blocs 2 à 9 réels, aucun bloc d'essai). Ses exigences E1 à E3 sont renommées **X1 à X3** au rang 2 (#133, avant #132) ; X4 garde son nom. `couverture_x4()` et `emission_e3()` (nom fixé par #133) sur un bloc 9 réel restent refusées par `OptionSansBlocDEssai` (`socle_partiel.py:453`).
7. **F3 lit la colonne des entreprises** (engagement 6 ; **aucun contrat partagé**). Constat : F3 lit les lignes 18, 1, 2 et 5 par `montant_execute_ligne` (`src/nations/blocs/investissement.py:268-271`), alors que la phase 9 lit déjà la ligne 7 par `montant_execute("7", "entreprises_courant")` (`:277`). F3 lira chaque ligne par `montant_execute(ligne, "entreprises_courant")`, interface existante (`Vue.montant_execute`, `ordonnanceur.py:368`), contrôlée par la même déclaration `Lecture(GRAND_LIVRE, ligne)` : **la déclaration du bloc 6 ne change pas**. La cellule est **signée** (+ pour un terme crédité à la colonne, − pour un terme débité ; `grand_livre.py:714-721`) : F3 en prend l'opposé pour une sortie, sur le précédent d'`impot_retenu`. Trajectoires identiques au bit tant que chaque ligne n'a qu'un terme des entreprises (l'opposé d'un flottant est exact).

8. **Table de paramètres `finances_publiques`** (P165, décision de forme de la session sous la délégation P153, **confirmée par le mainteneur le 15/11/2026**, comme P138 en J3-d1 ; **contrat partagé étendu**, F1 et H3.5, dans la forme de la table `menages` de J3-d1, point 2, et des tables `banque` et `banque_centrale` de J3-c). Constat : `EnsembleDesParametres` compte huit champs, de `cadre` à `banque_centrale` (`src/nations/moteur/parametres/ensemble.py:53-60`), sans table du bloc 9. Elle reçoit le champ `finances_publiques`, après `banque_centrale`, et porte ν_G, U^eq et les **valeurs à levier fermé** de θ_G, θ_Tr, τ_H, τ_F et φ.
   - **Leviers au J3** : ce sont des paramètres de la table, sur le précédent de π\* (BC4). Leur passage en commandes du joueur relève du J4 (G4), **sans drapeau de mode**.
   - **Conditions jointes** de `sec:finances_publiques-conditions` contrôlées au chargement de la table : dans `__post_init__`, sur le précédent de 0 < ν_H λ_H < 1 pour `menages`.

**Arrêt du § 1** (« contrat partagé à modifier au-delà de l'annotation du rang 1b ») : **non déclenché** par les sept points. Deux contrats partagés sont étendus, dans la forme déjà pratiquée par annotation : le schéma (point 2, v5) et la liste `DOMAINES_DES_ENTREES` (point 3). Le point 8 (P165) étend F1 et H3.5 dans la même forme.

**Effet sur les résultats** : aucun par l'annotation. Engagement 6, #133 et le bloc d'essai gardé : trajectoires identiques au bit. Le bloc 9 réel produit les premiers résultats du socle complet (rang 5), sans résultat final.

**Surface documentaire** (rang 6, `docwriter`) : variable d'état Y^HS et schéma v5 (`sec:finances_publiques-phases`, chapitre du moteur) ; ς_B dans la liste des domaines des entrées (`sec:cadre-phases`) ; `\limites` de E11 sous Em < 0 (P159) ; liste fermée des lectures brutes (`sec:cadre-caisse`).

Issues : #132, #133 ; renvois : #106, #142, `docs/feuille-de-route.md` § 1 et § 4 (P114, P124, P127, P138, P154, P159, P164).

### Annotation du 15/11/2026 (rang 8 de J3-d2, consignation) : retrait de `variation_sur_le_tour`, `emission_x3()`, F3 et la ligne 18, erratum de transcription de P165

Rédigée par `architect` (Opus, sans Fable) au rang 8 de J3-d2 (PR #146, tête `f1c8f2f`). **Aucune décision nouvelle** ; l'état consolidé (Contexte à Conséquences) et les annotations antérieures restent tels quels et se lisent avec les points ci-dessous. Conformément à P76, l'ADR 0012 n'est pas annoté : ses mentions visées au point 1 (l. 149 et 432) se lisent par le présent point.

1. **`variation_sur_le_tour` retirée** (#106, P51 ; code `380a325`, spécification `b5ea86b`). Aucun bloc ne déclarant la lecture à la fin du rang 3, elle sort de `LECTURES_DU_REGISTRE` et de `nations.moteur.registre`. Se lisent sans elle : F3 de l'ADR 0012 (l. 149) et de la présente consolidation (l. 96) — fonctions qui indexent le registre : `dernier_prix`, `glissement`, `avancer` ; la liste des lectures de l'ADR 0012 (l. 432) et H1 de la présente consolidation (l. 165), réduites à `vue.dernier_prix()` et `vue.glissement()`. `pas_du_tour` et `tour_du_pas` (`nations.moteur.calendrier`) sont conservées. Concordance : **90 labels** (aucun `eq:moteur-variation-tour`).
2. **`emission_e3()` renommée `emission_x3()`** (#133, `8352db8` ; `tests/invariants/socle_partiel.py:835`). Les mentions d'`emission_e3()` de l'annotation du rang 1b de J3-d1 (couverture X4, « Place » et « Composition ») et du point 6 de l'annotation du rang 1b de J3-d2 se lisent `emission_x3()`.
3. **Point 7 de l'annotation du rang 1b de J3-d2, tel qu'exécuté** : F3 lit chaque ligne à la colonne des entreprises, mais la **ligne 18** (crédit) se lit dans la colonne `entreprises_capital`, les lignes 1, 2, 5 et 7 dans `entreprises_courant` (`src/nations/blocs/investissement.py:281-290`). Trajectoires identiques au bit (critère de l'engagement 6, tenu).
4. **Erratum de transcription de P165** (point 8 de l'annotation du rang 1b de J3-d2 ; décision inchangée) : (a) U^eq **n'est pas** dans la table `finances_publiques` ; sa seule maison reste la table du travail (H3.3 ; spécification, `sec:finances_publiques-depense`, « paramètre du bloc travail ») ; r̄ reste dans la table de la banque centrale ; (b) `sec:finances_publiques-conditions` ne déclare aucune condition jointe entre champs de la table : `__post_init__` n'appelle que `valider_table`, les conditions de l'état stationnaire étant refusées par le script. Le code est conforme à la spécification (`src/nations/moteur/parametres/finances_publiques.py:23-32`). Même erratum dans `docs/feuille-de-route.md` § 4.

**Effet sur les résultats** : aucun.

Issues : #106, #132, #133 ; renvois : `docs/feuille-de-route.md` § 1 et § 4 (P51, P76, P165).

### Annotation du 16/11/2026 (rang 1b de la branche « forme du code ») : domaine contrôlé une fois, conversions partagées publiées, retrait de `g`, E7 en variables du pas, lectures de position filtrées, refus avec étape et bloc

Rédigée par `architect` (Opus, sans Fable) au rang 1b de la branche « forme du code » (`claude/j3-forme-du-code`, PR #151, tête `0d35718`), sous P172 à P187 (`docs/feuille-de-route.md` § 1 et § 4) et la délégation P175, **avant le code de #137, #144 et #150**. Elle fixe la forme des contrats partagés touchés (`docs/agents/routage.md` § 4.2) ; le point 5 rouvre a100.4 pour les seules positions (question Q-1b-1). Aucune équation ni coefficient ne change. Constats faits à `0d35718`.

1. **Domaine d'une variable d'état de bloc contrôlé une fois par pas** (#144, point 1 ; D1, B2, B5). Constat : `Vue.ecrire_etat` appelle `schema.defaut_de_domaine` (`ordonnanceur.py:471-474`), puis `schema.EtatPays(**champs)` (`:960`) le rappelle pour les mêmes valeurs (`schema.py:334`).
   - **Lieu retenu : l'écriture.** `Vue.ecrire_etat` reste le seul contrôle de domaine des variables d'état des blocs : le refus nomme le pas, l'étape et le bloc, et aucune valeur hors domaine n'est lisible sous `<nom>_suivant` dans la suite du pas. Une valeur non finie reste refusée par l'espace du pas.
   - **Construction de clôture** : une fonction de `nations.etat.schema`, `etat_de_cloture`, construit l'`EtatPays` du pas suivant. Elle contrôle le type de tous les champs et le domaine des autres champs (identité, `t`, registre, positions, V^flux), par `defaut_de_domaine`, seule fonction de domaine ; elle ne contrôle pas une seconde fois le domaine des variables d'état des blocs. Trois conditions : `executer_pas` en est le seul appelant dans `src/` ; `Vue.ecrire_etat` est le seul site qui remplit `_Pas.etat_suivant`, après le contrôle ; ni argument, ni champ, ni valeur par défaut ne module `EtatPays.__post_init__`. Les deux premières sont tenues par des tests textuels. Le mécanisme de construction est laissé à `coder`.
   - **Inchangé** : construction de l'état initial, `dataclasses.replace` et reprise (D4, hors chemin chaud), qui contrôlent tous les domaines. **D1 se lit** : « appelée à toute construction (état initial, reprise ; à la clôture du pas, pour les champs autres que les variables d'état des blocs, dont le domaine est contrôlé à l'écriture, une fois par pas) ».
   - **Garantie** : aucun `EtatPays` hors domaine. La valeur d'une variable d'état de bloc ne vient que de `etat_suivant`, qui ne reçoit qu'une valeur contrôlée, et le moteur refuse une variable non écrite (`ordonnanceur.py:955-958`).
   - **Test de décompte** : sur un pas du socle complet, `defaut_de_domaine` est appelée une fois par variable d'état de bloc. Une valeur hors domaine d'un champ du moteur passée à `etat_de_cloture` reste refusée.
   - **Options écartées** : (b) contrôle à la seule construction de clôture : refus tardif, sans l'étape ni le bloc, après des lectures de `<nom>_suivant` hors domaine (exception non typée possible) ; (c) argument ou `InitVar` qui désactive le contrôle dans `EtatPays` : drapeau de mode.
2. **Conversions partagées publiées une fois par pas, en grandeurs d'ouverture** (#144, point 2 ; C3, F2, H4).
   - **Règle** : la conversion d'un paramètre, invariante pendant une partie, devient une grandeur d'ouverture (C3) si plus d'un siège la lit (bloc × étape, `_facteur_g` du moteur compris) ou si elle combine les tables de plusieurs blocs (précédent de `facteur_g`, H4). Lue par un seul siège, elle reste au site, calculée une fois par pas. C'est le cas de 1/κ (production, phase 4) et des vitesses λ.
   - **Grandeurs ajoutées**, à la suite de `date_de_decision` :
     - `facteur_g_pr` = f(g_pr) : production (5), travail (1), `facteur_g` ;
     - `facteur_g_N` = f(g_N) : travail (4), `facteur_g` ;
     - `facteur_g` = `facteur_g_pr` · `facteur_g_N`, même produit dans le même ordre, donc identique au bit ;
     - `delta_pas` = `par_pas(δ)` : production (5), investissement (3 et 6), finances publiques (6).
   - **Forme des grandeurs ajoutées** : label renvoi (`eq:moteur-conversion-croissance` ou `eq:moteur-conversion-taux`), non balise. Unité « sans dimension » (P96). Lecture par `Lecture("0", …)`.
   - **Reconstruction refusée dans un bloc** : contrôle statique de `par_pas` ou `facteur_par_pas` appliqué à `delta`, `g_pr` ou `g_N` (modèle de Γ^e, annotation du rang 9 de J3-c, point 3). Le test « conversion unique » n'a aucune exemption nouvelle.
   - **Options écartées** :
     - (b) champ dérivé des tables de paramètres (F) : forme nouvelle du contrat des tables. `valider_table`, `varier` et les tests qui parcourent les champs devraient exclure des champs non déclarés (H3.5). Écartée pour une économie de quelques divisions par pas ;
     - (c) toutes les conversions de paramètres en grandeurs : perte de localité, puisque les vitesses propres à un bloc passeraient au moteur.
3. **`g` retirée** (#144, point 3 ; C3, H4 ; règle de P51, retrait faute de lecteur déclaré). Constat : aucun `Lecture("0", "g")` dans `src/`, `tests/` ni `outils/`, et `_facteur_g` ne lit plus g depuis P88. Le risque d'un futur lecteur qui recombinerait g et divergerait au bit de `facteur_g` (P88) disparaît avec la grandeur.
   - g reste une **notation** de la spécification (définie au `sec:production-visee`), sans label.
   - **Écart attendu au banc d'empreintes** : code 3, par le retrait de g et l'ajout des trois grandeurs du point 2 (P186 ; question Q-1b-2). L'écart est déclaré dans le commit.
4. **E7 calculé une fois par pas, en variables du pas** (#150, point 1 ; tableau du bloc 9 de l'annotation du rang 1b de J3-d2, point 1 ; P187).
   - **Écriture** : `phase_2` écrit `iB_BH`, `iB_BBk` et `iB_BCB`, les trois termes de E7. Ce sont les noms des termes des lignes 11a à 11c (« une valeur, un nom »). Le domaine se réduit à la finitude seule : le taux i_CB peut être négatif.
   - **Lecture** : `phase_6` lit ces trois variables (`Lecture("2", …)`) et les propose. Le siège 6 ne lit plus i_CB ni B_H, B_Bk, B_CB.
   - **Contrôle** : la somme de E6 reste formée en phase 2 sur les mêmes valeurs. Un test de décompte vérifie un appel de `interets_sur_titres` par pas.
   - **`tab:phases` inchangé** : le bloc 9 écrit déjà en phase 2, et la colonne « Lisent » de la phase 6 contient 2 (B1).
   - **`tab:finances_publiques-phases` change** : la phase 2 écrit les trois termes, la phase 6 les lit dans « ses calculs de la phase 2 » et ne lit plus la phase 1. Le lien exact de P170 (`test_tab_finances_publiques_phases_porte_chaque_ecriture`) échoue donc entre le commit `code:` et le passage de `docwriter`. Il est marqué en échec attendu strict, avec renvoi à #150, et la marque est retirée par un commit `tests:` qui suit immédiatement le commit `docs:` (précédent de `G_vise` et `T_F`, `f1c8f2f`).
   - **Critère** : jugé sur `etats` et `montants` et sur les variables du pas préexistantes (P187).
5. **Lecture d'une position filtrée à l'exécution** (#150, point 2 ; B2, B3, B5 ; **rouvre a100.4 pour les positions**).
   - **Constat mesuré** : H5 refuse déjà, dans `src/nations/blocs/`, une position lue sans déclaration dans son siège. Une copie de `finances_publiques.py` qui lit `B` au lieu de `M_G` en 8b donne deux écarts (« 'B' faite, non déclarée », « 'M_G' déclarée, jamais faite »). Le trou porte sur l'exécution (`LectureDuGrandLivre.position`, `ordonnanceur.py:382-383`) et sur les blocs hors de H5 (blocs d'essai, H6).
   - **Forme** : les droits du siège retiennent les postes déclarés (`Lecture(GRAND_LIVRE, poste)`, poste de `NOMS_POSTES`). `position` refuse un poste non déclaré par `RefusDuMoteur` qui nomme le pas, l'étape, le bloc et le poste, comme `_verifier_ligne`.
   - **À l'assemblage** : le contrôle est inchangé (position admise sans triangularité ni colonne « Lisent »). « Toujours admise » (`contrat_bloc.py:28`) se lit « admise à l'assemblage, lue seulement si déclarée ».
   - **Liste fermée, tenue par un test** : (`banque`, 8c, `Res`) et (`finances_publiques`, 8b, `M_G`).
   - **Inchangé** : ouverture, échelles et valeurs nettes restent non filtrées à l'exécution (H5.3 les refuse).
   - **Motif de la réouverture** : même garantie à l'exécution que les montants exécutés (a100.1 à a100.3), pour les blocs d'essai ; coût d'une recherche dans un ensemble par lecture, deux par pas.
   - **Option écartée** : maintien de a100.4, avec la docstring corrigée et un test de texte fabriqué sous H5. C'est la recommandation de repli de Q-1b-1.
6. **#137 et #142** (B4 ; aucun contrat partagé).
   - **#137** : `VariablesDuPas.ecrire(nom, valeur, *, etape, bloc)`, étape et bloc obligatoires, sans valeur par défaut. Les quatre refus génériques les portent. Le moteur passe (« 0 », `moteur`) pour les grandeurs et les entrées, (« 1 », `moteur`) pour les leviers. `Vue.ecrire_etat` passe son étape et son bloc pour `<nom>_suivant`.
   - **Interface des refus typés inchangée** : `ArretMoteur` a déjà les champs. Le refus de lecture avant écriture est hors de #137. B4 se lit : « chaque refus d'écriture nomme le pas, l'étape et le bloc écrivain ».
   - **#142** : fonctions des blocs 5 et 6 seulement, sans importateur hors de `tests/` (`grep` de `nations.blocs` dans `src/` et `outils/` : vide). Balises inchangées.

**Décomptes attendus** :
- grandeurs d'ouverture : **8 → 10**, dans l'ordre `annee`, `mois`, `date_de_decision`, `facteur_g_pr`, `facteur_g_N`, `facteur_g`, `delta_pas`, `pi_etoile_pas`, `Gamma_e`, `gamma_e` ;
- variables du pas du bloc 9 en phase 2 : six → neuf ;
- schéma inchangé (v5, 38 variables) ;
- concordance inchangée (**90 labels**, aucune balise nouvelle) ;
- `tab:phases` inchangé.

**Arrêt du § 1** (« contrat partagé à modifier au-delà de l'annotation du rang 1b ») : non déclenché si le code suit les points 1 à 6.

**Effet sur les résultats** : aucun sur `etats` et `montants`. Les grandeurs d'ouverture (points 2 et 3) et les variables du pas (point 4) changent, avec un écart déclaré.

**Surface documentaire** (rang 7, `docwriter`) :
- `sec:cadre-calendrier` : décompte « huit » des grandeurs, phrase « g reste publiée », grandeurs ajoutées, `facteur_g` ;
- encadré de `eq:moteur-croissance-nominale-attendue` : « facteur_g qui fait croître… dans leurs blocs » ;
- paragraphe « Ordonnanceur » : liste des grandeurs ;
- lectures des tableaux de phases des blocs 2, 3, 6 et 9 : δ, g_pr, g_N lus en phase 0 ;
- `tab:finances_publiques-phases` (point 4) et phase de E7 dans le récapitulatif du bloc 9 ;
- textes du contrôle de domaine et des lectures de position (`sec:cadre-phases`) ;
- journal des changements.

**Questions au mainteneur, décidées le 16/11/2026** :
- **Q-1b-1** : réouverture de a100.4 confirmée pour les seules lectures de position, au point 5 (P188).
- **Q-1b-2** : le code 3 de P186 couvre l'ajout de grandeurs d'ouverture comme le retrait de g (P189).

Issues : #137, #142, #144, #150 ; renvois : `docs/feuille-de-route.md` § 1 et § 4 (P51, P88, P170, P175, P186, P187), #125.
