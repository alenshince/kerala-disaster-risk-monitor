# 🌧️ Kerala Disaster Risk Monitor

An experimental AI and machine-learning prototype designed to explore
landslide and flood risk monitoring in Kerala, India.

## 🚨 Important

This project is currently a **prototype for research and educational purposes**.

It is NOT an official disaster-warning system and must NOT be used
for emergency decisions or evacuation decisions.

---

## 🎯 Project Goal

The long-term goal is to develop a system that can:

- Monitor rainfall and environmental conditions
- Estimate landslide and flood risk for specific locations
- Use historical Kerala disaster data
- Combine rule-based risk assessment with machine learning
- Display risk information on a map
- Eventually support automated warning mechanisms

The project is being developed step-by-step from a beginner-friendly
prototype toward a more realistic data-driven system.

---

## 🧠 Current System

The current prototype contains:

- 🌧️ Live rainfall data
- 📍 Kerala district selection
- 🗺️ Risk map
- 📋 Rule-based risk assessment
- 🤖 Machine-learning prediction
- 📊 Environmental condition inputs
- 🛡️ Evacuation information
- 📞 Emergency information
- 📲 Simulated emergency alert interface

---

## 🏗️ Current Architecture

```text
Weather Data
     │
     ▼
Environmental Conditions
     │
     ├──────────────┐
     ▼              ▼
Rule Engine     ML Model
     │              │
     └──────┬───────┘
            ▼
      Risk Assessment
            │
            ▼
       Streamlit UI