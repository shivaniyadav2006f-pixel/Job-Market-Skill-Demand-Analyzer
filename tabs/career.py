import streamlit as st
import pandas as pd


def career_tab(
    filtered_df,
    role_column,
    location_column,
    experience_column,
    skill_counts
):

    st.subheader("🚀 Career Intelligence")

    if filtered_df.empty:
        st.warning("No jobs match the selected filters.")
        return

    # =====================================================
    # CAREER OPPORTUNITIES
    # =====================================================

    st.markdown("#### 💼 Career Opportunities")

    # =====================================================
    # MOST IN-DEMAND ROLES
    # =====================================================

    if role_column:

        role_counts = (
            filtered_df[role_column]
            .dropna()
            .astype(str)
            .str.strip()
            .value_counts()
            .head(10)
        )

        if not role_counts.empty:

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("##### 🔥 Most In-Demand Roles")

                st.bar_chart(
                    role_counts.sort_values(),
                    horizontal=True,
                    height=400
                )

            with col2:

                st.markdown("##### 📋 Role Demand")

                role_table = (
                    role_counts
                    .rename("Job Count")
                    .reset_index()
                )

                role_table.columns = [
                    "Job Role",
                    "Job Count"
                ]

                st.dataframe(
                    role_table,
                    use_container_width=True,
                    hide_index=True
                )

    else:

        st.info("Job role information is not available.")

    st.divider()

    # =====================================================
    # TOP LOCATIONS
    # =====================================================

    if location_column:

        st.markdown("#### 📍 Top Job Locations")

        location_counts = (
            filtered_df[location_column]
            .dropna()
            .astype(str)
            .str.strip()
            .value_counts()
            .head(10)
        )

        if not location_counts.empty:

            st.bar_chart(
                location_counts.sort_values(),
                horizontal=True,
                height=400
            )

    st.divider()

    # =====================================================
    # EXPERIENCE DEMAND
    # =====================================================

    if experience_column:

        st.markdown("#### 🧑‍💻 Experience Level Demand")

        experience_counts = (
            filtered_df[experience_column]
            .dropna()
            .astype(str)
            .str.strip()
            .value_counts()
        )

        if not experience_counts.empty:

            st.bar_chart(
                experience_counts,
                height=350
            )

    st.divider()

    # =====================================================
    # SKILLS TO FOCUS ON
    # =====================================================

    st.markdown("#### 🎯 Skills to Focus On")

    if skill_counts is None or len(skill_counts) == 0:

        st.info("Skill information is not available.")

    else:

        top_skills = skill_counts.head(10)

        cols = st.columns(2)

        for index, (skill, count) in enumerate(
            top_skills.items()
        ):

            with cols[index % 2]:

                st.markdown(
                    f"""
                    <div style="
                        padding:14px;
                        margin-bottom:10px;
                        border-radius:12px;
                        background:#ffffff;
                        border:1px solid #e2e8f0;
                    ">

                        <strong>{skill}</strong>

                        <br>

                        <span style="color:#64748b;">
                            Required in {count} jobs
                        </span>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.divider()

    # =====================================================
    # CAREER SUMMARY
    # =====================================================

    st.markdown("#### 📌 Career Summary")

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:

        st.metric(
            "Jobs Analyzed",
            len(filtered_df)
        )

    with summary_col2:

        if role_column:

            unique_roles = (
                filtered_df[role_column]
                .dropna()
                .nunique()
            )

        else:

            unique_roles = 0

        st.metric(
            "Job Roles",
            unique_roles
        )

    with summary_col3:

        if location_column:

            unique_locations = (
                filtered_df[location_column]
                .dropna()
                .nunique()
            )

        else:

            unique_locations = 0

        st.metric(
            "Locations",
            unique_locations
        )