"""
Nations & Marchés — prototype v2.0 intégré (économie fermée, actifs optionnels).
Implémente les blocs : production (Cobb-Douglas + Leontief), emploi, salaires (Phillips),
investissement (q de Tobin + rationnement), ménages 3 strates (Keynes / Euler / mixte, LES),
marchés par ordres avec tâtonnement borné et rationnement, banque (monnaie endogène, CAR),
banque centrale (Taylor, ZLB, avances au Trésor), État (impôts, transferts, achats, dette,
taux apparent, prime), anticipations et crédibilité, terme d'encaisses réelles.
Pas de temps : semaine. Révisions mensuelles : salaires, prix administrés, IPC, anticipations, politique.
Toute la monnaie passe par un grand livre (Ledger) : les identités de bilan tiennent par construction.
"""
import numpy as np
try:
    from .households import plan_household,ConsumptionChoice
    from .buffer_stock import plan_buffer_stock
    from .wealth_utility import plan_wealth
    from .portfolio import household_balance_sheets
    from .bank_equity import change_book,begin_reconciliation,reconcile,redenominate_journal
    from .numerical_audit import central_bank_check
    from .treasury import rebate_plan, redeem_public_debt, redeemable_debt, purchase_public_bonds
    from .policies import wealth_buffer_weeks, income_tax_rates, update_natural_rate, update_taxes, public_productivity_feedback
except ImportError:
    from households import plan_household,ConsumptionChoice
    from buffer_stock import plan_buffer_stock
    from wealth_utility import plan_wealth
    from portfolio import household_balance_sheets
    from bank_equity import change_book,begin_reconciliation,reconcile,redenominate_journal
    from numerical_audit import central_bank_check
    from treasury import rebate_plan, redeem_public_debt, redeemable_debt, purchase_public_bonds
    from policies import wealth_buffer_weeks, income_tax_rates, update_natural_rate, update_taxes, public_productivity_feedback

MODEL_VERSION = "2.5-claude-w10-20260914"
try:
    from . import eight_points as eight, mortgage_vintages as mortgages
except ImportError:
    import eight_points as eight, mortgage_vintages as mortgages
WEEKS = 52
DECISION_WEEKS = 4
PERIODS_PER_YEAR = WEEKS / DECISION_WEEKS

def wk(r):  # taux annuel -> hebdomadaire
    return (1.0 + r) ** (1.0 / WEEKS) - 1.0

class Ledger:
    """Comptes de dépôt (passif de la banque) + réserves + créances. Chaque transfert débite/crédite."""
    def __init__(self):
        self.shortfalls = []; self.entries = []; self.dep = {}      # dépôts par agent
    def open(self, name, amount=0.0):
        self.dep[name] = amount
    def transfer(self, frm, to, amt):
        if not np.isfinite(amt): raise FloatingPointError("Transfert non fini")
        requested=amt
        if amt <= 0: return 0.0
        if frm != "FX" and frm[0] in "HFG":      # ménages, entreprises, État : pas de découvert (seule la banque crée la monnaie) ; FX = compte de change de la BC
            amt = min(amt, max(self.dep[frm], 0.0))
            if requested-amt > 1e-9*max(1.,requested):
                self.shortfalls.append((frm,to,requested,amt))
            if amt <= 0: return 0.0
        self.dep[frm] -= amt
        self.dep[to] += amt
        self.entries.append((frm,to,float(amt)))
        return amt
    def total(self):
        return sum(self.dep.values())

class Params:
    BOUNDS = {'chi_Z': (0.0, 0.9), 'chi_E': (0.0, 0.9), 'LTV': (0.3, 1.0), 'margin': (0.0, 1.5), 'kappa_CAR': (0.02, 0.3), 'pi_star': (0.0, 0.10)}
    def __init__(self, **kw):
        # secteurs : 0 alimentation, 1 énergie, 2 biens de consommation, 3 biens d'équipement
        self.eight_corrections = False  # opt-in; preserves old snapshots
        self.audit_corrections = False
        self.crisis_accounting = 'legacy_survival'
        self.neutral_redenomination = False
        self.joint_proxy_domain_guard = False
        self.pricing_cost_mode = 'legacy'
        self.precise_fiscal_deltas = False
        self.bank_reconciliation_mode = 'legacy_sum'
        # --- W10 (audit Claude, 14/09/2026) : trois corrections directes, toutes explicites ---
        self.residual_tolerance = 'legacy'      # 'stock_aware' : une identite de STOCK (livre bancaire ~5e7) ne peut etre verifiee a mieux que n*eps*|stock| ; la tolerance en Y hebdomadaire (F34) etait mal posee
        self.residual_eps_multiple = 64          # multiple d'epsilon machine applique a la somme des |operandes| de l'identite
        self.depression_detector = True          # F39 : indicateur de depression reelle (observation seule, aucune retroaction)
        self.depression_threshold = 0.5          # PIB reel (52 sem. glissantes) < seuil x maximum des 5 annees precedentes
        self.depression_weeks = 13               # pendant au moins 13 semaines
        self.util_normal = 0.8                   # 'normal_average' : couts fixes repartis sur max(Y, util_normal x capacite) (Godley-Lavoie 2007 ch.8, cout normal) ; F05 — ESSAYE SEUL 60 ANS : n'arrete pas la hausse du prix de l'equipement (x4,8). Piste fermee.
        self.joint_price_search = 'legacy'
        self.joint_price_search_steps = 12
        self.mortgage_contract_mode = 'legacy'
        self.mortgage_term_weeks = 1040
        self.mortgage_registry = False
        self.equity_valuation_mode = 'book_ratio'
        self.resolution_notice_weeks = 4
        self.resolution_max_haircut = .5
        self.resolution_cooldown_weeks = 52
        self.crisis_recovery_weeks = 52
        self.crisis_recovery_inflation = .10
        self.agreement_notice_weeks = 4
        self.agreement_max_share = .05
        self.agreement_deposit_cap = .25
        self.rate_speed_limit = .02  # annual rate change, 2 percentage points/year
        self.nsec = 4
        self.alpha = np.array([0.30, 0.40, 0.33, 0.33])
        self.delta = np.array([0.035, 0.045, 0.04, 0.05])       # /an
        # coefficients techniques a[k, j] : k consommé par j
        self.a = np.array([[0.00, 0.00, 0.05, 0.00],
                           [0.10, 0.05, 0.12, 0.10],
                           [0.00, 0.00, 0.00, 0.00],
                           [0.00, 0.00, 0.00, 0.00]])
        self.equipment_supply_response = True  # partial correction; not a stationary release
        self.equipment_price_mode = 'average_floor'  # 'orders_marginal' avoids fixed costs divided by zero realized output
        self.g0 = 0.015                    # PGF tendancielle /an
        self.tfp_trend_mode = 'common_tfp'  # 'balanced_sectoral': research option, common labor-augmenting trend
        self.mu_ema = 0.10                 # moyenne mobile des ventes
        self.s_star = 4.0                  # stock cible en semaines
        self.lam_inv = 0.03
        self.lam_L = 0.10                  # /semaine
        self.psi = 0.9                     # part du profit net distribuée
        self.payout_mode = 'psi'           # P1 (Claude, 15/09/2026) : 'leverage_target' — retention = (1-ell_star) x investissement + lam_ell x (ecart de levier signe)/52 ; dividende = residu ; psi endogene (Godley-Lavoie 2007 ch.11)
        self.ell_star = 0.30               # levier cible Loans/(pK K)
        self.lam_ell = 0.10                # vitesse annuelle de correction de l'ecart de levier
        self.m_bar = 8.0                   # trésorerie cible en semaines de CA
        self.iota = 0.20                   # Tobin
        self.ell_bar = 0.6; self.eta_ell = 2.0
        self.phi_F = 0.05                  # capital liquidé en faillite (le reste est repris)
        self.tauS = 0.20                   # cotisations employeur
        # salaires
        self.phi_u = 0.30; self.u_n = 0.05; self.gamma_A = 1.0; self.varpi_w = 1.0
        self.markup_inv = 0.0    # sensibilité hebdomadaire de la marge à l'écart de stocks (jambe 2, option)
        # ---- v2.0 : bloc salaires-prix WS-PS (Layard-Nickell-Jackman 1991) ----
        self.price_basis = "average"  # coût moyen majoré ; variante marginale expérimentale
        self.wsps2 = True          # active le bloc v2.0 : courbe de salaire avec niveau, équation de prix unique en marge, désancrage par le seigneuriage
        self.eps_goods = None      # élasticité de substitution entre variétés (Dixit-Stiglitz) : marge normale mu_n = 1/(eps-1) = 0,167 ; PARAMETRE D'ARCHETYPE (concurrence)
        self.kappa_mu_z = 0.05     # réponse hebdomadaire de la marge à l'excès de demande z
        self.kappa_mu_s = 0.01     # réponse hebdomadaire de la marge à l'écart de stocks
        self.lam_mu_n = 0.005      # rappel hebdomadaire de la marge vers la marge normale
        self.price_demand_feedback = False  # R3 : tatonnement direct de la v1, en complement du rappel au cout ; defaut inchange.
        self.mu_fast = 0.25        # vitesse hebdomadaire du prix vers (1+mu) x coût unitaire
        self.beta_u = 2.0          # (session 3 : 1,0 -> 2,0 ; provisoire) élasticité du salaire cible au chômage (Blanchflower-Oswald : -0,1 en log-log ; ici semi-élasticité sur u en points : 1,0 = -1 % de salaire par point de chômage)
        self.h_ins = 0.0           # (session 3 : 0,5 -> 0 ; provisoire : le poids des insiders élève le chômage d'équilibre de 2 points) poids des insiders : u de référence = h x chômage récent + (1-h) x u_n0 (Blanchard-Summers 1986)
        self.lam_w = 1.0           # (session 3 : 0,5 -> 1,0 ; 2,0 est instable) vitesse annuelle de convergence du salaire vers sa cible
        self.phi_S = 0.10          # fraction de l'excédent de stocks offerte chaque semaine (v2.0)
        self.lam_inv_2 = 0.02      # (session 3 : 0,01 -> 0,02) correction hebdomadaire des stocks vers la cible (v2.0)
        self.lam_L_2 = 0.04        # vitesse hebdomadaire d'ajustement de l'emploi (v2.0)
        self.G_on_potential = True # potentiel de production courant au chômage structurel
        self.phi_uf = 0.0          # stabilisateur budgétaire : élasticité des dépenses à l'écart de chômage (v2.0, voie budgétaire)
        self.d_scale = np.ones(4)  # v2.0 : facteurs d'équilibre initial du marché des biens (voir solve_init)
        self.price_mode = 'markup' # 'tat' : tâtonnement ancré sur le prix de monopole ; 'markup' : prix = marge vivante x coût (sessions 1-4)
        self.mu_c2 = 0.05          # rappel hebdomadaire vers le prix de monopole (mode 'tat')
        self.ups_s = 0.5           # désancrage : poids (annuel) du seigneuriage observé dans les anticipations quand la crédibilité est perdue (Sargent 1982)
        self.L_prof_va = False   # demande de travail au produit marginal (chantier salaires-prix) : OPTION, non retenue par défaut tant que le bloc prix n'est pas recalibré — fixe la part salariale (0,62, plus de dérive), K/Y 2,9-3,2, sigma(u) 0,1 pt, mais rend l'économie contrainte par l'offre avec des prix trop lents : monétisation non inflationniste (H7), pas d'effondrement (C2), multiplicateur 0,49 (T3). Voir RAPPORT_partage_etape_4
        self.idx_catchup = 0.0   # rattrapage de l'indexation salariale sur l'inflation réalisée (option, chantier partage)
        self.iota_Pi = 0.0   # investissement induit par le cash-flow (FHP 1988), OPTION NON RETENUE par défaut : effet stationnaire nul (K/Y borné par part du capital / coût d'usage : +0,04 pour iota_Pi 0,2-0,5) et H5 (archétype agraire) passe de 7,8 % à 15 % de chômage (profits volatils -> investissement volatil). Voir RAPPORT_partage_etape_2
        self.build_norm = True; self.lam_qZ = 1.0 / 52   # build_norm : seuil de rentabilité initial fixe ; lam_qZ héritée, inactive
        self.markup_live = False; self.lam_mk = 1.0 / 52   # voie 2 : marge normale vivante (option)
        self.ws_anchor = False; self.kappa_ws = 0.5; self.lam_ws = 1.0 / PERIODS_PER_YEAR          # rappel de la part salariale sectorielle vers 1 - alpha_j (option, chantier absorption)
        self.eta_u = 0.03 / PERIODS_PER_YEAR; self.eta_u2 = 0.01 / PERIODS_PER_YEAR   # hystérèse (mensuel)
        # ménages
        self.N = np.array([600.0, 300.0, 100.0])           # B, M, H
        self.omega = np.array([0.05, 0.25, 0.70])          # part du capital
        self.share_h = np.array([0.55, 0.30, 0.15])        # part de la masse salariale par strate (qualification)
        self.c = np.array([0.95, 0.90, 0.80]); self.cV = np.array([0.0, 0.04, 0.08])
        self.c_assets_B = np.array([0.90, 0.78, 0.55])   # calibrage B (v1.6, 10/09) de l'économie à actifs (référence de jeu) ; les suites A, C, H le passent explicitement ; l'ancienne valeur (0,95 ; 0,85 ; 0,70) donnait C/Y 0,74 et un taux d'épargne des ménages nul
        self.rho = 0.01; self.sigma = 1.0; self.kappaE = 0.9
        self.household_mode = "euler"  # "income" : contre-factuel de validation
        self.euler_share = np.array([0., 0.5, 1.])
        self.hh_horizon_years = 20.
        self.wiu_epsilon = 0.
        self.wiu_utility_scale = 1.
        self.wiu_targets = np.array([1.35,1.35,1.35])
        self.wiu_shift_weeks = 1.
        self.wiu_wealth_basis = 'liquid'  # net: conditional on given illiquid-wealth path, not joint portfolio optimization
        self.wiu_external_targets = np.zeros(3)
        self.hh_return_mode = 'anchored'  # current: extrapolate current financial return, no imposed far anchor
        self.investment_signal = 'accounting'  # marginal_product: sensitivity, not a full q-value solution
        self.investment_mode = 'legacy_q'  # 'sales_cost': conditional cost-minimizing capital target
        self.capital_adjust_speed = .20  # annual convergence of capital to the sales target
        self.capital_finance = 'forecast_wacc'  # or 'legacy_loan', paired diagnostic
        self.capital_price_years = 2.
        self.capital_price_forecast = 'stationary'  # adaptive is an explicit bubble-prone ablation
        self.joint_anchor_years = 2.
        self.wealth_net_debt = False  # subtract margin debt in marked household wealth
        self.margin_refinancing = True  # cash-out against existing equity, not secondary-market trading
        self.mortgage_refinancing = True
        self.wage_indexation_mode = 'legacy_asymmetric'
        self.public_productivity_mode = 'legacy_growth'
        self.public_capital_elasticity = .05
        self.portfolio_mode = 'legacy'
        self.joint_years = 10.
        self.joint_periods = 16  # deprecated snapshot field; every horizon now uses weekly dates
        self.joint_fee = .02
        self.joint_risk = .01
        self.joint_terminal = 'balanced_policy'
        self.joint_dividend_years = 1.
        self.hh_return_gap = 0.  # annual log return below rho+sigma*g
        self.hh_risk_probability = .02; self.hh_risk_loss = .90
        self.hh_buffer_weeks = 26.
        self.hh_liquid_wealth_ratio = None  # theta times annual permanent income at terminal date
        self.hh_rate_reversion = 2.
        self.hh_income_speed = 0.02
        self.hh_growth_min = -0.02; self.hh_growth_max = 0.04
        self.hh_income_growth = None  # prévision réelle adaptative : productivité observée lissée ; nombre = scénario exogène
        self.cash_consumption_fraction = 0.9  # ménages à règle de revenu
        self.gov_cash_ratio = 0.04
        self.treasury_redeem_all = True
        self.treasury_rebate_speed = 12.0  # annual adjustment speed; zero disables the dividend
        self.treasury_rebate_cap = 0.10    # hard annualized share of GDP paid at most each week
        self.treasury_drawdown_cap = 0.01 # extra payment above last week's pre-dividend surplus, /year; None = fixed cap
        self.fiscal_on_net_debt = False
        self.public_growth = None  # ancien paramètre retiré : le potentiel dépend des facteurs présents
        self.valuation_smoothing = 0.0  # années ; 0 = coût de remplacement courant
        self.audit_strict = False
        self.mortgage_amortization = 0.02
        self.mortgage_service_share = 0.30
        self.gamma = np.array([[0.30, 0.10, 0.05], [0.30, 0.10, 0.05], [0.30, 0.10, 0.05]])  # subsistance /tête (aliment, énergie, conso)
        self.beta_les = np.array([[0.35, 0.15, 0.50], [0.25, 0.12, 0.63], [0.15, 0.10, 0.75]])
        self.sB = 0.30                                      # part de l'épargne en obligations
        self.participation = 0.6
        # prix
        self.kappa_p = 0.10; self.kappa_bar = 0.05; self.varpi_p = 0.5; self.mu_c = 0.05
        self.xi_M = 0.02 / 4                                # /semaine (0,02/mois)
        self.V0 = 1.6; self.a_cagan = 2.0; self.money_norm = True; self.tau_m = 5.0   # v1.6 : norme lente des encaisses (5 ans) ; V0 ne sert plus qu'à l'initialisation de M
        # banque
        self.mL = 0.01; self.mD = 0.01; self.rho1 = 0.05; self.rho2 = 0.5; self.kappa_CAR = 0.09
        self.psi_bank = 0.5
        # banque centrale
        self.a_pi = 0.5; self.a_y = 0.5; self.pi_star = 0.02; self.okun = 2.0
        self.smooth_pi = 0.10; self.w_rule = 1.0; self.rule_months = 1; self.w_fore = 0.0
        self.rho_i = 0.70                                    # lissage mensuel
        # anticipations / crédibilité
        self.lam0 = 0.20; self.lam1 = 0.6; self.pi_hyper = 0.5; self.ups = 0.05
        self.nu1 = 0.01; self.nu2 = 0.5; self.nu3 = 0.2; self.eps_bar = 0.01
        # État
        self.tauW = np.array([0.05, 0.12, 0.25]); self.tauK = 0.25; self.tauPi = 0.20; self.tauC = 0.15
        self.repl = 0.5                                     # taux de remplacement chômage
        self.minima = 0.30                                  # minima sociaux (fraction du salaire moyen) pour strate B non employée ? (inactifs)
        self.G_share = 0.085                                 # achats publics de biens de conso, part du PIB
        self.Ginv_share = 0.03                              # investissement public (biens d'équipement), part du PIB
        self.LG_share = 0.10                                # emploi public, part des actifs
        self.Tbar = 7.0                                     # maturité
        self.s0 = 0.01; self.s1 = 0.06; self.b_bar = 0.8; self.s2 = 0.003; self.s4 = 0.03; self.kdom = 1.0
        self.eps_ev = 0.3; self.eps_adm = 0.95
        self.C_cal = 0.57
        self.order_cap = 1.1
        self.util_lo = 0.8; self.util_hi = 0.95
        self.eta_G = 0.02; self.zeta_G = 0.5
        self.phi_x = 0.3; self.u_n_floor = 0.03
        self.omega_G = 0.15   # poids des services publics dans le niveau de vie
        self.phi_liq = 0.0    # ratio de liquidité : titres publics détenus par la banque en part des dépôts (0 = désactivé)
        self.fert_endo = False; self.eta_fert = 0.5; self.eta_mort = 0.3   # fécondité et mortalité endogènes (niveau de vie, santé)
        # ---- chantiers v1.2 ----
        self.fiscal_rule = False; self.b_target = 0.6; self.phi_b = 0.3      # règle budgétaire : dépenses corrigées de l'écart de dette
        self.cap_on_capacity = False; self.survival = True; self.s_surv_slope = 2.0                        # économie de survie : unité de compte stable spontanée en forte inflation
        self.collapse_machine = True; self.collapse_weeks = 26; self.collapse_reforms = 2   # machine à états : bascule en économie de survie
        self.surv_util = 0.6; self.surv_pi = 0.5; self.M_conv = 0.6                                             # production à 60 % du potentiel, inflation résiduelle 50 %/an en unité stable
        self.equity_fund = True; self.psi_fundE = 2.0                          # actions : rappel vers la valeur fondamentale (dividendes actualisés)
        # ---- étape 4 : hétérogénéité ----
        self.hetero = False
        self.alpha_T = 0.25                                                    # part de la terre dans la production alimentaire
        self.T_land = 1.0                                                      # dotation en terre (indice)
        self.weather_sd = 0.0                                                  # aléa climatique annuel sur la production alimentaire (écart-type)
        self.resource = False; self.R0_stock = 150.0                            # ressource énergétique épuisable : stock initial en années de production
        self.cost_curve = 0.5; self.A_floor_energy = 0.4; self.R_plateau = 0.5                                                  # coût d'extraction : PGF énergie x (stock restant / stock initial)^cost_curve
        self.cohorts = False; self.age_share0 = np.array([0.25, 0.60, 0.15])   # jeunes, actifs, âgés
        self.birth = 0.014; self.aging = 1 / 45.0; self.death_old = 1 / 18.0     # naissances (part des actifs), passage jeune->actif (1/20 an) : voir code
        self.pension = 0.5                                                     # retraite en part du salaire moyen
        self.rural = False; self.rural_share0 = 0.5                            # part rurale de la population active (réservoir de Lewis)
        self.w_rural_rel = 0.5; self.mig_speed = 0.05                          # salaire rural relatif ; vitesse de migration (part de l'écart par an)
        self.mig_cost = 0.2                                                    # écart de salaire requis pour migrer (frais, risque de chômage)
        self.lam_I = 1.0
        self.sat_q = 0.03; self.lam_qbar = 1.0 / 52; self.lam_L_sec = np.array([1.0, 1.0, 1.0, 0.5]); self.lam_div = 0.1   # A1b, C1, C3 (transmission monétaire)
        # ---- étape 3 : actifs ----
        self.assets = False
        self.chi_Z = 0.3; self.chi_E = 0.3           # extrapolation (bulle si > 0,5)
        self.LTV = 0.8; self.margin = 0.5             # quotité hypothécaire, part du portefeuille d'actions finançable à crédit
        self.kappa_pz = 0.02; self.kappa_sup = 0.005; self.kappa_pe = 0.05; self.lam_Z = 0.005; self.psi_fund = 0.5; self.build_cap = 2.0; self.lev_mort = 0.35; self.margin_base = 0.05    # vitesse d'ajustement des prix d'actifs (hebdo)
        self.delta_Z = 0.02; self.zeta_Z = np.array([0.15, 0.25, 0.30])   # dépréciation logements ; part du revenu consacrée au logement par strate
        self.rho_Z = 0.02                             # prime de risque immobilière
        self.nu_build = 0.10                          # élasticité de la construction à p_Z / coût
        self.T_Z = 26                                 # délai de construction (semaines)
        self.sE = np.array([0.0, 0.15, 0.40])          # part de richesse désirée en actions par strate (hors prix)
        self.cV_Z = 0.015; self.cV_E = 0.015           # effet richesse annuel (immobilier, actions)
        self.phi_npl = 0.5                             # part des prêts sous l'eau qui fait défaut par an
        self.deposit_insurance = True; self.gold_cap = None   # garantie des dépôts ; plafond du refinancement (étalon-or) en part de H
        self.run_s1 = 40.0; self.run_s2 = 5.0; self.run_s3 = 2.0
        self.qe_rate = 0.0; self.dres = 0.0            # achats de titres publics par la BC (part du PIB/an) ; écart taux des réserves
        self.cb_include_external_assets = True  # structural reserve coverage includes the signed FX position
        self.s7 = 0.03
        self.phi_Bbank = 0.4; self.kappa_hB = 20.0; self.bank_issue = True; self.recap_thresh = 0.5; self.spread_excl_cb = True; self.psi_qe = 0.5; self.kfor_min = 0.3; self.rho_B = 0.0; self.chi_K = 0.0; self.s9 = 0.015; self.adv_interest = True; self.div_coverage = True   # rho_B : répression financière (détention obligatoire) ; chi_K : contrôle des capitaux (économie fermée ; en monde N pays, world.chiK) ; s9 : rabais de répression
        self.recap_thresh = 0.5   # recapitalisation publique si fonds propres < 50 % de l'exigence
        self.rho_E = 0.02        # prime de risque sur le capital (option B) ; variantes C-G : rho_E 0.03/0.05, G_share 0.095, cV (0,0.06,0.12), tauK 0.15
        self.lam_rstar = 0.02   # apprentissage du taux naturel (mensuel)
        self.rstar_mode = 'legacy'
        self.rstar_anchor = 'ramsey'  # 'deposit_wedge' converts the household net return to a policy-rate intercept
        self.rstar_band = .01
        self.rstar_reversion = 1.0  # /year
        self.tax_rule = False
        self.tax_scale_initial = 1.0
        self.tax_scale_min = 0.0; self.tax_scale_max = 3.0
        self.tax_debt_feedback = .20  # desired annual deficit response to net debt gap
        self.tax_adjust_speed = 1.0  # /year; 0 freezes effective rates in a fiscal counterfactual
        self.lam_r = 1.0
        self.lam_rstar_u = 0.0   # option : apprentissage du taux naturel sur l'écart de chômage (mensuel)
        self.acc = 0.0; self.lam_g = 1.0 / 52   # accélérateur désactivé (instable : cycles de Samuelson-Hicks)
        self.inv_cap = 2.0
        self.P_redenom = 1e6; self.nu9 = 0.12; self.max_weekly_price = 1.19; self.pi_e_sat = 1.0; self.cred_floor = 0.05; self.flex_infl = 5.0; self.i_max = 1.0; self.prime_max = 0.30
        unknown=set(kw)-set(self.__dict__)
        if unknown: raise TypeError("Paramètre(s) inconnu(s): "+", ".join(sorted(unknown)))
        self.__dict__.update(kw)
        if not isinstance(self.audit_corrections,bool) or not isinstance(self.neutral_redenomination,bool) or not isinstance(self.joint_proxy_domain_guard,bool):
            raise ValueError('Invalid audit flags')
        if self.crisis_accounting not in ('legacy_survival','continuous') or self.pricing_cost_mode not in ('legacy','orders_marginal_all','capacity_average','normal_average'):
            raise ValueError('Invalid audit accounting/pricing convention')
        if self.bank_reconciliation_mode not in ('legacy_sum','transaction_replay'):
            raise ValueError('Invalid bank reconciliation mode')
        if self.payout_mode not in ('psi','leverage_target') or not 0<=self.ell_star<=1 or not 0<=self.lam_ell<=2: raise ValueError('Invalid payout rule')
        if self.residual_tolerance not in ('legacy','stock_aware') or not 1<=self.residual_eps_multiple<=4096:
            raise ValueError('Invalid residual tolerance mode')
        if not isinstance(self.depression_detector,bool) or not 0<self.depression_threshold<1 or not isinstance(self.depression_weeks,int) or self.depression_weeks<1:
            raise ValueError('Invalid depression detector')
        if not 0<self.util_normal<=1:
            raise ValueError('Invalid normal utilisation')
        if not isinstance(self.crisis_recovery_weeks,int) or self.crisis_recovery_weeks<1 or not 0<self.crisis_recovery_inflation<.5:
            raise ValueError('Invalid crisis recovery observation window')
        if not isinstance(self.agreement_notice_weeks,int) or self.agreement_notice_weeks<4 or self.agreement_notice_weeks%4 or not 0<self.agreement_max_share<=.2 or not 0<self.agreement_deposit_cap<=1:
            raise ValueError('Invalid wage agreement terms')
        if self.joint_price_search not in ('legacy','feasible_scan') or not isinstance(self.joint_price_search_steps,int) or not 1<=self.joint_price_search_steps<=32:
            raise ValueError('Invalid price search protocol')
        if self.equity_valuation_mode not in ('book_ratio','market_quote') or (self.equity_valuation_mode=='market_quote' and self.portfolio_mode!='joint_equity'):
            raise ValueError('Invalid equity quotation mode')
        if self.mortgage_contract_mode not in ('legacy','finite_linear') or not isinstance(self.mortgage_term_weeks,int) or self.mortgage_term_weeks<4:
            raise ValueError('Invalid mortgage contract terms')
        if not isinstance(self.mortgage_registry,bool) or not isinstance(self.precise_fiscal_deltas,bool):
            raise ValueError('Explicit boolean profile parameters required')
        if not isinstance(self.resolution_notice_weeks,int) or self.resolution_notice_weeks<4 or self.resolution_notice_weeks%4 or not 0<self.resolution_max_haircut<=1 or self.resolution_cooldown_weeks<4:
            raise ValueError('Invalid resolution policy terms')
        if self.pricing_cost_mode!='legacy' and (not self.wsps2 or self.price_mode!='markup'):
            raise ValueError('Marginal order prices require WS-PS markup mode')
        if self.tfp_trend_mode not in ('common_tfp','balanced_sectoral'):
            raise ValueError('Convention de tendance sectorielle invalide')
        if self.wage_indexation_mode not in ('legacy_asymmetric','symmetric') or self.public_productivity_mode not in ('legacy_growth','level') or not 0<=self.public_capital_elasticity<=1:
            raise ValueError('Convention de salaires ou de capital public invalide')
        if self.portfolio_mode not in ('legacy','joint_equity') or not 1<=self.joint_years<=40 or not np.isclose(52*self.joint_years,round(52*self.joint_years)) or not isinstance(self.joint_periods,int) or not 4<=self.joint_periods<=80 or self.joint_fee<=0 or self.joint_risk<0:
            raise ValueError('Convention de portefeuille invalide')
        if self.portfolio_mode=='joint_equity' and self.margin_refinancing:
            raise ValueError('Joint equity requires margin_refinancing=False; existing margin debt is repaid with deposits at activation')
        if self.portfolio_mode=='joint_equity' and (self.sigma!=1 or self.household_mode!='euler' or not self.assets):
            raise ValueError('Joint equity requires log utility, Euler mode and assets')
        if self.joint_terminal not in ('none','balanced_policy') or (self.joint_terminal=='balanced_policy' and self.rho<=0):
            raise ValueError('Invalid joint terminal policy')
        if not 0<=self.joint_dividend_years<=20:
            raise ValueError('Invalid dividend expectation horizon')
        if self.investment_mode not in ('legacy_q','sales_cost') or self.capital_finance not in ('legacy_loan','forecast_wacc') or self.capital_price_forecast not in ('stationary','adaptive') or not 0<self.capital_adjust_speed<=2 or not 0<self.capital_price_years<=20 or not 0<self.joint_anchor_years<=20:
            raise ValueError('Invalid research7 capital/anchor closure')
        if (self.rstar_anchor=='joint_euler' or self.investment_mode=='sales_cost' and self.capital_finance=='forecast_wacc') and self.portfolio_mode!='joint_equity':
            raise ValueError('Research7 joint closure requires the joint household portfolio')
        if self.hh_return_mode not in ('anchored','current') or self.investment_signal not in ('accounting','marginal_product'):
            raise ValueError('Convention d’anticipation ou de rendement du capital invalide')
        for key,value in self.__dict__.items():
            if isinstance(value,(float,int,np.floating)) and not np.isfinite(value):
                raise ValueError("Paramètre non fini: "+key)
        for key in ("alpha","delta","N","omega","share_h","c","cV","tauW","euler_share","a","gamma","beta_les","lam_L_sec","d_scale","age_share0","sE"):
            setattr(self,key,np.asarray(getattr(self,key),dtype=float).copy())
        self.wiu_targets=np.asarray(self.wiu_targets,dtype=float)
        self.wiu_external_targets=np.asarray(self.wiu_external_targets,dtype=float)
        if self.wiu_wealth_basis not in ('liquid','net') or self.wiu_external_targets.shape!=(3,) or not np.all(np.isfinite(self.wiu_external_targets)) or np.any(self.wiu_external_targets<0):
            raise ValueError('Base patrimoniale WIU invalide')
        if not 0<=self.wiu_epsilon<=.08 or not 0<=self.wiu_utility_scale<=1 or not np.isfinite(self.wiu_shift_weeks) or self.wiu_shift_weeks<=0 or self.wiu_targets.shape!=(3,) or not np.all(np.isfinite(self.wiu_targets)) or np.any(self.wiu_targets<=0):
            raise ValueError('Paramètres de richesse dans utilité invalides')
        if self.wiu_epsilon>0 and (self.sigma!=1 or self.household_mode!='euler' or self.hh_return_gap!=0 or self.hh_rate_reversion<=0):
            raise ValueError('WIU : log consommation, mode Euler, écart additionnel nul et réversion positive requis')
        if self.sigma<=0 or self.rho<0 or self.hh_horizon_years<=0 or self.hh_buffer_weeks<0:
            raise ValueError("Préférences/horizon ménages invalides")
        if self.hh_liquid_wealth_ratio is not None and not 0<=self.hh_liquid_wealth_ratio<=10:
            raise ValueError('Cible de richesse liquide invalide')
        if self.rstar_mode not in ('legacy','anchored') or self.rstar_anchor not in ('ramsey','deposit_wedge','joint_euler'):
            raise ValueError('Règle de taux naturel invalide')
        if not 0<=self.rstar_band<=.10 or not 0<self.rstar_reversion<=13:
            raise ValueError('Ancrage de taux naturel invalide')
        if not isinstance(self.tax_rule,bool) or not 0<=self.tax_scale_min<=self.tax_scale_initial<=self.tax_scale_max or not 0<=self.tax_debt_feedback<=2 or not 0<=self.tax_adjust_speed<=13:
            raise ValueError('Règle fiscale invalide')
        if self.tax_rule and self.treasury_rebate_speed>0:
            raise ValueError('Règle fiscale : désactiver le dividende de trésorerie')
        if not isinstance(self.cb_include_external_assets,bool):
            raise ValueError('Couverture extérieure de la BC : booléen requis')
        if self.euler_share.shape!=(3,) or np.any((self.euler_share<0)|(self.euler_share>1)):
            raise ValueError("euler_share doit contenir trois poids entre 0 et 1")
        if not 0<=self.hh_return_gap<=.05 or not 0<self.hh_risk_probability<1 or not 0<self.hh_risk_loss<1:
            raise ValueError("Risque/impatience ménages invalides")
        if self.household_mode=="buffer_stock" and (self.hh_return_gap<=0 or self.hh_rate_reversion<=0):
            raise ValueError("buffer_stock requiert une impatience stricte et un retour de taux positif")
        if self.household_mode not in ("euler","income","buffer_stock"):
            raise ValueError("household_mode doit être euler, income ou buffer_stock")
        if not 0<=self.tauK<1 or np.any((self.tauW<0)|(self.tauW>=1)) or self.tauC<0:
            raise ValueError("Fiscalité invalide")
        if self.eps_goods is not None and self.eps_goods<=1:
            raise ValueError("eps_goods doit être supérieur à 1")
        if not isinstance(self.treasury_redeem_all,bool) or not isinstance(self.fiscal_on_net_debt,bool):
            raise ValueError('Options de trésorerie booléennes requises')
        if not 0<self.gov_cash_ratio<1 or not 0<=self.treasury_rebate_speed<=52 or not 0<=self.treasury_rebate_cap<=1:
            raise ValueError('Paramètres de trésorerie invalides')
        if self.treasury_drawdown_cap is not None and not 0<=self.treasury_drawdown_cap<=1:
            raise ValueError('Plafond de prélèvement de trésorerie invalide')
        if self.price_basis not in ("average","marginal") or self.price_mode not in ("markup","tat"):
            raise ValueError("Règle de prix inconnue")
        if not 1<=self.T_Z<200 or int(self.T_Z)!=self.T_Z or not 0<self.util_lo<self.util_hi<=1:
            raise ValueError("Délai de construction/fenêtre d'utilisation invalide")
        self.T_Z=int(self.T_Z)
        if not isinstance(self.equipment_supply_response,bool):
            raise ValueError("equipment_supply_response doit être booléen")
        if self.equipment_price_mode not in ('average_floor','orders_marginal') or self.equipment_price_mode=='orders_marginal' and not self.equipment_supply_response:
            raise ValueError('Invalid equipment price convention')
        if self.equipment_supply_response and (not self.wsps2 or self.price_basis!="average" or self.price_mode!="markup"):
            raise ValueError("Réponse d’offre : WS-PS, coût moyen majoré requis")
        if not isinstance(self.eight_corrections, bool) or not np.isfinite(self.rate_speed_limit) or self.rate_speed_limit<=0:
            raise ValueError("Invalid eight-point profile or rate speed limit")
        if self.public_growth is not None:
            raise ValueError("public_growth est retiré : le potentiel est calculé à partir des facteurs")
        if self.build_cap<0 or self.delta_Z<=0 or self.nu_build<0:
            raise ValueError("Paramètres de construction invalides")
        if self.hh_rate_reversion<0 or not 0<self.hh_income_speed<=1 or self.hh_growth_min>self.hh_growth_max:
            raise ValueError("Anticipations ménages invalides")
        if not 0<self.mortgage_service_share<=1 or self.mortgage_amortization<0:
            raise ValueError("Service hypothécaire invalide")
        if self.nsec!=4 or np.shape(self.a)!=(4,4) or np.any(self.a<0) or max(abs(np.linalg.eigvals(self.a)))>=1:
            raise ValueError("Quatre secteurs et matrice Leontief productive requis")
        for key,size in (("alpha",4),("delta",4),("N",3),("omega",3),("share_h",3),("c",3),("cV",3),("tauW",3)):
            v=getattr(self,key)
            if v.shape!=(size,) or not np.all(np.isfinite(v)) or np.any(v<0):
                raise ValueError("Vecteur invalide: "+key)
        if np.any((self.alpha<=0)|(self.alpha>=1)) or np.any(self.N<=0):
            raise ValueError("Production/population invalide")
        if not np.isclose(self.omega.sum(),1) or not np.isclose(self.share_h.sum(),1) or np.any(self.beta_les<=0) or not np.allclose(self.beta_les.sum(axis=1),1):
            raise ValueError("Parts de répartition non normalisées")
        for k, (lo, hi) in self.BOUNDS.items():   # bornes de jeu : au-delà, le prototype enchaîne des cycles d'actifs de grande amplitude
            if k in kw and not (lo <= kw[k] <= hi): raise ValueError(f"{k}={kw[k]} hors bornes [{lo}, {hi}]")


class Economy:
    def __init__(self, p: Params, seed=0, shock_sd=0.0):
        import copy
        self.p = p = copy.deepcopy(p); self.rng = np.random.default_rng(seed); self.shock_sd = shock_sd
        n = p.nsec
        self.t = 0
        # --- calibration d'un état initial proche du stationnaire ---
        Nact = p.participation * p.N.sum()*(1-p.rural_share0 if p.rural else 1); LG = p.LG_share * Nact
        emp = Nact * (1 - p.u_n) - LG
        self.p_ = np.ones(n)
        # calibration Leontief : x = (I-A)^{-1} d, avec d cohérent avec la consommation et l'investissement
        Ainv = np.linalg.inv(np.eye(n) - p.a)
        va_coef = 1 - p.a.sum(axis=0)
        g_initial=p.g0/(1-float(np.mean(p.alpha)))
        mu_initial=np.full(n,1/((p.eps_goods if p.eps_goods is not None else 7.)-1))
        mr_unit=1/(1+mu_initial)-p.a.sum(axis=0)
        real_loan_initial=(1+p.rho+p.sigma*p.g0+p.pi_star+p.mL)/(1+p.pi_star)-1
        q_initial=1+g_initial/p.iota
        ky_initial=p.alpha*mr_unit/(q_initial*(real_loan_initial+p.rho_E+p.delta)) if p.price_basis=="marginal" else np.full(n,3.)
        x = np.array([250.0, 200.0, 500.0, 250.0])
        Gam = (p.N[:, None] * p.gamma).sum(axis=0) / WEEKS           # subsistance agrégée hebdo
        beta_bar = (p.N[:, None] * p.beta_les).sum(axis=0) / p.N.sum()
        for _ in range(200):
            VA = x * va_coef; VAtot = VA.sum() + LG * 1.0
            C = p.C_cal * VAtot
            cons = Gam + beta_bar * max(C - Gam.sum(), 0) / (1 + p.tauC)
            K = ky_initial * x * WEEKS
            Iw = ((p.delta + (g_initial if p.price_basis=="marginal" else 0.)) * K).sum() / WEEKS
            d = np.array([cons[0], cons[1], cons[2] + p.G_share * VAtot, Iw + p.Ginv_share * VAtot])
            d = d * p.d_scale   # v2.0 (session 5) : facteur d'équilibre du marché des biens à t=0, résolu par point fixe (Economy.solve_init) pour que D = S dans chaque secteur sans tâtonnement
            x = Ainv @ d
        VA = x * va_coef
        eps = p.eps_goods if p.eps_goods is not None else 7.
        mu_initial = np.full(n,1/(eps-1))
        effective_va = x*(1/(1+mu_initial)-p.a.sum(axis=0)) if p.price_basis=="marginal" else VA
        Ldem = (1 - p.alpha) * effective_va / (1 + p.tauS)          # à W = 1
        Wcal = Ldem.sum() / emp                           # salaire qui emploie emp
        self.W = np.ones(n) * Wcal
        self.W_public_base = float(Wcal)
        self._cons_price_base = 1 + p.tauC
        self.L = Ldem / Wcal
        Ycol = x
        self.K = ky_initial * Ycol * WEEKS
        self.H = 1.0
        self.A = Ycol / (self.K ** p.alpha * self.L ** (1 - p.alpha))
        self.A0 = self.A.copy()
        rstar0 = p.rho + p.sigma * p.g0
        cuY = self.W * self.L * (1 + p.tauS) + (p.a * Ycol[None, :]).sum(axis=0) + p.delta / WEEKS * self.K
        self.markup = (rstar0 + p.rho_E) / WEEKS * self.K / cuY     # marge normale : rendement net requis (taux sûr + prime de risque) sur le coût unitaire
        if p.wsps2:   # v2.0 : à l'état initial (prix 1), la marge normale est celle que la part du capital alpha implique : mu_j = (1 - cu_j)/cu_j ; l'ancienne marge (rendement requis sur K) était inférieure de 2 à 14 points, et la première correction de prix était un choc déflationniste. eps implicite = 1 + 1/mu (6,0 ; 4,1 ; 6,6 ; 6,9)
            cu0 = cuY / Ycol
            self.markup = (1.0 - cu0) / cu0
            self.mu_n_sec = self.markup.copy()
        if p.wsps2 and p.price_basis=="marginal":
            self.markup = mu_initial.copy(); self.mu_n_sec = mu_initial.copy()
        self.Sinv = p.s_star * Ycol
        self.Xinv = 4.0 * p.a * Ycol[None, :]
        self.Qbar = Ycol.copy()
        self.Pi_marginal_bar = p.alpha * effective_va
        self.Pi_brut_bar = VA-(1-p.alpha)*effective_va              # part du capital
        self.div_last = 0.5 * self.Pi_brut_bar; self.div_bank_last = 0.0
        self._bank_shares=p.omega.copy(); self._bank_dividends_last=np.zeros(3)
        Yw = VA.sum() + LG * Wcal                    # PIB nominal hebdo (VA privée + salaires publics)
        self.KG = 0.5 * Yw * WEEKS                   # capital public initial : 50 % du PIB annuel (unités réelles, prix 1)
        self.KG_ratio0 = 0.5
        self._Ynom_w = Yw
        self.pi_e = p.pi_star; self.cred = 0.8
        self.u_n = p.u_n
        self.i_cb = p.rho + p.sigma * p.g0 + p.pi_star
        self.rstar_est = p.rho + p.sigma * p.g0
        self.tax_scale = p.tax_scale_initial
        self.i_app = self.i_cb + p.s0
        self.i_B = self.i_app
        self.P_hist = []
        self.pi = p.pi_star
        self.zombie = np.zeros(n, dtype=int)
        self.faillites = 0
        self.M_hist = 0; self.redenom = 0; self.rhoG = 1.0; self.recap = 0.0; self.last_recap = -10**6
        self.s_surv = 0.0                                   # part des transactions en unité stable (survie)
        self.collapsed = False; self.cap_weeks = 0; self.reform_times = []; self.collapse_t = None; self.collapses = 0
        self.R_stock = p.R0_stock * WEEKS * float(self.Qbar[1]) if p.resource else 1.0; self.R_stock0 = self.R_stock; self.A_energy0 = None
        self.age = p.age_share0.copy() * p.N.sum()          # effectifs par cohorte
        self.rural_pop = (p.rural_share0 * p.participation * p.N.sum()) if p.rural else 0.0   # réservoir rural (hors marché du travail urbain, autoconsommation)
        self.rural_pop0 = self.rural_pop
        self.weather = 1.0
        # --- grand livre ---
        Mtot = Yw * WEEKS / p.V0   # V0 : vitesse telle que P* = 1 au départ
        self.led = Ledger()
        hshare = np.array([0.35, 0.35, 0.30])
        for h in range(3): self.led.open(f"H{h}", 0.70 * Mtot * hshare[h])
        for j in range(n): self.led.open(f"F{j}", 0.26 * Mtot * Ycol[j] / Ycol.sum())
        self.led.open("G", 0.04 * Mtot)
        self.led.open("FX", 0.0)
        self.world = None; self.R_fx = 0.0; self.e = 1.0; self.B_foreign = 0.0
        # actifs : logements (stock Z par strate, prix p_Z), actions (valeur de marché des entreprises), crédits hypothécaires
        Yw0 = self._Ynom_w
        self.Z = 1.5 * Yw0 * WEEKS / 1.0 * np.array([0.35, 0.35, 0.30])   # stock de logements : 1,5 PIB en valeur, prix initial 1
        self.housing_q0 = 1.0
        self.pZ = 1.0; self.pZ_hist = []; self.gZ_e = p.g0; self.gE_e = p.g0; self.pipeline = np.zeros(200)   # anticipations de plus-value réelle
        self.pipeline_h=np.zeros((200,3))
        self.pipeline_h[:p.T_Z]=.02/WEEKS*self.Z[None,:]
        self.pipeline[:p.T_Z] = 0.02 / WEEKS * self.Z.sum()   # constructions en cours = remplacement
        self.LZ = 0.5 * Yw0 * WEEKS * np.array([0.4, 0.4, 0.2])            # dette hypothécaire : 50 % du PIB
        self.Loans_Z_total0 = self.LZ.sum()
        self.pE = 1.0; self.pE_hist = []; self.equity_value_hist = []; self.NPL_Z = 0.0; self.npl_rate = 0.0; self.LE = 0.0
        self.cbar_cb = self.i_app                                             # coupon moyen du portefeuille de la BC (figé à l'achat)
        self.cash_h=np.zeros(3)
        self.cash_out = 0.0; self.runs = 0; self.bank_failed = False; self.qe_rate = p.qe_rate
        self.Loans = 0.20 * self.K
        self.E_bank = 0.12 * self.Loans.sum()
        if p.assets: self.E_bank += 0.12 * 0.5 * self.led.total() * 0   # (les hypothèques sont ajoutées au bilan ci-dessous)
        Bt = 0.6 * Yw * WEEKS
        self.Bh = Bt * 0.60 * np.array([0.1, 0.3, 0.6])
        self.B_bank = Bt * 0.25; self.B_cb = Bt * 0.15; self.AG = 0.0
        self.B = self.Bh.sum() + self.B_bank + self.B_cb
        self.L_cb = 0.0
        if p.assets:
            self.LE = p.margin * p.margin_base * ((self.K * self.p_[3]).sum() - self.Loans.sum() + sum(self.led.dep[f'F{j}'] for j in range(n)))
            self.E_bank += 0.09 * (self.LZ.sum() + self.LE)
            for h, s_ in enumerate((0.35, 0.35, 0.30)): self.led.dep[f'H{h}'] += (self.LZ.sum() + self.LE) * s_   # les crédits passés ont créé des dépôts
        self.Res = self.led.total() + self.E_bank - self.Loans.sum() - self.B_bank - ((self.LZ.sum() + self.LE) if p.assets else 0.0)
        if self.Res < 0: self.L_cb = -self.Res; self.Res = 0.0
        if p.assets and self.Res > self.B_cb:   # la BC détient des titres publics en contrepartie des réserves (portefeuille de politique monétaire)
            extra = self.Res - self.B_cb; take_bk = min(extra, self.B_bank); self.B_bank -= take_bk; take_h = extra - take_bk
            self.Bh -= take_h * self.Bh / self.Bh.sum(); self.B_cb += extra
            self.Res = self.led.total() + self.L_cb + self.E_bank - self.Loans.sum() - self.B_bank - self.LZ.sum() - self.LE
        self.E_cb = self.B_cb + self.AG + self.L_cb - self.Res
        self.E_cb0 = self.E_cb          # fonds propres statutaires (niveau initial)
        self.AG_free = 0.0              # v1.6 : part des avances issue d'une conversion monétaire (émission de la nouvelle monnaie) : sans intérêt, réserves adossées non rémunérées
        self.M_G_prev = self.led.dep["G"]
        self.accounting = {}
        self.events = []
        self.flow_history = []
        self.consumption_history = []
        self.pol_override = None  # fonction t -> taux (tests)
        self.shock_i = 0.0
        self.monetize = 0.0       # avances /an en part du PIB (tests)
        self.transfer_shock = 0.0  # transferts supplémentaires en part du PIB
        self.hist_K = []
        self.hist = {k: [] for k in ["Y", "P", "pi", "u", "i_cb", "i_B", "i_app", "b", "cred", "pi_e", "M", "K", "q", "SoL", "deficit", "faillites", "check", "un", "Ebank", "def_pct", "Mhist", "rhoG", "pZ", "pE", "npl", "LZ", "Bcb", "Ecb", "runs", "rural", "age_old", "Rstock", "s_surv", "fisc"]}

        if p.equity_valuation_mode=='market_quote':self._equity_quote=float(self.pE*self.equity_book())

    # ------------------------------------------------------------------
    def money_supply(self):
        return sum(v for k, v in self.led.dep.items() if k not in ("G", "FX"))

    def step(self):
        if self.p.audit_corrections and getattr(self,'_step_failed',None):
            raise RuntimeError('Interrupted week: restore a completed checkpoint before continuing')
        try:return self._step_unchecked()
        except Exception as exc:
            if self.p.audit_corrections:self._step_failed=dict(week=self.t,type=type(exc).__name__,message=str(exc))
            raise

    def _step_unchecked(self):
        if self.world is not None:
            raise NotImplementedError("Pays relié : avancer tous les pays avec World.step()")
        if self.collapsed and self.p.crisis_accounting!='continuous':
            return self.survival_step()
        gen=self._step_normal()
        try:next(gen)
        except StopIteration:return
        raise RuntimeError("Barrière internationale sans monde")

    def _step_normal(self):
        if eight.enabled(self): eight.enable(self)
        if self.p.audit_corrections:
            from . import audit_profile as audit
            if not hasattr(self,'audit_profile'):audit.enable(self)
        p = self.p; n = p.nsec; t = self.t
        month = (t % DECISION_WEEKS == 0)
        if month: update_taxes(self)
        tauW_eff,tauK_eff=income_tax_rates(self)
        self._tauW_eff=tauW_eff; self._tauK_eff=tauK_eff
        led = self.led
        led.shortfalls=[]
        led.entries=[]
        self._recap_tick=0.
        self._bank_public_dividend=0.
        B_start=self.B; AG_start=self.AG
        fiscal_opening=np.r_[self.Bh.copy(),self.B_bank,self.B_cb,self.AG,self.led.dep["G"]]
        # ---------- 0. Production potentielle / prix du capital ----------
        pK = self.world.composite_price(self)[3] if self.world is not None else self.p_[3]
        K_start = self.K.copy()
        X_start = self.Xinv.copy()
        deposits_start = self.led.total()
        self._gov_cash_start = self.led.dep["G"]
        self._bank_equity_start = self.E_bank
        begin_reconciliation(self)
        if hasattr(self,'resolution_actions'):
            from .workplan import execute_resolutions
            execute_resolutions(self)
        A_eff = self.A.copy()
        if p.hetero:
            A_eff[0] *= self.weather * p.T_land ** p.alpha_T                     # terre et climat dans l'alimentation
            if p.resource:
                if self.A_energy0 is None: self.A_energy0 = self.A[1]
                ratio = max(self.R_stock / self.R_stock0, 0.0)
                A_eff[1] = self.A[1] * max(min(ratio / p.R_plateau, 1.0) ** p.cost_curve, p.A_floor_energy)   # plateau tant que la moitié du stock subsiste, puis coût d'extraction croissant ; plancher = substituts
        self._A_eff = A_eff
        Ycap = A_eff * self.K ** p.alpha * (self.H * self.L) ** (1 - p.alpha)
        # ---------- 1. Plans ----------
        vfac = np.exp(p.a_cagan * min(max(self.pi_e, 0), p.pi_e_sat))   # la monnaie tourne plus vite en forte inflation : les contraintes de caisse se relâchent
        if p.survival:   # économie de survie : au-delà de 50 % d'inflation anticipée, une part croissante des transactions passe en unité stable (troc, devise, indexation)
            s_des = float(np.clip(p.s_surv_slope * (self.pi_e - 0.5), 0, 0.8))
            self.s_surv = max(s_des, 0.995 * self.s_surv)
            vfac = vfac / max(1 - self.s_surv, 0.5)
        Yhat = self.Qbar * (1 + p.g0 / WEEKS) + (p.lam_inv_2 if p.wsps2 else p.lam_inv) * (p.s_star * self.Qbar - self.Sinv)   # v2.0 : la production suit les ventes, les stocks absorbent les surprises (correction lente)
        Yhat = np.maximum(Yhat, 0.05 * Ycap)
        # commandes d'intrants
        Xdem = p.a * Yhat[None, :] + 0.2 * np.maximum(0, 2 * p.a * Yhat[None, :] - self.Xinv)
        cashX = np.array([led.dep[f'F{j}'] for j in range(n)]) - self.W * self.L * (1 + p.tauS)
        costX = (Xdem * self.p_[:, None]).sum(axis=0)
        Xdem = Xdem * np.minimum(1.0, vfac * np.maximum(cashX, 0) / np.maximum(costX, 1e-9))[None, :]
        # demande de travail
        L_tech = (Yhat / (self._A_eff * self.K ** p.alpha * self.H ** (1 - p.alpha))) ** (1 / (1 - p.alpha))
        if p.L_prof_va or p.wsps2:   # chantier salaires-prix (v1.6) : demande de travail au produit marginal — W(1+tauS) L = (1-alpha) x VALEUR AJOUTEE (Cobb-Douglas sur la VA). La forme antérieure rapportait (1-alpha) au CHIFFRE D'AFFAIRES, intrants compris : l'entreprise acceptait une masse salariale allant jusqu'à (1-alpha)/(1-part des intrants) de la VA, soit à peu près toute la VA — l'emploi n'était borné que par la condition de non-perte, pas par le profit du capital
            revenue_price=self.p_/(1+self.markup) if p.price_basis=="marginal" else self.p_
            p_va = np.maximum(revenue_price - (p.a * self.p_[:, None]).sum(axis=0), 1e-9)   # prix de la valeur ajoutée unitaire
            # emploi qui égalise le produit marginal du travail et le salaire chargé, à la production EFFECTIVE (pas planifiée) : L* = [(1-alpha) p_va A K^alpha H^(1-alpha) / (W(1+tauS))]^(1/alpha)
            L_prof = ((1 - p.alpha) * p_va * self._A_eff * self.K ** p.alpha * self.H ** (1 - p.alpha) / (self.W * (1 + p.tauS))) ** (1 / p.alpha)
        else:
            L_prof = (1 - p.alpha) * self.p_ * Yhat / (self.W * (1 + p.tauS))
        Lstar = np.minimum(L_tech, L_prof); self._dbgL = (L_tech.copy(), L_prof.copy(), Yhat.copy()); Lt_last, Lp_last = L_tech, L_prof
        Lstar = np.where(self.zombie > 0, self.L, Lstar)
        # contrainte de liquidité : la masse salariale ne peut excéder la trésorerie disponible plus les ventes attendues
        cash0 = np.array([led.dep[f'F{j}'] for j in range(n)])
        L_cash = vfac * np.maximum(cash0 + 0.5 * self.p_ * self.Qbar, 0) / (self.W * (1 + p.tauS))
        Lstar = np.minimum(Lstar, L_cash)
        Nact = self.active_pop(); LG = p.LG_share * Nact
        self.excess_ld = max(Lstar.sum() / max((Nact - LG) * (1 - self.u_n), 1e-9) - 1, 0)   # excès de demande de travail sur l'offre disponible au plein emploi
        Lstar = np.minimum(Lstar, (Nact - LG) * 0.98 * Lstar / max(Lstar.sum(), 1e-9)) if Lstar.sum() > (Nact - LG) * 0.98 else Lstar
        self.L = self.L + (p.lam_L_2 if p.wsps2 else p.lam_L) * p.lam_L_sec * (Lstar - self.L)   # v2.0 : rétention de main-d'oeuvre (Oi 1962) : l'emploi suit la production avec un coût d'ajustement
        u = max(0.0, 1 - (self.L.sum() + LG) / Nact)
        if p.hetero: self.hetero_block(u, Y_fn=None)
        # ---------- 2. Production ----------
        Ycap = self._A_eff * self.K ** p.alpha * (self.H * self.L) ** (1 - p.alpha)
        L_full = np.minimum(np.maximum(self.L, L_prof), Nact - LG)                                 # bornée par la main-d'œuvre disponible
        Ycap_full = self._A_eff * self.K ** p.alpha * (self.H * L_full) ** (1 - p.alpha)   # capacité si l'emploi rentable était atteint
        need = p.a * Ycap[None, :]
        avail = self.Xinv
        ratio = np.where(need > 1e-12, avail / np.maximum(need, 1e-12), 10.0)
        thr = np.clip(ratio.min(axis=0), 0, 1)
        Y = Ycap * thr
        if p.hetero and p.resource:
            # Le plancher énergétique représente des substituts non épuisables.
            substitute=p.A_floor_energy*self.A[1]*self.K[1]**p.alpha[1]*(self.H*self.L[1])**(1-p.alpha[1])*thr[1]
            extraction=min(max(Y[1]-substitute,0.),self.R_stock)
            Y[1]=min(Y[1],substitute+extraction)
            self.R_stock-=extraction
        used = p.a * Y[None, :]
        self.Xinv = self.Xinv - used
        # ---------- 3. Ménages : revenus du tick précédent -> budget ----------
        Nact = self.active_pop()
        # répartition des travailleurs : strates par qualification (B 70% des emplois, M 25%, H 5%)
        share_h = p.share_h
        wage_bill = (self.W * self.L).sum()
        Wbar = wage_bill / max(self.L.sum(), 1e-9)
        # emploi public payé au salaire moyen
        pub_wages = LG * Wbar
        public_wages_full = pub_wages
        labor_income = (wage_bill + pub_wages) * share_h
        unemployed = Nact - self.L.sum() - LG
        Tr = np.zeros(3); Tr[0] = p.repl * Wbar * max(unemployed, 0)
        b_now = self.B / max(self.Y_nom_prev(), 1e-9)   # Y_nom_prev est déjà annuel
        if p.fiscal_on_net_debt:
            b_now=(self.B+self.AG-max(led.dep['G']-p.gov_cash_ratio*self.Y_nom_prev(),0.))/max(self.Y_nom_prev(),1e-9)
        fisc = float(np.clip(1 + p.phi_b * (p.b_target - b_now), 0.6, 1.6)) if p.fiscal_rule else 1.0   # règle budgétaire : dépenses (achats, investissement, minima) corrigées de l'écart à la cible de dette
        if p.wsps2 and p.phi_uf > 0:   # v2.0 (voie budgétaire) : stabilisateur contracyclique — dépenses relevées de phi_uf par point de chômage au-dessus de u_n0 (Blanchard-Perotti 2002 ; stabilisateurs automatiques : Fatás-Mihov 2001), combiné à la règle de dette si elle est active
            u_gap = float(np.mean(self.hist["u"][-13:])) - p.u_n if self.hist.get("u") else 0.0
            fisc = float(np.clip(fisc + p.phi_uf * u_gap, 0.6, 1.6))
        self._fisc = fisc
        Ynom_prev = self.Y_nom_prev()
        # Potentiel aux facteurs présents, même composition sectorielle, emploi structurel.
        # Une tendance exponentielle autonome ne peut représenter une capacité productive.
        Ynom_ref = self.potential_output_nominal(A_eff, Nact, LG, Wbar) if p.wsps2 and p.G_on_potential else Ynom_prev
        self._Ypotential_nominal = Ynom_ref
        planned = (p.repl * Wbar * max(unemployed, 0) + (p.pension * Wbar * self.age[2] + 0.5 * p.minima * Wbar * self.age[0] if p.cohorts else p.minima * Wbar * (p.N.sum() - Nact)) + pub_wages + self.transfer_shock * self.Y_nom_prev() / WEEKS + fisc * (p.G_share + p.Ginv_share) * Ynom_ref / WEEKS)
        cashG = led.dep['G'] + getattr(self, '_tax_prev', planned) + (self.monetize * self.Y_nom_prev() / WEEKS)
        rhoG = float(np.clip(min(self.rhoG, max(cashG, 0) / max(planned, 1e-9)), 0.0, 1.0))   # taux d'exécution : trésorerie disponible / dépenses prévues
        self.rhoG_eff = rhoG
        if p.cohorts:
            Tr += self._fisc * 0 + p.pension * Wbar * self.age[2] * np.array([0.6, 0.3, 0.1]) + p.minima * Wbar * self.age[0] * 0.5 * np.array([0.7, 0.2, 0.1])   # retraites aux âgés, minima aux jeunes
        else:
            Tr += self._fisc * p.minima * Wbar * (p.N.sum() - Nact) * np.array([0.6, 0.3, 0.1])   # retraites / minima aux inactifs (corrigés par la règle budgétaire)
        if p.rural and self.rural_pop > 0:
            Tr += p.w_rural_rel * Wbar * self.rural_pop * np.array([1.0, 0, 0]) * 0.0   # (le revenu rural est produit dans le secteur alimentaire, voir hetero_block)
        Tr += self.transfer_shock * self.Y_nom_prev() / WEEKS * np.array([1.0, 0, 0])
        Tr = np.maximum(Tr * rhoG, 0.); pub_wages *= rhoG
        planned_wages = self.W * self.L
        wage_paid = np.array([led.transfer(f"F{j}","H0",planned_wages[j]) for j in range(n)])
        paid_pub = led.transfer("G","H0",pub_wages)
        gross_labor = wage_paid.sum() + paid_pub
        led.transfer("H0","H1",gross_labor*share_h[1])
        led.transfer("H0","H2",gross_labor*share_h[2])
        labor_income = gross_labor * share_h
        pub_wages = paid_pub
        Tr = np.array([led.transfer("G",f"H{h}",Tr[h]) for h in range(3)])
        int_dep = (wk(max(self.i_cb-p.mD,0)) if self.E_bank>0 else 0.) * np.array([led.dep[f"H{h}"] for h in range(3)])
        for h in range(3): led.dep[f"H{h}"] += int_dep[h]
        change_book(self,-int_dep.sum(),'deposit_interest_expense')
        due = wk(self.i_app)*self.Bh
        int_bond=np.array([led.transfer("G",f"H{h}",due[h]) for h in range(3)])
        self.Bh += due-int_bond
        equity_div=getattr(self,"div_last",np.zeros(n)).sum()*self.equity_ownership()
        div = equity_div + getattr(self,"_bank_dividends_last",getattr(self,"div_bank_last",0.)*p.omega)
        gross_income = labor_income + div + int_dep + int_bond + Tr
        tax_base = float((p.tauW*labor_income).sum()+p.tauK*(div+int_dep+int_bond).sum())
        tax_due = tauW_eff*labor_income + tauK_eff*(div+int_dep+int_bond)
        taxes_h=np.array([led.transfer(f"H{h}","G",tax_due[h]) for h in range(3)])
        self._household_taxes_paid=float(taxes_h.sum())
        self._hh_debt_interest=np.zeros(3); self._hh_debt_amort=np.zeros(3)
        if p.assets: self.pay_household_debt()
        self._joint_margin_repayment=0.
        if p.portfolio_mode=='joint_equity' and self.LE>0:
            # Free pledged equity by paying its debt, never by cancellation.
            amounts=self.LE*p.omega
            if any(amounts[h]>led.dep[f'H{h}'] for h in range(3)):
                raise ValueError('Insufficient deposits to release pledged equity for joint trading')
            for h in range(3):led.dep[f'H{h}']-=amounts[h]
            self._joint_margin_repayment=float(self.LE);self.LE=0.
            self.events.append(dict(t=t,event='joint_margin_repayment',amounts=amounts.tolist()))
        Yd = gross_income - taxes_h - self._hh_debt_interest
        if p.audit_corrections:
            Yd += audit.agreement_payment(self)
        self._tax_prev = taxes_h.sum()
        # Fiscal dividend decided from opening cash, financed by an actual transfer.
        # Debt repayments at the previous close have priority in the combined mode.
        dividend=np.zeros(3)
        if p.treasury_rebate_speed>0:
            # Opening cash prevents rebating this week's newly collected taxes.
            # The target reserve remains available for regular payments later on.
            planned_dividend=rebate_plan(self,self.Y_nom_prev(),cash_available=self._gov_cash_start)
            dividend=np.array([led.transfer('G',f'H{h}',planned_dividend[h]) for h in range(3)])
            Tr+=dividend;gross_income+=dividend;Yd+=dividend
        self._treasury_dividend=float(dividend.sum())
        self._wage_shortfall = float((planned_wages-wage_paid).sum())
        self._public_wages = float(pub_wages)
        self._labor_paid = labor_income.copy()
        # Prix TTC ; composite supernuméraire Stone-Geary par strate.
        sh = self.world.home_share(self) if self.world is not None else np.ones(n)
        pimp = self.world.import_price(self) if self.world is not None else self.p_.copy()
        pcomp = self.world.composite_price(self) if self.world is not None else self.p_.copy()
        pc = pcomp[:3]*(1+p.tauC)
        V=np.array([led.dep[f"H{h}"] for h in range(3)])+self.Bh
        if p.wealth_net_debt: V=V-p.omega*self.LE
        self._VE = ((self.equity_market_value()*self.equity_ownership() if p.equity_valuation_mode=='market_quote' else self.pE*self.equity_ownership()*self.equity_book()) if p.assets else np.zeros(3))
        self._VZ = self.pZ*self.Z-self.LZ if p.assets else np.zeros(3)
        Ydw=Yd
        p_ch=np.exp(np.sum(p.beta_les*np.log(pc[None,:]/self._cons_price_base),axis=1))
        noninterest=np.maximum(Yd-(1-tauK_eff)*int_dep-self._hh_debt_amort,0.)
        now_real=noninterest/p_ch
        self.Yperm_real=getattr(self,"Yperm_real",now_real.copy())+p.hh_income_speed*(now_real-getattr(self,"Yperm_real",now_real))
        self.Yperm=self.Yperm_real*p_ch
        other_now=np.maximum(noninterest-(1-tauK_eff)*equity_div,0.)
        self._other_perm_real=getattr(self,'_other_perm_real',other_now/p_ch)+p.hh_income_speed*(other_now/p_ch-getattr(self,'_other_perm_real',other_now/p_ch))
        E_income=p.c*Ydw+p.cV*V/WEEKS
        if p.assets: E_income+=(p.cV_Z*self._VZ+p.cV_E*self._VE)/WEEKS
        cash=np.maximum(np.array([led.dep[f"H{h}"] for h in range(3)]),0.)
        E_income=np.clip(E_income,0,p.cash_consumption_fraction*cash)
        E_opt=np.zeros(3); hh_choices=[]
        growth=p.hh_income_growth if p.hh_income_growth is not None else getattr(self,"g_prod",p.g0/(1-float(np.mean(p.alpha))))
        growth=float(np.clip(growth,p.hh_growth_min,p.hh_growth_max))
        for h in range(3):
            subs=float(np.sum(pc*p.gamma[h])*p.N[h]/WEEKS)/p_ch[h]
            iD=max(self.i_cb-p.mD,0.) if self.E_bank>0 else 0.
            if p.portfolio_mode=='joint_equity':
                # The joint problem below replaces the liquid-only optimizer.
                expense=0.;choice=ConsumptionChoice(0.,0,0.,True)
                r_net=(1+(1-tauK_eff)*wk(iD))**WEEKS/(1+self.pi_e)-1
            elif p.wiu_epsilon>0 and p.euler_share[h]>0:
                if not hasattr(self,'_wiu_warm'):self._wiu_warm=[None]*3
                expense,choice,r_net,warm,diag=plan_wealth(cash[h]/p_ch[h],self.Yperm_real[h],subs,iD,tauK_eff,self.pi_e,
                    p.sigma,p.rho,growth,p.hh_horizon_years,wealth_buffer_weeks(p),p.hh_rate_reversion,
                    p.wiu_epsilon,p.wiu_targets[h],p.wiu_shift_weeks,self._wiu_warm[h],utility_scale=p.wiu_utility_scale,return_mode=p.hh_return_mode,
                    external_wealth=household_balance_sheets(self)['external'][h]/p_ch[h] if p.wiu_wealth_basis=='net' else 0.,
                    external_target_years=p.wiu_external_targets[h] if p.wiu_wealth_basis=='net' else 0.)
                self._wiu_warm[h]=warm
                if not hasattr(self,'_wiu_diag'):self._wiu_diag=[{} for _ in range(3)]
                self._wiu_diag[h]=diag
            elif p.household_mode=="buffer_stock":
                expense,choice,r_net=plan_buffer_stock(cash[h]/p_ch[h],self.Yperm_real[h],subs,iD,tauK_eff,self.pi_e,
                    p.sigma,p.rho,growth,p.hh_return_gap,p.hh_risk_probability,p.hh_risk_loss,p.hh_rate_reversion)
            else:
                expense,choice,r_net=plan_household(cash[h]/p_ch[h],self.Yperm_real[h],subs,iD,tauK_eff,self.pi_e,
                    p.sigma,p.rho,growth,p.hh_horizon_years,wealth_buffer_weeks(p),p.hh_rate_reversion,p.hh_return_gap)
            E_opt[h]=expense*p_ch[h]
            hh_choices.append(dict(binding=choice.binding_period,feasible=choice.feasible,r_net=r_net,
                                   planned_surplus=choice.surplus,pC=p_ch[h],growth=growth))
        mix=p.euler_share if p.household_mode!="income" else np.zeros(3)
        if p.portfolio_mode=='joint_equity':
            if p.wiu_epsilon<=0 or p.household_mode!='euler' or not p.assets:
                raise ValueError('Joint equity requires assets and positive WIU in Euler mode')
            try:from .joint_portfolio import decision_and_settlement
            except ImportError:from joint_portfolio import decision_and_settlement
            subs_nom=np.array([float(np.sum(pc*p.gamma[h])*p.N[h]/WEEKS) for h in range(3)])
            E_opt=decision_and_settlement(self,cash,self._other_perm_real*p_ch,subs_nom,float(np.exp(np.mean(np.log(p_ch)))),growth,tauK_eff)
            cash=np.array([led.dep[f'H{h}'] for h in range(3)])
            for h in range(3):
                hh_choices[h].update(binding=self._joint_diag['binding'][h],planned_surplus=max((E_opt[h]-subs_nom[h])/p_ch[h],0.))
            self._wiu_diag=[{} for _ in range(3)]
        E=np.minimum((1-mix)*E_income+mix*E_opt,cash)
        self._E_plan=E.copy()
        self._hh_choices=hh_choices
        self._diag_E=dict(Yd=Ydw.copy(),dep=cash.copy(),Yperm=self.Yperm.copy(),Eplan=E.copy(),
                          cY=p.c*Ydw,cV=p.cV*V/WEEKS,E_income=E_income,E_euler=E_opt,
                          euler_share=mix.copy(),r_net=np.array([h["r_net"] for h in hh_choices]))
        xh = np.zeros((3, 3)); Eh = np.zeros(3)
        for h in range(3):
            subs = (pc * p.gamma[h]).sum() * p.N[h] / WEEKS
            if E[h] >= subs:
                xh[h] = p.gamma[h] * p.N[h] / WEEKS + p.beta_les[h] * (E[h] - subs) / pc
            else:
                xh[h] = p.gamma[h] * p.N[h] / WEEKS * (E[h] / max(subs, 1e-9))
            Eh[h] = (xh[h] * pc).sum()
        Dcons = xh.sum(axis=0)
        # ---------- 4. Investissement désiré ----------
        r_now = (1+self.i_L())/(1+self.pi_e)-1
        if self.world is not None and getattr(self, 'sFX', 0.0) > 0:   # économie dollarisée : une part des décisions se finance en devise
            r_now = (1 - self.sFX) * r_now + self.sFX * (self.world.r_foreign_real() + p.mL)
        self.r_long = getattr(self, 'r_long', r_now) + p.lam_r * (r_now - getattr(self, 'r_long', r_now))   # taux réel long : moyenne anticipée des taux courts (le q dépend du taux long)
        r_L = self.r_long
        profit_signal=getattr(self,"Pi_marginal_bar",self.Pi_brut_bar) if p.price_basis=="marginal" else self.Pi_brut_bar
        if p.investment_signal=='marginal_product':profit_signal=getattr(self,'_mpk_profit_bar',p.alpha*np.maximum(self.p_-(p.a*self.p_[:,None]).sum(axis=0),0)*self.Qbar)
        Pi_brut_exp = profit_signal * WEEKS
        q = (Pi_brut_exp / np.maximum(pK * self.K, 1e-9)) / np.maximum(r_L + p.rho_E + p.delta, 0.01)   # coût du capital = taux réel + prime de risque + dépréciation
        ell = self.Loans / np.maximum(pK * self.K, 1e-9)
        Lam = np.clip(1 - p.eta_ell * (ell - p.ell_bar), 0, 1)
        LamBk = self.Lam_bank()
        util = np.clip(Yhat / np.maximum(Ycap_full, 1e-9), 0, 1.5)          # taux d'utilisation des capacités
        gate = np.clip((util - p.util_lo) / (p.util_hi - p.util_lo), 0, 1)  # pas d'investissement net avec des capacités inutilisées
        # accélérateur : investissement net proportionnel à la croissance anticipée des commandes (maintien du ratio capital/produit),
        # plus terme de rentabilité (q de Tobin) ; le tout rationné par le levier, la banque et l'utilisation des capacités
        g_e = np.clip(getattr(self, 'g_orders', np.full(n, p.g0)), -0.05, 0.10)
        if p.sat_q > 0:   # A1b : niveau porté par le q de long terme (moyenne lente), réaction saturante aux écarts de court terme
            self.q_bar = getattr(self, 'q_bar', q) + p.lam_qbar * (q - getattr(self, 'q_bar', q))
            qresp = p.iota * (self.q_bar - 1) + p.iota * p.sat_q * np.tanh((q - self.q_bar) / p.sat_q)
            if p.iota_Pi > 0:   # chantier partage (v1.6) : investissement induit par le cash-flow (Fazzari-Hubbard-Petersen 1988 ; Bhaduri-Marglin 1990) — une fraction iota_Pi du taux de profit net courant (profits nets lissés / capital) s'ajoute au taux d'investissement net ; sans retard (règle §7)
                cf_rate = np.clip(getattr(self, 'Pi_net_bar', np.zeros(p.nsec)) * WEEKS / np.maximum(pK * self.K, 1e-9), 0.0, 0.3)
                qresp = qresp + p.iota_Pi * cf_rate
                self._cf_rate = cf_rate
        else:
            qresp = p.iota * (q - 1)
        net_rate = np.minimum(np.maximum(g_e, 0) * p.acc + qresp, p.inv_cap * p.delta)
        Iw = self.K * (p.delta + np.maximum(net_rate, -0.5 * p.delta) * Lam * LamBk * gate) / WEEKS
        self._diag_inv = dict(q=q.copy(), qbar=self.q_bar.copy() if hasattr(self,'q_bar') else q.copy(), rL=r_L, util=util.copy(), gate=gate.copy(), Lam=Lam.copy(), LamBk=float(LamBk) if np.isscalar(LamBk) else LamBk, net=net_rate.copy(), qresp=qresp.copy(), acc=np.maximum(g_e,0)*p.acc)   # diagnostic (v1.6, chantier absorption)
        if p.investment_mode=='sales_cost':
            try:from .closure import investment_plan
            except ImportError:from closure import investment_plan
            Iw=investment_plan(self,np.maximum(self.Qbar,1e-12),pK,r_L,Lam,LamBk)
            self._diag_inv['net']=self._capital_diag['net_annual'].copy()
        Iw = np.where(self.zombie > 0, 0.0, Iw)
        # ajustement partiel : les programmes d'investissement se révisent lentement (délais de décision et de commande)
        Iw = getattr(self, 'Iw_prev', Iw) + p.lam_I * (Iw - getattr(self, 'Iw_prev', Iw)); self.Iw_prev = Iw.copy()
        # financement : trésorerie puis crédit
        cash = np.array([led.dep[f"F{j}"] for j in range(n)])
        rev_w = self.p_ * self.Qbar
        need_cash = Iw * pK + (Xdem * self.p_[:, None]).sum(axis=0)
        short = np.maximum(need_cash - np.maximum(cash - 0.5 * p.m_bar * rev_w, 0), 0)
        if getattr(p,'payout_mode','psi') == 'leverage_target':   # P1 : la firme emprunte la part ell_star de son investissement et corrige lentement l'ecart de levier (Godley-Lavoie 2007 ch.11) ; le dividende absorbe le residu
            short = np.maximum(short, p.ell_star * pK * Iw - p.lam_ell / WEEKS * (self.Loans - p.ell_star * pK * self.K))
        newloans = np.zeros(n)
        cap_room = self.credit_room()
        for j in range(n):
            if ell[j] < p.ell_bar + 0.4 and self.zombie[j] == 0 and self.E_bank > 0:
                nl = min(short[j], cap_room)
                newloans[j] = nl; cap_room -= nl
        self.Loans += newloans
        for j in range(n): led.dep[f"F{j}"] += newloans[j]   # crédit crée le dépôt
        # Aucun ordre ferme sans financement ; réserve cotisations et intérêts.
        cash=np.array([led.dep[f"F{j}"] for j in range(n)])
        reserve=p.tauS*wage_paid+wk(self.i_L())*self.Loans
        funding=np.minimum(1.,np.maximum(cash-reserve,0.)/np.maximum(need_cash,1e-12))
        Iw*=funding; Xdem*=funding[None,:]
        # État : achats (référence calculée avant les plans de revenu)
        G_cons = rhoG * self._fisc * p.G_share * Ynom_ref / WEEKS / pcomp[2]; G_inv = rhoG * self._fisc * p.Ginv_share * Ynom_ref / WEEKS / pK
        g_cost=G_cons*pcomp[2]+G_inv*pK
        g_reserve=wk(self.i_app)*self.B_bank+wk(self.cbar_cb if p.assets else self.i_app)*self.B_cb
        if p.adv_interest: g_reserve+=wk(self.i_cb)*max(self.AG-self.AG_free,0.)
        g_fund=min(1.,max(led.dep["G"]-g_reserve,0.)/max(g_cost,1e-12))
        G_cons*=g_fund; G_inv*=g_fund
        # ---------- 5. Marchés des biens ----------
        IZ_new = self.housing_block(Yd, pK) if p.assets else 0.0   # logements neufs commandés (unités) et crédit hypothécaire
        self._IZ_plan=float(IZ_new)
        Dfin = np.zeros(n); Dfin[:3] += Dcons; Dfin[2] += G_cons; Dfin[3] += Iw.sum() + G_inv + IZ_new   # demande finale
        Sinv_old=self.Sinv.copy()
        excess=np.maximum(Sinv_old-p.s_star*self.Qbar,0.)
        S=Y+(p.phi_S if p.wsps2 else .5)*excess
        if self.world is not None:
            goods_entry_start=len(led.entries)
            market=yield self.world.make_plan(self,S,xh,Iw,G_cons,G_inv,IZ_new,Xdem)
            Q=market['Q'];D=market['D'];x_obt=market['x_obt'];Xgot=market['Xgot']
            Igot=market['Igot'];EXV=market['EX'];IMV=market['IM']
            frac=np.minimum(1.,Q/np.maximum(D,1e-12))
            got=market['IZ_h'].sum()
            self.pipeline_h[p.T_Z-1]+=market['IZ_h'];self.pipeline=self.pipeline_h.sum(axis=1)
            cancelled=self.world.construction_refunds(self,market,IZ_new)
            for h in range(3):
                refund=min(cancelled[h],self.LZ[h],max(led.dep[f'H{h}'],0.))
                if eight.enabled(self): mortgages.cancel(self,self._IZ_contracts[h],refund)
                self.LZ[h]-=refund;led.dep[f'H{h}']-=refund
            self.KG=(1-.03/WEEKS)*self.KG+market['GI']
        else:
            EX = self.world.exports_to(self) if self.world is not None else np.zeros(n)              # commandes étrangères reçues (semaine précédente)
            IMq = (1 - sh) * Dfin                                                                     # importations en volume
            D = sh * Dfin + Xdem.sum(axis=1) + EX
            if p.rural and getattr(self, 'rural_output', 0) > 0:
                Y = Y.copy(); Y[0] += getattr(self, 'rural_output', 0.0) / WEEKS * 0   # (autoconsommation : ne transite pas par le marché)
            Sinv_old = self.Sinv.copy()
            excess = np.maximum(Sinv_old - p.s_star * self.Qbar, 0)
            S = Y + (p.phi_S if p.wsps2 else 0.5) * excess   # v2.0 : les stocks sont un tampon (Blinder-Maccini 1991) — seule une fraction phi_S de l'excédent est offerte chaque semaine, sinon l'excès d'offre mesuré s'auto-amplifie
            Q = np.minimum(D, S)
            EXq = np.minimum(EX, S)                                   # les exportations sont servies en priorité (contrats)
            Ddom = D - EX
            frac = np.where(Ddom > 1e-12, np.clip((Q - EXq) / np.maximum(Ddom, 1e-12), 0, 1), 1.0)
            # exécution : chaque acheteur obtient frac sur la part domestique ; les importations sont servies au prix rendu
            x_obt = xh * (sh[None, :3] * frac[None, :3] + (1 - sh[None, :3]))
            IMV = 0.0; IMVj = np.zeros(n)
            goods_entry_start=len(led.entries)
            for h in range(3):
                vat = (x_obt[h] * pcomp[:3] * p.tauC).sum()
                for j in range(3):
                    led.transfer(f"H{h}", f"F{j}", xh[h, j] * sh[j] * frac[j] * self.p_[j])
                    v = xh[h, j] * (1 - sh[j]) * pimp[j]; paid = led.transfer(f"H{h}", "FX", v); IMV += paid; IMVj[j] += paid
                led.transfer(f"H{h}", "G", vat)
            led.transfer("G", "F2", G_cons * sh[2] * frac[2] * self.p_[2]); paid = led.transfer("G", "FX", G_cons * (1 - sh[2]) * pimp[2]); IMV += paid; IMVj[2] += paid
            led.transfer("G", "F3", G_inv * sh[3] * frac[3] * pK); paid = led.transfer("G", "FX", G_inv * (1 - sh[3]) * pimp[3]); IMV += paid; IMVj[3] += paid
            Igot = Iw * (sh[3] * frac[3] + (1 - sh[3]))
            if p.assets and IZ_new > 0:
                got = IZ_new * (sh[3] * frac[3] + (1 - sh[3]))
                for h in range(3): led.transfer(f"H{h}", "F3", IZ_new * sh[3] * frac[3] * pK * self._IZ_share[h])
                self.pipeline_h[p.T_Z-1]+=got*self._IZ_share
                self.pipeline=self.pipeline_h.sum(axis=1)
                # Un prêt lié à une commande rationnée est immédiatement remboursé.
                cancelled=(1-got/max(IZ_new,1e-12))*self._IZ_loan
                for h in range(3):
                    refund=min(cancelled[h],self.LZ[h],max(led.dep[f"H{h}"],0.))
                    if eight.enabled(self): mortgages.cancel(self,self._IZ_contracts[h],refund)
                    self.LZ[h]-=refund; led.dep[f"H{h}"]-=refund   # livré après T_Z semaines
            self.KG = (1 - 0.03 / WEEKS) * self.KG + G_inv * (sh[3] * frac[3] + (1 - sh[3]))
            for j in range(n):
                led.transfer(f"F{j}", "F3", Iw[j] * sh[3] * frac[3] * pK); paid = led.transfer(f"F{j}", "FX", Iw[j] * (1 - sh[3]) * pimp[3]); IMV += paid; IMVj[3] += paid
            # exportations : payées par le compte de change aux producteurs
            EXV = 0.0
            EXtot = self.world.exports_value(self) if self.world is not None else (EX * self.p_).sum()   # ce que les importateurs ont payé, converti
            wv = EX * self.p_; wv = wv / wv.sum() if wv.sum() > 1e-12 else np.zeros(n)
            for j in range(n):
                if wv[j] > 0: EXV += led.transfer("FX", f"F{j}", EXtot * wv[j])
            tarif = IMV * (1 - 1 / (1 + (self.world.tauM if self.world is not None else 0.0)))
            led.transfer('FX', 'G', tarif); IMV -= tarif                 # recettes douanières à l'État ; IMV = valeur payée aux étrangers
            self.IMVj_last = IMVj / (1 + (self.world.tauM if self.world is not None else 0.0))   # valeur nette payée par bien
            self.IMq_last = IMq.copy(); self.EXq_last = EXq.copy(); self.IMV_last = IMV; self.EXV_last = EXV
            self.R_fx += (EXV - IMV) / self.e           # règlement du commerce en réserves (monnaie étrangère)
            Xgot = Xdem * frac[:, None]
            for k in range(n):
                for j in range(n):
                    if Xgot[k, j] > 0: led.transfer(f"F{j}", f"F{k}", Xgot[k, j] * self.p_[k])
        self.Xinv += Xgot
        receipts=np.zeros(n)
        for frm,to,amount in led.entries[goods_entry_start:]:
            if to.startswith("F") and to!="FX": receipts[int(to[1:])]+=amount
        self._goods_payment_residual=float(np.max(np.abs(receipts-Q*self.p_)))
        sold = Q
        self.Sinv = Sinv_old + Y - Q   # invendus + stock conservé
        # capital
        self.K = (1 - p.delta / WEEKS) * self.K + Igot
        # ---------- 6. Comptes des secteurs ----------
        revenue = sold * self.p_
        wages = wage_paid * (1+p.tauS)
        cotis = wage_paid * p.tauS
        for j in range(n): led.transfer(f"F{j}", "G", cotis[j])
        inputs_cost = (Xgot * self.p_[:, None]).sum(axis=0)
        interest = wk(self.i_L()) * self.Loans
        # L'intérêt impayé est capitalisé ; la perte éventuelle est comptabilisée séparément.
        interest_unpaid=np.zeros(n)
        for j in range(n):
            paid=min(interest[j],max(led.dep[f"F{j}"],0.))
            led.dep[f"F{j}"]-=paid
            interest_unpaid[j]=interest[j]-paid
            self.Loans[j]+=interest_unpaid[j]
            change_book(self,interest[j],'corporate_loan_interest')
        inputs_used=(used*self.p_[:,None]).sum(axis=0)
        inventory_change=(self.Sinv-Sinv_old)*self.p_
        Pi_brut = revenue + inventory_change - wages - inputs_used
        Pi = Pi_brut - p.delta / WEEKS * pK * K_start - interest
        taxPi = p.tauPi * np.maximum(Pi, 0)
        for j in range(n): led.transfer(f"F{j}", "G", taxPi[j])
        Pi_net = Pi - taxPi
        self.Pi_brut_bar = getattr(self, "Pi_brut_bar", Pi_brut) * 0.95 + 0.05 * Pi_brut
        marginal_profit=p.alpha*np.maximum(self.p_/(1+self.markup)-(p.a*self.p_[:,None]).sum(axis=0),0)*Y
        self.Pi_marginal_bar=.95*getattr(self,"Pi_marginal_bar",marginal_profit)+.05*marginal_profit
        mpk_profit=p.alpha*np.maximum(self.p_-(p.a*self.p_[:,None]).sum(axis=0),0)*Y
        self._mpk_profit_bar=.95*getattr(self,'_mpk_profit_bar',mpk_profit)+.05*mpk_profit
        # remboursement de dette puis distribution de la trésorerie excédentaire (au-delà de la cible)
        cash = np.array([led.dep[f"F{j}"] for j in range(n)])
        excess_cash = np.maximum(cash - p.m_bar * revenue, 0)
        repay = np.minimum(0.25 * excess_cash, np.maximum(self.Loans - p.ell_star * pK * self.K, 0) if getattr(p,'payout_mode','psi')=='leverage_target' else self.Loans)   # P1 : on ne rembourse que l'exces de levier
        self.Loans -= repay
        for j in range(n): led.dep[f"F{j}"] -= repay[j]
        excess_cash -= repay
        self.Pi_net_bar = getattr(self, 'Pi_net_bar', Pi_net) * (1 - p.lam_div) + p.lam_div * Pi_net   # C3 : dividendes sur profit lissé
        if p.payout_mode == 'leverage_target':   # P1
            retention = (1 - p.ell_star) * pK * getattr(self, 'Iw_prev', np.zeros(n)) + p.lam_ell / WEEKS * (self.Loans - p.ell_star * pK * self.K)
            base_div = np.clip(self.Pi_net_bar - retention, 0, np.maximum(cash - repay, 0))
            self._psi_eff = base_div / np.maximum(self.Pi_net_bar, 1e-9)
        else: base_div = np.minimum(p.psi * np.maximum(self.Pi_net_bar, 0), np.maximum(cash - repay, 0))   # dividendes prioritaires : psi du profit net (l'investissement se finance ensuite sur trésorerie et crédit)
        div = base_div + 0.25 * np.maximum(excess_cash - base_div, 0)
        for j in range(n):
            for h in range(3): led.transfer(f"F{j}", f"H{h}", div[j] * self.equity_ownership()[h])
        self.div_last = div
        # Défaut : intérêt non servi ou paie incomplète. Aucun dépôt créé par abandon de créance.
        self._capital_loss=np.zeros(n)
        for j in range(n):
            distress=interest_unpaid[j]>1e-9 or planned_wages[j]-wage_paid[j]>1e-9
            if distress:
                if self.zombie[j]==0:
                    self.faillites+=1
                    loss=min(self.Loans[j],.5*self.Loans[j])
                    self.Loans[j]-=loss; change_book(self,-loss,'corporate_default_loss')
                    self._capital_loss[j]=p.phi_F*self.K[j]
                    self.K[j]-=self._capital_loss[j]; self.L[j]*=1-p.phi_F
                self.zombie[j]=max(self.zombie[j],13)
            else: self.zombie[j]=max(0,self.zombie[j]-1)
        self._output_prices=self.p_.copy()
        self._flows=dict(I_real=float(Igot.sum()), IZ_real=float(IZ_new*frac[3]), C=float(np.sum(x_obt*pcomp[:3])),VAT=float(np.sum(x_obt*pcomp[:3])*p.tauC),
            I=float(Igot.sum()*pK),G=float(G_cons*frac[2]*self.p_[2]+G_inv*frac[3]*pK+pub_wages),
            IZ=float(IZ_new*frac[3]*pK),inventories=float(np.sum((self.Sinv-Sinv_old)*self.p_)+np.sum((self.Xinv-X_start)*self.p_[:,None])),
            EX=EXV,IM=IMV,Y=float(np.sum(self.p_*Y-inputs_used)+pub_wages),
            wage_share=float((wages.sum()+pub_wages)/max(np.sum(self.p_*Y-inputs_used)+pub_wages,1e-9)),
            stock_residual=float(np.max(np.abs(self.Sinv-Sinv_old-Y+Q))))
        if self.world is not None:
            self._flows.update(C=float(market['C']),VAT=float(market['VAT']),I=float(market['I']),
                IZ=float(market['IZ']),IZ_real=float(market['IZ_h'].sum()),G=float(market['G']+pub_wages),
                tariffs=float(market['tariff']))
        # ---------- 7. Prix ----------
        z = np.where(D + S > 1e-3 * self.Qbar, (D - S) / np.maximum(D + S, 1e-9), 0.0); self._dbg = (D.copy(), S.copy(), z.copy(), E.copy(), Yd.copy(), Iw.sum(), G_cons, Xdem.sum(axis=1))
        if p.wsps2:   # v2.0 : le coût unitaire de tarification utilise les intrants CONSOMMES (a_ij p_i Y), pas les achats de la semaine (Xgot, qui dépendent des stocks d'intrants et de la trésorerie) — l'ancienne mesure sous-estimait le coût de 3 à 11 % à l'initialisation et faisait chuter les prix
            inputs_used = (p.a * Y[None, :] * self.p_[:, None]).sum(axis=0)
            self._pK_repl = pK if p.valuation_smoothing<=0 else getattr(self,'_pK_repl',pK)+(pK-getattr(self,'_pK_repl',pK))/(p.valuation_smoothing*WEEKS)   # v2.0 (session 5) : prix de remplacement lissé sur un an pour la dépréciation dans le coût — casse la boucle prix-coût du secteur d'équipement (p_K entre dans son propre coût)
            cu = (wages + inputs_used + p.delta / WEEKS * self._pK_repl * K_start) / np.maximum(Y, 1e-9)
            if p.price_basis=="marginal":
                cu=(wages/np.maximum(1-p.alpha,1e-9)+inputs_used)/np.maximum(Y,1e-9)
            self._diag_cu = dict(wY=wages/np.maximum(Y,1e-9), xY=inputs_used/np.maximum(Y,1e-9), dY=p.delta/WEEKS*self._pK_repl*K_start/np.maximum(Y,1e-9), Y=Y.copy(), Q=self.Qbar.copy(), mu=self.markup.copy())
        else:
            cu = (wages + inputs_cost + p.delta / WEEKS * pK * self.K) / np.maximum(Y, 1e-9)
        if p.markup_live:   # voie 2 (chantier partage) : marge normale vivante = rendement requis (taux réel long + prime) sur le capital courant, rapporté au coût unitaire courant ; lissée sur un an
            cu_tot = np.maximum(wages + inputs_cost + p.delta / WEEKS * pK * self.K, 1e-9)
            mk_now = np.clip((max(self.r_long, 0.0) + p.rho_E) / WEEKS * pK * self.K / cu_tot, 0.0, 1.0)
            self.markup = self.markup + p.lam_mk * (mk_now - self.markup)
        if p.markup_inv > 0:   # jambe 2 (chantier salaires-prix) : marge cible sensible aux stocks (Godley-Lavoie 2007, ch. 8) — stocks sous la cible : marge relevée ; au-dessus : abaissée. Sans cela, la marge normale figée ancre le niveau des prix au coût et un excès de demande persistant reste un rationnement sans inflation (H7 sous L_prof_va)
            inv_gap = (p.s_star * self.Qbar - self.Sinv) / np.maximum(p.s_star * self.Qbar, 1e-9)
            self.markup = np.clip(self.markup * (1 + p.markup_inv * np.clip(inv_gap, -1, 1)), 0.0, 1.0)
            self._inv_gap = inv_gap
        flex = 1 + p.flex_infl * max(self.pi_e, 0)              # prix plus flexibles quand l'inflation est forte (coûts de menu négligeables)
        idx_w = np.clip(1 + z, 0, 1)   # un vendeur en excès d'offre n'indexe pas ses prix
        if p.wsps2 and p.price_mode == 'tat':   # v2.0 variante « tâtonnement ancré » (proposition du 10/09) : le prix cherche l'équilibre du marché par tâtonnement sur l'excès de demande, et son ancre de long terme est le prix de monopole (1+mu_n) x cu — la marge effective est mesurée, pas commandée
            mu_n = (1.0 / (p.eps_goods - 1.0)) if p.eps_goods is not None else self.mu_n_sec
            adj = np.clip(p.kappa_p * flex * z, -min(p.kappa_bar * flex, 0.5), min(p.kappa_bar * flex, 0.5)) + p.mu_c2 * np.clip(cu * (1 + mu_n) / self.p_ - 1, -0.5, 0.5)
            self.markup = np.clip(self.p_ / np.maximum(cu, 1e-9) - 1, 0.0, 2.0)   # marge observée
            self._inv_gap = (p.s_star * self.Qbar - self.Sinv) / np.maximum(p.s_star * self.Qbar, 1e-9)
        elif p.wsps2:   # v2.0 : une seule équation de prix — p -> (1+mu) x coût unitaire, la marge mu répondant à l'excès de demande et aux stocks (Godley-Lavoie ; Rotemberg-Woodford), rappelée vers la marge normale 1/(eps-1)
            mu_n = (1.0 / (p.eps_goods - 1.0)) if p.eps_goods is not None else self.mu_n_sec   # archétype : eps_goods fourni ; sinon marge normale sectorielle de l'état initial
            inv_gap = (p.s_star * self.Qbar - self.Sinv) / np.maximum(p.s_star * self.Qbar, 1e-9)
            self.markup = np.clip(self.markup * (1 + flex * (p.kappa_mu_z * z + p.kappa_mu_s * np.clip(inv_gap, -1, 1))) + p.lam_mu_n * (mu_n - self.markup), 0.0, 2.0)
            price_target = cu * (1 + self.markup)
            if p.equipment_supply_response:
                # Inverse marginal-product labor demand at forecast output.
                # Fixed capital is sunk at this weekly production decision;
                # depreciation remains in the usual average-cost target.
                input_unit = (p.a * self.p_[:, None]).sum(axis=0)
                mc_orders = input_unit + self.W * (1+p.tauS) * L_tech / np.maximum((1-p.alpha)*Yhat, 1e-12)
                self._equipment_price_diag=dict(average_target_ratio=float(price_target[3]/pK),marginal_target_ratio=float(mc_orders[3]/pK),
                    self_cost_gain=float((1+self.markup[3])*(p.a[3,3]+p.delta[3]*K_start[3]/(WEEKS*max(Y[3],1e-9)))))
                price_target[3] = mc_orders[3] if p.equipment_price_mode=='orders_marginal' else max(price_target[3], mc_orders[3])
            if p.pricing_cost_mode=='orders_marginal_all':
                from .audit_profile import marginal_order_prices
                price_target=marginal_order_prices(self,Yhat,L_tech)
            if p.pricing_cost_mode=='capacity_average':
                from .workplan import capacity_prices
                price_target=capacity_prices(self,Ycap,Y,wages,K_start,pK)
            if p.pricing_cost_mode=='normal_average':   # W10 : cout normal — les couts engages (salaires, depreciation) sont repartis sur max(Y, util_normal x capacite de l'emploi en place), jamais sur un debit rationne
                from .workplan import capacity_prices
                price_target=capacity_prices(self,np.maximum(Y,p.util_normal*Ycap),Y,wages,K_start,pK)
            adj = p.mu_fast * np.clip(price_target / self.p_ - 1, -0.5, 0.5)   # pas de terme d'indexation séparé : les coûts contiennent déjà les salaires indexés (double comptage sinon) ; l'inflation est la croissance du coût unitaire plus celle de la marge
            if p.price_demand_feedback:
                adj += np.clip(p.kappa_p * flex * z, -min(p.kappa_bar * flex, 0.5), min(p.kappa_bar * flex, 0.5))
            self._inv_gap = inv_gap
        else:
            adj = np.clip(p.kappa_p * flex * z, -min(p.kappa_bar * flex, 0.5), min(p.kappa_bar * flex, 0.5)) + idx_w * p.varpi_p * self.pi_e / WEEKS
            adj += p.mu_c * np.clip(cu * (1 + self.markup) / self.p_ - 1, -0.5, 0.5)   # rappel symétrique vers le coût unitaire majoré de la marge normale
        self._diag_p = dict(z=z.copy(), tat=np.clip(p.kappa_p * flex * z, -min(p.kappa_bar * flex, 0.5), min(p.kappa_bar * flex, 0.5))*WEEKS, idx=idx_w * p.varpi_p * self.pi_e, cost=p.mu_c * np.clip(cu * (1 + self.markup) / self.p_ - 1, -0.5, 0.5)*WEEKS, cu_gap=cu*(1+self.markup)/self.p_-1)   # diagnostic (annualisé)
        self.p_ *= np.clip(1 + adj, 0.7, p.max_weekly_price)   # borne : hyperinflation numériquement finie (~100 %/mois)
        self._price_step=np.log(np.clip(1+adj,0.7,p.max_weekly_price))
        if self.world is not None and getattr(self.world, 'energy_world', False):
            self.p_[1] = (1 - self.world.lam_lop) * self.p_[1] + self.world.lam_lop * self.e * self.world.p_w_energy   # rappel vers le prix mondial (loi du prix unique, arbitrage)
        self._DS_energy = (D[1], S[1])
        if self.world is not None:
            # Toutes les cotations productrices doivent être révisées avant
            # l'évaluation des bilans et des garanties dans les autres pays.
            yield 'prices'
        # ---------- 8. Banque, BC, État ----------
        # recapitalisation publique d'une banque insolvable (obligations souscrites par la banque centrale) : le coût va à la dette
        under_cap = self.E_bank < p.recap_thresh * p.kappa_CAR * (self.Loans.sum() + ((self.LZ.sum() + self.LE) if p.assets else 0.0))
        if (self.E_bank < 0 or under_cap) and self.t - self.last_recap >= WEEKS:   # banque insolvable ou sous-capitalisée : au plus un sauvetage par an
            need = p.kappa_CAR * 1.2 * max(self.Loans.sum() + ((self.LZ.sum() + self.LE) if p.assets else 0.0), 0.05 * Ynom_prev) - self.E_bank
            if not eight.enabled(self): self._recap_tick=float(need)
            try:from .bank_equity import public_grant
            except ImportError:from bank_equity import public_grant
            public_grant(self,need)
        if p.assets: self.assets_block(Ynom_prev, month)
        # émission d'actions bancaires : quand le capital est insuffisant (< 1,1 x exigence), la banque lève des fonds propres auprès des ménages
        Ltot_bk = self.Loans.sum() + ((self.LZ.sum() + self.LE) if p.assets else 0.0)
        if p.bank_issue and self.E_bank < 1.1 * p.kappa_CAR * Ltot_bk and self.E_bank > 0:
            need = 1.3 * p.kappa_CAR * Ltot_bk - self.E_bank
            cap = 0.02 * sum(max(led.dep[f'H{h}'], 0) for h in range(3))
            issue = min(need, cap)
            try:from .bank_equity import subscribe
            except ImportError:from bank_equity import subscribe
            subscribe(self,issue*p.omega)
        # réglementation de liquidité : la banque détient des titres publics au moins égaux à phi_liq des dépôts (achats aux ménages)
        if p.phi_liq > 0:
            need_b = p.phi_liq * led.total() - self.B_bank
            if need_b > 0 and self.Bh.sum() > 0:
                buy = min(need_b, 0.02 * self.Bh.sum()); sh_h = self.Bh / self.Bh.sum()
                self.Bh -= buy * sh_h; self.B_bank += buy
                for h in range(3): led.dep[f'H{h}'] += buy * sh_h[h]
        # profits bancaires -> dividendes aux ménages (si E > cible)
        Etarget = p.kappa_CAR * 1.3 * (self.Loans.sum() + ((self.LZ.sum() + self.LE) if p.assets else 0.0))
        car = self.E_bank / max(self.Loans.sum() + ((self.LZ.sum() + self.LE) if p.assets else 0.0), 1e-9)
        payout = 0.05 * float(np.clip(car / (1.3 * p.kappa_CAR), 1.0, 3.0)) if p.div_coverage else 0.05   # capital excédentaire (demande de crédit faible) -> distribution accélérée
        divb = max(0, (self.E_bank - Etarget)) * payout
        try:from .bank_equity import pay_dividends
        except ImportError:from bank_equity import pay_dividends
        pay_dividends(self,divb)
        # intérêts de la dette publique détenue par banque / BC
        E_cb_start = self.E_cb
        ib = wk(self.i_app)
        due_b=ib*self.B_bank
        cb_rate=wk(self.cbar_cb) if p.assets else ib
        due_cb=cb_rate*self.B_cb
        due_ag=wk(self.i_cb)*max(self.AG-self.AG_free,0.) if p.adv_interest else 0.
        share=min(1.,max(led.dep["G"],0.)/max(due_b+due_cb+due_ag,1e-12))
        led.dep["G"]-=share*(due_b+due_cb+due_ag)
        self.B_bank+=(1-share)*due_b; change_book(self,due_b,'sovereign_coupon_income')
        self.B_cb+=(1-share)*due_cb; self.AG+=(1-share)*due_ag
        self.E_cb+=due_cb+due_ag
        cb_cash_profit=share*(due_cb+due_ag)
        # Refinancement bancaire : charge effective au taux directeur.
        refin_cost=wk(self.i_cb)*self.L_cb
        change_book(self,-refin_cost,'refinancing_expense'); self.E_cb+=refin_cost; cb_cash_profit+=refin_cost
        if p.assets:
            ires = max(self.i_cb - p.dres, 0.0)
            Res_rem = min(self.Res, self.B_cb + max(self.AG - self.AG_free, 0.0) + self.L_cb)     # seules les réserves adossées à des actifs portant intérêt sont rémunérées (sinon : perte structurelle de la BC = monétisation)
            self.E_cb -= wk(ires) * Res_rem; change_book(self,wk(ires)*Res_rem,'reserve_interest_income')
            cb_cash_profit-=wk(ires)*Res_rem
            # opérations structurelles : le portefeuille de la BC suit ses réserves (sinon la rémunération des réserves est une perte structurelle = monétisation cachée)
            # FX settlement claims also back reserves. Ignoring them repeatedly
            # triggers domestic bond purchases in a creditor country; purchases
            # from households then create still more deposits/reserves. This is
            # coverage of the balance sheet, not an invented yield on FX claims:
            # the existing remunerated-reserve cap above remains unchanged.
            external_cover=self.e*self.R_fx if p.cb_include_external_assets else 0.
            gap_cb = self.Res - (self.B_cb + self.AG + self.L_cb + external_cover)
            if gap_cb > 0:
                purchase_public_bonds(self,gap_cb)
            if self.qe_rate > 0:   # QE : achats de titres au pair, coupon moyen actualisé
                want = self.qe_rate * Ynom_prev / WEEKS
                purchase_public_bonds(self,want)
        # seigneuriage : BC verse son profit à l'État (E_cb -> dépôt G)
        # seigneuriage : le profit de la période est versé à l'État si les fonds propres statutaires sont reconstitués (report à nouveau sinon)
        profit_cb = self.E_cb - E_cb_start
        seig = min(max(profit_cb,0.),max(cb_cash_profit,0.),max(self.E_cb-self.E_cb0,0.))
        self.E_cb -= seig; led.dep["G"] += seig
        # avances (monétisation) : test
        if self.monetize > 0:
            adv = self.monetize * Ynom_prev / WEEKS
            self.AG += adv; led.dep["G"] += adv
        # émission / rachat de dette pour ramener le compte du Trésor à sa cible
        Gtarget = p.gov_cash_ratio * Ynom_prev
        gap = Gtarget - led.dep["G"]  # >0 : besoin d'emprunter
        deficit_w = gap
        hh_financing=0.
        redemptions=dict(households=0.,bank=0.,central_bank=0.,advances=0.,total=0.)
        # placement : ménages achètent une part de leur épargne, banque absorbe le reste
        if gap > 0:
            hh_buy = np.array([max(min(p.sB * (Yd[h] - Eh[h]), led.dep[f"H{h}"] * 0.5), 0) for h in range(3)], dtype=float)
            hh_buy *= min(1.0, gap / max(hh_buy.sum(), 1e-9))
            # demande d'obligations sensible au rendement : quand l'écart souverain-dépôts s'élargit, les ménages arbitrent leurs dépôts vers les titres
            room_bk_pre = max(p.phi_Bbank * led.total() - self.B_bank, 0.0) if self.E_bank > 0 else 0.0
            resid = max(gap - hh_buy.sum() - room_bk_pre, 0.0)
            if resid > 0:
                elast = float(np.clip(p.kappa_hB * (self.i_B - max(self.i_cb - p.mD, 0)), 0.0, 1.0))
                extra = np.array([max(led.dep[f"H{h}"], 0) for h in range(3)]) * np.array([0.2, 0.3, 0.5]) * 0.05 * elast
                extra *= min(1.0, resid / max(extra.sum(), 1e-9))
                hh_buy += extra
            # Settle bounded purchases and issue the bonds actually paid for.
            # A fully subscribed issue has zero remaining financing need;
            # floating-point cancellation must never issue a negative bank bond.
            hh_buy=np.array([led.transfer(f"H{h}","G",hh_buy[h]) for h in range(3)])
            hh_financing=float(hh_buy.sum())
            self.Bh += hh_buy
            rest = max(gap - hh_buy.sum(),0.)
            room_bk = max(p.phi_Bbank * led.total() - self.B_bank, 0.0) if self.E_bank > 0 else 0.0   # la banque absorbe la dette publique jusqu'à une part de son bilan (limite de concentration), si elle est solvable
            bk_buy = min(rest, room_bk)
            self.B_bank += bk_buy; led.dep["G"] += bk_buy  # la banque crédite le Trésor contre l'obligation, dans la limite de ses fonds propres
            unplaced = rest - bk_buy
            # dette non placée : l'État réduit l'exécution de ses dépenses la semaine suivante
            self.rhoG = float(np.clip(self.rhoG - 0.1 * (unplaced > 1e-9) + 0.02 * (unplaced <= 1e-9), 0.2, 1.0))
        else:
            self.rhoG = float(min(self.rhoG + 0.02, 1.0))
            if p.treasury_redeem_all:
                redemptions=redeem_public_debt(self,-gap)
            else:
                buyback = min(-gap, self.B_bank)
                self.B_bank -= buyback; led.dep["G"] -= buyback
                redemptions.update(bank=float(buyback),total=float(buyback))
        self.B = self.Bh.sum() + self.B_bank + self.B_cb
        # Déficit par variation de dette et du compte du Trésor, avances incluses.
        deficit_w=(self.B+self.AG)-(B_start+AG_start)-(led.dep["G"]-self._gov_cash_start)
        legacy_deficit=deficit_w
        if p.precise_fiscal_deltas:
            import math
            closing=np.r_[self.Bh,self.B_bank,self.B_cb,self.AG,led.dep['G']]
            deltas=closing-fiscal_opening
            deficit_w=math.fsum([*deltas[:-1],-deltas[-1]])
            self._fiscal_precision=dict(legacy=float(legacy_deficit),component_deltas=deltas.copy(),opening=fiscal_opening.copy(),closing=closing.copy())
        cash_deficit=sum(a for frm,to,a in led.entries if frm=="G")-sum(a for frm,to,a in led.entries if to=="G")+hh_financing-redemptions['households']
        accrued_deficit=cash_deficit+due_b+due_cb+due_ag+float((due-int_bond).sum())-seig+self._recap_tick-self._bank_public_dividend
        self._flows["deficit"]=float(deficit_w)
        self._flows["deficit_from_flows"]=float(accrued_deficit)
        self._flows["debt_total"]=float(self.B+self.AG)
        self._flows.update(household_taxes=float(taxes_h.sum()),household_tax_base=tax_base,
            tax_scale=float(self.tax_scale),tauK_effective=float(tauK_eff),
            tax_deficit_target=float(getattr(self,'_tax_deficit_target',0.)),
            rstar=float(self.rstar_est),rstar_anchor=float(getattr(self,'_rstar_anchor',self.rstar_est)))
        self._flows.update(treasury_cash=float(led.dep['G']),treasury_target=float(Gtarget),
            treasury_dividend=self._treasury_dividend,
            redemption_households=redemptions['households'],redemption_bank=redemptions['bank'],
            redemption_cb=redemptions['central_bank'],redemption_advances=redemptions['advances'],
            redemption_total=redemptions['total'])
        # ---------- 9. Réserves / cohérence ----------
        # Bilan banque : Res + Loans + B_bank = Dépôts + L_cb + E_bank  -> Res dérivé
        Dtot = led.total()
        self.Res = Dtot + self.L_cb + self.E_bank - self.Loans.sum() - self.B_bank - ((self.LZ.sum() + self.LE) if p.assets else 0.0)
        # BC : B_cb + AG + L_cb = Res + E_cb ; si Res < 0 la banque se refinance
        if self.Res < 0:
            self.L_cb += -self.Res; self.Res = 0.0
        check = central_bank_check(self)
        # ---------- 10. Mensuel ----------
        Ynom = max((self._output_prices*Y-inputs_used).sum()+pub_wages,1e-6)
        self._Ynom_w = Ynom
        Yreal = max((Y-used.sum(axis=1)).sum()+LG*pub_wages/max(public_wages_full,1e-12)*self.W_public_base,1e-6)
        if month:
            w = np.array([0.35, 0.15, 0.50])
            P = (w * pcomp[:3]).sum()*(1+p.tauC)/self._cons_price_base
            self.P_hist.append(P)
            if len(self.P_hist) > int(PERIODS_PER_YEAR): self.pi = P / self.P_hist[-1-int(PERIODS_PER_YEAR)] - 1
            nb = int(p.rule_months); pi_m = float(np.clip(np.log(P / self.P_hist[-1 - nb]), -0.5, 0.5)) * PERIODS_PER_YEAR / nb if len(self.P_hist) > nb else self.pi   # inflation récente annualisée (log, bornée : pas d'amplification du bruit)
            self.pi_s = getattr(self, 'pi_s', self.pi) * (1 - p.smooth_pi) + p.smooth_pi * pi_m   # inflation lissée pour la règle
            # anticipations & crédibilité
            lam = p.lam0 + (p.lam1 if self.pi > p.pi_hyper else 0)
            M = max(self.money_supply(), 1e-9) * (1 - getattr(self, 'sFX', 0.0)); Mprev = getattr(self, "_M_prev", M); Yr_prev = getattr(self, "_Yr_prev", Yreal)
            gM = (M / Mprev - 1) * PERIODS_PER_YEAR if Mprev > 0 else 0; gY = (Yreal / max(Yr_prev, 1e-9) - 1) * PERIODS_PER_YEAR
            self.pi_e += (lam * (self.pi - self.pi_e) + self.cred * (p.pi_star - self.pi_e) + p.ups * (gM - gY - self.pi_e)) / PERIODS_PER_YEAR
            if p.wsps2 and self.monetize > 0:   # v2.0 : quand la crédibilité est perdue, les agents anticipent l'inflation qu'implique le seigneuriage observé (Sargent 1982 ; Cagan : pi = seigneuriage / encaisses réelles), avant que les prix ne la montrent
                pi_seig = self.monetize / max(M / max(self.Y_nom_prev(), 1e-9), 0.2)
                self.pi_e += (1 - self.cred) * p.ups_s * (pi_seig - self.pi_e) / PERIODS_PER_YEAR
            raw_expectation=float(self.pi_e)
            raw_credibility=self.cred + p.nu1 * (abs(self.pi - p.pi_star) < p.eps_bar) - p.nu2 * abs(self.pi - p.pi_star) / PERIODS_PER_YEAR - p.nu3 * (self.monetize > 0) / PERIODS_PER_YEAR
            credibility_cap=max(1-p.nu9*self.M_hist,p.cred_floor)
            self.pi_e = float(np.clip(raw_expectation, -0.1, 12.0))
            self.cred = float(np.clip(raw_credibility, 0, credibility_cap))
            self._belief_limits=dict(t=t,raw_expectation=raw_expectation,expectation_lower=-.1,expectation_upper=12.,
                expectation_clipped=bool(raw_expectation!=self.pi_e),raw_credibility=float(raw_credibility),
                credibility_lower=0.,credibility_upper=float(credibility_cap),
                credibility_clipped=bool(raw_credibility!=self.cred))
            self._M_prev = M; self._Yr_prev = Yreal
            # terme d'encaisses réelles
            Ypot = Yreal * (1 - self.u_n) / max(1 - u, 1e-6)
            if p.money_norm:   # v1.6 : la vitesse de référence 1/m_norm suit une norme lente des encaisses réelles (approfondissement financier), Cagan centré sur la cible ; le terme est nul à l'état stationnaire quel que soit M/Y
                m_obs = M / max(P * Ypot * WEEKS, 1e-9)
                if not hasattr(self, 'm_norm'): self.m_norm = m_obs
                self.m_norm += (m_obs - self.m_norm) / (p.tau_m * PERIODS_PER_YEAR)   # bloc mensuel
                Pstar = P * (m_obs / max(self.m_norm, 1e-9)) * np.exp(p.a_cagan * (min(self.pi_e, p.pi_e_sat) - p.pi_star))
            else:
                Vc = p.V0 * np.exp(p.a_cagan * min(self.pi_e, p.pi_e_sat))   # vitesse saturée (la fuite devant la monnaie a une limite physique)
                Pstar = M * Vc / max(Ypot * WEEKS, 1e-9)
            self.p_ *= np.clip(np.exp(p.xi_M * 4 * (np.log(Pstar) - np.log(P))), 0.8, 1.5)
            # salaires
            prod = Yreal / max(self.L.sum() + LG, 1e-9)                       # productivité apparente du travail
            gp = PERIODS_PER_YEAR * float(np.clip(np.log(prod / getattr(self, '_prod_prev', prod)), -0.1, 0.1)) if hasattr(self, '_prod_prev') else p.g0
            self._prod_prev = prod
            self.g_prod = getattr(self, 'g_prod', p.g0) * 0.9 + 0.1 * gp     # tendance lissée
            gA = self.g_prod                                                  # les gains de productivité réels sont partagés
            v = np.clip((Lstar - self.L) / np.maximum(self.L, 1e-9), -0.2, 0.2)
            realized_index = self.pi if p.wage_indexation_mode=='symmetric' else max(self.pi_e,self.pi)
            pi_ref = self.cred * self.pi_e + (1 - self.cred) * realized_index
            self._wage_index_ref=float(pi_ref)
            if p.idx_catchup > 0:   # chantier partage (v1.6) : rattrapage sur l'inflation réalisée (Gray 1976, Fischer 1977 : les contrats indexent ex post) — l'indexation sur la seule anticipation est un cliquet : quand l'inflation réalisée est sous l'anticipée (transition initiale, désinflation), le salaire réel gagne l'écart sans le rendre
                pi_ref = pi_ref + p.idx_catchup * (self.pi - self.pi_e)
            unprof = Lp_last < 0.5 * Lt_last                       # le salaire rend l'emploi non rentable : baisse forcée des offres
            idx_u = float(np.clip(1 - 2 * max(u - self.u_n, 0), 0, 1))   # l'indexation salariale s'affaiblit avec le chômage de masse
            tension = p.phi_x * min(self.excess_ld, 1.0)                     # surchauffe : surenchère salariale quand la main-d'œuvre manque (Phillips convexe)
            ws_corr = 0.0
            if p.ws_anchor:   # chantier absorption (v1.6) : rappel du salaire vers la productivité marginale du travail — part salariale sectorielle de la VA rappelée vers (1 - alpha_j) (Cobb-Douglas, négociation de Nash à la Mortensen-Pissarides) ; sans ce terme, le niveau du salaire n'est ancré que par l'indexation et Phillips, et la part salariale dérive
                VA_w = self.p_ * self.Qbar - (p.a * (self.p_[:, None] * self.Qbar[None, :])).sum(axis=0)
                ws_sec = self.W * self.L * (1 + p.tauS) / np.maximum(VA_w, 1e-9)
                self._ws_bar = getattr(self, '_ws_bar', ws_sec) + p.lam_ws * (ws_sec - getattr(self, '_ws_bar', ws_sec))   # part lissée (la négociation regarde la tendance, pas le mois)
                ws_corr = p.kappa_ws * ((1 - p.alpha) - self._ws_bar)
                self._ws_sec = ws_sec
            if p.wsps2:   # v2.0 : courbe de salaire avec NIVEAU (Blanchflower-Oswald 1994 ; LNJ) — cible = part (1-alpha) du produit moyen du travail en valeur ajoutée, décroissante avec le chômage mesuré par rapport à une référence mêlant insiders (chômage récent) et structure (u_n0)
                self._u_rec = getattr(self, '_u_rec', u) + (u - getattr(self, '_u_rec', u)) / (3*PERIODS_PER_YEAR)   # chômage récent (3 ans, mensuel)
                u_ref = p.h_ins * self._u_rec + (1 - p.h_ins) * p.u_n
                revenue_price=self.p_/(1+self.markup) if p.price_basis=="marginal" else self.p_
                p_va_w = np.maximum(revenue_price - (p.a * self.p_[:, None]).sum(axis=0), 1e-9)
                W_star = (1 - p.alpha) * p_va_w * self.Qbar / np.maximum(self.L, 1e-9) / (1 + p.tauS) * np.exp(-p.beta_u * (u - u_ref))
                level = p.lam_w * np.clip(np.log(W_star / np.maximum(self.W, 1e-9)), -0.5, 0.5)
                self._diag_w2 = dict(W_star_W=W_star / self.W, u_ref=u_ref)
                wage_indexation=getattr(self,'_agreement_indexation',p.varpi_w) if p.audit_corrections else p.varpi_w
                Wnew = self.W * np.where(unprof, 0.8, np.clip(1 + (idx_u * wage_indexation * pi_ref + level + p.gamma_A * gA) / PERIODS_PER_YEAR, 0.9, 2.0))
            else:
                Wnew = self.W * np.where(unprof, 0.8, np.clip(1 + (idx_u * p.varpi_w * pi_ref + p.phi_u * (self.u_n - u) + tension + 0.1 * v + p.gamma_A * gA + ws_corr) / PERIODS_PER_YEAR, 0.9, 2.0))
            self._diag_w = dict(idx=idx_u * p.varpi_w * pi_ref, phil=p.phi_u * (self.u_n - u), tension=tension, vac=0.1 * v, prod=p.gamma_A * gA, excess_ld=self.excess_ld)   # diagnostic
            cashW = np.array([led.dep[f'F{j}'] for j in range(n)]) + 0.5 * self.p_ * self.Qbar
            W_payable = vfac * np.maximum(cashW, 1e-12) / ((1 + p.tauS) * np.maximum(self.L, 1e-6))   # salaire payable pour l'effectif courant
            self.W = np.minimum(Wnew, np.maximum(W_payable, 0.5 * self.W))
            self.u_n = max(self.u_n + p.eta_u * (u - self.u_n) + p.eta_u2 * (p.u_n - self.u_n), p.u_n_floor)   # plancher frictionnel : l'hystérèse ne peut pas effacer le chômage de rotation
            # Taylor
            # taux naturel estimé par la banque centrale : apprentissage (terme intégral) — si l'inflation reste sous la cible, le taux neutre estimé baisse
            self.rstar_est = update_natural_rate(self,u)
            rstar = self.rstar_est
            yhat = -p.okun * (u - (p.u_n if p.wsps2 else self.u_n))   # v2.0 : l'écart est mesuré au chômage STRUCTUREL u_n0, non au chômage naturel hystérétique (qui suit u et efface l'écart) — double mandat (Taylor 1993 ; Yellen 2012)
            pi_rule = p.w_rule * self.pi_s + (1 - p.w_rule) * self.pi
            pi_rule = (1 - p.w_fore) * pi_rule + p.w_fore * self.pi_e   # règle prospective : poids des anticipations
            i_target = max(rstar + min(self.pi_e, pi_rule + 0.5) + p.a_pi * (pi_rule - p.pi_star) + p.a_y * yhat + self.shock_i, 0.0)   # anticipations bornées ; shock_i : choc additif (tests)
            self._policy_components=dict(anchor=getattr(self,'_rstar_anchor',rstar),estimated=rstar,anticipated=min(self.pi_e,pi_rule+.5),inflation=p.a_pi*(pi_rule-p.pi_star),activity=p.a_y*yhat,shock=self.shock_i,target=i_target)
            self._last_target = i_target
            unsmoothed=sum(self._policy_components[k] for k in ("estimated","anticipated","inflation","activity","shock"))
            smoothed=p.rho_i*self.i_cb+(1-p.rho_i)*i_target
            self._policy_limits=dict(raw_target=float(unsmoothed),target_floor_binding=bool(unsmoothed<0),
                smoothed_target=float(smoothed),rate_ceiling_binding=bool(smoothed>p.i_max),
                rate_floor=0.,rate_ceiling=float(p.i_max),override_active=False)
            self.i_cb = min(smoothed, p.i_max)
            if self.pol_override is not None:
                ov = self.pol_override(self.t)
                if ov is not None:
                    self.i_cb = max(ov, 0.0)   # taux imposé (tests)
                    self._policy_limits["override_active"]=True
            self._policy_limits["applied_rate"]=float(self.i_cb)
            # prime & taux apparent
            b = self.B / max(Ynom * WEEKS, 1e-9)
            pb = -(deficit_w * WEEKS - ib * self.B * WEEKS) / max(Ynom * WEEKS, 1e-9)
            snow = (self.i_app - self.pi - p.g0) * b
            dbproj = snow - pb
            if p.spread_excl_cb:   # convexité sur la dette détenue hors banque centrale (évite le double comptage avec le rabais de QE), pondérée par la part non-résidente
                b_ex = (self.B - self.B_cb) / max(Ynom * WEEKS, 1e-9)
                frac_for = self.B_foreign / max(self.B - self.B_cb, 1e-9) if self.world is not None else (1 - p.kdom)
                chiK = float(self.world.chiK[self.idx]) if self.world is not None else p.chi_K
                kmin = p.kfor_min * (1 - chiK * p.rho_B)   # v1.5 : plancher conditionnel. Le plancher (risque de refinancement) suppose que l'épargne ait une sortie ; il tombe à zéro quand la détention est obligatoire (rho_B) ET la sortie fermée (chi_K)
                conv = p.s1 * max(kmin, frac_for) * max(b_ex / p.b_bar - 1, 0) ** 2
                prime = p.s0 * (1 - p.psi_qe * self.B_cb / max(self.B, 1e-9)) + conv + p.s2 * max(dbproj, 0) * 100 + p.s4 * (1 - self.cred) - p.s9 * p.rho_B   # -s9 rho_B : répression financière (épargnants captifs), déjà dans (44) du document, absente du prototype jusqu'en v1.5   # la prime de terme baisse avec la duration retirée du marché (canal de portefeuille), le risque de défaut porte sur B - B_cb
            else:
                prime = p.s0 + p.s1 * (1 - p.kdom) * max(b / p.b_bar - 1, 0) ** 2 + p.s2 * max(dbproj, 0) * 100 + p.s4 * (1 - self.cred) - (p.s7 * self.B_cb / max(self.B, 1e-9) if p.assets else 0.0)
            self.i_B = self.i_cb + min(prime, p.prime_max)
            theta = 1 / p.Tbar + max(deficit_w * WEEKS, 0) / max(self.B, 1e-9)
            self.i_app += min(theta, 1) / PERIODS_PER_YEAR * (self.i_B - self.i_app)
            # PGF
            g_pub,public_factor=public_productivity_feedback(self,Yreal*WEEKS)
            self._public_growth_add=float(g_pub)
            self._public_level_step=public_factor.copy()
            trend=1+(p.g0+g_pub)/PERIODS_PER_YEAR
            if p.tfp_trend_mode=='balanced_sectoral':
                # Experimental common labor-augmenting factor. With constant
                # sectoral K/Y and employment, log A_j must grow in proportion
                # to (1-alpha_j). g0 retains its mean-TFP interpretation to
                # first order; this is an explicit change of growth assumption.
                trend=(1+(p.g0+g_pub)/(PERIODS_PER_YEAR*(1-float(np.mean(p.alpha)))) )**(1-p.alpha)
            self.A *= (trend + self.shock_sd * self.rng.normal(0, 1, n) / np.sqrt(PERIODS_PER_YEAR))*public_factor
            self.A = np.maximum(self.A, 0.2 * self.A0)
        # ---------- 11. Historique ----------
        Qbar_old = self.Qbar.copy()
        self.Qbar = (1 - p.mu_ema) * self.Qbar + p.mu_ema * np.minimum(D, p.order_cap * (np.maximum(S, Ycap_full) if p.cap_on_capacity else S))   # les entreprises suivent les commandes reçues, dans la limite de leur capacité (et non de l'offre courante : sinon une pénurie s'auto-entretient)
        g_now = WEEKS * np.log(np.maximum(self.Qbar, 1e-9) / np.maximum(Qbar_old, 1e-9))
        self.g_orders = getattr(self, 'g_orders', np.full(n, p.g0)) * (1 - p.lam_g) + p.lam_g * g_now   # croissance anticipée des commandes (lissée, ~1 an)
        b = self.B / max(Ynom * WEEKS, 1e-9)
        # SoL
        sol = 0.0
        for h in range(3):
            xph = x_obt[h] / max(p.N[h], 1e-9) * WEEKS
            sol += p.N[h] * np.exp((p.beta_les[h] * np.log(np.maximum(xph - p.gamma[h], 1e-6) + 1e-6)).sum()) * (1 - 0.5 * u)
        sol /= p.N.sum()
        # services publics : le niveau de vie inclut la consommation publique effective par tête (rationnée par rhoG), avec une élasticité modeste
        g_eff = ((market['GC']+market['GI']) if self.world is not None else (G_cons*frac[2]+G_inv*frac[3]))/p.N.sum()*WEEKS
        if not hasattr(self, 'g_eff_ref'): self.g_eff_ref = max(g_eff, 1e-9)
        sol *= (max(g_eff, 1e-9) / self.g_eff_ref) ** p.omega_G
        self.sol_ref = 0.99 * getattr(self, 'sol_ref', sol) + 0.01 * sol
        for k, v in [("Y", Yreal * WEEKS), ("P", self.P_hist[-1] if self.P_hist else 1.0), ("pi", self.pi), ("u", u), ("i_cb", self.i_cb), ("i_B", self.i_B), ("i_app", self.i_app), ("b", b), ("cred", self.cred), ("pi_e", self.pi_e), ("M", self.money_supply()), ("K", self.K.sum()), ("q", q.mean()), ("SoL", sol), ("deficit", deficit_w * WEEKS / max(Ynom * WEEKS, 1e-9)), ("faillites", self.faillites), ("check", check), ("un", self.u_n), ("Ebank", self.E_bank), ("def_pct", (Ynom * WEEKS)), ("Mhist", self.M_hist), ("rhoG", self.rhoG), ("pZ", self.pZ), ("pE", self.pE), ("npl", self.npl_rate), ("LZ", self.LZ.sum()), ("Bcb", self.B_cb), ("Ecb", self.E_cb), ("runs", self.runs), ("rural", self.rural_pop), ("age_old", self.age[2] / max(self.age.sum(), 1e-9)), ("Rstock", self.R_stock / max(self.R_stock0, 1e-9)), ("s_surv", self.s_surv), ("fisc", getattr(self, "_fisc", 1.0))]:
            self.hist[k].append(v)
        self.hist_K.append(self.K.copy())
        eight.observe(self, "normal")
        self._flows.update(Y_potential=float(self._Ypotential_nominal/WEEKS),
            K_value=float(self.p_[3]*self.K.sum()), Z_replacement=float(self.p_[3]*self.Z.sum()),
            Z_market=float(self.pZ*self.Z.sum()), equity_market=self.equity_market_value(),
            P_food_relative=float(self.p_[0]/self.p_[2]), output_food=float(Y[0]),
            fiscal_factor=float(fisc), gov_purchase_plan=float(fisc*(p.G_share+p.Ginv_share)*Ynom_ref/WEEKS))
        self._flows["Y_market"]=self._flows["Y"]+self._flows["VAT"]+self._flows.get("tariffs",0.)
        f=self._flows
        bank_statement=reconcile(self)
        self.accounting=dict(goods=f["stock_residual"],
            bank_book_flow_residual=bank_statement["book_residual"],
            bank_claim_flow_residual=float(np.max(abs(bank_statement["household_claim_residual"]))),
            bank_issued_claim_residual=bank_statement["issued_claim_residual"],
            bank_public_claim_residual=bank_statement["public_claim_residual"],
            expenditure_residual=f["Y"]+f.get("tariffs",0.)-(f["C"]+f["I"]+f["G"]+f["IZ"]+f["inventories"]+f["EX"]-f["IM"]),
            central_bank=check,central_bank_raw=self._cb_numerics["raw_relative"],wage_shortfall=self._wage_shortfall,
            goods_payment_residual=self._goods_payment_residual,
            fiscal_residual=deficit_w-accrued_deficit,
            minimum_deposit=min(led.dep[k] for k in led.dep if k!="FX"),
            payment_shortfall=sum(a-b for _,_,a,b in led.shortfalls),
            capital_residual=float(np.max(np.abs(self.K-(K_start*(1-p.delta/WEEKS)+Igot-self._capital_loss)))))
        if self.p.bank_reconciliation_mode=='transaction_replay' and 'book_residual_raw_exact' in bank_statement:
            self.accounting.update(bank_book_raw_residual=bank_statement['book_residual_raw_exact'],
                bank_book_predicted_rounding=bank_statement['book_predicted_rounding'])
        # W10 : tolerance des identites de stock bancaire. L'ancien critere (1e-8 x Y hebdomadaire) est conserve
        # et exporte ; le critere 'stock_aware' ajoute n x eps x (somme des |operandes|), soit l'erreur d'arrondi
        # maximale d'une somme de n termes en double precision (Goldberg 1991, Higham 2002 §3.1).
        scale=max(abs(f["Y"]),1.)
        operands=abs(bank_statement["opening_book"])+abs(bank_statement["closing_book"])+sum(abs(x["book_flow"]) for x in bank_statement["flows"].values())
        stock_tol=p.residual_eps_multiple*np.finfo(float).eps*operands if p.residual_tolerance=='stock_aware' else 0.
        self.accounting.update(bank_identity_tolerance_legacy=1e-8*scale,bank_identity_tolerance_stock=stock_tol,
            bank_identity_operands=float(operands))
        if p.audit_strict:
            bank_tol=1e-8*scale+stock_tol
            assert abs(self.accounting["bank_book_flow_residual"])<bank_tol,self.accounting
            assert abs(self.accounting["bank_claim_flow_residual"])<bank_tol,self.accounting
            assert abs(self.accounting["bank_public_claim_residual"])<bank_tol,self.accounting
            assert abs(self.accounting["bank_issued_claim_residual"])<bank_tol,self.accounting
            assert self.accounting["goods"]<1e-8*scale, self.accounting
            assert abs(self.accounting["expenditure_residual"])<1e-8*scale,self.accounting
            assert check<1e-8,self.accounting
            assert abs(self.accounting["goods_payment_residual"])<1e-8*scale,self.accounting
            assert abs(self.accounting["fiscal_residual"])<1e-8*scale,self.accounting
            assert abs(self.accounting["capital_residual"])<1e-8*scale,self.accounting
            assert self.accounting["minimum_deposit"]>=-1e-8*scale,self.accounting
        self.flow_history.append(dict(t=t,**f))
        self.consumption_history.append(dict(t=t,E=E.copy(),Yd=Yd.copy(),
            r_net=np.array([h["r_net"] for h in self._hh_choices]),
            binding=np.array([h["binding"] for h in self._hh_choices]),
            feasible=np.array([h["feasible"] for h in self._hh_choices]),
            share=mix.copy()))
        if p.audit_corrections:
            audit.recovery(self)
            audit.after_week(self,Y,x_obt,price_target if p.wsps2 and p.price_mode=='markup' else cu*(1+self.markup))
        if self.P_hist and self.P_hist[-1]>p.P_redenom:
            self.redenominate(p.P_redenom)
            if not p.neutral_redenomination:self.M_hist+=1
            self.redenom+=1
        # ---------- machine à états : détection de l'effondrement ----------
        if p.collapse_machine and not self.collapsed:
            self.cap_weeks = self.cap_weeks + 1 if self.pi_e >= 0.99 * 12.0 else 0
            recent = [x for x in self.reform_times if self.t - x <= 5 * WEEKS]
            if self.cap_weeks >= p.collapse_weeks or len(recent) >= p.collapse_reforms:
                self.enter_collapse()
        if p.depression_detector: self.detect_depression()   # W10 (F39) : observation seule
        self.t += 1

    def detect_depression(self):
        """F39 : `collapsed` ne s'allume que sur les anticipations ou les reformes ; une depression reelle
        (PIB reel a 1e-8 de son niveau initial, sales_wacc/joint_mc W09) restait `collapsed=False`.
        Indicateur : PIB reel des 52 dernieres semaines < seuil x maximum des cinq annees precedentes,
        pendant depression_weeks semaines. Aucune retroaction sur le moteur."""
        p=self.p; y=self.hist.get('Y',[])
        if not hasattr(self,'depression_count'): self.depression_count=0; self.depressed=False; self.depression_t=None
        if len(y)<6*WEEKS: return
        recent=float(np.mean(y[-WEEKS:])); past=y[-6*WEEKS:-WEEKS]
        peak=max(float(np.mean(past[i:i+WEEKS])) for i in range(0,len(past)-WEEKS+1,WEEKS))
        low=recent<p.depression_threshold*peak
        self.depression_count=self.depression_count+1 if low else 0
        if not self.depressed and self.depression_count>=p.depression_weeks:
            self.depressed=True; self.depression_t=self.t
            self.events.append(dict(t=self.t,event='depression_detected',ratio=recent/max(peak,1e-30),collapsed=bool(self.collapsed)))
        elif self.depressed and self.depression_count==0 and recent>=p.depression_threshold*peak:
            self.depressed=False
            self.events.append(dict(t=self.t,event='depression_ended',ratio=recent/max(peak,1e-30)))


    # ---------- machine à états : économie effondrée ----------
    def enter_collapse(self):
        """Bascule en économie de survie : les échanges passent en unité stable, la production se replie sur une fraction du potentiel,
        le crédit et l'investissement s'arrêtent, les anticipations et l'indexation nominales cessent de faire sens. Sortie : réforme monétaire."""
        p = self.p
        if p.crisis_accounting=='continuous':
            from .audit_profile import enter_crisis
            return enter_crisis(self)
        self.events.append(dict(t=self.t,event="collapse_inventory_loss",finished=self.Sinv.tolist(),inputs=self.Xinv.tolist()))
        self.collapsed = True; self.collapses += 1; self.collapse_t = self.t; self.cap_weeks = 0
        Nact = self.active_pop(); LG = p.LG_share * Nact
        L0 = self.L / self.L.sum() if self.L.sum() > 1e-9 else np.ones(p.nsec) / p.nsec
        self.L = p.surv_util * (Nact - LG) * L0
        self.Sinv = np.zeros(p.nsec); self.Xinv = np.zeros((p.nsec, p.nsec)); self.zombie[:] = 0
        P = self.P_hist[-1] if self.P_hist else 1.0
        self.p_ = np.full(p.nsec, P); self.W = np.full(p.nsec, 0.3 * P)      # prix relatifs ramenés à une structure simple en unité stable
        A_eff = getattr(self, '_A_eff', self.A)
        self.Qbar = A_eff * self.K ** p.alpha * (self.H * self.L) ** (1 - p.alpha)
        self.pi_e = p.surv_pi; self.pi_s = p.surv_pi; self.pi = p.surv_pi
        self.cred = 0.0; self.i_cb = min(self.i_cb, 1.0)

    def survival_step(self):
        """Pas stylisé d'économie effondrée : production à surv_util du potentiel, échanges en unité stable, inflation résiduelle constante,
        salaires et prix indexés à l'identique, État payé et payant en unité stable, pas de crédit ni d'investissement net."""
        if eight.enabled(self): eight.enable(self)
        if self.p.crisis_accounting=='continuous':return self.step()
        p, n, led = self.p, self.p.nsec, self.led
        Nact = self.active_pop(); LG = p.LG_share * Nact
        self.K *= (1 - 0.5 * p.delta / WEEKS)                                     # entretien partiel seulement
        A_eff = getattr(self, '_A_eff', self.A)
        Y = A_eff * self.K ** p.alpha * (self.H * self.L) ** (1 - p.alpha)
        self.Qbar = Y
        g = (1 + p.surv_pi) ** (1 / WEEKS) - 1
        self.redenominate(1/(1+g), rescale_history=False, record=False)
        led.entries=[]; led.shortfalls=[]
        # Freeze the controller in survival, but keep the last effective rates.
        # A collapse is not an implicit cancellation of the tax adjustment.
        tauW_eff,_=income_tax_rates(self)
        rev = Y * self.p_; wages = self.W * self.L; pub = LG * self.W.mean() * 0.6
        for j in range(n):
            for h, s_ in enumerate(p.share_h):
                led.transfer(f'F{j}', f'H{h}', wages[j] * s_ * (1 - tauW_eff[h])); led.transfer(f'F{j}', 'G', wages[j] * s_ * tauW_eff[h])
        for h, s_ in enumerate(p.share_h): led.transfer('G', f'H{h}', pub * s_)
        for h in range(3):
            budget = 0.5 * max(led.dep[f'H{h}'], 0)
            for j in range(3): led.transfer(f'H{h}', f'F{j}', budget * rev[j] / max(rev[:3].sum(), 1e-9))
        led.transfer('G', 'F2', 0.9 * max(led.dep['G'], 0))
        if self.monetize > 0:                                                       # avances : l'inflation résiduelle monte avec la monétisation
            adv = self.monetize * (wages.sum() + pub); self.AG += adv; led.dep['G'] += adv; self.p_ *= (1 + self.monetize / 4)
        u = max(0.0, 1 - (self.L.sum() + LG) / Nact); Yreal = Y.sum() + LG
        Dtot = led.total()
        self.Res = Dtot + self.L_cb + self.E_bank - self.Loans.sum() - self.B_bank - ((self.LZ.sum() + self.LE) if p.assets else 0.0)
        if self.Res<0: self.L_cb-=self.Res; self.Res=0.
        check=central_bank_check(self)
        self.accounting={"central_bank":check,"minimum_deposit":min(led.dep.values()),"stylized_survival":True}
        if p.audit_strict and check>1e-8: raise AssertionError(self.accounting)
        if self.t % 4 == 0:
            self.P_hist.append(float(self.p_[:3].mean()))
            if len(self.P_hist) > int(PERIODS_PER_YEAR): self.pi = self.P_hist[-1] / self.P_hist[-1-int(PERIODS_PER_YEAR)] - 1
        self._Ynom_w = float(rev.sum() + pub)
        b = self.B / max(self._Ynom_w * WEEKS, 1e-9)
        sol = 0.4 * getattr(self, 'sol_ref', 1.0)
        for k, v in [("Y", Yreal * WEEKS), ("P", self.P_hist[-1] if self.P_hist else 1.0), ("pi", self.pi), ("u", u), ("i_cb", self.i_cb), ("i_B", self.i_B), ("i_app", self.i_app), ("b", b), ("cred", self.cred), ("pi_e", self.pi_e), ("M", self.money_supply()), ("K", self.K.sum()), ("q", 0.0), ("SoL", sol), ("deficit", 0.0), ("faillites", self.faillites), ("check", check), ("un", self.u_n), ("Ebank", self.E_bank), ("def_pct", (self._Ynom_w * WEEKS)), ("Mhist", self.M_hist), ("rhoG", 0.0), ("pZ", self.pZ), ("pE", self.pE), ("npl", self.npl_rate), ("LZ", self.LZ.sum()), ("Bcb", self.B_cb), ("Ecb", self.E_cb), ("runs", self.runs), ("rural", self.rural_pop), ("age_old", self.age[2] / max(self.age.sum(), 1e-9)), ("Rstock", self.R_stock / max(self.R_stock0, 1e-9)), ("s_surv", 1.0), ("fisc", 1.0)]:
            self.hist[k].append(v)
        self.hist_K.append(self.K.copy())
        eight.observe(self, "survival")
        self.flow_history.append(dict(t=self.t,regime="survival",Y=self._Ynom_w))
        self.consumption_history.append(dict(t=self.t,regime="survival"))
        if self.P_hist and self.P_hist[-1]>p.P_redenom:
            self.redenominate(p.P_redenom); self.M_hist+=1; self.redenom+=1
        self.t += 1

    def exit_collapse(self):
        """Sortie de l'économie de survie après une réforme : stocks nominaux cohérents, production redémarrant au niveau courant,
        trésorerie de redémarrage, banque recapitalisée au minimum réglementaire, anticipations remises près de la cible."""
        if self.p.crisis_accounting=='continuous':
            raise ValueError('Recovery is observed over time; no instantaneous crisis reset')
        if eight.enabled(self):
            raise NotImplementedError('Legacy unfunded restart is disabled in the eight-point profile')
        p = self.p
        self.collapsed = False
        old_cb=self.E_cb; old_deposits=self.led.total()
        self.events.append(dict(t=self.t,event="restart_goods_endowment",finished=(4*self.Qbar).tolist(),inputs=(8*p.a*self.Qbar[None,:]).tolist()))
        self.Sinv = 4 * self.Qbar; self.Pi_brut_bar = 0.1 * (self.Qbar * self.p_)
        self.Xinv = 8 * p.a * self.Qbar[None, :]          # stocks d'intrants de redémarrage (huit semaines)
        self.div_last = np.zeros(p.nsec); self.div_bank_last = 0.0
        # v1.6 : les profits lissés hérités de l'hyperinflation (unité ancienne) sont réinitialisés dans l'unité courante, sinon ils commandent des dividendes égaux à toute la trésorerie de redémarrage (boom puis rechute) ; règle de la v1.3 : tout stock nominal de référence est réinitialisé à la sortie
        self.Pi_brut_bar = p.alpha * self.p_ * self.Qbar   # profit brut hebdomadaire de référence : part du capital dans la production de redémarrage
        self.Pi_net_bar = np.zeros(p.nsec)                          # pas de dividende avant que des profits nets se reconstituent
        if hasattr(self, 'm_norm'): del self.m_norm                 # v1.6 : la norme d'encaisses est réinitialisée dans l'unité nouvelle (elle mesure la fuite passée, pas la référence future)
        if hasattr(self,"Yperm_real"): del self.Yperm_real
        self.Yperm = 0.75 * self._Ynom_w * np.array([0.5, 0.3, 0.2])   # revenu permanent remis au niveau courant (l'EMA héritée de l'hyperinflation est sans signification)
        for j in range(p.nsec): self.led.dep[f'F{j}'] = 8 * (self.W[j] * self.L[j] * (1 + p.tauS) + (p.a[:, j] * self.Qbar[j] * self.p_).sum())   # trésorerie de redémarrage : huit semaines de charges ; l'excédent thésaurisé pendant la survie est annulé
        self.zombie[:] = 0; self.rhoG = 1.0; self.cap_weeks = 0
        self.pi = p.pi_star + 0.05; self.pi_s = self.pi; self.pi_e = self.pi
        if self.E_bank < p.kappa_CAR * self.Loans.sum(): change_book(self,1.3*p.kappa_CAR*max(self.Loans.sum(),0.05*self._Ynom_w*WEEKS)-self.E_bank,'explicit_reform_endowment')
        self.rstar_est = p.rho + p.sigma * p.g0
        if p.assets:   # prix d'actifs remis à leur valeur de référence dans la nouvelle unité
            self.pZ = 1.5 * self._Ynom_w * WEEKS / max(self.Z.sum(), 1e-9); self.pE = 1.0; self.pZ_hist = []; self.pE_hist = []; self.equity_value_hist = []
            self.gZ_e = p.g0; self.gE_e = p.g0; self.pZ_3y = self.pZ
            if hasattr(self, 'zeta_cal'): del self.zeta_cal
            if hasattr(self, 'sE_cal'): del self.sE_cal
        # conversion monétaire : la nouvelle monnaie est émise pour rétablir des encaisses de transaction (M/PIB = 0,8) contre avances au Trésor
        Y_ann = self._Ynom_w * WEEKS; M_now = self.money_supply(); M_tgt = p.M_conv * Y_ann
        if M_now < M_tgt:
            add = M_tgt - M_now
            for h, s_ in enumerate((0.35, 0.35, 0.30)): self.led.dep[f'H{h}'] += add * s_        # la nouvelle monnaie est distribuée aux ménages (conversion)
            self.AG += add; self.AG_free += add   # contrepartie : avances de la banque centrale au Trésor (émission de la nouvelle monnaie) ; sans intérêt (v1.6)
        self.Res = self.led.total() + self.L_cb + self.E_bank - self.Loans.sum() - self.B_bank - ((self.LZ.sum() + self.LE) if p.assets else 0.0)
        if self.Res<0: self.L_cb-=self.Res; self.Res=0.
        self.E_cb = self.B_cb + self.AG + self.L_cb + self.led.dep['FX'] + self.e * self.R_fx - self.Res - self.cash_out
        self.events.append(dict(t=self.t,event="restart_conversion",central_bank_equity_change=float(self.E_cb-old_cb),deposits_change=float(self.led.total()-old_deposits)))


    # ---------- étape 4 : hétérogénéité ----------
    def active_pop(self):
        p = self.p
        if p.cohorts:
            act = p.participation / p.age_share0[1] * self.age[1]        # participation rapportée à la cohorte active
        else:
            act = p.participation * p.N.sum()
        return max(act-(self.rural_pop if p.rural and hasattr(self,"rural_pop") else 0.),1.)   # les migrants ruraux rejoignent le marché du travail urbain

    def hetero_block(self, u, Y_fn=None):
        """cohortes (naissances, vieillissement, décès), migration rurale (Lewis), climat, ressource"""
        p = self.p; month = (self.t % 4 == 0)
        if p.cohorts and month:
            young, act, old = self.age
            sol_rel = max(getattr(self, 'sol_ref', 1.0) / max(getattr(self, 'sol_ref0', getattr(self, 'sol_ref', 1.0)), 1e-9), 0.1)
            if not hasattr(self, 'sol_ref0') and hasattr(self, 'sol_ref'): self.sol_ref0 = self.sol_ref
            f_b = sol_rel ** (-p.eta_fert) if p.fert_endo else 1.0          # transition démographique : la fécondité baisse avec le niveau de vie
            f_m = sol_rel ** (-p.eta_mort) if p.fert_endo else 1.0          # la mortalité des âgés baisse avec le niveau de vie (santé)
            births = f_b * p.birth / PERIODS_PER_YEAR * act; to_act = young / (20 * PERIODS_PER_YEAR); to_old = act / (45 * PERIODS_PER_YEAR); deaths = f_m * old / (18 * PERIODS_PER_YEAR)
            self.age = np.array([young + births - to_act, act + to_act - to_old, old + to_old - deaths])
            p.N*=self.age.sum()/p.N.sum()
        if p.rural and month:
            # Lewis : les ruraux migrent si le salaire urbain espéré (1-u) x W dépasse le revenu rural plus le coût
            Wbar = (self.W * self.L).sum() / max(self.L.sum(), 1e-9)
            w_rural = p.w_rural_rel * Wbar * (self.rural_pop0 / max(self.rural_pop, 1e-9)) ** 0.3 if hasattr(self, 'rural_pop0') else p.w_rural_rel * Wbar
            gain = (1 - u) * Wbar / max(w_rural, 1e-9) - 1 - p.mig_cost
            flow = p.mig_speed / PERIODS_PER_YEAR * gain * self.rural_pop if gain > 0 else 0.0
            self.rural_pop = max(self.rural_pop - flow, 0.0)
            # la production rurale (autoconsommation) accroît l'offre alimentaire et le revenu de la strate basse
            self.rural_output = w_rural * self.rural_pop / max(self.p_[0], 1e-9)
        if p.weather_sd > 0 and self.t % WEEKS == 0:
            self.weather = float(np.clip(1 + p.weather_sd * self.rng.normal(), 0.5, 1.3))
        # L'extraction est enregistrée sur la production effective dans _step_normal.

    # ---------- étape 3 : actifs ----------
    def potential_output_nominal(self, A_eff=None, Nact=None, LG=None, Wbar=None):
        """VA annuelle aux facteurs présents et au chômage structurel.

        Le travail privé est réparti selon les parts d'emploi actuelles ; la
        multiplication par l'emploi total potentiel retire le creux conjoncturel.
        Les intrants techniques sont retranchés de la production brute. Ce potentiel
        conditionnel n'est ni une trajectoire exogène ni une optimisation multisectorielle.
        """
        p=self.p
        A_eff=getattr(self,"_A_eff",self.A) if A_eff is None else A_eff
        Nact=self.active_pop() if Nact is None else Nact
        LG=p.LG_share*Nact if LG is None else LG
        Wbar=float(self.W@self.L/max(self.L.sum(),1e-9)) if Wbar is None else Wbar
        labor=max(Nact*(1-p.u_n)-LG,0.)*self.L/max(self.L.sum(),1e-9)
        gross=A_eff*self.K**p.alpha*(self.H*labor)**(1-p.alpha)
        va_price=self.p_-(p.a*self.p_[:,None]).sum(axis=0)
        return max(float(va_price@gross+LG*Wbar)*WEEKS,1e-9)

    def housing_orders(self, pK):
        """Commandes brutes avant financement, en logements par semaine.

        À q/q0=1, remplacement ; sous le coût, le parc peut décroître.
        Le seuil q0 est fixe : une longue baisse de valeur ne doit pas devenir
        automatiquement une nouvelle rentabilité normale. Aucun terme de PGF
        n'impose une croissance du parc indépendamment de la demande.
        """
        p=self.p; q=self.pZ/pK
        if p.build_norm:
            q0=self.housing_q0
            gross_rate=float(np.clip(p.delta_Z+p.nu_build*(q/q0-1),0.,p.delta_Z*(1+p.build_cap)))
        else:  # variante historique de sensibilité, sans croissance forcée
            gross_rate=p.delta_Z*(1+min(p.nu_build*max(q-1,0)/p.delta_Z,p.build_cap))
        self._housing_signal=dict(q=q,q0=self.housing_q0,gross_rate=gross_rate,net_rate=gross_rate-p.delta_Z)
        return self.Z.sum()*gross_rate/WEEKS

    def equity_book(self):
        """valeur comptable des entreprises (capital au prix courant moins dettes, plus trésorerie)"""
        return max((self.K*self.capital_price()).sum()+(self.Sinv*self.p_).sum()+(self.Xinv*self.p_[:,None]).sum()-self.Loans.sum()+sum(self.led.dep[f"F{j}"] for j in range(self.p.nsec)),1e-6*(float(self.p_.mean()) if eight.enabled(self) else 1.))

    def equity_market_value(self):
        if self.p.equity_valuation_mode=='market_quote':return float(self._equity_quote)
        return float(self.pE*self.equity_book())

    def equity_ownership(self):
        return getattr(self,'_equity_shares',self.p.omega)

    def capital_price(self):
        return self.world.capital_prices[self.idx] if self.world is not None else self.p_[3]

    def housing_block(self, Yd, pK):
        """prix immobilier : rendement attendu (loyer implicite + plus-value extrapolée) contre coût d'usage ; construction ; crédit hypothécaire.
        Retourne les unités de logements neufs commandées au secteur de la construction."""
        p = self.p
        iZ = self.i_L()
        uc = (1+iZ)/(1+self.pi_e)-1 + p.delta_Z + p.rho_Z                                 # coût d'usage hors plus-value
        uc0 = p.rho + p.sigma * p.g0 + p.mL + p.delta_Z + p.rho_Z                 # coût d'usage de référence (état stationnaire, taux réel neutre)
        if not hasattr(self, 'zeta_cal'):                                         # loyers implicites calibrés : rendement locatif initial = coût d'usage - plus-value tendancielle
            self.zeta_cal = (uc0 - p.g0) * self.pZ * self.Z / np.maximum(Yd * WEEKS, 1e-9)   # rendement locatif initial = coût d'usage réel - plus-value réelle tendancielle
        rent_yield = (self.zeta_cal * np.maximum(Yd,0.) * WEEKS).sum() / max(self.pZ * self.Z.sum(), 1e-9)
        pZ_fund = (self.zeta_cal * np.maximum(Yd,0.) * WEEKS).sum() / max(self.Z.sum() * max(uc - p.g0, 0.01), 1e-9)   # valeur fondamentale : loyers actualisés au coût d'usage réel net de la croissance
        excess = rent_yield + self.gZ_e - uc - p.psi_fund * np.log(self.pZ / max(pZ_fund,1e-9))   # rendement attendu moins coût, rappel vers la valeur fondamentale
        ltv_boost = 0.5 * (p.LTV - 0.8)                                           # un crédit plus facile élève la demande
        self.pZ = max(self.pZ * float(np.clip(1 + p.kappa_pz * (excess + ltv_boost) + self.pi_e / WEEKS, 0.9, 1.1)), 1e-6)   # excès de rendement réel répercuté, plus dérive nominale
        # construction : remplacement plus réponse des promoteurs au prix relatif ; livrée après T_Z semaines
        deliv = self.pipeline[0]
        new_units = self.housing_orders(pK)
        self._IZ_share = np.array([0.35, 0.35, 0.30])
        desired=new_units*pK*self._IZ_share
        funded=np.zeros(3); self._IZ_loan=np.zeros(3); room=self.credit_room()
        self._IZ_contracts=[None]*3
        for h in range(3):
            cash=max(self.led.dep[f"H{h}"]-self._E_plan[h],0.)
            cap_h=mortgages.capacity(self,h,Yd[h],iZ) if eight.enabled(self) else max(p.mortgage_service_share*max(Yd[h],0.)*WEEKS/max(iZ+p.mortgage_amortization,1e-6)-self.LZ[h],0.)
            loan_cap=min(cap_h,room) if not self.bank_failed else 0.
            amount=min(desired[h],cash+min(p.LTV*desired[h],loan_cap),cash/max(1-p.LTV,1e-9))
            loan=min(p.LTV*amount,loan_cap)
            funded[h]=amount; room-=loan; self._IZ_loan[h]=loan
            if eight.enabled(self): self._IZ_contracts[h]=mortgages.originate(self,h,loan,"construction",collateral_value=amount)
            self.LZ[h]+=loan; self.led.dep[f"H{h}"]+=loan
        self._IZ_share=funded/max(funded.sum(),1e-12)
        new_units=funded.sum()/pK
        # Refinancement du parc ; les remboursements préservent consommation et commandes.
        target=p.lev_mort*(p.LTV/.8)*self.pZ*self.Z
        self._refi_mortgage=np.zeros(3)
        for h in range(3):
            d=.10/WEEKS*(target[h]-self.LZ[h])
            if eight.enabled(self): d=max(d,0.)  # new LTV cannot accelerate old contracts
            if d>0 and not p.mortgage_refinancing:d=0.
            if d>0:
                cap_h=mortgages.capacity(self,h,Yd[h],iZ) if eight.enabled(self) else max(p.mortgage_service_share*max(Yd[h],0.)*WEEKS/max(iZ+p.mortgage_amortization,1e-6)-self.LZ[h],0.)
                if p.mortgage_registry:cap_h=min(cap_h,mortgages.unpledged_capacity(self,h))
                d=min(d,cap_h,room) if not self.bank_failed else 0.; room-=d
            else: d=-min(-d,max(self.led.dep[f"H{h}"]-self._E_plan[h]-funded[h],0.))
            if eight.enabled(self): mortgages.originate(self,h,d,"refinancing")
            self.LZ[h]+=d; self.led.dep[f"H{h}"]+=d
            self._refi_mortgage[h]=d
        # stock : livraisons moins dépréciation ; pression de l'offre nouvelle sur le prix
        self.Z = self.Z * (1 - p.delta_Z / WEEKS) + self.pipeline_h[0]
        self.pZ *= float(np.clip(1 - p.kappa_sup * (deliv - p.delta_Z / WEEKS * self.Z.sum()) / max(p.delta_Z * self.Z.sum() / WEEKS, 1e-9), 0.9, 1.1))   # l'offre nouvelle pèse sur le prix
        self.pipeline_h=np.roll(self.pipeline_h,-1,axis=0); self.pipeline_h[-1]=0.
        self.pipeline=self.pipeline_h.sum(axis=1)
        return float(new_units)

    def pay_household_debt(self):
        """Paiements effectifs réservés avant la consommation ; défauts dans assets_block."""
        p=self.p; rate=wk(self.i_L()); margin_debt=self.LE
        for h in range(3):
            due=rate*(self.LZ[h]+margin_debt*p.omega[h])
            paid=min(due,max(self.led.dep[f"H{h}"],0.))
            self.led.dep[f"H{h}"]-=paid; change_book(self,paid,'household_interest_paid')
            self._hh_debt_interest[h]=paid
            # Arriéré capitalisé, distinct du revenu effectivement reçu.
            unpaid=due-paid
            mortgage_due=rate*self.LZ[h]
            # An absent margin contract cannot acquire arrears through a
            # subtraction of nearly equal floating-point mortgage amounts.
            mortgage_unpaid=unpaid if p.audit_corrections and margin_debt==0. else unpaid*mortgage_due/max(due,1e-12)
            if eight.enabled(self): mortgages.capitalize(self,h,mortgage_unpaid)
            self.LZ[h]+=mortgage_unpaid; self.LE+=unpaid-mortgage_unpaid
            change_book(self,unpaid,'household_interest_capitalized')
            amort=mortgages.scheduled_payment(self,h,self.led.dep[f"H{h}"]) if eight.enabled(self) else min(p.mortgage_amortization/WEEKS*self.LZ[h],max(self.led.dep[f"H{h}"],0.))
            self.led.dep[f"H{h}"]-=amort; self.LZ[h]-=amort
            self._hh_debt_amort[h]=amort

    def assets_block(self, Ynom_prev, month):
        """intérêts hypothécaires, défauts, prix des actions, anticipations, ruées bancaires"""
        p = self.p; led = self.led
        # défauts : prêts récents (30 % de l'encours, ~3 ans) originés à la quotité LTV sur le prix moyen des 3 dernières années ;
        # ils sont sous l'eau quand le prix courant passe sous LTV x prix d'origine
        self.pZ_3y = getattr(self, 'pZ_3y', self.pZ) + (self.pZ - getattr(self, 'pZ_3y', self.pZ)) / (3 * WEEKS)
        under_frac = float(np.clip((p.LTV * self.pZ_3y - self.pZ) / max(p.LTV * self.pZ_3y, 1e-9), 0, 1))
        under = 0.30 * self.LZ * under_frac
        loss = mortgages.defaults(self) if eight.enabled(self) else (p.phi_npl / WEEKS) * under
        self.LZ -= loss; change_book(self,-loss.sum(),'mortgage_default_loss'); self.NPL_Z = loss.sum()
        self.npl_rate = 0.95 * self.npl_rate + 0.05 * (loss.sum() * WEEKS / max(self.LZ.sum() + self.Loans.sum(), 1e-9))
        # actions : rendement attendu vs richesse désirée
        book = self.equity_book(); div_yield = self.div_last.sum() * WEEKS / max(self.equity_market_value(), 1e-9)
        rE = div_yield + self.gE_e
        rreq = (1+self.i_B)/(1+self.pi_e)-1 + p.rho_E
        V = np.array([led.dep[f'H{h}'] for h in range(3)]) + self.Bh + self.pZ * self.Z - self.LZ + (self.equity_market_value()*self.equity_ownership() if p.equity_valuation_mode=='market_quote' else self.pE * self.equity_ownership() * book)
        if p.wealth_net_debt:V=V-p.omega*self.LE
        have = self.equity_market_value()
        if not hasattr(self, 'sE_cal'):   # calibration : la répartition initiale est désirée
            base = (p.sE * V).sum() * (1 + p.margin * 0.5); self.sE_cal = p.sE * have / max(base, 1e-9); self.rE0 = rE - rreq
        desired = (self.sE_cal * (1 + 3 * (rE - rreq - self.rE0))).clip(0, 0.9)   # part de richesse désirée en actions
        want = (desired * V).sum() * (1 + p.margin * 0.5)                          # les prêts sur marge amplifient la demande
        if p.equity_fund:   # rappel vers la valeur fondamentale : dividendes actualisés au rendement requis net de la croissance
            pE_fund = (self.div_last.sum() * WEEKS) / max(max(rreq - p.g0, 0.03) * book, 1e-9)   # taux d'actualisation plancher 3 % : la valeur fondamentale reste finie à taux zéro
            want = want * np.exp(float(np.clip(-p.psi_fundE * np.log(max(self.pE, 1e-9) / max(pE_fund, 1e-9)) * 0.1, -0.2, 0.2)))
        if p.portfolio_mode=='joint_equity':
            # The call-auction price was cum-dividend; detach the dividend
            # actually distributed at this close, keeping the quote per share.
            if p.equity_valuation_mode=='market_quote':
                from .equity_quote import detach_dividends
                self.pE=detach_dividends(self,self._equity_market_value,float(self.div_last.sum()))/book
            else:self.pE=max(self._equity_market_value-float(self.div_last.sum()),1e-6)/book
        else:
            self.pE = max(self.pE * float(np.clip(1 + p.kappa_pe * (want - have) / max(want + have, 1e-9), 0.8, 1.25)), 1e-6)
        # prêts sur marge : la banque finance une part 'margin' des portefeuilles d'actions ; les appels de marge et les pertes suivent le cours
        LE_target = (p.margin*p.margin_base*self.equity_market_value() if p.equity_valuation_mode=='market_quote' else p.margin * p.margin_base * self.pE * book)       # prêts sur marge : quelques % de la capitalisation
        room = max(self.E_bank / p.kappa_CAR - self.Loans.sum() - self.LZ.sum() - self.LE, 0) if (self.E_bank > 0 and not self.bank_failed) else 0.0
        LE_target = min(LE_target, self.LE + room)
        dLE = 0.1 * (LE_target - self.LE)
        if dLE>0 and not p.margin_refinancing:dLE=0.
        if dLE > 0 and (self.E_bank <= 0 or self.bank_failed): dLE = 0.0
        if dLE < 0:   # remboursement borné par les dépôts disponibles
            dLE = -min(-dLE, sum(max(led.dep[f'H{h}'], 0) * s_ for h, s_ in enumerate(p.omega)))
        if dLE < 0: dLE = -min(-dLE, min(max(led.dep[f'H{h}'], 0) / s_ for h, s_ in enumerate(p.omega) if s_>0))   # remboursement borné par le dépôt de chaque strate
        self.LE += dLE
        self._refi_margin=float(dLE)
        for h, s_ in enumerate(p.omega): led.dep[f'H{h}'] += dLE * s_          # credit and debt service use the same ownership shares
        under_E = max(self.LE - (0.9*p.margin_base*self.equity_market_value()*(1+p.margin) if p.equity_valuation_mode=='market_quote' else 0.9 * p.margin_base * self.pE * book * (1 + p.margin)), 0)   # collatéral insuffisant (après baisse du cours)
        lossE = min(under_E * 0.5, self.LE); self.LE -= lossE; change_book(self,-lossE,'margin_default_loss')
        self.npl_rate = 0.95 * self.npl_rate + 0.05 * (lossE * WEEKS / max(self.LZ.sum() + self.Loans.sum() + self.LE, 1e-9))
        if month:
            self.pZ_hist.append(self.pZ); self.pE_hist.append(self.pE)
            self.equity_value_hist.append(self.equity_market_value())
            if len(self.pZ_hist) > int(PERIODS_PER_YEAR):
                gZ = self.pZ_hist[-1] / self.pZ_hist[-1-int(PERIODS_PER_YEAR)] - 1; gE = self.equity_value_hist[-1] / self.equity_value_hist[-1-int(PERIODS_PER_YEAR)] - 1
                self.gZ_e = (1 - p.chi_Z) * p.g0 + p.chi_Z * float(np.clip((1+gZ)/(1+self.pi)-1, -0.5, 1.0))   # plus-value réelle extrapolée
                self.gE_e = (1 - p.chi_E) * p.g0 + p.chi_E * float(np.clip((1+gE)/(1+self.pi)-1, -0.5, 1.0))
            # ruées : probabilité croissante avec les créances douteuses et l'insuffisance de fonds propres, décroissante avec la garantie
            from math import erf, sqrt
            D = led.total()
            z = p.run_s1 * (self.npl_rate - 0.01) + p.run_s2 * max(-self.E_bank, 0) / max(D, 1e-9) - p.run_s3 * (1 if p.deposit_insurance else 0) - 1.5
            prob = 0.5 * (1 + erf(z / sqrt(2)))
            if not p.deposit_insurance and prob > 0.05 and not self.bank_failed:
                desired=np.array([min(prob,.5)*max(led.dep[f"H{h}"],0.) for h in range(3)])
                liquid=max(led.total()+self.L_cb+self.E_bank-self.Loans.sum()-self.B_bank-self.LZ.sum()-self.LE,0.)
                refi_cap=max(p.gold_cap*self.money_supply()-self.L_cb,0.) if p.gold_cap is not None else np.inf
                allowed=min(desired.sum(),liquid+refi_cap)
                self.L_cb+=max(allowed-liquid,0.)
                out=desired*allowed/max(desired.sum(),1e-12)
                for h in range(3): led.dep[f"H{h}"]-=out[h]
                self.cash_h+=out; self.cash_out=float(self.cash_h.sum()); self.runs+=1
                if allowed+1e-9<desired.sum():
                    self.bank_failed=True; self.cred=max(self.cred-.2,.05)
            if self.bank_failed and self.E_bank > 0 and self.npl_rate < 0.01: self.bank_failed = False
            # retour de la monnaie thésaurisée quand le calme revient
            if self.cash_out > 0 and prob < 0.02:
                back=.1*self.cash_h; self.cash_h-=back; self.cash_out=float(self.cash_h.sum())
                for h in range(3): led.dep[f'H{h}']+=back[h]

    def reform(self):
        """Réforme monétaire : nouvelle unité, arrêt des avances, remise à zéro des anticipations ; la mémoire M_hist plafonne la crédibilité future."""
        if self.world is not None:
            raise NotImplementedError('Réforme monétaire internationale hors périmètre du prototype')
        if eight.enabled(self):
            return eight.monetary_reform(self)
        self.monetize = 0.0
        for name in ("Yperm_real","q_bar","Pi_net_bar","Pi_marginal_bar","r_long","g_orders"):
            if hasattr(self,name): delattr(self,name)
        self.M_hist += 1
        if hasattr(self, 'm_norm'): del self.m_norm   # v1.6
        self.reform_times.append(self.t)
        if self.collapsed: self.exit_collapse()
        if self.P_hist and self.P_hist[-1]>1e3:
            self.redenominate(self.P_hist[-1])
        self.pi_e = self.p.pi_star + 0.05
        self.pi_s = self.p.pi_star + 0.05
        self.cred = max(1 - self.p.nu9 * self.M_hist, self.p.cred_floor) * 0.8
        self.rstar_est = self.p.rho + self.p.sigma * self.p.g0
        self.i_cb = self.rstar_est + self.pi_e   # nouveau régime : taux ramené au neutre
        cons = max(self.AG - self.AG_free, 0.0)
        if self.p.assets and self.p.adv_interest and cons > 0:   # v1.6 : consolidation des avances (hors conversion) en dette publique détenue par la BC, coupon au taux POST-réforme (le coupon pré-réforme, 90 %, relançait la spirale : C2 sous calibrage B) ; le stock ne se capitalise plus, et il compte dans b
            coupon = self.i_cb + self.p.mL
            self.cbar_cb = (self.cbar_cb * self.B_cb + coupon * cons) / max(self.B_cb + cons, 1e-9)
            self.B_cb += cons; self.B += cons; self.AG -= cons
        self.i_app = min(self.i_app, self.i_cb + 0.05)

    def redenominate(self, factor, rescale_history=True, record=True):
        """Divise l'unité nominale par factor ; pE est un ratio et reste inchangé.

        Les quantités, Yperm_real, la base de consommation, W_public_base et
        la tendance réelle publique restent dans leurs unités réelles d'origine.
        rescale_history=False est réservé à l'indexation stylisée de survie.
        """
        if not np.isfinite(factor) or factor<=0: raise ValueError("Facteur monétaire invalide")
        if self.p.neutral_redenomination:
            self._audit_unit=getattr(self,'_audit_unit',1.)/factor
            for agreement in getattr(self,'wage_agreements',[]):agreement['nominal_paid']/=factor
            for name in ('_agreement_paid','_agreement_due'):
                if hasattr(self,name):setattr(self,name,getattr(self,name)/factor)
            # Audit history is immutable and carries its observation's unit.
        for name in ("p_","W","Bh","Loans","B_bank","B_cb","AG","AG_free","B",
                     "B_foreign","E_bank","E_cb","E_cb0","E_cb_check","Res","L_cb",
                     "LZ","LE","pZ","pZ_3y","cash_h","cash_out","recap","e",
                     "Pi_brut_bar","Pi_net_bar","Pi_marginal_bar","_mpk_profit_bar","div_last","div_bank_last",
                     "_bank_dividends_last","_bank_issue_last",
                     "Yperm","_M_prev","_Ynom_w","_pK_repl","_tax_prev","M_G_prev",
                     "_output_prices","_Ypotential_nominal","_equity_market_value","_equity_quote"):
            if hasattr(self,name): setattr(self,name,getattr(self,name)/factor)
        for key in self.led.dep: self.led.dep[key]/=factor
        if hasattr(self,'_joint_diag'):
            self._joint_diag['price']/=factor
            for key in ('fees','trades'):self._joint_diag[key]=(np.asarray(self._joint_diag[key])/factor).tolist()
        if hasattr(self,'_joint_margin_repayment'):self._joint_margin_repayment/=factor
        redenominate_journal(self,factor)
        if eight.enabled(self):
            mortgages.redenominate(self,factor)
            if hasattr(self,"resolution_actions"):
                from .workplan import redenominate
                redenominate(self,factor)
            if hasattr(self,"_bank_public_dividend"): self._bank_public_dividend/=factor
            if hasattr(self,"_mortgage_residual"): self._mortgage_residual/=factor
        if hasattr(self,'_capital_diag') and 'expected_tax_base' in self._capital_diag:
            self._capital_diag['expected_tax_base']/=factor
        if rescale_history:
            self.P_hist=[x/factor for x in self.P_hist]
            self.pZ_hist=[x/factor for x in self.pZ_hist]
            self.equity_value_hist=[x/factor for x in self.equity_value_hist]
            for key in ("P","M","Ebank","def_pct","pZ","LZ","Bcb","Ecb"):
                self.hist[key]=[x/factor for x in self.hist[key]]
            for row in self.flow_history:
                for key in ("C","VAT","I","G","IZ","inventories","EX","IM","Y","Y_market","deficit","deficit_from_flows","debt_total","Y_potential","K_value","Z_replacement","Z_market","equity_market","gov_purchase_plan","tariffs","treasury_cash","treasury_target","treasury_dividend","redemption_households","redemption_bank","redemption_cb","redemption_advances","redemption_total","household_taxes","household_tax_base"):
                    if key in row: row[key]/=factor
            for row in self.consumption_history:
                for key in ("E","Yd"):
                    if key in row: row[key]/=factor
            for key in ("expenditure_residual","goods_payment_residual","fiscal_residual","wage_shortfall","minimum_deposit","payment_shortfall","bank_book_flow_residual","bank_claim_flow_residual","bank_issued_claim_residual","bank_public_claim_residual","bank_book_raw_residual","bank_book_predicted_rounding"):
                if key in self.accounting: self.accounting[key]/=factor
        if record: self.events.append(dict(t=self.t,event="redenomination",factor=float(factor)))

    @staticmethod
    def solve_init(p, n_iter=8, verbose=False):
        """v2.0 : point fixe de l'état initial sur le marché des biens — ajuste d_scale jusqu'à ce que l'excès de demande de la première semaine soit nul."""
        import copy
        for k in range(n_iter):
            e = Economy(p); e._last_target = e.i_cb; e.step()
            z0 = e._diag_p["z"]
            if verbose: print("  itération", k, "z0", np.round(z0, 4), "d_scale", np.round(p.d_scale, 4))
            if np.abs(z0).max() < 1e-3: break
            p.d_scale = p.d_scale * (1 + z0) / (1 - z0)
        return p

    def Y_nom_prev(self):
        return self._Ynom_w * WEEKS

    def Sinv_prev(self): return self.Sinv

    def i_L(self):
        ell = self.Loans.sum() / max((self.capital_price() * self.K).sum(), 1e-9)
        return self.i_cb + self.p.mL + self.p.rho1 * max(ell - self.p.ell_bar, 0)

    def Lam_bank(self):
        return float(np.clip(self.credit_room()/max(.1*self.Loans.sum(),1e-9),0,1))

    def credit_room(self):
        debt=self.Loans.sum()+((self.LZ.sum()+self.LE) if self.p.assets else 0.)
        return max(self.E_bank/self.p.kappa_CAR-debt,0.) if self.E_bank>0 and not self.bank_failed else 0.

    def run(self, years, quiet=True):
        for _ in range(int(years * WEEKS)):
            self.step()
        return {k: np.array(v) for k, v in self.hist.items()}
