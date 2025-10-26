import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta
import time
import json

import base64, pathlib

# Path to your font file (make sure fonts/Wonderia.otf exists next to app.py)
FONT_PATH = pathlib.Path("fonts/Wonderia.otf")

# Read and encode the font into base64 so the browser can load it
with open(FONT_PATH, "rb") as f:
    wonderia_b64 = base64.b64encode(f.read()).decode("utf-8")


st.set_page_config(page_title="Craftify Wrapped", page_icon="🎨", layout="wide")

# Data file path
DATA_FILE = "data/projects.json"

# Create data directory if it doesn't exist
pathlib.Path("data").mkdir(exist_ok=True)

# Load data from file
def load_projects():
    """Load projects from JSON file"""
    try:
        if pathlib.Path(DATA_FILE).exists():
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                # Convert date strings back to date objects
                for project in data:
                    project['date'] = date.fromisoformat(project['date'])
                return data
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return []

# Save data to file
def save_projects(projects):
    """Save projects to JSON file"""
    with open(DATA_FILE, 'w') as f:
        # Convert date objects to strings for JSON serialization
        serializable = []
        for project in projects:
            p = project.copy()
            p['date'] = project['date'].isoformat()
            serializable.append(p)
        json.dump(serializable, f, indent=2)

# Initialize session state with loaded data
if "projects" not in st.session_state:
    st.session_state.projects = load_projects()

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

/* Tab label colors - dark pink */
button[data-baseweb="tab"] {{
  color: #cc0066 !important;
  font-weight: 600 !important;
}}
button[data-baseweb="tab"]:hover {{
  color: #ff0066 !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
  color: #cc0066 !important;
}}

/* Change remaining white text to lighter pink */
p, span, label, div, input, select, textarea, code, pre, table {{
  color: #990055 !important;
}}

/* Keep button text white for contrast */
div.stButton > button:first-child,
div.stDownloadButton > button {{
  color: white !important;
}}

/* Keep h1-h6 dark pink */
h1, h2, h3, h4, h5, h6 {{
  color: #cc0066 !important;
}}

/* Keep sidebar text dark pink */
section[data-testid="stSidebar"] * {{
  color: #cc0066 !important;
}}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR: ADD PROJECT ----------
st.sidebar.header("➕ Add Project")

# Get category selection OUTSIDE the form so it updates immediately
category = st.sidebar.selectbox(
    "Category", 
    ["knitting","painting","paper","sewing","3D","other"],
    key="category_select"
)

# Show custom category input if "other" is selected - this will show/hide reactively
custom_category = ""
if category == "other":
    custom_category = st.sidebar.text_input("Enter custom category", key="custom_cat").strip()

# Now the form
with st.sidebar.form("add"):
    name = st.text_input("Project name").strip()
    hours = st.number_input("Hours spent", min_value=0.0, step=0.1)
    dt = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("Save")
    if submitted:
        if not name:
            st.sidebar.warning("Please enter a project name.")
        elif category == "other" and not custom_category:
            st.sidebar.warning("Please enter a custom category.")
        else:
            # Use custom category if provided, otherwise use the selected category
            final_category = custom_category if category == "other" and custom_category else category
            st.session_state["projects"].append({"name": name, "category": final_category, "hours": float(hours), "date": dt})
            # Save to file
            save_projects(st.session_state["projects"])
            msg = st.empty()
            msg.success("✅ Project added!")
            time.sleep(1)
            msg.empty()

# Data management will be moved to top right as icon

df = pd.DataFrame(st.session_state.projects)

# ---------- HEADER ----------
st.markdown("## Craftify Wrapped 🎨")

# ---------- TAB NAVIGATION ----------
slides = {
    "🏠 Home": "intro",
    "📊 Dashboard": "dashboard",
    "🎨 Projects": "projects",
    "⏱️ Hours": "hours",
    "🏆 Top Category": "top",
    "📈 Charts": "charts",
    "📦 Data": "data_management"
}

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

# ---------- CONTENT FUNCTIONS ----------
def render_tab_content(slide_key):
    """Render content for a specific tab"""
    
    # Data management tab - no need to check if df is empty
    if slide_key == "data_management":
        st.markdown("### 📦 Data Management")
        tab1, tab2, tab3 = st.tabs(["Export", "Import", "Clear"])
        
        # Export tab
        with tab1:
            st.markdown("Export your project data as a CSV file.")
            if st.session_state.projects:
                df_export = pd.DataFrame(st.session_state.projects)
                df_export['date'] = df_export['date'].astype(str)
                csv = df_export.to_csv(index=False)
                
                # Custom CSS for button styling
                st.markdown("""
                <style>
                div.stDownloadButton > button {
                    color: white !important;
                }
                div.stDownloadButton > button > div {
                    color: white !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name=f"craftify_data_{date.today()}.csv",
                    mime="text/csv"
                )
                st.markdown(f'<p style="color:black;">Ready to export {len(st.session_state.projects)} projects!</p>', unsafe_allow_html=True)
            else:
                st.info("No data to export yet")
        
        # Import tab
        with tab2:
            st.markdown("Import project data from a CSV file.")
            uploaded_file = st.file_uploader("Upload CSV file", type="csv")
            if uploaded_file is not None:
                try:
                    df_import = pd.read_csv(uploaded_file)
                    if 'date' in df_import.columns:
                        df_import['date'] = pd.to_datetime(df_import['date']).dt.date
                    imported_projects = df_import.to_dict('records')
                    
                    st.success(f"Found {len(imported_projects)} projects in the file.")
                    if st.button("Import Data"):
                        st.session_state["projects"] = imported_projects
                        save_projects(st.session_state["projects"])
                        st.success(f"✅ Imported {len(imported_projects)} projects!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error importing data: {str(e)}")
        
        # Clear tab
        with tab3:
            st.warning("⚠️ This will permanently delete all your data!")
            if st.session_state.projects:
                st.info(f"You currently have {len(st.session_state.projects)} projects.")
                if st.button("🗑️ Clear All Data", type="secondary"):
                    if st.button("⚠️ Confirm Delete", type="primary", key="confirm_del"):
                        st.session_state["projects"] = []
                        save_projects([])
                        st.success("All data cleared!")
                        st.rerun()
            else:
                st.info("No data to clear")
        return
    
    # For other tabs, check if df is empty
    if df.empty:
        st.info("Add a project to unlock your Wrapped!")
        return
    
    total_projects = len(df)
    total_hours = df["hours"].sum()
    top_category = df.groupby("category")["hours"].sum().idxmax()

    if slide_key=="dashboard":
        render_quick_dashboard(df)
    elif slide_key=="intro":
        st.markdown("# Welcome to Craftify Wrapped 🎨")
        st.markdown("---")
        st.markdown("### Track your creative journey")
        st.markdown("""
        **Craftify Wrapped** is your personal analytics dashboard for tracking all your creative projects!
        
        Get insights into:
        - 📊 Your project statistics and trends
        - 🎨 Your most worked-on categories
        - ⏱️ Total hours spent creating
        - 📈 Beautiful visualizations of your work
        
        **Get started:** Use the sidebar to add your first project!
        """)
        st.markdown("---")
        
        # Show quick stats if available
        if not df.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Projects", total_projects)
            with col2:
                st.metric("Total Hours", f"{round(total_hours, 1)} hrs")
            with col3:
                st.metric("Top Category", top_category)
    elif slide_key=="projects":
        st.metric("Total Projects", total_projects)
        st.dataframe(df.sort_values("date", ascending=False)[["date","name","category","hours"]],
                    use_container_width=True, hide_index=True)
    elif slide_key=="hours":
        st.metric("Total Hours", round(total_hours,1))
    elif slide_key=="top":
        st.metric("Top Category", top_category)
    elif slide_key=="charts":
        fig = px.pie(df, names="category", values="hours", title="Hours by Category",
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

# ---------- CREATE TABS ----------
tab_list = list(slides.keys())
tabs = st.tabs(tab_list)

# Render content for each tab
for idx, (tab_name, slide_key) in enumerate(slides.items()):
    with tabs[idx]:
        render_tab_content(slide_key)