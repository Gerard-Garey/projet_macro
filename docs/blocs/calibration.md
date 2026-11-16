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

