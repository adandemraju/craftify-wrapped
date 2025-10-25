import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import timedelta

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
