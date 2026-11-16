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
> - **À 2 %** : paire complexe de module 1,000035 et de période voisine de 2 050 tours (171 ans). L'enveloppe de l'écart double en 19 750 tours environ, et croît de 2,6 % en 720 tours. Couverture minimale : 0,011.
> - **Le module passe 1 à ζ_c = 8,76**, soit σ ≈ 0,70 sous la correspondance ζ = σ/(ϱ̄_L + δ). Ce seuil se trouve dans la fourchette de σ lue (0,5 à 1,0) : la boucle est faiblement explosive en deçà et faiblement amortie au-delà.
> - **À π̄ = 0** : module de 0,998235.
>
> Ce sont des valeurs de la maquette conjointe. Le moteur retrouve la racine dominante par identification sur 12 000 pas : 1,0000351 de période 2 049 tours à 2 %, 1,0096608 à 10 %, 0,9999998 à ζ_c. Les estimateurs par fenêtres ne mesurent pas une racine complexe de période plus longue que leur horizon. La méthode des racines sous φ = 0 ne voit que les racines réelles : elle corrobore 10 %, pas 2 %.

**Ce que le texte ne doit pas dire** :
- « stable à 2 % » : le module 1,000035 est au-dessus de 1 ;
- « converge sur 2 700 pas » : réfuté ;
- « ζ freine la boucle » : le module n'est pas monotone en ζ à π̄ = 0 ;
- un temps de doublement à 2 % issu des estimateurs par fenêtres (0,999746, 0,997465 : artefacts de phase).

À reprendre aussi :
- les valeurs « 381 tours » et « 63 tours », qui deviennent environ 19 750 et 72 tours à ζ = 8 ;
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

