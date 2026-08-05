"""
Patient Profile View for HealthGuardian AI
Provides patient demographics, medical history, lifestyle factors, and live metric previews.
"""

import streamlit as st
from database.db_handler import get_patient_profile, update_patient_profile
from utils.calculators import calculate_bmi, calculate_body_fat


def render_patient_profile_page():
    """Render Patient Demographics & Lifestyle Profile Manager."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="color: #1a365d; font-weight: 800;">👤 Patient Medical Profile</h2>
        <p style="color: #4a5568;">Manage patient physiological parameters, medical history, and lifestyle risk factors.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("authenticated", False):
        st.warning("Please log in to manage your Patient Profile.")
        if st.button("Go to Login"):
            st.session_state.page = "Login"
            st.rerun()
        return

    user = st.session_state.user
    profile = get_patient_profile(user["id"])

    with st.form("patient_profile_form"):
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Demographics & Vital Measurements")

        col1, col2, col3 = st.columns(3)
        with col1:
            full_name = st.text_input("Full Name", value=user.get("full_name", ""))
            age = st.number_input("Age (Years)", min_value=1, max_value=120, value=int(profile.get("age", 35)))
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=0 if profile.get("gender") == "Male" else 1)

        with col2:
            height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=float(profile.get("height", 170.0)))
            weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=float(profile.get("weight", 70.0)))
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], index=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"].index(profile.get("blood_group", "O+")))

        with col3:
            emergency_contact = st.text_input("Emergency Contact Number", value=profile.get("emergency_contact", ""))
            bmi, bmi_cat, bmi_color = calculate_bmi(weight, height)
            body_fat, fat_cat = calculate_body_fat(bmi, age, gender)

            st.markdown(f"""
            <div style="background: #edf2f7; padding: 12px; border-radius: 10px; margin-top: 10px;">
                <div style="font-size: 0.8rem; color: #4a5568; font-weight: 600;">LIVE BMI PREVIEW</div>
                <div style="font-size: 1.4rem; font-weight: 700; color: {bmi_color};">{bmi} kg/m² ({bmi_cat})</div>
                <div style="font-size: 0.75rem; color: #718096; margin-top: 4px;">Est. Body Fat: {body_fat}% ({fat_cat})</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🍷 Lifestyle Factors & Medical History")

        col_a, col_b = st.columns(2)
        with col_a:
            smoking = st.selectbox("Smoking Habits", ["Never", "Occasionally", "Regularly"], index=["Never", "Occasionally", "Regularly"].index(profile.get("smoking", "Never")))
            alcohol = st.selectbox("Alcohol Consumption", ["Never", "Occasionally", "Regularly"], index=["Never", "Occasionally", "Regularly"].index(profile.get("alcohol", "Never")))
            sleep_hours = st.slider("Average Sleep Hours / Night", min_value=3.0, max_value=12.0, value=float(profile.get("sleep_hours", 7.5)), step=0.5)

        with col_b:
            stress_level = st.select_slider("Stress Level", options=["Low", "Moderate", "High"], value=profile.get("stress_level", "Moderate"))
            exercise_freq = st.selectbox("Exercise Frequency", ["Never / Sedentary", "1-2 days/week", "3-4 days/week", "5+ days/week (Active)"], index=2)
            medical_history = st.text_area("Existing Conditions / Medical History", value=profile.get("medical_history", ""), placeholder="e.g. Asthma, Previous Surgeries, Allergies")

        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("Save Profile Updates 💾", use_container_width=True)
        if submitted:
            profile_data = {
                "age": age,
                "gender": gender,
                "height": height,
                "weight": weight,
                "blood_group": blood_group,
                "emergency_contact": emergency_contact,
                "medical_history": medical_history,
                "smoking": smoking,
                "alcohol": alcohol,
                "sleep_hours": sleep_hours,
                "stress_level": stress_level,
                "exercise_freq": exercise_freq
            }
            success = update_patient_profile(user["id"], profile_data)
            if success:
                st.session_state.patient_profile = get_patient_profile(user["id"])
                st.success("Patient Profile updated successfully!")
            else:
                st.error("Failed to update profile.")
