"""
Patient History View for HealthGuardian AI
Stores, searches, filters, deletes, and exports patient diagnostic history records.
"""

import streamlit as st
import pandas as pd
from database.db_handler import get_user_predictions, delete_prediction
from utils.exporter import export_to_csv, export_to_excel


def render_patient_history_page():
    """Render Patient Prediction History Table & Export Management."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="color: #1a365d; font-weight: 800;">📜 Patient Diagnostic History</h2>
        <p style="color: #4a5568;">Search, filter, manage, and export past health assessment records.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("authenticated", False):
        st.warning("Please sign in to view your patient diagnostic history.")
        if st.button("Go to Sign In"):
            st.session_state.page = "Login"
            st.rerun()
        return

    user = st.session_state.user
    predictions = get_user_predictions(user["id"])

    if not predictions:
        st.info("ℹ️ No diagnostic history records found. Run a Disease Prediction to record your first assessment.")
        return

    df = pd.DataFrame(predictions)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    # Search & Filters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_query = st.text_input("🔍 Search History Logs", placeholder="Filter by date, age, or score...")
    with col2:
        score_filter = st.selectbox("Filter Health Score", ["All Scores", "High (80-100)", "Moderate (50-79)", "Low (<50)"])
    with col3:
        sort_order = st.selectbox("Sort Order", ["Newest First", "Oldest First"])

    # Filter logic
    filtered_df = df.copy()
    if score_filter == "High (80-100)":
        filtered_df = filtered_df[filtered_df["health_score"] >= 80]
    elif score_filter == "Moderate (50-79)":
        filtered_df = filtered_df[(filtered_df["health_score"] >= 50) & (filtered_df["health_score"] < 80)]
    elif score_filter == "Low (<50)":
        filtered_df = filtered_df[filtered_df["health_score"] < 50]

    if sort_order == "Oldest First":
        filtered_df = filtered_df.sort_values(by="timestamp", ascending=True)
    else:
        filtered_df = filtered_df.sort_values(by="timestamp", ascending=False)

    if search_query:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        filtered_df = filtered_df[mask]

    st.markdown(f"**Found {len(filtered_df)} record(s)**")

    # Display Clean Table
    display_cols = ["id", "timestamp", "age", "bmi", "glucose", "blood_pressure", "diabetes_prob", "heart_prob", "health_score"]
    available_cols = [c for c in display_cols if c in filtered_df.columns]

    st.dataframe(filtered_df[available_cols], use_container_width=True)

    # Export Buttons
    st.markdown("#### 📥 Export Records")
    exp_col1, exp_col2, exp_col3 = st.columns(3)

    records_data = filtered_df.to_dict(orient="records")

    with exp_col1:
        csv_bytes = export_to_csv(records_data)
        st.download_button(
            "Export to CSV 📄",
            data=csv_bytes,
            file_name=f"HealthGuardian_History_{user['username']}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with exp_col2:
        excel_bytes = export_to_excel(records_data)
        st.download_button(
            "Export to Excel 📊",
            data=excel_bytes,
            file_name=f"HealthGuardian_History_{user['username']}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Delete Record Utility
    st.markdown("---")
    st.markdown("#### 🗑️ Manage & Delete Records")
    with st.expander("Delete a Record"):
        delete_id = st.number_input("Enter Record ID to Delete", min_value=1, step=1)
        if st.button("Delete Record", type="primary"):
            success = delete_prediction(int(delete_id), user["id"])
            if success:
                st.success(f"Record #{delete_id} deleted successfully.")
                st.rerun()
            else:
                st.error("Record ID not found or access denied.")
