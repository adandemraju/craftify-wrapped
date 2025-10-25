import pandas as pd
from datetime import timedelta

def summary(df: pd.DataFrame):
    if df.empty:
        return dict(total_projects=0, total_hours=0.0, top_category="—", last7_hours=0.0, avg_hours=0.0)
    total_projects = len(df)
    total_hours = float(df["hours"].sum())
    avg_hours = round(total_hours/total_projects, 2) if total_projects else 0.0
    by_cat = df.groupby("category")["hours"].sum().sort_values(ascending=False)
    top_category = by_cat.index[0] if not by_cat.empty else "—"
    last7_cut = (df["date"].max()) - timedelta(days=7)
    last7_hours = float(df[df["date"] >= last7_cut]["hours"].sum())
    return dict(total_projects=total_projects, total_hours=total_hours, top_category=top_category,
                last7_hours=last7_hours, avg_hours=avg_hours, by_cat=by_cat)

def monthly_hours(df: pd.DataFrame):
    if df.empty: return pd.DataFrame(columns=["date","hours"])
    by_month = df.groupby(df["date"].dt.to_period("M"))["hours"].sum().reset_index()
    by_month["date"] = by_month["date"].dt.to_timestamp()
    return by_month

def top5_projects(df: pd.DataFrame):
    return df.sort_values("hours", ascending=False).head(5).reset_index(drop=True)
