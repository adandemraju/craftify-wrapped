import streamlit as st

def inject():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    .stApp {
      background: radial-gradient(1200px 800px at 10% 10%, #fff0f6 0%, #ffd6e8 35%, #ffffff 75%);
      color: #2b0040;
    }
    section[data-testid="stSidebar"] {
      background: linear-gradient(180deg, #fff0f6 0%, #ffe6f0 100%) !important;
      border-right: 1px solid #ffd1e3;
    }
    section[data-testid="stSidebar"] * { color: #a0005a !important; }

    div.stButton > button:first-child {
      background: #ff66b2; color: #fff; border: none;
      border-radius: 14px; padding: 0.7rem 1.1rem; font-weight: 700;
      box-shadow: 0 10px 20px rgba(255,102,178,.25);
      transition: transform .15s ease, box-shadow .15s ease;
    }
    div.stButton > button:first-child:hover {
      transform: translateY(-2px) scale(1.02);
      box-shadow: 0 14px 26px rgba(255,102,178,.35);
    }

    h1, h2, h3, h4 { color: #8a0066; font-family: 'Montserrat', sans-serif; font-weight: 800; }

    .card {
      border-radius: 24px; padding: 22px; background: #ffffffcc;
      border: 1px solid #ffd1e3; box-shadow: 0 18px 40px rgba(170, 0, 102, 0.08);
    }
    .grad-1 { background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); color: #fff; }
    .grad-2 { background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%); color: #fff; }
    .grad-3 { background: linear-gradient(135deg, #ff9966 0%, #ff5e62 100%); color: #fff; }
    .grad-4 { background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); color: #fff; }
    .grad-5 { background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%); color: #fff; }

    .kpi .value { font-family: 'Montserrat', sans-serif; font-size: 44px; font-weight: 800; line-height: 1; }
    .kpi .label { opacity: .9; font-weight: 600; }

    .stAlert { background: #ffe0f0 !important; color: #6a004e !important; border-radius: 14px; }

    .fade-out { animation: fadeOut 1.2s ease forwards; }
    @keyframes fadeOut { 0%{opacity:1} 100%{opacity:0} }
    </style>
    """, unsafe_allow_html=True)