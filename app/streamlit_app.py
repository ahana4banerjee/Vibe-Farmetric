# app/streamlit_app.py
import streamlit as st
from predictor import load_ml_assets, predict_fertilizer
from sustainability import SustainabilityEngine

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Vibe-Farmetric | Agritech AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# LOAD ASSETS
# ==========================================
model, preprocessor, label_encoder, feature_columns = load_ml_assets()

# ==========================================
# UI: HEADER & DESCRIPTION
# ==========================================
st.title("🌱 Vibe-Farmetric")
st.subheader("AI-Assisted Sustainable Fertilizer Intelligence System")
st.markdown("""
This dashboard provides precision fertilizer recommendations while actively monitoring for 
**nutrient overuse, soil salinity risks, and sustainability penalties**. 
Adjust the farm parameters in the sidebar to generate real-time agronomic insights.
""")
st.divider()

# ==========================================
# UI: SIDEBAR INPUT PANEL
# ==========================================
st.sidebar.header("📋 Farm & Soil Parameters")

# Group 1: Soil Health
st.sidebar.subheader("1. Soil Properties")
soil_type = st.sidebar.selectbox("Soil Type", ['Loamy', 'Sandy', 'Clay', 'Black', 'Red'])
soil_ph = st.sidebar.slider("Soil pH", min_value=4.0, max_value=9.0, value=6.5, step=0.1, help="Ideal range is typically 6.0 - 7.5")
organic_carbon = st.sidebar.slider("Organic Carbon (%)", 0.1, 2.5, 1.0, 0.1)
ec = st.sidebar.slider("Electrical Conductivity (ds/m)", 0.1, 3.0, 0.8, 0.1, help="Values > 1.5 indicate potential salinity risk")

# Group 2: NPK Levels
st.sidebar.subheader("2. Macronutrients (ppm)")
n_level = st.sidebar.number_input("Nitrogen Level", min_value=0, max_value=200, value=80)
p_level = st.sidebar.number_input("Phosphorus Level", min_value=0, max_value=150, value=30)
k_level = st.sidebar.number_input("Potassium Level", min_value=0, max_value=150, value=40)

# Group 3: Environment & Crop
st.sidebar.subheader("3. Environment & Crop")
temperature = st.sidebar.slider("Temperature (°C)", 10.0, 45.0, 25.0, 0.5)
humidity = st.sidebar.slider("Humidity (%)", 20, 100, 60)
rainfall = st.sidebar.slider("Rainfall (mm)", 0, 300, 100)
crop_type = st.sidebar.selectbox("Crop Type", ['Wheat', 'Maize', 'Sugarcane', 'Cotton', 'Rice', 'Millets'])
season = st.sidebar.selectbox("Season", ['Kharif', 'Rabi', 'Zaid'])

# Group 4: Historical Data
st.sidebar.subheader("4. Historical Context")
yield_last = st.sidebar.slider("Yield Last Season (q/ha)", 0, 50, 20)

# FIX: Changed from a selectbox (text) to a number_input (numerical amount)
fert_last = st.sidebar.number_input("Amount of Fertilizer Used Last Season", min_value=0.0, max_value=500.0, value=120.0)

# Compile inputs into a dictionary matching the exact training dataset schema
farm_data = {
    'Soil_Type': soil_type,
    'Soil_pH': soil_ph,
    'Soil_Moisture': 50.0,            # INJECTED DEFAULT
    'Organic_Carbon': organic_carbon,
    'Electrical_Conductivity': ec,
    'Nitrogen_Level': n_level,
    'Phosphorus_Level': p_level,
    'Potassium_Level': k_level,
    'Temperature': temperature,
    'Humidity': humidity,
    'Rainfall': rainfall,
    'Crop_Type': crop_type,
    'Crop_Growth_Stage': 'Unknown',   # INJECTED DEFAULT
    'Season': season,
    'Irrigation_Type': 'Unknown',     # INJECTED DEFAULT
    'Previous_Crop': 'Unknown',       # INJECTED DEFAULT
    'Region': 'Unknown',              # INJECTED DEFAULT
    'Fertilizer_Used_Last_Season': fert_last,
    'Yield_Last_Season': yield_last
}

# ==========================================
# PREDICTION & ANALYSIS EXECUTION
# ==========================================
if model is not None:
    # 1. Get ML Recommendation
    recommended_fertilizer = predict_fertilizer(farm_data, model, preprocessor, label_encoder)
    
    # 2. Get Sustainability Analysis
    engine = SustainabilityEngine(farm_data)
    analysis = engine.evaluate()

    # ==========================================
# UI: MAIN DASHBOARD
# ==========================================
    col1, col2, col3 = st.columns(3)

    # A. Recommended Fertilizer Card
    with col1:
        st.markdown("### 🎯 Recommended Fertilizer")
        st.info(f"**{recommended_fertilizer}**", icon="✅")

    # B. Sustainability Score Card
    with col2:
        st.markdown("### 🌍 Sustainability Score")
        score = analysis['sustainability_score']
        # Dynamic color based on score
        if score >= 75:
            st.success(f"**{score} / 100 ({analysis['category']})**", icon="🌟")
        elif score >= 60:
            st.warning(f"**{score} / 100 ({analysis['category']})**", icon="⚠️")
        else:
            st.error(f"**{score} / 100 ({analysis['category']})**", icon="🛑")

    # C. Risk Level Card
    with col3:
        st.markdown("### 📉 Agronomic Risk Level")
        risk = analysis['risk_level']
        if risk == "Low":
            st.success(f"**{risk} Risk**", icon="🛡️")
        elif risk == "Moderate":
            st.warning(f"**{risk} Risk**", icon="🔍")
        else:
            st.error(f"**{risk} Risk**", icon="🔥")

    st.markdown("---")

    # D & E. Warnings, Recommendations & Details using Tabs
    tab1, tab2, tab3 = st.tabs(["🚨 Warnings & Alerts", "💡 Agronomy Recommendations", "📊 Score Breakdown"])

    with tab1:
        if analysis['warnings']:
            for warning in analysis['warnings']:
                # Differentiate visual severity based on text content
                if "High confidence" in warning or "Warning" in warning:
                    st.error(warning)
                else:
                    st.warning(warning)
        else:
            st.success("No critical overuse patterns or sustainability risks detected. Great job!")

    with tab2:
        if analysis['recommendations']:
            for rec in analysis['recommendations']:
                st.info(f"👉 {rec}")
        else:
            st.write("Maintain current balanced agricultural practices.")

    with tab3:
        st.write("### Penalty Deductions")
        if analysis['penalty_breakdown']:
            for penalty_name, deduction in analysis['penalty_breakdown'].items():
                st.metric(label=penalty_name, value=f"{deduction} pts")
        else:
            st.write("No penalties applied. Perfect score.")
        
        with st.expander("View Raw Assessment Data"):
            st.json(analysis)

# ==========================================
# FOOTER & DISCLAIMER
# ==========================================
st.markdown("---")
st.caption(f"**Disclaimer:** {analysis['disclaimer']} Always consult local agricultural extension services for certified soil testing and diagnosis.")