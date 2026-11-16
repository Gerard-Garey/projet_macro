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

