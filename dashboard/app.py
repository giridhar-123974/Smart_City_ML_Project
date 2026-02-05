import streamlit as st
import joblib
import numpy as np

# Load trained models
air_model = joblib.load("../models/air_quality_random_forest.pkl")
traffic_model = joblib.load("../models/traffic_random_forest.pkl")

# Page settings
st.set_page_config(
    page_title="Smart City Command Center",
    page_icon="🌆",
    layout="wide"
)

# Sidebar
st.sidebar.title("🌆 Smart City AI Platform")
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard Overview", "🚦 Traffic Control", "🌫️ Air Quality Monitor", "⚡ Energy Intelligence"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Authority Dashboard**

AI-powered system for:
• Traffic management  
• Pollution monitoring  
• Energy planning
""")

# ---------------- DASHBOARD OVERVIEW ----------------
if page == "🏠 Dashboard Overview":
    st.markdown("## 🏙️ Smart City Intelligence Command Center")

    col1, col2, col3 = st.columns(3)

    col1.metric("Traffic Status", "HIGH", "↑ Congestion")
    col2.metric("Air Quality", "MODERATE", "↓ Improving")
    col3.metric("Energy Demand", "STABLE", "Normal Load")

    st.markdown("---")

    st.subheader("🧠 AI System Insights")
    st.success("""
• Traffic congestion is increasing during peak hours  
• Pollution levels require monitoring in urban zones  
• Energy consumption is within safe operational limits  

**Recommended Actions:**  
✔ Optimize traffic signals  
✔ Issue pollution advisories  
✔ Maintain energy distribution
""")

# ---------------- TRAFFIC ----------------
elif page == "🚦 Traffic Control":
    st.markdown("## 🚦 Traffic Congestion Prediction")

    col1, col2, col3, col4 = st.columns(4)

    car = col1.number_input("🚗 Car Count", value=100)
    bike = col2.number_input("🏍️ Bike Count", value=50)
    bus = col3.number_input("🚌 Bus Count", value=10)
    truck = col4.number_input("🚚 Truck Count", value=5)

    total = car + bike + bus + truck

    if st.button("🔍 Analyze Traffic"):
        traffic_sample = np.array([[car, bike, bus, truck, total]])
        result = traffic_model.predict(traffic_sample)[0]

        levels = ["Low", "Medium", "High", "Very High"]
        level = levels[int(result)]

        if level in ["High", "Very High"]:
            st.error(f"🚨 Traffic Level: **{level}**")
            st.warning("AI Recommendation: Activate congestion control and reroute traffic.")
        else:
            st.success(f"✅ Traffic Level: **{level}**")

# ---------------- AIR QUALITY ----------------
elif page == "🌫️ Air Quality Monitor":
    st.markdown("## 🌫️ Air Quality Prediction (CO Level)")

    col1, col2, col3 = st.columns(3)

    with col1:
        PT08_S1 = st.number_input("PT08.S1(CO)", value=1360.0)
        NMHC = st.number_input("NMHC(GT)", value=150.0)
        C6H6 = st.number_input("C6H6(GT)", value=11.9)
        PT08_S2 = st.number_input("PT08.S2(NMHC)", value=1046.0)

    with col2:
        NOx = st.number_input("NOx(GT)", value=166.0)
        PT08_S3 = st.number_input("PT08.S3(NOx)", value=1056.0)
        NO2 = st.number_input("NO2(GT)", value=113.0)
        PT08_S4 = st.number_input("PT08.S4(NO2)", value=1692.0)

    with col3:
        PT08_S5 = st.number_input("PT08.S5(O3)", value=1268.0)
        T = st.number_input("Temperature (°C)", value=13.6)
        RH = st.number_input("Humidity (%)", value=48.9)
        AH = st.number_input("Absolute Humidity", value=0.7578)

    if st.button("🔍 Analyze Air Quality"):
        sample = np.array([[PT08_S1, NMHC, C6H6, PT08_S2, NOx,
                             PT08_S3, NO2, PT08_S4, PT08_S5, T, RH, AH]])
        result = air_model.predict(sample)[0]

        st.metric("Predicted CO(GT)", f"{result:.2f}")

        if result > 5:
            st.error("🚨 High Pollution Alert! Immediate action recommended.")
        else:
            st.success("✅ Air quality is within acceptable limits.")

# ---------------- ENERGY ----------------
elif page == "⚡ Energy Intelligence":
    st.markdown("## ⚡ Energy Consumption Intelligence")

    st.info("""
✔ Energy forecasting model trained successfully  
✔ System ready for real-time data integration  
✔ Supports power distribution planning
""")

    st.markdown("""
**Future Scope:**
• Real-time smart meter integration  
• Peak demand alerts  
• Renewable energy optimization
""")
