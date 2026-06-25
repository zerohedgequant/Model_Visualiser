"""Black-Scholes option pricing and Greeks explorer."""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
from theme import AHQ, plotly_layout, page_header, formula, insight

def bs_price(S, K, T, r, sigma, kind="call"):
    if T <= 0 or sigma <= 0:
        intrinsic = np.maximum(S-K,0) if kind=="call" else np.maximum(K-S,0)
        return intrinsic
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if kind == "call":
        return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    return K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

def greeks(S, K, T, r, sigma, kind="call"):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    pdf = norm.pdf(d1)
    delta = norm.cdf(d1) if kind=="call" else norm.cdf(d1)-1
    gamma = pdf / (S*sigma*np.sqrt(T))
    vega  = S*pdf*np.sqrt(T) / 100
    theta = (-(S*pdf*sigma)/(2*np.sqrt(T)) - r*K*np.exp(-r*T)*(norm.cdf(d2) if kind=="call" else norm.cdf(-d2)))/365
    return delta, gamma, vega, theta

def render():
    page_header("OPTIONS \u00b7 BLACK\u2013SCHOLES", AHQ["neonblue"],
                "Price the option, see the Greeks",
                "The closed-form fair value of a European option and its sensitivities. "
                "Move spot, volatility, or time and watch both the price and the Greek profiles deform.")
    formula("C = S\u00b7N(d\u2081) \u2212 K\u00b7e^(\u2212rT)\u00b7N(d\u2082)")

    c1, c2 = st.columns([1, 2.4])
    with c1:
        st.markdown("#### Inputs")
        kind = st.radio("Option type", ["call", "put"], horizontal=True)
        S = st.slider("Spot  S", 20.0, 200.0, 100.0, 1.0)
        K = st.slider("Strike  K", 20.0, 200.0, 100.0, 1.0)
        T = st.slider("Time to expiry  T (yrs)", 0.02, 2.0, 0.5, 0.02)
        sigma = st.slider("Volatility  \u03c3", 0.05, 1.0, 0.25, 0.01)
        r = st.slider("Risk-free rate  r", 0.0, 0.12, 0.05, 0.005)

        price = bs_price(S, K, T, r, sigma, kind)
        delta, gamma, vega, theta = greeks(S, K, T, r, sigma, kind)
        st.metric(f"{kind.title()} price", f"{price:.2f}")
        g1,g2 = st.columns(2)
        g1.metric("Delta", f"{delta:.3f}"); g2.metric("Gamma", f"{gamma:.4f}")
        g1.metric("Vega",  f"{vega:.3f}");  g2.metric("Theta", f"{theta:.4f}")

    with c2:
        Sgrid = np.linspace(max(5,K*0.4), K*1.6, 220)
        # price curve + payoff
        prices = np.array([bs_price(s,K,T,r,sigma,kind) for s in Sgrid])
        payoff = np.maximum(Sgrid-K,0) if kind=="call" else np.maximum(K-Sgrid,0)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Sgrid,y=payoff,name="payoff at expiry",
                                 line=dict(color=AHQ["mute"],dash="dash",width=1.5)))
        fig.add_trace(go.Scatter(x=Sgrid,y=prices,name="value now",
                                 line=dict(color=AHQ["neonblue"],width=2.5)))
        fig.add_vline(x=S, line=dict(color=AHQ["orange"],width=1.5),
                      annotation_text="spot", annotation_font_color=AHQ["orange"])
        fig = plotly_layout(fig, height=250, ytitle="option value", xtitle="spot S")
        fig.update_layout(margin=dict(l=50,r=20,t=10,b=30))
        st.plotly_chart(fig, use_container_width=True, key="bs_price")

        # greek profiles
        dvals=[]; gvals=[]
        for s in Sgrid:
            dd,gg,_,_ = greeks(s,K,T,r,sigma,kind); dvals.append(dd); gvals.append(gg)
        gv = np.array(gvals); gv = gv/gv.max() if gv.max()>0 else gv
        figg = go.Figure()
        figg.add_trace(go.Scatter(x=Sgrid,y=dvals,name="Delta",line=dict(color=AHQ["teal"],width=2.5)))
        figg.add_trace(go.Scatter(x=Sgrid,y=gv,name="Gamma (scaled)",line=dict(color=AHQ["orange"],width=2.5)))
        figg.add_vline(x=S, line=dict(color=AHQ["mute"],width=1,dash="dot"))
        figg = plotly_layout(figg, height=230, ytitle="sensitivity", xtitle="spot S")
        figg.update_layout(margin=dict(l=50,r=20,t=10,b=30))
        st.plotly_chart(figg, use_container_width=True, key="bs_greeks")

    insight("Delta is the slope of the value curve; Gamma is how fast that slope changes \u2014 it peaks "
            "at-the-money and near expiry. A delta-hedge neutralises direction so you're left trading volatility; "
            "high gamma is what makes that hedge need constant rebalancing.", AHQ["neonblue"])
