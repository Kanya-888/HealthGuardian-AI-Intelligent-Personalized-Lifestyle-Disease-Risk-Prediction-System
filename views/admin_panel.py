"""
Admin Panel View for HealthGuardian AI
Provides system administration: view users, delete accounts, monitor system reports & analytics.
"""

import streamlit as st
import pandas as pd
from database.db_handler import get_all_users, delete_user, get_all_predictions
from auth.authenticator import is_admin


def render_admin_panel_page():
    """Render Admin Console."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="color: #1a365d; font-weight: 800;">🔐 System Admin Console</h2>
        <p style="color: #4a5568;">User account management, security access, and system analytics audit.</p>
    </div>
    """, unsafe_allow_html=True)

    if not is_admin():
        st.error("⛔ Access Denied. Admin credentials required.")
        st.info("Log in with an administrator account to view this panel.")
        return

    tab_users, tab_reports = st.tabs(["👥 User Account Management", "📈 System-Wide Audit & Reports"])

    # TAB 1: USERS MANAGEMENT
    with tab_users:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Registered System Users")

        users = get_all_users()
        df_users = pd.DataFrame(users)
        st.dataframe(df_users, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 🗑️ Delete User Account")
        c1, c2 = st.columns([2, 1])
        with c1:
            del_user_id = st.number_input("Enter User ID to Delete", min_value=1, step=1)
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Permanently Delete User", type="primary"):
                # Prevent deleting current admin self
                if del_user_id == st.session_state.user["id"]:
                    st.error("Cannot delete your own active admin account!")
                else:
                    success = delete_user(int(del_user_id))
                    if success:
                        st.success(f"User #{del_user_id} deleted successfully.")
                        st.rerun()
                    else:
                        st.error("User ID not found.")
        st.markdown('</div>', unsafe_allow_html=True)

    # TAB 2: SYSTEM WIDE REPORTS
    with tab_reports:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### All Diagnostic Predictions Audit Log")

        all_preds = get_all_predictions()
        if all_preds:
            df_preds = pd.DataFrame(all_preds)
            if "details_json" in df_preds.columns:
                df_preds = df_preds.drop(columns=["details_json"])
            st.dataframe(df_preds, use_container_width=True)
        else:
            st.info("No system prediction logs recorded yet.")
        st.markdown('</div>', unsafe_allow_html=True)
