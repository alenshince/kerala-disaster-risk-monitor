import joblib
import pandas as pd


# ==========================================
# LOAD THE MACHINE LEARNING MODEL
# ==========================================

model = joblib.load("landslide_model.pkl")


# ==========================================
# 1. RULE-BASED RISK
# ==========================================

def calculate_rule_risk(
    rainfall_24h,
    rainfall_3h,
    soil_moisture,
    river_level,
    slope,
    previous_rainfall
):

    score = 0

    # Rainfall in 24 hours
    if rainfall_24h >= 150:
        score += 3
    elif rainfall_24h >= 100:
        score += 2
    elif rainfall_24h >= 50:
        score += 1

    # Rainfall in 3 hours
    if rainfall_3h >= 70:
        score += 3
    elif rainfall_3h >= 40:
        score += 2
    elif rainfall_3h >= 20:
        score += 1

    # Soil moisture
    if soil_moisture >= 80:
        score += 3
    elif soil_moisture >= 60:
        score += 2
    elif soil_moisture >= 40:
        score += 1

    # River level
    if river_level >= 8:
        score += 3
    elif river_level >= 6:
        score += 2
    elif river_level >= 4:
        score += 1

    # Slope
    if slope >= 30:
        score += 3
    elif slope >= 20:
        score += 2
    elif slope >= 10:
        score += 1

    # Previous rainfall
    if previous_rainfall >= 150:
        score += 3
    elif previous_rainfall >= 100:
        score += 2
    elif previous_rainfall >= 50:
        score += 1


    # Determine risk level

    if score >= 12:
        risk = "HIGH"

    elif score >= 7:
        risk = "MEDIUM"

    else:
        risk = "LOW"


    return risk, score


# ==========================================
# 2. MACHINE LEARNING RISK
# ==========================================

def calculate_ml_risk(
    rainfall_24h,
    rainfall_3h,
    soil_moisture,
    river_level,
    slope,
    previous_rainfall
):

    # Put the current conditions into a table

    input_data = pd.DataFrame([{
        "rainfall_24h": rainfall_24h,
        "rainfall_3h": rainfall_3h,
        "soil_moisture": soil_moisture,
        "river_level": river_level,
        "slope": slope,
        "previous_rainfall": previous_rainfall
    }])


    # ML prediction

    prediction = model.predict(input_data)[0]


    # Probability of landslide

    probability = model.predict_proba(input_data)[0][1]


    # Convert probability to risk level

    if probability >= 0.70:
        risk = "HIGH"

    elif probability >= 0.40:
        risk = "MEDIUM"

    else:
        risk = "LOW"


    return risk, probability, prediction


# ==========================================
# 3. COMBINE RULE + ML
# ==========================================

def calculate_final_risk(
    rainfall_24h,
    rainfall_3h,
    soil_moisture,
    river_level,
    slope,
    previous_rainfall
):

    # Get rule result

    rule_risk, rule_score = calculate_rule_risk(
        rainfall_24h,
        rainfall_3h,
        soil_moisture,
        river_level,
        slope,
        previous_rainfall
    )


    # Get ML result

    ml_risk, ml_probability, ml_prediction = calculate_ml_risk(
        rainfall_24h,
        rainfall_3h,
        soil_moisture,
        river_level,
        slope,
        previous_rainfall
    )


    # Risk levels

    risk_value = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3
    }


    # Take the more serious result

    final_value = max(
        risk_value[rule_risk],
        risk_value[ml_risk]
    )


    final_risk = {
        1: "LOW",
        2: "MEDIUM",
        3: "HIGH"
    }[final_value]


    return {
        "rule_risk": rule_risk,
        "rule_score": rule_score,
        "ml_risk": ml_risk,
        "ml_probability": ml_probability,
        "ml_prediction": ml_prediction,
        "final_risk": final_risk
    }


# ==========================================
# 4. TEST THE COMPLETE SYSTEM
# ==========================================

if __name__ == "__main__":

    # Demo environmental conditions

    rainfall_24h = 180
    rainfall_3h = 90
    soil_moisture = 85
    river_level = 8
    slope = 32
    previous_rainfall = 170


    # Calculate everything

    result = calculate_final_risk(
        rainfall_24h,
        rainfall_3h,
        soil_moisture,
        river_level,
        slope,
        previous_rainfall
    )


    # ======================================
    # DISPLAY RESULTS
    # ======================================

    print()
    print("=" * 55)
    print("       KERALA DISASTER RISK SYSTEM")
    print("=" * 55)

    print()

    print("ENVIRONMENTAL CONDITIONS")
    print("------------------------")

    print("Rainfall (24h):", rainfall_24h, "mm")
    print("Rainfall (3h):", rainfall_3h, "mm")
    print("Soil moisture:", soil_moisture, "%")
    print("River level:", river_level)
    print("Slope:", slope, "degrees")
    print("Previous rainfall:", previous_rainfall, "mm")

    print()

    print("RULE-BASED SYSTEM")
    print("------------------")

    print("Risk:", result["rule_risk"])
    print("Score:", result["rule_score"])

    print()

    print("MACHINE LEARNING SYSTEM")
    print("-----------------------")

    print("Prediction:", result["ml_prediction"])
    print("Risk:", result["ml_risk"])
    print(
        "Landslide probability:",
        f"{result['ml_probability']:.2%}"
    )

    print()

    print("========================================")
    print("FINAL RISK:", result["final_risk"])
    print("========================================")

    print()

    if result["final_risk"] == "HIGH":

        print("!!! HIGH RISK !!!")
        print("Demo warning would be triggered.")

    elif result["final_risk"] == "MEDIUM":

        print("CAUTION")
        print("Continue monitoring conditions.")

    else:

        print("LOW RISK")
        print("No demo warning required.")

    print()