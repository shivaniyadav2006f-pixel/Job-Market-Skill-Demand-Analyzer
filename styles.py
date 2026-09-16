import streamlit as st


def load_styles():

    st.markdown(
        """
        <style>

        /* =================================================
           GLOBAL APP
           ================================================= */

        .stApp {
            background:
                radial-gradient(
                    circle at 10% 10%,
                    rgba(99, 102, 241, 0.10),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 90% 10%,
                    rgba(139, 92, 246, 0.08),
                    transparent 28%
                ),
                linear-gradient(
                    135deg,
                    #f8f9ff 0%,
                    #f5f7ff 50%,
                    #fbfcff 100%
                );
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            background: transparent;
        }

        .block-container {
            padding-top: 28px;
            padding-bottom: 40px;
            max-width: 1450px;
        }


        /* =================================================
           HEADINGS
           ================================================= */

        h1, h2, h3, h4, h5, h6 {
            color: #172554 !important;
        }

        .main-title {
            color: #172554 !important;
            font-size: 38px;
            font-weight: 800;
            text-align: center;
            line-height: 1.15;
        }

        .subtitle {
            color: #000000 !important;
            text-align: center;
            font-size: 16px;
            margin-bottom: 25px;
        }

        .section-title {
            color: #172554 !important;
            font-size: 25px;
            font-weight: 800;
            margin-top: 20px;
        }


        /* =================================================
           LOGIN PAGE TEXT
           ================================================= */

        [data-testid="stTextInput"] label,
        [data-testid="stTextInput"] label p {
            color: #000000 !important;
            font-weight: 600 !important;
        }

        [data-testid="stTextInput"] input {
            color: #000000 !important;
        }

        [data-testid="stTextInput"] input::placeholder {
            color: #000000 !important;
            opacity: 1 !important;
        }


        /* =================================================
           SIDEBAR
           ================================================= */

        [data-testid="stSidebar"] {
            background: #111827 !important;
            border-right: 1px solid #1f2937;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 22px;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4 {
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] label {
            color: #ffffff !important;
            font-weight: 600 !important;
        }

        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span {
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] .stMarkdown {
            color: #ffffff !important;
        }


        /* =================================================
           SIDEBAR INPUTS
           ================================================= */

        [data-testid="stSidebar"] [data-baseweb="select"] {
            background: #1f2937 !important;
            border: 1px solid #374151 !important;
            border-radius: 10px !important;
        }

        [data-testid="stSidebar"] [data-baseweb="select"] * {
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] input {
            color: #ffffff !important;
        }


        /* =================================================
           BUTTONS
           ================================================= */

        .stButton > button {
            border-radius: 10px !important;
            border: none !important;
            min-height: 44px !important;
            font-weight: 700 !important;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            opacity: 0.94;
        }

        [data-testid="stSidebar"] .stButton > button {
            background: #374151 !important;
            color: #ffffff !important;
            border: 1px solid #4b5563 !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: #4b5563 !important;
        }


        /* =================================================
           METRIC CARDS
           ================================================= */

        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 18px 18px 14px 18px;
            box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
        }

        [data-testid="stMetricLabel"] {
            color: #000000 !important;
            font-weight: 600 !important;
        }

        [data-testid="stMetricValue"] {
            color: #172554 !important;
            font-weight: 800 !important;
        }

        [data-testid="stMetricDelta"] {
            color: #000000 !important;
        }


        

        /* =================================================
   TABS
   ================================================= */

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #ffffff !important;
    padding: 8px;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
}

/* Every tab */
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    padding: 12px 20px !important;
    font-weight: 700 !important;
    color: #000000 !important;
    background: #ffffff !important;
    opacity: 1 !important;
}

/* Tab text */
.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span,
.stTabs [data-baseweb="tab"] div {
    color: #000000 !important;
    opacity: 1 !important;
    font-weight: 700 !important;
}

/* Selected tab */
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: #eef2ff !important;
    color: #000000 !important;
    opacity: 1 !important;
}

/* Selected tab text */
.stTabs [data-baseweb="tab"][aria-selected="true"] p,
.stTabs [data-baseweb="tab"][aria-selected="true"] span,
.stTabs [data-baseweb="tab"][aria-selected="true"] div {
    color: #000000 !important;
    opacity: 1 !important;
    font-weight: 800 !important;
}

/* Tab hover */
.stTabs [data-baseweb="tab"]:hover {
    background: #f1f5f9 !important;
    color: #000000 !important;
}

/* Active underline */
.stTabs [data-baseweb="tab-highlight"] {
    background: #000000 !important;
}

        /* =================================================
           EXPANDER
           ================================================= */

        [data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.85);
            border: 1px solid #e2e8f0;
            border-radius: 14px;
        }

        [data-testid="stExpander"] p,
        [data-testid="stExpander"] span {
            color: #000000 !important;
        }


        /* =================================================
           DIVIDERS
           ================================================= */

        hr {
            border-color: #e2e8f0 !important;
        }


        /* =================================================
           CAPTIONS
           ================================================= */

        [data-testid="stCaptionContainer"] {
            color: #000000 !important;
        }

        [data-testid="stCaptionContainer"] p {
            color: #000000 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )