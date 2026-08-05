"""
Settings View for HealthGuardian AI
Handles Theme selection (Dark/Light), SMTP configuration, and Health Reminders.
"""

import streamlit as st
from utils.email_sender import send_pdf_report_email


def render_settings_page():
    """Render Settings & Preferences Panel."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="color: #1a365d; font-weight: 800;">⚙️ Application Settings & Preferences</h2>
        <p style="color: #4a5568;">Customize themes, notification alerts, email configuration, and account preferences.</p>
    </div>
    """, unsafe_allow_html=True)

    tab_theme, tab_email, tab_reminders = st.tabs(["🎨 Theme & Display", "📧 Email Integration", "⏰ Health Reminders"])

    # 1. THEME & DISPLAY
    with tab_theme:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Interface Customization")

        dark_toggle = st.toggle("🌙 Enable Dark Mode Glassmorphism", value=st.session_state.get("dark_mode", False))
        if dark_toggle != st.session_state.get("dark_mode", False):
            st.session_state.dark_mode = dark_toggle
            st.rerun()

        theme_accent = st.selectbox("Primary Color Theme", ["Medical Blue (Default)", "Emerald Health", "Deep Slate Gray"])
        st.caption("Theme preference applies across charts and UI cards.")
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. EMAIL INTEGRATION
    with tab_email:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### SMTP Email Sender Settings")
        st.caption("Configure SMTP credentials to email PDF Health Reports directly to patients.")

        smtp_server = st.text_input("SMTP Host Server", value=st.session_state.get("smtp_server", "smtp.gmail.com"))
        smtp_port = st.number_input("SMTP Port", value=st.session_state.get("smtp_port", 587))
        sender_email = st.text_input("Sender Email Address", value=st.session_state.get("sender_email", ""))
        sender_password = st.text_input("Sender App Password", type="password", value=st.session_state.get("sender_password", ""))

        if st.button("Save SMTP Credentials 💾"):
            st.session_state.smtp_server = smtp_server
            st.session_state.smtp_port = smtp_port
            st.session_state.sender_email = sender_email
            st.session_state.sender_password = sender_password
            st.success("SMTP configuration saved in active session.")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. HEALTH REMINDERS
    with tab_reminders:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Health Notification Alerts")

        rem_water = st.checkbox("💧 Hydration Alert: Drink 250ml water every 2 hours", value=True)
        rem_ex = st.checkbox("🏃 Daily Exercise Reminder: 30 minutes physical activity", value=True)
        rem_med = st.checkbox("💊 Medicine Schedule Notification", value=False)
        rem_check = st.checkbox("🩺 Biannual Health Checkup Reminder", value=True)

        if st.button("Save Notification Preferences 🔔"):
            st.success("Notification preferences updated.")
        st.markdown('</div>', unsafe_allow_html=True)
