import streamlit as st

from database import (
    register_user,
    login_user,
    is_admin
)


# =========================================================
# BLACK INPUT LABELS
# =========================================================

def black_input_labels():

    st.markdown(
        """
        <style>

        [data-testid="stTextInput"] label,
        [data-testid="stTextInput"] label p {
            color: #000000 !important;
            font-weight: 600 !important;
        }

        [data-testid="stTextInput"] input {
            color: #000000 !important;
        }

        [data-testid="stTextInput"] input::placeholder {
            color: #64748b !important;
            opacity: 1 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    black_input_labels()

    # Default login mode
    if "login_mode" not in st.session_state:
        st.session_state["login_mode"] = "user"

    st.title("📊 Job Market & Skill Demand Analyzer")

    st.caption(
        "🚀 Discover Skills • Analyze Demand • Grow Your Career"
    )

    st.divider()

    st.subheader("👋 Welcome Back!")

    st.markdown(
        "<p style='color: #000000; font-size: 16px; font-weight: 500;'>"
        "Sign in to access your job market intelligence dashboard."
        "</p>",
        unsafe_allow_html=True
    )

    # =====================================================
    # LOGIN TYPE
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "👤 User Login",
            use_container_width=True,
            key="user_login_mode"
        ):

            st.session_state["login_mode"] = "user"

            # Clear old login error/state
            st.rerun()

    with col2:

        if st.button(
            "🛡️ Admin Login",
            use_container_width=True,
            key="admin_login_mode"
        ):

            st.session_state["login_mode"] = "admin"

            # Clear old login error/state
            st.rerun()

    st.divider()

    # =====================================================
    # LOGIN MODE TITLE
    # =====================================================

    if st.session_state["login_mode"] == "admin":

        st.subheader("🛡️ Admin Login")

        st.markdown(
            "<p style='color:#4b5563;'>"
            "Authorized administrators only."
            "</p>",
            unsafe_allow_html=True
        )

    else:

        st.subheader("👤 User Login")

    # =====================================================
    # USERNAME
    # =====================================================

    username = st.text_input(
        "👤 Username",
        placeholder="Enter your username",
        key="login_username"
    )

    # =====================================================
    # PASSWORD
    # =====================================================

    st.markdown(
        "<div style='color:black; font-weight:600; margin-bottom:5px;'>"
        "🔒 Password"
        "</div>",
        unsafe_allow_html=True
    )

    password = st.text_input(
        "",
        type="password",
        placeholder="Enter your password",
        key="login_password"
    )

    # =====================================================
    # LOGIN BUTTON
    # =====================================================

    if st.session_state["login_mode"] == "admin":

        login_button = st.button(
            "🛡️ Login as Admin",
            use_container_width=True,
            key="admin_login_button"
        )

    else:

        login_button = st.button(
            "🚀 Login to Dashboard",
            use_container_width=True,
            key="login_button"
        )

    # =====================================================
    # LOGIN PROCESS
    # =====================================================

    if login_button:

        if not username or not password:

            st.warning(
                "⚠️ Please enter both username and password."
            )

        else:

            clean_username = username.strip()

            # -------------------------------------------------
            # CHECK USERNAME AND PASSWORD
            # -------------------------------------------------

            if login_user(clean_username, password):

                # =================================================
                # ADMIN LOGIN MODE
                # =================================================

                if st.session_state["login_mode"] == "admin":

                    if is_admin(clean_username):

                        st.session_state["logged_in"] = True
                        st.session_state["username"] = clean_username
                        st.session_state["profile_email"] = ""
                        st.session_state["page"] = "Admin"

                        st.success(
                            "🛡️ Admin login successful!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "❌ This account does not have "
                            "administrator access."
                        )

                # =================================================
                # NORMAL USER LOGIN MODE
                # =================================================

                else:

                    # Admin account cannot use normal user login
                    if is_admin(clean_username):

                        st.error(
                            "❌ This is an administrator account. "
                            "Please select 🛡️ Admin Login."
                        )

                    else:

                        st.session_state["logged_in"] = True
                        st.session_state["username"] = clean_username
                        st.session_state["profile_email"] = ""
                        st.session_state["page"] = "Dashboard"

                        st.success(
                            "✅ Login successful! Welcome back."
                        )

                        st.rerun()

            else:

                st.error(
                    "❌ Invalid username or password."
                )

    # =========================================================
    # CAREER INTELLIGENCE
    # =========================================================

    st.divider()

    st.subheader("✨ Explore Your Career Intelligence")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "📈 **Job Trends**\n\n"
            "Analyze hiring demand and market trends."
        )

    with col2:

        st.info(
            "💡 **Top Skills**\n\n"
            "Discover skills employers are looking for."
        )

    with col3:

        st.info(
            "💰 **Salary Insights**\n\n"
            "Explore salary trends and opportunities."
        )

    # =========================================================
    # CREATE ACCOUNT
    # =========================================================

    st.divider()

    st.subheader("🆕 New to the Platform?")

    st.write(
        "Create an account to start exploring the job market."
    )

    if st.button(
        "✨ Create New Account",
        use_container_width=True,
        key="create_account_button"
    ):

        st.session_state["page"] = "Register"

        st.rerun()

    st.caption(
        "🔒 Secure Login • 📊 Career Intelligence Platform"
    )


# =========================================================
# REGISTER PAGE
# =========================================================

def register_page():

    black_input_labels()

    st.title("📝 Create Your Account")

    st.caption(
        "🚀 Start exploring job market and career intelligence."
    )

    st.divider()

    st.subheader("👤 New Account")

    st.write(
        "Create your account to access the Job Market Dashboard."
    )

    username = st.text_input(
        "👤 Username",
        placeholder="Choose a username",
        key="register_username"
    )

    password = st.text_input(
        "🔒 Password",
        type="password",
        placeholder="Create a password",
        key="register_password"
    )

    confirm_password = st.text_input(
        "🔒 Confirm Password",
        type="password",
        placeholder="Re-enter your password",
        key="confirm_password"
    )

    if st.button(
        "✨ Create Account",
        use_container_width=True,
        key="register_button"
    ):

        if not username or not password or not confirm_password:

            st.warning(
                "⚠️ Please fill in all fields."
            )

        elif len(username.strip()) < 3:

            st.warning(
                "⚠️ Username must contain at least 3 characters."
            )

        elif len(password) < 6:

            st.warning(
                "⚠️ Password must contain at least 6 characters."
            )

        elif password != confirm_password:

            st.error(
                "❌ Passwords do not match."
            )

        else:

            registered = register_user(
                username.strip(),
                password
            )

            if registered:

                st.success(
                    "🎉 Account created successfully!"
                )

                st.info(
                    "Please login with your new account."
                )

                # Clear registration fields
                st.session_state.pop(
                    "register_username",
                    None
                )

                st.session_state.pop(
                    "register_password",
                    None
                )

                st.session_state.pop(
                    "confirm_password",
                    None
                )

                st.session_state["page"] = "Login"

                st.rerun()

            else:

                st.error(
                    "❌ Username already exists."
                )

    st.divider()

    if st.button(
        "← Back to Login",
        use_container_width=True,
        key="back_to_login_button"
    ):

        st.session_state["page"] = "Login"

        st.rerun()

    st.caption(
        "🔒 Your account is protected by the application database."
    )