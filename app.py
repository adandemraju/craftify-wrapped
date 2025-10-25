import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta
import time

import base64, pathlib

# Path to your font file (make sure fonts/Wonderia.otf exists next to app.py)
FONT_PATH = pathlib.Path("fonts/Wonderia.otf")

# Read and encode the font into base64 so the browser can load it
with open(FONT_PATH, "rb") as f:
    wonderia_b64 = base64.b64encode(f.read()).decode("utf-8")


st.set_page_config(page_title="Craftify Wrapped", page_icon="🎨", layout="wide")

# In-memory "database"
if "projects" not in st.session_state:
    st.session_state.projects = []

# ---------- THEME / CSS ----------
st.markdown(f"""
<style>
@font-face {{
  font-family: 'Wonderia';
  src: url(data:font/opentype;base64,{wonderia_b64}) format('opentype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}}

/* Apply Wonderia everywhere */
html, body, .stApp, [class^="css-"], [class*=" css-"],
p, span, div, label, input, select, textarea, button, code, pre, table {{
  font-family: 'Wonderia', !important;
}}

/* Keep your color scheme */
.stApp {{ background: linear-gradient(180deg, #ffd6e8 0%, #fff0f6 100%); color: #4a0033; }}
section[data-testid="stSidebar"] {{ background-color: #ffe6f0 !important; color: #cc0066 !important; }}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] span {{
  color: #cc0066 !important; font-weight: 600;
}}

div.stButton > button:first-child {{
  background-color: #ff66b2; color: white; border: none; border-radius: 12px;
  height: 3em; width: 8em; font-weight: 600; transition: 0.3s;
}}
div.stButton > button:first-child:hover {{ background-color: #ff3385; transform: scale(1.05); }}

.stAlert {{
  background-color: #ffcce0 !important; color: #800040 !important;
  border-radius: 10px; font-weight: 500;
}}

h1, h2, h3, h4, h5, h6 {{
  color: #cc0066 !important;
  font-family: 'Wonderia', !important;
}}

.card {{
  background: #ffffffcc; border: 1px solid #ffd1e3;
  border-radius: 16px; padding: 16px;
  box-shadow: 0 6px 18px rgba(204,0,102,.1);
}}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR: ADD PROJECT ----------
st.sidebar.header("➕ Add Project")
with st.sidebar.form("add"):
    name = st.text_input("Project name").strip()
    category = st.selectbox("Category", ["knitting","painting","paper","sewing","3D","other"])
    hours = st.number_input("Hours spent", min_value=0.0, step=0.1)
    dt = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("Save")
    if submitted:
        if not name:
            st.sidebar.warning("Please enter a project name.")
        else:
            st.session_state["projects"].append({"name": name, "category": category, "hours": float(hours), "date": dt})
            msg = st.empty()
            msg.success("✅ Project added!")
            time.sleep(1)
            msg.empty()

df = pd.DataFrame(st.session_state.projects)

# ---------- SLIDES + NAV ----------
if "slide" not in st.session_state:
    st.session_state.slide = 0

# NEW: add "dashboard" as first slide
slides = ["dashboard","intro","projects","hours","top","charts"]

def next_slide(): st.session_state.slide = min(st.session_state.slide+1,len(slides)-1)
def prev_slide(): st.session_state.slide = max(st.session_state.slide-1,0)

col1, col2 = st.columns([1,1])
with col1:
    if st.button("⬅ Prev"): prev_slide()
with col2:
    if st.button("Next ➡"): next_slide()

s = slides[st.session_state.slide]

st.markdown("## Craftify Wrapped 🎨")

# ---------- QUICK DASHBOARD RENDERER ----------
def render_quick_dashboard(data: pd.DataFrame):
    if data.empty:
        st.info("Add a project to unlock your Wrapped!")
        return
    df2 = data.copy()
    df2["date"] = pd.to_datetime(df2["date"])
    df2["hours"] = pd.to_numeric(df2["hours"], errors="coerce").fillna(0.0)

    total_projects = len(df2)
    total_hours = float(df2["hours"].sum())
    avg_hours = round(total_hours/total_projects, 2) if total_projects else 0.0
    by_cat = df2.groupby("category")["hours"].sum().sort_values(ascending=False)
    top_category = by_cat.idxmax() if not by_cat.empty else "—"

    last7_cut = df2["date"].max() - timedelta(days=7) if not df2.empty else pd.Timestamp.today()-timedelta(days=7)
    last7_hours = float(df2[df2["date"] >= last7_cut]["hours"].sum())

    # metrics row
    st.markdown('<div class="card">', unsafe_allow_html=True)
    a,b,c,d,e = st.columns(5)
    a.metric("Projects", total_projects)
    b.metric("Total Hours", round(total_hours,1))
    c.metric("Avg hrs / project", avg_hours)
    d.metric("Top Category", top_category)
    e.metric("Last 7 days (hrs)", round(last7_hours,1))
    st.markdown('</div>', unsafe_allow_html=True)

    # charts row
    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Hours by Category")
        fig_cat = px.bar(by_cat.reset_index(), x="category", y="hours",
                        labels={"hours":"Hours","category":"Category"}, height=350,
                        color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_cat.update_layout(margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig_cat, use_container_width=True)
    with c2:
        st.subheader("Hours Over Time (Monthly)")
        by_month = df2.groupby(df2["date"].dt.to_period("M"))["hours"].sum().reset_index()
        by_month["date"] = by_month["date"].dt.to_timestamp()
        fig_time = px.area(by_month, x="date", y="hours", markers=True, height=350,
                        color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_time.update_layout(margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig_time, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # recent table
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Recent Projects")
    recent = df2.sort_values("date", ascending=False)[["date","name","category","hours"]].head(10)
    st.dataframe(recent, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- CONTENT ----------
if df.empty:
    if s == "dashboard":
        st.info("Add a project to unlock your Wrapped!")
    else:
        st.info("Add a project to unlock your Wrapped!")
else:
    total_projects = len(df)
    total_hours = df["hours"].sum()
    top_category = df.groupby("category")["hours"].sum().idxmax()

    if s=="dashboard":
        render_quick_dashboard(df)
    elif s=="intro":
        st.subheader("Your Year in Making 🎉")
        st.caption("Use Next ➡ to browse highlights.")
    elif s=="projects":
        st.metric("Total Projects", total_projects)
        st.dataframe(df.sort_values("date", ascending=False)[["date","name","category","hours"]],
                    use_container_width=True, hide_index=True)
    elif s=="hours":
        st.metric("Total Hours", round(total_hours,1))
    elif s=="top":
        st.metric("Top Category", top_category)
    elif s=="charts":
        fig = px.pie(df, names="category", values="hours", title="Hours by Category",
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)