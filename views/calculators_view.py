"""
Health Calculators View for HealthGuardian AI
Provides interactive UI for 10 medical and physiological calculators.
"""

import streamlit as st
from utils.calculators import (
    calculate_bmi, calculate_body_fat, calculate_water_intake,
    calculate_bmr, calculate_tdee, calculate_calories_breakdown,
    calculate_protein_requirement, calculate_ideal_weight,
    calculate_whr, calculate_bsa
)


def render_calculators_page():
    """Render interactive Health Calculators interface."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="color: #1a365d; font-weight: 800;">🧮 Interactive Health Calculators</h2>
        <p style="color: #4a5568;">Instant clinical assessment of physiological indicators and metabolic targets.</p>
    </div>
    """, unsafe_allow_html=True)

    tab_bmi, tab_fat, tab_water, tab_cal, tab_protein, tab_ibw, tab_bmr, tab_whr, tab_bsa = st.tabs([
        "⚖️ BMI", "📊 Body Fat %", "💧 Water", "🔥 Calories/TDEE",
        "🥩 Protein", "🎯 Ideal Weight", "⚡ BMR", "📐 WHR", "📐 BSA"
    ])

    # 1. BMI CALCULATOR
    with tab_bmi:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Body Mass Index (BMI) Calculator")
        c1, c2 = st.columns(2)
        with c1:
            h_bmi = st.number_input("Height (cm)", 100.0, 230.0, 172.0, key="calc_h_bmi")
            w_bmi = st.number_input("Weight (kg)", 30.0, 250.0, 72.0, key="calc_w_bmi")
        with c2:
            bmi, category, color = calculate_bmi(w_bmi, h_bmi)
            st.markdown(f"""
            <div style="background: #edf2f7; padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 0.9rem; color: #4a5568; font-weight: 600;">YOUR BMI RESULT</div>
                <div style="font-size: 2.5rem; font-weight: 800; color: {color};">{bmi}</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: {color};">{category}</div>
                <p style="font-size: 0.8rem; color: #718096; margin-top: 8px;">Standard Range: 18.5 - 24.9 kg/m²</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. BODY FAT PERCENTAGE
    with tab_fat:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Body Fat Percentage Estimator (Deurenberg Formula)")
        c1, c2 = st.columns(2)
        with c1:
            bmi_f = st.number_input("BMI (kg/m²)", 12.0, 50.0, 24.5, key="calc_bmi_f")
            age_f = st.number_input("Age (Years)", 15, 100, 30, key="calc_age_f")
            gen_f = st.selectbox("Gender", ["Male", "Female"], key="calc_gen_f")
        with c2:
            fat_pct, fat_cat = calculate_body_fat(bmi_f, age_f, gen_f)
            st.markdown(f"""
            <div style="background: #edf2f7; padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 0.9rem; color: #4a5568; font-weight: 600;">ESTIMATED BODY FAT</div>
                <div style="font-size: 2.5rem; font-weight: 800; color: #2b6cb0;">{fat_pct}%</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #2b6cb0;">Category: {fat_cat}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. WATER INTAKE
    with tab_water:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Daily Water Intake Calculator")
        c1, c2 = st.columns(2)
        with c1:
            w_w = st.number_input("Weight (kg)", 30.0, 200.0, 70.0, key="calc_w_water")
            ex_w = st.selectbox("Exercise Frequency", ["Never / Sedentary", "1-2 days/week", "3-4 days/week", "5+ days/week (Active)"], key="calc_ex_w")
        with c2:
            liters, glasses = calculate_water_intake(w_w, ex_w)
            st.markdown(f"""
            <div style="background: #ebf8ff; padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 0.9rem; color: #2b6cb0; font-weight: 600;">RECOMMENDED DAILY HYDRATION</div>
                <div style="font-size: 2.5rem; font-weight: 800; color: #3182ce;">{liters} Liters</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #2b6cb0;">{glasses}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. CALORIES & TDEE
    with tab_cal:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### TDEE & Daily Calorie Requirement Calculator")
        c1, c2 = st.columns(2)
        with c1:
            w_c = st.number_input("Weight (kg)", 30.0, 200.0, 70.0, key="calc_w_cal")
            h_c = st.number_input("Height (cm)", 100.0, 230.0, 170.0, key="calc_h_cal")
            age_c = st.number_input("Age", 15, 100, 30, key="calc_age_cal")
            gen_c = st.selectbox("Gender", ["Male", "Female"], key="calc_gen_cal")
            act_c = st.selectbox("Activity Level", [
                "Sedentary (Little or no exercise)", "Lightly Active (1-3 days/week)",
                "Moderately Active (3-5 days/week)", "Very Active (6-7 days/week)"
            ], key="calc_act_cal")
            goal_c = st.selectbox("Fitness Goal", ["Maintain Weight", "Weight Loss (Mild)", "Weight Loss (Aggressive)", "Weight Gain"], key="calc_goal_cal")
        with c2:
            bmr = calculate_bmr(w_c, h_c, age_c, gen_c)
            tdee = calculate_tdee(bmr, act_c)
            target_cal, macros = calculate_calories_breakdown(tdee, goal_c)

            st.markdown(f"""
            <div style="background: #f7fafc; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0;">
                <div style="font-weight: 700; color: #2b6cb0;">Basal Metabolic Rate (BMR): <span style="color:#1a202c;">{bmr} kcal</span></div>
                <div style="font-weight: 700; color: #2b6cb0; margin-top: 4px;">Total Daily Energy (TDEE): <span style="color:#1a202c;">{tdee} kcal</span></div>
                <hr>
                <div style="font-size: 1.4rem; font-weight: 800; color: #38a169;">Target Calorie Intake: {target_cal} kcal</div>
                <div style="margin-top: 8px; font-weight: 600; font-size: 0.9rem;">Macro Targets:</div>
                <ul style="font-size: 0.85rem; color: #4a5568;">
                    <li>Carbohydrates: {macros['Carbs (g)']}g</li>
                    <li>Proteins: {macros['Protein (g)']}g</li>
                    <li>Fats: {macros['Fat (g)']}g</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. PROTEIN REQUIREMENT
    with tab_protein:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Daily Protein Requirement Calculator")
        c1, c2 = st.columns(2)
        with c1:
            w_p = st.number_input("Weight (kg)", 30.0, 200.0, 70.0, key="calc_w_p")
            act_p = st.selectbox("Activity Level", ["Sedentary", "Moderately Active", "Very Active / Athlete"], key="calc_act_p")
        with c2:
            prot_g, prot_desc = calculate_protein_requirement(w_p, act_p)
            st.markdown(f"""
            <div style="background: #edf2f7; padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 0.9rem; color: #4a5568; font-weight: 600;">DAILY PROTEIN REQUIREMENT</div>
                <div style="font-size: 2.5rem; font-weight: 800; color: #dd6b20;">{prot_g} grams</div>
                <div style="font-size: 0.9rem; color: #718096;">{prot_desc}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 6. IDEAL WEIGHT
    with tab_ibw:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Ideal Body Weight (IBW) Calculator (Devine Formula)")
        c1, c2 = st.columns(2)
        with c1:
            h_ibw = st.number_input("Height (cm)", 120.0, 230.0, 175.0, key="calc_h_ibw")
            gen_ibw = st.selectbox("Gender", ["Male", "Female"], key="calc_gen_ibw")
        with c2:
            min_w, max_w = calculate_ideal_weight(h_ibw, gen_ibw)
            st.markdown(f"""
            <div style="background: #edf2f7; padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 0.9rem; color: #4a5568; font-weight: 600;">IDEAL BODY WEIGHT RANGE</div>
                <div style="font-size: 2.2rem; font-weight: 800; color: #38a169;">{min_w} kg - {max_w} kg</div>
                <div style="font-size: 0.85rem; color: #718096;">Based on clinical Devine / Robinson formulas</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 7. BMR
    with tab_bmr:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Basal Metabolic Rate (BMR)")
        c1, c2 = st.columns(2)
        with c1:
            w_b = st.number_input("Weight (kg)", 30.0, 200.0, 70.0, key="calc_w_bmr")
            h_b = st.number_input("Height (cm)", 100.0, 230.0, 170.0, key="calc_h_bmr")
            age_b = st.number_input("Age", 15, 100, 30, key="calc_age_bmr")
            gen_b = st.selectbox("Gender", ["Male", "Female"], key="calc_gen_bmr")
        with c2:
            bmr_val = calculate_bmr(w_b, h_b, age_b, gen_b)
            st.markdown(f"""
            <div style="background: #edf2f7; padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 0.9rem; color: #4a5568; font-weight: 600;">BASAL METABOLIC RATE (BMR)</div>
                <div style="font-size: 2.5rem; font-weight: 800; color: #805ad5;">{bmr_val} kcal/day</div>
                <div style="font-size: 0.85rem; color: #718096;">Energy expended at complete rest</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 8. WHR
    with tab_whr:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Waist-to-Hip Ratio (WHR) Calculator")
        c1, c2 = st.columns(2)
        with c1:
            waist = st.number_input("Waist Circumference (cm)", 40.0, 180.0, 85.0, key="calc_waist")
            hip = st.number_input("Hip Circumference (cm)", 40.0, 180.0, 98.0, key="calc_hip")
            gen_whr = st.selectbox("Gender", ["Male", "Female"], key="calc_gen_whr")
        with c2:
            whr, whr_cat = calculate_whr(waist, hip, gen_whr)
            st.markdown(f"""
            <div style="background: #edf2f7; padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 0.9rem; color: #4a5568; font-weight: 600;">WAIST-TO-HIP RATIO</div>
                <div style="font-size: 2.5rem; font-weight: 800; color: #2b6cb0;">{whr}</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #2b6cb0;">Category: {whr_cat}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 9. BSA
    with tab_bsa:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Body Surface Area (BSA) Calculator (Mosteller Formula)")
        c1, c2 = st.columns(2)
        with c1:
            h_bsa = st.number_input("Height (cm)", 100.0, 230.0, 170.0, key="calc_h_bsa")
            w_bsa = st.number_input("Weight (kg)", 30.0, 200.0, 70.0, key="calc_w_bsa")
        with c2:
            bsa_val = calculate_bsa(h_bsa, w_bsa)
            st.markdown(f"""
            <div style="background: #edf2f7; padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 0.9rem; color: #4a5568; font-weight: 600;">BODY SURFACE AREA</div>
                <div style="font-size: 2.5rem; font-weight: 800; color: #2b6cb0;">{bsa_val} m²</div>
                <div style="font-size: 0.85rem; color: #718096;">Used for clinical dosage scaling</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
