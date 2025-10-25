import streamlit as st
import plotly.express as px
import pandas as pd

def kpi_card(label: str, value, grad_class: str = "grad-1"):
    st.markdown(f"""
        <div class="card {grad_class} kpi">
          <div class="label">{label}</div>
          <div class="value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

def bar_category(by_cat: pd.Series):
    fig = px.bar(
        by_cat.reset_index(), x="category", y="hours",
        labels={"hours":"Hours","category":"Category"},
        height=360, color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)

def area_monthly(by_month: pd.DataFrame):
    fig = px.area(by_month, x="date", y="hours", markers=True, height=360,
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)

def pie_category(df: pd.DataFrame):
    fig = px.pie(df, names="category", values="hours",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)
