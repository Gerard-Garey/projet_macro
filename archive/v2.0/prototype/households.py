"""Choix intertemporel CRRA sous contrainte de liquidité, en unités réelles.

Convention : a[t+1] = R[t] * (a[t] + y[t] - subs[t] - c[t]).
c est le composite supernuméraire Stone-Geary, R le rendement réel NET.
Les revenus y excluent les intérêts déjà portés par R. Les ressources de t=0
peuvent être fournies dans a0 après paiement du revenu courant (alors y[0]=0).
Le taux rho est continu annuel ; dt est la durée d'une période en années.
Le choix courant minimise les plafonds budgétaires de tous les préfixes :
Euler sur un segment intérieur, a=0 à la première contrainte rencontrée.
"""
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class ConsumptionChoice:
    surplus: float
    binding_period: int
    unconstrained_surplus: float
    feasible: bool


def initial_consumption(a0, income, gross_returns, sigma=1., rho=.01,
                        dt=1/52, subsistence=None, terminal_assets=0.):
    """Premier choix de l'optimum déterministe à horizon fini, sans emprunt.

    terminal_assets >= 0 est une obligation de patrimoine en fin d'horizon,
    pas une ressource gratuite. Pour sigma>0, la concavité rend ce choix unique.
    Si la subsistance est infaisable, feasible=False : le moteur doit passer
    à son régime de subsistance rationnée, et ne prétend pas satisfaire Euler.
    """
    y=np.asarray(income,dtype=float)
    R=np.broadcast_to(np.asarray(gross_returns,dtype=float),y.shape)
    s=np.zeros_like(y) if subsistence is None else np.broadcast_to(subsistence,y.shape)
    if not np.all(np.isfinite([sigma,dt,rho,a0,terminal_assets])) or y.ndim!=1 or not len(y) or sigma<=0 or dt<=0 or rho<0 or a0<0 or terminal_assets<0:
        raise ValueError('Paramètres de décision invalides')
    if not np.all(np.isfinite(y)) or not np.all(np.isfinite(R)) or np.any(R<=0) or not np.all(np.isfinite(s)) or np.any(s<0):
        raise ValueError('Prévisions non finies ou rendement brut non positif')
    log_R=np.log(R)
    cumulative=np.concatenate(([0.],np.cumsum(log_R)))
    if np.max(np.abs(cumulative))>500 or np.max(np.abs((cumulative[:-1]-rho*dt*np.arange(len(y)))/sigma))>500:
        raise ValueError('Horizon/rendements hors domaine numérique du solveur')
    D=np.exp(-cumulative[:-1])
    q=np.exp((cumulative[:-1]-rho*dt*np.arange(len(y)))/sigma)
    resources=a0+np.cumsum(D*(y-s))
    resources[-1]-=np.exp(-cumulative[-1])*terminal_assets
    weights=np.cumsum(D*q)
    ceilings=resources/weights
    ix=int(np.argmin(ceilings))
    value=float(ceilings[ix])
    return ConsumptionChoice(max(value,0.),ix+1,float(ceilings[-1]),value>=-1e-10*max(a0,1.))


def consumption_path(a0,income,gross_returns,sigma=1.,rho=.01,dt=1/52,
                     subsistence=None,terminal_assets=0.):
    """Chemin complet pour validation indépendante des budgets et conditions KKT."""
    y=np.asarray(income,dtype=float); n=len(y)
    R=np.broadcast_to(np.asarray(gross_returns,dtype=float),y.shape)
    s=np.zeros(n) if subsistence is None else np.broadcast_to(subsistence,y.shape)
    c=np.zeros(n); a=np.zeros(n+1); a[0]=a0; start=0
    while start<n:
        choice=initial_consumption(max(a[start],0.),y[start:],R[start:],sigma,rho,dt,s[start:],terminal_assets)
        if not choice.feasible: raise ValueError('Subsistance/condition terminale infaisable')
        end=start+choice.binding_period
        logs=np.concatenate(([0.],np.cumsum(np.log(R[start:end-1]))))
        growth=np.exp((logs-rho*dt*np.arange(end-start))/sigma)
        c[start:end]=choice.surplus*growth
        for t in range(start,end):
            a[t+1]=R[t]*(a[t]+y[t]-s[t]-c[t])
        start=end
    return c,a


def plan_household(cash, noninterest_income, subsistence, annual_deposit_rate,
                   tax_rate, expected_inflation, sigma, rho, growth,
                   horizon_years=20., terminal_buffer_weeks=26., rate_reversion=2., return_gap=0.):
    """Prévisions déterministes à horizon glissant, tous les montants en réel.

    Le rendement proche suit le dépôt net observé ; son ancre lointaine est
    rho + sigma*g - return_gap, une anticipation subjective explicite, pas un taux imposé
    à la banque centrale. La subsistance réelle est constante dans la prévision.
    """
    values=[cash,noninterest_income,subsistence,annual_deposit_rate,tax_rate,
            expected_inflation,sigma,rho,growth,horizon_years,
            terminal_buffer_weeks,rate_reversion,return_gap]
    if not np.all(np.isfinite(values)) or cash<0 or subsistence<0 or expected_inflation<=-1 or not 0<=tax_rate<1 or horizon_years<=0 or terminal_buffer_weeks<0 or rate_reversion<0 or not 0<=return_gap<=.05:
        raise ValueError('Prévision ménages invalide')
    n=max(2,int(round(horizon_years*52)))
    if n>5200 or abs(growth)*horizon_years>100:
        raise ValueError('Horizon ménages limité à 100 ans et croissance bornée')
    t=np.arange(n)/52
    y=max(noninterest_income,0.)*np.exp(growth*t)
    y[0]=0.  # le revenu courant est déjà dans cash
    net_week=(1+max(annual_deposit_rate,0.))**(1/52)-1
    log_real_now=np.log1p((1-tax_rate)*net_week)-np.log1p(expected_inflation)/52
    long_log=(rho+sigma*growth-return_gap)/52
    decay=np.exp(-t/rate_reversion) if rate_reversion>0 else np.ones(n)
    R=np.exp(long_log+(log_real_now-long_log)*decay)
    terminal=terminal_buffer_weeks*max(noninterest_income,0.)*np.exp(growth*horizon_years)
    choice=initial_consumption(cash,y,R,sigma,rho,1/52,np.full(n,subsistence),terminal)
    if not choice.feasible:
        # Aucun plan ne peut financer toute la subsistance annoncée : la
        # dépense courante reste bornée par la caisse et le revenu de maintien.
        expenditure=min(cash,max(noninterest_income,0.))
    else:
        expenditure=min(cash,subsistence+choice.surplus)
    return max(float(expenditure),0.),choice,float(np.expm1(log_real_now*52))
