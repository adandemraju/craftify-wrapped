# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta
import time

st.set_page_config(page_title="Craftify Wrapped", page_icon="🎨", layout="wide")

# ---------------- In-memory "database" ----------------
if "projects" not in st.session_state:
    st.session_state["projects"] = []
if "slide" not in st.session_state:
    st.session_state["slide"] = 0

# ---------------- Fonts + Theme CSS (Spotify-ish) ----------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
<style>
/* App background + default text */
html, body, [class*="css"] {
  font-family: 'Poppins', sans-serif;
}
.stApp {
  background: radial-gradient(1200px 800px at 10% 10%, #fff0f6 0%, #ffd6e8 35%, #ffffff 75%);
  color: #2b0040;
}

/* Sidebar pastel */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #fff0f6 0%, #ffe6f0 100%) !important;
  border-right: 1px solid #ffd1e3;
}
section[data-testid="stSidebar"] * {
  color: #a0005a !important;
}

/* Buttons */
div.stButton > button:first-child {
  background: #ff66b2; color: #fff; border: none;
  border-radius: 14px; padding: 0.7rem 1.1rem; font-weight: 700;
  box-shadow: 0 10px 20px rgba(255, 102, 178, 0.25);
  transition: transform .15s ease, box-shadow .15s ease;
}
div.stButton > button:first-child:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 14px 26px rgba(255, 102, 178, 0.35);
}

/* Headings */
h1, h2, h3, h4 { color: #8a0066; font-family: 'Montserrat', sans-serif; font-weight: 800; }

/* Reusable cards */
.card {
  border-radius: 24px; padding: 22px; background: #ffffffcc;
  border: 1px solid #ffd1e3; box-shadow: 0 18px 40px rgba(170, 0, 102, 0.08);
}
.grad-1 { background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); color: #fff; }
.grad-2 { background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%); color: #fff; }
.grad-3 { background: linear-gradient(135deg, #ff9966 0%, #ff5e62 100%); color: #fff; }
.grad-4 { background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); color: #fff; }
.grad-5 { background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%); color: #fff; }

/* KPI blocks */
.kpi .value { font-family: 'Montserrat', sans-serif; font-size: 44px; font-weight: 800; line-height: 1; }
.kpi .label { opacity: .9; font-weight: 600; }

/* Alerts */
.stAlert {
  background: #ffe0f0 !important; color: #6a004e !important; border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar: Add Project ----------------
st.sidebar.header("➕ Add Project")
with st.sidebar.form("add_project"):
    name = st.text_input("Project name")
    category = st.selectbox("Category", ["knitting", "painting", "paper", "sewing", "3D", "other"])
    hours = st.number_input("Hours spent", min_value=0.1, step=0.1)
    dt = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("Save")
    if submitted:
        nm = (name or "").strip()
        if not nm:
            st.sidebar.warning("Please enter a project name.")
        else:
            st.session_state["projects"].append(
                {"name": nm, "category": category, "hours": float(hours), "date": dt}
            )
            toast = st.empty()
            toast.success("✅ Project added!")
            time.sleep(1.5)
            toast.empty()

df = pd.DataFrame(st.session_state["projects"])

# ---------------- Slide Nav ----------------
slides = ["dashboard", "intro", "projects", "hours", "top", "charts"]
def next_slide(): st.session_state["slide"] = min(st.session_state["slide"] + 1, len(slides) - 1)
def prev_slide(): st.session_state["slide"] = max(st.session_state["slide"] - 1, 0)

left, right = st.columns([1, 1])
with left:
    if st.button("⬅ Prev"): prev_slide()
with right:
    if st.button("Next ➡"): next_slide()

s = slides[st.session_state["slide"]]
st.markdown("## Craftify Wrapped 🎨")

# ---------------- Helpers ----------------
def kpi_card(label: str, value, grad_class: str = "grad-1"):
    st.markdown(f"""
    <div class="card {grad_class} kpi">
      <div class="label">{label}</div>
      <div class="value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def render_quick_dashboard(data: pd.DataFrame):
    if data.empty:
        st.info("Add a project to unlock your Wrapped!")
        return

    df2 = data.copy()
    df2["date"] = pd.to_datetime(df2["date"])
    df2["hours"] = pd.to_numeric(df2["hours"], errors="coerce").fillna(0.0)

    total_projects = len(df2)
    total_hours = float(df2["hours"].sum())
    avg_hours = round(total_hours / total_projects, 2) if total_projects else 0.0
    by_cat = df2.groupby("category")["hours"].sum().sort_values(ascending=False)
    top_category = by_cat.idxmax() if not by_cat.empty else "—"

    last7_cut = (df2["date"].max() or pd.Timestamp.today()) - timedelta(days=7)
    last7_hours = float(df2[df2["date"] >= last7_cut]["hours"].sum())

    # KPI row (gradient cards)
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: kpi_card("Projects", total_projects, "grad-2")
    with k2: kpi_card("Total Hours", round(total_hours, 1), "grad-3")
    with k3: kpi_card("Avg hrs / project", avg_hours, "grad-4")
    with k4: kpi_card("Top Category", top_category, "grad-5")
    with k5: kpi_card("Last 7 days (hrs)", round(last7_hours, 1), "grad-1")

    # Charts row
    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Hours by Category")
        fig_cat = px.bar(
            by_cat.reset_index(),
            x="category", y="hours",
            labels={"hours": "Hours", "category": "Category"},
            height=360,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_cat.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_cat, use_container_width=True)
    with c2:
        st.subheader("Hours Over Time (Monthly)")
        by_month = df2.groupby(df2["date"].dt.to_period("M"))["hours"].sum().reset_index()
        by_month["date"] = by_month["date"].dt.to_timestamp()
        fig_time = px.area(
            by_month, x="date", y="hours", markers=True, height=360,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_time.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_time, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Recent table
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Recent Projects")
    recent = df2.sort_values("date", ascending=False)[["date", "name", "category", "hours"]].head(10)
    st.dataframe(recent, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Content ----------------
if df.empty:
    st.info("Add a project to unlock your Wrapped!")
else:
    # Normalize numeric & dates once
    df["hours"] = pd.to_numeric(df["hours"], errors="coerce").fillna(0.0)
    df["date"] = pd.to_datetime(df["date"])

    total_projects = len(df)
    total_hours = float(df["hours"].sum())
    by_cat_series = df.groupby("category")["hours"].sum().sort_values(ascending=False)
    top_category = by_cat_series.index[0] if not by_cat_series.empty else "—"

    if s == "dashboard":
        render_quick_dashboard(df)

    elif s == "intro":
        st.markdown('<div class="card grad-1">', unsafe_allow_html=True)
        st.markdown("<h2>Your Year in Making 🎉</h2>", unsafe_allow_html=True)
        st.caption("Use Next ➡ to browse highlights.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif s == "projects":
        st.markdown('<div class="card grad-2">', unsafe_allow_html=True)
        st.markdown('<div class="kpi"><div class="label">Projects Completed</div>'
                    f'<div class="value">{total_projects}</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card" style="margin-top:12px;">', unsafe_allow_html=True)
        st.subheader("All Projects")
        st.dataframe(
            df.sort_values("date", ascending=False)[["date", "name", "category", "hours"]],
            use_container_width=True, hide_index=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    elif s == "hours":
        st.markdown('<div class="card grad-3">', unsafe_allow_html=True)
        st.markdown('<div class="kpi"><div class="label">Hours Creating</div>'
                    f'<div class="value">{round(total_hours, 1)}</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif s == "top":
        st.markdown('<div class="card grad-4">', unsafe_allow_html=True)
        st.markdown('<div class="kpi"><div class="label">Top Category</div>'
                    f'<div class="value">{top_category}</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Top 5 (categories + projects) for extra Wrapped vibe
        st.markdown('<div class="card" style="margin-top:12px;">', unsafe_allow_html=True)
        cA, cB = st.columns(2)
        with cA:
            st.subheader("🏆 Top 5 Categories")
            top5_cat = by_cat_series.head(5)
            for i, (cat, hrs) in enumerate(top5_cat.items(), start=1):
                st.markdown(f"**{i}. {cat.capitalize()}** — {hrs:.1f} hrs")
        with cB:
            st.subheader("🖌️ Top 5 Projects")
            top5_proj = df.sort_values("hours", ascending=False).head(5).reset_index(drop=True)
            for i, row in top5_proj.iterrows():
                st.markdown(f"**{i+1}. {row['name']}** — {row['hours']} hrs ({row['category']})")
        st.markdown("</div>", unsafe_allow_html=True)

    elif s == "charts":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Hours by Category")
        fig = px.pie(
            df, names="category", values="hours",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)