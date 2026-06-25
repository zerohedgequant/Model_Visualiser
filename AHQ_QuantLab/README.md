# AlphaHedgeQuant — Quant Model Explorer

An interactive, single-app hub for visualising core quantitative-finance models. Move a slider, watch the theory respond. Built in Python with Streamlit + Plotly.

![models](models covered: GARCH, Black–Scholes, Monte Carlo, Ornstein–Uhlenbeck, VaR/ES, Cointegration)

## Run it

```bash
# 1. install dependencies (ideally in a virtualenv)
pip install -r requirements.txt

# 2. launch
streamlit run app.py
```

It opens in your browser at `http://localhost:8501`. Pick a model from the sidebar.

## Models

| Page | What it shows | Key controls |
|------|---------------|--------------|
| **Volatility · GARCH** | Volatility clustering; conditional variance σ²ₜ evolving from shocks + persistence | ω, α, β, length |
| **Options · Black–Scholes** | European call/put value vs spot, plus the Delta & Gamma profiles | S, K, T, σ, r, type |
| **Simulation · Monte Carlo** | Thousands of GBM price paths and the payoff distribution they imply | μ, σ, T, paths, strike |
| **Mean Reversion · OU** | The Ornstein–Uhlenbeck spring + its z-score trading signal | θ, μ, σ, x₀, half-life |
| **Risk · VaR & ES** | Where VaR stops and Expected Shortfall begins; normal vs fat-tailed | confidence, vol, distribution |
| **Stat-Arb · Pairs** | Two cointegrated series, the spread, and the z-score entries | cointegration strength, β, entry threshold |

## Structure

```
quantlab/
├── app.py              # hub: nav, routing, home page
├── theme.py            # dark terminal palette, CSS, Plotly styling
├── requirements.txt
└── models/
    ├── garch.py
    ├── blackscholes.py
    ├── montecarlo.py
    ├── meanrev.py
    ├── var_es.py
    └── pairs.py
```

Adding a model is one file: write a `render()` function in `models/yourmodel.py`, import it in `app.py`, and add a sidebar entry.

## Notes

- Charts run on **simulated data** generated live from the controls — the goal is intuition for how each parameter shapes the model, not live market signals.
- The math is the real thing (correct Black–Scholes, a genuine GARCH recursion, a real OU SDE discretisation), just driven by synthetic inputs so everything is reproducible from a seed.
- To extend toward live data, swap the simulated series for a data source (e.g. `yfinance`, your Upstox feed) inside each model's `render()`.

## Possible next steps

- Plug in real price data and **fit** GARCH/OU by maximum likelihood rather than simulating.
- Add an implied-volatility surface and a volatility-smile page.
- Export any chart's underlying series to CSV.
- Deploy to Streamlit Community Cloud for a public link.
