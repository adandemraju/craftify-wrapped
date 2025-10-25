import streamlit as st
import json, io
import pandas as pd

KEY = "projects"

def init_state():
    if KEY not in st.session_state:
        st.session_state[KEY] = []

def add_project(name: str, category: str, hours: float, date_str: str):
    st.session_state[KEY].append({
        "name": name, "category": category, "hours": float(hours), "date": date_str
    })

def get_projects_df() -> pd.DataFrame:
    df = pd.DataFrame(st.session_state.get(KEY, []))
    if not df.empty:
        df["hours"] = pd.to_numeric(df["hours"], errors="coerce").fillna(0.0)
        df["date"] = pd.to_datetime(df["date"])
    return df

def download_json_button(label: str = "Download JSON"):
    buf = io.StringIO()
    json.dump(st.session_state.get(KEY, []), buf, indent=2)
    return st.download_button(label, buf.getvalue(), file_name="projects.json", mime="application/json")

def upload_json(file):
    data = json.load(file)
    if isinstance(data, list):
        st.session_state[KEY] = data
        return True
    return False

def download_csv_button(label: str = "Download CSV"):
    df = pd.DataFrame(st.session_state.get(KEY, []))
    csv = df.to_csv(index=False).encode("utf-8")
    return st.download_button(label, csv, "projects.csv", "text/csv")
