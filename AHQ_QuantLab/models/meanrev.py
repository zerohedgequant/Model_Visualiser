"""Ornstein-Uhlenbeck mean-reversion process explorer."""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from theme import AHQ, plotly_layout, page_header, formula, insight

def render():
    page_header("MEAN REVERSION \u00b7 ORNSTEIN\u2013UHLENBECK", AHQ["purple"],
                "A noisy spring on a spread",
                "Some series don't wander freely \u2014 they're pulled back toward a mean. The OU process adds a "
                "restoring force to Brownian motion: the further from the mean, the stronger the pull. "
                "Tune the speed, mean, and noise, and read off the half-life.")
    formula("dx = \u03b8\u00b7(\u03bc \u2212 x)\u00b7dt + \u03c3\u00b7dW")

    c1, c2 = st.columns([1, 2.4])
    with c1:
        st.markdown("#### Parameters")
        theta = st.slider("\u03b8  speed of reversion", 0.005, 0.30, 0.05, 0.005, format="%.3f")
        mu = st.slider("\u03bc  long-run mean", -5.0, 5.0, 0.0, 0.5)
        sigma = st.slider("\u03c3  noise", 0.05, 1.5, 0.4, 0.05)
        x0 = st.slider("x\u2080  start", -8.0, 8.0, 4.0, 0.5)
        n = st.slider("Length", 200, 1500, 600, 50)
        seed = st.number_input("Seed", 0, 9999, 5, 1)

        half = np.log(2)/theta
        st.metric("Half-life", f"{half:.1f} steps")
        eq_sd = sigma/np.sqrt(2*theta)
        st.metric("Equilibrium \u00b1\u03c3", f"{eq_sd:.2f}")
        insight(f"Half-life = ln(2)/\u03b8. With \u03b8={theta:.3f}, the gap to the mean closes by half every "
                f"<b>{half:.0f}</b> steps. Short half-life \u2192 more round-trips to trade.", AHQ["purple"])

    with c2:
        rng = np.random.default_rng(seed)
        x = np.zeros(n); x[0]=x0
        for t in range(1,n):
            x[t] = x[t-1] + theta*(mu-x[t-1]) + sigma*rng.standard_normal()
        idx = np.arange(n)
        fig = go.Figure()
        # equilibrium band
        fig.add_hrect(y0=mu-2*eq_sd, y1=mu+2*eq_sd, fillcolor="rgba(167,139,250,0.10)", line_width=0)
        fig.add_hline(y=mu, line=dict(color=AHQ["mute"],dash="dash"),
                      annotation_text="\u03bc", annotation_font_color=AHQ["mute"])
        fig.add_trace(go.Scatter(x=idx,y=x,line=dict(color=AHQ["purple"],width=2),name="x\u209c"))
        fig = plotly_layout(fig, height=340, ytitle="x\u209c", xtitle="step")
        fig.update_layout(margin=dict(l=50,r=20,t=10,b=30))
        st.plotly_chart(fig, use_container_width=True, key="ou_path")

        # z-score view
        z = (x-mu)/eq_sd
        figz = go.Figure()
        for lvl,c in [(2,AHQ["coral"]),(-2,AHQ["teal"])]:
            figz.add_hline(y=lvl, line=dict(color=c,dash="dot"))
        figz.add_trace(go.Scatter(x=idx,y=z,line=dict(color=AHQ["neonblue"],width=1.8),name="z-score"))
        figz = plotly_layout(figz, height=200, ytitle="z", xtitle="step", legend=False)
        figz.update_layout(margin=dict(l=50,r=20,t=10,b=30))
        st.plotly_chart(figz, use_container_width=True, key="ou_z")

    insight("Normalised to a z-score, the same series becomes a trading signal: fade it when it pushes beyond "
            "\u00b12\u03c3, exit as it reverts toward zero. The OU model is what turns \u201cit always comes back\u201d "
            "into estimable parameters \u2014 a speed, a mean, a band \u2014 instead of a hunch.", AHQ["purple"])
