import streamlit as st
import importlib

from data_loader import load_data, find_column
from filters import sidebar_filters, apply_filters
from analytics import get_skill_counts, get_role_counts

from tabs.overview import overview_tab
from tabs.skills import skills_tab
from tabs.career import career_tab
from tabs.salary import salary_tab
from tabs.explorer import explorer_tab
from resume_matcher import resume_matcher_tab
from live_jobs import live_jobs_tab

from database import (
    get_user,
    update_profile,
    change_password,
    delete_user
)


# =========================================================
# SESSION PREFERENCES
# =========================================================

def init_preferences():

    if "show_dataset_info" not in st.session_state:
        st.session_state.show_dataset_info = True

    if "show_welcome" not in st.session_state:
        st.session_state.show_welcome = True

    if "show_footer" not in st.session_state:
        st.session_state.show_footer = True


# =========================================================
# LOGOUT
# =========================================================

def logout():

    st.session_state.logged_in = False
    st.session_state.page = "Login"

    st.session_state.pop("username", None)

    st.rerun()


# =========================================================
# PROFILE PAGE
# =========================================================

def profile_page():

    st.title("👤 My Profile")

    username = st.session_state.get("username", "")

    user = get_user(username)

    if not user:
        st.error("User profile not found.")
        return

    st.markdown("### Profile Information")

    with st.form("profile_form"):

        new_username = st.text_input(
            "Username",
            value=user["username"]
        )

        email = st.text_input(
            "Email",
            value=user.get("email", "")
        )

        save = st.form_submit_button(
            "💾 Save Changes",
            use_container_width=True
        )

        if save:

            new_username = new_username.strip()
            email = email.strip()

            if not new_username:

                st.error("Username cannot be empty.")

            else:

                success = update_profile(
                    user["username"],
                    new_username,
                    email
                )

                if success:

                    st.session_state.username = new_username

                    st.success(
                        "Profile updated successfully!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Username already exists or update failed."
                    )


# =========================================================
# SETTINGS PAGE
# =========================================================

def settings_page():

    st.title("⚙️ Settings")

    username = st.session_state.get("username", "")

    # =====================================================
    # PASSWORD
    # =====================================================

    st.markdown("### 🔐 Change Password")

    with st.form("password_form"):

        current_password = st.text_input(
            "Current Password",
            type="password"
        )

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm New Password",
            type="password"
        )

        change = st.form_submit_button(
            "🔑 Change Password",
            use_container_width=True
        )

        if change:

            if (
                not current_password
                or not new_password
                or not confirm_password
            ):

                st.error(
                    "Please fill all password fields."
                )

            elif new_password != confirm_password:

                st.error(
                    "New passwords do not match."
                )

            elif len(new_password) < 6:

                st.error(
                    "Password must be at least 6 characters."
                )

            else:

                success = change_password(
                    username,
                    current_password,
                    new_password
                )

                if success:

                    st.success(
                        "Password changed successfully!"
                    )

                else:

                    st.error(
                        "Current password is incorrect."
                    )

    st.divider()

    # =====================================================
    # DELETE ACCOUNT
    # =====================================================

    st.markdown("### 🗑️ Delete Account")

    st.warning(
        "Deleting your account cannot be undone."
    )

    if st.button(
        "🗑️ Delete My Account",
        use_container_width=True,
        key="delete_account_button"
    ):

        success = delete_user(username)

        if success:

            st.session_state.logged_in = False
            st.session_state.page = "Login"

            st.session_state.pop(
                "username",
                None
            )

            st.success(
                "Account deleted successfully."
            )

            st.rerun()

        else:

            st.error(
                "Unable to delete account."
            )


# =========================================================
# SIDEBAR ACCOUNT
# =========================================================

def sidebar_account():

    username = st.session_state.get(
        "username",
        "User"
    )

    st.sidebar.markdown(
        """
        <div style="
            color: #ffffff;
            font-size: 20px;
            font-weight: 800;
            margin-top: 10px;
            margin-bottom: 8px;
        ">
            👤 Account
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        """
        <div style="
            color: #cbd5e1;
            font-size: 13px;
            margin-bottom: 3px;
        ">
            Logged in as
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        f"""
        <div style="
            color: #ffffff;
            font-size: 17px;
            font-weight: 700;
            margin-bottom: 12px;
        ">
            👤 {username}
        </div>
        """,
        unsafe_allow_html=True
    )

    account_page = st.sidebar.radio(
        "Account Menu",
        [
            "🏠 Dashboard",
            "👤 Profile",
            "⚙️ Settings"
        ],
        key="account_navigation"
    )

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True,
        key="logout_button"
    ):

        logout()

    return account_page


# =========================================================
# DASHBOARD SETTINGS
# =========================================================

def sidebar_settings():

    if "settings_open" not in st.session_state:
        st.session_state.settings_open = False

    if st.sidebar.button(
        "🎛️ Dashboard Display",
        use_container_width=True,
        key="display_settings_button"
    ):

        st.session_state.settings_open = (
            not st.session_state.settings_open
        )

        st.rerun()

    if st.session_state.settings_open:

        st.sidebar.markdown(
            """
            <div style="
                color: #ffffff;
                font-size: 18px;
                font-weight: 800;
                margin-top: 12px;
                margin-bottom: 12px;
            ">
                🎛️ Dashboard Display
            </div>
            """,
            unsafe_allow_html=True
        )

        st.sidebar.checkbox(
            "👋 Show welcome message",
            key="show_welcome"
        )

        st.sidebar.checkbox(
            "ℹ️ Show dataset information",
            key="show_dataset_info"
        )

        st.sidebar.checkbox(
            "📌 Show footer",
            key="show_footer"
        )

        st.sidebar.markdown(
            """
            <div style="
                color: #94a3b8;
                font-size: 12px;
                margin-top: 10px;
                line-height: 1.5;
            ">
                Preferences are saved during this session.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.sidebar.divider()


# =========================================================
# DASHBOARD HEADER
# =========================================================

def dashboard_header():

    username = st.session_state.get(
        "username",
        "User"
    )

    st.title(
        "📊 Job Market Intelligence Dashboard"
    )

    st.caption(
        "Analyze hiring demand, skills, companies, "
        "salary trends and career opportunities "
        "using your job-market dataset."
    )

    st.divider()


# =========================================================
# KPI SECTION
# =========================================================

def show_kpis(
    df,
    skill_counts,
    role_counts,
    company_column
):

    total_jobs = len(df)

    unique_companies = (
        df[company_column]
        .dropna()
        .nunique()
        if company_column
        else 0
    )

    unique_roles = len(role_counts)

    unique_skills = len(skill_counts)

    top_skill = (
        skill_counts.index[0]
        if not skill_counts.empty
        else "N/A"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "💼 Total Jobs",
            f"{total_jobs:,}"
        )

    with col2:

        st.metric(
            "🏢 Companies",
            f"{unique_companies:,}"
        )

    with col3:

        st.metric(
            "📈 Job Roles",
            f"{unique_roles:,}"
        )

    with col4:

        st.metric(
            "🧠 Unique Skills",
            f"{unique_skills:,}"
        )

    with col5:

        st.metric(
            "🔥 Top Skill",
            top_skill
        )


# =========================================================
# DATASET INFORMATION
# =========================================================

def dataset_info(df):

    with st.expander(
        "ℹ️ Dataset Information"
    ):

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Rows",
                f"{len(df):,}"
            )

        with col2:

            st.metric(
                "Columns",
                f"{len(df.columns):,}"
            )

        with col3:

            missing_values = int(
                df.isna().sum().sum()
            )

            st.metric(
                "Missing Values",
                f"{missing_values:,}"
            )

        st.write(
            "**Available Columns:**"
        )

        st.write(
            ", ".join(
                str(column)
                for column in df.columns
            )
        )


# =========================================================
# PROFESSIONAL FOOTER
# =========================================================

def dashboard_footer():

    if not st.session_state.show_footer:
        return

    st.divider()

    st.caption(
        "📊 Job Market & Skill Demand Analyzer"
    )

    st.caption(
        "Career Intelligence Platform • Analyze • Discover • Grow"
    )


# =========================================================
# MAIN DASHBOARD
# =========================================================

def dashboard():

    # -----------------------------------------------------
    # SESSION PREFERENCES
    # -----------------------------------------------------

    init_preferences()

    # -----------------------------------------------------
    # SIDEBAR ACCOUNT
    # -----------------------------------------------------

    account_page = sidebar_account()

    # -----------------------------------------------------
    # PROFILE
    # -----------------------------------------------------

    if account_page == "👤 Profile":

        profile_page()

        return

    # -----------------------------------------------------
    # SETTINGS
    # -----------------------------------------------------

    if account_page == "⚙️ Settings":

        settings_page()

        return

    # -----------------------------------------------------
    # LOAD DATA
    # -----------------------------------------------------

    df = load_data()

    if df is None:

        st.error(
            "❌ job_market.csv was not found."
        )

        st.info(
            "Place job_market.csv in the same "
            "folder as app.py."
        )

        st.stop()

    if df.empty:

        st.warning(
            "The dataset is empty."
        )

        st.stop()

    # -----------------------------------------------------
    # DASHBOARD DISPLAY SETTINGS
    # -----------------------------------------------------

    sidebar_settings()

    # -----------------------------------------------------
    # MARKET FILTERS
    # -----------------------------------------------------

    (
        location_column,
        role_column,
        experience_column,
        selected_location,
        selected_roles,
        selected_experience
    ) = sidebar_filters(df)

    # -----------------------------------------------------
    # LIVE API CONTROL
    # -----------------------------------------------------

    st.sidebar.divider()

    st.sidebar.markdown(
        "### 🌐 Live Job API"
    )

    use_live_api = st.sidebar.checkbox(
        "Enable Live Job API",
        value=True,
        key="use_live_job_api"
    )

    if use_live_api:

        st.sidebar.caption(
            "Selected Job Role and Location will be used "
            "for live job search."
        )

    else:

        st.sidebar.caption(
            "Live API search is disabled."
        )

    # -----------------------------------------------------
    # APPLY FILTERS
    # -----------------------------------------------------

    filtered_df = apply_filters(
        df,
        location_column,
        role_column,
        experience_column,
        selected_location,
        selected_roles,
        selected_experience
    )

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    dashboard_header()

    # -----------------------------------------------------
    # FILTER MESSAGE
    # -----------------------------------------------------

    if len(filtered_df) != len(df):

        st.info(
            f"🔎 Filters active: showing "
            f"**{len(filtered_df):,}** "
            f"of **{len(df):,}** jobs."
        )

    # -----------------------------------------------------
    # ANALYTICS
    # -----------------------------------------------------

    skill_counts = get_skill_counts(
        filtered_df
    )

    role_counts = get_role_counts(
        filtered_df
    )

    # -----------------------------------------------------
    # COMPANY COLUMN
    # -----------------------------------------------------

    company_column = find_column(
        filtered_df,
        [
            "Company",
            "Company Name",
            "Employer",
            "Organization"
        ]
    )

    # -----------------------------------------------------
    # KPI
    # -----------------------------------------------------

    filter_applied = (
        bool(selected_location)
        or bool(selected_roles)
        or bool(selected_experience)
    )

    if filter_applied:

        show_kpis(
            filtered_df,
            skill_counts,
            role_counts,
            company_column
        )

        st.write("")

    else:

        st.info(
            "🔎 Please select a Market Filter to view "
            "job-market KPIs and insights."
        )

    # -----------------------------------------------------
    # DATASET INFORMATION
    # -----------------------------------------------------

    if st.session_state.show_dataset_info:

        dataset_info(
            filtered_df
        )

    # -----------------------------------------------------
    # TABS
    # -----------------------------------------------------

    tab_labels = [
        "📊 Overview",
        "🧠 Skill Intelligence",
        "🎯 Career Intelligence",
        "💰 Salary Intelligence",
        "📄 Data Explorer",
        "📄 Resume Matcher",
        "🌐 Live Jobs"
    ]

    dashboard_tabs = st.tabs(tab_labels)

    (
        overview,
        skills,
        career,
        salary,
        explorer,
        resume_matcher,
        live_jobs
    ) = dashboard_tabs

    # -----------------------------------------------------
    # OVERVIEW
    # -----------------------------------------------------

    with overview:

        overview_tab(
            filtered_df,
            role_counts,
            skill_counts,
            company_column
        )

    # -----------------------------------------------------
    # SKILLS
    # -----------------------------------------------------

    with skills:

        skills_tab(
            filtered_df,
            skill_counts
        )

    # -----------------------------------------------------
    # CAREER
    # -----------------------------------------------------

    with career:

        career_tab(
            filtered_df,
            role_column,
            location_column,
            experience_column,
            skill_counts
        )

    # -----------------------------------------------------
    # SALARY
    # -----------------------------------------------------

    with salary:

        salary_tab(
            filtered_df,
            role_column
        )

    # -----------------------------------------------------
    # DATA EXPLORER
    # -----------------------------------------------------

    with explorer:

        explorer_tab(
            filtered_df
        )

    # -----------------------------------------------------
    # RESUME MATCHER
    # -----------------------------------------------------

    with resume_matcher:

        resume_matcher_tab(
            filtered_df
        )

    # -----------------------------------------------------
    # LIVE JOBS
    # -----------------------------------------------------

    with live_jobs:

        if live_jobs_tab is None:

            st.error(
                "❌ live_jobs.py could not be imported."
            )

        else:

            live_jobs_tab()

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    dashboard_footer()