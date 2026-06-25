"""Value at Risk and Expected Shortfall explorer."""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm, t as student_t
from theme import AHQ, plotly_layout, page_header, formula, insight

def render():
    page_header("RISK \u00b7 VALUE-AT-RISK & EXPECTED SHORTFALL", AHQ["coral"],
                "The threshold vs the tail",
                "VaR reports a loss quantile \u2014 the loss you won't exceed with some confidence. It says nothing "
                "about how bad the rest of the tail gets. Expected Shortfall averages that tail. "
                "Switch the return distribution to fat-tailed and watch the gap between them widen.")
    formula("VaR\u2090 = quantile\u2090(loss)   \u2502   ES\u2090 = E[ loss | loss > VaR\u2090 ]")

    c1, c2 = st.columns([1, 2.4])
    with c1:
        st.markdown("#### Portfolio & distribution")
        conf = st.slider("Confidence level", 0.90, 0.995, 0.95, 0.005, format="%.3f")
        mu = st.slider("Mean daily return %", -0.20, 0.20, 0.03, 0.01)
        vol = st.slider("Daily volatility %", 0.3, 5.0, 1.2, 0.1)
        dist = st.radio("Distribution", ["Normal", "Fat-tailed (Student-t)"])
        if dist.startswith("Fat"):
            dof = st.slider("Degrees of freedom (lower = fatter)", 2.5, 15.0, 4.0, 0.5)
        seed = st.number_input("Seed", 0, 9999, 2, 1)

    N = 200000
    rng = np.random.default_rng(seed)
    if dist == "Normal":
        rets = rng.normal(mu, vol, N)
    else:
        raw = student_t.rvs(dof, size=N, random_state=seed)
        raw = raw/np.std(raw)  # standardise then scale
        rets = mu + vol*raw
    losses = -rets
    a = conf
    var = np.percentile(losses, a*100)
    es = losses[losses >= var].mean()

    with c1:
        st.metric(f"VaR ({a*100:.1f}%)", f"{var:.2f}%")
        st.metric(f"ES ({a*100:.1f}%)", f"{es:.2f}%")
        st.metric("ES / VaR ratio", f"{es/var:.2f}\u00d7")

    with c2:
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=rets, nbinsx=140, marker_color="rgba(59,158,255,0.45)", name="returns"))
        fig.add_vline(x=-var, line=dict(color=AHQ["coral"],width=2.5),
                      annotation_text=f"VaR", annotation_font_color=AHQ["coral"])
        fig.add_vline(x=-es, line=dict(color=AHQ["purple"],width=2.5,dash="dash"),
                      annotation_text="ES", annotation_font_color=AHQ["purple"])
        fig = plotly_layout(fig, height=360, ytitle="frequency", xtitle="daily return %", legend=False)
        fig.update_layout(margin=dict(l=50,r=20,t=10,b=30))
        st.plotly_chart(fig, use_container_width=True, key="var_hist")

    if dist.startswith("Fat"):
        insight("With fat tails, VaR may barely move but ES jumps \u2014 because the rare losses beyond the "
                "threshold are far larger than a normal distribution predicts. This is exactly why Basel moved "
                "capital rules from VaR to ES: VaR can look reassuring while the true tail is brutal.", AHQ["coral"])
    else:
        insight("Under a normal distribution VaR and ES are close. Switch to fat tails to see them diverge \u2014 "
                "the divergence is the whole point. VaR marks the door; ES measures the cliff behind it.", AHQ["coral"])
