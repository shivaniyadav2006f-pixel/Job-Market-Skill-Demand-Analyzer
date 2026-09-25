import streamlit as st
import pandas as pd
import re

from adzuna_api import fetch_live_jobs


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_description(text):
    if text is None:
        return ""

    try:
        if pd.isna(text):
            return ""
    except Exception:
        pass

    text = str(text).strip()

    if not text or text.lower() in [
        "nan",
        "none",
        "null",
        "not available"
    ]:
        return ""

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Clean extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# =========================================================
# SAFE VALUE
# =========================================================

def clean_value(value, default="Not Available"):
    if value is None:
        return default

    try:
        if pd.isna(value):
            return default
    except Exception:
        pass

    value = str(value).strip()

    if not value or value.lower() in [
        "nan",
        "none",
        "null",
        "not available"
    ]:
        return default

    return value


# =========================================================
# SALARY FORMAT
# =========================================================

def format_salary(salary_min, salary_max):
    min_valid = False
    max_valid = False

    if salary_min is not None:
        try:
            min_valid = (
                pd.notna(salary_min)
                and str(salary_min).strip() != ""
            )
        except Exception:
            min_valid = False

    if salary_max is not None:
        try:
            max_valid = (
                pd.notna(salary_max)
                and str(salary_max).strip() != ""
            )
        except Exception:
            max_valid = False

    if min_valid and max_valid:
        try:
            return (
                f"₹{float(salary_min):,.0f} - "
                f"₹{float(salary_max):,.0f}"
            )
        except Exception:
            return f"{salary_min} - {salary_max}"

    if min_valid:
        try:
            return f"From ₹{float(salary_min):,.0f}"
        except Exception:
            return f"From {salary_min}"

    if max_valid:
        try:
            return f"Up to ₹{float(salary_max):,.0f}"
        except Exception:
            return f"Up to {salary_max}"

    return "Not Available"


# =========================================================
# LIVE JOBS TAB
# =========================================================

def live_jobs_tab():

    st.subheader("🌐 Live Job Search")

    st.caption(
        "Search current job opportunities directly from Adzuna."
    )

    st.markdown("### 🔎 Search Filters")

    col1, col2, col3 = st.columns(3)

    with col1:
        job_role = st.text_input(
            "💼 Job Role",
            placeholder="e.g. Data Scientist",
            key="live_job_role"
        )

    with col2:
        location = st.text_input(
            "📍 Location",
            placeholder="e.g. Mumbai",
            key="live_job_location"
        )

    with col3:
        experience = st.text_input(
            "🎓 Experience",
            placeholder="e.g. Fresher / 1 year / 2 years",
            key="live_job_experience"
        )

    st.write("")

    search_clicked = st.button(
        "🔎 Search Live Jobs",
        use_container_width=True,
        key="search_live_jobs_button"
    )

    if not search_clicked:
        st.info(
            "Enter a Job Role and Location, then click "
            "'Search Live Jobs'."
        )
        return

    job_role = job_role.strip()
    location = location.strip()
    experience = experience.strip()

    if not job_role:
        st.warning("⚠️ Please enter a Job Role.")
        return

    if not location:
        st.warning("⚠️ Please enter a Location.")
        return

    # =====================================================
    # API SEARCH
    # =====================================================

    with st.spinner("🔄 Fetching live jobs from Adzuna..."):
        jobs_df, error = fetch_live_jobs(
            job_role=job_role,
            location=location,
            experience=experience
        )

    if error:
        st.error(error)
        return

    if jobs_df is None or jobs_df.empty:
        st.warning("😕 No live jobs were found for this search.")
        st.info(
            "Try a broader Job Role or Location, "
            "for example: Data Scientist + Mumbai."
        )
        return

    # =====================================================
    # RESULT SUMMARY
    # =====================================================

    st.success(
        f"✅ Found {len(jobs_df)} live job opportunities."
    )

    st.divider()

    # =====================================================
    # JOB CARDS
    # =====================================================

    for index, job in jobs_df.iterrows():

        title = clean_value(
            job.get("Job Title", ""),
            "Job Title Not Available"
        )

        company = clean_value(
            job.get("Company", ""),
            "Company Not Available"
        )

        job_location = clean_value(
            job.get("Location", ""),
            "Location Not Available"
        )

        job_type = clean_value(
            job.get("Job Type", ""),
            "Not Available"
        )

        job_time = clean_value(
            job.get("Job Time", ""),
            "Not Available"
        )

        description = clean_description(
            job.get("Description", "")
        )

        salary = format_salary(
            job.get("Salary Min"),
            job.get("Salary Max")
        )

        apply_url = clean_value(
            job.get("Apply URL", ""),
            ""
        )

        # =================================================
        # JOB CARD
        # =================================================

        with st.container(border=True):

            # Force the job-card text to remain dark.
            st.markdown(
                """
                <style>
                .live-job-title,
                .live-job-title * {
                    color: #111827 !important;
                    opacity: 1 !important;
                }

                .live-job-detail,
                .live-job-detail * {
                    color: #111827 !important;
                    opacity: 1 !important;
                }

                .live-job-description,
                .live-job-description * {
                    color: #111827 !important;
                    opacity: 1 !important;
                }

                .live-job-muted,
                .live-job-muted * {
                    color: #4b5563 !important;
                    opacity: 1 !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            # -------------------------------------------------
            # TITLE
            # -------------------------------------------------

            st.markdown(
                f"""
                <div class="live-job-title"
                     style="
                        font-size:26px;
                        font-weight:700;
                        line-height:1.4;
                        margin:4px 0 14px 0;
                     ">
                    💼 {title}
                </div>
                """,
                unsafe_allow_html=True
            )

            # -------------------------------------------------
            # DETAILS
            # -------------------------------------------------

            st.markdown(
                f"""
                <div class="live-job-detail"
                     style="
                        font-size:16px;
                        line-height:1.8;
                        margin:4px 0;
                     ">
                    🏢 <strong>Company:</strong> {company}
                </div>

                <div class="live-job-detail"
                     style="
                        font-size:16px;
                        line-height:1.8;
                        margin:4px 0;
                     ">
                    📍 <strong>Location:</strong> {job_location}
                </div>

                <div class="live-job-detail"
                     style="
                        font-size:16px;
                        line-height:1.8;
                        margin:4px 0;
                     ">
                    💰 <strong>Salary:</strong> {salary}
                </div>

                <div class="live-job-detail"
                     style="
                        font-size:16px;
                        line-height:1.8;
                        margin:4px 0;
                     ">
                    📝 <strong>Job Type:</strong> {job_type}
                </div>
                """,
                unsafe_allow_html=True
            )

            if job_time != "Not Available":
                st.markdown(
                    f"""
                    <div class="live-job-detail"
                         style="
                            font-size:16px;
                            line-height:1.8;
                            margin:4px 0;
                         ">
                        ⏱️ <strong>Job Time:</strong> {job_time}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # -------------------------------------------------
            # DESCRIPTION
            # -------------------------------------------------

            if description:
                with st.expander(
                    "📋 View Full Job Description"
                ):
                    st.markdown(
                        f"""
                        <div class="live-job-description"
                             style="
                                font-size:15px;
                                line-height:1.7;
                                text-align:justify;
                                padding:4px 0;
                             ">
                            {description}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    """
                    <div class="live-job-muted"
                         style="
                            font-size:14px;
                            margin:10px 0;
                         ">
                        📋 Job description not available.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # -------------------------------------------------
            # APPLY BUTTON
            # -------------------------------------------------

            if apply_url:
                st.link_button(
                    "🚀 Apply Now",
                    apply_url,
                    use_container_width=True
                )
            else:
                st.markdown(
                    """
                    <div class="live-job-muted"
                         style="
                            font-size:14px;
                            margin-top:10px;
                         ">
                        🔗 Application link not available.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.divider()

    st.caption(
        "ℹ️ Job listings are provided through the Adzuna API."
    )
