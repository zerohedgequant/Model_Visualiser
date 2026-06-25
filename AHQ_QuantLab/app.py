"""
AlphaHedgeQuant — Quant Model Explorer
A single-file Streamlit hub for visualising quantitative finance models interactively.

Run:  streamlit run app.py
"""
import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import norm

import models.garch as garch
import models.blackscholes as bs
import models.montecarlo as mc
import models.meanrev as meanrev
import models.var_es as var_es
import models.pairs as pairs
from theme import inject_css, AHQ

st.set_page_config(
    page_title="AHQ · Quant Model Explorer",
    page_icon="\u03b1",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# ---------- sidebar nav ----------
with st.sidebar:
    st.markdown(
        f"""<div class="ahq-brand">
        <span class="ahq-bracket">[</span><span class="ahq-alpha">&#945;</span><span class="ahq-bracket">]</span>
        <div class="ahq-word">Alpha<span class="ahq-accent">Hedge</span>Quant</div>
        <div class="ahq-tag">QUANT MODEL EXPLORER</div>
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='ahq-navlabel'>MODELS</div>", unsafe_allow_html=True)
    page = st.radio(
        "Model",
        ["Home",
         "Volatility \u00b7 GARCH",
         "Options \u00b7 Black\u2013Scholes",
         "Simulation \u00b7 Monte Carlo",
         "Mean Reversion \u00b7 OU",
         "Risk \u00b7 VaR & ES",
         "Stat-Arb \u00b7 Pairs"],
        label_visibility="collapsed",
    )
    st.markdown("<div class='ahq-foot'>Models are illustrative, fit on simulated data unless noted. Educational use.</div>", unsafe_allow_html=True)

# ---------- routing ----------
if page == "Home":
    st.markdown("<div class='ahq-hero-eyebrow'>QUANTITATIVE RESEARCH \u00b7 INTERACTIVE</div>", unsafe_allow_html=True)
    st.markdown("<h1 class='ahq-hero'>See the models, not just the math.</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='ahq-lede'>Six core models from quantitative finance, each rendered as a live, "
        "parameter-driven visualisation. Move a slider and watch the theory respond \u2014 "
        "volatility clustering, option surfaces, diffusion paths, mean reversion, tail risk, and cointegration.</p>",
        unsafe_allow_html=True,
    )

    cards = [
        ("Volatility \u00b7 GARCH", "Volatility clusters and mean-reverts. Fit GARCH(1,1) and watch \u03c3\u00b2 evolve.", AHQ['orange']),
        ("Options \u00b7 Black\u2013Scholes", "Price calls and puts; see the Greeks deform as inputs move.", AHQ['neonblue']),
        ("Simulation \u00b7 Monte Carlo", "Thousands of geometric Brownian paths and the payoff distribution they imply.", AHQ['teal']),
        ("Mean Reversion \u00b7 OU", "The Ornstein\u2013Uhlenbeck spring: tune speed, mean, noise, half-life.", AHQ['purple']),
        ("Risk \u00b7 VaR & ES", "Where Value-at-Risk stops and Expected Shortfall begins, on the loss tail.", AHQ['coral']),
        ("Stat-Arb \u00b7 Pairs", "Two cointegrated series, the spread, and the z-score that trades it.", AHQ['neonteal']),
    ]
    cols = st.columns(3)
    for i, (title, desc, col) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(
                f"""<div class='ahq-card' style='border-top:3px solid {col};'>
                <div class='ahq-card-title'>{title}</div>
                <div class='ahq-card-desc'>{desc}</div>
                </div>""",
                unsafe_allow_html=True,
            )
    st.markdown("<div class='ahq-note'>Select a model from the sidebar to begin. Every chart recomputes live from the controls.</div>", unsafe_allow_html=True)

elif page.startswith("Volatility"):
    garch.render()
elif page.startswith("Options"):
    bs.render()
elif page.startswith("Simulation"):
    mc.render()
elif page.startswith("Mean"):
    meanrev.render()
elif page.startswith("Risk"):
    var_es.render()
elif page.startswith("Stat-Arb"):
    pairs.render()
