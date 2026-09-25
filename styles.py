import streamlit as st


def load_styles():

    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL APP BACKGROUND
           ===================================================== */

        .stApp {
            background: linear-gradient(
                135deg,
                #f7f8ff 0%,
                #eef1ff 100%
            ) !important;
        }

        [data-testid="stAppViewContainer"] {
            background: transparent !important;
        }

        [data-testid="stMain"] {
            background: transparent !important;
        }

        .block-container {
            max-width: 1450px !important;
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }


        /* =====================================================
           STREAMLIT TOP HEADER
           Remove black top bar
           ===================================================== */

        header[data-testid="stHeader"] {
            background: #f7f8ff !important;
            box-shadow: none !important;
        }

        [data-testid="stHeader"] {
            background: #f7f8ff !important;
        }

        [data-testid="stToolbar"] {
            background: #f7f8ff !important;
        }

        [data-testid="stDecoration"] {
            background: #f7f8ff !important;
        }


        /* =====================================================
           MAIN CONTENT TEXT
           ===================================================== */

        [data-testid="stMain"]
        [data-testid="stMarkdownContainer"] p,

        [data-testid="stMain"]
        [data-testid="stMarkdownContainer"] li,

        [data-testid="stMain"]
        [data-testid="stMarkdownContainer"] span,

        [data-testid="stMain"]
        [data-testid="stMarkdownContainer"] strong,

        [data-testid="stMain"]
        [data-testid="stMarkdownContainer"] em,

        [data-testid="stMain"]
        [data-testid="stMarkdownContainer"] div {
            color: #111827 !important;
            opacity: 1 !important;
        }


        /* =====================================================
           MAIN HEADINGS
           ===================================================== */

        [data-testid="stMain"] h1,
        [data-testid="stMain"] h2,
        [data-testid="stMain"] h3,
        [data-testid="stMain"] h4,
        [data-testid="stMain"] h5,
        [data-testid="stMain"] h6 {
            color: #173b75 !important;
            opacity: 1 !important;
        }


        /* =====================================================
           CAPTIONS
           ===================================================== */

        [data-testid="stMain"]
        [data-testid="stCaptionContainer"] {
            color: #4b5563 !important;
            opacity: 1 !important;
        }


        /* =====================================================
           METRICS / KPI CARDS
           ===================================================== */

        [data-testid="stMetric"] {
            background: #ffffff !important;
            border-radius: 14px !important;
            padding: 14px !important;
            border: 1px solid #e5e7eb !important;
        }

        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] *,
        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] *,
        [data-testid="stMetricDelta"],
        [data-testid="stMetricDelta"] * {
            color: #111827 !important;
            opacity: 1 !important;
        }


        /* =====================================================
           TABS
           ===================================================== */

        [data-testid="stTabs"] button {
            color: #173b75 !important;
            font-weight: 600 !important;
        }

        [data-testid="stTabs"] button[aria-selected="true"] {
            color: #173b75 !important;
            font-weight: 800 !important;
        }


        /* =====================================================
           EXPANDERS
           ===================================================== */

        [data-testid="stExpander"] {
            background: #ffffff !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 12px !important;
        }

        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary *,
        [data-testid="stExpander"] p,
        [data-testid="stExpander"] span {
            color: #111827 !important;
            opacity: 1 !important;
        }


        /* =====================================================
           DATAFRAME / TABLE
           ===================================================== */

        [data-testid="stDataFrame"] {
            background: #ffffff !important;
        }


        /* =====================================================
           MAIN INPUT LABELS
           ===================================================== */

        [data-testid="stMain"]
        [data-testid="stTextInput"] label,

        [data-testid="stMain"]
        [data-testid="stTextInput"] label *,

        [data-testid="stMain"]
        [data-testid="stNumberInput"] label,

        [data-testid="stMain"]
        [data-testid="stNumberInput"] label *,

        [data-testid="stMain"]
        [data-testid="stSelectbox"] label,

        [data-testid="stMain"]
        [data-testid="stSelectbox"] label *,

        [data-testid="stMain"]
        [data-testid="stMultiSelect"] label,

        [data-testid="stMain"]
        [data-testid="stMultiSelect"] label *,

        [data-testid="stMain"]
        [data-testid="stTextArea"] label,

        [data-testid="stMain"]
        [data-testid="stTextArea"] label * {
            color: #111827 !important;
            font-weight: 600 !important;
        }


        /* =====================================================
           MAIN TEXT INPUTS
           ===================================================== */

        [data-testid="stMain"]
        [data-testid="stTextInput"] input,

        [data-testid="stMain"]
        [data-testid="stNumberInput"] input,

        [data-testid="stMain"]
        [data-testid="stTextArea"] textarea {
            color: #111827 !important;
            background: #ffffff !important;
            caret-color: #111827 !important;
        }

        [data-testid="stMain"]
        [data-testid="stTextInput"] input::placeholder,

        [data-testid="stMain"]
        [data-testid="stNumberInput"] input::placeholder,

        [data-testid="stMain"]
        [data-testid="stTextArea"] textarea::placeholder {
            color: #6b7280 !important;
            opacity: 1 !important;
        }


        /* =====================================================
           MAIN SELECTBOX / MULTISELECT
           ===================================================== */

        [data-testid="stMain"]
        [data-testid="stSelectbox"] div,

        [data-testid="stMain"]
        [data-testid="stMultiSelect"] div {
            color: #111827 !important;
        }


        /* =====================================================
           BUTTONS
           ===================================================== */

        .stButton > button,
        .stLinkButton > a {
            font-weight: 600 !important;
        }


        /* =====================================================
           SIDEBAR
           ===================================================== */

        section[data-testid="stSidebar"] {
            background: #111827 !important;
            border-right: 1px solid #1f2937 !important;
        }

        section[data-testid="stSidebar"] > div {
            background: #111827 !important;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            background: #111827 !important;
        }


        /* =====================================================
           SIDEBAR TEXT
           ===================================================== */

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] h5,
        section[data-testid="stSidebar"] h6,
        section[data-testid="stSidebar"] strong {
            color: #ffffff !important;
            opacity: 1 !important;
        }


        /* =====================================================
           SIDEBAR MARKDOWN
           ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stMarkdownContainer"] p,

        section[data-testid="stSidebar"]
        [data-testid="stMarkdownContainer"] span,

        section[data-testid="stSidebar"]
        [data-testid="stMarkdownContainer"] strong,

        section[data-testid="stSidebar"]
        [data-testid="stMarkdownContainer"] div {
            color: #ffffff !important;
            opacity: 1 !important;
        }


        /* =====================================================
           SIDEBAR INPUTS
           ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stTextInput"] input,

        section[data-testid="stSidebar"]
        [data-testid="stNumberInput"] input {
            color: #111827 !important;
            background: #ffffff !important;
            border: 1px solid #d1d5db !important;
        }

        section[data-testid="stSidebar"]
        [data-testid="stTextInput"] input::placeholder,

        section[data-testid="stSidebar"]
        [data-testid="stNumberInput"] input::placeholder {
            color: #6b7280 !important;
            opacity: 1 !important;
        }


        /* =====================================================
           SIDEBAR SELECTBOX
           ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSelectbox"] > div,

        section[data-testid="stSidebar"]
        [data-testid="stMultiSelect"] > div {
            color: #111827 !important;
        }

        section[data-testid="stSidebar"]
        [data-testid="stSelectbox"] div,

        section[data-testid="stSidebar"]
        [data-testid="stMultiSelect"] div {
            color: #111827 !important;
        }


        /* =====================================================
           SIDEBAR BUTTONS
           ===================================================== */

        section[data-testid="stSidebar"]
        .stButton > button {
            background: #1f2937 !important;
            color: #ffffff !important;
            border: 1px solid #374151 !important;
            border-radius: 8px !important;
        }

        section[data-testid="stSidebar"]
        .stButton > button:hover {
            background: #374151 !important;
            color: #ffffff !important;
        }


        /* =====================================================
           SIDEBAR CHECKBOX / RADIO
           ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stCheckbox"] label,

        section[data-testid="stSidebar"]
        [data-testid="stRadio"] label {
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"]
        [data-testid="stCheckbox"] label span,

        section[data-testid="stSidebar"]
        [data-testid="stRadio"] label span {
            color: #ffffff !important;
        }


        /* =====================================================
           SIDEBAR DIVIDER
           ===================================================== */

        section[data-testid="stSidebar"] hr {
            border-color: #374151 !important;
        }


        /* =====================================================
           ALERTS
           ===================================================== */

        [data-testid="stAlert"] p,
        [data-testid="stAlert"] span,
        [data-testid="stAlert"] div {
            opacity: 1 !important;
        }


        /* =====================================================
           JOB / RESUME CONTENT SAFETY
           ===================================================== */

        .live-job-title,
        .live-job-title *,

        .live-job-detail,
        .live-job-detail *,

        .live-job-description,
        .live-job-description *,

        .resume-content,
        .resume-content *,

        .resume-skill,
        .resume-skill *,

        .recommended-job,
        .recommended-job * {
            color: #111827 !important;
            opacity: 1 !important;
        }


        /* =====================================================
           HIDE STREAMLIT DEFAULT MENU / FOOTER
           ===================================================== */

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        </style>
        """,
        unsafe_allow_html=True
    )