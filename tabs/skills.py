import streamlit as st


# =========================================================
# SKILLS TAB
# =========================================================

def skills_tab(
    filtered_df,
    skill_counts
):

    st.subheader(
        "🧠 Skill Intelligence"
    )

    # -----------------------------------------------------
    # TOP SKILLS
    # -----------------------------------------------------

    if skill_counts.empty:

        st.warning(
            "No skill data available for the selected filters."
        )

        return

    st.markdown(
        "#### 🔥 Most In-Demand Skills"
    )

    top_skills = (
        skill_counts
        .head(20)
        .sort_values()
    )

    st.bar_chart(
        top_skills,
        horizontal=True,
        height=550
    )

    st.divider()

    # -----------------------------------------------------
    # SKILL TABLE
    # -----------------------------------------------------

    st.markdown(
        "#### 📋 Skill Demand Details"
    )

    skill_table = (
        skill_counts
        .head(20)
        .rename("Job Count")
        .reset_index()
    )

    skill_table.columns = [
        "Skill",
        "Job Count"
    ]

    st.dataframe(
        skill_table,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # SELECTED DATASET INFORMATION
    # -----------------------------------------------------

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Skills",
            len(skill_counts)
        )

    with col2:

        st.metric(
            "Jobs Analyzed",
            len(filtered_df)
        )