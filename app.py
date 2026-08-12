import streamlit as st
import pandas as pd

from risk_engine import calculate_final_risk
from weather_api import get_rainfall_data

# ==========================================
# PAGE SETTINGS & CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="Kerala Disaster Risk Monitor",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Injecting Custom UI/UX Styling
st.markdown("""
    <style>
    /* Main Background & Fonts */
    .stApp {
        background-color: #0E1117;
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom Headers */
    h1, h2, h3 {
        color: #F8F9FA !important;
        font-weight: 700 !important;
    }

    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #1E232A;
        border: 1px solid #2B303A;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border-left: 5px solid #00D26A; /* Neon Green Accent */
    }
    
    /* Styled Buttons */
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px 24px;
        transition: all 0.3s ease;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(37, 99, 235, 0.4);
    }
    
    /* Alert Banners */
    .stAlert {
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# HERO BANNER & HEADER
# ==========================================
st.image("https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1600&q=80", use_container_width=True)

st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 3rem; margin-bottom: 0;">🌧️ Kerala Disaster Risk Monitor</h1>
        <p style="color: #9CA3AF; font-size: 1.2rem;">AI-Powered Landslide Prediction & Emergency Alert System</p>
    </div>
""", unsafe_allow_html=True)


# ==========================================
# KERALA LOCATIONS & DEMO DATA
# ==========================================
locations = {
    "Wayanad": {"latitude": 11.6854, "longitude": 76.1320},
    "Idukki": {"latitude": 9.9189, "longitude": 76.9680},
    "Kozhikode": {"latitude": 11.2588, "longitude": 75.7804},
    "Malappuram": {"latitude": 11.0510, "longitude": 76.0711},
    "Kannur": {"latitude": 11.8745, "longitude": 75.3704},
    "Kasaragod": {"latitude": 12.5102, "longitude": 74.9852},
    "Palakkad": {"latitude": 10.7867, "longitude": 76.6548},
    "Thrissur": {"latitude": 10.5276, "longitude": 76.2144},
    "Ernakulam": {"latitude": 9.9816, "longitude": 76.2999},
    "Kottayam": {"latitude": 9.5916, "longitude": 76.5222},
    "Alappuzha": {"latitude": 9.4981, "longitude": 76.3388},
    "Pathanamthitta": {"latitude": 9.2648, "longitude": 76.7870},
    "Kollam": {"latitude": 8.8932, "longitude": 76.6141},
    "Thiruvananthapuram": {"latitude": 8.5241, "longitude": 76.9366}
}

demo_data = {
    "Wayanad": {"rainfall_24h": 180, "rainfall_3h": 90, "soil_moisture": 85, "river_level": 8, "slope": 32, "previous_rainfall": 170},
    "Idukki": {"rainfall_24h": 160, "rainfall_3h": 75, "soil_moisture": 80, "river_level": 7, "slope": 35, "previous_rainfall": 150},
    "Kozhikode": {"rainfall_24h": 100, "rainfall_3h": 40, "soil_moisture": 65, "river_level": 5, "slope": 20, "previous_rainfall": 90},
    "Malappuram": {"rainfall_24h": 120, "rainfall_3h": 50, "soil_moisture": 70, "river_level": 6, "slope": 25, "previous_rainfall": 110},
    "Kannur": {"rainfall_24h": 60, "rainfall_3h": 20, "soil_moisture": 45, "river_level": 3, "slope": 15, "previous_rainfall": 50},
    "Kasaragod": {"rainfall_24h": 70, "rainfall_3h": 25, "soil_moisture": 50, "river_level": 4, "slope": 18, "previous_rainfall": 60},
    "Palakkad": {"rainfall_24h": 110, "rainfall_3h": 45, "soil_moisture": 60, "river_level": 5, "slope": 22, "previous_rainfall": 100},
    "Thrissur": {"rainfall_24h": 90, "rainfall_3h": 35, "soil_moisture": 55, "river_level": 4, "slope": 18, "previous_rainfall": 80},
    "Ernakulam": {"rainfall_24h": 80, "rainfall_3h": 30, "soil_moisture": 50, "river_level": 5, "slope": 12, "previous_rainfall": 70},
    "Kottayam": {"rainfall_24h": 130, "rainfall_3h": 55, "soil_moisture": 72, "river_level": 6, "slope": 28, "previous_rainfall": 120},
    "Alappuzha": {"rainfall_24h": 100, "rainfall_3h": 45, "soil_moisture": 68, "river_level": 8, "slope": 5, "previous_rainfall": 90},
    "Pathanamthitta": {"rainfall_24h": 140, "rainfall_3h": 60, "soil_moisture": 75, "river_level": 7, "slope": 30, "previous_rainfall": 130},
    "Kollam": {"rainfall_24h": 85, "rainfall_3h": 35, "soil_moisture": 55, "river_level": 5, "slope": 15, "previous_rainfall": 75},
    "Thiruvananthapuram": {"rainfall_24h": 75, "rainfall_3h": 30, "soil_moisture": 50, "river_level": 4, "slope": 14, "previous_rainfall": 65}
}


# ==========================================
# APP NAVIGATION (TABS)
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🔴 Live Risk Monitor", 
    "🗺️ Threat Map", 
    "🛡️ Evacuation Protocols", 
    "📞 Emergency Helplines"
])

# ------------------------------------------
# TAB 1: LIVE RISK MONITOR
# ------------------------------------------
with tab1:
    st.header("📍 Monitor Regional Risk")
    
    selected_location = st.selectbox("Select Kerala District to Monitor", list(locations.keys()))
    location = locations[selected_location]
    latitude, longitude = location["latitude"], location["longitude"]

    st.write("---")
    
    # Live Weather Integration
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🌩️ API Weather Fetch")
        if "live_weather" not in st.session_state:
            st.session_state.live_weather = None
        if "weather_location" not in st.session_state:
            st.session_state.weather_location = None

        if st.button("📡 Fetch Live API Data"):
            with st.spinner("Connecting to Open-Meteo Satellite..."):
                st.session_state.live_weather = get_rainfall_data(latitude, longitude)
                st.session_state.weather_location = selected_location
                if st.session_state.live_weather:
                    st.success("✅ Uplink established!")
                else:
                    st.error("❌ Connection failed.")

    with col2:
        if st.session_state.live_weather and st.session_state.weather_location == selected_location:
            st.subheader("Current Atmospheric Data")
            w_col1, w_col2, w_col3 = st.columns(3)
            w_col1.metric("Rainfall (Last 3h)", f"{st.session_state.live_weather['rainfall_3h']:.2f} mm")
            w_col2.metric("Rainfall (Last 24h)", f"{st.session_state.live_weather['rainfall_24h']:.2f} mm")
            w_col3.metric("Humidity", f"{st.session_state.live_weather['humidity']:.0f}%")
        else:
            st.info("Awaiting live satellite fetch. Using local historical demo data as fallback.")

    st.write("---")

    # Environmental Inputs & Prediction
    st.subheader("🌍 Terrain & Moisture Variables")
    values = demo_data[selected_location]
    use_live_weather = (st.session_state.live_weather is not None and st.session_state.weather_location == selected_location)

    default_r24 = float(st.session_state.live_weather["rainfall_24h"]) if use_live_weather else float(values["rainfall_24h"])
    default_r3 = float(st.session_state.live_weather["rainfall_3h"]) if use_live_weather else float(values["rainfall_3h"])

    input_col1, input_col2 = st.columns(2)
    with input_col1:
        rainfall_24h = st.number_input("Rainfall in last 24 hours (mm)", value=default_r24)
        rainfall_3h = st.number_input("Rainfall in last 3 hours (mm)", value=default_r3)
        soil_moisture = st.number_input("Soil moisture (%)", value=float(values["soil_moisture"]))
    with input_col2:
        river_level = st.number_input("River level", value=float(values["river_level"]))
        slope = st.number_input("Slope (degrees)", value=float(values["slope"]))
        previous_rainfall = st.number_input("Previous rainfall (mm)", value=float(values["previous_rainfall"]))

    st.write("---")
    
    # ML Prediction Trigger
    if st.button("🔍 RUN AI RISK ASSESSMENT", use_container_width=True):
        result = calculate_final_risk(rainfall_24h, rainfall_3h, soil_moisture, river_level, slope, previous_rainfall)
        final_risk = result["final_risk"]

        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.subheader("🚨 Final Risk Assessment")
            if final_risk == "HIGH":
                st.error("🔴 CRITICAL: HIGH RISK")
                try:
                    st.audio("alert.mp3", autoplay=True)
                except Exception:
                    pass
            elif final_risk == "MEDIUM":
                st.warning("🟠 WARNING: MEDIUM RISK")
            else:
                st.success("🟢 STABLE: LOW RISK")
            
            st.write(f"**ML Landslide Probability:** {result['ml_probability']:.2%}")
            
            # Progress bar for visual probability
            st.progress(float(result['ml_probability']))

        with res_col2:
            st.subheader("📡 Regional Mobile Broadcast")
            st.caption("Simulate broadcasting emergency alerts to residents in the danger zone.")
            target_phone = st.text_input("Target Mobile Number:", placeholder="9876543210")
            
            if st.button("📲 SEND EMERGENCY ALERT", type="primary"):
                if target_phone:
                    st.success(f"⚡ Emergency alert broadcast dispatched to **{target_phone}**!")
                    st.code(
                        f"🚨 EMERGENCY ALERT: High Landslide Risk predicted in {selected_location}. "
                        f"Current conditions: {rainfall_24h}mm rainfall. Move to safe ground immediately.",
                        language="markdown"
                    )
                else:
                    st.warning("Please enter a valid mobile number.")


# ------------------------------------------
# TAB 2: THREAT MAP
# ------------------------------------------
with tab2:
    st.header("🗺️ Topographical ML Threat Map")
    st.write("Visual overview of risk levels across all monitored districts.")
    
    map_rows = []
    for district in locations:
        v = demo_data[district]
        res = calculate_final_risk(v["rainfall_24h"], v["rainfall_3h"], v["soil_moisture"], v["river_level"], v["slope"], v["previous_rainfall"])
        color = "#FF0000" if res["final_risk"] == "HIGH" else "#FFA500" if res["final_risk"] == "MEDIUM" else "#00FF00"
        
        map_rows.append({
            "District": district,
            "latitude": locations[district]["latitude"],
            "longitude": locations[district]["longitude"],
            "Risk Level": res["final_risk"],
            "Probability": f"{res['ml_probability']:.1%}",
            "color": color
        })

    map_df = pd.DataFrame(map_rows)
    
    st.map(map_df, latitude="latitude", longitude="longitude", size=2000, color="color", zoom=6)
    
    st.dataframe(map_df.drop(columns=["color", "latitude", "longitude"]), use_container_width=True)


# ------------------------------------------
# TAB 3: EVACUATION PROTOCOLS
# ------------------------------------------
with tab3:
    st.header("🛡️ Standard Evacuation Protocols")
    st.image("https://images.unsplash.com/photo-1628042571216-40742ddb9e83?auto=format&fit=crop&w=1600&q=80", caption="Preparedness saves lives.", use_container_width=True)
    
    st.markdown("""
    ### 🔴 During a High-Risk Alert
    * **Evacuate Immediately:** Do not wait for a landslide to happen. If ordered to evacuate, leave instantly.
    * **Avoid River Valleys:** Stay away from the path of rivers, streams, and low-lying valleys.
    * **Listen to Unusual Sounds:** Trees cracking or boulders knocking together indicate moving debris. 
    * **Stay Awake & Alert:** Many severe landslides occur at night. If heavy rains continue, stay awake.

    ### 🟢 Preparation (Low/Medium Risk)
    * **Emergency Kit:** Have a grab-and-go bag with a flashlight, batteries, basic first aid, and essential documents.
    * **Know Your Route:** Identify a safe evacuation path that avoids steep slopes and streams.
    * **Stay Informed:** Keep monitoring this dashboard and local news outlets.
    """)


# ------------------------------------------
# TAB 4: EMERGENCY HELPLINES
# ------------------------------------------
with tab4:
    st.header("📞 KSDMA Official Emergency Helplines")
    st.info("The following numbers are official lines provided by the Kerala State Disaster Management Authority (KSDMA).")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("State & National Helplines")
        st.markdown("""
        * **Distress Helpline (ERSS):** 112
        * **State Emergency Helpline:** 1070 / 1079
        * **Ambulance Service:** 108
        * **Fire Service Control Room:** 101
        * **Police Helpline:** 100
        """)
        
    with col_b:
        st.subheader("District & Specialized")
        st.markdown("""
        * **District Control Room:** 1077
        * **Highway Police Alert:** 9846100100
        * **Coastal Police Helpline:** 1093
        * **National Disaster Response Force (NDRF):** 04177-246594
        """)

# ==========================================
# FOOTER
# ==========================================
st.divider()
st.markdown("<p style='text-align: center; color: #6B7280;'>Developed as a technical prototype. Data models and alert interfaces are for demonstration purposes.</p>", unsafe_allow_html=True)