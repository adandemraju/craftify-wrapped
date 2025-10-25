CSS = """
<style>
    .stApp { background: linear-gradient(180deg, #ffd6e8 0%, #fff0f6 100%); color: #4a0033; }
    section[data-testid="stSidebar"] { background-color: #ffe6f0 !important; color: #cc0066 !important; }
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] div, 
    section[data-testid="stSidebar"] span {
        color: #cc0066 !important; font-weight: 600;
    }
    div.stButton > button:first-child {
        background-color: #ff66b2; color: white; border: none; border-radius: 12px;
        height: 3em; width: 8em; font-weight: 600; transition: 0.3s;
    }
    div.stButton > button:first-child:hover { background-color: #ff3385; transform: scale(1.05); }
    .stAlert { background-color: #ffcce0 !important; color: #800040 !important; border-radius: 10px; font-weight: 500; }
    h1, h2, h3, h4, h5, h6 { color: #cc0066 !important; font-family: 'Poppins', sans-serif; }
    .card { background: #ffffffcc; border: 1px solid #ffd1e3; border-radius: 16px; padding: 16px; box-shadow: 0 6px 18px rgba(204,0,102,.1); }
</style>
"""
