import streamlit as st

from styles import load_styles
from auth import login_page, register_page
from dashboard import dashboard
from database import get_user


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Job Market & Skill Demand Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD STYLES
# =========================================================

load_styles()


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Login"

if "username" not in st.session_state:
    st.session_state.username = ""


# =========================================================
# PAGE CONTROL
# =========================================================

if st.session_state.logged_in:

    dashboard()

elif st.session_state.page == "Register":

    register_page()

else:

    login_page()
