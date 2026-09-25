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

        # -------------------------------------------------
        # PREDEFINED LOCATIONS
        # -------------------------------------------------

        predefined_locations = [

            # General
            "All India",

            # Mumbai
            "Mumbai",
            "Andheri",
            "Borivali",
            "Bandra",
            "Powai",
            "Goregaon",
            "Malad",
            "Thane",
            "Kalyan",
            "Dombivli",
            "Navi Mumbai",

            # Pune
            "Pune",
            "Hinjewadi",
            "Kharadi",
            "Wakad",
            "Viman Nagar",
            "Hadapsar",

            # Delhi NCR
            "Delhi",
            "Noida",
            "Greater Noida",
            "Gurugram",
            "Ghaziabad",
            "Faridabad",

            # Bengaluru
            "Bengaluru",
            "Whitefield",
            "Electronic City",
            "Koramangala",
            "Marathahalli",

            # Hyderabad
            "Hyderabad",
            "Hitech City",
            "Gachibowli",
            "Madhapur"
        ]

        # -------------------------------------------------
        # INDIA STATES
        # -------------------------------------------------

        india_states = [
            "Andhra Pradesh",
            "Arunachal Pradesh",
            "Assam",
            "Bihar",
            "Chhattisgarh",
            "Goa",
            "Gujarat",
            "Haryana",
            "Himachal Pradesh",
            "Jharkhand",
            "Karnataka",
            "Kerala",
            "Madhya Pradesh",
            "Maharashtra",
            "Manipur",
            "Meghalaya",
            "Mizoram",
            "Nagaland",
            "Odisha",
            "Punjab",
            "Rajasthan",
            "Sikkim",
            "Tamil Nadu",
            "Telangana",
            "Tripura",
            "Uttar Pradesh",
            "Uttarakhand",
            "West Bengal"
        ]

        # -------------------------------------------------
        # ADD LOCATIONS FROM DATASET
        # -------------------------------------------------

        dataset_locations = (
            df[location_column]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        # Combine predefined + states + dataset locations
        all_locations = sorted(
            set(
                predefined_locations
                + india_states
                + dataset_locations
            ),
            key=lambda x: (
                x != "All India",
                x.lower()
            )
        )

        selected_location = st.sidebar.multiselect(
            "📍 Location",
            all_locations,
            key="selected_location"
        )

    else:
        selected_location = []

    # =====================================================
    # JOB ROLE
    # =====================================================

    role_column = find_column(
        df,
        [
            "Job Role",
            "Job Title",
            "Role",
            "Title",
            "Position",
            "Job"
        ]
    )

    if role_column:

        # -------------------------------------------------
        # PREDEFINED JOB ROLES
        # -------------------------------------------------

        predefined_roles = [

            # Data & Analytics
            "Data Analyst",
            "Data Scientist",
            "Data Engineer",
            "Business Analyst",
            "BI Analyst",
            "Data Visualization Analyst",
            "Machine Learning Engineer",
            "AI Engineer",

            # Software & Development
            "Software Developer",
            "Software Engineer",
            "Python Developer",
            "Java Developer",
            "Full Stack Developer",
            "Frontend Developer",
            "Backend Developer",
            "Web Developer",
            "Mobile App Developer",

            # Cloud & DevOps
            "Cloud Engineer",
            "Cloud Architect",
            "DevOps Engineer",
            "Site Reliability Engineer",
            "System Engineer",
            "Network Engineer",

            # Cybersecurity
            "Cybersecurity Analyst",
            "Security Engineer",
            "Information Security Analyst",
            "SOC Analyst",
            "Ethical Hacker",

            # Testing & Quality
            "QA Engineer",
            "Software Tester",
            "Automation Tester",
            "Test Engineer",

            # Business & Management
            "Product Manager",
            "Project Manager",
            "Product Analyst",
            "Business Consultant",
            "Business Intelligence Analyst",

            # Design
            "UI/UX Designer",
            "UX Designer",
            "Graphic Designer",
            "Product Designer",

            # IT & Other Technology
            "Database Administrator",
            "System Administrator",
            "Technical Support Engineer",
            "IT Support Specialist",
            "Solutions Architect",
            "Technical Consultant"
        ]

        # -------------------------------------------------
        # ADD ROLES FROM DATASET
        # -------------------------------------------------

        dataset_roles = (
            df[role_column]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        all_roles = sorted(
            set(predefined_roles + dataset_roles),
            key=lambda x: x.lower()
        )

        selected_roles = st.sidebar.multiselect(
            "💼 Job Role",
            all_roles,
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

        # -------------------------------------------------
        # PREDEFINED EXPERIENCE OPTIONS
        # -------------------------------------------------

        predefined_experience = [
            "Fresher",
            "0-1 Years",
            "1-3 Years",
            "2-4 Years",
            "2-5 Years",
            "3-5 Years",
            "5-8 Years",
            "8+ Years"
        ]

        # -------------------------------------------------
        # ADD EXPERIENCE FROM DATASET
        # -------------------------------------------------

        dataset_experience = (
            df[experience_column]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        all_experience = sorted(
            set(
                predefined_experience
                + dataset_experience
            ),
            key=lambda x: x.lower()
        )

        selected_experience = st.sidebar.multiselect(
            "🧑‍💻 Experience",
            all_experience,
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

        # If "All India" is selected,
        # do not apply location restriction.
        if "All India" not in selected_location:

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