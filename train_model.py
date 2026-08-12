import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

print("Loading the new 3,000-row training dataset...")
df = pd.read_csv("final_training_data.csv")

# These are the environmental features the model will look at
X = df[['rainfall_24h', 'rainfall_3h', 'soil_moisture', 'river_level', 'slope', 'previous_rainfall']]

# This is the answer key (1 = landslide, 0 = safe)
y = df['landslide']

print("Training the AI model (this might take a few seconds)...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

print("Saving the upgraded model...")
with open("landslide_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\n--- Success! ---")
print("✅ Model trained and saved as landslide_model.pkl!")