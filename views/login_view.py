"""
Login & Authentication View for HealthGuardian AI
Provides Glassmorphism UI, Animated Doctor SVG Illustration,
Register, Login, Remember Me, Forgot Password, and Bcrypt Password Hashing.
"""

import streamlit as st
from auth.authenticator import login, register, reset_password


def render_login_page():
    """Render Glassmorphic Login/Register Portal."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px;">
        <h1 style="color: #1a365d; font-weight: 800; font-size: 2.2rem; margin-bottom: 5px;">
            🏥 HealthGuardian AI Authentication Portal
        </h1>
        <p style="color: #4a5568; font-size: 1rem;">
            Secure SQLite Authentication & Encrypted Patient Access
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    # Left Column: Doctor Illustration & Info
    with col1:
        st.markdown("""
        <div class="glass-card animate-fade-in" style="text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <svg width="220" height="220" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="100" cy="100" r="90" fill="#EBF8FF" stroke="#3182CE" stroke-width="4"/>
                <path d="M100 40C75 40 60 55 60 75C60 95 80 110 100 125C120 110 140 95 140 75C140 55 125 40 100 40Z" fill="#3182CE" opacity="0.15"/>
                <!-- Cross Icon -->
                <rect x="92" y="60" width="16" height="40" rx="4" fill="#2B6CB0"/>
                <rect x="80" y="72" width="40" height="16" rx="4" fill="#2B6CB0"/>
                <!-- Doctor Avatar Body -->
                <circle cx="100" cy="120" r="22" fill="#2D3748"/>
                <path d="M65 165C65 145 80 135 100 135C120 135 135 145 135 165V180H65V165Z" fill="#3182CE"/>
                <path d="M92 135H108V165H92V135Z" fill="#FFFFFF"/>
                <!-- Stethoscope -->
                <path d="M85 145C85 155 115 155 115 145" stroke="#E2E8F0" stroke-width="4" stroke-linecap="round"/>
            </svg>
            <h3 style="color: #2b6cb0; margin-top: 15px; font-size: 1.3rem;">Clinical Decision Intelligence</h3>
            <p style="color: #718096; font-size: 0.88rem; max-width: 320px; margin-top: 8px;">
                Log in to evaluate lifestyle disease risks, manage patient history logs, and download verified PDF reports.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Right Column: Login / Register Form Tabs
    with col2:
        st.markdown('<div class="glass-card animate-fade-in">', unsafe_allow_html=True)
        tab_login, tab_register, tab_forgot = st.tabs(["🔒 Account Login", "📝 New Registration", "🔑 Forgot Password"])

        # TAB 1: LOGIN
        with tab_login:
            st.markdown("#### Sign In to Your Account")
            login_username = st.text_input("Username or Email", key="login_uname")
            login_password = st.text_input("Password", type="password", key="login_pwd")
            remember_me = st.checkbox("Remember Me on this Browser", value=True)

            if st.button("Sign In 🚀", use_container_width=True):
                success, msg = login(login_username, login_password)
                if success:
                    st.success(msg)
                    st.session_state.page = "Home"
                    st.rerun()
                else:
                    st.error(msg)

        # TAB 2: REGISTER
        with tab_register:
            st.markdown("#### Create New Account")
            reg_name = st.text_input("Full Name", key="reg_name")
            reg_username = st.text_input("Username", key="reg_uname")
            reg_email = st.text_input("Email Address", key="reg_email")
            reg_pwd = st.text_input("Password", type="password", key="reg_pwd")
            reg_pwd_confirm = st.text_input("Confirm Password", type="password", key="reg_pwd_confirm")
            user_role = st.selectbox("Role", ["patient", "admin"], key="reg_role")

            if st.button("Register Account 🎉", use_container_width=True):
                success, msg = register(reg_username, reg_email, reg_pwd, reg_pwd_confirm, reg_name, user_role)
                if success:
                    st.success(msg + " You can now sign in.")
                else:
                    st.error(msg)

        # TAB 3: FORGOT PASSWORD
        with tab_forgot:
            st.markdown("#### Password Reset Utility")
            reset_uname = st.text_input("Registered Username", key="reset_uname")
            reset_email = st.text_input("Registered Email", key="reset_email")
            new_pwd = st.text_input("New Password", type="password", key="reset_new_pwd")

            if st.button("Reset Password 🔐", use_container_width=True):
                success, msg = reset_password(reset_uname, reset_email, new_pwd)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

        st.markdown('</div>', unsafe_allow_html=True)
