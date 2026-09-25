import os
import streamlit as st

from database import (
    is_admin,
    search_users,
    get_user_count,
    get_login_history,
    delete_user,
    clear_login_history,
    get_all_resumes,
    delete_resume_record
)


def admin_panel():

    username = st.session_state.get("username", "")

    # ---------------------------------------------------------
    # ADMIN ACCESS CHECK
    # ---------------------------------------------------------

    if not is_admin(username):

        st.error("❌ Access Denied")

        return

    # ---------------------------------------------------------
    # ADMIN HEADER
    # ---------------------------------------------------------

    st.title("🛡️ Admin Panel")

    st.caption(
        "Manage registered users, resumes and login activity."
    )

    st.divider()

    # =========================================================
    # USER MANAGEMENT
    # =========================================================

    st.subheader("👥 User Management")

    total_users = get_user_count()

    st.metric(
        "👥 Total Registered Users",
        total_users
    )

    st.divider()

    st.subheader("🔍 Search User")

    search_text = st.text_input(
        "Search by Username or Email",
        placeholder="Enter username or email..."
    )

    st.subheader("👤 Registered Users")

    users = search_users(search_text)

    if not users:

        st.info("No users found.")

    else:

        for user_id, user_name, email, role in users:

            # Do not show admin accounts
            if role == "admin":
                continue

            with st.container():

                col1, col2, col3 = st.columns(
                    [2, 3, 1]
                )

                with col1:

                    st.write(
                        f"👤 **{user_name}**"
                    )

                with col2:

                    st.write(
                        f"📧 {email or 'No email'}"
                    )

                with col3:

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_{user_id}"
                    ):

                        success = delete_user(
                            user_name
                        )

                        if success:

                            st.success(
                                f"{user_name} deleted successfully."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Unable to delete user."
                            )

                st.divider()

    # =========================================================
    # RESUME MANAGEMENT
    # =========================================================

    st.subheader("📄 Resume Management")

    st.caption(
        "View, download and delete resumes uploaded by users."
    )

    resumes = get_all_resumes()

    if not resumes:

        st.info(
            "📭 No resumes have been uploaded yet."
        )

    else:

        st.write(
            f"**Total Uploaded Resumes: {len(resumes)}**"
        )

        st.divider()

        for (
            resume_id,
            resume_username,
            original_filename,
            stored_filename,
            upload_time
        ) in resumes:

            with st.container():

                col1, col2, col3, col4 = st.columns(
                    [2, 3, 2, 1]
                )

                # -------------------------------------------------
                # USERNAME
                # -------------------------------------------------

                with col1:

                    st.write(
                        f"👤 **{resume_username}**"
                    )

                # -------------------------------------------------
                # FILE NAME
                # -------------------------------------------------

                with col2:

                    st.write(
                        f"📄 {original_filename}"
                    )

                    st.caption(
                        f"Uploaded: {upload_time}"
                    )

                # -------------------------------------------------
                # DOWNLOAD
                # -------------------------------------------------

                with col3:

                    if os.path.exists(
                        stored_filename
                    ):

                        try:

                            with open(
                                stored_filename,
                                "rb"
                            ) as resume_file:

                                resume_data = (
                                    resume_file.read()
                                )

                            st.download_button(
                                label="⬇️ Download",
                                data=resume_data,
                                file_name=original_filename,
                                key=f"download_resume_{resume_id}",
                                use_container_width=True
                            )

                        except Exception as e:

                            st.error(
                                f"Unable to read resume: {e}"
                            )

                    else:

                        st.warning(
                            "Resume file not found."
                        )

                # -------------------------------------------------
                # DELETE
                # -------------------------------------------------

                with col4:

                    if st.button(
                        "🗑️",
                        key=f"delete_resume_{resume_id}",
                        help="Delete this resume"
                    ):

                        # Delete actual file
                        if os.path.exists(
                            stored_filename
                        ):

                            try:

                                os.remove(
                                    stored_filename
                                )

                            except Exception as e:

                                st.error(
                                    f"Unable to delete file: {e}"
                                )

                                continue

                        # Delete database record
                        deleted = delete_resume_record(
                            resume_id
                        )

                        if deleted:

                            st.success(
                                "Resume deleted successfully."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Unable to delete resume record."
                            )

                st.divider()

    # =========================================================
    # LOGIN HISTORY
    # =========================================================

    st.subheader("🕒 Login History")

    history = get_login_history()

    if not history:

        st.info(
            "No login history available."
        )

    else:

        for login_username, login_time in history:

            st.write(
                f"👤 **{login_username}** "
                f"— 🕒 {login_time}"
            )

    st.divider()

    # =========================================================
    # CLEAN LOGIN DATA
    # =========================================================

    st.subheader("🧹 Clean Data")

    st.warning(
        "Clearing login history will permanently remove "
        "the stored login records."
    )

    if st.button(
        "🧹 Clear All Login History",
        use_container_width=True
    ):

        clear_login_history()

        st.success(
            "Login history cleared successfully."
        )

        st.rerun()