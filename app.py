import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta
import time

from ui.theme import CSS
from ui.dashboard import render_quick_dashboard

st.set_page_config(page_title="Craftify Wrapped", page_icon="🎨", layout="wide")

# In-memory "database"
if "projects" not in st.session_state:
    st.session_state["projects"] = []

# ---------- THEME / CSS ----------
st.markdown(CSS, unsafe_allow_html=True)

# (Optional tiny boot marker so you see something immediately)
st.write("✅ App loaded")  # ▶ remove later if you want

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
            st.session_state["projects"].append(
                {"name": name, "category": category, "hours": float(hours), "date": dt}
            )
            msg = st.empty()
            msg.success("✅ Project added!")
            time.sleep(1)
            msg.empty()

df = pd.DataFrame(st.session_state["projects"])

# ---------- SLIDES + NAV ----------
if "slide" not in st.session_state:
    st.session_state["slide"] = 0

slides = ["dashboard","intro","projects","hours","top","charts"]

def next_slide(): st.session_state["slide"] = min(st.session_state["slide"]+1, len(slides)-1)
def prev_slide(): st.session_state["slide"] = max(st.session_state["slide"]-1, 0)

col1, col2 = st.columns([1,1])
with col1:
    if st.button("⬅ Prev"): prev_slide()
with col2:
    if st.button("Next ➡"): next_slide()

s = slides[st.session_state["slide"]]
st.markdown("## Craftify Wrapped 🎨")

# ---------- CONTENT ----------
try:  # ▶ show any errors inside the page
    if df.empty:
        st.info("Add a project to unlock your Wrapped!")
    else:
        # Coerce types once for all slides
        df2 = df.copy()
        df2["date"] = pd.to_datetime(df2["date"])
        df2["hours"] = pd.to_numeric(df2["hours"], errors="coerce").fillna(0.0)

        total_projects = len(df2)
        total_hours = float(df2["hours"].sum())
        by_cat_series = df2.groupby("category")["hours"].sum().sort_values(ascending=False)
        top_category = by_cat_series.idxmax() if not by_cat_series.empty else "—"

        if s == "dashboard":
            render_quick_dashboard(df2)
        elif s == "intro":
            st.subheader("Your Year in Making 🎉")
            st.caption("Use Next ➡ to browse highlights.")
        elif s == "projects":
            st.metric("Total Projects", total_projects)
            st.dataframe(
                df2.sort_values("date", ascending=False)[["date","name","category","hours"]],
                use_container_width=True, hide_index=True
            )
        elif s == "hours":
            st.metric("Total Hours", round(total_hours, 1))
        elif s == "top":
            st.metric("Top Category", top_category)
        elif s == "charts":
            fig = px.pie(
                df2, names="category", values="hours", title="Hours by Category",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error("Something went wrong rendering the page:")
    st.exception(e)  # ▶ shows full traceback in the app
