import streamlit as st


# =========================================================
# OVERVIEW TAB
# =========================================================

def overview_tab(
    filtered_df,
    role_counts,
    skill_counts,
    company_column
):

    st.subheader(
        "📊 Market Overview"
    )

    # -----------------------------------------------------
    # JOB ROLE DEMAND
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "#### 💼 Top Job Roles"
        )

        if role_counts.empty:

            st.info(
                "Job role data is not available."
            )

        else:

            chart = (
                role_counts
                .head(10)
                .sort_values()
            )

            st.bar_chart(
                chart,
                horizontal=True,
                height=400
            )

    # -----------------------------------------------------
    # COMPANY DEMAND
    # -----------------------------------------------------

    with col2:

        st.markdown(
            "#### 🏢 Top Hiring Companies"
        )

        if company_column is None:

            st.info(
                "Company data is not available."
            )

        else:

            companies = (
                filtered_df[company_column]
                .dropna()
                .astype(str)
                .str.strip()
                .value_counts()
                .head(10)
                .sort_values()
            )

            if companies.empty:

                st.info(
                    "Company data is not available."
                )

            else:

                st.bar_chart(
                    companies,
                    horizontal=True,
                    height=400
                )

    st.divider()

    # -----------------------------------------------------
    # TOP SKILLS
    # -----------------------------------------------------

    st.subheader(
        "🔥 Skill Demand"
    )

    if skill_counts.empty:

        st.warning(
            "No skill column was found."
        )

    else:

        top_skills = (
            skill_counts
            .head(15)
            .sort_values()
        )

        st.bar_chart(
            top_skills,
            horizontal=True,
            height=500
        )