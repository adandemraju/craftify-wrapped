import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import time

st.set_page_config(page_title="MakerMetrics Wrapped", page_icon="🎨", layout="wide")

# In-memory "database"
if "projects" not in st.session_state:
    st.session_state.projects = []

# Add Project Form
st.sidebar.header("➕ Add Project")
with st.sidebar.form("add"):
    name = st.text_input("Project name")
    category = st.selectbox("Category", ["knitting","painting","paper","sewing","3D","other"])

    hours = st.number_input("Hours spent", min_value=0.1, step=0.1)
    dt = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("Save")
    if submitted:
        st.session_state["projects"].append({"name": name, "category": category, "hours": hours, "date": dt})
        msg = st.empty()
        msg.success("✅ Project added!")
        time.sleep(2)
        msg.empty()

df = pd.DataFrame(st.session_state.projects)

# Wrapped slides
if "slide" not in st.session_state:
    st.session_state.slide = 0

slides = ["intro","projects","hours","top","charts"]

def next_slide(): st.session_state.slide = min(st.session_state.slide+1,len(slides)-1)
def prev_slide(): st.session_state.slide = max(st.session_state.slide-1,0)

col1, col2 = st.columns([1,1])
with col1:
    if st.button("⬅ Prev"): prev_slide()
with col2:
    if st.button("Next ➡"): next_slide()

s = slides[st.session_state.slide]

st.markdown("## MakerMetrics Wrapped 🎨")

if df.empty:
    st.info("Add a project to unlock your Wrapped!")
else:
    total_projects = len(df)
    total_hours = df["hours"].sum()
    top_category = df.groupby("category")["hours"].sum().idxmax()

    if s=="intro":
        st.subheader("Your Year in Making 🎉")
    elif s=="projects":
        st.metric("Total Projects", total_projects)
    elif s=="hours":
        st.metric("Total Hours", round(total_hours,1))
    elif s=="top":
        st.metric("Top Category", top_category)
    elif s=="charts":
        fig = px.pie(df, names="category", values="hours", title="Hours by Category")
        st.plotly_chart(fig, use_container_width=True)
