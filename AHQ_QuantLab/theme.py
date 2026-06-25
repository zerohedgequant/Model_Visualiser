"""Shared theme: dark quant-terminal palette + CSS + Plotly layout helper."""
import streamlit as st

AHQ = {
    "bg":       "#0B0F1A",
    "panel":    "#121A28",
    "panel2":   "#0E1420",
    "line":     "#1E2A3D",
    "ink":      "#EAF1FB",
    "mute":     "#8A99AE",
    "blue":     "#2563EB",
    "neonblue": "#3B9EFF",
    "teal":     "#10B6A8",
    "neonteal": "#19E0C4",
    "orange":   "#FF6A2B",
    "coral":    "#FF5C7A",
    "purple":   "#A78BFA",
    "green":    "#34E29B",
}

def inject_css():
    st.markdown(f"""
    <style>
    .stApp {{ background: {AHQ['bg']}; }}
    header[data-testid="stHeader"] {{ background: {AHQ['bg']}; }}
    .stApp > header {{ background: transparent; }}
    div[data-testid="stToolbar"] {{ right: 8px; }}
    section[data-testid="stSidebar"] {{ background: {AHQ['panel2']}; border-right: 1px solid {AHQ['line']}; }}
    /* brand block */
    .ahq-brand {{ text-align:center; padding: 8px 0 18px; border-bottom:1px solid {AHQ['line']}; margin-bottom:18px; }}
    .ahq-bracket {{ font-size:34px; color:{AHQ['ink']}; font-weight:700; }}
    .ahq-alpha {{ font-size:38px; color:{AHQ['orange']}; font-weight:700; }}
    .ahq-word {{ font-size:21px; font-weight:700; color:{AHQ['ink']}; letter-spacing:0.3px; margin-top:2px; }}
    .ahq-accent {{ color:{AHQ['orange']}; }}
    .ahq-tag {{ font-size:10px; letter-spacing:3px; color:{AHQ['mute']}; margin-top:4px; }}
    .ahq-navlabel {{ font-size:10px; letter-spacing:2.5px; color:{AHQ['mute']}; margin:6px 0 2px 4px; }}
    .ahq-foot {{ font-size:10.5px; color:{AHQ['mute']}; margin-top:24px; line-height:1.5; border-top:1px solid {AHQ['line']}; padding-top:12px; }}
    /* hero */
    .ahq-hero-eyebrow {{ font-size:12px; letter-spacing:3px; color:{AHQ['neonblue']}; font-weight:700; margin-bottom:8px; }}
    .ahq-hero {{ font-size:46px; font-weight:800; color:{AHQ['ink']}; line-height:1.05; margin:0 0 14px; }}
    .ahq-lede {{ font-size:17px; color:{AHQ['mute']}; max-width:760px; line-height:1.6; }}
    /* cards */
    .ahq-card {{ background:{AHQ['panel']}; border:1px solid {AHQ['line']}; border-radius:14px; padding:18px 16px; margin:8px 0; min-height:120px; }}
    .ahq-card-title {{ font-size:16px; font-weight:700; color:{AHQ['ink']}; margin-bottom:6px; }}
    .ahq-card-desc {{ font-size:13px; color:{AHQ['mute']}; line-height:1.5; }}
    .ahq-note {{ margin-top:18px; font-size:13px; color:{AHQ['mute']}; font-style:italic; }}
    /* model page headers */
    .ahq-mtitle {{ font-size:32px; font-weight:800; color:{AHQ['ink']}; margin:0 0 2px; }}
    .ahq-mkicker {{ font-size:12px; letter-spacing:3px; font-weight:700; margin-bottom:6px; }}
    .ahq-msub {{ font-size:15px; color:{AHQ['mute']}; line-height:1.55; max-width:820px; margin-bottom:6px; }}
    .ahq-formula {{ background:{AHQ['panel2']}; border:1px solid {AHQ['line']}; border-radius:10px;
                    padding:12px 16px; color:{AHQ['ink']}; font-family:'DejaVu Sans Mono',monospace;
                    font-size:16px; margin:10px 0; }}
    .ahq-insight {{ background:{AHQ['panel']}; border-left:3px solid {AHQ['neonblue']}; border-radius:6px;
                    padding:12px 16px; color:{AHQ['ink']}; font-size:14px; margin:10px 0; }}
    /* metrics */
    div[data-testid="stMetricValue"] {{ color:{AHQ['ink']}; font-size:26px; }}
    div[data-testid="stMetricLabel"] {{ color:{AHQ['mute']}; }}
    /* sliders */
    .stSlider label {{ color:{AHQ['ink']} !important; font-weight:600; }}
    h2, h3 {{ color:{AHQ['ink']}; }}
    </style>
    """, unsafe_allow_html=True)

def plotly_layout(fig, height=440, ytitle=None, xtitle=None, legend=True):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=AHQ["panel2"],
        font=dict(color=AHQ["ink"], family="DejaVu Sans, Arial"),
        height=height,
        margin=dict(l=50, r=20, t=30, b=40),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=AHQ["line"]),
        showlegend=legend,
    )
    fig.update_xaxes(gridcolor=AHQ["line"], zerolinecolor=AHQ["line"], title_text=xtitle)
    fig.update_yaxes(gridcolor=AHQ["line"], zerolinecolor=AHQ["line"], title_text=ytitle)
    return fig

def page_header(kicker, kcolor, title, sub):
    st.markdown(f"<div class='ahq-mkicker' style='color:{kcolor}'>{kicker}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='ahq-mtitle'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='ahq-msub'>{sub}</div>", unsafe_allow_html=True)

def formula(latex_text):
    st.markdown(f"<div class='ahq-formula'>{latex_text}</div>", unsafe_allow_html=True)

def insight(text, color=None):
    c = color or AHQ["neonblue"]
    st.markdown(f"<div class='ahq-insight' style='border-left-color:{c}'>{text}</div>", unsafe_allow_html=True)
