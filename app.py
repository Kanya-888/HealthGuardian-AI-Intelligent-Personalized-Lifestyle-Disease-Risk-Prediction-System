"""
HealthGuardian AI – Intelligent Personalized Lifestyle Disease Risk Prediction System
Main Streamlit Entry Point & Application Router
"""

import os
import sys
import streamlit as st

# Set Streamlit Page Configuration (Must be first Streamlit command)
st.set_page_config(
    page_title="HealthGuardian AI – Lifestyle Disease Risk Prediction System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure current directory is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from auth.authenticator import init_session_state, logout, is_admin
from views.home import render_home_page
from views.login_view import render_login_page
from views.patient_profile import render_patient_profile_page
from views.calculators_view import render_calculators_page
from views.disease_prediction import render_disease_prediction_page
from views.analytics_dashboard import render_analytics_dashboard_page
from views.patient_history import render_patient_history_page
from views.admin_panel import render_admin_panel_page
from views.settings_view import render_settings_page


def load_custom_css():
    """Load custom CSS styles."""
    css_path = os.path.join(PROJECT_ROOT, "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        if st.session_state.get("dark_mode", False):
            dark_css = """
            <script>
                document.body.classList.add('dark-theme');
            </script>
            <style>
            .stApp {
                background-color: #040d1a !important;
                color: #f1f5f9 !important;
            }
            </style>
            """
            st.markdown(dark_css + f"<style>{css_content}</style>", unsafe_allow_html=True)
        else:
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def render_saas_top_navbar():
    """Render Corporate Healthcare SaaS Top Navbar (Matching Inspiration UI)."""
    user_status = "CLINICAL PORTAL"
    if st.session_state.get("authenticated") and st.session_state.get("user"):
        user_status = f"USER: {st.session_state.user['username'].upper()}"

    st.markdown(f"""
    <div class="saas-navbar">
        <div class="saas-logo-box">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 8v8M8 12h8"/>
            </svg>
            <span class="saas-logo-text">HEALTHGUARDIAN AI</span>
        </div>
        <div class="saas-nav-links">
            <a href="https://github.com/Kanya-888/HealthGuardian-AI-Intelligent-Personalized-Lifestyle-Disease-Risk-Prediction-System" target="_blank" class="saas-nav-item" style="display: inline-flex; align-items: center; gap: 6px;">
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
                GITHUB REPO
            </a>
            <span class="saas-nav-item">HEALTHCARE PROVIDERS</span>
            <span class="saas-nav-item">RESEARCHERS</span>
        </div>
        <div>
            <span class="saas-cta-btn">{user_status}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main Application Entry Point."""
    # Initialize session state
    init_session_state()

    # Load custom styling
    load_custom_css()

    # Render SaaS Top Navbar Banner
    render_saas_top_navbar()

    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        st.markdown("""
        <div style="padding: 10px 0 5px 0;">
            <div style="font-size: 0.75rem; color: #38bdf8; font-weight: 800; letter-spacing: 1px;">SaaS NAVIGATION DOCK</div>
            <h3 style="color: #ffffff; font-weight: 800; font-size: 1.2rem; margin-top: 2px;">Clinical Intelligence</h3>
        </div>
        <hr style="margin-top: 5px; border-color: rgba(255,255,255,0.1);">
        """, unsafe_allow_html=True)

        # Active user badge
        if st.session_state.authenticated and st.session_state.user:
            u_name = st.session_state.user['full_name']
            u_role = st.session_state.user['role'].upper()
            st.markdown(f"""
            <div style="background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.3); padding: 12px; border-radius: 12px; margin-bottom: 15px;">
                <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 700;">AUTHENTICATED PROVIDER</div>
                <div style="font-weight: 700; color: #ffffff; font-size: 0.95rem;">{u_name}</div>
                <span class="badge-low" style="font-size: 0.7rem; margin-top: 4px; display: inline-block;">ROLE: {u_role}</span>
            </div>
            """, unsafe_allow_html=True)

        nav_options = ["Home", "Disease Prediction", "Health Calculators", "Analytics Dashboard", "Patient Profile", "Patient History"]

        if not st.session_state.authenticated:
            nav_options.insert(1, "Login / Register")

        if is_admin():
            nav_options.append("Admin Panel")

        nav_options.append("Settings")

        # Handle page navigation
        if st.session_state.page not in nav_options:
            st.session_state.page = "Home"

        selected_page = st.radio("Platform Navigation", nav_options, index=nav_options.index(st.session_state.page))
        st.session_state.page = selected_page

        st.markdown("---")

        if st.session_state.authenticated:
            if st.button("Sign Out 🚪", use_container_width=True):
                logout()
                st.rerun()
        else:
            if st.button("Sign In / Register 🔒", use_container_width=True):
                st.session_state.page = "Login / Register"
                st.rerun()

        st.markdown("""
        <div style="position: relative; bottom: 0; margin-top: 40px; font-size: 0.72rem; color: #64748b; text-align: center;">
            HealthGuardian AI Corporate SaaS v2.5<br>
            Enterprise Decision Support System
        </div>
        """, unsafe_allow_html=True)

    # --- PAGE ROUTING ---
    page = st.session_state.page

    if page == "Home":
        render_home_page()
    elif page in ["Login", "Login / Register"]:
        render_login_page()
    elif page == "Patient Profile":
        render_patient_profile_page()
    elif page == "Health Calculators":
        render_calculators_page()
    elif page == "Disease Prediction":
        render_disease_prediction_page()
    elif page == "Analytics Dashboard":
        render_analytics_dashboard_page()
    elif page == "Patient History":
        render_patient_history_page()
    elif page == "Admin Panel":
        render_admin_panel_page()
    elif page == "Settings":
        render_settings_page()


if __name__ == "__main__":
    main()
