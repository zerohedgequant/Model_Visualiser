"""Monte Carlo simulation of geometric Brownian motion + payoff distribution."""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from theme import AHQ, plotly_layout, page_header, formula, insight

def render():
    page_header("SIMULATION \u00b7 MONTE CARLO", AHQ["teal"],
                "Many futures from one present",
                "Geometric Brownian motion is the workhorse price process behind Black\u2013Scholes. "
                "Simulate thousands of paths from the same starting point and see the distribution of "
                "outcomes they imply \u2014 and how an option payoff is just an expectation over that distribution.")
    formula("dS = \u03bc\u00b7S\u00b7dt + \u03c3\u00b7S\u00b7dW")

    c1, c2 = st.columns([1, 2.4])
    with c1:
        st.markdown("#### Parameters")
        S0 = st.slider("Start price  S\u2080", 50.0, 200.0, 100.0, 1.0)
        mu = st.slider("Drift  \u03bc (annual)", -0.20, 0.30, 0.07, 0.01)
        sigma = st.slider("Volatility  \u03c3 (annual)", 0.05, 0.80, 0.25, 0.01)
        T = st.slider("Horizon  T (years)", 0.25, 3.0, 1.0, 0.25)
        npaths = st.select_slider("Paths", [200,500,1000,2000,5000], value=1000)
        K = st.slider("Call strike for payoff  K", 50.0, 200.0, 110.0, 1.0)
        seed = st.number_input("Seed", 0, 9999, 42, 1)

    steps = 252
    dt = T/steps
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal((npaths, steps))
    logret = (mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z
    paths = S0*np.exp(np.cumsum(logret, axis=1))
    paths = np.concatenate([np.full((npaths,1),S0), paths], axis=1)
    final = paths[:,-1]

    with c2:
        x = np.linspace(0, T, steps+1)
        fig = go.Figure()
        show = min(120, npaths)
        for i in range(show):
            fig.add_trace(go.Scatter(x=x, y=paths[i], mode="lines",
                                     line=dict(color="rgba(25,224,196,0.10)", width=1),
                                     showlegend=False, hoverinfo="skip"))
        # mean & quantile bands
        mean_p = paths.mean(axis=0)
        q05 = np.percentile(paths,5,axis=0); q95 = np.percentile(paths,95,axis=0)
        fig.add_trace(go.Scatter(x=x,y=q95,line=dict(color=AHQ["mute"],width=0),showlegend=False,hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=x,y=q05,fill="tonexty",fillcolor="rgba(138,153,174,0.12)",
                                 line=dict(color=AHQ["mute"],width=0),name="5\u201395%"))
        fig.add_trace(go.Scatter(x=x,y=mean_p,line=dict(color=AHQ["teal"],width=2.5),name="mean path"))
        fig = plotly_layout(fig, height=300, ytitle="price", xtitle="time (years)")
        fig.update_layout(margin=dict(l=50,r=20,t=10,b=30))
        st.plotly_chart(fig, use_container_width=True, key="mc_paths")

    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Mean final", f"{final.mean():.1f}")
    m2.metric("Median", f"{np.median(final):.1f}")
    payoff = np.maximum(final-K,0)
    disc = np.exp(-mu*T)  # rough discount using mu for illustration
    m3.metric(f"E[max(S\u2212K,0)]", f"{payoff.mean():.2f}")
    m4.metric("P(S > K)", f"{(final>K).mean()*100:.1f}%")

    cc1, cc2 = st.columns(2)
    with cc1:
        figh = go.Figure()
        figh.add_trace(go.Histogram(x=final, nbinsx=60, marker_color=AHQ["teal"],
                                    opacity=0.8, name="final price"))
        figh.add_vline(x=K, line=dict(color=AHQ["orange"],width=2),
                       annotation_text="K", annotation_font_color=AHQ["orange"])
        figh = plotly_layout(figh, height=260, ytitle="frequency", xtitle="final price S\u209c", legend=False)
        figh.update_layout(margin=dict(l=50,r=10,t=10,b=30))
        st.plotly_chart(figh, use_container_width=True, key="mc_hist")
    with cc2:
        figp = go.Figure()
        figp.add_trace(go.Histogram(x=payoff[payoff>0], nbinsx=50, marker_color=AHQ["orange"],
                                    opacity=0.8, name="payoff>0"))
        figp = plotly_layout(figp, height=260, ytitle="frequency", xtitle="call payoff max(S\u2212K,0)", legend=False)
        figp.update_layout(margin=dict(l=50,r=10,t=10,b=30))
        st.plotly_chart(figp, use_container_width=True, key="mc_payoff")

    insight("The lognormal fan of prices is exactly what Black\u2013Scholes assumes. The option's fair value is "
            "the discounted average of the payoff across all these paths \u2014 Monte Carlo and the closed-form "
            "formula are two routes to the same number, which is why MC is the fallback when no formula exists "
            "(path-dependent and exotic options).", AHQ["teal"])
