import streamlit as st
from data_loader import find_column


def normalize_filter_value(value):
    return (
        str(value)
        .strip()
        .lower()
        .replace("–", "-")
        .replace("—", "-")
    )


def reset_filters():
    st.session_state["reset_filters_triggered"] = True


def sidebar_filters(df):

    # =====================================================
    # RESET CHECK
    # =====================================================

    if st.session_state.get("reset_filters_triggered", False):

        st.session_state.pop("selected_location", None)
        st.session_state.pop("selected_roles", None)
        st.session_state.pop("selected_experience", None)

        st.session_state["reset_filters_triggered"] = False

        st.rerun()

    # =====================================================
    # MARKET FILTERS TITLE
    # =====================================================

    st.sidebar.markdown(
        """
        <div style="
            color: #ffffff !important;
            font-size: 21px;
            font-weight: 800;
            margin-bottom: 18px;
        ">
            🔎 Market Filters
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # LOCATION
    # =====================================================

    location_column = find_column(
        df,
        ["Location", "City", "Job Location", "Work Location"]
    )

    if location_column:

        locations = sorted(
            df[location_column]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        selected_location = st.sidebar.multiselect(
            "📍 Location",
            locations,
            key="selected_location"
        )

    else:
        selected_location = []

    # =====================================================
    # JOB ROLE
    # =====================================================

    role_column = find_column(
        df,
        ["Job Role", "Job Title", "Role", "Title", "Position", "Job"]
    )

    if role_column:

        roles = sorted(
            df[role_column]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        selected_roles = st.sidebar.multiselect(
            "💼 Job Role",
            roles,
            key="selected_roles"
        )

    else:
        selected_roles = []

    # =====================================================
    # EXPERIENCE
    # =====================================================

    experience_column = find_column(
        df,
        [
            "Experience",
            "Experience Level",
            "Years of Experience",
            "Experience Required"
        ]
    )

    if experience_column:

        experiences = sorted(
            df[experience_column]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        selected_experience = st.sidebar.multiselect(
            "🧑‍💻 Experience",
            experiences,
            key="selected_experience"
        )

    else:
        selected_experience = []

    # =====================================================
    # RESET BUTTON
    # =====================================================

    st.sidebar.button(
        "🔄 Reset All Filters",
        use_container_width=True,
        on_click=reset_filters,
        key="reset_filters_button"
    )

    # =====================================================
    # RETURN FILTERS
    # =====================================================

    return (
        location_column,
        role_column,
        experience_column,
        selected_location,
        selected_roles,
        selected_experience
    )


def apply_filters(
    df,
    location_column,
    role_column,
    experience_column,
    selected_location,
    selected_roles,
    selected_experience
):

    filtered_df = df.copy()

    # =====================================================
    # LOCATION FILTER
    # =====================================================

    if location_column and selected_location:

        selected_locations = {
            normalize_filter_value(value)
            for value in selected_location
        }

        filtered_df = filtered_df[
            filtered_df[location_column]
            .astype(str)
            .map(normalize_filter_value)
            .isin(selected_locations)
        ]

    # =====================================================
    # JOB ROLE FILTER
    # =====================================================

    if role_column and selected_roles:

        selected_role_values = {
            normalize_filter_value(value)
            for value in selected_roles
        }

        filtered_df = filtered_df[
            filtered_df[role_column]
            .astype(str)
            .map(normalize_filter_value)
            .isin(selected_role_values)
        ]

    # =====================================================
    # EXPERIENCE FILTER
    # =====================================================

    if experience_column and selected_experience:

        selected_experience_values = {
            normalize_filter_value(value)
            for value in selected_experience
        }

        filtered_df = filtered_df[
            filtered_df[experience_column]
            .astype(str)
            .map(normalize_filter_value)
            .isin(selected_experience_values)
        ]

    return filtered_df.reset_index(drop=True)