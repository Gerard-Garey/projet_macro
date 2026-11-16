---
bloc: calibration du socle (fiche transverse T1)
module: transverse : valeurs et sources des tables de src/nations/moteur/parametres/ ; défauts d'outils/etat_stationnaire.py
expert pilote: macro (#92, #55, #62, #45) | monnaie (#130 ; #143 avec macro)
experts consultés: monnaie (#55, #45) ; macro (#130) ; jeu
statut: en instruction
décision: M34 (réservée au rang 2, P206) | —
issue: #92, #55, #130, #62, #45 ; #143 (instruction, sans Closes)
---

# Fiche transverse — calibration du socle

Fiche transverse de la branche « calibration » (PR #162 ; P205). Une section par issue, dans l'ordre du plan (`docs/feuille-de-route.md` § 1) : #92, #143, #55, #130, #62, #45. Chaque section donne la définition empirique, les sources lues ou « non trouvée » (P208), la valeur proposée et ses variantes, le tableau avant / après **prédit** par `outils/etat_stationnaire.py` à π̄ = 0, 2 et 10 %, et les conditions d'existence. La décision porte sur la table calibrée entière (M34, rang 2, P206). Les agents n'écrivent pas la fiche dans le dépôt : la session y verse leur compte rendu.

## 1. #92 — Marge normale μ̄ (bloc 4, prix) : part salariale

*Instruite par `macro` (expert pilote) le 16/11/2026, rang 1 de la branche « calibration » (PR #162, tête `0ab2cda`). Les chiffres du modèle viennent du script d'état stationnaire **non modifié**, appelé à μ̄ surchargé (méthode au § 4.1). Ce sont des résultats du modèle, pas des faits. Les faits portent leur source et leur date. Chaque conclusion est marquée **vérifiée**, **hypothèse** ou **non vérifiée**.*

### 1. Grandeur visée et correspondance avec le modèle

**Grandeur du modèle (critère propre de #92).** La part salariale ΣWB/ΣVA est une fraction. Sa valeur ajoutée vaut p v + ΔIN, égale au PIB nominal dans une économie fermée, sans consommation intermédiaire. Elle se mesure sur 12 tours, à π̄ = 2 %, n_a = 12 et ν_G = 1,15. C'est la ligne « Part salariale » de `tab:etat-stationnaire` et la ligne B4 de `tab:criteres-j3`.

**Relation entre μ̄ et ΣWB/ΣVA dans le modèle.** Forme fermée de `sec:travail-stationnaire` :

ΣWB/ΣVA = (y/v) / [(1 + μ̄) + γ̄ ρ̄_IN n_a σ], avec γ̄ = Γ̄ − 1.

À π̄ = 2 %, n_a = 12, le script donne y/v = 1,0023122138, γ̄ = 0,0033058903, ρ̄_IN = 0,9960571465 et n_a σ = 1,4. La part vaut donc presque exactement 1/(1 + μ̄). L'écart à ω̄ = 1/(1 + μ̄) vient de la variation des stocks, valorisée au coût, dans la valeur ajoutée. **Vérifiée** : pour trois parts visées, la valeur de μ̄ tirée de la forme fermée égale à 1e−10 près celle qu'une bissection donne sur l'état complet du script (sortie au § 4.2). Aucune vitesse n'entre dans cette relation.

**Les cinq traits du concept du modèle, que la définition empirique doit respecter :**

| Trait | Dans le modèle (vérifié sur `etat_stationnaire`, l. 432 à 452) | Conséquence pour la source |
|---|---|---|
| Revenu mixte | Aucun travailleur indépendant : tout l'emploi N est salarié, payé W | La rémunération des salariés doit être **corrigée de l'emploi non salarié**. La série non corrigée sous-estime la part du travail. |
| Brute ou nette | Le PIB contient l'investissement brut. L'amortissement δK/n_a est une charge payée sur la marge. | La valeur ajoutée doit être **brute**. |
| Impôts sur la production | Il n'y en a aucun. τ_F porte sur le profit (E5) et vaut 0 au socle. La valeur ajoutée est donc au coût des facteurs. | Mieux vaut un dénominateur **au coût des facteurs**. Au prix de base, il inclut les autres impôts nets sur la production (D.29 − D.39). L'écart est déclaré au § 2. |
| Secteur | Les entreprises produisent toute la valeur ajoutée, y compris les biens achetés par l'État. L'État n'emploie personne. La banque n'a pas de valeur ajoutée. | Prendre l'**économie totale**. Le secteur des sociétés non financières ne contient pas la production des services publics, que le modèle fait produire par les entreprises. |
| Logement | Les ménages ne détiennent pas de logement ; il n'y a pas de loyers imputés. | Limite déclarée : l'excédent des loyers imputés pèse dans le dénominateur observé, et le modèle ne l'a pas. |

### 2. Sources lues et citées

**Source retenue (lue).** K. Bodnár et M. Mohr, « The development of the wage share in the euro area since the start of the pandemic », Banque centrale européenne, *Economic Bulletin*, numéro 4/2023, encadré, page web <https://www.ecb.europa.eu/pub/economic-bulletin/focus/2023/html/ecb.ebbox202304_04~0dee9ead8e.en.html>. Consultée le 16/11/2026 par WebFetch.
- **Définition** (note 1 de l'encadré) : rémunération totale des salariés, corrigée de la part des indépendants, à qui l'on impute le revenu moyen par personne des salariés de leur secteur. Le dénominateur est la valeur ajoutée brute nominale, égale au PIB au prix de base, c'est-à-dire la somme des revenus des facteurs, de la consommation de capital fixe et des autres impôts nets de subventions sur la production. Le champ couvre toutes les branches NACE, services publics compris.
- **Zone et fréquence** : zone euro, données trimestrielles, dernière observation T1 2023.
- **Sources de l'encadré** : Eurostat, Euro Area Business Cycle Network (EABCN), calculs de la BCE.
- **Valeur** : note du graphique A, citation courte rendue par l'outil, « The long-term average wage share calculated over the period 1998-2023 is 62.4% ». Le texte précise que la part était un peu au-dessus de 62 % fin 2019, proche de cette moyenne. Elle est passée au-dessus de 65 % au T2 2020, puis à un peu plus de 61 % au T4 2022.
- **Page** : sans objet, c'est une page web. Repère : note du graphique A et note 1.
- **Statut** : fait établi, **vérifié**, avec deux réserves. L'outil de lecture ne restitue qu'une citation courte et un résumé, et je n'ai pas vu le graphique lui-même.

**Sources lues, sans niveau utilisable :**
- N. Battistini, H. Grapow, E. Hahn et M. Soudan, « Wage share dynamics and second-round effects on inflation after energy price surges in the 1970s and today », BCE, *Economic Bulletin*, numéro 5/2022, encadré. Consulté le 16/11/2026. Il définit la part salariale comme la rémunération corrigée par le rapport des personnes employées aux salariés, rapportée au PIB nominal, et ne donne aucun niveau.
- C. Bates, K. Bodnár, V. Botelho et F. Rousseau, « Real wage catch-up in the euro area », BCE, *Economic Bulletin*, numéro 5/2025. Consulté le 16/11/2026. Il ne traite pas de la part salariale.

**Sources inaccessibles dans cette session, non lues** (P208 : aucun chiffre n'en est tiré) :
- AMECO, série ALCD2 : part salariale corrigée, économie totale, en % du PIB au coût des facteurs. C'est le dénominateur le plus proche du modèle. Le téléchargement direct (`ec.europa.eu`) a été refusé par le proxy (CONNECT 403). Le miroir DBnomics (`db.nomics.world`) et Eurostat (`ec.europa.eu`) ne se résolvent pas par WebFetch. Une recherche web en a rendu un résumé, non vérifié et à ne pas citer : moyenne de 63,2 % pour la zone euro (EA20) de 1995 à 2023.
- Part salariale des sociétés non financières (Eurostat, comptes de secteur) : non lue, pour la même raison.
- OCDE (*Compendium of Productivity Indicators*), OIT et Penn World Table : non consultés. La consigne de l'outil demande de cesser d'essayer d'autres hôtes après deux refus.
- Pour lire ALCD2, il faut autoriser `ec.europa.eu` ou `db.nomics.world` dans les réglages réseau de la session.

**Pas une source.** La valeur de 0,52 « Penn World Table, extrait » de la fiche 3 (`docs/blocs/travail.md`, l. 497) vient de la première tentative et n'a pas été relue. Elle ne sert pas.

**Écart de définition déclaré (contesté).** La source rapporte la rémunération au PIB **au prix de base**, alors que le modèle est **au coût des facteurs**. Au coût des facteurs, la part observée serait plus haute, puisque le dénominateur ôte les autres impôts nets sur la production. L'ampleur n'est **pas vérifiée**, faute de source lue sur D.29 − D.39. Le résumé non vérifié d'ALCD2 laisse supposer un écart inférieur à un point. **Hypothèse.**

### 3. Valeur proposée et variantes

**Proposée : μ̄ = 0,60.** Le modèle donne ΣWB/ΣVA = 0,624645 à π̄ = 2 % (0,625541 à 0 %, 0,621303 à 10 %). L'écart à la source (62,4 %) est de +0,06 point, dans la tolérance d'un point du critère de #92. **Vérifiée.**

**Motif.** La valeur ronde ne prétend pas à plus de précision que la source, qui donne une décimale. La marge se lit simplement : « prix égal à 1,6 fois le coût salarial unitaire ». C'est une marge sur le **coût salarial unitaire**, la seule charge courante du prix (option M, M26). Elle doit couvrir l'amortissement, les intérêts, les profits non distribués et les dividendes. Elle ne se compare pas aux marges sur le coût marginal de la littérature d'organisation industrielle, que je n'ai pas lue ici.

| Variante | μ̄ | Part à 0 / 2 / 10 % | Motif | Avis |
|---|---|---|---|---|
| V0, statu quo | 0,25 | 0,80037 / 0,79890 / 0,79344 | Hypothèse de l'instruction, sans source | Écartée : 17,5 points au-dessus de la source, critère de #92 non tenu |
| **V1, proposée** | **0,60** | **0,62554 / 0,62465 / 0,62130** | Source de la BCE, arrondie | **Recommandée** |
| V2, part exacte | 0,6016595755 | 0,624894 / 0,624000 / 0,620665 | Égalité exacte à 62,4 % à π̄ = 2 % | Précision illusoire ; ne change aucun verdict |
| V3a, bord haut | 0,5763240932 | 0,634923 / 0,634000 / 0,630557 | Part de la source + 1 point. C'est l'ordre de grandeur d'une lecture au coût des facteurs (hypothèse, § 2). | Variante si le mainteneur exige le coût des facteurs sans source lue |
| V3b, bord bas | 0,6278203177 | 0,614865 / 0,614000 / 0,610771 | Part de la source − 1 point | Bornes du critère |

**Domaine admissible de μ̄ dans le modèle** (mesuré à x = 2, Δϱ = 0, ν_G = 1,15) :

| Condition | π̄ = 0 | 2 % | 10 % |
|---|---|---|---|
| Div_F = 0 en dessous de μ̄ = | 0,1812 | 0,1789 | 0,1759 |
| Distribution = 0,2 (borne basse de #55) en dessous de μ̄ = | 0,1914 | 0,1956 | 0,2073 |
| Distribution = 0,9 (borne haute de #55) au-dessus de μ̄ = | **0,6931** (part 0,5912) | 1,2873 | jamais pour μ̄ ≤ 3 (distribution 0,8811 à μ̄ = 3) |

À π̄ = 0, μ̄ = 0,60 est donc à 0,093 de la borne haute de la distribution. Une source plus basse que 59,1 % ne serait pas compatible avec la bande de #55 à écarts et ζ actuels. **Vérifiée.**

### 4. Tableau avant / après prédit (μ̄ = 0,25 → 0,60)

#### 4.1 Méthode et commandes

Le script n'a pas d'option pour surcharger μ̄. Pour ne modifier aucun fichier du dépôt, une sonde du scratchpad importe `outils/etat_stationnaire.py` par son chemin, sans le modifier, puis appelle la fonction publique `calculer(replace(Parametres(), mu_bar=x))`. C'est la fonction qu'appelle `main`, avec les mêmes autres défauts.

Commandes, lancées depuis `/home/user/projet_macro` à `0ab2cda` :
- `uv run python outils/etat_stationnaire.py` → code 0. Sortie de référence : 449 valeurs publiées, toutes « égal ».
- `uv run python -I <scratchpad>/outils_mu/mu92.py 0.25 0.60` (`<scratchpad>` : dossier temporaire de la session, non versé ; la mesure se reproduit par l'appel ci-dessus, et par le script lui-même une fois le défaut changé au rang 3) → à μ̄ = 0,25, plus grand résidu 4,636e−15, 449 valeurs « égal » sur 449 ; à μ̄ = 0,6, plus grand résidu 4,792e−15 ≤ 1e−12, aucun refus de domaine, 173 valeurs publiées en écart sur 449, point de référence ν_G = 1 publié aux trois π̄.
- Sondes `mu92b.py` (μ̄ pour une part visée, seuils), `mu92c.py` (niveaux invariants), `mu92e.py` (n_a = 4, superneutralité), `mu92f.py` (dépendance à n_a), `mu92g.py` (décomposition de la valeur ajoutée), même dossier. Sorties intégrales : `<scratchpad>/sortie_mu_025_060_precis.txt`, `sortie_mu_variantes.txt` et `sortie_mu92b.txt`.

#### 4.2 Une seule cause pour tous les ratios agrégés (vérifiée)

μ̄ ne fait que déplacer le revenu des entreprises entre salaires et dividendes. Mesure `mu92c.py`, de μ̄ = 0,25 à μ̄ = 0,60, aux trois π̄ :
- ΔDiv_F = −ΔWB, à 6e−17 près.
- Le revenu des ménages ne bouge pas : WB + Div_F = p v − δK/n_a − (i_L L − i_D D_F)/n_a − γ̄ (K + D_F − L). Le terme ΔIN du profit se compense avec la part γ̄ IN des profits non distribués.
- D_H, YD, C, G, I, L, D_F, B, M^G, T_H, Π^Bk, Div_Bk et K ont des niveaux inchangés, à 6e−16 près en relatif.
- Seuls changent WB, Div_F, le stock IN (valorisé au coût UC), V_F, ΔIN, FU et le PIB.

Le PIB baisse d'un facteur 1/1,000404, 1/1,000804 et 1/1,002298 à π̄ = 0, 2 et 10 %. Chaque ratio au PIB ci-dessous monte exactement de ce facteur.

L'explication commune est notée **(P)** : dénominateur PIB plus petit, parce que la variation des stocks est valorisée à un coût unitaire plus bas, UC = p/(1 + μ̄).

#### 4.3 `tab:etat-stationnaire` (n_a = 12, ν_G = 1,15)

| Grandeur | Avant 0 / 2 / 10 % | Après 0 / 2 / 10 % | Écart à 2 % | Explication |
|---|---|---|---|---|
| Capital sur production (b), prix courant | 2,0009 / 1,9973 / 1,9836 | 2,0017 / 1,9989 / 1,9882 | +0,0016 | (P) |
| Capital sur production (c), comptable | 2,0009 / 1,5551 / 0,8360 | 2,0017 / 1,5563 / 0,8379 | +0,0012 | (P) |
| Part salariale | 0,80037 / 0,79890 / 0,79344 | 0,62554 / 0,62465 / 0,62130 | −0,17426 | #92 : ω̄ = 1/(1 + μ̄) passe de 0,8 à 0,625 (forme du § 1) |
| Taux d'investissement, % du PIB | 13,970 / 13,945 / 13,849 | 13,976 / 13,956 / 13,881 | +0,011 pt | (P) ; I inchangé |
| Masse monétaire, années de PIB | 0,81917 / 0,81658 / 0,81108 | 0,81950 / 0,81723 / 0,81295 | +0,00065 | (P) ; D_H et D_F inchangés |
| Dette consolidée, années de PIB | 0,09884 / 0,25674 / 0,51013 | 0,09888 / 0,25695 / 0,51130 | +0,00021 | (P) ; B, M^G inchangés |
| Dette brute | 0,11987 / 0,27849 / 0,53645 | 0,11992 / 0,27871 / 0,53769 | +0,00022 | (P) |
| Dette brute, ν_G = 1 | 0,11712 / 0,27564 / 0,53299 | 0,11717 / 0,27587 / 0,53421 | +0,00023 | (P) |
| Dette brute affichée, % | 12,1 / 28,5 / 57,1 | 12,1 / 28,5 / 57,2 | 0,0 (seul 10 % bouge à l'arrondi) | (P) |
| Déficit public (Domar), % du PIB | 0,1959 / 1,0185 / 5,9005 | 0,1960 / 1,0193 / 5,9141 | +0,0008 pt | (P) |
| Solde primaire, % du PIB | −0,0971 / −0,2432 / −0,2381 | −0,0971 / −0,2433 / −0,2386 | −0,0001 pt | (P) ; T_H et G inchangés |

Huit lignes sont **inchangées** à toutes les décimales publiées : capital sur production (a), r̄, taux directeur, taux réel restitué, ϱ_L, inflation, hausse par pas et **θ_G**. θ_G vaut 0,218474 / 0,219573 / 0,219568, à 1e−15 près : G et y^pot sont inchangés.

#### 4.4 Valeurs résolues de `tab:criteres-j3` (π̄ = 2 %) qui changent

| N° | Avant | Après | Explication |
|---|---|---|---|
| B4 part salariale | 0,798903 | **0,624645** | #92 ; la bande ±1 pt reste centrée sur la valeur résolue (M25) |
| B6 marge p/UC − 1 | 0,25 | **0,60** | #92, par définition (μ̃ = ln 1,6 = 0,470004) |
| B12 capital au prix courant | 1,99726 | 1,99887 | (P) |
| B13 taux d'investissement | 13,945 % | 13,956 % | (P) |
| B15 dépôts des entreprises | 0,16605 | 0,16619 | (P) ; D_F inchangé |
| B16 masse monétaire | 0,81658 | 0,81723 | (P) |
| B19 encaisse du Trésor | 0,021748 | 0,021765 | (P) |
| B20 titres de la banque | 0,27849 | 0,27871 | (P) |
| B21 dette consolidée | 0,25674 | 0,25695 | (P) |
| B22 déficit public | 1,0185 % | 1,0193 % | (P) |

Lignes inchangées : B1, B2, B3, B5, B7, B8, B9, B10 (0,980566), B11 (3,8900 %), B14, B17, B18, B24, B25 et B26. Les lignes B10 et B11 rapportent à YD, inchangé ; les autres sont des paramètres ou des taux.

#### 4.5 Autres valeurs publiées (surface de `docwriter`)

173 valeurs publiées sur 449 passent en écart dans le script. Elles se répartissent ainsi :

| Endroit | Valeurs en écart |
|---|---|
| `sec:finances_publiques-stationnaire` | 46 |
| `sec:banque-stationnaire` | 37 |
| `tab:etat-stationnaire` | 30 |
| `sec:investissement-stationnaire` | 28 |
| `sec:banque-restitution` | 6 |
| fiche 9, § 3.C | 6 |
| `sec:travail-stationnaire` | 5 |
| `sec:banque_centrale-restitution` | 5 |
| `sec:prix-stationnaire` | 3 |
| `sec:finances_publiques-restitution` | 3 |
| `sec:banque-conditions` | 1 |
| `sec:finances_publiques-impots` | 1 |
| `sec:finances_publiques-transferts` | 1 |
| fiche 9, § 6.3 | 1 |

Ce sont toutes des valeurs (P) ou de partage. Phrases à reprendre dans `sec:travail-stationnaire` et `sec:prix-stationnaire` :
- « inférieure de 0,110 point à ω̄ = 0,8 (0,656 point à 10 %) » devient 0,035 point à ω̄ = 0,625 (0,370 point à 10 %) ;
- la dépendance à n_a passe de 0,0004 point et 0,0075 point à 0,0003 et 0,0047 point (parts 0,624648 / 0,624645 / 0,624644 à 2 % ; 0,621337 / 0,621303 / 0,621290 à 10 %) ;
- le statut de `tab:etat-stationnaire` (« la part salariale de 0,80 tient à la marge normale μ̄ = 0,25 ») ;
- la ligne μ̄ de `tab:calibration` ;
- la valeur indicative de `nations.moteur.parametres.prix.MU_BAR` et le défaut `Parametres.mu_bar` du script.

Superneutralité (#80) : les cinq grandeurs de `superneutralite` sont identiques à 1e−14 près. Le verdict de #80 ne change pas. **Vérifiée.**

### 5. Conditions d'existence au point fixe (μ̄ = 0,60, n_a = 12, ν_G = 1,15)

| Condition | π̄ = 0 | 2 % | 10 % | Verdict |
|---|---|---|---|---|
| Div_F > 0 : Div_F/(p v) | 0,2221 (0,0467 avant) | 0,2238 (0,0484) | 0,2260 (0,0506) | tenue, marge accrue |
| Dividende stationnaire de la banque : marge ϑ i_CB + ϖ_L + ϖ_D D/L − ϑ n_a γ̄, par an | 0,029253 | 0,032180 | 0,043789 | tenue, **inchangée** à 1e−10 près (L, D, E^Bk inchangés) |
| Coefficient de richesse λ_H/n_a + ν_H λ_H π^pas − γ̄^e | 0,031682 | 0,030688 | 0,026884 | tenu, indépendant de μ̄ (`controler_domaine`) |
| ν_H λ_H < 1 | 0,4 | 0,4 | 0,4 | tenu, inchangé |
| Domaine de μ̄ (table du bloc 4 : μ̄ > 0, P71) | 0,60 | | | tenu, sans écrêtage |
| D1, D2, marge de E1, plafond de E6 | inchangés (D1 0,99221, D2 0,99712, E1 0,15979, E6 1,0986 à 2 %) | | | tenus |
| Caisse des entreprises en phase 4, marge (D_F + ΔL − WB)/D_F, n_a = 12 | 0,6947 (0,6070 avant) | 0,6992 (0,6115) | 0,7063 (0,6186) | tenue, marge accrue |

Toutes les conditions sont **vérifiées**. Aucune condition d'arrêt du plan n'est rencontrée sur ce point.

**Constat nouveau, n_a = 4 (#87).** La caisse de phase 4 passe de −0,1789 / −0,1655 / −0,1439 à **+0,0842 / +0,0976 / +0,1192**. La durée minimale de dépôts ν_F,min passe de 0,1965 / 0,1943 / 0,1907 an à 0,1526 / 0,1504 / 0,1468 an, sous ν_F = 1/6 an. Le point n_a = 4 entre donc dans le domaine de la lecture nette du contrôle de caisse. Les phrases « hors du domaine » de `tab:etat-stationnaire` (dépendances déclarées), de `sec:travail-stationnaire`, de `sec:prix-stationnaire` et de `sec:cadre-caisse` sont à reprendre. #87, qui porte sur la caisse hors de l'état stationnaire, reste ouverte. **Vérifiée** (`mu92e.py`).

### 6. Grandeurs publiées sans cible

| Grandeur | Avant 0 / 2 / 10 % | Après 0 / 2 / 10 % |
|---|---|---|
| Taux de distribution Div_F/(Div_F + FU), configuration R (#55) | 0,61710 / 0,50480 / 0,36359 | **0,88598 / 0,82751 / 0,72390** |
| Même taux, configuration C-F (écarts nuls) | — / 0,56853 / 0,39995 | — / 0,83609 / 0,73116 |
| Dividendes sur ventes Div_F/(p v), % | 4,67 / 4,84 / 5,06 | **22,21 / 22,38 / 22,60** |
| Dette consolidée (C42), années de PIB | 0,09884 / 0,25674 / 0,51013 | 0,09888 / 0,25695 / 0,51130 (P) |
| θ_G | 0,218474 / 0,219573 / 0,219568 | inchangé |

**Décomposition de la valeur ajoutée, en % du PIB, à π̄ = 2 %** (`mu92g.py` ; somme égale au PIB à 1e−16 près) :

| Composante | Avant | Après |
|---|---|---|
| Salaires | 79,890 | 62,465 |
| Amortissement comptable δK/n_a | 7,775 | 7,782 |
| Amortissement au coût de remplacement (pour information) | 9,986 | 9,994 |
| Intérêts nets | 2,787 | 2,789 |
| Profits non distribués FU | 4,728 | 4,651 |
| Dividendes | 4,819 | **22,313** |

Ce que cela signifie : la marge supplémentaire part **entièrement en dividendes**. Le modèle n'a ni impôts sur la production, ni loyers imputés, ni amortissement au-delà de δ = 5 % (hypothèse ; OCDE 2009 non lu). Tout le revenu non salarial qui n'est pas amortissement ou intérêt devient donc profit distribué. Je n'ai lu aucune source sur la consommation de capital fixe ni sur les dividendes observés, rapportés au PIB. Le réalisme de 22 % du PIB en dividendes est donc **non vérifié**, et c'est la question Q3 du § 8.

### 7. Effets sur #55 et #130

**#55, distribution.** Seuils de x = K^vol/(n_a y), en années de production, obtenus en faisant varier κ/t̄u à taux inchangés, comme pour le x_max publié :

| Seuil | Avant 0 / 2 / 10 % | Après 0 / 2 / 10 % |
|---|---|---|
| x_max (Div_F = 0) | 2,631 / 2,660 / 2,697 | **4,999 / 5,054 / 5,114** |
| x tel que distribution = 0,2 | 2,512 / 2,469 / 2,356 | 4,790 / 4,723 / 4,559 |
| x tel que distribution = 0,9 | 0,819 / 0,425 / — | **1,806 / 1,185 / 0,366** |

Les valeurs avant reproduisent celles publiées : 2,660, 2,697 et 2,469.

- La borne **basse** de la bande [0,2 ; 0,9] s'éloigne. Sous Δϱ = −2 points, x = 2 e^{0,02 ζ}. Pour atteindre x = 4,723 à 2 %, il faudrait ζ ≈ 43, au-delà de la borne ζ ≤ 20 (P139). **Hypothèse** : la correspondance entre Δϱ et x néglige l'effet direct du taux sur les intérêts, qui pousse dans le même sens (intérêts plus bas, Div_F plus haut). Le verdict revient à la section de #55.
- La borne **haute** devient le côté proche : distribution de 0,886 à π̄ = 0, à 0,014 de 0,9. Elle serait franchie si x < 1,806 an, soit Δϱ ≥ +2,55 points à ζ = 4. Le critère de #55 se mesure sous Δϱ = −2 points, qui éloigne de ce bord. Une hausse de ϖ_L (#130) l'éloignerait aussi.
- **La frontière de #143** n'est pas mesurée ici ; elle relève de l'instruction de #143.

**#130, banque.** Contrairement au motif du regroupement (« μ̄ pèse sur la condition d'existence du dividende de la banque »), μ̄ n'a **aucun effet** sur cette condition. L, D_H, D_F et E^Bk sont inchangés en niveau, donc la marge d'existence, le rendement des fonds propres (36,147 % à 2 %), la marge nette d'intérêt (2,4969 %) et la part distribuée (0,89025) sont identiques à 1e−10 près. Seuls changent les ratios au PIB, par (P) : Π^Bk/PIB passe de 2,2485 % à 2,2503 %. **Vérifiée.** #130 peut s'instruire sans attendre la valeur de μ̄, sauf pour les ratios au PIB.

**Ce qui n'est pas mesuré** : les bancs choqués (720 pas). Le revenu des ménages et la demande sont invariants à l'état stationnaire, mais la boucle salaires–prix lit ω* = 1/(1 + μ̄). La mesure relève du rang 8 du plan. **Non vérifiée.**

### 8. Questions ouvertes au mainteneur

1. **Définition retenue.** Je propose la part de l'économie totale, corrigée des indépendants, sur la valeur ajoutée brute au prix de base (BCE 2023, zone euro, moyenne 1998–2023 de 62,4 %). Deux autres définitions sont possibles. (b) Le coût des facteurs (AMECO ALCD2) est plus proche du modèle, mais non lu : il faut autoriser `ec.europa.eu` ou `db.nomics.world` dans la session. (c) Les sociétés non financières : je l'écarte, car ce champ exclut la production publique que le modèle fait produire par les entreprises. *Avis : (a) maintenant, avec l'écart prix de base / coût des facteurs déclaré contesté ; une relecture d'ALCD2 si l'hôte est ouvert, prospective, et si elle s'écarte de plus d'un point.*
2. **Valeur** : 0,60, ronde, ou 0,60166, égalité exacte. *Avis : 0,60.*
3. **Dividendes de 22 % du PIB.** Tout le revenu non salarial non amorti devient dividende, et δ = 5 % est une hypothèse sans source. Ce n'est pas une condition d'arrêt pour #92 à mon avis : la relation entre μ̄ et la part ne contient pas δ, et le critère de #92 publie les dividendes sans cible. Mais c'est un effet de fond hors des cinq issues. *Avis : le consigner comme limite déclarée, et ouvrir une issue sur δ et la consommation de capital fixe (proposée ci-dessous), hors de cette branche. Si vous jugez que c'est une question de fond nouvelle au sens du plan, c'est une condition d'arrêt, et c'est à vous de le dire.*
4. **n_a = 4 entre dans le domaine de caisse** (#87). C'est un constat publié, sans décision. *Avis : mise à jour du texte par `docwriter` ; #87 reste ouverte.*
5. **Borne haute de #55 proche à π̄ = 0** (0,886 contre 0,9). *Avis : l'accepter, et la vérifier dans la section de #55 avec ζ et les écarts de #130.*
6. **Motif du plan à corriger** : μ̄ ne pèse pas sur la condition d'existence du dividende de la banque (§ 7). *Avis : le noter dans la PR #162.*

**Points pour `jeu`** (je ne les tranche pas) :
- Une part salariale de 62 % est conforme aux ordres de grandeur du débat public.
- Une « marge de 60 % » risque d'être lue comme un taux de profit sur les ventes. Mieux vaut l'intituler « marge sur le coût salarial unitaire » et restituer la décomposition du § 6.
- Au point fixe, une baisse de μ̄ (#48) transfère des dividendes vers les salaires un pour un, sans effet sur la demande agrégée, puisque les ménages touchent les deux.

### 9. Issue proposée (créée : #164)

- **Titre** : J3 — Taux d'amortissement δ : consommation de capital fixe sur une source lue, et part des dividendes dans la valeur ajoutée
- **Libellés** : `needs-triage`
- **Corps** :

> *Rédigé par l'agent macro (IA).*
>
> **Constat** (instruction de #92, 16/11/2026, script d'état stationnaire à μ̄ = 0,60). Calée sur la part salariale corrigée de la zone euro (BCE, *Economic Bulletin* 4/2023, 62,4 % en moyenne 1998–2023), la marge normale donne une décomposition de la valeur ajoutée du modèle, à π̄ = 2 % : salaires 62,5 %, amortissement comptable 7,8 % (10,0 % au coût de remplacement), intérêts nets 2,8 %, profits non distribués 4,7 %, dividendes 22,3 % du PIB. δ = 5 % est une hypothèse (`tab:calibration`, OCDE 2009 non lu). Le modèle n'a ni impôts sur la production ni loyers imputés.
>
> **À faire.**
> - Lire une source de la consommation de capital fixe rapportée au PIB ou au stock de capital : définition, zone, fenêtre.
> - Dire si δ doit être recalé et avec quel effet sur K/Y (#55), le taux d'investissement et les dividendes.
> - Publier les dividendes des sociétés rapportés à la valeur ajoutée, s'ils sont lus.
>
> **Hors périmètre** : μ̄ (#92) et le levier de répartition (#48).
>
> **Liens** : #92, #55, `sec:investissement-stationnaire`, `tab:calibration` (δ).

### 10. Statut des conclusions

- **Vérifiées** (commande et sortie, ou source citée) :
  - relation entre μ̄ et la part ; valeurs des § 3 à 7 ;
  - invariance des niveaux et facteur (P) ;
  - conditions d'existence ; constat n_a = 4 ;
  - absence d'effet sur la banque et sur #80 ;
  - valeur de 62,4 % et définition de la source de la BCE.
- **Hypothèses** :
  - écart prix de base / coût des facteurs inférieur à un point ;
  - correspondance entre Δϱ et x du § 7.
- **Non vérifiées** :
  - réalisme de 22 % du PIB en dividendes ;
  - ALCD2 ;
  - effet sur les bancs choqués.

### 11. Décisions du mainteneur sur la section (16/11/2026)

- Questions 1 et 2 : définition de la BCE (prix de base), écart au coût des facteurs déclaré contesté ; **μ̄ = 0,60** retenu comme valeur proposée pour la table soumise à M34. Relecture prospective d'AMECO ALCD2 maintenant que `ec.europa.eu` et `db.nomics.world` sont ouverts à la session.
- Question 3 : dividendes à 22 % du PIB consignés comme **limite déclarée**, sans arrêt de la branche ; issue #164 (δ et consommation de capital fixe), hors branche.
- Questions 4 à 6 : avis de `macro` suivis sous la délégation P211 (constat n_a = 4 publié, #87 ouverte ; borne haute de #55 vérifiée dans la section #55 ; motif du plan corrigé dans la PR #162).

### 12. Relecture d'AMECO ALCD2 (P213, prospective)

*Relue par `macro` le 16/11/2026, rang 1 de la branche « calibration » (PR #162, tête `708c1aa`). Relecture prospective décidée par P213 : elle ne déplace pas la valeur proposée μ̄ = 0,60, et l'ancien texte du § 2 reste publié.*

**Source lue.** Commission européenne, DG ECFIN, base AMECO, variable ALCD2 : « Adjusted wage share: total economy: as percentage of GDP at current factor cost (Compensation per employee as percentage of GDP at factor cost per person employed.) ». Unité : « Percentage of GDP at factor cost ». Requête du service en ligne d'AMECO (`ec.europa.eu/economy_finance/ameco/wq/series`, variable `1.0.0.0.ALCD2`, zones EA20, EA12 et EU27), consultée le 16/11/2026 à 21:31 UTC.

**Définition.** La rémunération par salarié est rapportée au PIB au coût des facteurs par personne employée. Cela revient à imputer aux non-salariés la rémunération moyenne des salariés. Le dénominateur est le **PIB au coût des facteurs**, c'est-à-dire sans les impôts nets de subventions sur la production et les importations. C'est le dénominateur que le § 1 jugeait le plus proche du modèle.

**Valeur.** Zone euro à 20 pays (EA20), moyenne annuelle de 1998 à 2023 (26 observations) : **63,11 %**. Minimum 61,20 % (2007), maximum 64,17 % (1999), 61,93 % en 2023. Variantes de fenêtre : 63,27 % de 1995 à 2023, 63,11 % de 1998 à 2024. EA12, même fenêtre : valeurs à moins de 0,14 point de l’EA20 chaque année (écart maximal 0,131 point, en 2014). Calcul : moyenne arithmétique des valeurs annuelles rendues par la requête, commande Python dans le scratchpad de la session. **Vérifiée.**

**Millésime non identifié.** La série court jusqu'en 2027, donc ses dernières années sont des prévisions. Les pages d'AMECO qui datent la mise à jour sont refusées par le proxy (CONNECT 403). La fenêtre 1998–2023 évite les années de prévision les plus probables, mais les valeurs passées restent révisables.

**Écart à 62,4 %** (BCE, *Economic Bulletin* 4/2023, prix de base, même fenêtre 1998–2023) : **+0,71 point**. Il reste **sous le seuil d'un point** : aucune question au mainteneur n'est ouverte.
- **Ce que cela tranche.** L'hypothèse du § 2, « écart entre prix de base et coût des facteurs inférieur à un point », devient un constat sourcé : +0,71 point sur 1998–2023. Les zones ne sont pas exactement les mêmes : l'EA20 pour AMECO, la zone euro de l'encadré de la BCE, dont la composition n'est pas relue. Les millésimes diffèrent aussi.
- **Effet sur #92.** Le modèle donne ΣWB/ΣVA = 0,624645 à μ̄ = 0,60 et π̄ = 2 %, soit −0,65 point sous ALCD2. Le critère de #92 (un point) tient sous les deux définitions. La valeur proposée μ̄ = 0,60 ne change pas.
- **Lecture au coût des facteurs.** Elle correspondrait à la variante V3a du § 3, part de 63,4 % à μ̄ = 0,5763, à 0,3 point d'ALCD2. Je ne la recommande pas : l'écart de 0,71 point tient pour l'essentiel à la définition du dénominateur, et il est déclaré.

**Statut.** Valeur, fenêtre, définition et écart : **vérifiés** (requête et calcul ci-dessus). Millésime : **non vérifié**.

## 2. #143 — S6 : ti = 0 au-delà d'une frontière (bloc 6) ; domaine du taux réel du crédit (instruction, sans `Closes`)

*Instruite par `monnaie` (expert pilote) le 16/11/2026, rang 1 de la branche « calibration » (PR #162, tête `dfe352e`), avant la section de #55 (P207). `macro` est consulté ensuite sur la frontière crédit. Les chiffres du modèle viennent de sondes hors dépôt qui appellent, sans les modifier, `outils/etat_stationnaire.py`, le socle d'essai `tests/invariants/socle_partiel.py`, les assistants de `tests/invariants/test_socle_complet.py` et les fonctions du moteur (méthode au § 2.3.1). Ce sont des résultats du modèle, pas des faits. Les faits portent leur source et leur date. Chaque conclusion est marquée **vérifiée**, **hypothèse** ou **non vérifiée**. La voie de #143 se tranche au plus tard au J4 (P207). P148 a retenu la voie (1), une borne de domaine du taux réel du crédit liée au domaine du levier de taux, sans rouvrir M28. Cette section ne la rouvre pas : elle la chiffre et en montre les limites.*

### 2.1 Question et grandeurs

**Question.** S6, ti_{t+1} = ti_t exp[(λ_ti/n_a)(tu_t − tu*_t)] avec tu*_t = t̄u exp(ζ Δϱ_t) (S2), rend ti_{t+1} = 0,0 en double précision au-delà d'un écart Δϱ. Le pas est alors refusé en phase 5 (domaine ti > 0). Il faut établir :
- où se trouve cette frontière en fonction de ζ, de μ̄ et des écarts bancaires de #130 ;
- quel arrêt du moteur lie le premier ;
- si cette frontière est atteignable ;
- quelles voies restent ouvertes pour le J4.

**Grandeurs.**

| Grandeur | Définition | Unité | Dénominateur | Fenêtre |
|---|---|---|---|---|
| ϱ_{L,t} | (1 + i_{L,t})/(1 + π\*_t) − 1, forme exacte de Fisher (S1, `eq:investissement-taux-reel-credit`), i_L et π\* lus à l'ouverture | par an | déflateur : la **cible** π\*, pas l'inflation réalisée ni π^e (M28) | un pas |
| Δϱ_t | ϱ_{L,t} − ϱ̄_L ; ϱ̄_L est la norme résolue, recopiée à chaque pas (P128) | par an | — | un pas |
| ζ | élasticité de niveau de tu\* à Δϱ (S2) | sans dimension, par unité de taux réel annuel | — | — |
| Frontière S6 | plus petit Δϱ tel que ti_{t+1} = 0,0 | par an | — | un pas, depuis l'état résolu, tu = t̄u |
| Frontière de caisse | plus petit i_{L,0} tel que le pas 0 est refusé par `eq:noyau-caisse-nette` (entreprises, ligne 9, phase 6) | par an | — | pas 0 depuis l'état résolu ; seul i_{L,0} est changé |
| Frontière liante | plus petit i_{L,0} qui arrête le pas 0, quelle qu'en soit la cause | par an | — | idem |

### 2.2 Sources

- **Forme de la frontière** : spécification (S2, S6, `sec:investissement-conditions`) et code du bloc 6 (`src/nations/blocs/investissement.py:92-126`), lus à `dfe352e`. Ce sont des sources du modèle, pas des faits.
- **Plage historique des taux directeurs et des taux réels du crédit**, qui fonderait la valeur d'une borne de domaine du levier (voie 1) : **non trouvée**. Deux accès ont échoué :
  - la série FEDFUNDS de `fred.stlouisfed.org` : proxy CONNECT 403, hôte hors de la liste ouverte ;
  - le téléchargement H.15 de `www.federalreserve.gov` : la page `releases/h15/data.htm` rend une redirection 301 et l'URL de `datadownload` une réponse vide.
  
  Aucun chiffre historique n'est donc avancé (P208). Cette valeur relève du J4, pas de la table soumise à M34.
- **Seuil d'hyperinflation** : le seuil de 50 % **par mois** attribué à Cagan (1956, « The Monetary Dynamics of Hyperinflation ») n'a été trouvé que dans des sources secondaires, par recherche web le 16/11/2026 (résumé de l'outil ; tableau de Hanke et Krus cité dans ces résultats). Le texte original n'est pas relu : **non vérifié**. Aucune conclusion ci-dessous n'en dépend.
- **Pas une source** : aucun résultat de la v1.5 ni de la v2.0 n'est utilisé.

### 2.3 Frontière mesurée

#### 2.3.1 Méthode et commandes

Sondes du scratchpad de la session, non versées, lancées depuis `/home/user/projet_macro` à `dfe352e` (`git status` vide avant et après) :
- **`s6.py`** : bisection jusqu'à deux flottants adjacents sur `utilisation_visee` puis `part_visee_suivante`. Les fonctions pures du bloc et les valeurs de la table (t̄u = 0,8, λ_ti/n_a = 0,02/12) sont utilisées sans modification, comme dans `test_frontiere_de_la_double_precision_des_bornes_b`. ti et ϱ̄_L viennent du sentier du script `socle_partiel.sentier(π̄, mu_bar=μ̄)`.
- **`moteur.py`** : bisection sur i_{L,0} (80 itérations) du premier pas 0 refusé par `ordonnanceur.executer_pas`.
  - L'état initial est résolu par le script ; seul i_{L,0} est changé.
  - Socle complet : blocs 2 à 9 réels, `blocs_du_socle_complet`. Socle partiel : blocs 2 à 8 réels.
  - Tables : μ̄ (bloc 4) et ζ (bloc 6) par `varier` ; blocs 7 à 9 alignés sur le sentier par `parametres_du_sentier`.
- **`caisse.py`** : la même mesure à ζ = 0. tu\* = t̄u y est constant, donc S6 ne lie jamais et seule reste la frontière de caisse ; sensibilité à ϖ_L, ϖ_D et ϑ.
- Commande type : `uv run python -I <scratchpad>/sondes143/<sonde>.py`. Les sorties intégrales sont dans `<scratchpad>/sondes143/sortie_*.txt`.
- Contrôle : à μ̄ = 0,25, π̄ = 2 %, ζ = 4, la sonde reproduit la frontière publiée de S6, Δϱ = 3,307756 (i_L = 3,424111). Elle reproduit aussi l'arrêt de caisse relevé par `coder` et `audit` (commentaire de #143), i_{L,0} = 3,252184. Les socles complet et partiel donnent des frontières de pas 0 identiques à toutes les décimales imprimées.

#### 2.3.2 La frontière de S6 ne dépend que du produit ζΔϱ (vérifiée)

ti vaut 0,139638 aux six points (μ̄ ∈ {0,25 ; 0,60} × π̄ ∈ {0 ; 2 ; 10 %}) : la part d'investissement stationnaire ne dépend ni de μ̄ ni de π̄. La frontière est donc la même partout :

**ζ Δϱ_lim = c = 13,231023**, soit Δϱ_lim = 13,231023/ζ par an.

Forme fermée, avec tu = t̄u : c = ln{1 + [1075 ln 2 + ln ti]/[(λ_ti/n_a) t̄u]} = 13,230992, à 2,3e−6 relatif de la bisection. Ce résultat retrouve la forme raffinée publiée.

| ζ | Δϱ_lim (par an) | i_L à la frontière, π̄ = 0 / 2 / 10 % | Δi_L = Δi_CB, écarts constants, 0 / 2 / 10 % |
|---|---|---|---|
| 4 | 3,307756 | 3,337756 / 3,424111 / 3,769531 | 3,307756 / 3,373911 / 3,638531 |
| 6 | 2,205171 | 2,235171 / 2,299474 / 2,556688 | 2,205171 / 2,249274 / 2,425688 |
| 8 | 1,653878 | 1,683878 / 1,737155 / 1,950266 | 1,653878 / 1,686955 / 1,819266 |
| 12 | 1,102585 | 1,132585 / 1,174837 / 1,343844 | 1,102585 / 1,124637 / 1,212844 |
| 17 | 0,778295 | 0,808295 / 0,844061 / 0,987125 | 0,778295 / 0,793861 / 0,856125 |
| 20 | 0,661551 | 0,691551 / 0,724982 / 0,858706 | 0,661551 / 0,674782 / 0,727706 |

Les colonnes sont identiques à μ̄ = 0,25 et à μ̄ = 0,60 (sortie `sortie_s6.txt`).

Dépendances :
- **μ̄** : aucune, puisque ti est inchangé. **Vérifiée.**
- **π̄** : aucune en Δϱ. En i_L, la frontière se lit par S1 inversée, i_L = (1 + π\*)(1 + ϱ̄_L + Δϱ) − 1. **Vérifiée.**
- **Écarts de #130** : aucune en Δϱ ni en Δi_CB, puisque ϱ̄_L est la norme du même ϖ_L et que ϖ_L s'annule dans l'écart. Le niveau de i_L à la frontière suit ϱ̄_L, donc ϖ_L, à peu près point pour point. ϖ_D et ϑ n'entrent pas dans S2 ni dans S6. **Vérifiée** (forme ; ϱ̄_L à 2 % = 0,029608 pour r̄ = 0,01 et ϖ_L = 0,02).
- **λ_ti**, hors des cinq issues : c baisse de ln 2 quand λ_ti double. Au bord du domaine, λ_ti = n_a, on a c = 6,835 et Δϱ_lim = 0,342 à ζ = 20. **Vérifiée** (forme fermée).

#### 2.3.3 Arrêt liant au pas 0 : caisse ou S6 selon ζ (vérifiée)

Frontière de caisse seule, mesurée à ζ = 0 sur le socle complet (`sortie_caisse.txt`). L'arrêt est un `DefautComptable` en phase 6, `eq:noyau-caisse-nette`, entreprises, ligne 9 : les intérêts i_L L/n_a épuisent D_F. Le seuil ζ\* = c/Δϱ_caisse marque où les deux frontières se croisent.

| μ̄ | π̄ | i_{L,0} de caisse (par an) | Δϱ de caisse | i_L L/(n_a D_F) au seuil | ζ\* |
|---|---|---|---|---|---|
| 0,25 | 0 | 2,517284 | 2,487284 | 1,0092 | 5,319 |
| 0,25 | 2 % | 3,252184 | 3,139200 | 1,0152 | 4,215 |
| 0,25 | 10 % | 6,090332 | 5,417574 | 1,0291 | 2,442 |
| **0,60** | 0 | 2,735863 | 2,705863 | 1,0969 | **4,890** |
| **0,60** | 2 % | 3,533060 | 3,414569 | 1,1029 | **3,875** |
| **0,60** | 10 % | 6,609380 | 5,889437 | 1,1168 | **2,247** |

Lecture :
- Si ζ < ζ\*, la caisse des entreprises arrête le pas 0 avant S6. Si ζ > ζ\*, c'est S6 qui l'arrête en phase 5 : c'est la frontière de #143.
- Le seuil de caisse vaut à peu près i_L ≈ n_a D_F/L. Il croît avec π̄ parce que le levier porte sur le capital **comptable** (L = 9,12 / 7,10 / 3,84 à D_F égal à 1,8956).
- μ̄ = 0,60 le repousse d'environ 8,5 % (rapports 1,0868 / 1,0864 / 1,0852) : la marge accrue apporte plus de caisse avant la phase 6.

| μ̄ | π̄ | ζ = 4 : premier i_{L,0} arrêté, cause | ζ = 20 : premier i_{L,0} arrêté, cause |
|---|---|---|---|
| 0,25 | 0 | 2,517284, caisse (phase 6) | 0,691551, S6 (phase 5) |
| 0,25 | 2 % | 3,252184, caisse (phase 6) | 0,724982, S6 |
| 0,25 | 10 % | 3,769531, S6 | 0,858706, S6 |
| 0,60 | 0 | 2,735863, caisse (phase 6) | 0,691551, S6 |
| 0,60 | 2 % | **3,424111, S6** (la caisse liait à μ̄ = 0,25) | 0,724982, S6 |
| 0,60 | 10 % | 3,769531, S6 | 0,858706, S6 |

Sensibilité de la frontière de caisse aux paramètres de #130, à μ̄ = 0,60 et π̄ = 2 % : i_{L,0} = 3,533058 et 3,533062 pour ϖ_L = 0,01 et 0,03 ; 3,534395 et 3,530391 pour ϖ_D = 0,005 et 0,02 ; 3,533060 pour ϑ = 0,08 et 0,15. Elle est négligeable, au plus 0,004 par an. **Vérifiée.**

**Constat pour la table de M34.** Avec μ̄ = 0,60 et ζ = 4, la frontière liante à π̄ = 2 % passe de la caisse à S6 (3,252 → 3,424 par an). La phrase du test `test_part_visee_nulle_refusee_par_le_moteur`, « sur ce socle, le pas échoue déjà en phase 6 […] pour i_{L,0} ≳ 3,25 par an », devient fausse à π̄ = 2 % une fois μ̄ changé au rang 3. Elle reste vraie à π̄ = 0. Les deux tests devraient rester verts : le second se place au-delà de la frontière de S6, qui lie avant la caisse à ce point (déduit des mesures ci-dessus ; tests non exécutés à μ̄ = 0,60). Seul le texte publié est à reprendre (surface de `docwriter` et du commit `code:`/`tests:` de #92). **Vérifiée.**

### 2.4 La frontière de S6 n'est pas le domaine pertinent (mesures complémentaires)

La frontière de #143 est un écart **d'un pas** de 66 à 331 points de taux réel. Deux mesures montrent que le moteur sort de son domaine bien avant, et pour d'autres causes.

#### 2.4.1 Le cas atteignable est une spirale inflationniste, pas un taux réel élevé (vérifiée)

Sonde `c62.py` : cas de `macro` du 15/11/2026, rejoué sur le socle complet avec les assistants du test C62 (`bloc_9_compose`, `choc_de_theta_G(1,01)`), non modifiés. Réglages : φ = 0, π\* = 10 %, 720 pas. π glissant = P_{t−1}/P_{t−13} − 1 (`eq:moteur-glissement`).

| Pas | π glissant (par an) | i_L (par an) | Δϱ sur π\* (S1) | Taux réel ex post (1 + i_L)/(1 + π) − 1 | ti |
|---|---|---|---|---|---|
| 403 | 0,1799 | 0,2904 | 0,1449 | 0,0936 | 0,1323 |
| 463 | 0,4273 | 0,6247 | 0,4488 | 0,1383 | 0,1151 |
| 487 | 1,1063 | 1,2437 | 1,0115 | 0,0652 | 0,06944 |
| 511 | 2,0835 | 2,5716 | 2,2187 | 0,1583 | 1,1e−19 |
| 523, arrêt S6 (phase 5) | 2,5287 | 3,3812 | 2,9547 | 0,2416 | 1,8e−275 |

- L'arrêt au pas 523 est reproduit. Il est identique à μ̄ = 0,25 et à μ̄ = 0,60.
- π glissant dépasse 50 % par an dès le pas 468.
- ti tombe sous 1e−3 × ti_0 dès le pas 502, soit 21 pas avant l'arrêt.

À ζ = 8, l'arrêt survient au pas 543. À ζ = 20, il n'y en a **aucun** sur 720 pas : i_L = 0,1594 et π = 0,1040 au pas 720. **Vérifiée.**

Conséquences :
- **(a)** Le cas atteignable est une spirale inflationniste sous φ = 0 (C62), menée par la règle de taux (BC1, levier fermé). Ce n'est pas un taux réel élevé : au moment de l'arrêt, le taux réel ex post est de +24 %. Le Δϱ de 295 points n'existe que parce que S1 déflate par la **cible** π\* (M28). Dans une spirale, ϱ_L mesure donc le taux nominal. **Vérifiée.**
- **(b)** Une borne de domaine du **levier** (voie 1, P148) n'empêche pas ce cas : le joueur n'y touche pas le levier. **Vérifiée** (le taux directeur y est la prescription de la règle, `banque_centrale.py:153-155`).
- **(c)** L'inflation y atteint 253 % par an, soit 11,1 % par mois. C'est loin du seuil conventionnel de 50 % par mois (non vérifié, § 2.2) : de l'inflation forte, pas une hyperinflation au sens usuel. **Hypothèse** quant au classement.
- **(d)** L'existence même de l'arrêt dépend de ζ : arrêt à ζ = 4 et 8, aucun à ζ = 20. C'est à reprendre dans #55 (§ 2.6).

#### 2.4.2 Sous un écart durable du taux directeur, la caisse arrête bien avant S6 (vérifiée, avec une réserve de méthode)

Sonde `durable2.py` sur le socle complet, 720 pas. À l'ouverture de chaque pas, r̂\* est relevé de δ au-dessus de sa valeur stationnaire. BC1 rend alors un taux directeur au-dessus de la règle, et i_L et i_D suivent par le bloc 7, à écarts constants. Ce montage imite un levier de taux tenu par le joueur. **Réserve** : c'est une manipulation externe de l'état par la sonde, pas un scénario du moteur. Le levier n'existe pas avant le J4.

| μ̄ | π̄ | ζ | δ = +10 points (Δϱ moyen réalisé) | δ = +20 points (Δϱ moyen réalisé) |
|---|---|---|---|---|
| 0,25 | 0 | 4 | arrêt pas 462 (38,5 ans), caisse des entreprises, phase 4, ligne 5 (0,088) | arrêt pas 23, même cause (0,190) |
| 0,25 | 2 % | 4 | aucun arrêt (0,088) | arrêt pas 62 (5,2 ans), même cause (0,185) |
| 0,25 | 0 | 20 | arrêt pas 451, même cause (0,069) | arrêt pas 43, même cause (0,163) |
| 0,60 | 0 | 4 | aucun arrêt (0,085) | arrêt pas 479 (39,9 ans), **caisse de l'État**, phase 7, ligne 19a-banque, M_G (0,175) |
| 0,60 | 0 | 20 | arrêt pas 494, caisse de l'État, phase 7 (0,066) | arrêt pas 258, même cause (0,156) |
| 0,60 | 2 % | 4 | aucun arrêt (0,088 ; ti × 0,84) | aucun arrêt (0,179 ; ti × 0,66) |
| 0,60 | 2 % | 20 | aucun arrêt (0,072 ; ti × 0,21) | aucun arrêt (0,166 ; **ti × 1,1e−6**) |
| 0,60 | 10 % | 20 | aucun arrêt (0,080 ; ti × 0,15) | aucun arrêt (0,177 ; **ti × 1,8e−9** ; D_F/L = 421) |

À δ = +2 et +5 points, aucun arrêt dans aucune des 24 configurations (sortie `sortie_durable2.txt`). Les arrêts surviennent à des Δϱ moyens réalisés de 6,6 à 19 points, soit 4 à 38 fois moins que la frontière de S6 au même ζ (17 à 38 fois à ζ = 4, 4 à 10 fois à ζ = 20). **Vérifiée.**

Ce que cela signifie :
- **μ̄ = 0,60 supprime les arrêts de caisse des entreprises** dans la grille mesurée, grâce à une marge plus large. **Vérifiée.**
- **Arrêts de la caisse de l'État.** Ils apparaissent à π̄ = 0 sous un écart durable de 10 à 20 points, après 21 à 41 ans. Leur mécanisme n'est **pas diagnostiqué** (émission E8 à E11 face à une charge d'intérêts croissante, hypothèse). Ils relèvent de la frontière avec `macro` (solde) et de mon domaine (placement).
- **Économie vidée d'investissement.** À ζ = 20 et δ = +20 points, le moteur tourne 60 ans **sans arrêt** pendant que ti est divisé par un million à un milliard. Ce n'est pas un refus mais une économie sans investissement, que S-ζ rend stationnaire (x = 2 e^{−ζΔϱ}). C'est à rapprocher de « tu\* > 1 sans plafond » (#143, corps). **Vérifiée** (mesure) ; caractère indésirable : **hypothèse**.

Une première version de la sonde (`durable.py`) relevait i_L et i_D sans toucher à i_CB. Elle donne des arrêts du même ordre (phases 4 et 7, dès +10 points). Elle est écartée comme incohérente : la banque y emprunte au taux directeur de la règle.

#### 2.4.3 Échelle des frontières en ζΔϱ, côté hausse du taux

| Seuil | ζΔϱ | Δϱ à ζ = 4 | Δϱ à ζ = 20 | Statut |
|---|---|---|---|---|
| tu\* = 1 (capacité normale atteinte) | 0,2231 | 0,056 | 0,011 | vérifiée (forme) |
| distribution = 0,9 (borne haute de #55), μ̄ = 0,60, π̄ = 0 / 2 / 10 % | 0,102 / 0,523 / 1,698 | 0,026 / 0,131 / 0,425 | 0,005 / 0,026 / 0,085 | hypothèse : x = 2 e^{−ζΔϱ} et seuils de x du § 1.7, effet direct des intérêts négligé |
| arrêts sous écart durable (§ 2.4.2), Δϱ moyen réalisé | ≈ 0,35 à 3,3 | 0,085 à 0,19 | 0,066 à 0,16 | vérifiée (sonde) |
| arrêt de caisse au pas 0 | 9,9 à 23,6 | 2,49 à 5,89 | sans objet (S6 lie avant) | vérifiée |
| **S6 au pas 0 (#143)** | **13,231** | 3,308 | 0,662 | vérifiée |

Côté baisse, pour mémoire (#55) : Div_F = 0 à ζΔϱ = −0,916 / −0,927 / −0,939, à μ̄ = 0,60 et π̄ = 0 / 2 / 10 %. Ces valeurs sont tirées des x_max du § 1.7, sous la même hypothèse.

### 2.5 Voies possibles pour #143 (avis, sans trancher)

| Voie | Contenu | Couvre le cas atteignable (§ 2.4.1) ? | Rouvre | Coût de calcul | Avis |
|---|---|---|---|---|---|
| **(1) P148**, borne de domaine du taux réel du crédit liée au levier (J4) | Le levier de taux refuse un i_CB qui porterait \|Δϱ\| au-delà d'une borne déclarée | **Non** : la règle y conduit seule | rien | nul | Nécessaire au J4, insuffisante seule |
| **(1′)** Domaine de validité de S-ζ en ζΔϱ, refusé et typé | Refus typé « hors du domaine de S-ζ » quand ζ\|Δϱ\| > c_dom, avec c_dom déclaré bien en deçà de 13,23 (par exemple tu\* ≤ un multiple déclaré de t̄u) ; contrôle du moteur, aucune équation changée | Oui : l'arrêt est diagnostiqué plus tôt et nommé | rien, si c'est un contrôle de domaine (P139) | une comparaison par pas | **Recommandée en J3-e2** (branche des refus typés), avec (1) au J4 |
| (2) Statu quo | Arrêt générique en phase 5 au-delà de 13,23/ζ | arrêt brut après 43 ans de jeu | rien | nul | Acceptable seulement jusqu'au J4 |
| (3) S2 ou S6 bornées par construction (tu\* logistique, par exemple) | Mécanisme plutôt que borne | Oui, sans arrêt | **M28** ; équation nouvelle : condition d'arrêt de la branche | négligeable | Écartée dans cette branche ; à instruire seulement si (1′) se révèle trop restrictive |
| (4) S1 déflatée par π^e plutôt que par π\* | Supprime l'artefact du § 2.4.1 (a) | Partiellement : avec λ_e = 0,2 par an, π^e retarde beaucoup sur π dans une spirale (non mesuré) | **M28** (lecture « ϱ_L sur π\* ») | nul | Non recommandée maintenant ; non mesurée |
| (5) Mécanisme de crise au J6 | Défaut des entreprises (#57), spirale inflationniste et « économie effondrée » comme condition de fin typée (J6, J7) | Oui, et de façon jouable | rien au socle | à évaluer | **Cible de long terme**, à lier à (1′) |

**Mon avis.** Garder P148 : voie (1) au J4, sans rouvrir M28. La compléter par (1′), un domaine de validité de S-ζ **exprimé en ζΔϱ** et non en Δϱ, puisque la frontière ne dépend que du produit (§ 2.3.2). Son refus typé relève de J3-e2 ; le mécanisme de crise (5) relève du J6. Deux motifs :
- la frontière de S6 est un symptôme numérique : l'économie du modèle est sortie de son domaine bien avant, que ce soit par l'investissement effondré, la caisse ou l'État (§ 2.4) ;
- le seul cas atteignable connu ne passe pas par le levier (§ 2.4.1).

La valeur de c_dom ne se fixe pas dans cette branche : elle dépend du ζ retenu (#55) et du domaine du levier (J4). **Hypothèse** : un c_dom de l'ordre de 0,5 à 1, soit tu\* ≤ 1,3 à 2,2 fois t̄u, couvrirait les écarts durables de quelques points sans faux refus. Ce chiffre n'est **pas mesuré**.

**Réponse à la question posée à `monnaie`** (commentaire de #143 : « une entreprise doit-elle pouvoir financer des intérêts supérieurs à sa caisse ? »). **Avis : le refus est le comportement voulu au socle.**
- Sous la règle F, le crédit finance le capital (F1 : ΔL^d = lv\*[(1 − δ/n_a)K + I^plan] − L), et le crédit est servi à la demande (M31).
- Un découvert automatique qui paierait les intérêts par du crédit nouveau ferait de la banque le prêteur d'une dette qui se capitalise sans limite. Le noyau ne verrait jamais l'insolvabilité, et la crise serait masquée au lieu d'être diagnostiquée.
- Le mécanisme juste est le défaut de l'emprunteur, avec ses pertes sur crédits et ses fonds propres bancaires (#57, J6). Ce n'est pas un découvert.
- Ce point est mon avis de domaine, sans source lue : **hypothèse** de conception, à confirmer par le mainteneur.
- Le refus doit devenir un refus typé nommé, comme le veut J3-e2, et non un `DefautComptable` brut. **Vérifiée** quant à la forme actuelle de l'arrêt : `DefautComptable` en phase 6, ou en phase 4 sous écart durable.

### 2.6 Ce que `macro` doit reprendre dans la section #55

1. **Frontière de #143 au ζ retenu** (critère de #55) : Δϱ_lim = 13,231/ζ par an, indépendante de μ̄, de π̄ et des écarts de #130 (§ 2.3.2). La publier avec la frontière **liante** du pas 0, c'est-à-dire la caisse si ζ < ζ\*, avec ζ\* = 4,890 / 3,875 / 2,247 à μ̄ = 0,60 et π̄ = 0 / 2 / 10 % (§ 2.3.3).
2. **Verdict C51 « à ζ calibré »** (P161) et **C62** : l'arrêt du cas atteignable dépend de ζ (pas 523 à ζ = 4, 543 à ζ = 8, aucun à ζ = 20 ; § 2.4.1). Remesurer `test_temps_de_doublement_sous_phi_nul` au ζ retenu, et le publier dans le tableau avant / après.
3. **Borne haute de la distribution** (§ 1.7, question 5 du § 1.8) : en ζΔϱ, elle est la plus proche de toutes les frontières (0,102 à π̄ = 0, § 2.4.3). Un ζ élevé la rend franchissable dès quelques dixièmes de point d'écart durable. Ce critère, plus que #143, contraint ζ par le haut.
4. **Économie vidée d'investissement à ζ élevé** (§ 2.4.2) : à ζ = 20, un écart durable de 17 à 18 points de Δϱ réalisé (δ = +20) divise ti par un million en 60 ans, sans arrêt. Dire si c'est acceptable pour la plage de ζ retenue, ou si ζ ≤ 20 (P139) doit être resserré.
5. **Côté baisse** (critère « −2 points » de #55) : il n'est pas touché par #143. S6 ne sous-dépasse que pour Δϱ > 0, et S2 sous-dépasse seulement vers tu\* = 0 à ζΔϱ ≈ −745, hors de toute portée.
6. **Frontière avec `monnaie`** : les arrêts de la caisse de l'État sous écart durable (§ 2.4.2) relèvent du solde (à toi) et du placement (à moi). Je propose qu'ils soient diagnostiqués au J3-f2 (#87, #154) ou au J4, pas dans cette branche.

### 2.7 Questions au mainteneur

1. **Voie de #143.** Garder P148 (voie 1, au J4) et y ajouter (1′), domaine de validité de S-ζ en ζΔϱ, refus typé en J3-e2, puis le mécanisme de crise (5) au J6 ? Ou statu quo jusqu'au J4 ? *Avis : (1) + (1′) + (5), sans rouvrir M28.*
2. **Caisse des entreprises.** Confirmer que le refus est voulu au socle (pas de découvert automatique), et que le mécanisme relève du défaut des entreprises (#57, J6) ? *Avis : oui.*
3. **Texte du test** `test_part_visee_nulle_refusee_par_le_moteur` (« ≳ 3,25 par an ») : à reprendre avec le commit de #92, puisque la frontière liante passe à S6 à π̄ = 2 % (§ 2.3.3). *Avis : oui, au rang 3, texte seulement.*
4. **Arrêts sous écart durable** (§ 2.4.2) : faut-il les consigner dans #143 (commentaire proposé ci-dessous), ou ouvrir une issue pour le domaine du levier de taux au J4 ? *Avis : commentaire sur #143, sans issue nouvelle ; #87, #154 et #57 couvrent les mécanismes.*
5. **Source d'une plage historique des taux** pour la borne du levier : non trouvée dans cette session (FRED bloqué, H.15 illisible). Faut-il ouvrir `fred.stlouisfed.org` pour le J4 ? *Avis : oui, au J4, pas maintenant.*

### 2.8 Points pour `jeu` (je ne les tranche pas)

- Au statu quo, le joueur voit un arrêt du moteur après environ 43 ans dans le seul cas atteignable connu (φ = 0, π\* = 10 %). C'est illisible : la cause réelle, une spirale inflationniste due au financement des intérêts par le déficit, reste cachée derrière « ti hors domaine ».
- Une borne du levier (voie 1) se lit simplement : « taux directeur entre X et Y ». Elle ne protège pas d'une spirale menée par la règle.
- À ζ élevé, un taux tenu haut pendant des décennies vide l'économie de son investissement, sans signal. Il faudra un indicateur visible (taux d'investissement, utilisation visée).

### 2.9 Commentaire publié sur #143 (P217)

> *Rédigé par l'agent monnaie (IA).*
>
> Instruction au rang 1 de la branche « calibration » (PR #162, `dfe352e` ; `docs/blocs/calibration.md`, section #143) :
> - La frontière de S6 ne dépend que du produit **ζΔϱ = 13,231**. Elle est indépendante de μ̄ (0,25 ou 0,60), de π̄ (0, 2, 10 %) et des écarts de #130, puisque ti = 0,139638 aux six points.
> - Au pas 0, la caisse des entreprises lie la première si ζ < ζ\* (4,890 / 3,875 / 2,247 à μ̄ = 0,60 ; π̄ = 0 / 2 / 10 %), et S6 au-delà.
> - Le cas atteignable (φ = 0, π\* = 10 %, pas 523, identique à μ̄ = 0,60) est une spirale inflationniste menée par la règle. Au moment de l'arrêt : π = 253 % par an, taux réel ex post +24 %, Δϱ de 295 points seulement parce que S1 déflate par π\*. Arrêt au pas 543 à ζ = 8, aucun à ζ = 20.
> - Sous un écart durable du taux directeur de +10 à +20 points (sonde), le moteur s'arrête par la caisse des entreprises (μ̄ = 0,25) ou de l'État (μ̄ = 0,60, π̄ = 0), bien avant S6.
> - Avis de `monnaie` sur la caisse : le refus est voulu au socle ; le mécanisme relève du défaut des entreprises (#57).
> - Voie proposée : P148 (levier, J4), complétée d'un domaine de validité de S-ζ en ζΔϱ (refus typé, J3-e2) et d'un mécanisme de crise (J6).

### 2.10 Statut des conclusions

- **Vérifiées** (commande et sortie) :
  - frontière de S6 en ζΔϱ = 13,231 et son invariance à μ̄, π̄ et #130 ;
  - frontières de caisse et ζ\* ;
  - frontière liante aux 12 points (μ̄ × π̄ × ζ ∈ {4, 20}), socle complet et socle partiel ;
  - changement de cause liante à μ̄ = 0,60, π̄ = 2 %, ζ = 4 ;
  - cas atteignable rejoué : pas 523, π, taux ex post, ti, dépendance à ζ ;
  - arrêts sous écart durable (sonde) ;
  - sensibilité négligeable de la caisse à ϖ_L, ϖ_D et ϑ.
- **Hypothèses** :
  - correspondance x = 2 e^{−ζΔϱ} pour le seuil de distribution ;
  - c_dom de 0,5 à 1 ;
  - refus voulu au socle (avis de conception) ;
  - mécanisme des arrêts de la caisse de l'État ;
  - classement « inflation forte, non hyperinflation ».
- **Non vérifiées** :
  - seuil de Cagan (original non relu) ;
  - plage historique des taux (source non trouvée) ;
  - effet de la voie (4) ;
  - représentativité d'un levier par r̂\* relevé (le levier n'existe qu'au J4).
- **Conditions d'arrêt du plan** :
  - aucune rencontrée : aucune valeur hors domaine, aucune équation à changer dans cette branche ;
  - aucun banc d'empreintes n'a été exécuté ici ; le seul cas connu qui atteint la frontière, C62 à π\* = 10 %, est un test déjà publié avec son arrêt, inchangé au pas près à μ̄ = 0,60 (pas 523) ;
  - la dépendance de C62 à ζ est à surveiller au commit de #55.

### 2.11 Décisions du mainteneur sur la section (16/11/2026)

- Question 1 : voie **(1) + (1′) + (5)**, sans rouvrir M28 (P215). (1) borne du levier au J4 (P148) ; (1′) domaine de validité de S-ζ en ζΔϱ, refus typé, en J3-e2 (c_dom fixé après le ζ retenu par #55 et le domaine du levier) ; (5) mécanisme de crise au J6 (#57).
- Question 2 : refus de la caisse des entreprises **confirmé** comme comportement voulu au socle, sans découvert automatique ; refus typé en J3-e2 ; défaut des entreprises au J6 (#57) (P216).
- Questions 4 et 5 : arrêts sous écart durable consignés par un commentaire sur #143, sans issue nouvelle ; `fred.stlouisfed.org` à ouvrir au J4 seulement (P217).
- Question 3 : texte du test `test_part_visee_nulle_refusee_par_le_moteur` repris avec le commit de #92 au rang 3 (délégation P211).

## 3. #55 — Taux de distribution, capital et ζ (bloc 6)

*Instruite par `macro` (expert pilote) le 16/11/2026, rang 1 de la branche « calibration » (PR #162, tête `708c1aa`), après la section #143 (P207). Les chiffres du modèle viennent de sondes hors dépôt. Elles appellent, sans les modifier, `outils/etat_stationnaire.py`, `outils/maquette_conjointe.py`, le socle d'essai `tests/invariants/socle_partiel.py` et les assistants de `tests/invariants/test_socle_complet.py` (méthode au § 3.4.1). Ce sont des résultats du modèle, pas des faits. Les faits portent leur source et leur date. Chaque conclusion est marquée **vérifiée**, **hypothèse** ou **non vérifiée**. La base est l'état à μ̄ = 0,60 du § 1 (P213).*

### 3.1 Grandeurs visées et correspondance avec le modèle

| Grandeur | Définition | Unité | Dénominateur | Fenêtre |
|---|---|---|---|---|
| Taux de distribution (fiche 6, § 9.4 et § 9.6, test « Bornes » (a) et (d)) | ΣDiv_F/Σ(Div_F + FU) ; au point fixe du script, Div_F/(Div_F + FU) | fraction | résultat des entreprises après intérêts et impôt, Div_F + FU | 12 tours |
| Capital au prix courant (B12, `tab:criteres-j3`) | p K^vol/(12 PIB) | années de PIB | PIB nominal sur 12 tours | ouverture |
| x | K^vol/(n_a y) = (κ/t̄u) e^{−ζΔϱ} | années de production | production | état stationnaire |
| ζ (S2) | élasticité de niveau de tu\* à Δϱ, donc d ln x/dϱ = −ζ à long terme | sans dimension, par unité de taux réel annuel | — | — |

**Traits du modèle que la source doit respecter** (vérifiés sur `etat_stationnaire`, l. 375 à 452 à `708c1aa`) :

| Trait | Dans le modèle | Conséquence pour la source |
|---|---|---|
| Secteur | Un seul secteur des entreprises, consolidé (J = 1). Il ne détient pas d'actions et ne reçoit aucun dividende. | Sociétés non financières (S11), avec les **dividendes versés nets des dividendes reçus** (D.42), pour approcher un secteur consolidé |
| Profits non distribués | FU = γ̄ V_F, après intérêts, amortissement comptable δK/n_a et impôt τ_F (nul au socle) | Épargne nette B.8n de S11. Écart déclaré : B.8n est nette de la consommation de capital fixe **au coût de remplacement**, alors que le modèle amortit au coût historique |
| Capital | K^vol, net (amortissement géométrique δ), valorisé au prix courant p, donc au coût de remplacement. Pas de logements. Les entreprises produisent toute la valeur ajoutée, l'État n'a pas de capital. | Actifs fixes nets **hors logements**, au coût de remplacement courant, **économie totale** (même choix de champ qu'au § 1) |
| Dénominateur de B12 | PIB = p v + ΔIN, sans impôts sur la production ni loyers imputés | PIB aux prix du marché, avec en variante la valeur ajoutée au prix de base. Les loyers imputés ne sont pas retirés : écart déclaré |

**ζ n'entre pas dans l'état stationnaire de référence** (Δϱ = 0). Grille complète du script à μ̄ = 0,60 : le plus grand écart relatif entre ζ = 4 et ζ ∈ {5 ; 6 ; 6,28 ; 8 ; 8,79 ; 10 ; 12,56 ; 17 ; 20} vaut **0** (sortie `sortie_s55.txt`). ζ n'agit que hors de l'état stationnaire, et dans la mesure (α) de #80, où Δϱ ≠ 0. **Vérifiée.**

**Correspondance entre ζ et la littérature** (fiche 6, § 9.2). En CES, ln(K/Y) = cte − σ ln c, où c = (ϱ + δ) est le coût d'usage réel et σ l'élasticité du rapport capital-production à ce coût. Il en découle d ln(K/Y)/dϱ = −σ/(ϱ̄_L + δ), d'où **ζ = σ/(ϱ̄_L + δ)**. À δ = 0,05 (hypothèse, #164) et ϱ̄_L = 0,030 / 0,029608 / 0,028182 (π̄ = 0 / 2 / 10 %), ζ = 8 correspond à σ = 0,640 / 0,637 / 0,625, et ζ = 4 à σ = 0,320 / 0,318 / 0,313. **Hypothèse** de correspondance, sous deux conditions :
- (i) tout le coût du capital suit ϱ_L. Si seule la part financée par crédit (lv\* = 0,4) le suivait, ζ serait multiplié par 0,4 ;
- (ii) δ vaut 5 %. À δ = 8 % ou 10 %, ζ serait plus bas de 27 % ou 39 % (σ = 0,7 donnerait ζ = 6,39 ou 5,40 au lieu de 8,79).

### 3.2 Sources lues et citées

**(a) Taux de distribution, lu.** Eurostat, comptes annuels des secteurs, jeu `nasa_10_nf_tr` (« Non-financial transactions - annual data »), mise à jour du 29/10/2026. Requête de l'API de diffusion (`ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data`) : S11, millions d'euros courants, D.42 versé et reçu, B.8n. Consultée le 16/11/2026. Zone euro à 21 pays (EA21 ; la requête ne rend pas d’agrégat EA20 pour ce jeu).

| Définition | Moyenne 1999–2023 (25 ans) | Minimum ; maximum | Moyenne 2010–2024 | UE à 27, 1999–2023 |
|---|---|---|---|---|
| **Nette** : (D.42 versé − D.42 reçu)/(D.42 versé − D.42 reçu + B.8n) | **0,790** | 0,607 (2021) ; 0,986 (2000) | 0,717 | 0,715 |
| Brute : D.42 versé/(D.42 versé + B.8n) | 0,860 | 0,729 (2021) ; 0,990 (2000) | 0,814 | 0,807 |

Faits, **vérifiés** (requête et calcul, scratchpad `dl55/`). Non corrigé : bénéfices réinvestis d'investissement direct (D.43), revenus de la propriété attribués (D.44, D.45). Ces postes déplacent le partage, et leur ampleur n'est **pas vérifiée**.

**(b) Capital productif, lu.** Eurostat, `nama_10_nfa_st` (« Fixed assets by type of asset »), mise à jour du 14/11/2026 : coût de remplacement courant (`CRC_MEUR`), branches totales, actifs fixes nets N11N moins logements nets N111N, EA20. PIB : `nama_10_gdp`, B1GQ et B1G, prix courants. Consultés le 16/11/2026.

| Rapport | Moyenne 2000–2023 (24 ans) | Minimum ; maximum |
|---|---|---|
| **Capital net hors logements / PIB aux prix du marché** | **1,676 an** | 1,595 (2001) ; 1,772 (2020) |
| Même capital / valeur ajoutée brute au prix de base | 1,871 an | — |
| Pour mémoire : capital net total, logements compris / PIB | 3,229 ans | — |

Répartition par secteur, de `nama_10_nfa_bs` (prix courants, publiée depuis 2012), capital net hors logements sur PIB en 2019 :
- sociétés non financières, 0,989 ;
- administrations publiques, 0,493 ;
- ménages et ISBLSM, 0,137 ;
- sociétés financières, 0,043.

Le total, 1,662, est égal à celui de `nama_10_nfa_st`. Faits, **vérifiés**.

**(c) ζ : élasticité du capital au coût d'usage, lue.**
- R. Klump, P. McAdam et A. Willman, « The normalized CES production function: theory and empirics », BCE, *Working Paper Series*, n° 1294, février 2011. Tableau 2, « Empirical Studies of Aggregate Elasticity of Substitution in Selected Other Countries », page 30 du document (page 31 du PDF) :
  - zone euro : 0,7 (Klump et al. 2007b, 1970–2003, trimestriel, progrès technique augmentant les facteurs) ; 0,95–1,05 (Willman 2002, 1970–1997, neutre au sens de Solow) ;
  - estimations par pays de Bolt et van Els (2000), 1971–1996 : de 0,24 (Autriche) à 1 (Espagne).

  Section 6, conclusions : les données rejettent la Cobb-Douglas au profit d'une CES d'élasticité « generally below unity ». Lu le 16/11/2026, PDF de `www.ecb.europa.eu`. **Vérifiée.** Ce sont des élasticités de substitution σ. Leur lecture comme élasticité de K/Y au coût d'usage est l'hypothèse du § 3.1.
- S. Gilchrist et E. Zakrajšek, « Investment and the Cost of Capital: New Evidence from the Corporate Bond Market », NBER *Working Paper* 13174, juin 2007. Données de firmes américaines émettrices d'obligations.
  - Résumé : une hausse d'un point du coût d'usage réduit le taux d'investissement de 50 à 75 points de base.
  - Page 21 : « The elasticity of capital with respect to the user cost is equal to unity in the long run ». Même page : le taux d'intérêt après impôt représente environ les deux tiers du coût d'usage.

  Lu le 16/11/2026, PDF de `www.nber.org`. **Vérifiée.**
- B. Coulibaly et J. N. Millar, « The 'Elusive' Capital-User Cost Elasticity Revisited », Réserve fédérale, *Finance and Economics Discussion Series* 2007-25. Panel de 24 branches manufacturières sud-africaines, 1970–2000. Élasticité de long terme « between -0.80 and -1.0 » (conclusions). Lu le 16/11/2026 par WebFetch, qui ne rend qu'une citation courte et un résumé : **vérifiée avec réserve**.
- **Non lus** : R. S. Chirinko, S. M. Fazzari et A. P. Meyer (1999), *Journal of Public Economics* 74(1), cité par la fiche 6 ; S. Gechert et al. (2022), *Review of Economic Dynamics* ; Knoblach, Rössler et Zwerschke (méta-régression). Aucun chiffre n'en est tiré.

**Fourchette lue.** σ (ou élasticité du capital au coût d'usage) de 0,5 à 1,0 pour la zone euro et pour les études de firmes. Valeurs nationales jusqu'à 0,24. Conversion du § 3.1 à π̄ = 2 % : **ζ de 6,3 à 12,6**, et 4,0 pour σ = 0,32. Sous la condition (i) restreinte au crédit : ζ de 2,5 à 5,0. Le niveau de σ est **contesté** : la conclusion de Klump et al. (« below unity ») et celle de Gilchrist et Zakrajšek (« unity ») divergent.

**(d) Pour #164, lu au passage.** Mêmes jeux, EA21, moyenne 2000–2023 : D.42 versé par S11, 9,39 % du PIB ; net des D.42 reçus, 5,68 % du PIB. Le modèle verse 22,31 % du PIB en dividendes à μ̄ = 0,60 (§ 1.6). L'écart confirme la limite P214. Il relève de #164, pas de #55. **Vérifiée** (mesure de la source).

### 3.3 Valeur proposée et variantes

**Capital : κ inchangé (x = 2 ans).** B12 vaut 1,99887 an à π̄ = 2 %. C'est +19,3 % au-dessus de la source rapportée au PIB (1,676) et +6,8 % au-dessus de la source rapportée à la valeur ajoutée (1,871). Écart **déclaré**, pour trois motifs :
- **Bande de #55.** Caler x sur 1,676 porterait la distribution à **0,9087** à π̄ = 0, hors de la bande (sortie `sortie_s55.txt` : 0,9087 / 0,8590 / 0,7649 à π̄ = 0 / 2 / 10 %). La bande est franchie dès x < 1,806 à π̄ = 0 (distribution 0,9000). **Vérifiée.**
- **Dénominateur.** Le PIB observé contient des impôts sur les produits et des loyers imputés, que le modèle n'a pas. La valeur ajoutée au prix de base (1,871) est plus proche du concept du modèle.
- **Calibration conjointe.** κ et δ se calibrent ensemble sur la consommation de capital fixe (#164). Recaler κ seul avant δ ferait deux changements successifs de l'état de référence.

**Distribution : aucune valeur à caler.** C'est un résultat de μ̄ (#92), de x, de lv\* et des écarts de #130. À μ̄ = 0,60, elle vaut 0,886 / 0,828 / 0,724. À π̄ = 2 %, le modèle (0,828) tombe entre la source nette (0,790) et la source brute (0,860), donc dans la plage observée de 1999 à 2023 (0,607 à 0,986). **Vérifiée.**

**ζ proposé : 8.** C'est une valeur ronde, qui équivaut à σ ≈ 0,64 sous la correspondance du § 3.1. Elle se trouve dans la fourchette lue, entre l'estimation de la zone euro de Klump et al. (0,7) et la borne basse de 0,5. Elle figure déjà dans le script, comme second point de la plage de sensibilité (`ZETA_PLAGE` = (4 ; 8)), et dans les valeurs publiées à ζ = 8 (§ 3.6). Statut : **choix déclaré, source lue, niveau contesté**.

| Variante | ζ | σ équivalent (2 %) | Distribution sous −2 points, 0 / 2 / 10 % | Δϱ où la distribution atteint 0,9, π̄ = 0 | Δϱ_lim de S6 | Rayon de la maquette, φ = 0, π̄ = 2 % | Δr̄_α (#80) | Avis |
|---|---|---|---|---|---|---|---|---|
| V0, statu quo | 4 | 0,318 | 0,8798 / 0,8169 / 0,7056 | +4,26 points | 3,308 | 1,001818 | 0,632 point | Sous la fourchette de la zone euro ; garde les valeurs publiées de C62 |
| V2 | 6 | 0,478 | 0,8733 / 0,8079 / 0,6938 | +2,34 points | 2,205 | 1,000125 | non relevé | Borne basse de la fourchette |
| **V1, proposée** | **8** | **0,637** | **0,8662 / 0,7981 / 0,6811** | **+1,61 point** | **1,654** | **1,000035** | **0,297 point** | **Recommandée** |
| V1′ | 8,79 | 0,70 | 0,8633 / 0,7941 / 0,6759 | +1,43 point | 1,505 | non relevé | 0,266 point | Égalité à σ = 0,7 ; précision illusoire |
| V3, Cobb-Douglas | 12,56 | 1,0 | 0,8478 / 0,7729 / 0,6491 | +0,94 point | 1,053 | 0,999818 | 0,175 point | Haut de la fourchette ; borne haute de la distribution franchie dès +0,94 point à π̄ = 0 |
| V4, lecture « crédit seul » | ≈ 3,5 | 0,7 × 0,4 | non mesurée | non mesurée | 3,78 | non mesuré | non relevé | Écartée : S2 ne lit que ϱ_L, mais le coût des fonds propres n'est pas modélisé, ce qui ne prouve pas qu'il soit fixe |

Mesures : sorties `sortie_s55.txt` et `sortie_maq.txt`. Δϱ_lim = 13,231/ζ (§ 2.3.2). **Vérifiées.**

### 3.4 Tableau avant / après prédit

#### 3.4.1 Méthode et commandes

Sondes du scratchpad, lancées depuis `/home/user/projet_macro` à `708c1aa` (`git status` vide avant et après), dossier `<scratchpad>/sondes55/` :
- **`s55.py`** : appelle `calculer(replace(Parametres(), mu_bar=0.60, zeta=z))` pour dix valeurs de ζ et compare chaque valeur publiée (champ `script`) et toute la grille à ζ = 4. La distribution sous Δϱ = −2 points se calcule par `etat_stationnaire(par, r_neutre=r̄ − 0,02, rho_bar_L=norme, controler=False)`, comme `test_distribution_positive_sous_un_ecart_de_taux_de_moins_deux_points`. Les seuils en Δϱ s'obtiennent par bissection. Elle traite aussi la variante κ.
- **`main2.py`** : distribution à Δϱ = 0 et −2 points pour (μ̄, ζ) = (0,25 ; 4), (0,60 ; 4) et (0,60 ; 8).
- **`bas.py`** : côté baisse, de Δϱ = −2 à −30 points.
- **`c62z.py`** : `test_temps_de_doublement_sous_phi_nul` rejoué, choc de 1 %, 720 pas. Assistants du test non modifiés ; sentier et tables à (μ̄, ζ) par `socle.sentier(pi, mu_bar=…, zeta=…)` et `varier`, comme la sonde `c62.py` de `monnaie`.
- **`c62lin.py`** : `test_temps_de_doublement_en_regime_lineaire` rejoué, choc de 1e−6, 2 700 pas, fenêtres de 120 pas.
- **`maq.py`** : `rayon_c` de `outils/maquette_conjointe.py` sous φ = 0.
- **`durable8.py`** : sonde `durable2.py` de `monnaie` (§ 2.4.2) à ζ = 8.
- **Contrôles.** À ζ = 4, les sondes retrouvent les valeurs publiées : 320 et 31 tours, arrêt au pas 523 ; ρ̂ = 1,001819 ; rayons 1,001818 et 1,011036 ; distributions de main 0,61710 / 0,50480 / 0,36359.
- Commande type : `uv run python -I <scratchpad>/sondes55/<sonde>.py`. Sorties : `<scratchpad>/sondes55/sortie_*.txt`.

#### 3.4.2 `tab:etat-stationnaire` et valeurs résolues B1 à B26

- **Contre l'état à μ̄ = 0,60 (§ 1) : aucune ligne ne change**, à toutes les décimales. Plus grand écart relatif sur toute la grille : 0. Ni ζ, ni κ inchangé n'entrent à Δϱ = 0. **Vérifiée.**
- **Contre `main`** : le tableau est celui du § 1.4, sans ligne de plus. Tout le changement de l'état stationnaire de référence vient de #92.

#### 3.4.3 Valeurs publiées du script qui changent avec ζ (μ̄ = 0,60 ; ζ = 4 → 8)

185 valeurs publiées sur 449 sont en écart, contre 173 au § 1. Les douze en plus viennent toutes de la mesure (α) de #80 :

| Endroit | Grandeur | ζ = 4 (main et § 1) | ζ = 8 |
|---|---|---|---|
| `sec:banque_centrale-conditions` ; fiche 9 § 3.Q | r̄_α à π\* = 0 / 1 / 3 / 4 / 6 / 10 %, % | 1,632 / 1,264 / 0,818 / 0,706 / 0,656 / 1,146 | 1,297 / 1,122 / 0,919 / 0,872 / 0,865 / 1,144 |
| `sec:banque_centrale-conditions` | r̄_α(0) − r̄_α(10 %), point | 0,486 | 0,152 |
| idem | écart maximal de r̄_α sur le profil, point | 0,976 | 0,432 |
| idem | marche de cible de 2 à 3 %, point | −0,18 | −0,081 |
| idem | Δr̄_α, verdict, point (le libellé « (ζ = 4) » est à reprendre) | 0,632 | 0,297 |
| idem | (α) : écart de C/Y_o, point | 0,633 | 0,631 |
| idem | (α) : écart de ti, point | 0,186 | 0,278 |

Explication commune : sous la lecture (α), la cible change et Δϱ ≠ 0 entre deux cibles. Un ζ plus élevé fait porter davantage de l'ajustement par x, et moins par r̄_α. Quatre autres valeurs bougent à 1e−13 près sans changer à l'arrondi publié : écart de tu et trois lignes C/PIB de la fiche 9.

**#80 reste en échec attendu** : Δr̄_α = 0,297 point et écart de C/Y_o = 0,631 point, au-dessus du seuil de 0,1 point des deux tests `xfail(strict=True)`. Aucun succès inattendu. **Vérifiée** (valeurs du script ; tests non exécutés à ζ = 8).

**C51 « à ζ calibré »** (P161) : `calculer` ne lève aucun refus à ζ = 8 (ni à 5, 6, 6,28, 8,79, 10, 12,56, 17 ou 20). La racine de la fonction de fermeture est donc unique sur [−60 % ; 100 %], sans pôle, et les trois « racines parasites » restent « aucune ». **Vérifiée sous φ = 1.** Sous φ = 0, la publication des racines n'est **pas mesurée**.

#### 3.4.4 Lignes propres à #55 et à C62

| Grandeur | `main` (μ̄ = 0,25, ζ = 4) | § 1 (μ̄ = 0,60, ζ = 4) | Proposé (μ̄ = 0,60, ζ = 8) | Explication |
|---|---|---|---|---|
| Distribution, Δϱ = 0, π̄ = 0 / 2 / 10 % | 0,61710 / 0,50480 / 0,36359 | 0,88598 / 0,82751 / 0,72390 | identique au § 1 | #92 ; ζ n'entre pas |
| Distribution, Δϱ = −2 points | 0,60988 / 0,47950 / 0,31459 | 0,87983 / 0,81694 / 0,70560 | **0,86624 / 0,79812 / 0,68114** | x = 2 e^{0,02ζ} : 2,1666 → 2,3470. Plus de capital, donc plus d'amortissement et de V_F à faire croître |
| Div_F/(p v) sous −2 points, % | 4,84 / 4,66 / 4,29 | 22,38 / 22,20 / 21,83 | 21,19 / 20,99 / 20,58 | idem |
| tu sous −2 points | 0,7385 | 0,7385 | 0,6817 | S2 |
| Frontière de S6, Δϱ_lim, par an | 3,307756 | 3,307756 | **1,653878** | c/ζ, avec c = 13,231 (§ 2.3.2) |
| Arrêt liant du pas 0, π̄ = 2 % : i_{L,0} et cause | 3,252184, caisse | 3,424111, S6 | **1,737155, S6** (déduite) | ζ = 8 > ζ\* aux trois π̄ (§ 2.3.3) ; non remesurée par bissection |
| C62, choc de 1 %, π̄ = 2 % : ρ̂ et temps de doublement | 320 tours (publié) | 1,002170 ; 320 tours | **0,997465 ; aucun doublement**, pas d'arrêt | voir ci-dessous |
| C62, choc de 1 %, π̄ = 10 % | 31 tours, arrêt au pas 523 | 1,022593 ; 31 tours ; arrêt au pas 523 | 1,019156 ; 37 tours ; arrêt au pas 543 | idem |
| C62 en régime linéaire, π̄ = 2 %, trois dernières fenêtres | 381 tours (publié) | 1,001819 (381 tours) | **0,999746 / 0,998568 / 0,996747** | idem |
| C62 en régime linéaire, π̄ = 10 % | 63 tours (publié) | 1,011219 / 1,011744 / 1,014105 ; arrêt au pas 1 362 | 1,010274 / 1,011828 / 1,022700 ; arrêt au pas 1 500 | idem |
| Rayon de la maquette conjointe, φ = 0, π̄ = 0 / 2 / 10 % | 0,997894 / 1,001818 / 1,011036 | identique | **0,998235 / 1,000035 / 1,009661** | idem |

**C62 change de nature à π̄ = 2 %** (vérifiée).
- **À ζ = 8, la boucle sous φ = 0 n'est plus explosive à l'échelle d'une partie.** Le rayon de la maquette, 1,000035, donne un temps de doublement de l'ordre de 20 000 tours. Le moteur, en régime linéaire, converge sur 2 700 pas.
- **Elle reste explosive à 10 %.** Rayon 1,009661 ; arrêt du choc de 1 % au pas 543 au lieu de 523.
- **Le canal.** ζ renforce le canal de l'investissement : une hausse durable du taux réduit x et la demande. Ce frein compense le canal rentier, qui pousse vers l'explosion sous φ = 0. Ce mécanisme est une **hypothèse**, non décomposée.
- **Ce qui est à réécrire.** Les phrases publiées « la boucle conjointe est explosive » sous φ = 0 (`sec:finances_publiques-impots`, `sec:finances_publiques-conditions`) et « 381 tours ». La couverture minimale qui stabilise, 0,174 à 2 %, est à remesurer : **non mesurée**.
- μ̄ n'a aucun effet sur ces mesures : rayons identiques à μ̄ = 0,25 et 0,60.

### 3.5 Critère de #55 (écrit avant l'essai)

| Point | π̄ = 0 | π̄ = 2 % | π̄ = 10 % | Verdict |
|---|---|---|---|---|
| Distribution dans [0,2 ; 0,9], Δϱ = 0 | 0,88598 | 0,82751 | 0,72390 | **tenu** ; marge haute de 0,014 à π̄ = 0 |
| Même bande, Δϱ = −2 points (taux directeur, écarts constants, M33), ζ = 8 | 0,86624 | 0,79812 | 0,68114 | **tenu** |
| B12 rapporté à une source de capital productif au coût de remplacement, définition déclarée | 2,0017 contre 1,676 | 1,9989 contre 1,676 (1,871 sur la valeur ajoutée) | 1,9882 | **rapporté** ; écart de +19 % (PIB) ou +7 % (valeur ajoutée), déclaré (§ 3.3) |
| ζ sur une source, ou déclaré | ζ = 8, σ ≈ 0,64, dans la fourchette lue de 0,5 à 1,0 | | | **sourcé, contesté** |
| Publiés : C51 « à ζ calibré », frontière de #143 au ζ retenu | racine unique (φ = 1) ; Δϱ_lim = 1,654 par an | | | **publiés** |

Le critère tient à **tout ζ ≤ 20** mesuré. Sous −2 points, la plus basse valeur est 0,5848, à ζ = 20 et π̄ = 10 %. Le critère ne départage donc pas les variantes. **Vérifiée.**

### 3.6 Points repris du § 2.6

1. **Frontière de #143 au ζ retenu.** À ζ = 8, Δϱ_lim = 1,653878 par an, soit i_L = 1,683878 / 1,737155 / 1,950266 à π̄ = 0 / 2 / 10 %. C'est la mesure de `monnaie`, § 2.3.2, faite à ζ = 8 ; **vérifiée**. Comme ζ = 8 dépasse ζ\* (4,890 / 3,875 / 2,247), **S6 lie la première au pas 0 aux trois π̄**, avant les seuils de caisse (2,735863 / 3,533060 / 6,609380). C'est une **déduction** des § 2.3.2 et 2.3.3, non remesurée par bissection à ζ = 8 : le seuil de caisse du pas 0 ne lit pas ζ, puisque S2 n'entre qu'à ti_{t+1}.
2. **C51 et C62.** C51 tient à ζ = 8 (§ 3.4.3). C62 : § 3.4.4. **Constat principal de cette section** : à 2 %, le régime « intérêts financés par le déficit » cesse d'être explosif sur l'horizon d'une partie.
3. **Borne haute de la distribution.** Mesure directe, qui remplace l'hypothèse x = 2 e^{−ζΔϱ} du § 2.4.3 : à ζ = 8, la distribution atteint 0,9 pour un Δϱ durable de **+1,61 / +7,15 / +19,33 points** à π̄ = 0 / 2 / 10 % (ζΔϱ = 0,129 / 0,572 / 1,547, contre 0,102 / 0,523 / 1,698 dans l'hypothèse). Ce n'est pas une condition d'existence : Div_F reste positif. La bande de #55 est un critère de calibration à l'état de référence, pas un domaine. À π̄ = 0, un resserrement durable de 1,6 point suffit à la franchir, contre 4,3 points à ζ = 4. **Vérifiée.**
4. **Économie vidée d'investissement.** Sonde de `monnaie` à ζ = 8, μ̄ = 0,60 :
   - aucun arrêt, sauf à π̄ = 0 sous +20 points : arrêt de la **caisse de l'État** au pas 364 (30,3 ans), phase 7, ligne 19a-banque, contre le pas 479 à ζ = 4 ;
   - ti multiplié par 0,93 / 0,82 / 0,64 / 0,33 à π̄ = 0 sous +2 / +5 / +10 / +20 points ; par 0,275 et 0,249 à 2 % et 10 % sous +20 points ;
   - rien de comparable aux facteurs de 10⁻⁶ à 10⁻⁹ mesurés à ζ = 20.

   Avis : **la borne ζ ≤ 20 (P139) n'a pas à être resserrée dans cette branche**. ζ = 8 en est loin. c_dom de (1′) se fixe en J3-e2 avec ζ = 8 : sous l'hypothèse de `monnaie` (c_dom de 0,5 à 1), Δϱ admis de 6,3 à 12,5 points. **Vérifiée** (sortie `sortie_durable8.txt`), sauf c_dom (**hypothèse**).
5. **Côté baisse.** À ζ = 8, la distribution reste au-dessus de 0,2 pour tout Δϱ ≥ −10 points aux trois π̄ (0,778 / 0,647 / 0,416 à −10 points). À π̄ = 10 %, elle descend à 0,174 à −15 points, puis Div_F < 0 à −20 points (i_L = −8,9 %, hors de tout domaine réaliste). À π̄ = 0 et 2 %, Div_F ne s'annule pas jusqu'à −30 points : la baisse des intérêts domine la hausse de x, et la distribution n'est pas monotone. L'hypothèse du § 2.4.3, « Div_F = 0 à ζΔϱ ≈ −0,93 », est donc **réfutée** à π̄ = 0 et 2 %. **Vérifiée** (sortie de `bas.py`).
6. **Arrêts de la caisse de l'État** (frontière avec `monnaie`). Ils surviennent plus tôt à ζ = 8 (pas 364 contre 479, π̄ = 0, +20 points). Je partage l'avis de `monnaie` : diagnostic en J3-f2 (#87, #154) ou au J4, hors de cette branche. Mécanisme **non diagnostiqué**.

### 3.7 Conditions d'existence au point fixe

ζ n'entre pas à Δϱ = 0, et κ est inchangé : toutes les conditions du § 1.5 sont **identiques** à μ̄ = 0,60. Il s'agit de Div_F > 0, du dividende stationnaire de la banque, du coefficient de richesse, de ν_H λ_H < 1, de D1, D2, de la marge de E1, du plafond de E6 et de la caisse de phase 4. Le domaine de ζ (ζ ≥ 0, ζ ≤ 20 selon P139) est tenu. **Vérifiée** (grille identique ; `calculer` sans refus).

**Conditions d'arrêt du plan** : aucune rencontrée.
- Aucune valeur n'est hors domaine et aucune équation n'est à changer.
- Aucun banc d'empreintes n'a été exécuté : c'est la mesure du rang 8. Les trajectoires choquées changeront avec ζ, puisque Δϱ ≠ 0 hors de l'état stationnaire, et le maintien du plafond des bancs D et BF n'est **pas vérifié**.
- Le seul cas connu qui atteint la frontière de #143 (C62 à 10 %) s'arrête plus tard à ζ = 8 (pas 543 au lieu de 523).

### 3.8 Questions au mainteneur

1. **Valeur de ζ.** ζ = 8 (σ ≈ 0,64 ; source lue, niveau contesté), ζ = 4 (statu quo, σ ≈ 0,32, sous la fourchette de la zone euro lue), ou ζ = 12,56 (Cobb-Douglas) ? *Avis : **ζ = 8**, déclaré « σ ≈ 0,64 ; Klump, McAdam et Willman (2011) et Gilchrist et Zakrajšek (2007) ; correspondance ζ = σ/(ϱ̄_L + δ), contestée ».*
2. **Changement de C62 à 2 %.** À ζ = 8, le régime φ = 0 n'est plus explosif à π̄ = 2 % sur l'horizon d'une partie : rayon de 1,000035, contre 1,001818 à ζ = 4. Il reste explosif à 10 %. Ce changement d'un résultat publié (sans verdict) suit de ζ. Faut-il l'accepter, avec réécriture de `sec:finances_publiques-impots` et remesure de la couverture minimale qui stabilise ? Faut-il plutôt garder ζ = 4 pour préserver la propriété ? *Avis : l'accepter. La propriété « explosif à 2 % » reposait sur un ζ indicatif sans source, et elle reste vraie à 10 %. C'est une frontière avec `monnaie` (dette publique) et un point pour `jeu` (§ 3.9).*
3. **Capital.** Garder κ = 1,6 (x = 2, B12 = 2,0 an) avec l'écart déclaré à la source (+19 % sur le PIB, +7 % sur la valeur ajoutée), et renvoyer le calage conjoint de κ et δ à #164 ? *Avis : oui. Caler x = 1,676 seul ferait sortir la distribution de la bande à π̄ = 0 (0,9087).*
4. **Définition de la distribution observée.** Nette des dividendes reçus (0,790, EA21, 1999–2023), ou brute (0,860) ? *Avis : nette, puisque le secteur du modèle est consolidé ; publiée avec la brute.*
5. **Dividendes rapportés au PIB** (§ 3.2 (d)) : 5,68 % net observé, contre 22,31 % dans le modèle. *Avis : le verser en commentaire sur #164 (texte au § 3.10), sans effet sur cette branche.*

### 3.9 Points pour `jeu` (je ne les tranche pas)

- À ζ = 8, un point de taux réel du crédit maintenu pèse davantage sur l'investissement à long terme : e^{−0,08} − 1 = −7,7 % de capital par point durable, contre −3,9 % à ζ = 4. Le libellé « −2 % d'investissement par point, davantage s'il dure » (fiche 6, condition 2) reste juste. Son chiffre est à recalculer après M34.
- Sous φ = 0 à 2 %, le joueur ne voit plus de dérive lente du taux directeur. Elle reste visible à 10 % (arrêt après 45 ans environ au choc de 1 %). La leçon « financer les intérêts par le déficit est explosif » ne vaut plus qu'à inflation élevée.
- À π̄ = 0, un resserrement durable de 1,6 point fait passer la distribution au-dessus de 0,9. Cette mesure de répartition est sans conséquence de domaine.

### 3.10 Commentaire proposé sur #164 (création sur accord)

> *Rédigé par l'agent macro (IA).*
>
> Mesures lues pendant l'instruction de #55 (`docs/blocs/calibration.md`, § 3.2), Eurostat, consultées le 16/11/2026 :
> - capital net hors logements au coût de remplacement courant (`nama_10_nfa_st`, EA20) : 1,676 an de PIB en moyenne de 2000 à 2023 (1,871 an de valeur ajoutée au prix de base) ;
> - dividendes versés par les sociétés non financières (`nasa_10_nf_tr`, D.42, EA21) : 9,39 % du PIB, ou 5,68 % nets des dividendes reçus.
>
> Le modèle donne, à μ̄ = 0,60 : B12 = 2,0 ans et des dividendes de 22,3 % du PIB. Recaler κ et δ ensemble sur la consommation de capital fixe réduirait l'écart. Le faire avec κ seul ferait sortir la distribution de la bande de #55 à π̄ = 0 (0,909 à x = 1,676).

### 3.11 Surface pour `coder` et `docwriter` (rang 3 à 9)

- Table du bloc 6 (`ZETA`) : valeur 8 et source. Défaut `zeta` du script et sa déclaration, aujourd'hui « valeur de la maquette… n'entre que si Δϱ ≠ 0 ».
- `ZETA_PLAGE` = (4 ; 8) : la valeur retenue y figure déjà. Le libellé « Δr̄_α, verdict (ζ = 4) » est à reprendre.
- Les douze valeurs publiées du § 3.4.3.
- 21 occurrences de « ζ = 4 » dans la spécification, dans dix sections au moins : `sec:banque_centrale-conditions`, `sec:finances_publiques-*`, `sec:cadre-*`, `sec:banque-*`, `sec:investissement-conditions`, et d'autres. Il faut aussi reprendre les textes publiés de C62 (320, 31, 381 et 63 tours).
- Chiffres de la fiche 6 donnés à ζ = 4, à remesurer au rang 8 : e_I(120), (d2), tu et x hors cible durable (1,098 et 1,457 à ζ = 4 ; 1,508 et 1,061 à ζ = 8, chiffres de maquette non remesurés).

### 3.12 Statut des conclusions

- **Vérifiées** (commande et sortie, ou source citée) :
  - ζ sans effet sur l'état stationnaire (grille identique) ;
  - critère de #55 aux trois π̄ et sous −2 points ;
  - les douze valeurs publiées qui changent ; #80 toujours en échec ;
  - C51 sous φ = 1 ;
  - C62 (choc de 1 %, régime linéaire, maquette) à ζ = 4 et 8 ;
  - borne haute et côté baisse ;
  - sonde d'écart durable à ζ = 8 ;
  - variante κ (0,9087) ;
  - sources Eurostat (distribution, capital, dividendes) ;
  - Klump et al. (tableau 2) et Gilchrist et Zakrajšek (p. 21).
- **Vérifiée avec réserve** : Coulibaly et Millar (résumé de l'outil).
- **Hypothèses** :
  - correspondance ζ = σ/(ϱ̄_L + δ), et lecture de σ comme élasticité du capital au coût d'usage ;
  - mécanisme du changement de C62 ;
  - c_dom.
- **Déduite** : frontière liante du pas 0 à ζ = 8.
- **Non vérifiées** :
  - bancs d'empreintes à ζ = 8 (rang 8) ;
  - couverture minimale qui stabilise sous φ = 0 ;
  - racines sous φ = 0 ;
  - postes D.43 à D.45 ;
  - millésime d'AMECO (§ 1.12) ;
  - Chirinko, Fazzari et Meyer (1999).

### 3.13 Remesures de C62 à ζ = 8 (avant M34)

*Instruite par `macro` (expert pilote) le 16/11/2026, sur la demande du mainteneur (P219) et les quatre mesures demandées par `monnaie` (§ 3.14). Dépôt à `2f5641a`, puis `3da48c0` (commit `docs:` seul, sans effet sur les mesures), `git status` vide avant et après. Les sondes sont hors dépôt (`<scratchpad>/sondes62/`). Elles appellent sans les modifier `outils/maquette_conjointe.py`, `outils/etat_stationnaire.py`, `tests/invariants/socle_partiel.py` et les assistants de `tests/invariants/test_socle_complet.py`. Ce sont des résultats du modèle, pas des faits. Base : μ̄ = 0,60 (P213) ; ζ = 4 sert de contrôle. Chaque conclusion est marquée **vérifiée**, **hypothèse** ou **non vérifiée**.*

#### 3.13.1 Méthode et commandes

Commande type : `uv run python -I <scratchpad>/sondes62/<sonde>.py <arguments>`, lancée depuis `/home/user/projet_macro`. Sorties : `<scratchpad>/sondes62/sortie_*.txt`.

- **`regimes.py`** et **`grille_zeta.py`** : racines de la lecture (c) de la maquette sous φ = 0, pour chaque régime de T4 et sur une grille de ζ. Elles viennent de `jacobiennes_carte` et `lectures`, restreintes à la variété des identités, sans la racine nominale ni les racines en 1/Γ̄.
- **`serie.py MU ZETA PI N F PHI SORTIE`** : série **signée** Δi_CB (choqué moins contrôle) du moteur, selon le protocole des deux tests C62 : choc θ_G × (1 + F) aux tours 1 à 12, contrôle apparié, φ = 0, `bloc_9_compose` et `choc_de_theta_G`. Seule la longueur change : jusqu'à 12 000 pas. Le relevé ne garde que les variables du pas. Durée : 13 s pour 12 000 pas.
- **`analyse.py SERIE DEBUT ORDRE [FIN]`** : changements de signe et crêtes de chaque demi-cycle, puis identification de la racine dominante par **prédiction linéaire (méthode de Prony)**. La série x_t = Σ_j a_j x_{t−j} est ajustée par moindres carrés sur [DEBUT ; FIN[ ; les racines viennent du polynôme caractéristique. C'est le « jacobien du moteur » demandé, sous sa forme sans différences finies : la racine dominante de la réponse linéaire du moteur.
- **`zeta_c.py`** : ζ_c par `frontiere`, la bissection de la maquette (40 itérations). Elle donne aussi ζ_f, où une racine réelle vaut 1, par bissection sur le signe de (1 − λ₁)(1 − λ₂), et la coalescence des deux racines réelles.
- **`phi_star.py`** et **`phi_grille.py`** : φ\* par `frontiere` sur [0 ; 1], comme `phi_star` du script, et grille de φ pour vérifier qu'une seule traversée a lieu.
- **`racines_phi0.py`** : racines de la lecture (α) sous φ = 0, par `resoudre_alpha` et `racines_balayage`, θ_G visé inchangé ou réduit de 5 % (#88), avec dθ_G/dr̄ à chaque racine (différence centrée, h = 1e−5). C'est le calcul de la ligne (b) de C51, que C62 cite.
- **`pli.py`** : à π̄ donné, compare le ζ où dθ_G/dr̄ s'annule au point de référence (script) au ζ où une racine réelle de la maquette vaut 1.
- **`option.py`** : vecteur propre de la racine dominante, plan 2 × 2.

**Contrôles.** Sous ζ = 4, les sondes retrouvent les valeurs publiées :
- rayons 1,001818 et 1,011036 ;
- φ\* = 0,1741 et 0,6495 (`phi_star` du script : 0,1741 / 0,6495) ;
- racines sous φ = 0 : −0,347 % et 1,000 % à 2 %, −11,017 % et 0,920 % à 10 %, pentes de +0,034, −0,034, +0,302 et −0,267, valeurs de la ligne (b) de C51 (`sec:finances_publiques-conditions`), à μ̄ = 0,25 comme à 0,60 ;
- racine dominante du moteur (Prony) : 1,0018181, contre 1,001818 pour la maquette.

#### 3.13.2 Mesure 1 : l'écart entre maquette et moteur vient de l'estimateur

**La racine dominante change de nature entre ζ = 4 et ζ = 8.** Racines de la lecture (c), φ = 0, π̄ = 2 % (`regimes.py`) :

| ζ | Régime « hausse » | Régime « baisse » |
|---|---|---|
| 4 | **1,001818, réelle** ; 0,998600 ; 0,996267 | 1,001818 ; 0,998600 ; 0,996267 |
| 8 | **paire complexe 1,000035 ∠ ±0,176°** ; 0,996263 ; 0,994468 | 1,000035 ∠ ±0,176° ; 0,996263 ; 0,994468 |

À ζ = 8, la racine dominante est **complexe**, de période 360/0,176 ≈ **2 049 tours (171 ans)**. Les deux régimes de T4 coïncident à 1e−6 près : le coude de l'emploi n'explique pas l'écart. **Vérifiée.**

**Le moteur retrouve la paire complexe** (`serie.py 0.6 8 0.02 12000 1e-6 0` puis `analyse.py … 3000 4`, `sortie_moteur.txt`) :

| Mesure sur le moteur, ζ = 8, π̄ = 2 %, φ = 0 | Choc de 1e−6 | Choc de 1e−9 | Choc de 1 % |
|---|---|---|---|
| Changements de signe de Δi_CB (pas) | 719, 1 744, 2 769, 3 793, …, 11 989 | identiques à un pas près | 730, 1 746, 2 780, … |
| Crêtes des demi-cycles, \|Δi_CB\| | 1,184e−7 (pas 225) → 1,804e−7 (pas 11 481) | 1,183e−10 → 1,804e−10 | 1,204e−3 → 1,852e−3 |
| Taux par pas entre crêtes successives (après le pas 3 000) | 1,0000349 à 1,0000352 | 1,0000346 à 1,0000355 | 1,0000284 à 1,0000430 (demi-cycles asymétriques) |
| Prony (ordre 2, 4 ou 6) sur les pas 3 000 à 12 000 | **1,0000351 ∠ ±0,1757°** (période 2 049 tours), résidu relatif 4e−9 | 1,0000347 à 1,0000350 ∠ ±0,1757° | 1,0000321 ∠ ±0,1762° |
| Maquette | 1,000035 ∠ ±0,176° | | |

Accord entre maquette et moteur : 1e−7 sur le module, 0,0003° sur l'argument. Le résultat ne dépend pas de l'amplitude du choc (1e−6 et 1e−9), donc le régime est linéaire. **Vérifiée.**

**Origine de l'écart.** Les deux estimateurs de C62 comparent des maxima de \|Δi_CB\| sur des fenêtres. Ils supposent une racine dominante réelle. Sur une paire complexe de période 2 049 tours, ils mesurent la phase de l'oscillation, pas son module :
- **Régime linéaire, 2 700 pas.** La série change de signe aux pas 719, 1 744 et 2 769. Les trois dernières fenêtres (pas 2 340 à 2 700) précèdent l'annulation du pas 2 769, d'où les ρ̂ décroissants 0,999746 / 0,998568 / 0,996747 publiés au § 3.4.4.
- **Choc de 1 %, 720 pas.** La seconde fenêtre (pas 600 à 720) finit au changement de signe du pas 730, d'où ρ̂ = 0,997465.

Ces valeurs ne sont donc pas des racines. **Aucun défaut de la maquette ni du moteur** n'est en cause, mais l'estimateur de C62 ne convient pas à une racine dominante complexe lente (issue proposée au § 3.13.9). **Vérifiée.**

**Correction de ma section § 3.4.4** (prospective ; l'ancien texte reste publié) : « Le moteur, en régime linéaire, converge sur 2 700 pas » est **réfuté**. Le moteur diverge à 1,0000351 par pas en oscillant. La ligne « 0,997465 ; aucun doublement » est un artefact de phase.

**Contrôles complémentaires** (`sortie_moteur.txt`) :
- **π̄ = 10 %, ζ = 8.** Prony sur les pas 300 à 900 : 1,0096608, contre 1,009661 pour la maquette.
- **π̄ = 0, ζ = 8.** Pas 2 000 à 7 000 : 0,9982378 ∠ ±0,2424°, contre 0,998235 ∠ ±0,243° pour la maquette.
- **Racine supplémentaire de Prony** sous ζ = 4 à 2 % et sous ζ = 8 à 10 % : 1,0036 et 1,0195, soit à peu près λ². Elle disparaît avec un choc de 1e−9 (ζ = 4 : seules restent 1,0018181 et 0,998). C'est donc l'harmonique quadratique de la non-linéarité. **Vérifiée.**

#### 3.13.3 Mesure 2 : ζ_c à π̄ = 2 % et σ correspondant

`zeta_c.py` (`sortie_zeta_c.txt`) :
- `frontiere` sur [8 ; 12,56] et sur [8 ; 9] : **ζ_c = 8,763277**, où le rayon vaut 1,000000000. Pour chaque régime de T4 pris seul : 8,753636 (« hausse ») et 8,763277 (« baisse », pire des deux, retenu par `rayon_c`). Le moteur bascule entre les deux, donc ζ_c se situe dans [8,754 ; 8,763].
- **σ_c = ζ_c (ϱ̄_L + δ) = 8,763277 × (0,029608 + 0,05) = 0,698**, sous la correspondance du § 3.1 (**hypothèse**, conditions (i) et (ii)). À titre de comparaison, ζ = 8 correspond à σ = 0,637.
- **Contrôle sur le moteur** (`serie.py` puis Prony, pas 3 000 à 12 000) :

| ζ | σ | Maquette (pire régime) | Moteur (Prony) | Période (moteur) |
|---|---|---|---|---|
| 8,263 (ζ_c − 0,5) | 0,658 | 1,000023 | 1,0000230 | 1 969 tours |
| 8,763 (ζ_c) | 0,698 | 1,000000 | 0,9999998 | 1 840 tours |
| 9,263 (ζ_c + 0,5) | 0,737 | 0,999977 | 0,9999764 | 1 734 tours |

  Le moteur traverse 1 au même ζ, à 0,005 près en ζ. **Vérifiée.**

**Lieu des racines à 2 %** (`grille_zeta.py`) :
- **ζ = 4 et 4,5** : deux racines réelles, 1,001818 et 0,998600, puis 1,001222 et 0,999154.
- **ζ_f = 4,842994** : la plus petite traverse 1 en montant (σ_f = 0,386).
- **ζ ≈ 4,853** : les deux racines réelles se rejoignent à 1,00017 et deviennent une paire complexe.
- **Au-delà**, le module de la paire décroît de façon monotone : 1,000167 (ζ = 5), 1,000125 (6), 1,000035 (8), 0,999942 (10), 0,999818 (12,56), 0,999443 (20).

**À π̄ = 10 %, aucun ζ_c dans le domaine** : le rayon reste au-dessus de 1 sur toute la grille [0,5 ; 20] (1,012105 à ζ = 0,5, 1,009661 à 8, 1,003526 à 20). **À π̄ = 0, le rayon est inférieur à 1 sur [2 ; 20]** et dépasse 1 à ζ = 0,5 (1,000927). **Vérifiée.**

**Pourquoi le rayon monte avec ζ à π̄ = 0** (remarque de `monnaie`). À π̄ = 0, la paire est déjà complexe à ζ = 4 (0,997894 ∠ ±0,133°). La coalescence a lieu avant ζ = 4 : à ζ = 2, il y a encore deux racines réelles, 0,999781 et 0,997063. Le module de la paire n'est pas monotone : 0,997894 (ζ = 4), 0,998179 (6), 0,998235 (8), 0,998232 (10), 0,998187 (12,56), 0,997949 (20), avec un maximum entre 8 et 10. ζ ne freine donc pas une racine réelle. Il la **convertit en oscillation lente**, dont le module dépend ensuite de ζ sans signe fixe. L'hypothèse du § 3.4.4, « frein par l'investissement qui compense le canal rentier », est **réfutée sous cette forme** et remplacée par ce constat. **Vérifiée** (lieu des racines) ; l'interprétation économique de la rotation est au § 3.13.6.

#### 3.13.4 Mesure 3 : couverture minimale qui stabilise (maquette)

`phi_star.py` et `phi_grille.py` (`sortie_phi_star.txt`, `sortie_phi_grille.txt`) :

| ζ | σ | φ\* à π̄ = 2 % | φ\* à π̄ = 10 % |
|---|---|---|---|
| 4 (publié) | 0,318 | 0,1741 | 0,6495 |
| **8** | **0,637** | **0,0111** | **0,5713** |
| 8,263 (ζ_c − 0,5) | 0,658 | 0,0073 | 0,5691 |
| 8,663 (ζ_c − 0,1) | 0,690 | 0,0015 | 0,5658 |
| 8,863 (ζ_c + 0,1) | 0,706 | 0 (rayon 0,999995 sous φ = 0) | 0,5641 |
| 9,263 (ζ_c + 0,5) | 0,737 | 0 (rayon 0,999977) | 0,5606 |
| 12,56 | 1,0 | 0 (rayon 0,999818) | 0,5299 |

- **Une seule traversée de 1 en φ** : le rayon décroît sur toute la grille à ζ = 8. À ζ = 4 et 2 %, il remonte de 0,996861 (φ = 0,90) à 0,997118 (φ = 1), toujours au-dessous de 1, ce qui ne crée pas de seconde traversée.
- φ\* est une **mesure de maquette**, où φ est lu comme continu. Le moteur n'admet que φ ∈ {0 ; 1} (C62, M33) et ne mesure aucun seuil.

**Vérifiée** (maquette).

#### 3.13.5 Mesure 4 : corroboration par les racines sous φ = 0 (ligne (b) de C51, citée par C62)

`racines_phi0.py` (`sortie_racines_phi0.txt`), lecture (α), θ_G visé de l'état à 2 %, r̄ = 1 %, ν_G = 1,15, n_a = 12, μ̄ = 0,60 :

| ζ | π̄ = 0 | π̄ = 2 % | π̄ = 10 % |
|---|---|---|---|
| 4 (publié) | aucune racine | −0,347 % (+0,034) ; **1,000 % (−0,034)** | −11,017 % (+0,302) ; 0,920 % (−0,267) |
| 4,843 (ζ_f) | 2,198 % (+0,045) ; 3,601 % (−0,044) | **1,000 % (−0,000)**, racine double | −7,674 % (+0,263) ; 0,890 % (−0,233) |
| **8** | 1,422 % (+0,204) ; 5,238 % (−0,182) | **1,000 % (+0,127)** ; 3,506 % (−0,118) | −1,198 % (+0,086) ; 0,573 % (−0,082) |
| 8,763 (ζ_c) | 1,366 % (+0,237) ; 5,408 % (−0,207) | 1,000 % (+0,157) ; 3,837 % (−0,143) | aucune racine |
| 12,56 | 1,214 % (+0,396) ; 5,915 % (−0,312) | 1,000 % (+0,310) ; 4,874 % (−0,256) | aucune racine |

Entre parenthèses : dθ_G/dr̄, en fraction de la production potentielle par unité de taux.

**Dépense visée réduite de 5 % (#88), ζ = 8** : deux racines à chaque π̄ :
- π̄ = 0 : −1,402 % (+0,590) et 8,724 % (−0,436) ;
- π̄ = 2 % : −2,345 % (+0,551) et 7,516 % (−0,413) ;
- π̄ = 10 % : −4,908 % (+0,529) et 4,922 % (−0,405).

Sous φ = 1, à ζ = 8 : une seule racine à chaque π̄, 1,297 / 1,000 / 1,144 %, ce qui retrouve r̄_α du § 3.4.3. **Vérifiée.**

**Ce que la méthode des racines mesure** (`pli.py`, `sortie_pli.txt`). Au point de référence, r̄ = 1 % avec le θ_G et la norme de l'état résolu au même π̄, la pente dθ_G/dr̄ sous φ = 0 s'annule exactement là où une racine **réelle** de la maquette traverse 1 :

| π̄ | ζ où la pente s'annule (script) | ζ où une racine réelle vaut 1 (maquette) |
|---|---|---|
| 0 | 1,765598 | 1,765596 |
| 2 % | 4,842996 | 4,842994 |
| 10 % | 11,412443 | 11,412442 |

Les deux transcriptions sont indépendantes (le script d'état stationnaire d'un côté, la carte d'un pas de la maquette de l'autre). Elles s'accordent à 2e−6 près en ζ. **Vérifiée.**

Conséquences :
- **Le signe de la pente donne la parité du nombre de racines réelles supérieures à 1** : il bascule à chaque traversée réelle (à 10 %, la pente devient positive à ζ = 11,41 alors que la racine dominante, réelle, reste à 1,0077). Il ne voit **ni une paire complexe ni un nombre pair de racines réelles instables**. C'est une propriété générale du déterminant de I − J. Elle est **vérifiée ici** aux trois points ; ce n'est pas un théorème établi pour ce modèle.
- **À ζ = 8 et 2 %**, la pente au point de référence est positive (+0,127), du même signe que sous φ = 1. La méthode des racines **ne corrobore plus l'instabilité** que la maquette et le moteur mesurent (paire de module 1,000035). Elle n'y contredit pas non plus : elle ne la voit pas. La phrase publiée « le moteur les corrobore par les racines sous φ = 0 » ne vaut plus à 2 %.
- **À ζ = 8 et 10 %**, la racine haute 0,573 % a une pente négative, ce qui est cohérent avec la racine réelle de 1,009661. Entre ζ = 8 et ζ = 8,763, les deux racines de θ_G inchangé disparaissent à 10 % : aucun état stationnaire sous φ = 0 ne garde la dépense visée de l'état à 2 %. Le ζ exact de cette disparition n'est **pas mesuré**.

#### 3.13.6 Option : vecteur propre et plan 2 × 2

`option.py` (`sortie_option.txt`), π̄ = 2 %, φ = 0, régime « hausse ».

**Vecteur propre à droite.** Coordonnées mises à l'échelle (S⁻¹JS : 0,01 pour un taux, PIB pour un montant), composantes relatives à la plus grande :

| ζ | λ | Composantes dominantes |
|---|---|---|
| 4 | 1,0018181 (réelle) | r̂\* 1,000 ; i_D 0,526 ; i_L 0,211 ; B_Bk 0,124 ; D_H 0,046 ; Y^HS 0,041 ; P 0,040 |
| 8 | 1,0000302 − 0,0030664 i | r̂\* 1,000 ∠0° ; i_D 0,507 ∠−4° ; i_L 0,204 ∠−4° ; B_Bk 0,131 ∠27° ; π^e 0,072 ∠−79° ; D_H 0,047 ; K^vol 0,040 ∠−119° |

Ramenées en points de taux, les composantes de i_D et i_L égalent celle de r̂\*, puisque les deux taux suivent i_CB. Le mode est donc :
- une dérive du taux réel neutre estimé (BC2, intégrateur) ;
- portée par la dette détenue par les banques ;
- qui alimente les dépôts des ménages.

À ζ = 8 s'y ajoutent le capital en volume, en retard de phase de 119°, et l'anticipation, en retard de 79° : ce sont eux qui font tourner le mode. **Vérifiée** (composantes) ; lecture économique : **hypothèse**.

**Plan 2 × 2** (lecture (c), pire des deux régimes) :

| | φ = 0 | φ = 1 |
|---|---|---|
| ζ = 4, règle de taux | 1,001818 | 0,997118 |
| ζ = 8, règle de taux | 1,000035 | 0,996922 |
| ζ = 4, taux directeur tenu (`taux = "exogene"`) | 0,997975 | 0,997975 |
| ζ = 8, taux directeur tenu | 0,997975 | 0,997975 |

- **Sans la règle de taux, le rayon ne dépend ni de ζ ni de φ.** Sans le canal rentier coupé par la couverture (φ = 1), il est sous 1 aux deux ζ.
- L'instabilité sous φ = 0 exige donc les deux à la fois : la règle de taux (BC1, BC2) et le surcroît d'intérêts versé au privé. ζ n'agit qu'**à l'intérieur** de cette boucle.
- Le plan coupe la règle et non le seul canal rentier. Une coupe du canal rentier seul, par exemple en neutralisant les intérêts sur titres dans Div_Bk, demanderait une variante de la carte : **non mesurée**.

**Vérifiée.**

#### 3.13.7 Formulation à publier

Je propose ce texte pour `sec:finances_publiques-impots`, `sec:finances_publiques-conditions` (ligne (b) de C62) et C62 de la fiche 9. Il ne retient que ce qui est établi ci-dessus.

> **Sous φ = 0** (intérêts financés par le déficit), à ζ = 8, la boucle conjointe est **explosive à 10 %** et **quasi neutre à 2 %**, avec **un signe qui dépend de ζ**. Elle est stable à π̄ = 0.
> - **À 10 %** : racine réelle de 1,009661, écart doublé en 72 tours (6 ans). Couverture minimale qui stabilise : 0,571. La boucle reste explosive sur tout le domaine de ζ mesuré, de 0,5 à 20.
> - **À 2 %** : paire complexe de module 1,000035 et de période voisine de 2 050 tours (171 ans). L'enveloppe de l'écart double en 19 800 tours environ, et croît de 2,6 % en 720 tours. Couverture minimale : 0,011.
> - **À 2 %, le module passe 1 à ζ_c = 8,76**, soit σ ≈ 0,70 sous la correspondance ζ = σ/(ϱ̄_L + δ). Ce seuil se trouve dans la fourchette de σ lue (0,5 à 1,0) : la boucle est faiblement explosive en deçà et faiblement amortie au-delà.
> - **À π̄ = 0** : module de 0,998235.
>
> Ce sont des valeurs de la maquette conjointe. Le moteur retrouve la racine dominante par identification sur 12 000 pas : 1,0000351 de période 2 049 tours à 2 %, 1,0096608 à 10 %, 0,9999998 à ζ_c. Les estimateurs par fenêtres ne mesurent pas une racine complexe de période plus longue que leur horizon. La méthode des racines sous φ = 0 ne détecte que la parité des racines réelles supérieures à 1 : elle corrobore 10 %, pas 2 %.
>
> Résultat du modèle sous la calibration soumise à M34 ; ζ_c reste à remesurer (rang 8, P224).

**Ce que le texte ne doit pas dire** :
- « stable à 2 % » : le module 1,000035 est au-dessus de 1 ;
- « converge sur 2 700 pas » : réfuté ;
- « ζ freine la boucle » : le module n'est pas monotone en ζ à π̄ = 0 ;
- un temps de doublement à 2 % issu des estimateurs par fenêtres (0,999746, 0,997465 : artefacts de phase).

À reprendre aussi :
- les valeurs « 381 tours » et « 63 tours », qui deviennent environ 19 800 (maquette ; 19 750 au module du moteur) et 72 tours à ζ = 8 ;
- « 0,174 et 0,650 », qui deviennent 0,011 et 0,571 ;
- « double l'écart en 5 ans » (fiche 9, l. 1267, relevé par `jeu`), qui devient 6 ans à 10 %.

#### 3.13.8 Réserves

- **Marge infime.** À 2 %, le module s'écarte de 1 de 3,5e−5 par tour. Les autres paramètres que M34 recalibre peuvent faire changer le signe : λ_w (#45), a_π et a_I (#163), δ (#164). La sensibilité de ζ_c à ces paramètres n'est **pas mesurée**. La formule « signe dépendant de ζ » doit se lire « et du reste de la calibration », et ζ_c est à remesurer après M34.
- σ_c = 0,70 repose sur la correspondance du § 3.1 (**hypothèse**). Sous la lecture « crédit seul » (condition (i)), σ_c serait de 0,28.

#### 3.13.9 Issue proposée (création sur accord)

**Titre** : C62 : estimateur du temps de doublement inadapté à une racine dominante complexe (ζ = 8)
**Libellés** : `needs-triage`
**Corps** :

> *Rédigé par l'agent macro (IA).*
>
> Les deux tests de C62 (`test_temps_de_doublement_sous_phi_nul` et `test_temps_de_doublement_en_regime_lineaire`, `tests/invariants/test_socle_complet.py`) estiment ρ̂ par rapport de maxima de |Δi_CB| sur des fenêtres de 120 pas. À ζ = 8 (P218) et π̄ = 2 %, la racine dominante sous φ = 0 est une paire complexe de module 1,000035 et de période voisine de 2 049 tours (`docs/blocs/calibration.md`, § 3.13.2). Les fenêtres mesurent alors la phase de l'oscillation, pas son module. Le test en régime linéaire publierait 0,999746 / 0,998568 / 0,996747 (changement de signe au pas 2 769), et le test du choc de 1 % publierait 0,997465 (changement de signe au pas 730). L'identification par prédiction linéaire (Prony, ordres 2 à 6) sur 12 000 pas donne 1,0000351 ∠ ±0,1757°, et la maquette 1,000035 ∠ ±0,176°.
>
> À décider (mainteneur) : remplacer ou compléter l'estimateur publié par une identification de la racine dominante, ou par un rapport de crêtes de demi-cycles sur un horizon d'au moins deux périodes ; ou publier la racine de la maquette seule, le moteur la corroborant. Les mesures sont publiées sans verdict : aucun critère jugé ne change, mais les valeurs publiées changent (tableau avant / après au commit de #55).

#### 3.13.10 Points pour `jeu` (je ne les tranche pas)

- À ζ = 8 et 2 %, sous φ = 0, un choc de dépense de 1 % fait osciller le taux directeur avec une amplitude de 0,12 point et une période de 171 ans. L'enveloppe croît de 2,6 % en 60 ans. C'est **imperceptible sur une partie** : le joueur ne verra ni dérive ni explosion à 2 %.
- À 10 %, la dérive reste nette : doublement en 6 ans, arrêt du choc de 1 % au pas 543.
- La leçon publiable est « financer les intérêts par le déficit est dangereux quand l'inflation est élevée ». À inflation basse, son signe dépend de paramètres contestés.

#### 3.13.11 Statut des conclusions

- **Vérifiées** (commande et sortie) :
  - écart entre maquette et moteur levé : paire complexe 1,000035 ∠ ±0,176° dans les deux, à 1e−7 près sur le module ; régime linéaire (1e−6 et 1e−9) ;
  - les estimateurs de C62 mesurent la phase (changements de signe aux pas 719, 730 et 2 769) ; aucun défaut de la maquette ni du moteur ;
  - « converge sur 2 700 pas » (§ 3.4.4) réfuté ;
  - harmonique λ² dans les fits de Prony, absente avec un choc de 1e−9 ;
  - ζ_c = 8,763 (« hausse » 8,754), confirmé sur le moteur à ζ_c et ζ_c ± 0,5 ; aucun ζ_c à 10 % sur [0,5 ; 20] ; stable à π̄ = 0 sur [2 ; 20] ;
  - lieu des racines : ζ_f = 4,843, coalescence vers 4,853, module non monotone à π̄ = 0 ; l'hypothèse « frein » est réfutée sous sa forme du § 3.4.4 ;
  - φ\* à ζ = 8 : 0,0111 et 0,5713, avec une seule traversée ; aux ζ_c ± 0,1 et ± 0,5 ; contrôle à ζ = 4 ;
  - racines sous φ = 0 à ζ = 8, avec et sans la réduction de 5 % ; contrôle des valeurs publiées à ζ = 4 ;
  - coïncidence entre le zéro de la pente et la racine réelle égale à 1, aux trois π̄, à 2e−6 près en ζ ;
  - composantes du vecteur propre ; plan 2 × 2 (règle de taux × φ).
- **Hypothèses** :
  - σ_c = 0,70 (correspondance du § 3.1) ;
  - lecture économique du vecteur propre (rotation par le capital et l'anticipation) ;
  - généralité de la règle de parité hors des trois points mesurés.
- **Non vérifiées** :
  - sensibilité de ζ_c aux paramètres recalibrés par M34 ;
  - coupe du seul canal rentier ;
  - ζ où les racines à 10 % disparaissent sous θ_G inchangé ;
  - les deux tests C62 exécutés par `pytest` à ζ = 8 (les sondes rejouent leur protocole, mais le paramètre du dépôt reste ζ = 4).

### 3.14 Avis consultés et décisions du mainteneur (16/11/2026)

**Avis de `monnaie`** (frontière dette publique, sur les sorties de `macro`, sans réexécution) : accepter ζ = 8 ; garder ζ = 4 pour préserver « explosif à 2 % » reviendrait à caler un paramètre sur un résultat attendu. Le rayon sous φ = 0 à 2 % passe sous 1 entre ζ = 8 et ζ = 12,56, à l'intérieur de la fourchette de σ lue : aucun verdict tranché n'est défendable à 2 %. À ζ = 8, maquette (1,000035) et moteur (ρ̂ non stabilisé, 0,999746 → 0,996747) divergent ; « converge » est prématuré. Formulation proposée : « explosif à 10 % ; quasi neutre à 2 %, signe dépendant de ζ ». Le rayon monte avec ζ à π̄ = 0, ce qui affaiblit l'hypothèse d'un simple frein par l'investissement. Remesures demandées avant M34 (§ 3.13). Littérature non relue dans la consultation.

**Avis de `jeu`** (lecture des fiches, sans scénario) :
- perte de « explosif à 2 % » : lisible, le joueur lit les précurseurs de M33, pas un rayon ; textes d'aide à reprendre sinon « à revoir » (signe d'une hausse de taux sous φ = 0, `docs/blocs/banque_centrale.md` l. 1368 et 1458 ; « double l'écart en 5 ans », `docs/blocs/finances_publiques.md` l. 1267) ;
- « marge de 60 % » et dividendes à 22 % du PIB : à clarifier ; intituler « marge sur le coût salarial unitaire », afficher à côté de la part salariale, restituer la décomposition du § 1.6 et renvoyer à #164 ;
- ζ = 8 : exiger un indicateur d'investissement au tour (#165) ; recalculer le libellé « −2 % d'investissement par point » après M34 ; l'aide ne cite pas la couverture minimale tant qu'elle n'est pas remesurée.

**Décisions du mainteneur** :
- question 1 : **ζ = 8** retenu comme valeur proposée de la table soumise à M34, déclaré « σ ≈ 0,64, niveau contesté » (P218) ;
- question 2 : C62 remesuré avant M34 (écart maquette–moteur, ζ_c, couverture minimale, racines sous φ = 0), puis reformulé ; formulation visée « explosif à 10 % ; quasi neutre à 2 %, signe dépendant de ζ » (P219) ;
- question 3 : κ inchangé, écart déclaré ; calage conjoint de κ et δ dans #164, où les mesures d'Eurostat sont versées en commentaire (P220) ;
- indicateur d'investissement au tour : issue #165, rattachée au J4 (P221) ;
- question 4 (distribution nette, publiée avec la brute) : avis de `macro` suivi sous la délégation P211.
- remesures de C62 (§ 3.13) : formulation du § 3.13.7 adoptée pour M34, sous relecture de `monnaie` (P222) ; issue #166 sur l'estimateur de C62, ajoutée au périmètre et traitée au rang 3 (P223) ; ζ_c remesuré au rang 8 (P224).
- relecture de `monnaie` du § 3.13 (16/11/2026, sans réexécution) : conforme sur les quatre demandes ; aucun point bloquant avant M34 ; retouches 1 à 4 de la formulation du § 3.13.7 appliquées par la session sous P211 (« à 2 % » devant ζ_c ; 19 800 tours au module de la maquette, ln 2 / ln 1,000035 = 19 805, contre 19 748 au module du moteur ; « parité des racines réelles supérieures à 1 » ; réserve de calibration). Remarques de méthode consignées sans retouche : le signe de det(I − J) = Π(1 − λᵢ) ne change qu'au passage d'une racine réelle par 1, fait algébrique général, le lien propre au modèle étant celui de la pente dθ_G/dr̄ à ce déterminant (§ 3.13.5) ; le rayon 0,997975 du plan 2×2 sous taux tenu est celui d'un autre mode, puisque tenir le taux supprime l'intégrateur r̂\* qui porte le mode dominant (§ 3.13.6) ; mécanisme proposé, hypothèse : sous φ = 0, l'État finance par le déficit tous les intérêts nominaux, y compris la part qui compense l'inflation, d'où un danger croissant avec π̄.

## 4. #130 — Écarts bancaires ϖ_L et ϖ_D, fonds propres visés ϑ (bloc 7) et taux réel neutre r̄ (bloc 8)

*Instruite par `monnaie` (expert pilote) le 16/11/2026, rang 1 de la branche « calibration » (PR #162, tête `3da48c0`), après la section #55. `macro` est consulté ensuite sur le dividende et la distribution (§ 4.7). Les chiffres du modèle viennent de sondes hors dépôt qui appellent, sans le modifier, `outils/etat_stationnaire.py` (méthode au § 4.4.1). Ce sont des résultats du modèle, pas des faits. Les faits portent leur source et leur date. Chaque conclusion est marquée **vérifiée**, **hypothèse** ou **non vérifiée**. La base est l'état à μ̄ = 0,60 et ζ = 8 des § 1 et 3 (P213, P218), notée **A** ; l'état proposé est noté **P**.*

### 4.1 Grandeurs visées et correspondance avec le modèle

| Grandeur | Définition dans le modèle | Unité | Dénominateur | Fenêtre |
|---|---|---|---|---|
| ϖ_L (B1) | i_{L,t} − i_{CB,t−1}, appliqué à **tout l'encours** L (ligne 9) | point de % par an, taux de flux | — | constant, tout π̄, tout n_a |
| ϖ_D (B2) | i_{CB,t−1} − i_{D,t}, appliqué à **tous les dépôts** D_H + D_F (ligne 10), sans distinction de durée | point de % par an | — | idem |
| ϑ (B6) | fonds propres visés E^Bk/L, L crédits de clôture | fraction | crédits aux entreprises (seuls crédits du modèle) | clôture |
| r̄ (BC1, E4) | taux réel neutre de l'état stationnaire, Fisher sur la cible : 1 + i_CB = (1 + r̄)(1 + π\*) | % par an | — | état stationnaire |

**Traits du modèle que la définition empirique doit respecter** (vérifiés sur `etat_stationnaire`, l. 401 à 465, et `sec:banque-stationnaire`) :

| Trait | Dans le modèle | Conséquence pour la source |
|---|---|---|
| Taux directeur | Corridor de largeur nulle : i_res = i_B = i_CB (M32, M33) | Le taux observé comparable est le **taux du jour le jour du marché** (EONIA, puis €STR), qui suit le taux opérationnel en système de plancher comme en corridor ; pas le taux des opérations principales seul |
| Crédit | Une seule classe : crédits aux entreprises, à taux révisé chaque pas (variable) | Taux des **crédits aux sociétés non financières** ; affaires nouvelles (prix vu par l'emprunteur, fiche 7 § 9.2) et encours en variante |
| Dépôts | Une seule rémunération pour les dépôts des ménages et des entreprises, à vue ou non | **Taux moyen pondéré** des dépôts des ménages et des SNF (à vue, à terme, à préavis), pondéré par les encours |
| Écart constant | ϖ_D ne dépend ni du niveau ni du sens du taux (bêta des dépôts égal à 1) | La moyenne observée dépend du régime de taux : à déclarer (§ 4.2) |
| Fonds propres | E^Bk = ϑ L ; l'actif est L + B_Bk + Res ; titres publics et réserves ne portent aucune exigence | Sous les pondérations de Bâle 1988 (0 % État et banque centrale en monnaie nationale, 100 % secteur privé), **les actifs pondérés de la banque du modèle sont exactement L**. ϑ est donc un ratio de fonds propres sur actifs pondérés « Bâle I ». Le ratio observé (Bâle III, approches internes) a un dénominateur plus petit : écart déclaré |
| Nature des fonds propres | Fonds propres purs, sans dette subordonnée | **CET1** (fonds propres de base de catégorie 1) plutôt que le ratio de solvabilité total, qui inclut des instruments de dette (AT1, Tier 2) |
| Coûts | Aucun coût d'exploitation, aucune perte sur crédit, aucun impôt | Le rendement des fonds propres et la marge nette d'intérêt ne sont **pas des cibles** (fiche 7, critère 17) |

**Formes fermées en jeu** (`sec:banque-stationnaire`) : n_a Π^Bk = i_CB E^Bk + ϖ_L L + ϖ_D D ; rendement des fonds propres i_CB + (ϖ_L + ϖ_D D/L)/ϑ ; part distribuée 1 − n_a(Γ̄ − 1)/rendement ; condition d'existence ϑ i_CB + ϖ_L + ϖ_D D/L ≥ ϑ n_a(Γ̄ − 1). Aucune vitesse n'y entre. **Vérifiée** (forme brute contre forme réduite, résidu ≤ 4,8e−15 dans `controles`).

**Ce qui ne dépend pas des paramètres de #130** (mesuré, sortie `sortie_v1.txt`) : ϑ n'entre ni dans le bloc 6, ni dans les prix, ni dans le travail : capital, part salariale, I/PIB, D_F, distribution, Div_F, caisse des entreprises sont identiques à A au bit. ϖ_L et ϖ_D changent i_L, i_D, Div_F et la distribution, mais pas θ_G, ni la dette (à l'arrondi publié : les variations de Div_F et de Div_Bk se compensent dans le revenu des ménages, comme pour μ̄ au § 1.4.2). **Vérifiée.**

### 4.2 Sources lues et citées

**(a) Écart du crédit, lu.** BCE, statistiques de taux d'intérêt des IFM (MIR), lues sur le miroir DBnomics (`db.nomics.world`, pages des séries, mise à jour indiquée par la page ; tableau des valeurs embarqué), consultées le 16/11/2026 :
- `ECB/MIR/M.U2.B.A2I.AM.R.A.2240.EUR.N` : indicateur composite du coût de l'emprunt des sociétés non financières (S.11), affaires nouvelles, zone euro à composition variable, mensuel, 2003-01 à 2026-08 ;
- `ECB/MIR/M.U2.B.A20.A.R.A.2240.EUR.O` : crédits aux SNF, encours, toutes durées (variante) ;
- taux du jour le jour : EONIA, moyenne mensuelle (`ECB/FM/M.U2.EUR.4F.MM.EONIA.HSTA`), jusqu'en 2019-09 ; €STR, moyenne mensuelle des observations quotidiennes (`ECB/EST/B.EU000A2X2A25.WT`), dès 2019-10. Sur le chevauchement 2019-10 à 2021-12, EONIA − €STR vaut 0,0850 point chaque mois (calculé) : le raccord déplace la moyenne 2003–2024 de moins de 0,01 point.

| Fenêtre (moyenne de mois) | n | ϖ_L, affaires nouvelles | ϖ_L, encours | taux du jour le jour moyen |
|---|---|---|---|---|
| **2003–2024** | 264 | **2,09** | 2,30 | 1,07 |
| 2003-01 à 2008-08 (avant la crise, corridor) | 68 | 1,64 | 1,94 | 2,80 |
| 2003-01 à 2014-05 (taux positifs) | 137 | 2,16 | 2,51 | 1,70 |
| 2014-06 à 2022-06 (taux négatifs) | 97 | 2,15 | 2,53 | −0,37 |
| 2022-07 à 2024-12 (hausse des taux) | 30 | 1,52 | 0,56 | 2,85 |
| 2003–2025 | 276 | 2,06 | 2,25 | 1,12 |

Minimum et maximum mensuels, 2003–2024, affaires nouvelles : 1,21 et 3,16 points. L'écart sur les affaires nouvelles est **stable entre régimes** (1,5 à 2,2 points selon la fenêtre). L'écart sur les encours s'effondre en 2022–2024 parce que les encours à taux fixe ne suivent pas la hausse : c'est la transformation d'échéances, que le modèle n'a pas. Faits, **vérifiés** (sonde `ecarts.py`, sortie ci-dessus).

**(b) Écart des dépôts, lu.** Mêmes statistiques, encours pondérés par les encours de la BSI (IFM hors SEBC, stocks de fin de mois) :
- taux : dépôts à vue des ménages (`L21…2250.EUR.N`) et des SNF (`L21…2240.EUR.N`) ; dépôts à terme, encours (`L22.A…2250.EUR.O`, `L22.A…2240.EUR.O`) ; dépôts à préavis de 3 mois au plus des ménages (`L23.D…2250.EUR.N`), employé aussi pour les SNF, faute de série trouvée (part de 1,1 % des encours en décembre 2024) ;
- poids : `ECB/BSI/M.U2.N.A.{L21,L22,L23}.A.1.U2.{2250,2240}.Z01.E`. En décembre 2024 : à vue 58,6 % (ménages 39,2, SNF 19,4), à terme 22,1 %, à préavis 19,3 %.

| Fenêtre | ϖ_D, taux pondéré | ϖ_D, dépôts à vue des ménages seuls |
|---|---|---|
| 2003–2024 | **−0,05** | 0,67 |
| **2003-01 à 2008-08** | **0,85** | 1,93 |
| 2014-06 à 2022-06 | −0,74 | −0,43 |
| **2022-07 à 2024-12** | **1,93** | 2,60 |
| 2023–2025 | 1,97 | 2,71 |

Minimum et maximum mensuels 2003–2024 (pondéré) : −1,29 et 2,77 points. Faits, **vérifiés**.

**Lecture.** L'écart des dépôts **dépend du régime** : négatif quand le taux directeur est négatif (les banques n'ont pas reporté les taux négatifs sur les dépôts), positif et de l'ordre d'un à deux points quand le taux du jour le jour est voisin de 3 %. La moyenne longue (−0,05) est dominée par huit ans de taux négatifs, régime que l'état de référence du modèle n'a pas (i_CB = 3,02 % à π̄ = 2 %). La dépendance de l'écart au niveau du taux (« bêta des dépôts » inférieur à 1) est une **limite de la forme B2**, pas un objet de calibration. La littérature sur ce point (Drechsler, Savov et Schnabl, « The Deposits Channel of Monetary Policy », *QJE*, 2017) **n'a pas été lue** : aucun chiffre n'en est tiré.

**(c) Fonds propres, lus.**
- **Comité de Bâle sur le contrôle bancaire**, *International Convergence of Capital Measurement and Capital Standards*, Bâle, juillet 1988 (PDF de `www.bis.org`, lu le 16/11/2026 ; texte extrait par `pdftotext`) :
  - § 44 (partie III, p. 14) : « the target standard ratio of capital to weighted risk assets should be set at 8% (of which the core capital element will be at least 4%) » ;
  - annexe 2, « Risk weights by category of on-balance-sheet asset » (p. 21 et 22) : 0 % pour « Cash » et « Claims on central governments and central banks denominated in national currency and funded in that currency » ; 50 % pour « Loans fully secured by mortgage on residential property » ; 100 % pour « Claims on the private sector ».
  - **Vérifiée.** Cela lève la réserve de `tab:calibration` (« texte non lu ») et de la fiche 7 § 9.2 (« lu dans un extrait de moteur de recherche »).
- **BCE, statistiques de supervision bancaire** (MSU, « Significant institutions », échantillon variable), `ECB/SUP/Q.B01.W0._Z.I4008._T.SII._Z._Z._Z.PCT.C` (ratio CET1, % des actifs pondérés) et `…I4001…` (ratio de solvabilité total), DBnomics, consultés le 16/11/2026 :

| Grandeur (MSU, établissements importants) | 2015T3–2024T4, moyenne (38 trimestres) | min ; max | 2024T4 |
|---|---|---|---|
| **CET1 / actifs pondérés** | **14,75 %** | 12,77 ; 15,97 | 15,97 % |
| Fonds propres totaux / actifs pondérés | 18,51 % | 16,06 ; 20,10 | 20,10 % |

- **BCE, BSI**, IFM hors SEBC, zone euro, stocks de décembre, « capital et réserves » (`L60.X.1.Z5.0000`) sur crédits (`A20.A.1.U2`), même consultation :

| Rapport comptable | 2003–2024 (22 décembres) | min ; max |
|---|---|---|
| Capital et réserves / crédits aux SNF | 0,491 | 0,366 ; 0,595 |
| … / crédits aux SNF et aux ménages | 0,221 | 0,173 ; 0,259 |
| … / crédits à tous les résidents non IFM | 0,182 | 0,144 ; 0,215 |

  Faits, **vérifiés** (sonde `theta.py`). Réserve : le bilan de la BSI est **agrégé, non consolidé** (les participations entre IFM ne sont pas éliminées) et le capital couvre aussi les titres, les prêts interbancaires et les actifs extérieurs. Ce rapport surestime les fonds propres qui adossent les crédits ; l'ampleur n'est pas mesurée.

**Écart de définition déclaré (critère propre de #130).** ϑ est un rapport **fonds propres sur crédits**. Le ratio CET1 est un rapport **fonds propres sur actifs pondérés des risques**. Pour la banque du modèle, qui ne détient que des crédits aux entreprises, des titres publics et des réserves, les deux coïncident sous les pondérations de Bâle 1988 (100 % et 0 %, lues). Le ratio observé est calculé sous Bâle III, en grande partie par les approches internes, avec des pondérations des crédits aux entreprises en moyenne inférieures à 100 %. Le ratio observé rapporté à des actifs pondérés à 100 % serait donc plus bas que 14,75 %. L'ampleur n'est **pas vérifiée** : la densité des actifs pondérés (`I4011`) n'a pas été trouvée sur le miroir. **Contesté.**

**(d) Taux réel neutre, lus.**
- **BCE, *Economic Bulletin* 1/2024**, encadré « Estimates of the natural interest rate for the euro area: an update », C. Brand, N. Lisack et F. Mazelis (`www.ecb.europa.eu`, lu le 16/11/2026 par WebFetch, citations courtes rendues par l'outil). Définition : « the real rate of interest that is neither expansionary nor contractionary ». Depuis le second semestre 2023, les modèles de structure par terme et semi-structurels donnent des estimations comprises entre « about minus three-quarters of a percentage point to around half a percentage point ». Dernière observation : 2023T4.
- **BCE, *Economic Bulletin* 1/2025**, encadré « Natural rate estimates for the euro area: insights, uncertainties and shortcomings » (même hôte, lu le même jour ; auteurs non restitués par l'outil). Fin 2024 : « the most recent estimates of real r\* span a range between -½% and +½% » ; avec les trois estimations de type Holston, Laubach et Williams, « the range of real r\* is -½% to 1% ». L'encadré souligne une incertitude « very high » et des bandes d'estimation qui « can span up to several percentage points ». Dernière observation : 2024T4 (2024T3 pour HLW).
- **Réserve fédérale, *Summary of Economic Projections*, 16/09/2026**, tableau 1 (`www.federalreserve.gov`, lu le 16/11/2026) : taux des fonds fédéraux de long terme, médiane **3,2 %**, tendance centrale 3,0–3,6, étendue 2,9–3,9 ; inflation PCE de long terme 2,0. Le taux réel implicite (soustraction, 3,2 − 2,0) vaut **1,2 %**, tendance centrale 1,0 à 1,6 %, étendue 0,9 à 1,9 %. C'est une projection des participants au FOMC, pas une estimation économétrique.
- **Non lus** : Holston, Laubach et Williams (2017, *Journal of International Economics*, et mises à jour de la Réserve fédérale de New York : hôte non ouvert) ; Laubach et Williams (2003) ; FMI, *Perspectives de l'économie mondiale*, avril 2023, chapitre 2 ; Borio et al. (BRI, *Working Paper* 685). Aucun chiffre n'en est tiré.

**Fourchette lue de r̄** : de **−0,5 % à +1,0 %** pour la zone euro (BCE, fin 2024), de **0,9 % à 1,9 %** pour les États-Unis (FOMC, septembre 2026, étendue). Fourchette d'ensemble : **−0,5 % à +1,9 %**. Le niveau est **contesté** (critère 23 de la fiche 8) : les sources elles-mêmes le disent incertain de plusieurs points.

### 4.3 Valeurs proposées et variantes

**Écarts : ϖ_L = 0,02 et ϖ_D = 0,01, inchangés, désormais sourcés.**
- ϖ_L = 0,02 : moyenne 2003–2024 de l'écart du coût composite de l'emprunt des SNF au taux du jour le jour, 2,09 points ; arrondie au point entier. Stable entre régimes (1,5 à 2,2). **Vérifiée.**
- ϖ_D = 0,01 : moyenne des fenêtres de **taux positifs comparables à l'état de référence** (0,85 avant la crise ; 1,93 en 2022–2024). Valeur ronde dans cette plage. La moyenne longue (−0,05) n'est pas retenue : elle mêle un régime de taux négatifs que le modèle n'a pas. **Choix déclaré, source lue, fenêtre contestée.**
- Motif supplémentaire : l'égalité ϖ_D = r̄ = 0,01 rend i_D nul à π̄ = 0. Les tests de stationnarité classent cette nullité en arithmétique exacte (`sec:calibration`, verdicts P94). Garder les deux valeurs évite de toucher cette liste.

**ϑ proposé : 0,15.** C'est le ratio CET1 moyen des établissements importants du MSU, 2015T3–2024T4 (14,75 %), arrondi. Motifs :
- c'est la seule mesure lue dont le dénominateur coïncide avec celui du modèle, sous les pondérations de Bâle 1988 (lues) ;
- 0,10 est **sous toutes les observations** de la série (minimum 12,77 %) ; il ne dépasse que le minimum réglementaire de Bâle 1988 (8 %, dont 4 % de fonds propres de base) ;
- le CET1 est la mesure la plus proche de fonds propres purs.

Statut : **choix déclaré, source lue, écart de dénominateur contesté** (§ 4.2 (c)).

**r̄ proposé : 0,01, inchangé, déclaré contesté.** Il est dans les deux fourchettes lues : borne haute de la zone euro (−0,5 à 1,0), bas de l'étendue du FOMC (0,9 à 1,9). C'est une valeur ronde, au milieu de la fourchette d'ensemble (−0,5 à 1,9). Elle garde r̄ < g (1 % contre 2 % de croissance de la productivité), propriété déjà publiée de l'état de référence. Statut : **choix de conception, fourchette lue, niveau contesté** (P208 ; critère 23).

**Variantes mesurées** (sorties `sortie_v1.txt` et `sortie_v2.txt` ; à π̄ = 2 % sauf mention ; « publiées en écart » : nombre de valeurs publiées du script, sur 449, en écart à la publication actuelle) :

| Variante | Paramètres | ROE % | Marge nette % | Dette consolidée | Part distribuée Bk | Existence, par an | Distribution, π̄ = 0 | Publiées en écart | Avis |
|---|---|---|---|---|---|---|---|---|---|
| A (base) | ϖ 0,02 / 0,01 ; ϑ 0,10 ; r̄ 0,01 | 36,15 | 2,497 | 0,25695 | 0,89025 | 0,032180 | 0,88598 | 185 | Statu quo de #130 |
| **P, proposée** | **ϑ = 0,15** | **25,10** | **2,514** | **0,28785** | **0,84197** | **0,031703** | **0,88598** | 284 | **Recommandée** |
| ϑ bas | ϑ = 0,08 | 44,43 | 2,490 | 0,24459 | 0,91071 | 0,032371 | 0,88598 | non relevé | Minimum de Bâle 1988 ; sous toutes les observations |
| ϑ comptable | ϑ = 0,18 | 21,42 | 2,524 | 0,30639 | 0,81480 | 0,031417 | 0,88598 | non relevé | BSI, crédits aux non-IFM ; dénominateur trop large, bilan non consolidé |
| Écarts d'avant la crise | ϖ_L 0,0165 ; ϖ_D 0,0085 | 30,68 | 2,119 | 0,25695 | 0,87069 | 0,026711 | 0,88735 | 234 | Fenêtre courte ; rend i_D ≠ 0 à π̄ = 0 |
| Écarts longs | ϖ_L 0,021 ; ϖ_D 0 | — | — | — | — | 0,020053 | — | **refus du script** | Écartée : voir ci-dessous |
| r̄ bas | r̄ = 0,005 | 35,62 | 2,463 | 0,25596 | 0,88863 | 0,031655 | 0,88741 | 328 | Dans les deux fourchettes de la zone euro ; i_D = −0,5 % à π̄ = 0 |
| r̄ haut | r̄ = 0,015 | 36,67 | 2,530 | 0,25794 | 0,89183 | 0,032706 | 0,88452 | 333 | Tient la liste O1 de la première tentative (1,5 à 3 %), qui n'est pas une source |
| r̄ = g | r̄ = 0,02 | 37,20 | 2,564 | 0,25894 | 0,89336 | 0,033232 | 0,88302 | 336 | Au-dessus des deux fourchettes lues (FOMC : 1,9 au plus) ; solde primaire stationnaire positif (+0,019 % à 2 %) |

**Variante « écarts longs » (ϖ_D = 0) : l'état de référence existe, le script la refuse.** La marge d'existence est positive aux trois π̄ et aux trois n_a (0,020053 par an à π̄ = 2 %, n_a = 12). Mais `calculer` lève `HorsDomaine` dans `_canal_ecarts_nominaux` (l. 2268), qui force ϖ_L = 0 pour une mesure publiée : avec ϖ_D = 0 aussi, les deux écarts sont nuls et la condition d'existence échoue, comme publié (« avec des écarts nuls, elle échoue »). C'est une limite d'une mesure publiée, pas de l'état. **Vérifiée** (trace d'appel, sonde `wlong.py`). Elle n'est pas proposée.

**Variantes de r̄** (π̄ = 0 / 2 / 10 %) : taux directeur i_CB = (1 + r̄)(1 + π̄) − 1, calculé à la main et égal au script.

| r̄ | i_CB, % | Taux réel restitué, % | θ_G | Solde primaire, % du PIB | i_D à π̄ = 0 |
|---|---|---|---|---|---|
| 0,005 | 0,50 / 2,51 / 10,55 | 0,50 / 0,51 / 0,55 | 0,218839 / 0,220541 / 0,221662 | −0,146 / −0,373 / −0,518 | −0,50 % |
| **0,01** | **1,00 / 3,02 / 11,10** | **1,00 / 1,02 / 1,10** | **0,218474 / 0,219573 / 0,219568** | **−0,097 / −0,243 / −0,239** | **0,00** |
| 0,015 | 1,50 / 3,53 / 11,65 | 1,50 / 1,53 / 1,65 | 0,218107 / 0,218598 / 0,217456 | −0,048 / −0,113 / +0,043 | 0,50 % |
| 0,02 | 2,00 / 4,04 / 12,20 | 2,00 / 2,04 / 2,20 | 0,217737 / 0,217615 / 0,215325 | +0,002 / +0,019 / +0,327 | 1,00 % |

Le signe du solde primaire stationnaire suit celui de r̄ − g, à la dette consolidée près. À r̄ ≥ g, l'État dégage un excédent primaire à l'état stationnaire. C'est le résultat attendu de la dynamique de dette (condition de Domar), pas un fait empirique. **Vérifiée** (mesure) ; lecture : **hypothèse** de mécanisme, non décomposée.

### 4.4 Tableau avant / après prédit

#### 4.4.1 Méthode et commandes

Sondes du scratchpad, lancées depuis `/home/user/projet_macro` à `3da48c0` (`git status` vide avant et après), dossier `<scratchpad>/outils130/` :
- **`sonde130.py`** : importe `outils/etat_stationnaire.py` par son chemin, sans le modifier, et appelle `calculer(replace(Parametres(), mu_bar=0.60, zeta=8.0, **variante))`. Noms de champs exacts du script : `varpi_L`, `varpi_D`, `vartheta`, `rbar` (classe `Parametres`, l. 106 à 153). Lecture de la grille à (ν_G = 1,15, π̄, n_a = 12), clés de `valeurs` (l. 989).
- **`sonde130b.py`** : nombre de valeurs publiées en écart, Δr̄_α de #80, plus grand résidu, caisse des entreprises.
- **`tableau.py`** : tableau ci-dessous, et recensement des valeurs publiées qui changent entre A et P, par section.
- **`dist.py`** : distribution sous Δϱ = −2 points (`etat_stationnaire(par, r_neutre=r̄ − 0,02, rho_bar_L=ϱ_L de l'état, controler=False)`, comme au § 3.4.1).
- **`wlong.py`** : variante ϖ_D = 0.
- **`divbk.py`** : variation du dividende de la banque et du revenu disponible de A à P ; marge d'existence sous écarts nuls.
- **`ecarts.py`**, **`theta.py`**, **`dbn.py`** : lecture des séries de DBnomics et calcul des moyennes du § 4.2.
- Commande type : `uv run python -I <scratchpad>/outils130/<sonde>.py '<variantes en JSON>'`. Sorties : `<scratchpad>/sortie_v1.txt`, `sortie_v2.txt`, `sortie_tableau.txt`.
- **Contrôles** : à (μ̄, ζ) = (0,25 ; 4), la sonde retrouve les 449 valeurs publiées « égal » (0 en écart). À A, elle retrouve les 185 valeurs en écart du § 3.4.3, la distribution 0,88598 / 0,82751 / 0,72390 et, sous −2 points, 0,86624 / 0,79812 / 0,68114. Plus grand résidu à P : 4,79e−15.

#### 4.4.2 `tab:etat-stationnaire` et valeurs résolues (n_a = 12, ν_G = 1,15) : P contre A, et contre `main`

Une seule cause pour toutes les lignes qui changent de A à P, notée **(ϑ)** : E^Bk = ϑ L monte de 0,05 L, soit +0,031127 année de PIB à 2 %. Par l'identité C42, B − M^G = V_H + D_F − (1 − ϑ) L, la dette publique consolidée monte d'autant, moins une baisse de la richesse des ménages : ΔV_H = −0,000223. Celle-ci vient du dividende de la banque : ΔDiv_Bk = (i_CB − n_a γ̄) ΔE^Bk/n_a < 0, puisque i_CB = 3,02 % est sous la croissance nominale (n_a γ̄ = 3,967 %). D'où ΔD_c = +0,031127 − 0,000223 = +0,030904, conforme à la mesure. θ_G, résolu, monte parce que C baisse à production inchangée. Le déficit de Domar, n_a γ̄ D_c, et le canal rentier, proportionnel à D_c, montent d'environ 12 % (+12,03 % et +12,07 % à 2 %). **Vérifiée** (bouclage à la main contre la sortie).

| Grandeur | `main` 0 / 2 / 10 % | A 0 / 2 / 10 % | **P** 0 / 2 / 10 % | P − A à 2 % | Explication |
|---|---|---|---|---|---|
| Capital (a), (b), (c) ; part salariale ; I/PIB | voir § 1.4.3 | § 1.4.3 | = A | 0 | ϑ n'entre pas dans les blocs 2 à 6 |
| r̄, i_CB, taux réel restitué, ϱ_L, inflation | 1,00 ; 1,00 / 3,02 / 11,10 ; … | = `main` | = `main` | 0 | r̄, ϖ_L inchangés |
| θ_G | 0,218474 / 0,219573 / 0,219568 | = `main` | **0,218765 / 0,219791 / 0,219626** | +0,000219 | (ϑ) : C plus bas |
| Masse monétaire | 0,81917 / 0,81658 / 0,81108 | 0,81950 / 0,81723 / 0,81295 | **0,81921 / 0,81701 / 0,81289** | −0,00022 | (ϑ) : V_H plus bas |
| Dette consolidée | 0,09884 / 0,25674 / 0,51013 | 0,09888 / 0,25695 / 0,51130 | **0,13862 / 0,28785 / 0,52800** | +0,03090 (+12,0 %) | (ϑ) : C42 |
| Dette brute | 0,11987 / 0,27849 / 0,53645 | 0,11992 / 0,27871 / 0,53769 | **0,15972 / 0,30973 / 0,55457** | +0,03101 | (ϑ) |
| Dette brute, ν_G = 1 | 0,11712 / 0,27564 / 0,53299 | 0,11717 / 0,27587 / 0,53421 | **0,15696 / 0,30687 / 0,55107** | +0,03100 | (ϑ) |
| Dette brute affichée, % | 12,1 / 28,5 / 57,1 | 12,1 / 28,5 / 57,2 | **16,1 / 31,6 / 59,0** | +3,2 pt | (ϑ) |
| Déficit (Domar), % du PIB | 0,1959 / 1,0185 / 5,9005 | 0,1960 / 1,0193 / 5,9141 | **0,2747 / 1,1419 / 6,1072** | +0,1226 pt | (ϑ) : n_a γ̄ D_c |
| Solde primaire, % du PIB | −0,0971 / −0,2432 / −0,2381 | −0,0971 / −0,2433 / −0,2386 | **−0,1361 / −0,2726 / −0,2464** | −0,0293 pt | (ϑ) |

**Valeurs résolues de `tab:criteres-j3` (π̄ = 2 %)** qui changent de A à P :

| N° | `main` | A | **P** | Explication |
|---|---|---|---|---|
| B16 masse monétaire | 0,81658 | 0,81723 | **0,81701** | (ϑ) |
| B17 fonds propres E^Bk/L | 0,1 | 0,1 | **0,15** | #130, par définition |
| B19 encaisse du Trésor | 0,021748 | 0,021765 | **0,021875** | (ϑ) : M^G suit les paiements bruts, dont les intérêts de B |
| B20 titres de la banque | 0,27849 | 0,27871 | **0,30973** | (ϑ) |
| B21 dette consolidée | 0,25674 | 0,25695 | **0,28785** | (ϑ) |
| B22 déficit public | 1,0185 % | 1,0193 % | **1,1419 %** | (ϑ) |

Inchangées de A à P (écart relatif ≤ 3e−15) : B1 à B15, B18 (2 et 1 points), B24 à B26. B10 (0,980566) et B11 (3,8900 %) ne bougent pas : V_H et YD baissent dans la même proportion (règle de richesse). **Vérifiée.**

**Contre `main`** : le tableau est celui du § 1.4, plus les lignes ci-dessus. Aucune ligne n'est due à ϖ_L, ϖ_D ni r̄, inchangés.

#### 4.4.3 Autres valeurs publiées (surface de `docwriter`)

233 valeurs publiées changent entre A et P (284 en écart à la publication actuelle, contre 185 à A). Répartition :

| Endroit | Valeurs | Endroit | Valeurs |
|---|---|---|---|
| `sec:banque-stationnaire` | 66 | `sec:banque-restitution` | 6 |
| `sec:finances_publiques-stationnaire` | 51 | `sec:banque-conditions` | 5 |
| `tab:etat-stationnaire` | 24 | `sec:finances_publiques-restitution` | 4 |
| `sec:banque_centrale-stationnaire` | 13 | fiche 9, § 3.C et § 9.6 | 4 |
| `sec:finances_publiques-emission` | 12 (+3 avec `tab:calibration`) | `sec:finances_publiques-transferts`, fiche 9 § 6.3, fiche 9 § 3.C, `sec:banque-resultat` | 2 chacun |
| `sec:banque_centrale-conditions` | 12 (+6 avec la fiche 9 § 3.Q, +1 avec la fiche 8 § 9.6) | `sec:finances_publiques-impots`, fiche 8 § 9.6 | 1 chacun |
| `sec:banque_centrale-restitution` | 9 | `sec:finances_publiques-depense` | 7 |

Phrases à reprendre en plus des nombres :
- `sec:banque-stationnaire` : « Avec des écarts nuls, elle échoue […] marge de −0,000947 à π̄ = 2 % » devient −0,001421 (ϑ (i_CB − n_a γ̄), sonde `divbk.py` ; −0,001473 et −0,000700 à 0 et 10 %) ; « fonds propres ϑL : 0,08004 ; 0,06220 ; 0,03344 » ; la dépendance à n_a de la part distribuée (0,841495 / 0,841966 / 0,842146 pour n_a = 4, 12, 52) ; la décomposition de Δ(dette consolidée) entre 2 et 10 % (terme −ϑΔL) ;
- `sec:banque-conditions` : le couplage ∂Div_Bk/∂I^plan = −ϑ lv\* passe de −0,04 à **−0,06** ;
- `tab:calibration` : sources de ϖ_L, ϖ_D, ϑ, r̄ (texte au § 4.10) ;
- fiche 7 et fiche 8 : « rendement des fonds propres de 37 % » ;
- valeur indicative `fonds_propres_vises` de la table du bloc 7 et défaut `Parametres.vartheta` du script.

**#80** : Δr̄_α passe de 0,2966 point (A) à **0,2764** point (P), et l'écart de C/Y_o de 0,6308 à 0,6904 point. Les deux restent au-dessus du seuil de 0,1 point : #80 reste en échec attendu, sans succès inattendu. **Vérifiée** (valeurs du script ; tests non exécutés à P).

### 4.5 Conditions d'existence au point fixe (P : μ̄ = 0,60, ζ = 8, ϑ = 0,15 ; n_a = 12, ν_G = 1,15)

| Condition | π̄ = 0 | 2 % | 10 % | Verdict |
|---|---|---|---|---|
| **Dividende stationnaire de la banque** (`sec:banque-stationnaire`) : ϑ i_CB + ϖ_L + ϖ_D D/L − ϑ n_a γ̄, par an | 0,028758 (A : 0,029253) | 0,031703 (0,032180) | 0,043554 (0,043789) | **tenue** ; baisse de ϑ(i_CB − n_a γ̄) = −0,00048 à 2 % |
| Même marge, écarts nuls (pour mémoire, non admissible) | −0,001473 | −0,001421 | −0,000700 | échoue, comme publié |
| Div_F ≥ 0 : Div_F/(p v), % | 22,21 | 22,38 | 22,60 | tenue, = A |
| Coefficient de richesse ; ν_H λ_H < 1 (0,4) | = A | | | tenus, indépendants de #130 |
| D1 | 0,99250 | 0,99221 | 0,98852 | tenue, = A |
| D2 | 0,99904 | 0,99712 | 0,98946 | tenue, = A |
| Marge du plafond de E1 | 0,13531 | 0,16319 | 0,31515 | tenue (A : 0,13375 / 0,15979 / 0,31057) |
| Plafond de E6 (valeur) | 1,13469 | 1,09346 | 0,91028 | A : 1,13823 / 1,09859 / 0,91571 ; nature inchangée |
| Caisse des entreprises, phase 4, (D_F + ΔL − WB)/D_F | 0,6947 | 0,6992 | 0,7063 | tenue, = A au bit |
| Domaine : ϑ > 0 ; r̄ > −5 % (C51) ; ϖ sans condition de signe | 0,15 ; 0,01 | | | tenus, sans écrêtage |
| `calculer` aux 18 points de la grille et au point ν_G = 1 | aucun refus | | | **vérifiée** |

Mêmes conditions pour les variantes du § 4.3 : toutes tenues, sauf le refus du script sous ϖ_D = 0. **Aucune condition d'arrêt du plan n'est rencontrée** : aucune valeur hors domaine, aucune équation à changer, aucune vitesse en jeu.

### 4.6 Grandeurs publiées sans cible

| Grandeur (définition du script) | `main` = A, 0 / 2 / 10 % | **P**, 0 / 2 / 10 % | Observé, pour mémoire (non une cible) |
|---|---|---|---|
| Marge nette d'intérêt n_a Π^Bk/(L + B_Bk + Res), % par an, actif d'ouverture | 2,717 / 2,497 / 2,126 | **2,645 / 2,514 / 2,294** | MSU, établissements importants, `I2120` « Net interest margin » : 1,45 % (moyenne des T4, 2015–2024 ; 1,21 à 1,60). Définition de la BCE non relue |
| Rendement des fonds propres n_a Π^Bk/E^Bk, % par an | 31,23 / 36,15 / 55,36 | **21,15 / 25,10 / 40,60** | MSU, `I2003` « Return on equity » : 5,96 % (moyenne des T4, 2015–2024 ; 1,53 à 9,54) |
| Part distribuée Div_Bk/Π^Bk | 0,93655 / 0,89025 / 0,79105 | 0,90631 / 0,84197 / 0,71512 | non lue |
| Π^Bk, % du PIB | A : 2,5010 / 2,2503 / 1,8553 (`main` : 2,4999 / 2,2485 / 1,8510, effet (P) du § 1) | 2,5407 / 2,3441 / 2,0412 | non lu |

Le rendement des fonds propres reste quatre fois au-dessus de l'observé à P. C'est attendu : le modèle n'a ni coûts d'exploitation, ni pertes sur crédit, ni impôt sur la banque. C'est l'artefact déjà déclaré (fiche 7, critère 17). La marge nette d'intérêt du modèle dépasse l'observée d'environ un point. Le modèle applique ϖ_L à tous ses crédits, alors que le bilan observé contient des crédits immobiliers, des titres et de l'interbancaire. Les observations sont des **faits vérifiés** (DBnomics, 16/11/2026), leur comparaison au modèle une **lecture**.

### 4.7 Effets sur #55 (distribution) et sur la caisse

**Distribution de #55.** ϑ n'entre pas dans le bloc 6. À P, la distribution est **identique à A au bit** : 0,88598 / 0,82751 / 0,72390 à Δϱ = 0 ; 0,86624 / 0,79812 / 0,68114 sous Δϱ = −2 points, ζ = 8. La borne haute à π̄ = 0 (**0,886**, à 0,014 de 0,9) est inchangée. **Vérifiée** (`dist.py`).

Sensibilité de la borne haute aux autres paramètres de #130 (π̄ = 0) :
- r̄ = 0,005 : 0,88741 (+0,0014) ; r̄ = 0,015 : 0,88452 ; r̄ = 0,02 : 0,88302. Un r̄ plus bas rapproche de 0,9 : intérêts plus bas, Div_F plus haut.
- ϖ_L = 0,0165 (et ϖ_D = 0,0085) : 0,88735 (+0,0014).
- En extrapolant linéairement (**hypothèse**, non mesurée par bissection), la borne de 0,9 serait atteinte vers ϖ_L ≈ −1,6 % ou r̄ ≈ −3,9 %, loin des valeurs lues.

Le critère de #55 tient donc à P, et sous toutes les variantes du § 4.3.

**Caisse.**
- Caisse des entreprises de phase 4 à l'état stationnaire : identique à A au bit (0,6947 / 0,6992 / 0,7063). Ni ϑ, ni ϖ, ni r̄ n'entrent dans D_F, ΔL ni WB. **Vérifiée** pour ϑ et ϖ ; pour r̄, valeurs `caisse_DF4` identiques (sortie `sonde130b.py`).
- Frontière de caisse du pas 0 (§ 2.3.3) : déjà mesurée insensible, au plus 0,004 par an (ϑ = 0,08 et 0,15 donnent 3,533060). P ne la déplace pas. **Vérifiée** (mesure du § 2.3.3).
- Frontière de S6 de #143 : Δϱ_lim = 13,231/ζ, indépendante de #130 (P215). r̄ n'y entre pas, puisque Δϱ est un écart à la norme. **Vérifiée** par P215 pour ϖ et ϑ ; pour r̄, **déduite**.

**Point pour `macro`** (dividende et distribution) : le dividende de la banque baisse de 1,69 / 1,48 / 0,54 % à π̄ = 0 / 2 / 10 % à P (ΔDiv_Bk = (i_CB − n_a γ̄) ΔE^Bk/n_a < 0). Le revenu disponible baisse de 0,030 / 0,023 / 0,007 % du PIB (−0,034 % de YD à 2 %), et θ_G résolu monte de 0,000219 à 2 %. **Vérifiée** (`divbk.py`). C'est le seul canal de ϑ vers l'économie réelle à l'état stationnaire. À confirmer par `macro`.

### 4.8 Questions au mainteneur

1. **ϑ.** 0,15 (CET1 du MSU, 2015–2024, 14,75 %, dénominateur Bâle III déclaré contesté), 0,10 (statu quo, sous toutes les observations lues), ou 0,08 (minimum de Bâle 1988) ? *Avis : **0,15**.* Il change l'état de référence : dette consolidée +12 %, déficit +0,12 point de PIB, ROE de 36 % à 25 %. Il ne change ni la distribution de #55, ni la caisse.
2. **ϖ_D et la fenêtre.** 0,01, sur les fenêtres de taux positifs (0,85 et 1,93), ou la moyenne longue (≈ 0, que le script refuse aujourd'hui) ? *Avis : **0,01**, la moyenne longue déclarée et écartée pour cause de régime.* La dépendance de l'écart au niveau du taux est une limite de B2, à consigner (issue proposée au § 4.11), sans changer d'équation dans cette branche.
3. **ϖ_L** : 0,02, inchangé, sur l'écart des affaires nouvelles (2,09, 2003–2024). *Avis : oui.*
4. **r̄** : 0,01, inchangé, déclaré « contesté ; fourchette lue de −0,5 % à +1,9 % (BCE 2025 ; FOMC 09/2026) » ? Ou 0,015 pour tenir la liste O1 de la première tentative (taux réel de 1,5 à 3 %) ? *Avis : **0,01**.* La liste O1 n'est pas une source, et 1,5 % sort de la fourchette de la zone euro lue. Le verdict « O1 non tenu à r̄ = 1 % » reste publié (D3). La liste O1 est « à confirmer par le mainteneur au jalon J3 » (`docs/exigences.md`, l. 44) : la question est à vous.
5. **Zone de référence.** Toutes les sources de la branche sont de la zone euro (#92, #55, #130), sauf le FOMC, lu pour la seule fourchette de r̄. *Avis : garder la zone euro ; le FOMC élargit la fourchette, sans fixer la valeur.*

### 4.9 Points pour `jeu` (je ne les tranche pas)

- Un rendement des fonds propres de la banque de **25 %** (contre 36 %) reste irréaliste (≈ 6 % observé). L'aide doit dire qu'il s'agit d'un rendement **avant coûts d'exploitation**, que le socle n'a pas. Sinon, l'indicateur de la fiche détaillée de la banque induira le joueur en erreur.
- La dette publique de référence affichée passe de **28,5 % à 31,6 % du PIB** à π̄ = 2 %, sans aucune décision du joueur : c'est le passif de l'État qui finance les fonds propres de la banque (C42). À expliquer si l'aide décompose la dette.
- Les écarts de taux affichés (2 et 1 points) sont désormais adossés à une source ; le libellé peut le dire.
- Sous un taux directeur négatif (r̄ bas ou désinflation), le modèle rend i_D < 0 sur tous les dépôts. Les données lues montrent que les banques ne l'ont pas fait. Un joueur qui pousse le taux sous zéro verra des dépôts à rendement négatif que l'expérience ne confirme pas (limite B2, § 4.8 q. 2).

### 4.10 Surface pour `coder` et `docwriter` (rangs 3 à 9)

- **Table du bloc 7** (`nations.moteur.parametres.banque`) : `fonds_propres_vises` 0,10 → 0,15 et sa source ; sources de `ecart_taux_credit` et `ecart_taux_depots`, valeurs inchangées. **Table du bloc 8** : source de `r_bar`, valeur inchangée. Défaut `Parametres.vartheta` du script et déclarations de `varpi_L`, `varpi_D`, `vartheta`, `rbar` (l. 162 et 171 à 173). Égalité tenue par `test_valeurs_indicatives_egales_a_celles_du_script` et `tests/unitaires/test_parametres_des_blocs_7_et_8.py`.
- **Texte de source proposé pour `tab:calibration`** :
  - ϖ_L : « BCE, MIR, coût composite de l'emprunt des SNF, affaires nouvelles, moins EONIA puis €STR, zone euro, moyenne mensuelle 2003–2024 : 2,09 points (encours : 2,30) ; DBnomics, consulté le 16/11/2026 » ;
  - ϖ_D : « même source, taux des dépôts des ménages et des SNF pondéré par les encours de la BSI : 0,85 point (2003-01 à 2008-08) et 1,93 point (2022-07 à 2024-12) ; moyenne 2003–2024 de −0,05 point, dominée par les taux négatifs, écartée ; écart dépendant du régime (limite de B2) » ;
  - ϑ : « BCE, statistiques de supervision, CET1 des établissements importants, moyenne 2015T3–2024T4 : 14,75 % des actifs pondérés ; égal à fonds propres sur crédits sous les pondérations de Bâle 1988 (§ 44 et annexe 2, lus) ; dénominateur Bâle III plus petit, écart non mesuré, contesté » ;
  - r̄ : « choix de conception ; fourchette lue de −0,5 % à +1,0 % (BCE, *Economic Bulletin* 1/2025, fin 2024) et de 0,9 % à 1,9 % (FOMC, SEP du 16/09/2026, long terme, nominal moins 2 %) ; niveau contesté (critère 23) ».
- **Tests** : la nullité de i_D à π\* = 0 reste valide (r̄ = ϖ_D) ; la liste des nullités est inchangée. B17 vaut 0,15. Le couplage publié vaut −0,06.
- **Concordance** : aucun label ajouté ni retiré (90).

### 4.11 Issue proposée (création sur accord)

- **Titre** : Écart des dépôts dépendant du niveau du taux directeur (bêta des dépôts) : forme B2 à instruire
- **Libellés** : `needs-triage`
- **Corps** :

> *Rédigé par l'agent monnaie (IA).*
>
> **Constat** (instruction de #130, 16/11/2026, `docs/blocs/calibration.md` § 4.2 (b)). L'écart entre le taux du jour le jour et le taux moyen des dépôts des ménages et des SNF de la zone euro (BCE, MIR et BSI, via DBnomics) dépend du régime : +0,85 point en 2003-01 à 2008-08, −0,74 point en 2014-06 à 2022-06 (taux négatifs non reportés sur les dépôts), +1,93 point en 2022-07 à 2024-12. La forme B2 (i_D = i_CB − ϖ_D, ϖ_D constant) impose un bêta des dépôts de 1 et des taux de dépôt négatifs sous un taux directeur négatif.
>
> **À faire.**
> - Lire la littérature sur le canal des dépôts, notamment Drechsler, Savov et Schnabl (2017, *QJE*), et dire si une forme à bêta inférieur à 1 est nécessaire à la lisibilité ou à la justesse du levier de taux.
> - Dire ses effets sur la condition d'existence du dividende de la banque, sur la condition C43 (rendement marginal de la richesse égal au taux directeur) et sur le canal rentier.
>
> **Hors périmètre** : la calibration de ϖ_D (#130), faite sur les fenêtres de taux positifs.
>
> **Liens** : #130, `sec:banque-taux`, fiche 7 critère 17, J4 (levier de taux) ou J6 (plancher des taux).

### 4.12 Statut des conclusions

- **Vérifiées** (commande et sortie, ou source citée) :
  - écarts du crédit et des dépôts, toutes fenêtres (MIR, BSI, EONIA, €STR ; raccord de 8,5 points de base) ;
  - Bâle 1988 (§ 44, annexe 2) ; CET1 et solvabilité du MSU ; rapports comptables de la BSI ;
  - ROE et marge nette observés (MSU) ;
  - fourchettes de r\* de la BCE (2024 et 2025, citations courtes de l'outil) et projection de long terme du FOMC (09/2026) ;
  - tableaux des § 4.3 à 4.7 ; mécanisme (ϑ) bouclé à la main ;
  - invariance de la distribution et de la caisse ;
  - #80 toujours en échec ; refus du script sous ϖ_D = 0 et sa cause.
- **Hypothèses** :
  - lecture de ϑ comme ratio CET1 sous pondérations de Bâle I ;
  - extrapolation linéaire de la borne 0,9 de la distribution ;
  - mécanisme du solde primaire selon r̄ − g.
- **Déduite** : indépendance de la frontière de S6 à r̄.
- **Non vérifiées** :
  - densité des actifs pondérés, donc l'ampleur de l'écart de dénominateur de ϑ ;
  - définition exacte de `I2120` et `I2003` ;
  - auteurs de l'encadré de 2025 ;
  - Drechsler et al. (2017), Holston, Laubach et Williams, FMI 2023, BRI ;
  - bancs d'empreintes et trajectoires choquées à P (rang 8) : le maintien du plafond des bancs D et BF n'est pas vérifié ;
  - tests du dépôt exécutés à P.

### 4.13 Avis de `macro` (expert consulté, 16/11/2026)

Lecture du § 4 et du script (`outils/etat_stationnaire.py`, l. 449 à 466), sans réexécution des sondes :
- **Mécanisme et bouclage (§ 4.4.2) : conforme.** X0 = −L + D_F + E^Bk, donc D_c = D_H + X0 et V_H = D_H ; Div_Bk = Π^Bk − γ̄ E^Bk. ΔD_c = +0,031127 − 0,000223 en découle exactement (**vérifiée**, lecture du code). Retouches de rédaction, prospectives (le texte de `monnaie` reste publié) : (1) « seul canal » est trop fort : s'y ajoutent deux effets de second ordre (ϖ_D ΔD_H et la taxe t_cou sur D_c) et la composition C/G (θ_G) ; (2) le revenu disponible baisse de 0,023 % du PIB et non de 0,0295 %, parce que l'impôt τ_H = 0,25 en absorbe une part (0,0295 × 0,75 ≈ 0,022 ; **hypothèse**, calcul à la main, non décomposé).
- **Dette de référence à 31,6 % du PIB : aucune objection.** Les bandes de B20 à B22 et le critère 15 portent sur l'écart à la valeur résolue, non sur un niveau ; la fiche 9, critère 22, signalait la dette « basse, environ 26 % (C-3) » (**vérifiée**). Pour `docwriter` : la forme fermée du critère 5 (b) contient E^Bk/(12 PIB) ; citer ϑ parmi les paramètres qui fixent le ratio (critère 5 (c)). Pour `jeu` (hypothèse) : un paramètre prudentiel qui déplace la dette de 3 points peut surprendre le joueur.
- **Signe du solde primaire (§ 4.3) : retouche.** À l'état stationnaire, le solde primaire vaut (i_CB/n_a − γ̄) D_c par pas, i_CB annuel composé et γ̄ mensuel : son signe suit i_CB/n_a − γ̄, non r̄ − g. Recalcul : +1,51e−5 par mois à r̄ = 0,02 et π̄ = 0 ; +6,94e−5 à r̄ = 0,015 et π̄ = 10 %, positif alors que r̄ < g (effet de convention de composition, croissant avec π̄). La phrase « le signe du solde primaire stationnaire suit celui de r̄ − g, à la dette consolidée près » est donc inexacte ; la lecture passe de « hypothèse » à « **vérifiée** (identité) » sous la forme corrigée. Recalcul refait par la session (`python3`, mêmes valeurs).

### 4.14 Décisions du mainteneur sur la section (16/11/2026)

- Question 1 : **ϑ = 0,15** retenu comme valeur proposée de la table soumise à M34 (CET1 du MSU ; écart de dénominateur déclaré contesté) (P225).
- Questions 2 à 5 : ϖ_L = 0,02, ϖ_D = 0,01 (fenêtres de taux positifs ; moyenne longue écartée) et r̄ = 0,01 (contesté, fourchette lue −0,5 à 1,9 %) inchangés et sourcés ; zone euro de référence, FOMC pour la seule fourchette de r̄ (P226).
- Issue proposée au § 4.11 : créée, #167 (bêta des dépôts, limite de B2), hors branche (P227).
- Retouches de `macro` (§ 4.13) : suivies sous la délégation P211 dans le texte publié par `docwriter`.

## 5. #62 — Richesse visée ν_H et vitesse λ_H (bloc 5, ménages)

*Instruite par `macro` (expert pilote) le 16/11/2026, rang 1 de la branche « calibration » (PR #162). Dépôt à `1aaba84`, puis `7f433d6` (décisions P228 à P231) : ces commits ne diffèrent de `d865683` que par des fichiers `docs/`, sans effet sur les mesures. `git status` est vide avant et après. Les chiffres du modèle viennent de sondes hors dépôt (méthode au § 5.4.1). Elles appellent, sans les modifier, `outils/etat_stationnaire.py`, `outils/maquette_conjointe.py`, `tests/invariants/socle_partiel.py`, `tests/invariants/test_socle_complet.py` et les fonctions de `tests/invariants/test_menages.py`. Ce sont des résultats du modèle, pas des faits. Les faits portent leur source et leur date. Chaque conclusion est marquée **vérifiée**, **hypothèse** ou **non vérifiée**. La base est la table proposée : μ̄ = 0,60 (§ 1), ζ = 8 (§ 3) et ϑ = 0,15 (§ 4, P225), avec ϖ_L, ϖ_D et r̄ inchangés. Elle est notée **P** ; l'état proposé, P avec ν_H = 1,1, est noté **N**.*

### 5.1 Grandeurs visées et correspondance avec le modèle

| Grandeur | Définition dans le modèle | Unité | Dénominateur | Fenêtre |
|---|---|---|---|---|
| ν_H (H3) | richesse visée V\*_H = ν_H n_a (YD^e − π^{∗,pas} V_H) ; à l'état stationnaire sous C2, V_H/(n_a YD^HS) = ν_H exactement | an | 12 × YD^HS du pas (revenu de Haig-Simons) | état stationnaire |
| B10 (`tab:criteres-j3`) | V_H/(12 YD) = ν_H/(1 + ν_H n_a π^{∗,pas}) | années de revenu disponible nominal | 12 × YD du pas | ouverture |
| λ_H (H4) | vitesse de rappel de la richesse vers sa cible, λ_H/n_a par pas ; propension d'impact α_Y = 1 − ν_H λ_H (forme réduite, fiche 5, § 9.1) | par an, taux de flux | — | — |
| Part propre d'un transfert (critère 12 (d)) | Σ_{tours 1 à 12} ΔC / Σ transferts, transfert de 1 % du YD stationnaire aux tours 1 à 12, bloc seul, i_D = 3 % (protocole de `test_part_d_un_transfert_depensee_en_12_tours`) | fraction | transferts cumulés | 12 tours |
| Dépense cumulée d'une aubaine | Σ_{tours 1 à h} ΔC / aubaine, aubaine de 1 % du YD stationnaire au seul tour 1, même bloc seul | fraction | aubaine | h = 3 tours (un trimestre) et 12 tours |

**Traits du modèle que la définition empirique doit respecter** (vérifiés sur `etat_stationnaire`, l. 449 à 466, et `sec:menages`) :

| Trait | Dans le modèle | Conséquence pour la source |
|---|---|---|
| Actifs des ménages | Dépôts seuls : B_H ≡ 0 au socle ; ni titres, ni actions, ni fonds de pension, ni logement (M27, encadré `portee`) | Numérateur : **numéraire et dépôts (F.2)** des ménages. Les actions, parts de fonds et droits à pension ne sont pas de la richesse du ménage du modèle : le capital des entreprises (V_F) n'est détenu par aucun secteur |
| Passifs des ménages | Aucun crédit aux ménages (J6, M22) | Rapport **brut** des dépôts, pas net des crédits : le modèle n'a pas d'hypothèque à retrancher. Le rapport net (F.2 − F.4 passif) est publié pour mémoire |
| Revenu | YD = WB + Tr − T_H + i_D D_H/n_a + Div_F + Div_Bk, sans revenu mixte, sans loyers imputés, sans consommation de capital fixe des ménages | **Revenu disponible brut (B.6g)** des ménages et ISBLSM (S14_S15). Le revenu net (B.6n) est publié en variante. Écart déclaré : B.6g contient l'excédent d'exploitation des logements et le revenu mixte |
| Revenu de Haig-Simons | ν_H porte sur YD^HS = YD − π^{∗,pas} V_H. Le revenu observé est nominal | Le rapport observé R se compare à **B10**. On en tire ν_H = R/(1 − R n_a π^{∗,pas}), à π\* = 2 % (n_a π^{∗,pas} = 0,019819) |
| Épargne | Toute l'épargne des ménages est une accumulation de dépôts : 1 − C/YD = ΔV_H/YD | Contrôle de cohérence stock-flux : **acquisition nette de F.2 / B.6g**. Le taux d'épargne brut observé (B.8g), qui finance aussi le logement et les autres actifs, n'est pas comparable |
| Aubaine | Un transfert du tour n entre dans le plan au tour n + 1 (délai de H2) ; une seule marchandise, durables compris | Propension à dépenser un revenu transitoire, **dépense totale** (durables compris), sur le trimestre de réception |

**Ce que fait chaque paramètre à l'état stationnaire** (formes de `etat_stationnaire`, l. 452 à 466) :
- **ν_H** fixe D_H = ν_H n_a ((1 − τ_H) A0′ + Tr)/D1. La dette consolidée vaut D_c = D_H + X0 (C42), où X0 = −L + D_F + E^Bk ne dépend pas de ν_H. **L'État porte donc la richesse supplémentaire des ménages, euro pour euro.** θ_G se résout ensuite par la fermeture du marché des biens (#44, lecture (e)).
- **λ_H** n'entre que dans la condition de domaine (`controler_domaine`, l. 264 et 275) : aucune grandeur de l'état stationnaire ne le lit.

### 5.2 Sources lues et citées

**(a) Richesse liquide des ménages, lue.** Eurostat, comptes annuels des secteurs (SEC 2010), consultés le 16/11/2026 par l'API de diffusion (`ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data`), sonde `ratios62.py` :
- `nasa_10_f_bs` (« Financial balance sheets - annual data », mise à jour du 16/11/2026) : S14_S15, millions d'euros, non consolidé, actifs F.2 (numéraire et dépôts), F (actifs financiers), BF90 (actifs financiers nets), passif F.4 (crédits) ;
- `nasa_10_nf_tr` (« Non-financial transactions - annual data », même date) : S14_S15, prix courants, B.6g et B.6n (revenu disponible brut et net) ;
- zone : EA21. La requête ne rend pas d'agrégat EA20 pour `nasa_10_nf_tr`, comme au § 3.2. L'UE à 27 est publiée en contrôle ;
- fenêtre : la série des bilans commence en 2001. Moyenne 2001–2023 (23 ans), même borne finale que les § 1 et 3.

| Rapport (EA21), en années | Moyenne 2001–2023 | Min ; max | 2010–2024 | UE à 27, 2001–2023 |
|---|---|---|---|---|
| **Numéraire et dépôts / revenu disponible brut, F.2/B.6g** | **1,076** | 0,884 (2001) ; 1,279 | 1,154 | 1,035 |
| F.2 / revenu disponible net, F.2/B.6n | 1,154 | 0,939 ; 1,381 | 1,242 | 1,107 |
| Dépôts nets des crédits, (F.2 − F.4)/B.6g | 0,163 | 0,037 ; 0,331 | 0,219 | 0,115 |
| Actifs financiers nets, BF90/B.6g | 2,309 | 1,859 ; 3,004 | 2,512 | 2,291 |
| Actifs financiers bruts, F/B.6g | 3,328 | 2,802 ; 4,051 | 3,550 | 3,312 |

Valeurs brutes de contrôle : F.2 = 4 227 219 et B.6g = 4 781 855 millions d'euros en 2001 (rapport 0,884) ; 10 488 658 et 9 101 843 en 2023 (1,152). Le rapport monte presque continûment sur la fenêtre. Faits, **vérifiés** (requête et calcul).

**(b) Contrôle stock-flux, lu.** `nasa_10_f_tr` (« Financial transactions - annual data », mise à jour du 16/11/2026), S14_S15, acquisition nette d'actifs F.2, EA21, rapportée à B.6g : **4,32 %** en moyenne 2002–2023 (22 ans ; min 1,15, max 9,76), 4,01 % sur 2010–2024. Pour mémoire, le taux d'épargne brut B.8g/(B.6g + D.8) vaut 13,59 % (2001–2023) ; il n'est pas comparable, puisqu'il finance aussi le logement et les autres actifs (§ 5.1). Faits, **vérifiés** (sonde `flux62.py`).

**(c) Propension à dépenser un revenu transitoire, lue** (pages de résumé de `www.nber.org`, lues le 16/11/2026 par WebFetch, qui ne rend que des citations courtes) :
- J. A. Parker, N. S. Souleles, D. S. Johnson et R. McClelland, « Consumer Spending and the Economic Stimulus Payments of 2008 », NBER *Working Paper* 16684, janvier 2011 (publié dans l'*American Economic Review* en 2013, version publiée non lue). Les ménages ont dépensé « about 12-30% » des paiements en biens non durables « during the three-month period in which the payments were received ». La réponse totale, durables compris (surtout des véhicules), atteint « about 50-90% of the payments ». Le résumé lu ne précise pas séparément la période de ce second chiffre ; d'après le texte, c'est le même trimestre (**lecture à confirmer sur l'article**). États-Unis, 2008. **Vérifiée avec réserve** (résumé).
- D. S. Johnson, J. A. Parker et N. S. Souleles, « Household Expenditure and the Income Tax Rebates of 2001 », NBER *Working Paper* 10784, septembre 2004. « about 20-40 percent » des remboursements dépensés en biens non durables « during the three-month period in which their rebates were received », et « roughly another third » au trimestre suivant. États-Unis, 2001. **Vérifiée avec réserve** (résumé).
- G. Kaplan et G. L. Violante, « A Model of the Consumption Response to Fiscal Stimulus Payments », NBER *Working Paper* 17338, août 2011, révisé en janvier 2014. Repère empirique du résumé : « around 25 percent » des paiements dépensés en consommation non durable dans le trimestre. Leur conclusion est que le modèle à un seul actif liquide donne une réponse « an order of magnitude » trop faible, et qu'il faut un actif illiquide pour l'expliquer. **Vérifiée avec réserve** (résumé).

**Fourchette lue** : la dépense **totale** sur le trimestre de réception va de 0,5 à 0,9 (Parker et al.). Sur les seuls non durables, elle va de 0,12 à 0,40 (Parker et al., Johnson et al.). Les sources sont américaines et portent sur des versements **annoncés** avant d'être reçus. Le modèle n'a ni annonce, ni durables séparés, ni hétérogénéité des ménages : la correspondance est **une hypothèse**.

**(d) Non lus** (aucun chiffre n'en est tiré) :
- A. Fagereng, M. B. Holm et G. J. Natvik, « MPC Heterogeneity and Household Balance Sheets », *American Economic Journal: Macroeconomics* 13(4), 2021 (gains de loterie, Norvège). Les copies trouvées sont sur des hôtes non ouverts (`www.duo.uio.no` a été refusé par la résolution de noms ; `ifo.de` et `swopec.hhs.se` n'ont pas été essayés, selon la consigne de l'outil). Pour la lire, il faut ouvrir l'un de ces hôtes. C'est la source la plus directe sur une aubaine de richesse **liquide**, celle que demandait l'issue.
- T. Jappelli et L. Pistaferri, « Fiscal Policy and MPC Heterogeneity », *AEJ: Macroeconomics* 6(4), 2014 : aucune version sur les hôtes ouverts (CEPR, CSEF, CFS).
- A. Fuster, G. Kaplan et B. Zafar, NBER *Working Paper* 24386 (2018) : le résumé, lu, ne donne aucun chiffre.
- C. D. Carroll, M. Otsuka et J. Slacalek (effet richesse de 2 à 10 cents par an, cité par la fiche 5, § 9.2) : **non relu** dans cette instruction.

**(e) Pour mémoire, sans cible.** Dette brute des administrations publiques (`gov_10dd_edpt1`, S13, GD, % du PIB, EA20, mise à jour du 21/10/2026) : 81,8 % en moyenne 2001–2023 (65,9 à 96,3). Le modèle n'a ni non-résidents, ni assureurs, ni détention de titres par les ménages : ce n'est **pas une cible** (§ 5.9). Fait, **vérifié**.

### 5.3 Valeurs proposées et variantes

**ν_H proposé : 1,1 an.** Le rapport F.2/B.6g de 2001–2023, 1,076, donne ν_H = 1,076/(1 − 1,076 × 0,019819) = **1,0995** à π\* = 2 %. Valeur ronde : 1,1. Le modèle donne alors B10 = 1,076531 à π̄ = 2 %, à +0,05 % de la source. **Vérifiée.**

Motifs :
- c'est la seule mesure lue dont le numérateur a la composition de V_H : dépôts seuls, sans passif ;
- **contrôle stock-flux indépendant** : à ν_H = 1,1, le taux d'épargne nominal du modèle, qui est l'accumulation de dépôts sur le revenu, vaut **4,2707 %** à π̄ = 2 %. L'acquisition nette de dépôts observée vaut 4,32 % de B.6g (2002–2023). C'est un écart de 0,05 point, sans calage sur cette grandeur. **Vérifiée** (mesure et source). Interprétation, **hypothèse** : la cohérence tient à ce que le modèle et les données ont une croissance nominale voisine ; la croissance observée n'a pas été lue ;
- à ν_H = 1, B10 vaut 0,980566, soit 8,9 % sous la source.

**λ_H proposé : 0,4 par an, inchangé.** C'est un **choix déclaré dans la fourchette lue**. À ν_H = 1,1, la dépense cumulée d'une aubaine sur 3 tours vaut 0,605, et 0,705 sur 12 tours (§ 5.5). La fourchette lue de la dépense totale sur un trimestre, 0,5 à 0,9 (Parker et al.), correspond à **0,098 ≤ λ_H ≤ 0,511** à ν_H = 1,1 (sonde `front_mpc.py`). Sur 12 tours, la dépense cumulée reste au-dessus de 0,5 sur tout le domaine ν_H λ_H < 1. **Vérifiée** (mesure ; correspondance : hypothèse).

Motifs : la fourchette lue est large, et sa correspondance imparfaite (versements annoncés, données américaines, hétérogénéité). Aucune source lue ne départage 0,3 et 0,4. Garder 0,4 évite de changer les trajectoires sans fait nouveau. λ_H ne change pas l'état stationnaire (§ 5.4.5).

| Variante | ν_H ; λ_H | Source ou motif | B10 (2 %) | Dette brute affichée, 0 / 2 / 10 % | Part 12 (d) | Aubaine, 3 tours | Rayon C62, φ = 0, 2 % | Avis |
|---|---|---|---|---|---|---|---|---|
| P (statu quo de #62) | 1 ; 0,4 | indicative, sans source | 0,980566 | 16,1 / 31,6 / 59,0 | 0,6280 | 0,643 | 1,000438 | 8,9 % sous la source |
| ν_H = 1,05 | 1,05 ; 0,4 | milieu entre statu quo et source | 1,028595 | 19,5 / 35,0 / 62,5 | non relevée | non relevée | non relevé | Sans motif propre |
| **N, proposée** | **1,1 ; 0,4** | **F.2/B.6g, EA21, 2001–2023** | **1,076531** | **22,8 / 38,4 / 66,0** | **0,5966** | **0,605** | **1,000995** | **Recommandée** |
| N, λ_H bas | 1,1 ; 0,3 | centre de la fourchette de Parker et al. (aubaine sur 3 tours : 0,701) | 1,076531 | = N | 0,6666 | 0,701 | non relevé (1,001020 à λ_H = 0,35) | Variante si le mainteneur veut le centre de la source |
| ν_H revenu net | 1,18 ; 0,4 | F.2/B.6n (1,154), ou F.2/B.6g sur 2010–2024 (1,154) | 1,153035 | 28,2 / 43,8 / 71,7 | ≈ 0,57 (1,2 : 0,5651) | ≈ 0,57 (1,2 : 0,566) | 1,002847 à ν_H = 1,2 (racine réelle) | Dénominateur moins proche ; fenêtre courte |
| Actifs financiers nets | 2,4 ; 0,2 | BF90/B.6g (2,309 → ν_H = 2,42) | 2,291026 | 110,4 / 126,9 / 159,3 | 0,5215 | 0,542 | non relevé | **Écartée** : actions et droits à pension, absents du modèle ; λ_H ≤ 0,212 imposé par 12 (d) |

Mesures : sorties `sortie_tab_nu110.txt`, `sortie_variantes_nu.txt`, `sortie_part.txt`, `sortie_front_mpc.txt`, `sortie_zc.txt`. **Vérifiées.**

### 5.4 Tableau avant / après prédit

#### 5.4.1 Méthode et commandes

Sondes du scratchpad, dossier `<scratchpad>/sondes62H/`. Elles sont lancées depuis `/home/user/projet_macro` à `1aaba84`, avec `git status` vide avant et après. Commande type : `uv run python -I <scratchpad>/sondes62H/<sonde>.py <arguments>`.
- **`base.py`** : importe `outils/etat_stationnaire.py` par son chemin et appelle `calculer(replace(Parametres(), mu_bar=0.60, zeta=8.0, vartheta=0.15, nu_H=…, lambda_H=…))`. Noms de champs exacts de `Parametres` : `nu_H` (l. 128) et `lambda_H` (l. 145).
- **`tab62.py NU LAM`** : tableau main / P / N sur la grille (ν_G = 1,15, π̄, n_a = 12), clés de `valeurs`, et recensement des valeurs publiées qui changent de P à N, par section. Les valeurs en écart se comptent sur le champ `verdict` ≠ « égal ».
- **`lam62.py`** : plus grand écart relatif sur toute la grille, et nombre de valeurs publiées qui changent, pour λ_H ∈ {0,1 ; 0,2 ; 0,3 ; 0,35 ; 0,45 ; 0,5 ; 0,55 ; 0,6 ; 0,634}, à ν_H = 1 et 1,1.
- **`part62.py`**, **`front_mpc.py`**, **`reperes.py`** : chargent `tests/invariants/test_menages.py` sans le modifier et remplacent `TABLE` par un objet qui porte ν_H. Ils mesurent la part du critère 12 (d) (`_part_d_un_transfert`), la boucle propre (`_boucle_propre`), le continuum (`_ratio_converge`), et la dépense d'une aubaine au seul tour 1 (`_pas_du_bloc_seul`), ainsi que les frontières en λ_H par bissection.
- **`f5s97.py`** : lignes du § 9.7 de la fiche 5 (script, formes fermées, fonctions `revenu_attendu`, `richesse_visee`, `plan_de_la_regle`, `budget_de_consommation` du bloc).
- **`meca.py`** : niveaux de D_H, YD, C, G, T_H, Div_Bk et D_c rapportés au PIB, de P à N.
- **`s80.py`** : valeurs publiées de #80 et racines parasites de C51.
- **`c62H.py`**, **`zc2.py`**, **`phiH.py`** : `rayon_c` de `outils/maquette_conjointe.py` sous φ = 0 et φ = 1, sur `replace(mc.parametres_socle(π̄), mu_bar=0.60, zeta=ζ, vartheta=…, nu_H=…, lambda_H=…)`. Ils donnent aussi ζ_c par `frontiere`, une grille de ζ de 0,5 à 20 et φ\* par `frontiere`.
- **`serieH.py`** : la sonde `serie.py` du § 3.13, étendue à ϑ, ν_H et λ_H (sentier `socle.sentier(π̄, mu_bar, zeta, vartheta, nu_H, lambda_H)` et table `menages` variée). Elle est suivie d'**`analyse.py`** (Prony) du § 3.13.
- **Contrôles** :
  - à P, les valeurs publiées en écart sont 284, comme au § 4.4.3 ;
  - la part du critère 12 (d) à ν_H = 1 redonne 0,628 / 0,618 / 0,760 / 0,423, et la boucle propre 0,96706 / 0,98352 / 0,93419 (repères de `test_menages.py`) ;
  - le changement de cible redonne +0,5543 %, la frontière du coefficient de richesse 85,1175 % et la baisse des impôts doublés 10,12 ;
  - sous ϑ = 0,10, la maquette redonne 1,000035 et ζ_c = 8,763277, et le moteur 1,0000351 ∠ ±0,1757° (§ 3.13).
- Plus grand résidu du script à N : 6,65e−15.
- Sorties : `<scratchpad>/sondes62H/sortie_*.txt`. Sources : `<scratchpad>/dl62/`, `<scratchpad>/ratios62.py`, `<scratchpad>/flux62.py`.

#### 5.4.2 Une seule cause pour toutes les lignes qui changent de P à N (vérifiée)

Notée **(ν)**. À N, D_H monte de 10,09 % à π̄ = 2 % : +10 % par ν_H, plus 0,08 % de YD^HS, qui croît par les intérêts sur dépôts et le dividende de la banque. Par C42, D_c = D_H + X0, X0 étant inchangé, la dette consolidée monte du même montant : +0,065644 année de PIB, **+22,8 %** à 2 %. Le déficit de Domar n_a γ̄ D_c et le canal rentier, tous deux proportionnels à D_c, montent d'autant. Le ménage épargne davantage pour faire croître un stock plus grand : C/YD passe de 0,96110 à 0,95729 et C baisse de 0,124 %. θ_G, résolu, monte de 0,36 % pour fermer le marché des biens. Rien ne change dans les blocs 2 à 4 ni 6. **Vérifiée** (sortie `sortie_meca.txt` : ΔD_c = ΔD_H à toutes les décimales).

#### 5.4.3 `tab:etat-stationnaire` (n_a = 12, ν_G = 1,15) : N contre P, et contre `main`

| Grandeur | `main` 0 / 2 / 10 % | P 0 / 2 / 10 % | **N** 0 / 2 / 10 % | N − P à 2 % | Explication |
|---|---|---|---|---|---|
| Capital (a), (b), (c) ; part salariale ; I/PIB ; r̄, i_CB, taux réel restitué, ϱ_L, inflation | § 1.4.3 et § 4.4.2 | § 4.4.2 | = P | 0 | ν_H n'entre pas dans les blocs 2 à 4 ni 6 |
| θ_G | 0,218474 / 0,219573 / 0,219568 | 0,218765 / 0,219791 / 0,219626 | **0,219575 / 0,220584 / 0,220187** | +0,000793 | (ν) : C plus bas |
| Masse monétaire, années de PIB | 0,81917 / 0,81658 / 0,81108 | 0,81921 / 0,81701 / 0,81289 | **0,88503 / 0,88265 / 0,87848** | +0,065644 | (ν) : D_H |
| Dette consolidée | 0,09884 / 0,25674 / 0,51013 | 0,13862 / 0,28785 / 0,52800 | **0,20444 / 0,35350 / 0,59359** | +0,065644 (+22,8 %) | (ν) : C42 |
| Dette brute | 0,11987 / 0,27849 / 0,53645 | 0,15972 / 0,30973 / 0,55457 | **0,22568 / 0,37564 / 0,62091** | +0,065910 | (ν) |
| Dette brute, ν_G = 1 | 0,11712 / 0,27564 / 0,53299 | 0,15696 / 0,30687 / 0,55107 | **0,22291 / 0,37274 / 0,61731** | +0,065870 | (ν) |
| Dette brute affichée, % | 12,1 / 28,5 / 57,1 | 16,1 / 31,6 / 59,0 | **22,8 / 38,4 / 66,0** | +6,7 pt | (ν) |
| Déficit (Domar), % du PIB | 0,1959 / 1,0185 / 5,9005 | 0,2747 / 1,1419 / 6,1072 | **0,4052 / 1,4023 / 6,8659** | +0,2604 pt | (ν) : n_a γ̄ D_c |
| Solde primaire, % du PIB | −0,0971 / −0,2432 / −0,2381 | −0,1361 / −0,2726 / −0,2464 | **−0,2007 / −0,3348 / −0,2770** | −0,0622 pt | (ν) |

Aucune autre ligne de `tab:etat-stationnaire` ne change de P à N. **Vérifiée.**

#### 5.4.4 Valeurs résolues de `tab:criteres-j3` (π̄ = 2 %) qui changent

| N° | `main` | P | **N** | Explication |
|---|---|---|---|---|
| B10 richesse des ménages V_H/(12 YD) | 0,980566 | 0,980566 | **1,076531** | #62 : ν_H/(1 + ν_H n_a π^{∗,pas}) ; la bande de ±2 % reste centrée sur la valeur résolue |
| B11 taux d'épargne nominal | 3,8900 % | 3,8900 % | **4,2707 %** | #62 : épargne de maintien et réelle proportionnelles à V_H/YD (2,1336 + 2,1371) |
| B16 masse monétaire | 0,81658 | 0,81701 | **0,88265** | (ν) |
| B19 encaisse du Trésor | 0,021748 | 0,021875 | **0,022141** | (ν) : M^G suit les paiements bruts, dont les intérêts de B |
| B20 titres de la banque | 0,27849 | 0,30973 | **0,37564** | (ν) |
| B21 dette consolidée | 0,25674 | 0,28785 | **0,35350** | (ν) |
| B22 déficit public | 1,0185 % | 1,1419 % | **1,4023 %** | (ν) |

Inchangées de P à N (écart nul) : B1 à B9, B12 à B15, B17, B18 et B24 à B26. **Vérifiée.**

**Autres valeurs publiées.** 246 valeurs publiées changent de P à N (309 en écart à la publication actuelle, contre 284 à P) :
- `sec:banque-stationnaire` : 63 ;
- `sec:finances_publiques-stationnaire` : 50 ;
- `tab:etat-stationnaire` : 24 ;
- `sec:menages-stationnaire` : 20 ;
- `sec:banque_centrale-stationnaire` : 13 ;
- `sec:finances_publiques-emission` : 12 (+3 avec `tab:calibration`) ;
- `sec:banque_centrale-conditions` : 12 (+6 avec la fiche 9 § 3.Q, +1 avec la fiche 8 § 9.6) ;
- `sec:banque_centrale-restitution` : 9 ;
- `sec:finances_publiques-depense` : 7 ;
- `sec:banque-restitution` : 6 ;
- `sec:finances_publiques-restitution` : 4 ;
- fiche 9 § 3.C et § 9.6 : 4 ;
- 2 chacune : `sec:finances_publiques-transferts`, fiche 9 § 6.3, fiche 9 § 3.C, `sec:banque-resultat` ;
- 1 chacune : `sec:finances_publiques-impots`, `sec:finances_publiques-caisse`, `sec:banque-conditions`, fiche 8 § 9.6.

Ce sont toutes des valeurs (ν) ou des valeurs de ménages. Sortie : `sortie_tab_nu110.txt`.

**#80** : Δr̄_α passe de 0,2764 point (P) à 0,2779 point (N), et l'écart de C/Y_o de 0,6904 à 0,8537 point. Les deux restent au-dessus du seuil de 0,1 point : #80 reste en échec attendu, sans succès inattendu. **C51** : aucune racine parasite à N (φ = 1). **Vérifiée** (valeurs du script ; tests non exécutés à N).

#### 5.4.5 λ_H seul ne change rien à l'état stationnaire (critère propre ; vérifiée)

À ν_H = 1 comme à ν_H = 1,1, pour λ_H ∈ {0,1 ; 0,2 ; 0,3 ; 0,35 ; 0,45 ; 0,5 ; 0,55 ou 0,634 ; 0,6} contre λ_H = 0,4 :
- plus grand écart relatif sur **toute la grille** du script (18 points, toutes les clés) : **0** ;
- valeurs publiées qui changent : **aucune**. Les trois « racines parasites » sont NaN des deux côtés, et la sonde les comptait par erreur, NaN ≠ NaN.

Le critère « écart relatif ≤ 1e−12 » tient exactement, puisque λ_H n'entre dans aucune forme de l'état stationnaire (§ 5.1). Aucun continuum d'équilibres n'est en jeu sous C2. Hors C2, le continuum déclaré de la fiche 5 (§ 9.6) demeure. Sortie : `sortie_lam.txt`.

### 5.5 Critères propres de #62 (écrits avant l'essai)

| Point | Mesure à N (ν_H = 1,1 ; λ_H = 0,4) | Verdict |
|---|---|---|
| ν_H λ_H < 1 | 0,44 | **tenu** |
| 0,080 ≤ λ_H ≤ 0,634 à ν_H = 1, **remesuré au ν_H retenu** | à ν_H = 1,1 : **0,0721 ≤ λ_H ≤ 0,5536** (frontières de la part du critère 12 (d), 0,85 et 0,50) ; λ_H = 0,4 | **tenu** ; part de 0,5966, à 0,097 au-dessus de 0,50 |
| Tableau du § 9.7 de la fiche 5 | ci-dessous | **publié** |
| λ_H seul ne change aucune valeur de `tab:etat-stationnaire` (≤ 1e−12) | écart nul sur toute la grille | **tenu** |

Frontières du critère 12 (d) selon ν_H, à i_D = 3 % (`sortie_part.txt`) :

| ν_H | 1 | 1,05 | 1,1 | 1,15 | 1,2 | 1,25 | 2,4 |
|---|---|---|---|---|---|---|---|
| λ_H pour une part de 0,85 | 0,0803 | 0,0760 | 0,0721 | 0,0687 | 0,0655 | 0,0626 | 0,0311 |
| λ_H pour une part de 0,50 | 0,6335 | 0,5908 | 0,5536 | 0,5209 | 0,4919 | 0,4660 | 0,2119 |

**Tableau du § 9.7 de la fiche 5**, remesuré : colonne « P » (= `main` pour ces grandeurs : ni μ̄, ni ζ, ni ϑ ne les changent) contre N. Sorties : `sortie_f5s97.txt`, `sortie_part.txt`, `sortie_reperes.txt`.

| Grandeur | P (ν_H = 1) | **N (ν_H = 1,1)** | Écart | Explication |
|---|---|---|---|---|
| V/(n_a YD) stationnaire, 2 % / 10 % | 0,980566 / 0,912667 | **1,076531 / 0,995242** | +9,79 % / +9,05 % | ν_H/(1 + ν_H n_a π^{∗,pas}) |
| V/(n_a YD^HS) | 1 exactement | **1,1 exactement** | +10 % | définition de ν_H ; niveau normal restitué |
| Dépendance de V/(n_a YD) à n_a (n_a = 4 / 12 / 52), 2 % | 0,980535 / 0,980566 / 0,980578 | 1,076493 / 1,076531 / 1,076545 | — | idem ; π^{∗,pas} géométrique (ADR 0008, I.6) |
| Même dépendance, 10 % | 0,912030 / 0,912667 / 0,912911 | 0,994485 / 0,995242 / 0,995532 | — | idem |
| Taux d'épargne nominal, 2 % / 10 % | 3,8900 % / 10,5565 % | **4,2707 % / 11,5116 %** | +0,38 / +0,96 pt | idem |
| dont maintien + épargne réelle, 2 % ; 10 % | 1,9434 + 1,9466 ; 8,7333 + 1,8232 | 2,1336 + 2,1371 ; 9,5234 + 1,9882 | — | idem |
| Taux d'épargne de Haig-Simons, 2 % / 10 % | 1,9852 % / 1,9977 % | 2,1837 % / 2,1975 % | +0,20 pt | idem |
| Taux de Haig-Simons selon n_a (4 / 12 / 52), 2 % | 1,9950 / 1,9852 / 1,9814 % | 2,1945 / 2,1837 / 2,1795 % | — | idem |
| C/YD, 0 / 2 / 10 % | 0,98018 / 0,96110 / 0,89443 | 0,97820 / 0,95729 / 0,88488 | −0,0038 (2 %) | idem |
| α_Y = 1 − ν_H λ_H | 0,600 | **0,560** | −0,040 | propension d'impact |
| Coefficient de richesse × n_a, 2 % (0 / 2 / 10 % par pas) | 0,3683 (0,031682 / 0,030688 / 0,026884) | 0,3690 (0,031682 / 0,030754 / 0,027203) | +0,0007 | ν_H λ_H π^{∗,pas} |
| Frontière du coefficient de richesse en π\* | 85,1175 % | **93,1884 %** | +8,07 pt | idem ; à λ_H = 0,2 : 24,9425 % → 25,6496 % |
| Boucle propre, i_D = 0 / 3 % ; π̄ = 10 %, i_D = 11 % | 0,96612 / 0,96706 ; 0,96727 | 0,96605 / 0,96710 ; 0,96733 | ≤ 6e−5 | λ_H inchangé ; ν_H ne joue que par i_D |
| Boucle propre, λ_H × 0,5 / × 2 (i_D = 3 %) | 0,98352 / 0,93419 | 0,98354 / 0,93428 | ≤ 9e−5 | idem |
| Continuum hors C2, écart à la lecture exacte, λ_H = 0,2 / 0,4 / 0,8 : 3 % ; 10 % | −3,35 / −1,29 / −0,22 % ; −19,76 / −8,58 / −1,56 % | −3,29 / −1,21 / −0,13 % ; −19,40 / −8,06 / −0,95 % | — | lecture exacte ν_H/(1 + ν_H n_a π^pas) (voir § 5.10) |
| Part propre d'un transfert, 12 tours, 2 % / 10 % (i_D = 3 %) | 0,628 / 0,618 | **0,597 / 0,586** | −0,031 / −0,032 | α_Y plus bas |
| Même part, λ_H × 0,5 / × 2 | 0,760 / 0,423 | 0,743 / 0,370 | — | idem |
| Même part, i_D de l'état P (2,02 %) | 0,6268 | 0,5954 | — | pour mémoire ; le protocole publié garde 3 % |
| Dépense cumulée d'une aubaine (tour 1), sur 3 / 12 / 36 / 60 tours | 0,643 / 0,734 / 0,875 / 0,939 | 0,605 / 0,705 / 0,862 / 0,932 | — | grandeur nouvelle, rapportée à la source (§ 5.3) |
| Frontières de λ_H pour le seuil 12 (d) | 0,080 à 0,634 | **0,072 à 0,554** | — | idem |
| Marge du plafond | 12,24 mois | **13,49 mois** | +1,25 | 12 (V/YD)/(C/YD) |
| Impôts doublés : baisse du plan au tour suivant (ΔT_H = 16) | 10,12 | 9,48 | −0,64 | α_Y Γ^e plus bas |
| Effet d'un changement de cible (2 % → 1 %) | +0,5543 % | **+0,5750 %** | +0,02 pt | terme ν_H λ_H π^{∗,pas} ; reste dans [0,3 % ; 0,8 %] |
| m_H d'impact et de long terme (fiche 2) | 0,4808 ; 0,7922 | **non remesuré** | — | — |
| Boucle conjointe (§ 3.C-10, point 8) | — | **non remesurée** ; voir C62 au § 5.7 | — | — |

### 5.6 Conditions d'existence au point fixe (N : P avec ν_H = 1,1 ; n_a = 12, ν_G = 1,15)

| Condition | π̄ = 0 | 2 % | 10 % | Verdict |
|---|---|---|---|---|
| Div_F > 0 : Div_F/(p v), % | 22,21 | 22,38 | 22,60 | tenue, = P |
| Dividende stationnaire de la banque (`sec:banque-stationnaire`), par an | 0,029580 (P : 0,028758) | 0,032758 (0,031703) | 0,045511 (0,043554) | **tenue**, marge accrue par ϖ_D ΔD_H |
| Coefficient de richesse λ_H/n_a + ν_H λ_H π^{∗,pas} − γ^e, par pas | 0,031682 | 0,030754 | 0,027203 | tenu |
| ν_H λ_H < 1 | 0,44 | | | tenu |
| Domaine de la table : ν_H > 0, 0 < λ_H ≤ n_a | 1,1 ; 0,4 | | | tenu, sans écrêtage |
| D1 | 0,99175 | 0,99144 | 0,98737 | tenue (P : 0,99250 / 0,99221 / 0,98852) |
| D2 | 0,99904 | 0,99712 | 0,98946 | tenue, = P |
| Marge du plafond de E1 | 0,13785 | 0,17026 | 0,33230 | tenue, accrue (P : 0,13531 / 0,16319 / 0,31515) |
| Plafond de E6 (valeur) | 1,12890 | 1,08283 | 0,88993 | P : 1,13469 / 1,09346 / 0,91028 ; nature inchangée |
| Caisse des entreprises, phase 4 | 0,6947 | 0,6992 | 0,7063 | = P |
| Caisse des ménages, phase 4 (`caisse_DH4`) | 1,0725 | 1,0727 | 1,0726 | tenue (P : 1,0800 à 2 %) |
| `calculer` aux 18 points de la grille et au point ν_G = 1 | aucun refus | | | **vérifiée** |

**Conditions d'arrêt du plan** : aucune condition au sens strict n'est rencontrée. Sous P228, la valeur recommandée (ν_H = 1,1 ; λ_H = 0,4) repose sur une source lue et tient les critères du plan. Elle reste à soumettre à l'absence d'objection de `jeu` et de `monnaie`.
- Aucune valeur n'est hors domaine et aucune équation n'est à changer.
- λ_H ne change pas l'état stationnaire.
- La source de ν_H est lue : le « non trouvé » de P208 n'est pas invoqué.
- **Non vérifié** : le maintien, par les bancs D et BF, de leur plafond de E1 et de E6 (P184). La mesure relève du rang 8. La marge de E1 monte et la valeur du plafond de E6 baisse de 1 % à 2 %.
- **Un résultat publié sans verdict change de nature** : C62 (§ 5.7). Il est soumis au mainteneur (§ 5.8, question 4).

### 5.7 Effet sur C62 et sur ζ_c (P224)

Sorties : `sortie_zc.txt`, `sortie_c62H.txt`, `sortie_phi.txt`, `sortie_moteur.txt`. Lecture (c) de la maquette, pire des deux régimes de T4, μ̄ = 0,60.

**Rayon sous φ = 0, π̄ = 2 %, selon ζ** :

| Configuration | ζ = 4 | 6 | 8 | 10 | 12,56 | 17 | 20 | ζ_c (2 %) |
|---|---|---|---|---|---|---|---|---|
| A (ϑ = 0,10, ν_H = 1) : contrôle du § 3.13 | 1,001818 | 1,000125 | 1,000035 | 0,999942 | 0,999818 | 0,999596 | 0,999443 | **8,7633** |
| **P** (ϑ = 0,15, ν_H = 1) | 1,002776 | 1,000530 | **1,000438** | 1,000341 | 1,000214 | 0,999988 | 0,999832 | **16,7632** |
| P, λ_H = 0,2 | 1,003173 | 1,000641 | 1,000468 | 1,000293 | 1,000065 | 0,999664 | 0,999389 | 13,2842 |
| A, ν_H = 1,1 (ϑ = 0,10) | 1,003333 | 1,001550 | 1,000622 | 1,000517 | 1,000382 | 1,000148 | 0,999989 | 19,7935 |
| **N** (ϑ = 0,15, ν_H = 1,1) | 1,004125 | 1,002828 | **1,000995** | 1,000890 | 1,000755 | 1,000519 | 1,000360 | **aucun sur [0,5 ; 20]** |
| N, λ_H = 0,35 | 1,004218 | 1,002899 | 1,001020 | 1,000905 | 1,000757 | 1,000498 | 1,000323 | aucun |
| N, λ_H = 0,2 / 0,55 (ζ = 8) | | | 1,001200 / 1,000951 | | | | | aucun |
| P, ν_H = 1,2 | 1,005204 | 1,004248 | 1,002847 (réelle) | 1,001366 | 1,001226 | 1,000985 | 1,000823 | aucun |

**À ζ = 8, selon π̄ et φ** :

| Configuration | φ = 0 : 0 % | 2 % | 10 % | φ = 1 : 0 / 2 / 10 % | φ\* à 2 % / 10 % | Doublement sous φ = 0, 2 % ; 10 % |
|---|---|---|---|---|---|---|
| A | 0,998235 | 1,000035 ∠ ±0,176° | 1,009661 | 0,997240 / 0,996922 / 0,997148 | 0,0111 / 0,5713 | 19 659 tours ; 72 tours |
| **P** | 0,998668 | **1,000438 ∠ ±0,154°** | 1,010255 | 0,997246 / 0,996954 / 0,997202 | **0,1231 / 0,5874** | **1 584 tours (132 ans)** ; 68 tours |
| **N** | 0,999272 | **1,000995 ∠ ±0,091°** | 1,011201 | 0,997282 / 0,997028 / 0,997334 | **0,2466 / 0,6151** | **697 tours (58 ans)** ; 62 tours |
| N, λ_H = 0,35 | 0,999247 | 1,001020 ∠ ±0,092° | 1,011725 | 0,997238 / 0,996986 / 0,997323 | 0,2448 / 0,6140 | 680 ; 59 tours |

Une seule traversée de 1 en φ sur une grille de 21 points, à chaque cas.

**Corroboration sur le moteur** (`serieH.py`, Prony du § 3.13, choc θ_G aux tours 1 à 12, φ = 0, ζ = 8) :

| Cas | Maquette | Moteur |
|---|---|---|
| Contrôle A, 2 %, choc de 1e−6, pas 3 000 à 12 000 | 1,000035 ∠ ±0,176° | 1,0000351 ∠ ±0,1757° |
| P, 2 %, choc de 1e−6, pas 3 000 à 12 000 | 1,000437 ∠ ±0,154° | **1,0004375 ∠ ±0,1535°** (période 2 345 tours) |
| N, 2 %, choc de 1e−9, pas 2 000 à 7 000, ordres 2, 4 et 6 | 1,000995 ∠ ±0,091° | **1,0009952 ∠ ±0,0909°** (période 3 959 tours) |
| P, 10 %, pas 300 à 900, ordre 2 | 1,010255 | 1,0102558 (et 1,0208 ≈ λ², harmonique) |
| N, 10 %, pas 300 à 900, ordre 2 | 1,011201 | 1,0112014 (et 1,0227 ≈ λ²) |

À N et 2 %, un choc de 1e−6 sur 12 000 pas sort du régime linéaire : Prony y rend des racines réelles de 1,0147 et 1,0055. C'est pourquoi le choc de 1e−9 est retenu, sur une fenêtre plus courte. **Vérifiée.**

**Note de méthode.** À 10 % sous φ = 0, la trajectoire de contrôle **non choquée** de 12 000 pas s'arrête au pas 2 936, sur la caisse de l'État en phase 7 (ligne 19a-banque). C'est le bruit d'arrondi qui croît à 1,0112 par pas. Les mesures à 10 % ont donc été faites sur 1 500 pas. Avec un choc de 1e−6, les trajectoires choquées s'arrêtent au pas 1 319 (N) et 1 421 (P) sur ti = 0 (frontière de #143), cas déjà connu de C62 à 10 % (§ 3.7). φ = 0 n'est pas la configuration de référence. **Vérifiée.**

**Constats** :
1. **λ_H agit peu sur C62.** À 2 %, le module à ζ = 8 vaut 1,000468, 1,000438 et 1,000431 pour λ_H = 0,2, 0,4 et 0,6 à ν_H = 1 ; 1,001200, 1,000995 et 1,000951 pour λ_H = 0,2, 0,4 et 0,55 à ν_H = 1,1. Il décroît avec λ_H. **Vérifiée.**
2. **ν_H agit fortement.** À 2 % et ζ = 8, le module passe de 1,000438 (ν_H = 1) à 1,000995 (1,1) puis à 1,002847 (1,2), où la racine dominante devient réelle. À ν_H = 1,1, aucun ζ ≤ 20 ne ramène le rayon sous 1 (1,000360 à ζ = 20). **Vérifiée.** Mécanisme, **hypothèse** cohérente avec le § 3.13.6 : la dette consolidée D_c porte le canal rentier, et (ν) la relève de 22,8 % à 2 %.
3. **ϑ = 0,15 (#130, déjà retenu par P225) avait déjà déplacé ζ_c de 8,76 à 16,76.** C'est un effet que le § 4 ne mesurait pas : C62 n'y était pas remesuré. La formulation adoptée pour M34 (P222, § 3.13.7) dit « À 2 %, le module passe 1 à ζ_c = 8,76 ». Elle ne vaut donc plus dès la table P, et le § 3.13.8 l'avait prévu (« marge infime », remesure après M34). **Vérifiée.** Ce point est à la frontière de `monnaie` (dette publique).
4. **φ = 1 reste stable** dans tous les cas mesurés (rayons de 0,99660 à 0,99744). π̄ = 0 reste stable sous φ = 0. 10 % reste explosif, avec un doublement en 62 tours (5 ans) à N au lieu de 72. **Vérifiée.**

**Formulation que la table N rendrait publiable** (proposition, à relire par `monnaie`) :

> Sous φ = 0, à la table calibrée (ζ = 8, ϑ = 0,15, ν_H = 1,1), la boucle conjointe est explosive à 10 % (racine réelle de 1,011201, écart doublé en 62 tours), **faiblement explosive à 2 %** (paire complexe de module 1,000995 et de période voisine de 4 000 tours, enveloppe doublée en 697 tours, soit 58 ans) et stable à π̄ = 0 (0,999272). Couverture minimale qui stabilise : 0,247 à 2 %, 0,615 à 10 %. Le signe à 2 % ne dépend plus de ζ sur [0,5 ; 20], mais il dépend de ν_H et de ϑ : à ν_H = 1 et ϑ = 0,10, il basculait à ζ_c = 8,76. Valeurs de la maquette, corroborées par le moteur (1,0009952 et 1,0112014).

ζ_c reste à remesurer au rang 8 (P224), avec λ_w (#45).

### 5.8 Questions au mainteneur

1. **Définition de ν_H.** Je propose le numéraire et les dépôts des ménages sur leur revenu disponible brut (F.2/B.6g, EA21, 2001–2023, 1,076). Autres définitions possibles :
   - (b) le revenu net, B.6n (1,154) ;
   - (c) la fenêtre 2010–2024 (1,154) ;
   - (d) les actifs financiers nets, BF90 (2,309), que j'écarte, puisque le modèle n'a ni actions ni droits à pension et que la dette de référence passerait à 127 % du PIB.

   *Avis : (a), avec le contrôle stock-flux (4,32 % observé contre 4,27 % dans le modèle).*
2. **Valeur de ν_H** : 1,1 (ronde), 1,0995 (égalité exacte de B10 à 1,076), ou 1 (statu quo, 8,9 % sous la source) ? *Avis : **1,1**.* Elle change l'état de référence : dette consolidée +22,8 %, dette affichée de 31,6 à 38,4 % du PIB, déficit de 1,14 à 1,40 % du PIB, θ_G +0,0008 (§ 5.4).
3. **λ_H** : 0,4 inchangé, déclaré « choix dans la fourchette lue » (aubaine sur un trimestre : 0,605, contre 0,5 à 0,9 chez Parker et al., 2011), ou 0,3, au centre de cette fourchette (0,701) ? *Avis : **0,4**.* Aucune source lue ne départage, λ_H ne change pas l'état stationnaire, et la source la plus directe (Fagereng et al., gains de loterie) est sur un hôte non ouvert : `www.duo.uio.no` ou `ifo.de` à autoriser pour la lire.
4. **C62 à 2 % sous φ = 0** (frontière avec `monnaie`). À la table proposée, le module reste au-dessus de 1, comme à P (1,000438) et à A (1,000035) : le signe ne change pas. Mais la boucle devient **faiblement explosive**, avec un doublement en 58 ans, et le seuil chiffré de la formulation de P222 (« ζ_c = 8,76 ») ne vaut plus. ϑ = 0,15 (#130) l'avait déjà déplacé à 16,76, et ν_H = 1,1 le fait sortir du domaine de ζ. P230 couvre un changement de signe dû à #62 par la formulation de P222, sans arrêt. Ici, aucun signe ne change, mais les chiffres publiés de la formulation changent, dont une partie par #130.
   *Avis : publier sous P230 les nombres du § 5.7, après relecture de `monnaie`. Ne pas garder ν_H = 1 pour préserver la formulation : ce serait caler un paramètre sur un résultat attendu, ce que le mainteneur a refusé pour ζ (§ 3.14). La propriété ne porte sur aucun verdict, et l'écart reste imperceptible sur une partie (§ 5.9).*
5. **Dette de référence plus élevée** (38,4 % à 2 %, contre 81,8 % observés en moyenne pour la zone euro de 2001 à 2023, non comparable). *Avis : publiée sans cible. ν_H est le premier paramètre lu qui rapproche la dette du modèle de l'ordre de grandeur observé, mais ce n'est pas son objet.*

### 5.9 Points pour `jeu` (je ne les tranche pas)

- **Seuil du critère 12 (d)** (consultation prévue) :
  - à ν_H = 1,1, la part propre d'un transfert dépensée en 12 tours passe de 0,63 à **0,60** ; le seuil [0,50 ; 0,85] tient pour 0,072 ≤ λ_H ≤ 0,554 ;
  - la littérature lue (dépense totale de 0,5 à 0,9 sur un trimestre) est compatible avec ce seuil ;
  - la phrase d'aide « part propre au ménage dépensée en 12 tours de 0,63 » (`sec:menages`, l. 2101) devient 0,60.
- **Richesse en années de revenu** : le niveau normal affiché, « à la cible », passe de **1 an à 1,1 an**, et le ratio nominal de 0,98 à 1,08.
- **Taux d'épargne nominal** : de 3,89 % à **4,27 %**. Il reste loin du taux d'épargne brut observé (13,6 %), qui comprend l'investissement en logement absent du modèle. L'aide doit le dire, sinon le joueur comparera le chiffre à celui de la presse.
- **Dette publique de référence affichée** : de 31,6 % à **38,4 % du PIB** à 2 %, sans décision du joueur. C'est la contrepartie des dépôts des ménages (C42).
- **C62** : sous φ = 0 à 2 %, l'enveloppe double en 58 ans (×2,05 sur 720 tours). C'est imperceptible sur une partie de 10 à 30 ans (durée : #155), et visible seulement sur la fenêtre de 60 ans. La leçon « financer les intérêts par le déficit est dangereux » vaut désormais aussi à 2 %, mais lentement.

### 5.10 Surface pour `coder` et `docwriter` (rangs 3 à 9)

- **Table du bloc 5** (`nations.moteur.parametres.menages`) : `nu_H` passe de 1,0 à 1,1 et reçoit sa source ; `lambda_H` garde 0,4 et reçoit sa source. Défaut `Parametres.nu_H` du script et déclarations de `nu_H` et `lambda_H` (l. 174 et 192, aujourd'hui « tab:calibration (indicative) »). Égalité tenue par `test_valeurs_indicatives_egales_a_celles_du_script`.
- **Texte de source proposé pour `tab:calibration`** :
  - ν_H : « Eurostat, comptes des secteurs (`nasa_10_f_bs`, `nasa_10_nf_tr`), ménages et ISBLSM (S14_S15), numéraire et dépôts (F.2) sur revenu disponible brut (B.6g), EA21, moyenne 2001–2023 : 1,076 an ; ν_H = R/(1 − R n_a π^{∗,pas}) à π\* = 2 % : 1,0995, arrondi à 1,1 ; contrôle : acquisition nette de F.2 sur B.6g, 4,32 % (2002–2023), contre 4,27 % dans le modèle ; consulté le 16/11/2026 » ;
  - λ_H : « choix de conception dans la fourchette lue : dépense totale de 50 à 90 % d'un versement sur le trimestre de réception (Parker, Souleles, Johnson et McClelland, NBER WP 16684, 2011) ; dépense cumulée d'une aubaine sur 3 tours de 0,605 à ν_H = 1,1 ; correspondance contestée (versements annoncés, données américaines, ménage représentatif) ; effet richesse sur la richesse illiquide plus faible, non comparable ».
- **Valeurs publiées des tests** :
  - `tests/invariants/test_menages.py` : repères de la part (0,628 / 0,618 / 0,760 / 0,423 → 0,597 / 0,586 / 0,743 / 0,370), de la boucle propre (§ 5.5) et du continuum ;
  - `tests/unitaires/test_menages.py` : changement de cible (0,5543 → 0,5750) ; coefficient × n_a (0,368 → 0,369) ; frontières en π\* (85,1175 → 93,1884 % ; à λ_H = 0,2 : 24,9425 → 25,6496 %) ; marge du plafond (12,24 → 13,49 mois) ; impôts doublés (10,12 → 9,48).
- **Constat sur un test (à corriger au même commit, sans changer le protocole)** : `test_continuum_hors_c2_sur_la_forme_fermee` calcule la « lecture exacte » comme 1/(1 + n_a π^pas), sans ν_H. La fiche (§ 9.6) la définit à ν_H près, et la formule n'est juste qu'à ν_H = 1. À ν_H = 1,1, la forme correcte ν_H/(1 + ν_H n_a π^pas) donne les écarts du § 5.5. La forme actuelle les décalerait d'environ +10 %. **Vérifiée** par lecture du code (l. 573) et par recalcul.
- **Spécification** : `sec:menages-stationnaire` (20 valeurs), `sec:menages-conditions` (frontière de π\*), `sec:menages` (« 0,63 », l. 2101 ; « 1 an », niveaux normaux), `tab:etat-stationnaire`, `tab:criteres-j3` (B10, B11, B16, B19 à B22), les 246 valeurs du § 5.4.4. Il faut aussi reprendre la formulation de C62 (`sec:finances_publiques-impots`, `sec:finances_publiques-conditions`, fiche 9, C62) selon la question 4.
- **Fiche 5** : la réserve 7 est levée pour ν_H et maintenue pour λ_H ; la phrase « aucune source lue sur la richesse liquide (Fed Z.1 non lue, BCE inaccessible) » est remplacée par la source du § 5.2.
- **Concordance** : aucun label ajouté ni retiré (90).

### 5.11 Statut des conclusions

- **Vérifiées** (commande et sortie, ou source citée) :
  - rapports d'Eurostat F.2/B.6g, F.2/B.6n, (F.2 − F.4)/B.6g, BF90/B.6g, F/B.6g ; acquisition nette de F.2 ; taux d'épargne brut ; dette publique EA20 ;
  - ν_H = 1,0995 tiré de 1,076 ; B10 = 1,076531 à N ;
  - tableaux des § 5.4 à 5.6, et mécanisme (ν) bouclé (ΔD_c = ΔD_H) ;
  - invariance exacte de l'état stationnaire en λ_H (grille entière, 449 valeurs publiées) ;
  - frontières en λ_H du critère 12 (d) ; dépense cumulée d'une aubaine ; frontières de λ_H pour la fourchette de Parker et al. ;
  - lignes du § 9.7 de la fiche 5 ; #80 toujours en échec ; C51 sans racine parasite ;
  - C62 : rayons, ζ_c, φ\* et doublements de la maquette, corroborés par le moteur à P et N (2 % et 10 %) ;
  - déplacement de ζ_c par ϑ (8,76 → 16,76) ;
  - constat sur la lecture exacte du test du continuum.
- **Vérifiées avec réserve** (résumés de `www.nber.org` rendus par l'outil) : Parker et al. (2011), Johnson et al. (2004), Kaplan et Violante (2011/2014). La période du chiffre « 50-90 % » est à confirmer sur l'article.
- **Hypothèses** :
  - correspondance entre la dépense d'une aubaine dans le modèle et les réponses aux versements fiscaux observées ;
  - lecture de la cohérence stock-flux (croissance nominale voisine) ;
  - mécanisme du changement de C62 par ν_H (canal rentier porté par D_c).
- **Non vérifiées** :
  - Fagereng, Holm et Natvik (2021) et Jappelli et Pistaferri (2014), sur des hôtes non ouverts ;
  - Carroll, Otsuka et Slacalek, non relu ;
  - m_H et la boucle conjointe du § 3.C-10 de la fiche 5 à N ;
  - persistance (condition 10 de `jeu`) ;
  - bancs d'empreintes à N (rang 8), dont le maintien du plafond des bancs D et BF ;
  - tests du dépôt exécutés à N ;
  - croissance nominale observée du revenu disponible (non lue).

### 5.12 Avis consultés et décisions (16/11/2026, délégation P228)

**Avis de `jeu`** : **pas d'objection**. ν_H = 1,1 ne crée ni ne ferme de levier ; part dépensée d'un transfert sur 12 tours 0,63 → 0,60, imperceptible ; C62 à 2 % sous φ = 0 invisible sur une partie. Seuil du critère 12 (d) conforme (part 0,597 dans [0,50 ; 0,85], `tests/invariants/test_menages.py` l. 62 ; λ_H = 0,4 dans [0,072 ; 0,554]) ; vigilance : la borne haute baisse vite quand ν_H monte. À clarifier dans l'aide : la dette de départ (38 % du PIB) est la contrepartie des dépôts des ménages (C42), non comparable aux 82 % observés (ni non-résidents ni assureurs) ; même remarque pour le taux d'épargne de 4,27 %.

**Avis de `monnaie`** : **pas d'objection**. La richesse supplémentaire des ménages a pour contrepartie des titres publics détenus par la banque, euro pour euro (C42 ; ΔD_c = ΔD_H, vérifié) ; λ_H sans contenu monétaire. Dette de référence publiée sans cible ; réserve pour le futur : les seuils de la prime souveraine devront se fixer par rapport à la dette de référence du modèle (hypothèse). C62 à la table combinée (μ̄ 0,60, ζ 8, ϑ 0,15, ν_H 1,1, λ_w 0,18 ; maquette, vérifié) : sous φ = 0, à 2 % paire complexe de module 1,000891 ∠ ±0,084°, doublement en 778 tours, de 1,00079 à 1,00431 sur ζ ∈ [2 ; 20] sans traversée de 1, φ* = 0,286 ; à 10 % racine réelle 1,008216, doublement en 85 tours ; à π̄ = 0, 0,999538 ; sous φ = 1, 0,99746 à 2 %. Le signe à 2 % ne change pas ; les chiffres du § 6.13 (1,00049 ; 1 415 tours) ne valent plus à la table combinée. À joindre au dossier M34 : corroboration par le moteur (non vérifiée), φ* à 10 %, test zéro à φ = 1.

**Décisions de la session sous délégation** (P228 ; M34 réservée) : **ν_H = 1,1 et λ_H = 0,4** retenus comme valeurs proposées de la table soumise à M34 (définition F.2/B.6g, questions 1 à 3 et 5 : avis de `macro` suivis) ; question 4 (C62) : chiffres de la table combinée repris au dossier M34 (§ 7), sous P230 ; la correction du test du continuum (`tests/invariants/test_menages.py`, l. 573) accompagne le commit de #62 (P233).

## 6. #45 — Vitesse de correction salariale λ_w (bloc 3, travail)

*Instruite par `macro` (expert pilote) le 16/11/2026, rang 1 de la branche « calibration » (PR #162, tête `d865683`). `git status` était vide après les sondes : aucun fichier du dépôt n'a été modifié. Les sondes sont hors dépôt (`<scratchpad>/outils45/`). Elles appellent sans les modifier `outils/etat_stationnaire.py`, `outils/maquette_conjointe.py`, `tests/invariants/socle_partiel.py` et les assistants de `tests/invariants/test_socle_complet.py`. Les chiffres du modèle sont des résultats du modèle, pas des faits. Les faits portent leur source et leur date. Chaque conclusion est marquée **vérifiée**, **hypothèse** ou **non vérifiée**. Le périmètre est #45 réduite à λ_w (P204). β, a_π, a_I et λ_e restent hors périmètre (#163).*

### 6.1 Grandeurs visées et correspondance avec le modèle

**Règle exécutée** (`eq:travail-salaire`, `nations.blocs.travail.salaire`, l. 81 à 91 ; appelée en phase 1 avec `par_pas(table.lambda_w)`, l. 141 à 145 ; **active** au socle complet) :

ln W_t = ln W_{t−1} + (1/n_a)[ln(1 + g_pr) + ln(1 + π^e_t)] + (λ_w/n_a)[ln(ω*/ω_{t−1}) − β(U_{t−1} − U^eq)], avec ω* = 1/(1 + μ̄).

Coefficients effectifs aujourd'hui : λ_w = 1 par an (`nations.moteur.parametres.travail.LAMBDA_W`, défaut `Parametres.lambda_w` du script), β = 2, U^eq = 0,05, n_a = 12.

**Définitions** (n_a = 12) :

| Grandeur | Définition | Unité, dénominateur, fenêtre |
|---|---|---|
| λ_w, vitesse d'ajustement salarial | Part λ_w/n_a de l'écart [ln(ω*/ω) − β(U − U^eq)] qui passe dans le salaire nominal à chaque tour | Par an, taux de flux linéaire (P65) ; domaine 0 < λ_w ≤ n_a |
| Correction annuelle c | 1 − (1 − λ_w/12)^12 : part d'un écart de salaire réel résorbée en 12 tours, à prix exogènes et U = U^eq | Fraction de l'écart initial ; 12 tours |
| Demi-vie de SN | ln 2 / [−ln(1 − λ_w/n_a)], valeur propre du salaire à prix exogènes (critère 5 (b) de la fiche 3) | Tours |
| Pente (effet de niveau) | λ_w·β : hausse du salaire nominal sur 12 tours par point d'écart durable U − U^eq, marge à sa norme, π^e donnée | Points de hausse annuelle par point de chômage, par an |
| β, semi-élasticité de long terme | −∂ ln(salaire réel visé)/∂U ; β = e/U*, où e est l'élasticité de la courbe des salaires en ln U | Sans dimension, par unité de taux de chômage |

**Correspondance avec les sources** :
- Un coefficient ρ du salaire retardé en données annuelles donne c = 1 − ρ, d'où λ_w = 12(1 − ρ^{1/12}).
- Un coefficient de correction d'erreur annuel donne c directement.
- Une pente en données trimestrielles non annualisées (Galí) se multiplie par 4. Une pente en glissement annuel (BCE) se lit telle quelle.
- **Hypothèse.** Ces pentes viennent de formes réduites sans terme de niveau. Elles sont comparables à λ_w·β seulement si la marge reste à sa norme. Sous SN, un ω variable ajoute le terme ln(ω*/ω), que ces régressions omettent.
- **Hypothèse.** Les sources indexent sur l'inflation passée avec un coefficient inférieur à 1, alors que SN indexe sur π^e avec un coefficient de 1 (frontière avec `monnaie`, § 6.9).

### 6.2 Sources lues et citées

Toutes les sources ont été lues le 16/11/2026, en PDF, sur `www.nber.org` et `www.ecb.europa.eu`. Les pages sont celles des versions lues.

**(S1) D. G. Blanchflower et A. J. Oswald, « The Wage Curve Reloaded », NBER WP 11338, 2005** (texte extrait par `pdftotext`).
- **Données** : panel d'États américains, 1980–2001, cellules État-année (1 122 observations), donc **annuel**. Salaire horaire (CPS ORG) en logarithme, sur le logarithme du chômage de l'État, avec indicatrices d'année : les salaires sont **relatifs** entre États.
- **Élasticité de long terme** : environ −0,1. La méta-analyse de Nijkamp et Poot la ramène à −0,07 après correction du biais de publication (p. 4). Bande du livre de 1994 : « −0.05 to −0.20 » (p. 4, note 5). Tableau 1, colonne 2 : −0,08 (p. 11). Colonnes 6 et 7, les plus complètes : environ −0,1 (p. 12).
- **Coefficient du salaire retardé ρ (salaire horaire)** :
  - 0,955 sans effets fixes d'État (tableau 1, colonne 1, p. 11), spécification que les auteurs jugent trop simple ;
  - 0,699 avec effets fixes (tableau 1, colonne 2, p. 11) ;
  - 0,60 dans la spécification préférée, salaire retardé instrumenté (tableau 4, partie C, ligne 4, p. 15) ;
  - 0,81 et 0,71 (tableau 5, colonnes 1 et 2, p. 15).
- **Gains annuels** (CPS de mars, tableau 6, p. 16) : environ 0,35 avec effets d'État, d'année et de branche ; environ 0,13 avec tendances d'État.
- **Conversions** :
  - salaire horaire, ρ de 0,81 à 0,60 : c de 0,19 à 0,40, soit λ_w de 0,209 à 0,500 ;
  - gains annuels, ρ de 0,35 et 0,13 : c de 0,65 et 0,87, soit λ_w de 1,005 et 1,876.
- **Vérifiée.** Les gains annuels n'étaient pas cités dans la fiche 3. λ_w = 1 leur correspond, mais pas aux salaires horaires que les auteurs privilégient.

**(S2) O. J. Blanchard et L. F. Katz, « Wage Dynamics: Reconciling Theory and Evidence », NBER WP 6924, février 1999** (PDF numérisé, lu en images).
- **Fréquence** : la relation américaine (1) est estimée sur des « aggregate (annual) time series data » (p. 2).
- **Correction d'erreur** (équation (6), p. 5) : coefficient du terme de correction « close to zero », de signe souvent faux, pour les États-Unis ; « In most European countries […] the error correction term comes in with a significant, and right signed coefficient. On average, (1 − μλ) is around 0.25 » (p. 5). Les estimations européennes sont renvoyées à OCDE 1997, **non lu**, sans fréquence explicite.
- **Biais des données régionales** (p. 7) : avec des effets fixes d'année, l'effet du salaire agrégé retardé est absorbé, d'où un **biais vers le bas** de γ, le coefficient du salaire retardé. Les vitesses régionales de S1 surestimeraient donc la vitesse agrégée. C'est un argument de S2, non une mesure ; S1 n'y répond pas dans les passages lus (p. 11 à 16).
- **Correspondance** (équations (3) à (6), p. 3 à 5) : le β de Blanchard et Katz est la pente d'impact, et β/(1 − μλ) est la semi-élasticité de long terme. Le λ_w de SN correspond à 1 − μλ, et la pente d'impact λ_w·β de SN à leur β.
- Conversion : c = 0,25 par an donne λ_w = 0,284. Si c était trimestriel, c annuel vaudrait 0,684 et λ_w 1,097.
- **Vérifiée**, à une réserve près : la fréquence européenne n'est pas écrite. La lire comme annuelle, dans le cadre annuel du texte, est une **hypothèse**. `sec:travail-conditions` dit déjà « de fréquence non précisée ».

**(S3) J. Galí, « The Return of the Wage Phillips Curve », NBER WP 15758, février 2010** (texte extrait).
- **Données** : trimestrielles, États-Unis, taux de chômage civil (p. 18). Tableau 1 : gains des salariés de production et hors encadrement, 1964T1–2009T3 ; colonnes 7 et 8 arrêtées à 2007T4. Tableau 2 : rémunération, depuis 1948T1. L'inflation en glissement est « expressed as a quarterly rate to facilitate comparison of coefficients » (p. 23).
- **Effet de niveau** δ = −(ψ0 + ψ1), coefficients du chômage courant et retardé (tableau 1, p. 38 du PDF ; tableau 2, même page) :

| Colonne | Indexation | δ, gains (tableau 1) | 4δ, par an | δ, rémunération (tableau 2) | 4δ, par an |
|---|---|---|---|---|---|
| (3) | glissement, u_t seul | 0,079 | 0,316 | 0,087 | 0,348 |
| (5) | trimestre sur trimestre | 0,177 − 0,153 = 0,024 | 0,096 | 0,227 − 0,189 = 0,038 | 0,152 |
| (6) | glissement | 0,377 − 0,304 = 0,073 | 0,292 | 0,387 − 0,310 = 0,077 | 0,308 |
| (7) | trimestre sur trimestre, jusqu'à 2007T4 | 0,334 − 0,294 = 0,040 | 0,160 | 0,241 − 0,189 = 0,052 | 0,208 |
| (8) | glissement, jusqu'à 2007T4 | 0,552 − 0,453 = 0,099 | **0,396** | 0,397 − 0,301 = 0,096 | 0,384 |

- **Indexation** : 0,565 à 0,687 (glissement), 0,415 à 0,522 (trimestre sur trimestre).
- **Vérifiée.** La fourchette 0,29–0,40 de la fiche 3 est celle des colonnes en glissement. Toutes colonnes confondues, l'effet de niveau va de **0,10 à 0,40** par an. Sa borne haute exacte est 0,396.

**(S4, source nouvelle) F. Tagliati, « Wage growth in the euro area: a Phillips curve analysis using panel data », encadré 2 (p. 20–21) de C. Nickel, E. Bobeica, G. Koester, E. Lis et M. Porqueddu (dir.), *Understanding low wage growth in the euro area and European countries*, BCE, Occasional Paper n° 232, septembre 2019, révisé en décembre 2020** (`ecb.europa.eu/pub/pdf/scpops/ecb.op232~4b89088255.en.pdf`, texte extrait).
- **Données** : panel des 19 pays de la zone euro, 2000T1–2018T4. Variable expliquée : glissement annuel de la rémunération par salarié, avec effets fixes pays et pondération par le PIB.
- **Pentes** (tableau A, p. 21) : taux de chômage −0,317 (0,050) ; **écart de chômage −0,364 (0,085)** ; mesures larges du chômage −0,25 à −0,26.
- **Indexation** sur l'inflation passée : 0,39 à 0,42.
- C'est la seule pente lue de la **zone de référence** (P226), et l'écart de chômage est le concept de SN (U − U^eq). Sa variable expliquée est déjà en glissement annuel, d'où une pente de **0,32 à 0,36** par an.
- **Vérifiée.**

**Synthèse des fourchettes lues** :
- **Vitesse c** :
  - agrégée : ≈ 0 aux États-Unis, 0,25 en Europe (S2) ;
  - régionale, borne haute selon S2 : 0,19 à 0,40 pour les salaires horaires, 0,65 à 0,87 pour les gains annuels (S1).
- **Pente** : 0,29 à 0,40 en glissement aux États-Unis (S3 ; 0,10 à 0,40 toutes colonnes) ; 0,32 à 0,36 dans la zone euro (S4).
- **β** : avec β = 2, la pente sourcée de 0,29 à 0,40 exige λ_w de 0,145 à 0,198 ; celle de la zone euro, de 0,158 à 0,182.

### 6.3 Valeur proposée et variantes

**Proposée : λ_w = 0,18 par an**, à β = 2 inchangé.
- Pente λ_w·β = **0,36**, égale à la pente de l'écart de chômage dans la zone euro (S4 : 0,364) et dans la fourchette de S3 (0,29 à 0,40).
- Correction annuelle c = **0,166** : dans la fourchette agrégée de S2 (≈ 0 à 0,25), sous la borne basse régionale de S1 (0,19), que S2 tient pour surestimée (p. 7).
- Demi-vie de SN : **45,86 tours**.
- Statut : **choix déclaré, sources lues ; vitesse contestée (S1 contre S2 ; fréquence de S2 présumée)**.

| Variante | λ_w | c | Demi-vie de SN (tours) | Pente | Vitesse (S1, S2) | Pente (S3, S4) | Avis |
|---|---|---|---|---|---|---|---|
| V0, statu quo | 1 | 0,648 | 7,97 | 2,00 | au-dessus de S2 et de S1 (salaire horaire) ; dans S1 (gains annuels) | 5 à 7 fois la pente lue | Écartée : critère de #45 non tenu |
| **V1, proposée** | **0,18** | **0,166** | **45,86** | **0,36** | dans S2 (agrégé) ; sous S1 (salaire horaire, régional) | dans S3 et S4 | **Recommandée** |
| V2, valeur ronde | 0,20 | 0,183 | 41,24 | 0,40 | idem V1 | au bord de S3 (0,396), au-dessus de S4 (0,364) | Acceptable. Égale à λ_e = 0,2 : même demi-vie de 41,2 tours que l'anticipation (§ 6.9) |
| V3, vitesse européenne | 0,284 | 0,250 | 28,94 | 0,57 | = S2 (Europe) ; dans S1 (salaire horaire) | 1,4 fois S3 et 1,6 fois S4 | Écartée : la pente sort de la fourchette |
| V4, hors périmètre | 0,25 avec β = 1,4 | 0,223 | 32,92 | 0,35 | près de S2 (Europe) ; dans S1 | dans S3 et S4 | Concilie les deux critères, mais change β (élasticité corrigée de −0,07, S1 p. 4). Hors de #45 réduite (P204) : question 3 |
| Bord bas de la pente | 0,145 | 0,136 | 57,02 | 0,29 | dans S2 | bord de S3 | Pour mémoire |
| V1 × 0,5 et × 2 (critère 5 (b)) | 0,09 et 0,36 | 0,086 et 0,303 | 92,07 et 22,76 | 0,18 et 0,72 | — | — | Publiés, sans exigence de bande |

**Vérifiée** (valeurs calculées, `boucle45.py`, `var45.py`).

### 6.4 Tableau avant / après prédit

#### 6.4.1 Méthode et commandes

Les commandes ont été lancées depuis `/home/user/projet_macro` à `d865683`, sous la forme `uv run python -I <scratchpad>/outils45/<sonde>.py <arguments>`.
- **`es45.py`** : appelle `calculer(replace(Parametres(), **table, lambda_w=x))` sur la table de `main` et sur la table P (μ̄ = 0,60, ζ = 8, ϑ = 0,15). Elle compare **toutes les feuilles** du résultat (9 698), y compris les 449 valeurs publiées. `es45b.py` donne les résidus des contrôles.
- **`moteur45.py 720 x…`** : socle complet du moteur, 720 pas sans choc depuis l'état résolu, aux trois π\*. Les paramètres sont ceux du dépôt, et seule λ_w change (`varier`). La sonde juge le critère « Branche » (`juger`) et compare chaque champ d'état, pas par pas, au déroulé à λ_w = 1.
- **`boucle45.py`** et **`var45.py`** : critère 5 (d) (`carte_offre(m, "regle", True, lambda_w=x)`, π^e = π\* exogène), à μ̄ = 0,25 et 0,60 ; demi-vies ; variantes.
- **`socle45.py ϑ x…`** : lecture (c) du socle (`lectures`, pire des deux régimes de T4), sous φ = 1 et φ = 0, à π̄ = 0, 2 et 10 %, μ̄ = 0,60 et ζ = 8. Elle donne ζ_c par `frontiere` sur [2 ; 20] et φ\* sur [0 ; 1].
- **`bancs45.py x…`** : bancs D et BF du moteur (constructions d'`outils/empreintes_des_bancs.py`), 720 pas, table du dépôt, seule λ_w changée.
- **`maq45.py x`** : relevé des chiffres publiés de la maquette (`releve`, `evaluer`). Seul le défaut λ_w de `Parametres` change, en mémoire.
- **Contrôles** :
  - à λ_w = 1, `socle45.py 0.10 1.0` retrouve les valeurs du § 3.13 : 1,000035 ∠ ±0,176°, ζ_c = 8,7633, φ\* = 0,0111 et 0,5713 ;
  - `boucle45.py` retrouve les rayons publiés de la boucle salaires – prix : 0,8969 / 0,9068 / 0,9225 / 0,9385 et 0,9172 ;
  - `maq45.py 1.0` donne 9 écarts, tous préexistants dans le dépôt (`uv run python outils/maquette_conjointe.py` en donne les mêmes 9, à la même tête) ;
  - les sorties sont dans `<scratchpad>/outils45/sortie_*.txt`.

#### 6.4.2 État stationnaire : inchangé (aucune condition d'arrêt)

| Mesure | Résultat | Verdict |
|---|---|---|
| Script, table de `main` et table P, λ_w ∈ {0,18 ; 0,2 ; 0,284 ; 0,5 ; 2} contre 1 | 9 698 feuilles : écart relatif maximal **0**, au bit. Valeurs publiées en écart : 0/449 (`main`) et 284/449 (P), identiques à λ_w = 1 | **Inchangé au bit** ; critère « ≤ 1e−12 » tenu |
| Seule feuille qui bouge (λ_w = 2 et 12, table P) | Résidu d'arrondi du contrôle de la seconde route (P2) : 5,8e−16 contre 2,3e−16. Plus grand résidu des contrôles inchangé, 4,79e−15 | Arrondi, sans objet |
| Moteur, 720 pas, λ_w ∈ {0,18 ; 0,2 ; 0,284} | Critère « Branche » tenu aux trois π\* : 0 hors seuil ; pire écart relatif 2,4e−13 à 7,1e−13, contre 2,0e−13 à 8,2e−13 à λ_w = 1 | Tenu |
| Moteur, écart au déroulé à λ_w = 1 | ≤ 1,9e−13 relatif, sauf π^e à π\* = 0, grandeur nulle à son échelle. Seuls les arrondis diffèrent : ils s'amortissent au rythme de SN | Aucun déplacement de l'état d'arrivée |

`tab:etat-stationnaire` et les valeurs résolues B1 à B26 ne changent pas, ni à la table de `main` ni à la table P. λ_w figure dans les `VITESSES` du script, qui n'entrent pas dans l'état d'arrivée. Le terme qu'elle multiplie est nul au point fixe (ω = ω\*, U = U^eq). **Vérifiée** (mesure et lecture du code, `etat_stationnaire.py` l. 205 à 211 et 588 à 590).

#### 6.4.3 Demi-vie de la règle SN (à prix exogènes)

| | `main` (λ_w = 1) | Après (λ_w = 0,18) |
|---|---|---|
| Valeur propre du salaire | 0,916667 | 0,985000 |
| Demi-vie | **7,97 tours** | **45,86 tours** (3,8 ans) |
| Correction annuelle | 0,648 | 0,166 |
| × 0,5 / × 2 | 16,29 / 3,80 tours | 92,07 / 22,76 tours |

L'issue annonçait « environ 16 à 29 tours ». Ce chiffre supposait λ_w = 0,284 à 0,5, c'est-à-dire une vitesse sans contrainte de pente. **Vérifiée.**

#### 6.4.4 Critère 5 (d) de la fiche 3 (boucle salaires – prix ; = 5 (e) de la fiche 4)

π^e = π\* = 2 %, rayon hors de la racine nominale (racine nominale à ≤ 4,6e−11 de 1) :

| m | λ_w = 1 (publié) | **λ_w = 0,18** | λ_w = 0,09 | λ_w = 0,36 |
|---|---|---|---|---|
| 0,5 | 0,8969 (période 145, demi-vie 6,4) | **0,9357** (96 ; 10,4) | 0,9389 | 0,9289 |
| 0,6 | 0,9068 (105 ; 7,1) | **0,9471** (94 ; 12,7) | 0,9503 | 0,9402 |
| 0,7 | 0,9225 (95 ; 8,6) | **0,9596** (98 ; 16,8) | 0,9627 | 0,9529 |
| 0,8 | 0,9385 (95 ; 10,9) | **0,9724** (110 ; 24,7) | 0,9754 | 0,9660 |
| Marge constante, m = 0,6 | 0,9172 | 0,9404 | — | — |

Période en tours, demi-vie en tours.
- Les rayons sont identiques à μ̄ = 0,25 et à μ̄ = 0,60 : la forme logarithmique rend la boucle indépendante de μ̄.
- **Exigence tenue** : rayon < 1 à la calibration et aux variantes × 0,5 et × 2.
- La boucle est plus lente. Sa période reste de 94 à 110 tours (8 à 9 ans), dans la fenêtre de 60 à 120 tours du critère 11 (d).
- **Vérifiée** (maquette).

#### 6.4.5 Socle conjoint, C62 et ζ_c (μ̄ = 0,60, ζ = 8, n_a = 12)

| Configuration | φ = 1 : 0 / 2 / 10 % | φ = 0 : 0 / 2 / 10 % | ζ_c à 2 %, φ = 0 | φ\* 2 % / 10 % | Doublement sous φ = 0, 2 % / 10 % |
|---|---|---|---|---|---|
| ϑ = 0,10, λ_w = 1 (§ 3.13, contrôle) | 0,997240 / 0,996922 / 0,997148 | 0,998235 / **1,000035** / 1,009661 | **8,763** | 0,0111 / 0,5713 | 19 805 / 72 tours |
| ϑ = 0,10, λ_w = 0,18 | — | ζ = 8 : 1,000184 à 2 % | **aucun sur [2 ; 20]** (1,002882 à ζ = 2, 1,000191 à ζ = 20) | 0,0745 / 0,5946 | — |
| **ϑ = 0,15**, λ_w = 1 (table P sans #45) | 0,997246 / 0,996954 / 0,997202 | 0,998668 / **1,000438** / 1,010255 | **16,763** | 0,1231 / 0,5874 | 1 583 / 68 tours |
| **ϑ = 0,15, λ_w = 0,18 (table P avec #45)** | **0,997752 / 0,997502 / 0,997336** | **0,999071 / 1,000490 / 1,007513** | **aucun sur [2 ; 20]** (1,003457 à ζ = 2 ; 1,000469 à ζ = 20) | **0,1789 / 0,6100** | **1 415 / 93 tours** |
| ϑ = 0,15, λ_w = 0,2 / 0,284 / 0,5 | 0,997423 / 0,997226 / 0,997051 à 2 % | 1,000486 / 1,000473 / 1,000454 à 2 % | aucun sur [2 ; 20] | 0,1723 / 0,1544 / 0,1356 à 2 % | — |

À 2 %, sous φ = 0, la racine dominante est une paire complexe dans toutes les configurations (périodes de 2 049 à 2 554 tours). À 10 %, elle est réelle. **Vérifiée** (maquette).

Ce que cela change pour C62 (P219, P222, P224) :
- **Constat indépendant de #45.** ϑ = 0,15 (#130), seul, déplace déjà ζ_c de 8,76 à **16,76**, soit σ_c ≈ 16,76 × (0,029608 + 0,05) ≈ 1,33 sous la correspondance du § 3.1 (**hypothèse**). C'est au-dessus de la fourchette de σ lue (0,5 à 1,0). **Vérifiée** pour ζ_c ; σ_c est une hypothèse.
- Avec λ_w = 0,18, **aucun ζ_c n'existe dans le domaine** (ζ ≤ 20, P139). À 2 % et sous φ = 0, la boucle est faiblement explosive pour tout ζ : module 1,00049, enveloppe doublée en 1 415 tours (118 ans), imperceptible sur une partie.
- La formule adoptée pour M34, « quasi neutre à 2 %, signe dépendant de ζ », **ne tient plus** à la table P, avec ou sans #45 (question 5).
- À 10 %, λ_w = 0,18 **ralentit** la dérive (doublement en 93 tours contre 68) et relève φ\* de 0,587 à 0,610.
- La réserve du § 3.13.8 se confirme : la marge de 3,5e−5 à 2 % change de signe avec le reste de la calibration (ϑ, λ_w).
- Sous φ = 1 (socle de référence), le rayon reste sous 1 : 0,997502 à 2 %, demi-vie de 277 tours, contre 227.

#### 6.4.6 Bancs choqués (moteur, 720 pas ; table du dépôt, seule λ_w change)

| Banc, π\* | Grandeur (écart au sentier sans choc) | λ_w = 1 | λ_w = 0,284 | **λ_w = 0,18** |
|---|---|---|---|---|
| D, 2 % (θ_G × 1,25, tours 1 à 12) | Arrêt ; plafond de E1 | aucun ; actif au pas 0 | aucun ; actif au pas 0 | **aucun ; actif au pas 0** |
| | Pic du glissement des prix − π\* | +16,00 pt (pas 13) | +10,43 pt | **+9,54 pt** |
| | Pic de i_CB − ī | +9,99 pt (pas 15) | +6,52 pt | **+5,95 pt** |
| | U − U^eq extrême | −5,00 pt (borne N ≤ N^pa) | −5,00 pt | −5,00 pt |
| | U − U^eq au pas 719 | −0,009 pt | −0,038 pt | **−0,068 pt** |
| D, 10 % (× 1,60) | Pic de récession U − U^eq | +12,41 pt (pas 22) | +7,23 pt | **+5,84 pt** (pas 26) |
| | Pic du glissement − π\* | +48,7 pt | +35,3 pt | **+33,3 pt** |
| D, 0 % | Pic du glissement − π\* | +15,48 pt | +10,07 pt | +9,21 pt |
| BF, 2 % (ς_B = 0,5 au pas 5, θ_CB = 0,5) | Arrêt ; plafond de E6 (Tr/Tr^lev au pas 6) | aucun ; 0,4954, non versés > 0 | idem | **idem** |
| | Pic du glissement − π\* | +6,21 pt | +3,15 pt | **+2,71 pt** |
| BF, 0 et 10 % | Plafond de E6 | 0,4989 et 0,4814 | idem | idem |

- **Aucun banc arrêté.** D lie encore le plafond de E1, et BF celui de E6 (P184).
- Une vitesse salariale plus faible amortit la spirale salaires – prix : le pic d'inflation baisse d'environ 40 %, la récession qui suit à 10 % de moitié.
- Le retour est plus lent : écart résiduel de chômage de −0,07 point au bout de 60 ans à 2 %.
- La borne N ≤ N^pa est atteinte dans les deux cas.
- **Vérifiée** sur le moteur, à la table de `main`. Les bancs à la table P sont **non mesurés** (rang 8).

#### 6.4.7 Autres valeurs publiées (surface de `docwriter`)

**Maquette conjointe** (`maq45.py 0.18`, table de `main`) :
- 148 chiffres relevés : **67 en écart**, contre 9 à λ_w = 1, tous préexistants ;
- **8 sans mesure**, parce que la frontière publiée n'existe plus dans son intervalle.

| Endroit (ligne du `.tex`) | Chiffres | Exemple, publié → λ_w = 0,18 |
|---|---|---|
| `sec:prix-conditions` (l. 1695) | 7 | boucle salaires – prix, § 6.4.4 |
| `sec:menages-inflation` (l. 1918), `tab:instabilites` (l. 4142) | 12 + 6 | lecture (a), terme d'entretien : 1,030357 / 1,005801 / 1,059130 / 1,060998 → **0,98682 / 0,98721 / 0,99696 / 0,99161** ; glissement de Haig-Simons : 1,0231 / 1,0271 → 0,9798 / 0,9792 |
| `sec:menages-conditions` (l. 2001) | 6 | 0,9640 → ≈ 0,977 |
| `sec:banque_centrale-conditions` et `sec:finances_publiques-conditions` (l. 3015, 3455) | 21 | demi-vie du socle 240 → 247,5 tours ; marge conjointe (facteur 1,7135 sur β, a_π, η_r) : **plus de frontière sur [1 ; 2]** |
| `sec:finances_publiques-impots` (l. 3256) | 6 | doublement sous φ = 0 : 381,6 → 421,6 ; 63 → 85,3 tours (ζ = 4) |
| l. 115 et l. 4079 | 3 | lecture (a) à n_a = 4 : 1,0415 → 0,9588 |
| Frontières disparues | 8 | ν_H = 0,586 et h = 0,604 (instabilité 17) ; facteur de la marge conjointe et ses périodes |

**Texte de la spécification** :
- `sec:travail-conditions`, `\limites`, « Calibration » : à réécrire avec S1 à S4 (§ 6.2).
- `sec:banque_centrale-…` : ratio de sacrifice 1/(λ_e λ_w β) = 2,5 et coût en chômage 2,5000 / 2,4510 (`tests/invariants/test_boucle_t3_bc3.py`, l. 519) ; ils deviennent **13,89 / 13,62** point-années par point à λ_w = 0,18 (formule, **vérifiée** ; mesure moteur non refaite).
- `tab:calibration` : ligne λ_w.
- Fiche 3, § 3.N-7 et § 3.N-11.

### 6.5 Conditions d'existence et domaine

- Domaine 0 < λ_w ≤ n_a : 0,18 est tenu, sans écrêtage.
- λ_w n'entre dans aucune condition d'existence du point fixe (Div_F, dividende de la banque, ν_H λ_H, coefficient de richesse, D1, D2, E1, E6, caisse) : le script est identique au bit (§ 6.4.2).
- Aucune équation, aucune phase ni aucune variable d'état ne change.
- **Aucune condition d'arrêt du plan n'est rencontrée** : l'état stationnaire est inchangé, aucun banc n'est arrêté, et D et BF lient leur plafond.
- Deux constats touchent des résultats publiés hors de #45 : C62 (§ 6.4.5) et l'instabilité 17 (§ 6.6). Le mainteneur dit s'ils sont une « question de fond hors des cinq issues » (questions 5 et 6).
- **Vérifiée.**

### 6.6 Instabilité connue n° 17 : conditionnelle à λ_w (constat)

- `tab:instabilites`, ligne 17, et `sec:menages-inflation` motivent l'écart de la lecture (a) des ménages (#58 ; M27) par une boucle « explosive » : 1,0275 / 1,0029 / 1,0561 / 1,0580, mesurée à λ_w = 1.
- À λ_w = 0,284, trois configurations sur quatre passent sous 1 (0,985 / 0,985 / **1,0046** / 0,998).
- À λ_w = 0,18, **les quatre passent sous 1** (0,9867 / 0,9871 / 0,9940 / 0,9887), et n_a = 4 aussi (0,9588).
- Les frontières ν_H < 0,586 et h < 0,604 n'existent plus. L'instabilité voisine (glissement de Haig-Simons, 1,0223 / 1,0218) passe à 0,98 environ.
- L'instabilité n'est pas réintroduite : elle disparaît à la vitesse sourcée. Mais le motif de stabilité publié de M27 ne tient qu'à λ_w = 1.
- **Vérifiée** (maquette, table de `main`). À μ̄ = 0,60 et ν_H recalibré (#62) : **non mesuré**.

### 6.7 Questions au mainteneur

1. **Valeur de λ_w** : 0,18 (pente de la zone euro), 0,20 (valeur ronde, au bord de la pente lue, égale à λ_e) ou 0,284 (vitesse européenne de S2, pente hors fourchette) ? *Avis : **0,18**.*
2. **Lecture du critère de #45 pour la vitesse.** λ_w = 0,18 donne c = 0,166. C'est dans la fourchette agrégée de S2 (≈ 0 à 0,25), mais sous la fourchette régionale de S1 (0,19 à 0,40), que S2 juge biaisée vers le haut (p. 7 ; argument non mesuré). *Avis : retenir la fourchette agrégée et déclarer S1 comme borne haute régionale, contestée.* Aucune valeur de λ_w à β = 2 n'est à la fois dans S1 (salaire horaire) et dans la pente de S3 et S4 : l'intersection est vide, de 0,198 à 0,209.
3. **β hors périmètre** (P204). Avec β = 1,4 (élasticité corrigée de −0,07), λ_w = 0,25 tiendrait les deux fourchettes (variante V4). *Avis : garder β = 2, conforme (fiche 3) ; consigner V4 comme variante, sans issue tant qu'aucune mesure ne le demande.*
4. **Coût de la désinflation.** À λ_e = 0,2 inchangé, le coût en chômage d'un choc d'anticipations passe de 2,45 à **13,6** point-années par point (× 5,6). Aucune source de ratio de sacrifice n'a été lue : **non vérifié**. *Avis : committer λ_w au rang 7 comme prévu, publier ce coût « non calibré, #163 », et instruire #163 dès J3-f1.* Un ordre différent (#163 avancée, ou λ_w tenu jusqu'à #163) est à vous.
5. **C62.** À la table P, la formule « quasi neutre à 2 %, signe dépendant de ζ » (P219, P222) ne tient plus : ϑ = 0,15 seul donne ζ_c = 16,76, et avec λ_w = 0,18 il n'y a plus de ζ_c sur [2 ; 20]. *Avis : formule visée pour M34 : « à 2 %, faiblement explosive sur tout le domaine de ζ (module 1,00049 ; doublement en 1 415 tours) ; explosive à 10 % (doublement en 93 tours ; couverture minimale 0,61) » ; remesure sur le moteur au rang 8 (P224).*
6. **Instabilité 17 et M27.** Est-ce une question de fond hors des cinq issues, donc une condition d'arrêt ? *Avis : non pour #45 (aucune équation à changer). Republier la ligne 17 sous la forme « explosive à λ_w = 1 ; stable à λ_w calibrée », et ouvrir une issue sur le motif de M27 (§ 6.10), hors branche.*

### 6.8 Points pour `jeu` (je ne les tranche pas)

- **Vitesse salariale perçue.**
  - Un écart du salaire réel à sa norme se résorbe de moitié en **46 tours (près de 4 ans)**, contre 8 tours aujourd'hui.
  - Un point de chômage au-dessus de la normale freine la hausse des salaires de **0,36 point par an**, contre 2 points.
  - Le levier « pouvoir de négociation » (#48, J4), qui passe par ω\*, agirait en quelques années, non en quelques mois.
- **Boucle salaires – prix** : cycle de 8 à 9 ans (94 à 110 tours), visible sur une partie de 60 à 120 tours, plus lent à s'amortir (demi-vie de 10 à 25 tours selon m).
- **Chocs** :
  - une relance excessive produit un pic d'inflation d'environ 40 % plus bas (9,5 contre 16 points) ;
  - à 10 %, la récession qui suit est deux fois moins profonde ;
  - le retour à la normale est plus long, le joueur voit donc les séquelles plus longtemps.
- **Désinflation** : à loi d'anticipation inchangée, elle coûterait environ 13,6 points-années de chômage par point (question 4), un coût que le joueur percevrait comme prohibitif tant que #163 n'est pas traitée.
- À 2 %, sous φ = 0, aucun effet perceptible (doublement en 118 ans).

### 6.9 Points pour `monnaie` (frontière inflation et dette publique)

- **Indexation.** SN indexe sur π^e avec un coefficient de 1. Les sources indexent sur l'inflation passée avec 0,39 à 0,42 (S4) ou 0,565 à 0,687 (S3). Les pentes lues sont estimées sous cette indexation partielle, et leur transposition à SN est une **hypothèse**.
- **C7 et #163** : coût en chômage multiplié par 5,6 (question 4). λ_w = 0,20 donnerait λ_w = λ_e et deux persistances égales (demi-vie de 41,2 tours), coïncidence sans effet visible sur les rayons mesurés (§ 6.4.4 et 6.4.5 ; racine double non recherchée, **non vérifiée**).
- **C62** : formulation de la question 5, à relire. ζ_c dépend de ϑ (#130) autant que de λ_w.
- **Instabilité 17, M27 et C26** : la lecture (a) devient stable à λ_w calibré (§ 6.6), ce qui touche la clause de réouverture C26 (`sec:menages-inflation`).

### 6.10 Issue proposée (création sur accord)

- **Titre** : Instabilité 17 conditionnelle à λ_w : remesurer la lecture (a) des ménages à la calibration de M34 et réexaminer le motif de stabilité de M27
- **Libellés** : `needs-triage`
- **Corps** :

> *Rédigé par l'agent macro (IA).*
>
> **Constat** (instruction de #45, 16/11/2026, `docs/blocs/calibration.md` § 6.6, `outils/maquette_conjointe.py`, table de `main`). La ligne 17 de `tab:instabilites` et `sec:menages-inflation` donnent la lecture (a) des ménages (glissement mesuré au lieu de la cible dans Γ^e de H2 et dans le terme d'entretien de H4) comme explosive : 1,0275 / 1,0029 / 1,0561 / 1,0580, et stable seulement pour ν_H < 0,586 ou h < 0,604. Ces valeurs sont mesurées à λ_w = 1. À λ_w = 0,18, valeur proposée par #45, les quatre rayons valent 0,9867 / 0,9871 / 0,9940 / 0,9887 ; à λ_w = 0,284, 0,985 / 0,985 / 1,0046 / 0,998. Les deux frontières n'existent plus sur [0,3 ; 1].
>
> **À faire.**
> - Remesurer la ligne 17 et l'instabilité voisine (glissement de Haig-Simons) à la calibration retenue par M34 (μ̄, ϑ, ν_H, λ_w).
> - Dire si le motif de stabilité de M27 (lecture (c) sur la cible déclarée) tient encore, et si la clause C26 doit être relue.
>
> **Hors périmètre** : la valeur de λ_w (#45) ; la loi d'anticipation (#163).
>
> **Liens** : #45, #58, #65, M27, `tab:instabilites`, `sec:menages-inflation`.

### 6.11 Surface pour `coder` et `docwriter` (rangs 7 à 9)

- **Valeurs et sources**
  - Table du bloc 3 : `LAMBDA_W` 1,0 → 0,18 et sa source.
  - Défaut `Parametres.lambda_w` du script et sa déclaration (l. 140 et 187).
  - L'égalité est tenue par `test_valeurs_indicatives_egales_a_celles_du_script`.
- **Texte de source proposé pour `tab:calibration`** : « 0,18 par an : pente λ_w β = 0,36 point de hausse annuelle du salaire par point d'écart de chômage, égale à la pente de l'écart de chômage dans un panel de 19 pays de la zone euro (−0,364, glissement annuel de la rémunération par salarié, 2000T1–2018T4 ; F. Tagliati, BCE, Occasional Paper 232, 2019, encadré 2, tableau A) et dans la fourchette de 0,29 à 0,40 des États-Unis (Galí, NBER WP 15758, 2010, tableau 1, colonnes 6 et 8, ×4) ; correction annuelle 0,166, sous la correction européenne de 0,25 (Blanchard et Katz, NBER WP 6924, 1999, p. 5, fréquence présumée annuelle) ; la persistance régionale américaine (0,60 à 0,81, Blanchflower et Oswald, NBER WP 11338, 2005, p. 11 et 15) est tenue pour une borne haute contestée ; consulté le 16/11/2026 ».
- **Valeurs publiées** : celles du § 6.4.7, qui sont des valeurs de la maquette conjointe et du script ; les demi-vies du § 6.4.3 ; `sec:travail-conditions`.
- **Tests** : `tests/unitaires/test_travail.py` l. 133 (tuple paramétré qui contient 0,91667) est à relire par `coder` (non vérifié). Le banc P87 (`test_boucle_t3_bc3.py`) change de trajectoire, ce qui est attendu.
- **Concordance** : aucun label ajouté ni retiré (90).

### 6.12 Statut des conclusions

- **Vérifiées** (source citée, ou commande et sortie) :
  - S1 à S4, contre leur texte ; conversions ;
  - λ_w n'entre dans l'état stationnaire, ni du script (au bit, deux tables) ni du moteur (critère « Branche », 720 pas, trois π\*) ;
  - demi-vies ; critère 5 (d) à la calibration et aux variantes ;
  - rayons du socle sous φ = 0 et φ = 1 ; ζ_c, φ\* et doublements ;
  - bancs D et BF (table de `main`) ;
  - chiffres de la maquette en écart et frontières disparues ;
  - instabilité 17 à λ_w = 0,18 et 0,284 ;
  - formule du coût en chômage.
- **Hypothèses** :
  - comparabilité des pentes de formes réduites sans terme de niveau avec λ_w β, marge à sa norme ;
  - transposition de l'indexation partielle ;
  - fréquence annuelle de la correction européenne de S2 ;
  - σ_c ≈ 1,33 (correspondance du § 3.1) ;
  - biais régional de S1 selon S2 (argument de S2, non mesuré).
- **Non vérifiées** :
  - OCDE 1997 ; une source de ratio de sacrifice ;
  - bancs, C62 et instabilité 17 à la table P complète, avec ν_H de #62 (rang 8) ;
  - tests du dépôt exécutés à λ_w = 0,18 ; coût en chômage remesuré sur le moteur.

### 6.13 Avis consultés et décisions (16/11/2026, délégation P228)

**Avis de `jeu`** : **pas d'objection**. Vitesse salariale lisible (demi-vie de 46 tours, dans une partie de 60 à 120 tours, `docs/exigences.md` O5). Coût de désinflation de 13,6 point-années par point (formule, non mesurée sur le moteur) : non bloquant maintenant, mais il rendrait « laisser filer l'inflation » dominant ; **à revoir avant la démonstration J4** : #163 doit passer avant J4, sinon le point devient bloquant ; d'ici là, publié « non calibré, #163 ». À clarifier : délai du levier « pouvoir de négociation » (#48) dans l'aide ; cycle salaires – prix de 94 à 110 tours, à signaler par un indicateur de l'écart du salaire réel à sa norme ; borne N ≤ N^pa atteinte en surchauffe (préexistant).

**Avis de `monnaie`** : **pas d'objection**, avec réserves. Indexation de SN sur π^e à coefficient 1 juste pour le moteur (C1) ; transposition des pentes estimées sous indexation partielle plausible, non démontrée (hypothèse). Coût de 13,89 point-années par point vérifié par la formule 1/(λ_e λ_w β) ; l'excès vient de λ_e, non sourcé (#163) ; aucun verdict de désinflation ne doit en dépendre avant #163. C62 : formulation juste, à retoucher (ci-dessous). Instabilité 17 : à republier avec une issue hors branche, sans arrêt ; C26 porte sur la lecture (b), non sur la lecture (a) (`nations_et_marches.tex` l. 1920 et 4021, vérifié) : la stabilité de (a) ne déclenche pas C26 et ne rouvre pas M27 d'elle-même.

**Décisions de la session sous délégation** (P228 à P230 ; M34 réservée au mainteneur) :
- **λ_w = 0,18** retenu comme valeur proposée de la table soumise à M34, β = 2 inchangé (questions 1 à 3 : avis de `macro` suivis ; V4 consignée comme variante) (P232) ;
- **formulation de C62 visée pour M34** (P230 ; retouches (a) à (e) de `monnaie`) : « Sous φ = 0, à la table proposée (μ̄ = 0,60, ζ = 8, ϑ = 0,15, λ_w = 0,18) : faiblement explosive à 2 % sur ζ ∈ [2 ; 20] mesuré (module 1,00049 à ζ = 8, de 1,00047 à 1,00346 sur [2 ; 20] ; doublement en 1 415 tours) ; explosive à 10 % (doublement en 93 tours ; couverture minimale 0,61 dans la maquette, φ lu continu) ; stable sous φ = 1 (0,997502 à 2 %). Valeurs de la maquette, à remesurer au rang 8 (P224). » Elle remplace la formulation du § 3.13.7 (P222), qui ne tient plus à la table proposée ;
- **question 4** (coût de désinflation et ordre entre λ_w et #163) : **réservée au mainteneur avec M34** ; recommandation de `macro`, `monnaie` et `jeu` : committer λ_w au rang 7, publier le coût « non calibré, #163 », et consigner dans M34 la condition « #163 traitée avant la démonstration J4 » ;
- **question 6** (instabilité 17, M27) : pas une condition d'arrêt (aucune équation changée, instabilité qui disparaît ; avis de `macro` et `monnaie`) ; ligne 17 à republier par `docwriter` : « explosive à λ_w = 1 ; stable à λ_w = 0,18 (maquette, table de `main`) ; non mesurée à la table proposée » ; l'issue du § 6.10 est **rédigée, non créée** (P229).

## 7. Dossier M34 : table calibrée entière et tableau prédit consolidé

*Préparé par `macro` (expert pilote) le 16/11/2026, sous P206 et P231, pour la décision M34 (rang 2). Dépôt à `5cfcd14`, puis `fe320ed` (deux commits `docs:` seuls, § 5.12 et P233, sans effet sur les mesures) ; `git status` vide avant et après. Sondes hors dépôt, dossier `<scratchpad>/m34/` ; elles appellent sans les modifier `outils/etat_stationnaire.py`, `outils/maquette_conjointe.py`, `tests/invariants/socle_partiel.py` et les assistants de `tests/invariants/test_socle_complet.py`. Ce sont des résultats du modèle, pas des faits. Chaque conclusion est marquée **vérifiée**, **hypothèse** ou **non vérifiée**. Deux variantes : **T1**, la table proposée (μ̄ = 0,60 ; ζ = 8 ; ϑ = 0,15 ; ν_H = 1,1 ; λ_H = 0,4 ; λ_w = 0,18 ; β = 2 ; le reste inchangé) ; **T0**, la même avec ν_H = 1 (repli si #62 n'était pas retenue). Depuis P233, T1 est la table proposée entière. **Consultation de `monnaie`** : l'agent `macro` n'a pas d'outil pour lancer un autre agent ; les lignes de la banque (§ 7.11) sont à lui soumettre par la session. Son avis du § 5.12 couvre déjà C62 à T1 et la dette de référence ; les chiffres qu'il y cite sont retrouvés ici à l'identique (§ 7.7).*

### 7.1 Méthode, commandes et contrôles

Commande type, depuis `/home/user/projet_macro` : `uv run python -I <scratchpad>/m34/<sonde>.py <arguments>`. Sorties : `<scratchpad>/m34/sortie_*.txt`.
- **`base34.py`** : importe le script par son chemin et définit la chaîne cumulée des rangs 3 à 7, `calculer(replace(Parametres(), **table))`. Noms de champs exacts de `Parametres` (l. 106 à 153) : `mu_bar`, `zeta`, `vartheta`, `nu_H`, `lambda_H`, `lambda_w`, `beta` ; inchangés : `varpi_L`, `varpi_D`, `rbar`, `kappa`, `delta`, `sigma`, `tu_bar`, `lv`, `nu_F`, `tau_H`, `nu_G`, `eta_r`, `a_pi`, `a_I`, `lambda_e` et les autres.
- **`tab34.py`** : `tab:etat-stationnaire` et B1 à B26 aux trois π̄, sur les états main, #92, #55, #130, #62, #45 et T0 ; écart maximal de grille (18 points, toutes les clés) entre commits successifs ; valeurs publiées du script qui changent, par commit et par section ; #80 et racines parasites de C51. `gen34.py` en tire les tableaux ci-dessous, sans recopie à la main.
- **`cond34.py`** : conditions d'existence aux 18 points de la grille (π̄ × n_a × ν_G), à main, T0 et T1.
- **`c62_34.py`** : C62 dans la maquette (`rayon_c`, pire des deux régimes de T4 ; racine dominante de `jacobiennes_carte`), φ = 0 et φ = 1, grille de ζ de 0,5 à 20, ζ_c et φ\* par `frontiere`. **`pli34.py`** : nature de la traversée à π̄ = 0.
- **`serie34.py`** (sonde `serieH.py` du § 5.4.1, étendue à λ_w par `varier(REF.travail, lambda_w=…)` et `sentier(…, lambda_w=…)`) puis **`analyse34.py`** (Prony du § 3.13) : série signée Δi_CB du moteur sous φ = 0, choc θ_G aux tours 1 à 12.
- **`ins17_34.py`** : instabilité 17 et lectures voisines (`carte_menages`), `mc.BASE` remplacée en mémoire.
- **`maq34.py`** : relevé des chiffres publiés de la maquette (`releve`, `evaluer`), défauts de `Parametres` remplacés en mémoire.
- **`c51_34.py`** : racines de la lecture (α) sous φ = 0 et φ = 1 (méthode du § 3.13.5).
- **`banque34.py`**, **`decomp34.py`** : lignes de la banque, distribution, décomposition par issue.

**Contrôles** (tous retrouvés) :
- `main` : 449 valeurs publiées « égal », plus grand résidu 4,636e−15 ; maquette : 9 écarts préexistants sur 148 ;
- valeurs en écart à la publication : 173 (#92), 185 (#55), 284 (#130), 309 (#62), comme aux § 1.4.5, 3.4.3, 4.4.3 et 5.4.4 ;
- maquette, φ = 0, ζ = 8 : 1,000035 (A), 1,000438 (P), 1,000995 (N), 1,000490 (P avec λ_w = 0,18, § 6.4.5) ; ζ_c = 8,7633 (A) et 16,7632 (P) ;
- moteur (Prony), contrôle A : 1,0000351 ∠ ±0,1757° ; choc de 1 %, 10 %, contrôle A : arrêt au pas 543, comme au § 3.4.4 ;
- instabilité 17, table de `main` : 1,0275 / 1,0029 / 1,0561 / 1,0580, frontières 0,586 et 0,604 ; à λ_w = 0,18 : 0,9867 / 0,9870 / 0,9940 / 0,9887 (§ 6.6 : 0,9871 pour le deuxième, écart d'arrondi à la quatrième décimale) ;
- C51 sous φ = 0 à ζ = 8, ϑ = 0,10 : 1,422 % / 5,238 %, 1,000 % / 3,506 %, −1,198 % / 0,573 % (§ 3.13.5).

**Vérifiée.**

### 7.2 Table des paramètres

| Paramètre (champ du script ; table du moteur) | Avant (`main`) | **T1** | T0 | Statut de la source | Section | Décision |
|---|---|---|---|---|---|---|
| μ̄, marge normale (`mu_bar` ; bloc 4, `MU_BAR`) | 0,25 | **0,60** | 0,60 | Source lue : BCE, *Economic Bulletin* 4/2023, part salariale de la zone euro 1998–2023, 62,4 % de la valeur ajoutée brute au prix de base ; écart au coût des facteurs contesté (AMECO ALCD2 : 63,11 %, § 1.12) | § 1 | P213 (proposée) |
| ζ, élasticité de ti au taux réel (`zeta` ; bloc 6, `ZETA`) | 4 | **8** | 8 | Source lue, niveau contesté : σ ≈ 0,64 sous ζ = σ/(ϱ̄_L + δ) (hypothèse) ; Klump, McAdam et Willman (2011), Gilchrist et Zakrajšek (2007) | § 3 | P218 |
| ϑ, fonds propres visés (`vartheta` ; bloc 7, `fonds_propres_vises`) | 0,10 | **0,15** | 0,15 | Source lue : CET1 des établissements importants du MSU, 2015T3–2024T4, 14,75 % ; dénominateur contesté | § 4 | P225 |
| ϖ_L, écart du crédit (`varpi_L`) | 0,02 | 0,02 | 0,02 | Source lue (MIR, 2003–2024 : 2,09 points) ; valeur inchangée | § 4 | P226 |
| ϖ_D, écart des dépôts (`varpi_D`) | 0,01 | 0,01 | 0,01 | Source lue, fenêtre contestée (0,85 et 1,93 point sur les fenêtres de taux positifs) | § 4 | P226 ; limite de B2 : #167 |
| r̄, taux réel neutre (`rbar` ; bloc 8) | 0,01 | 0,01 | 0,01 | Choix de conception, contesté ; fourchette lue −0,5 à 1,9 % | § 4 | P226 (P208) |
| ν_H, richesse visée (`nu_H` ; bloc 5) | 1 | **1,1** | **1** | T1 : source lue, Eurostat F.2/B.6g, EA21, 2001–2023, 1,076 an → 1,0995, arrondi ; T0 : valeur indicative, sans source (8,9 % sous la source) | § 5 | P233 (T1 proposée) |
| λ_H, vitesse de richesse (`lambda_H` ; bloc 5) | 0,4 | 0,4 | 0,4 | Choix déclaré dans la fourchette lue (Parker et al., NBER WP 16684, résumé ; correspondance hypothèse) | § 5 | P233 |
| λ_w, vitesse salariale (`lambda_w` ; bloc 3, `LAMBDA_W`) | 1 | **0,18** | **0,18** | Choix déclaré, sources lues : pente λ_w β = 0,36 (Tagliati, BCE OP 232 ; Galí, NBER WP 15758) ; vitesse contestée (Blanchard et Katz contre Blanchflower et Oswald) | § 6 | P232 |
| β, effet du chômage (`beta` ; bloc 3) | 2 | 2 | 2 | Inchangé, conforme à la fiche 3 ; hors périmètre (P204) ; variante V4 consignée | § 6 | P232 |
| κ, δ (`kappa`, `delta`) | 1,6 ; 0,05 | inchangés | inchangés | Écart de B12 déclaré (+19 % sur le PIB, +7 % sur la valeur ajoutée) ; calage conjoint dans #164 | § 3 | P220 ; #164 |
| a_π, a_I, λ_e (bloc 8) | 0,5 ; 0,25 ; 0,2 | inchangés | inchangés | Non calibrés : #163 (C7) | § 6 | P204 ; ordre : question 3 du § 7.13 |
| Tous les autres paramètres | — | inchangés | inchangés | — | — | — |

**Domaine** : chaque valeur est dans le domaine de sa table et du script (`controler_domaine` sans refus à T1 et à T0 ; ν_H λ_H = 0,44 et 0,40 ; 0 < λ_w ≤ n_a ; 0 ≤ ζ ≤ 20 ; ϑ > 0). Aucun écrêtage. **Vérifiée** (`cond34.py`).

### 7.3 Tableau avant / après prédit : `tab:etat-stationnaire` (n_a = 12, ν_G = 1,15 sauf mention)

Explications par issue, une cause chacune (vérifiées aux sections citées et remesurées ici) :
- **(P)**, #92 (§ 1.4.2) : le PIB baisse d'un facteur 1/1,000404, 1/1,000804 et 1/1,002298 à π̄ = 0, 2 et 10 %, parce que ΔIN est valorisé à UC = p/(1 + μ̄). Les niveaux de D_H, YD, C, G, I, L, D_F, B, M^G, T_H, Π^Bk, Div_Bk et K sont inchangés : chaque ratio au PIB monte de ce facteur. La part salariale suit ω̄ = 1/(1 + μ̄).
- **#55** : ζ n'entre pas à Δϱ = 0. Écart de grille nul, au bit (§ 3.4.2 ; remesuré : écart maximal 0 sur les 18 points).
- **(ϑ)**, #130 (§ 4.4.2) : E^Bk = ϑ L monte de 0,05 L ; par C42, la dette consolidée monte d'autant, moins ΔV_H dû au dividende de la banque ; C baisse, θ_G résolu monte.
- **(ν)**, #62 (§ 5.4.2) : D_H monte de 10,09 % à 2 % ; par C42, ΔD_c = ΔD_H ; θ_G résolu monte (C/YD plus bas).
- **#45** : λ_w n'entre pas dans l'état d'arrivée. Écart de grille nul, au bit (§ 6.4.2 ; remesuré).
- **T0 = état après #130**, au bit : λ_w ne change rien (remesuré : écart de grille 0, 0 valeur publiée changée entre l'état #130 et T0).

La dernière colonne numérique décompose l'écart total à 2 % dans l'ordre #92, #130, #62 (#55 et #45 : 0). Sortie : `sortie_tab34.txt`, `sortie_decomp34.txt`.

| Grandeur | `main` 0 / 2 / 10 % | **T1** 0 / 2 / 10 % | T0 0 / 2 / 10 % | T1 − `main` à 2 % = #92 + #130 + #62 | Explication |
|---|---|---|---|---|---|
| Capital (a), volume | 2,000 / 2,000 / 2,000 | **2,000 / 2,000 / 2,000** | 2,000 / 2,000 / 2,000 | 0 | aucune issue (κ, t̄u inchangés) |
| Capital (b), prix courant | 2,0009 / 1,9973 / 1,9836 | **2,0017 / 1,9989 / 1,9882** | 2,0017 / 1,9989 / 1,9882 | +0,001607 = +0,00161 + 0 + 0 | #92 seul, effet (P) : PIB plus petit (ΔIN valorisé à UC = p/(1 + μ̄)) |
| Capital (c), comptable | 2,0009 / 1,5551 / 0,8360 | **2,0017 / 1,5563 / 0,8379** | 2,0017 / 1,5563 / 0,8379 | +0,001251 = +0,00125 + 0 + 0 | #92 seul, (P) |
| Part salariale | 0,80037 / 0,79890 / 0,79344 | **0,62554 / 0,62465 / 0,62130** | 0,62554 / 0,62465 / 0,62130 | −0,1743 = −0,174 + 0 + 0 | #92 seul : ω̄ = 1/(1 + μ̄), 0,8 → 0,625 |
| r̄, % | 1,00 / 1,00 / 1,00 | **1,00 / 1,00 / 1,00** | 1,00 / 1,00 / 1,00 | 0 | aucune (r̄ = 0,01 inchangé, P226) |
| Taux directeur, % | 1,00 / 3,02 / 11,10 | **1,00 / 3,02 / 11,10** | 1,00 / 3,02 / 11,10 | 0 | aucune |
| Taux réel restitué, % | 1,00 / 1,02 / 1,10 | **1,00 / 1,02 / 1,10** | 1,00 / 1,02 / 1,10 | 0 | aucune |
| ϱ_L, % | 3,000 / 2,961 / 2,818 | **3,000 / 2,961 / 2,818** | 3,000 / 2,961 / 2,818 | 0 | aucune (ϖ_L inchangé) |
| Inflation, % | 0 / 2 / 10 | **0 / 2 / 10** | 0 / 2 / 10 | 0 | aucune |
| Hausse par pas, % | 0,00000 / 0,16516 / 0,79741 | **0,00000 / 0,16516 / 0,79741** | 0,00000 / 0,16516 / 0,79741 | 0 | aucune |
| θ_G | 0,218474 / 0,219573 / 0,219568 | **0,219575 / 0,220584 / 0,220187** | 0,218765 / 0,219791 / 0,219626 | +0,001011 = +1,11e−16 + 0,000219 + 0,000793 | #130 (ϑ) puis #62 (ν) : C plus bas, θ_G résolu plus haut ; #92 et #55 : 0 |
| I/PIB, % | 13,970 / 13,945 / 13,849 | **13,976 / 13,956 / 13,881** | 13,976 / 13,956 / 13,881 | +0,01122 = +0,0112 + 0 + 0 | #92 seul, (P) ; I inchangé |
| Masse monétaire | 0,81917 / 0,81658 / 0,81108 | **0,88503 / 0,88265 / 0,87848** | 0,81921 / 0,81701 / 0,81289 | +0,06608 = +0,000657 − 0,000223 + 0,0656 | #92 (P) + ; #130 (ϑ) − (V_H) ; #62 (ν) + (D_H) |
| Dette consolidée | 0,09884 / 0,25674 / 0,51013 | **0,20444 / 0,35350 / 0,59359** | 0,13862 / 0,28785 / 0,52800 | +0,09676 = +0,000207 + 0,0309 + 0,0656 | #92 (P) ; #130 (ϑ) : C42 ; #62 (ν) : C42, ΔD_c = ΔD_H |
| Dette brute | 0,11987 / 0,27849 / 0,53645 | **0,22568 / 0,37564 / 0,62091** | 0,15972 / 0,30973 / 0,55457 | +0,09715 = +0,000224 + 0,031 + 0,0659 | idem |
| Dette brute, ν_G = 1 | 0,11712 / 0,27564 / 0,53299 | **0,22291 / 0,37274 / 0,61731** | 0,15696 / 0,30687 / 0,55107 | +0,0971 = +0,000222 + 0,031 + 0,0659 | idem |
| Dette brute affichée, % | 12,1 / 28,5 / 57,1 | **22,8 / 38,4 / 66,0** | 16,1 / 31,6 / 59,0 | +9,925 = +0,0229 + 3,17 + 6,73 | idem |
| Déficit (Domar), % du PIB | 0,1959 / 1,0185 / 5,9005 | **0,4052 / 1,4023 / 6,8659** | 0,2747 / 1,1419 / 6,1072 | +0,3838 = +0,000819 + 0,123 + 0,26 | idem : n_a γ̄ D_c |
| Solde primaire, % du PIB | −0,0971 / −0,2432 / −0,2381 | **−0,2007 / −0,3348 / −0,2770** | −0,1361 / −0,2726 / −0,2464 | −0,09163 = −0,000196 − 0,0293 − 0,0622 | idem : (i_CB/n_a − γ̄) D_c |


À 0 et 10 %, la décomposition a la même forme (sortie `sortie_decomp34.txt`). Exemples : dette consolidée +0,10560 à 0 % (= +0,00004 + 0,03974 + 0,06582) et +0,08346 à 10 % (= +0,00117 + 0,01670 + 0,06559) ; θ_G +0,001101 à 0 % (= 0 + 0,000291 + 0,000810) et +0,000619 à 10 % (= 0 + 0,000058 + 0,000560). Lignes inchangées de `main` à T1 (écart nul à toutes les décimales publiées) : capital (a), r̄, taux directeur, taux réel restitué, ϱ_L, inflation, hausse par pas. **Vérifiée.**

**T0 contre T1** : seules les lignes (ν) diffèrent ; T0 est le tableau P du § 4.4.2, au bit.

### 7.4 Valeurs résolues B1 à B26 (n_a = 12, ν_G = 1,15)

Les valeurs résolues de `tab:criteres-j3` sont publiées à π̄ = 2 % ; elles sont données ici aux trois π̄, comme le demande A2.

| N° | `main` 0 / 2 / 10 % | **T1** 0 / 2 / 10 % | T0 0 / 2 / 10 % | Explication |
|---|---|---|---|---|
| B1 | 1,4 / 1,4 / 1,4 | **1,4 / 1,4 / 1,4** | 1,4 / 1,4 / 1,4 | aucune |
| B2 | 0,80 / 0,80 / 0,80 | **0,80 / 0,80 / 0,80** | 0,80 / 0,80 / 0,80 | aucune |
| B3, % | 5,0 / 5,0 / 5,0 | **5,0 / 5,0 / 5,0** | 5,0 / 5,0 / 5,0 | aucune |
| B4 | 0,800369 / 0,798903 / 0,793445 | **0,625541 / 0,624645 / 0,621303** | 0,625541 / 0,624645 / 0,621303 | #92 |
| B5, % | 2,00 / 2,00 / 2,00 | **2,00 / 2,00 / 2,00** | 2,00 / 2,00 / 2,00 | aucune |
| B6 | 0,25 / 0,25 / 0,25 | **0,60 / 0,60 / 0,60** | 0,60 / 0,60 / 0,60 | #92, par définition |
| B7, % | 0 / 2 / 10 | **0 / 2 / 10** | 0 / 2 / 10 | aucune |
| B9, % | 1,00 / 1,02 / 1,10 | **1,00 / 1,02 / 1,10** | 1,00 / 1,02 / 1,10 | aucune |
| B10 | 1,000000 / 0,980566 / 0,912667 | **1,100000 / 1,076531 / 0,995242** | 1,000000 / 0,980566 / 0,912667 | #62 : ν_H/(1 + ν_H n_a π^{∗,pas}) |
| B11, % | 1,9819 / 3,8900 / 10,5565 | **2,1801 / 4,2707 / 11,5116** | 1,9819 / 3,8900 / 10,5565 | #62 |
| B12 | 2,00092 / 1,99726 / 1,98361 | **2,00173 / 1,99887 / 1,98817** | 2,00173 / 1,99887 / 1,98817 | #92 (P) |
| B13, % | 13,970 / 13,945 / 13,849 | **13,976 / 13,956 / 13,881** | 13,976 / 13,956 / 13,881 | #92 (P) |
| B14 | 0,4 / 0,4 / 0,4 | **0,4 / 0,4 / 0,4** | 0,4 / 0,4 / 0,4 | aucune |
| B15 | 0,16636 / 0,16605 / 0,16492 | **0,16643 / 0,16619 / 0,16530** | 0,16643 / 0,16619 / 0,16530 | #92 (P) |
| B16 | 0,81917 / 0,81658 / 0,81108 | **0,88503 / 0,88265 / 0,87848** | 0,81921 / 0,81701 / 0,81289 | #92, #130, #62 |
| B17 | 0,10 / 0,10 / 0,10 | **0,15 / 0,15 / 0,15** | 0,15 / 0,15 / 0,15 | #130, par définition |
| B19 | 0,021027 / 0,021748 / 0,026322 | **0,021242 / 0,022141 / 0,027318** | 0,021101 / 0,021875 / 0,026566 | #92 (P), #130 (ϑ), #62 (ν) : M^G suit les paiements bruts |
| B20 | 0,11987 / 0,27849 / 0,53645 | **0,22568 / 0,37564 / 0,62091** | 0,15972 / 0,30973 / 0,55457 | #92, #130, #62 |
| B21 | 0,09884 / 0,25674 / 0,51013 | **0,20444 / 0,35350 / 0,59359** | 0,13862 / 0,28785 / 0,52800 | #92, #130, #62 |
| B22, % | 0,1959 / 1,0185 / 5,9005 | **0,4052 / 1,4023 / 6,8659** | 0,2747 / 1,1419 / 6,1072 | #92, #130, #62 |


Lignes sans clé numérique dans le script, inchangées par construction : **B8** (π^e − π\* = 0), **B18** (i_L − i_CB = 2 points et i_CB − i_D = 1 point aux trois π̄, mesurés), **B24** (croissance de y = 2 %, g_pr et g_N inchangés), **B25** (r̂\* − r̄ = 0 exactement, mesuré), **B26** (i_CB − i^règle = 0 exactement). B23 est fusionnée dans B19. B5 se lit comme (1 + hausse_salaire_an)/(1 + glissement) − 1 = 2,00 %. **Vérifiée** (`tab34.py`).

### 7.5 Prédit par commit (rangs 3 à 7) : référence « mesuré égal au prédit à 1e−9 » (P206)

**Quatre états distincts seulement.** La chaîne cumulée ne produit que quatre états stationnaires : E0 = `main` ; E1 = après #92, identique au bit après #55 ; E2 = après #130, identique au bit à T0 ; E3 = après #62, identique au bit après #45 (= T1). Écarts de grille mesurés entre commits successifs (`tab34.py`, 18 points, toutes les clés) : #92 → #55 : **0** ; #62 → #45 : **0** ; état #130 → T0 : **0**. Entre #55 et #130 comme entre #130 et #62, le plus grand écart relatif de la grille porte sur `epargne_residu`, résidu d'arrondi de l'ordre de 1e−16 en valeur absolue (relatif sans objet sur une grandeur nulle), qui n'entre dans aucun tableau jugé.

| Rang | Commit | État avant → après | `tab:etat-stationnaire` et B1 à B26 | Valeurs publiées du script qui changent (sur 449) | En écart à la publication après le commit | Chiffres de la maquette non égaux (écart + sans mesure, sur 148) |
|---|---|---|---|---|---|---|
| 3 | #92 (μ̄) | E0 → E1 | lignes (P) et part salariale, B4, B6, B12, B13, B15, B16, B19 à B22 | 194 | 173 | 35 (9 avant) |
| 4 | #55 (ζ) | E1 → E1 | **aucune** (au bit) | 12 (mesure (α) de #80, § 3.4.3) | 185 | 72 |
| 5 | #130 (ϑ ; sources de ϖ_L, ϖ_D, r̄) | E1 → E2 | θ_G, lignes de dette et de déficit, B16, B17, B19 à B22 | 233 | 284 | 73 |
| 6 | #62 (ν_H, λ_H), **T1** | E2 → E3 | θ_G, masse monétaire, dette et déficit, B10, B11, B16, B19 à B22 | 246 | 309 | 72 |
| 6 | #62, **T0** (ν_H = 1 ; sources seules) | E2 → E2 | **aucune** ; commit sans changement de valeur : critère « identique au bit » | 0 | 284 | 73 |
| 7 | #45 (λ_w) | E3 → E3 (T1) ou E2 → E2 (T0) | **aucune** (au bit ; critère propre de #45, ≤ 1e−12) | 0 | 309 (T1) ; 284 (T0) | 83 (75 + 8 sans mesure), T1 comme T0 |

Un commit par issue, dans l'ordre du plan (rangs 3 à 7). Les comptes de la maquette sont cumulés à chaque état (`maq34.py`), non différenciés par commit : le nombre de chiffres qui changent à chaque commit n'est **pas mesuré**. **Vérifiée** (`sortie_tab34.txt`, `sortie_maq34.txt`, `sortie_maq34_etapes.txt`).

**Valeurs de référence**, 10 chiffres significatifs, `valeurs` du script à (ν_G, π̄, n_a = 12) ; elles se reproduisent par `calculer(replace(Parametres(), **table))` avec la table cumulée du commit. Lignes absentes : constantes de E0 à E3 (capital (a) = 2 ; r̄ = 1 ; taux directeur 1 / 3,02 / 11,1 ; taux réel restitué 1 / 1,02 / 1,1 ; ϱ_L 3 / 2,960784314 / 2,818181818 ; inflation 0 / 2 / 10 ; hausse par pas 0 / 0,1651581302 / 0,7974140429 ; B1 1,4 ; B2 0,8 ; B3 0,05 ; B5 2 ; B14 0,4 ; B18 2 et 1 ; B25 0). B4 = part salariale, B6 = 0,25 puis 0,6 dès E1, B12 = capital (b), B13 = I/PIB, B16 = masse monétaire, B20 = dette brute (ν_G = 1,15), B21 = dette consolidée.

| Grandeur (clé de `valeurs`, ν_G) | E0 = `main` | E1 = après #92 (= après #55) | E2 = après #130 (= T0) | E3 = après #62 (= T1) |
|---|---|---|---|---|
| Capital (b), prix courant (`K_courant`, 1,15) | 2,000923178 / 1,997258541 / 1,983611826 | 2,001731658 / 1,9988652 / 1,988170605 | 2,001731658 / 1,9988652 / 1,988170605 | 2,001731658 / 1,9988652 / 1,988170605 |
| Capital (c), comptable (`K_comptable`, 1,15) | 2,000923178 / 1,555096263 / 0,8359781761 | 2,001731658 / 1,556347232 / 0,8378994388 | 2,001731658 / 1,556347232 / 0,8378994388 | 2,001731658 / 1,556347232 / 0,8378994388 |
| Part salariale (`part_salariale`, 1,15) | 0,8003692711 / 0,7989034166 / 0,7934447306 | 0,6255411431 / 0,624645375 / 0,6213033141 | 0,6255411431 / 0,624645375 / 0,6213033141 | 0,6255411431 / 0,624645375 / 0,6213033141 |
| θ_G (`theta_G`, 1,15) | 0,2184743768 / 0,219572848 / 0,219567785 | 0,2184743768 / 0,219572848 / 0,219567785 | 0,2187652899 / 0,2197913784 / 0,2196262804 | 0,2195754371 / 0,220583889 / 0,2201867129 |
| I/PIB, % (`I_sur_PIB`, 1,15) | 13,97024066 / 13,94465454 / 13,84937458 | 13,97588538 / 13,95587207 / 13,8812035 | 13,97588538 / 13,95587207 / 13,8812035 | 13,97588538 / 13,95587207 / 13,8812035 |
| Masse monétaire (`masse_monetaire`, 1,15) | 0,8191730634 / 0,8165753482 / 0,8110836466 | 0,8195040532 / 0,8172322275 / 0,8129476962 | 0,819207001 / 0,8170093975 / 0,8128883615 | 0,8850281093 / 0,8826537543 / 0,878475765 |
| Dette consolidée (`dette_consolidee`, 1,15) | 0,09884071938 / 0,2567406936 / 0,5101315032 | 0,09888065632 / 0,256947224 / 0,5113038982 | 0,1386182373 / 0,2878513386 / 0,5280025523 | 0,2044393457 / 0,3534956955 / 0,5935899558 |
| Dette brute (`dette_brute`, 1,15) | 0,119867657 / 0,2784883444 / 0,5364538062 | 0,1199160899 / 0,2787123693 / 0,5376866957 | 0,1597196103 / 0,3097268108 / 0,5545687375 | 0,2256814061 / 0,3756369498 / 0,6209079682 |
| Dette brute, ν_G = 1 (`dette_brute`, 1,00) | 0,1171227293 / 0,275644561 / 0,5329887162 | 0,1171700531 / 0,2758662983 / 0,5342136422 | 0,1569649656 / 0,3068663132 / 0,5510715427 | 0,2229083955 / 0,3727416977 / 0,6173118022 |
| Dette brute affichée, % (`dette_brute_affichee`, 1,15) | 12,11583628 / 28,45087904 / 57,06550997 | 12,12073172 / 28,47376583 / 57,19665913 | 16,14394322 / 31,64225795 / 58,99249376 | 22,81114885 / 38,3757584 / 66,04935866 |
| Déficit (Domar), % du PIB (`deficit_i`, 1,15) | 0,1958921808 / 1,01850789 / 5,900522757 | 0,1959713317 / 1,01932721 / 5,914083464 | 0,2747271465 / 1,141925946 / 6,107231285 | 0,4051778408 / 1,402341599 / 6,865859138 |
| Solde primaire, % du PIB (`primaire`, 1,15) | −0,09705146142 / −0,2431509952 / −0,2380630719 | −0,0970906754 / −0,2433465936 / −0,2386101935 | −0,1361089093 / −0,2726149037 / −0,2464029545 | −0,2007384951 / −0,334784599 / −0,2770106285 |
| B10 (`richesse_YD`, 1,15) | 1 / 0,9805661827 / 0,9126671662 | 1 / 0,9805661827 / 0,9126671662 | 1 / 0,9805661827 / 0,9126671662 | 1,1 / 1,076530691 / 0,9952421511 |
| B11 (`epargne`, 1,15) | 1,981897562 / 3,889973107 / 10,55651994 | 1,981897562 / 3,889973107 / 10,55651994 | 1,981897562 / 3,889973107 / 10,55651994 | 2,180087319 / 4,270670874 / 11,51163754 |
| B15 (`depots_F`, 1,15) | 0,1663589407 / 0,1660542588 / 0,164919656 | 0,1664261586 / 0,1661878382 / 0,1652986779 | 0,1664261586 / 0,1661878382 / 0,1652986779 | 0,1664261586 / 0,1661878382 / 0,1652986779 |
| B17 (`E_sur_L`, 1,15) | 0,1 / 0,1 / 0,1 | 0,1 / 0,1 / 0,1 | 0,15 / 0,15 / 0,15 | 0,15 / 0,15 / 0,15 |
| B19 (`encaisse`, 1,15) | 0,0210269376 / 0,02174765084 / 0,02632230301 | 0,02103543361 / 0,02176514534 / 0,02638279749 | 0,02110137305 / 0,02187547219 / 0,0265661852 | 0,02124206041 / 0,02214125431 / 0,02731801243 |
| B22 (`deficit_ii`, 1,15) | 0,1958921808 / 1,01850789 / 5,900522757 | 0,1959713317 / 1,01932721 / 5,914083464 | 0,2747271465 / 1,141925946 / 6,107231285 | 0,4051778408 / 1,402341599 / 6,865859138 |

**Lecture du critère sur une valeur prédite nulle.** L'écart relatif n'est pas défini quand la valeur prédite vaut 0 : inflation et hausse par pas à π̄ = 0, B8, B25, B26 (et `i_D` à π̄ = 0, 8,7e−16, hors des tableaux). Je propose de lire « ≤ 1e−9 relatif » comme « ≤ 1e−12 en valeur absolue, dans l'unité de la grandeur » pour ces seules valeurs, comme A2 pour les grandeurs nulles. C'est une précision de critère, réservée au mainteneur (question 6 du § 7.13), à fixer avant le premier commit.

**Visa demandé** : la colonne E1 couvre les commits #92 et #55, E2 le commit #130 (et les commits #62 et #45 sous T0), E3 les commits #62 et #45 sous T1.

### 7.6 Conditions d'existence (T1 et T0 ; π̄ ∈ {0 ; 2 ; 10 %} ; n_a ∈ {4 ; 12 ; 52} ; ν_G = 1,15)

Sortie : `sortie_cond34.txt`. Valeurs à n_a = 4 / 12 / 52, dans l'ordre π̄ = 0 / 2 / 10 % à l'intérieur de chaque cellule.

| Condition | T1 | T0 | Verdict |
|---|---|---|---|
| Div_F > 0 : Div_F/(p v) | n_a = 12 : 0,22213 / 0,22378 / 0,22597 ; n_a = 4 et 52 : 0,2221 à 0,2261 | identique à T1 | tenue (ν_H n'entre pas dans le bloc 6) |
| Dividende stationnaire de la banque, marge par an (`existence_Bk`) | n_a = 12 : 0,029580 / 0,032758 / 0,045511 ; n_a = 4 : 0,029575 / 0,032751 / 0,045495 ; n_a = 52 : 0,029583 / 0,032760 / 0,045517 | n_a = 12 : 0,028758 / 0,031703 / 0,043554 ; n_a = 4 : 0,028753 / 0,031696 / 0,043528 ; n_a = 52 : 0,028760 / 0,031706 / 0,043563 | tenue |
| Coefficient de richesse λ_H/n_a + ν_H λ_H π^{∗,pas} − γ^e, par pas | n_a = 4 : 0,095037 / 0,092233 / 0,081414 ; 12 : 0,031682 / 0,030754 / 0,027203 ; 52 : 0,007311 / 0,007098 / 0,006283 | n_a = 4 : 0,095037 / 0,092035 / 0,080449 ; 12 : 0,031682 / 0,030688 / 0,026884 ; 52 : 0,007311 / 0,007083 / 0,006210 | tenu |
| ν_H λ_H < 1 | 0,44 | 0,40 | tenu |
| D1 | 0,98713 à 0,99175 | 0,98830 à 0,99250 | tenue |
| D2 | 0,96899 à 0,99978 | identique à T1 | tenue |
| Marge du plafond de E1 | 0,13665 à 0,33341 | 0,13410 à 0,31640 | tenue |
| Plafond de E6 (valeur) | 0,85052 à 1,13109 | 0,87053 à 1,13688 | > 0 ; nature inchangée |
| Caisse des entreprises, phase 4 (`caisse_DF4`) | n_a = 4 : 0,0842 / 0,0976 / 0,1192 ; 12 : 0,6947 / 0,6992 / 0,7063 ; 52 : 0,9296 / 0,9306 / 0,9322 | identique à T1 | tenue, **y compris à n_a = 4** (constat du § 1.5, dû à #92 ; `main` : −0,1789 / −0,1655 / −0,1439) |
| Caisse des ménages, phase 4 (`caisse_DH4`) | 1,0167 à 1,2180 | 1,0184 à 1,2400 | tenue |
| `calculer` aux 18 points et au point ν_G = 1 | aucun refus ; plus grand résidu 6,651e−15 | aucun refus ; 4,792e−15 | **vérifiée** |

Au point de référence ν_G = 1 (hors domaine, déclaré), la marge de E1 descend à 0,00677 (T1, n_a = 4, π̄ = 0) et 0,00384 (T0), positives. **Aucune condition d'existence n'est violée, ni aucune condition d'arrêt du plan rencontrée par interaction des paramètres.** **Vérifiée.**

### 7.7 C62 à T1 et à T0

Sorties : `sortie_c62_34.txt`, `sortie_moteur34.txt`, `sortie_pli34.txt`, `sortie_choc1pc34.txt`. Maquette conjointe, lecture (c), pire des deux régimes de T4, ζ = 8 sauf mention ; doublement = ln 2 / ln ρ, en tours.

**Maquette, à ζ = 8** :

| Table | φ = 0 : π̄ = 0 | φ = 0 : 2 % | φ = 0 : 10 % | φ = 1 : 0 / 2 / 10 % | φ\* à 2 % / 10 % (φ lu continu) | Doublement sous φ = 0 : 2 % ; 10 % |
|---|---|---|---|---|---|---|
| **T1** | 0,999538 (paire, ∠ ±0,193°) | **1,000891, paire ∠ ±0,0844°, période 4 267 tours** | **1,008216, réelle** | 0,997701 / 0,997460 / 0,997414 | **0,2860 / 0,6325** | **778 tours (65 ans) ; 85 tours (7,1 ans)** |
| **T0** | 0,999071 (paire, ∠ ±0,227°) | **1,000490, paire ∠ ±0,1410°, période 2 554 tours** | **1,007513, réelle** | 0,997752 / 0,997502 / 0,997336 | **0,1789 / 0,6100** | **1 416 tours (118 ans) ; 93 tours (7,7 ans)** |
| Contrôle P (ν_H = 1, λ_w = 1) | 0,998668 | 1,000438 | 1,010255 | 0,997246 / 0,996954 / 0,997202 | 0,1231 / 0,5874 | 1 584 ; 68 |
| Contrôle N (ν_H = 1,1, λ_w = 1) | 0,999272 | 1,000995 | 1,011201 | 0,997282 / 0,997028 / 0,997334 | 0,2466 / 0,6151 | 697 ; 62 |

Une seule traversée de 1 en φ sur 21 points, à chaque cas. Enveloppe sur 720 tours sous φ = 0 à 2 % : ×1,90 (T1), ×1,42 (T0). **Vérifiée** (maquette).

**ζ_c sur [2 ; 20]** (rayon sous φ = 0, ζ ∈ {2 ; 4 ; 6 ; 8 ; 10 ; 12,56 ; 15 ; 17 ; 20}) :
- **À 2 %, aucun ζ_c** à T1 ni à T0. T1 : de 1,004314 (ζ = 2) à 1,000790 (ζ = 20), décroissant ; T0 : de 1,003457 à 1,000469, non monotone entre 6 et 12,56 (1,000481 ; 1,000490 ; 1,000492 ; 1,000491). La boucle est faiblement explosive à 2 % sur tout le domaine de ζ mesuré.
- **À 10 %**, aucun ζ_c : de 1,009462 à 1,003264 (T1), de 1,008902 à 1,003013 (T0).
- **À π̄ = 0, un ζ_c existe dans le domaine** : **3,6605 (T1)** et **2,4926 (T0)**. En deçà, la boucle est explosive à π̄ = 0 (T1 : 1,001587 à ζ = 2 ; T0 : 1,000490). La racine qui traverse est **réelle** (argument 0 à ζ = 2 et 3), et la pente dθ_G/dr̄ du script au point de référence s'y annule (−7,5e−8 à T1, −1,7e−7 à T0) : c'est la coïncidence du § 3.13.5, retrouvée. Ce ζ_c est identique à celui de P (2,4926) et de N (3,6605) : il ne dépend pas de λ_w, ce qu'on attend d'une traversée réelle, liée à l'état stationnaire. **Vérifiée.** Conséquence : la phrase « à π̄ = 0, le rayon est inférieur à 1 sur [2 ; 20] » (§ 3.13.3, mesurée à ϑ = 0,10) ne vaut plus dès ϑ = 0,15 ; à la table retenue, elle se lit « stable à π̄ = 0 pour ζ ≥ 3,66 (T1) ».

**Corroboration par le moteur** (Prony sur la série signée Δi_CB, φ = 0, ζ = 8, choc θ_G aux tours 1 à 12) :

| Cas | Maquette | Moteur | Fenêtre et choc |
|---|---|---|---|
| T1, 2 % | 1,000891 ∠ ±0,0844° (4 267 tours) | **1,0008906 ∠ ±0,0844° (4 265 tours)** ; 1,0008908 (4 264) sur 3 000 à 12 000 | choc de 1e−9 ; pas 2 000 à 7 000, ordres 2 et 4 ; résidu relatif 2e−8 |
| T0, 2 % | 1,000490 ∠ ±0,1410° (2 554 tours) | **1,0004886 ∠ ±0,1410° (2 554 tours)** | choc de 1e−9 ; pas 3 000 à 12 000, ordres 2 et 4, et 2 000 à 7 000 |
| T1, 10 % | 1,008216 | **1,0082205** (et 1,0034) | choc de 1e−6 ; pas 300 à 900, ordre 2 ; 1 500 pas sans arrêt |
| T0, 10 % | 1,007513 | **1,0075154** | idem |

Accord de 3e−7 (T1) et 1,1e−6 (T0) sur le module, 0,0002° sur l'argument. Changements de signe de Δi_CB à T1, 2 % : pas 1 851, 3 984, 6 117, 8 250, 10 383 (demi-période 2 133 pas). **Vérifiée.**

**Protocole du test C62 « choc de 1 % »** (720 pas ; publié à ζ = 8 et ϑ = 0,10 : arrêt au pas 543 à 10 %, retrouvé) : à T1 et à T0, **aucun arrêt en 720 pas**, ni à 2 % ni à 10 %. À 10 %, Δi_CB atteint +104,6 points au pas 720 (T1) et +63,9 points (T0) : l'explosion demeure, plus lente (λ_w = 0,18). La valeur publiée « arrêt au pas 543 » disparaît ; la frontière de #143 n'est pas atteinte en 720 pas. À 2 %, Δi_CB vaut +0,35 point au pas 720 (T1). **Vérifiée** (moteur, protocole rejoué hors pytest ; les deux tests C62 ne sont pas exécutés par pytest à T1).

**C51, ligne (b), citée par C62** (`c51_34.py`, lecture (α), θ_G visé de l'état à 2 %, pente dθ_G/dr̄ entre parenthèses) :

| Table | π̄ = 0 | 2 % | 10 % |
|---|---|---|---|
| T1, φ = 0 | 1,637 % (+0,101) ; 3,477 % (−0,095) | 1,000 % (+0,053) ; 2,018 % (−0,052) | −2,435 % (+0,153) ; 0,499 % (−0,142) |
| T0, φ = 0 | 1,456 % (+0,170) ; 4,713 % (−0,154) | 1,000 % (+0,102) ; 3,048 % (−0,096) | −1,461 % (+0,093) ; 0,469 % (−0,088) |
| T1, φ = 1 | 1,270 % (+0,322) | 1,000 % (+0,320) | 1,278 % (+0,292) |
| T0, φ = 1 | 1,276 % (+0,321) | 1,000 % (+0,319) | 1,199 % (+0,293) |

Sous φ = 0, réduite de 5 % (#88) : T1 −1,800 % / 7,519 %, −2,856 % / 6,484 %, −5,599 % / 4,246 % ; T0 −1,578 % / 8,414 %, −2,549 % / 7,268 %, −5,131 % / 4,781 %. Comme au § 3.13.5 : à 2 %, la pente au point de référence est positive, la méthode des racines ne voit pas la paire complexe ; à 10 %, la racine haute à pente négative est cohérente avec la racine réelle de 1,0082. **Vérifiée.**

**Formulation à publier** (remplace celle de P232, qui vaut à T0 ; chiffres de T1, déjà cités par `monnaie` au § 5.12 et retrouvés ici) :

> **Sous φ = 0** (intérêts financés par le déficit), à la table calibrée (μ̄ = 0,60 ; ζ = 8 ; ϑ = 0,15 ; ν_H = 1,1 ; λ_H = 0,4 ; λ_w = 0,18), la boucle conjointe est :
> - **explosive à 10 %** : racine réelle de 1,008216, écart doublé en 85 tours (7 ans) ; couverture minimale qui stabilise 0,63 (maquette, φ lu continu) ;
> - **faiblement explosive à 2 %** sur tout ζ ∈ [2 ; 20] mesuré : paire complexe de module 1,000891 à ζ = 8 (de 1,00079 à 1,00431 sur [2 ; 20]), période voisine de 4 270 tours, enveloppe doublée en 778 tours (65 ans) ; couverture minimale 0,29 ;
> - **stable à π̄ = 0** au ζ retenu (0,999538), explosive à π̄ = 0 pour ζ < 3,66 (racine réelle).
>
> **Sous φ = 1**, elle est stable : 0,997701 / 0,997460 / 0,997414 à 0, 2 et 10 %.
>
> Valeurs de la maquette conjointe. Le moteur retrouve la racine dominante par identification : 1,0008906 ∠ ±0,084° à 2 %, 1,0082205 à 10 %. Les estimateurs par fenêtres ne mesurent pas une racine complexe de période plus longue que leur horizon (#166). La méthode des racines sous φ = 0 ne détecte que la parité des racines réelles supérieures à 1 : elle corrobore 10 %, pas 2 %. Le signe à 2 % ne dépend plus de ζ sur [2 ; 20], mais il dépend du reste de la calibration (ϑ, ν_H) : à ϑ = 0,10, ν_H = 1 et λ_w = 1, il basculait à ζ_c = 8,76. Résultat du modèle à la calibration de M34.

Variante T0 de la même phrase : 1,000490 (de 1,00047 à 1,00346 sur [2 ; 20]), période 2 554 tours, doublement en 1 416 tours (118 ans), couverture 0,18 ; 10 % : 1,007513, 93 tours, couverture 0,61 ; π̄ = 0 : 0,999071, explosive pour ζ < 2,49 ; moteur 1,0004886 et 1,0075154. C'est la formulation de P232, complétée de π̄ = 0 et du moteur.

Ce qui ne doit plus être dit : « quasi neutre à 2 %, signe dépendant de ζ » (P219, P222) ; « ζ_c = 8,76 » comme seuil de la table retenue ; « stable à π̄ = 0 » sans le domaine de ζ ; « arrêt au pas 543 » à 10 % ; « double l'écart en 5 ans ».

### 7.8 Instabilité 17 (lecture (a) des ménages) à T1 et à T0

Sorties : `sortie_ins17_34.txt`, confirmées par le relevé de la maquette (`sortie_maq34.txt`). Maquette ménages (`carte_menages`), rayons ; θ_H = 0,8 puis 1, régime de hausse puis de baisse.

| Table | Lecture (a) : 0,8 h / 0,8 b / 1 h / 1 b | n_a = 4 | Frontières ν_H et h (publiées 0,586 et 0,604) | Glissement dans le seul terme d'entretien (a_entretien) | Haig-Simons sur le glissement, θ_H = 1 (h / b) ; idem par pas | Lecture retenue (c), M27 |
|---|---|---|---|---|---|---|
| `main` (contrôle) | 1,0275 / 1,0029 / 1,0561 / 1,0580 | 1,0907 | 0,586 ; 0,604 | 1,0304 / 1,0058 / 1,0591 / 1,0610 | 1,0231 / 1,0271 ; 1,0223 / 1,0218 | 0,9640 / 0,9617 / 0,9564 / 0,9537 |
| μ̄ = 0,60, λ_w = 1, ν_H = 1 (après #92) | 1,0041 / 0,9851 / 1,0596 / 1,0618 | 1,0178 | **0,924 ; 0,930** | 1,0070 / 0,9879 / 1,0626 / 1,0648 | 1,0264 / 1,0302 ; 1,0219 / 1,0212 | 0,9645 / 0,9627 / 0,9565 / 0,9537 |
| **T0** | 0,9828 / 0,9832 / **0,9985** / 0,9932 | 0,9469 | n'existent plus (rayon < 1 de ν_H = 0,3 à 2) | 0,9830 / 0,9834 / **1,0014** / 0,9961 | 0,9802 / 0,9795 ; 0,9842 / 0,9818 | 0,9775 / 0,9779 / 0,9733 / 0,9735 |
| **T1** | 0,9831 / 0,9835 / **1,0019** / 0,9965 | 0,9479 | n'existent plus | 0,9833 / 0,9836 / **1,0044** / 0,9990 | 0,9797 / 0,9790 ; 0,9898 / 0,9871 | 0,9776 / 0,9779 / 0,9733 / 0,9736 |

Constats :
1. **À T1, la lecture (a) est faiblement explosive dans une configuration sur quatre** : θ_H = 1, régime de hausse, 1,0019 (période 17,8 tours). La lecture « a_entretien » l'est aussi dans la même configuration (1,0044). Les trois autres configurations sont stables. **Vérifiée** (deux chemins : sonde et relevé).
2. **À T0, la lecture (a) est stable dans les quatre** (max 0,9985), mais « a_entretien » est explosive pour θ_H = 1, hausse (1,0014). **Vérifiée.**
3. Le motif publié de M27 (« lecture (a) explosive ») ne tient donc **ni partout, ni nulle part** à la table retenue : il tient dans la configuration θ_H = 1, où les ménages reçoivent aussi le résultat des entreprises, ce qui est le cas du socle (YD contient Div_F et Div_Bk). Que cette configuration soit la plus représentative du socle est une **hypothèse**.
4. **#92 seul déplace déjà la ligne 17** : les frontières passent de 0,586 à 0,924 (ν_H) et de 0,604 à 0,930 (h), et la configuration θ_H = 0,8, baisse passe sous 1 (0,9851). La surface du § 1.4.5 ne listait pas ces chiffres de la maquette : 26 chiffres de la maquette changent avec μ̄ (§ 7.10).
5. La lecture retenue (c) est stable à T1 et à T0 (0,9733 à 0,9779), plus lente qu'à `main` (λ_w plus bas). **Vérifiée.**

Ce n'est pas une condition d'arrêt (aucune équation à changer ; la lecture (a) est écartée par M27 et n'est pas exécutée par le moteur), mais la phrase de republication décidée au § 6.13 (« stable à λ_w = 0,18 (maquette, table de `main`) ; non mesurée à la table proposée ») est à remplacer (question 4 du § 7.13), et le corps de l'issue du § 6.10 à amender (§ 7.14).

### 7.9 #80 et C51 à T1 et à T0

| Grandeur (script, `superneutralite`, ζ de la table) | `main` | #92 | #55 | **T0** (= #130) | **T1** (= #62 = #45) | Seuil |
|---|---|---|---|---|---|---|
| Δr̄_α, point (libellé publié « (ζ = 4) » à reprendre) | 0,632318 | 0,632318 | 0,296551 | **0,276390** | **0,277898** | < 0,1 |
| Écart de C/Y_o sous (α), point | 0,632684 | 0,632684 | 0,630807 | **0,690396** | **0,853730** | < 0,1 |
| r̄_α à π\* = 0 / 2 / 10 %, % (C51, φ = 1) | — | — | — | 1,276 / 1,000 / 1,199 | 1,270 / 1,000 / 1,278 | racine unique |
| Racines parasites à 0, 2 et 10 % (φ = 1) | aucune | aucune | aucune | aucune | aucune | aucune |

**#80 reste en échec attendu à T1 et à T0** (les deux grandeurs restent au-dessus de 0,1 point) : aucun succès inattendu prévu ; les deux tests `xfail(strict=True)` ne sont pas exécutés ici. **C51 tient** sous φ = 1 (racine unique sur [−60 % ; 100 %], aucun refus de `calculer`). Sous φ = 0, deux racines à chaque π̄ (§ 7.7). **Vérifiée** (valeurs du script ; tests non exécutés).

### 7.10 Valeurs publiées en écart : surface de `docwriter`

**Script d'état stationnaire** (449 valeurs ; `verdict` ≠ « égal » contre la publication actuelle) : **309 à T1, 284 à T0**.

| Section | T1 | T0 |
|---|---|---|
| `sec:banque-stationnaire` | 75 | 73 |
| `sec:finances_publiques-stationnaire` | 52 | 49 |
| `tab:etat-stationnaire` | 36 | 36 |
| `sec:investissement-stationnaire` | 28 | 28 |
| `sec:menages-stationnaire` | 20 | 0 |
| `sec:finances_publiques-emission` (+ avec `tab:calibration`) | 12 (+3) | 12 (+3) |
| `sec:banque_centrale-conditions` (+ fiche 9 § 3.Q ; + fiche 8 § 9.6) | 12 (+6 ; +1) | 12 (+6 ; +1) |
| `sec:banque_centrale-stationnaire` | 10 | 12 |
| `sec:banque_centrale-restitution` | 9 | 8 |
| `sec:finances_publiques-depense` | 7 | 7 |
| `sec:banque-restitution` | 6 | 6 |
| `sec:travail-stationnaire` | 5 | 5 |
| `sec:banque-conditions` | 5 | 5 |
| `sec:finances_publiques-restitution` | 4 | 4 |
| fiche 9 § 3.C et § 9.6 | 4 | 4 |
| `sec:prix-stationnaire` | 3 | 3 |
| `sec:finances_publiques-transferts`, fiche 9 § 6.3, fiche 9 § 3.C, `sec:banque-resultat` | 2 chacune | 2 chacune |
| `sec:finances_publiques-impots`, fiche 8 § 9.6 | 1 chacune | 1 chacune |
| `sec:finances_publiques-caisse` | 1 | 0 |

Par commit : 194 (#92), 12 (#55), 233 (#130), 246 (#62 sous T1 ; 0 sous T0), 0 (#45) valeurs changent ; détail par section dans `sortie_tab34.txt`. **Vérifiée.**

**Maquette conjointe** (148 chiffres relevés par `releve`) : **75 en écart et 8 sans mesure à T1 comme à T0**, contre 9 écarts préexistants à `main`.

| Famille (ligne du `.tex`) | Non égaux à T1 | Exemple, publié → T1 |
|---|---|---|
| `socle` : rayons, racines, demi-vies, grilles, marge conjointe (l. 3015, 3455) | 25 + 6 sans mesure | demi-vie du socle 240 → 272,5 tours ; période à 10 % 3 617 → 1 796 tours ; facteur de marge conjointe 1,7135 : plus de frontière sur [1 ; 2] |
| `finances` : C62 (l. 3256, 4079, et 8 chiffres sans ligne, préexistants) | 17 | rayon sous φ = 0, 1,001818 → 1,000891 (2 %) et 1,011036 → 1,008216 (10 %) ; doublement 381,6 → 778,4 et 63 → 84,7 ; φ\* 0,174 → 0,286 et 0,650 → 0,632 |
| `menages_inflation` (l. 1918, 4142) | 14 | a_entretien 1,059130 → 1,00437 ; Haig-Simons sur le glissement 1,0231 → 0,9797 |
| `instabilite17` (l. 4142, l. 115) | 6 + 2 sans mesure | § 7.8 ; frontières 0,586 et 0,604 disparues |
| `salaires_prix` (l. 1695) | 7 | boucle salaires – prix 0,8969 → 0,9357 (λ_w ; indépendante de μ̄) |
| `menages` (l. 2001) | 6 | 0,9640 → 0,9776 |

Comptes cumulés par état (non égaux) : 9 (`main`), 35 (#92), 72 (#55), 73 (#130), 72 (#62), 83 (#45). Les 26 chiffres apportés par #92 (ménages, ménages et inflation, instabilité 17) ne figuraient pas dans la surface du § 1.4.5. **Vérifiée** (`sortie_maq34.txt`, `sortie_maq34_etapes.txt`).

**Texte à reprendre en plus des nombres** (renvois) : `tab:calibration` (lignes μ̄, ζ, ϑ, ϖ_L, ϖ_D, r̄, ν_H, λ_H, λ_w ; textes de source des § 3.11, 4.10, 5.10, 6.11) ; statut de `tab:etat-stationnaire` (« la part salariale de 0,80 tient à μ̄ = 0,25 », « la dette consolidée de 0,26 », « le taux d'épargne de 3,89 % », dépendance à n_a et point n_a = 4) ; C62 (§ 7.7) ; ligne 17 de `tab:instabilites` (§ 7.8) ; `sec:travail-conditions` (§ 6.4.7) ; coût de la désinflation « non calibré, #163 » (§ 6.4.7, 13,89 point-années par point par la formule) ; « 21 occurrences de ζ = 4 » (§ 3.11) ; repères de `sec:menages` (§ 5.10).

### 7.11 Lignes de la banque (à soumettre à `monnaie`)

`sortie_banque34.txt`, n_a = 12, ν_G = 1,15, 0 / 2 / 10 % :

| Grandeur | `main` | T0 | **T1** | Explication de T0 à T1 |
|---|---|---|---|---|
| B17 E^Bk/L | 0,10 | 0,15 | 0,15 | #130, par définition |
| B18 écarts | 2 et 1 points | idem | idem | ϖ inchangés |
| Rendement des fonds propres, % par an | 31,23 / 36,15 / 55,36 | 21,15 / 25,10 / 40,60 | **21,70 / 25,81 / 41,91** | (ν) : ϖ_D ΔD_H accroît le résultat, E^Bk inchangé |
| Marge nette d'intérêt, % par an | 2,717 / 2,497 / 2,126 | 2,645 / 2,514 / 2,294 | **2,540 / 2,414 / 2,204** | (ν) : l'actif grossit des titres B_Bk |
| Part distribuée Div_Bk/Π^Bk | 0,9365 / 0,8903 / 0,7910 | 0,9063 / 0,8420 / 0,7151 | **0,9087 / 0,8463 / 0,7240** | (ν) |
| Π^Bk, % du PIB | 2,4999 / 2,2485 / 1,8510 | 2,5407 / 2,3441 / 2,0412 | **2,6065 / 2,4097 / 2,1068** | (ν) |
| Marge d'existence du dividende, par an | 0,029253 / 0,032180 / 0,043789 | 0,028758 / 0,031703 / 0,043554 | **0,029580 / 0,032758 / 0,045511** | (ν) : ϖ_D D/L monte |
| Canal rentier (`canal_rentier`) | 0,1514 / 0,3870 / 0,7205 | 0,2124 / 0,4337 / 0,7441 | **0,3129 / 0,5311 / 0,8284** | (ν) : proportionnel à D_c |
| B19, B20, B21, B22 | § 7.4 | | | |

Distribution des entreprises (#55), identique à T1 et T0 : 0,88598 / 0,82751 / 0,72390 ; sous −2 points, 0,86624 / 0,79812 / 0,68114, dans [0,2 ; 0,9]. **Vérifiée** (mesure). Le jugement de fond sur ces lignes revient à `monnaie` (pilote du bloc 7, frontière dette publique) : **non consulté par `macro`** dans ce dossier.

### 7.12 Risques signalés pour le rang 8 (non mesurés ; aucun banc de 720 pas lancé)

- **Bancs D et BF** (P184) : à T1, la marge de E1 monte (0,17026 contre 0,15979 à 2 %) et la valeur du plafond de E6 baisse (1,08283 contre 1,09859). Lecture statique, **hypothèse** : le banc D (θ_G × 1,25, × 1,60 à 10 %) dépasserait encore le plafond de E1 dès le pas 0 (1,25 × (1 − 0,17) ≈ 1,04 > 1 ; à 10 %, 1,60 × (1 − 0,33) ≈ 1,07) ; le banc BF lierait plus tôt E6. **Non vérifié** : dynamique et λ_w = 0,18 changent les trajectoires.
- **Frontière de #143** : à T1 et T0, le choc de 1 % sous φ = 0 à 10 % ne l'atteint plus en 720 pas (§ 7.7) ; les bancs d'empreintes à φ = 1 ne sont pas mesurés.
- **Stationnarité** (`test_stationnarite_du_socle_complet`) : à λ_w = 0,18, la demi-vie du socle sous φ = 1 passe de 240 à 272,5 tours (maquette) : l'horizon S2 (20 demi-vies) s'allonge ; l'arrondi s'amortit plus lentement. **Non vérifié.**
- **Test zéro à φ = 1** (demandé par `monnaie`, § 5.12) : relève de J3-e1 ; le rayon de la maquette sous φ = 1 reste sous 1 à T1 (0,997460 à 2 %). **Non vérifié** sur le moteur.

### 7.13 Questions réservées au mainteneur pour M34

1. **Table entière** : T1 (proposée sous P228 à P233) ou T0 (repli, ν_H = 1) ? *Avis : **T1**.* Chaque valeur repose sur une source lue ou un choix déclaré dans une fourchette lue ; aucune condition d'existence ni d'arrêt n'est rencontrée (§ 7.6) ; `jeu` et `monnaie` n'ont pas d'objection (§ 3.14, 4.13, 5.12, 6.13).
2. **Visa du tableau prédit** (P206) : colonnes E1, E2, E3 du § 7.5 comme référence « mesuré égal au prédit à 1e−9 » de chaque commit. *Avis : viser.*
3. **Ordre entre λ_w et #163** (§ 6.7, question 4 ; P232). À λ_e = 0,2 inchangé, le coût en chômage d'un choc d'anticipations passe de 2,45 à 13,6 point-années par point (formule 1/(λ_e λ_w β) ; mesure moteur non refaite). *Avis (`macro`, `monnaie`, `jeu`) : committer λ_w au rang 7, publier ce coût « non calibré, #163 », et consigner dans M34 la condition « #163 traitée avant la démonstration J4 ».* Alternatives : avancer #163, ou tenir λ_w jusqu'à #163.
4. **Instabilité 17** (§ 7.8). Republication de la ligne 17 à la table retenue. *Avis : « explosive à λ_w = 1 (table indicative) ; à la table de M34, faiblement explosive pour θ_H = 1, régime de hausse (1,0019 ; a_entretien 1,0044), stable dans les trois autres configurations ; frontières en ν_H et h disparues ». Pas une condition d'arrêt ; issue du § 6.10 à créer avec le corps amendé du § 7.14 (P229).*
5. **C62** : formulation du § 7.7 (T1) au lieu de celles de P222 et P232. *Avis : l'adopter, ζ_c restant à remesurer au rang 8 (P224) ; elle tient compte de la corroboration par le moteur et du ζ_c à π̄ = 0 que `monnaie` demandait (§ 5.12).*
6. **Critère sur les valeurs prédites nulles** (§ 7.5) : « ≤ 1e−12 en valeur absolue » pour les seules valeurs prédites exactement nulles. *Avis : l'écrire dans le plan avant le premier commit (précision prospective du critère, non un déplacement).*
7. **Dette de référence** (§ 5.8, question 5 ; § 4.14) : 38,4 % du PIB affiché à 2 % (T1), 31,6 % (T0), 28,5 % (`main`) ; 81,8 % observés (EA20, 2001–2023), non comparable (ni non-résidents, ni assureurs, ni titres des ménages). *Avis : publiée sans cible ; réserve de `monnaie` pour les seuils futurs de la prime souveraine, rapportés à la dette du modèle.*
8. **Surface de #92** : 26 chiffres de la maquette (ménages, instabilité 17) changent avec μ̄ et manquaient au § 1.4.5. *Avis : les verser à la surface du commit #92 ; aucune décision de fond.*
9. **Questions encore ouvertes des sections 1 à 6**, sans effet sur la table : millésime d'AMECO (§ 1.12) ; période du chiffre « 50-90 % » de Parker et al. à confirmer sur l'article, et Fagereng, Holm et Natvik (2021) sur un hôte non ouvert (§ 5.2) ; OCDE 1997 et une source de ratio de sacrifice (§ 6.12, #163) ; coupe du seul canal rentier (§ 3.13.6). Aucune ne bloque M34.

### 7.14 Corps amendé de l'issue du § 6.10 (création sur accord, P229)

- **Titre** : Instabilité 17 : remesurer la lecture (a) des ménages à la calibration de M34 et réexaminer le motif de stabilité de M27
- **Libellés** : `needs-triage`
- **Corps** :

> *Rédigé par l'agent macro (IA).*
>
> **Constat** (`docs/blocs/calibration.md`, § 6.6 et § 7.8 ; `outils/maquette_conjointe.py`, `carte_menages`). La ligne 17 de `tab:instabilites` et `sec:menages-inflation` donnent la lecture (a) des ménages comme explosive : 1,0275 / 1,0029 / 1,0561 / 1,0580 (θ_H = 0,8 puis 1, régimes de hausse puis de baisse), stable seulement pour ν_H < 0,586 ou h < 0,604. Ces valeurs sont mesurées à la table indicative (μ̄ = 0,25, λ_w = 1). À la table de M34 (μ̄ = 0,60, ν_H = 1,1, λ_w = 0,18) : 0,9831 / 0,9835 / **1,0019** / 0,9965 ; lecture « a_entretien » : 0,9833 / 0,9836 / **1,0044** / 0,9990 ; frontières en ν_H et h disparues sur [0,3 ; 2]. μ̄ seul les déplace déjà (0,924 et 0,930). La lecture retenue (c) reste stable (0,9733 à 0,9779).
>
> **À faire.**
> - Republier la ligne 17 et l'instabilité voisine (glissement de Haig-Simons) à la calibration de M34.
> - Dire si le motif de stabilité de M27 tient encore : la lecture (a) reste explosive dans la seule configuration θ_H = 1 (ménages qui reçoivent le résultat des entreprises, comme au socle).
> - C26 porte sur la lecture (b) (`monnaie`, § 6.13) : la stabilité de (a) ne la déclenche pas.
>
> **Hors périmètre** : les valeurs de λ_w (#45) et de ν_H (#62) ; la loi d'anticipation (#163).
>
> **Liens** : #45, #62, #92, #58, #65, M27, `tab:instabilites`, `sec:menages-inflation`.

### 7.15 Statut des conclusions

- **Vérifiées** (commande et sortie) :
  - tableau prédit aux trois π̄ et décomposition par issue ; quatre états distincts ; écarts de grille nuls pour #55, #45 et T0 ;
  - valeurs publiées du script par commit et par section ; chiffres de la maquette par état ;
  - conditions d'existence aux 18 points, à T1 et T0 ;
  - C62 dans la maquette (rayons, nature, ζ_c, φ\*, doublements), corroboré par le moteur à 2 et 10 % (T1 et T0) ; ζ_c à π̄ = 0 et sa nature réelle ; protocole du choc de 1 % rejoué ;
  - C51 sous φ = 0 et φ = 1 ; #80 (valeurs du script) ;
  - instabilité 17 et lectures voisines, par deux chemins ;
  - lignes de la banque (mesure).
- **Hypothèses** :
  - représentativité de la configuration θ_H = 1 pour le socle (§ 7.8) ;
  - lecture statique des bancs D et BF (§ 7.12) ;
  - correspondances déjà déclarées dans les sections 1 à 6 (σ, pentes salariales, aubaine).
- **Non vérifiées** :
  - bancs d'empreintes, stationnarité du socle complet, test zéro et tests du dépôt à T1 (rang 8, J3-e1) ;
  - nombre de chiffres de la maquette qui changent à chaque commit (seuls les comptes cumulés sont mesurés) ;
  - consultation de `monnaie` sur les lignes de la banque (§ 7.11), non faite par `macro`.
