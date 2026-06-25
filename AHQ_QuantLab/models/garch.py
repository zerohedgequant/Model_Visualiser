"""GARCH(1,1) volatility model explorer."""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from theme import AHQ, plotly_layout, page_header, formula, insight

def simulate_garch(n, omega, alpha, beta, seed):
    rng = np.random.default_rng(seed)
    r = np.zeros(n); sig2 = np.zeros(n)
    sig2[0] = omega / max(1e-6, (1 - alpha - beta))
    for t in range(1, n):
        sig2[t] = omega + alpha * r[t-1]**2 + beta * sig2[t-1]
        r[t] = np.sqrt(sig2[t]) * rng.standard_normal()
    return r, np.sqrt(sig2)

def render():
    page_header("VOLATILITY \u00b7 GARCH(1,1)", AHQ["orange"],
                "Volatility clustering, modelled",
                "Returns don't have constant volatility \u2014 large moves cluster and then fade. "
                "GARCH lets today's variance depend on yesterday's shock and yesterday's variance. "
                "Adjust the parameters and watch the conditional volatility \u03c3\u209c respond.")
    formula("\u03c3\u00b2\u209c = \u03c9 + \u03b1\u00b7r\u00b2\u209c\u208b\u2081 + \u03b2\u00b7\u03c3\u00b2\u209c\u208b\u2081")

    c1, c2 = st.columns([1, 2.4])
    with c1:
        st.markdown("#### Parameters")
        omega = st.slider("\u03c9  (baseline variance)", 0.001, 0.20, 0.02, 0.001, format="%.3f")
        alpha = st.slider("\u03b1  (shock reaction)", 0.0, 0.50, 0.10, 0.01)
        beta  = st.slider("\u03b2  (variance persistence)", 0.0, 0.98, 0.85, 0.01)
        n     = st.slider("Sample length (days)", 200, 2000, 600, 50)
        seed  = st.number_input("Random seed", 0, 9999, 7, 1)

        persistence = alpha + beta
        if persistence >= 1:
            st.markdown(f"<div class='ahq-insight' style='border-left-color:{AHQ['coral']}'>"
                        f"\u03b1+\u03b2 = {persistence:.2f} \u2265 1 \u2014 the process is non-stationary; "
                        f"variance never settles. Real fits keep \u03b1+\u03b2 just below 1.</div>",
                        unsafe_allow_html=True)
        else:
            lr_var = omega / (1 - persistence)
            st.metric("Persistence \u03b1+\u03b2", f"{persistence:.3f}")
            st.metric("Long-run \u03c3 (daily)", f"{np.sqrt(lr_var):.3f}")
            half = np.log(0.5)/np.log(persistence) if persistence>0 else float('inf')
            st.metric("Vol shock half-life", f"{half:.1f} days")

    with c2:
        r, sig = simulate_garch(n, omega, alpha, beta, seed)
        x = np.arange(n)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=r, mode="lines", name="returns",
                                 line=dict(color=AHQ["neonblue"], width=1)))
        fig = plotly_layout(fig, height=240, ytitle="return")
        fig.update_layout(margin=dict(l=50,r=20,t=10,b=10))
        st.plotly_chart(fig, use_container_width=True, key="garch_ret")

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=x, y=sig, mode="lines", name="\u03c3\u209c (conditional vol)",
                                  line=dict(color=AHQ["orange"], width=2),
                                  fill="tozeroy", fillcolor="rgba(255,106,43,0.12)"))
        if persistence < 1:
            fig2.add_hline(y=np.sqrt(omega/(1-persistence)), line=dict(color=AHQ["mute"], dash="dash"),
                           annotation_text="long-run \u03c3", annotation_font_color=AHQ["mute"])
        fig2 = plotly_layout(fig2, height=240, ytitle="\u03c3\u209c")
        fig2.update_layout(margin=dict(l=50,r=20,t=10,b=30))
        st.plotly_chart(fig2, use_container_width=True, key="garch_vol")

    insight("Notice how a single large return inflates \u03c3\u209c, which then decays slowly back toward the "
            "long-run level \u2014 that slow decay is the <b>persistence</b> term \u03b2. High \u03b2 means calm and "
            "stormy periods both last a long time. This is why volatility is far more forecastable than returns.",
            AHQ["orange"])

    with st.expander("How this differs from real GARCH fitting"):
        st.markdown(
            "- Here we **simulate** a GARCH process from parameters you choose, to build intuition for what "
            "each parameter does.\n"
            "- In practice you **estimate** \u03c9, \u03b1, \u03b2 from observed returns by maximum likelihood "
            "(e.g. `arch` library in Python).\n"
            "- Extensions: **EGARCH / GJR-GARCH** add asymmetry so that negative shocks raise volatility more "
            "than positive ones (the leverage effect)."
        )
