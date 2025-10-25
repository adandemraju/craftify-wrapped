import streamlit as st
import pandas as pd
from datetime import date
import time

import theme
import store
import stats
import components as ui

st.set_page_config(page_title="Craftify Wrapped", page_icon="🎨", layout="wide")

# Init state and theme
store.init_state()
if "slide" not in st.session_state: st.session_state["slide"] = 0
theme.inject()

# Sidebar: Add / Save / Load
st.sidebar.header("➕ Add Project")
with st.sidebar.form("add_project"):
    name = st.text_input("Project name")
    category = st.selectbox("Category", ["knitting","painting","paper","sewing","3D","other"])
    hours = st.number_input("Hours spent", min_value=0.1, step=0.1)
    dt = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("Save")
    if submitted:
        nm = (name or "").strip()
        if not nm:
            st.sidebar.warning("Please enter a project name.")
        else:
            store.add_project(nm, category, float(hours), str(dt))
            toast = st.empty()
            toast.success("✅ Project added!")
            time.sleep(0.8)
            toast.markdown('<div class="fade-out"> </div>', unsafe_allow_html=True)
            time.sleep(0.5)
            toast.empty()

st.sidebar.markdown("---")
store.download_json_button("💾 Download JSON")
uploaded = st.sidebar.file_uploader("📥 Load JSON", type=["json"])
if uploaded:
    if store.upload_json(uploaded):
        st.sidebar.success("Loaded projects from JSON.")
    else:
        st.sidebar.error("Invalid JSON.")

store.download_csv_button("⬇️ Download CSV")

# Slide nav
slides = ["dashboard","intro","projects","hours","top","charts"]
def next_slide(): st.session_state["slide"] = min(st.session_state["slide"]+1,len(slides)-1)
def prev_slide(): st.session_state["slide"] = max(st.session_state["slide"]-1,0)

left, right = st.columns([1,1])
with left:
    if st.button("⬅ Prev"): prev_slide()
with right:
    if st.button("Next ➡"): next_slide()

s = slides[st.session_state["slide"]]
st.markdown("## Craftify Wrapped 🎨")

df = store.get_projects_df()

if df.empty:
    st.info("Add a project to unlock your Wrapped!")
else:
    meta = stats.summary(df)
    total_projects = meta["total_projects"]
    total_hours = meta["total_hours"]
    top_category = meta["top_category"]
    by_cat = meta["by_cat"]
    monthly = stats.monthly_hours(df)

    if s == "dashboard":
        # KPI row
        k1,k2,k3,k4,k5 = st.columns(5)
        with k1: ui.kpi_card("Projects", total_projects, "grad-2")
        with k2: ui.kpi_card("Total Hours", round(total_hours,1), "grad-3")
        with k3: ui.kpi_card("Avg hrs / project", meta["avg_hours"], "grad-4")
        with k4: ui.kpi_card("Top Category", top_category, "grad-5")
        with k5: ui.kpi_card("Last 7 days (hrs)", round(meta["last7_hours"],1), "grad-1")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Hours by Category")
            ui.bar_category(by_cat)
        with c2:
            st.subheader("Hours Over Time (Monthly)")
            ui.area_monthly(monthly)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card" style="margin-top:12px;">', unsafe_allow_html=True)
        cA, cB = st.columns(2)
        with cA:
            st.subheader("🏆 Top 5 Categories")
            for i, (cat, hrs) in enumerate(by_cat.head(5).items(), start=1):
                st.markdown(f"**{i}. {cat.capitalize()}** — {hrs:.1f} hrs")
        with cB:
            st.subheader("🖌️ Top 5 Projects")
            for i, row in stats.top5_projects(df).iterrows():
                st.markdown(f"**{i+1}. {row['name']}** — {row['hours']} hrs ({row['category']})")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card" style="margin-top:12px;">', unsafe_allow_html=True)
        st.subheader("Recent Projects")
        recent = df.sort_values("date", ascending=False)[["date","name","category","hours"]].head(10)
        st.dataframe(recent, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif s == "intro":
        st.markdown('<div class="card grad-1">', unsafe_allow_html=True)
        st.markdown("<h2>Your Year in Making 🎉</h2>", unsafe_allow_html=True)
        st.caption("Use Next ➡ to browse highlights.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif s == "projects":
        st.markdown('<div class="card grad-2">', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi"><div class="label">Projects Completed</div><div class="value">{total_projects}</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div class="card" style="margin-top:12px;">', unsafe_allow_html=True)
        st.subheader("All Projects")
        st.dataframe(df.sort_values("date", ascending=False)[["date","name","category","hours"]],
                     use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif s == "hours":
        st.markdown('<div class="card grad-3">', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi"><div class="label">Hours Creating</div><div class="value">{round(total_hours,1)}</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif s == "top":
        st.markdown('<div class="card grad-4">', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi"><div class="label">Top Category</div><div class="value">{top_category}</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div class="card" style="margin-top:12px;">', unsafe_allow_html=True)
        cA, cB = st.columns(2)
        with cA:
            st.subheader("🏆 Top 5 Categories")
            for i, (cat, hrs) in enumerate(by_cat.head(5).items(), start=1):
                st.markdown(f"**{i}. {cat.capitalize()}** — {hrs:.1f} hrs")
        with cB:
            st.subheader("🖌️ Top 5 Projects")
            for i, row in stats.top5_projects(df).iterrows():
                st.markdown(f"**{i+1}. {row['name']}** — {row['hours']} hrs ({row['category']})")
        st.markdown("</div>", unsafe_allow_html=True)

    elif s == "charts":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Hours by Category")
        ui.pie_category(df)
        st.markdown("</div>", unsafe_allow_html=True)
