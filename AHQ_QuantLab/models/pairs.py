"""Cointegration / pairs-trading explorer."""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from theme import AHQ, plotly_layout, page_header, formula, insight

def render():
    page_header("STAT-ARB \u00b7 COINTEGRATION & PAIRS", AHQ["neonteal"],
                "Two wanderers, one leash",
                "Two prices can each be non-stationary \u2014 wandering with no fixed mean \u2014 yet move together so "
                "their spread is stationary. That bound spread is a tradeable equilibrium. Tune how tightly the "
                "pair is linked and see the spread and its z-score signal.")
    formula("spread = A \u2212 \u03b2\u00b7B      z = (spread \u2212 \u03bc) / \u03c3")

    c1, c2 = st.columns([1, 2.4])
    with c1:
        st.markdown("#### Parameters")
        coint = st.slider("Cointegration strength", 0.0, 1.0, 0.8, 0.05,
                          help="0 = independent random walks, 1 = tightly bound spread")
        beta = st.slider("Hedge ratio  \u03b2", 0.5, 2.0, 1.0, 0.05)
        spread_vol = st.slider("Spread noise", 0.1, 2.0, 0.6, 0.1)
        n = st.slider("Length", 200, 1200, 500, 50)
        entry = st.slider("Entry z-threshold", 1.0, 3.0, 2.0, 0.25)
        seed = st.number_input("Seed", 0, 9999, 11, 1)

    rng = np.random.default_rng(seed)
    common = np.cumsum(rng.standard_normal(n)*0.5)        # shared stochastic trend
    # spread is mean-reverting only if cointegrated
    sp = np.zeros(n)
    theta = 0.02 + 0.18*coint                              # more coint => stronger reversion
    for t in range(1,n):
        sp[t] = sp[t-1] + theta*(0-sp[t-1]) + spread_vol*rng.standard_normal()
    A = 50 + common + sp + rng.standard_normal(n)*0.2
    B = (50 + common - rng.standard_normal(n)*0.2)/beta
    spread = A - beta*B
    mu = spread.mean(); sd = spread.std()
    z = (spread-mu)/sd

    with c2:
        idx=np.arange(n)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=idx,y=A,name="Asset A",line=dict(color=AHQ["neonblue"],width=1.8)))
        fig.add_trace(go.Scatter(x=idx,y=beta*B,name="\u03b2\u00b7Asset B",line=dict(color=AHQ["orange"],width=1.8)))
        fig = plotly_layout(fig, height=240, ytitle="price")
        fig.update_layout(margin=dict(l=50,r=20,t=10,b=10))
        st.plotly_chart(fig, use_container_width=True, key="pairs_px")

        figz=go.Figure()
        figz.add_hrect(y0=-entry,y1=entry,fillcolor="rgba(25,224,196,0.07)",line_width=0)
        figz.add_hline(y=entry,line=dict(color=AHQ["coral"],dash="dot"),
                       annotation_text=f"+{entry:g}\u03c3",annotation_font_color=AHQ["coral"])
        figz.add_hline(y=-entry,line=dict(color=AHQ["teal"],dash="dot"),
                       annotation_text=f"\u2212{entry:g}\u03c3",annotation_font_color=AHQ["teal"])
        figz.add_hline(y=0,line=dict(color=AHQ["mute"],dash="dash"))
        figz.add_trace(go.Scatter(x=idx,y=z,name="spread z-score",line=dict(color=AHQ["neonteal"],width=2)))
        figz = plotly_layout(figz, height=240, ytitle="z", xtitle="step")
        figz.update_layout(margin=dict(l=50,r=20,t=10,b=30))
        st.plotly_chart(figz, use_container_width=True, key="pairs_z")

    # crude signal stats
    crossings = int(np.sum(np.abs(z) > entry))
    m1,m2,m3 = st.columns(3)
    m1.metric("Spread \u03c3", f"{sd:.2f}")
    m2.metric("Reversion speed \u03b8", f"{theta:.3f}")
    m3.metric(f"Signals beyond \u00b1{entry:g}\u03c3", f"{crossings}")

    if coint < 0.25:
        insight("At low cointegration strength the spread itself drifts \u2014 there's no stable mean to revert to, "
                "and the z-score signal becomes a trap. This is the spurious-correlation failure mode: it can look "
                "tradeable in-sample and fall apart out-of-sample. Always test with ADF before trusting a pair.",
                AHQ["coral"])
    else:
        insight("With a bound spread, the z-score oscillates around zero and the \u00b12\u03c3 crossings are your "
                "entries: short the spread when rich, long it when cheap, exit on reversion. The position is "
                "market-neutral \u2014 you profit from the gap closing, not from market direction.", AHQ["neonteal"])
