import pandas as pd
import numpy as np

print("Generating robust ML training dataset...")

# We will generate exactly 1500 landslide events and 1500 safe events (3000 total)
num_events = 1500

print("Simulating historical weather conditions...")

# 1. Simulate Landslide Events (landslide = 1)
real_events = pd.DataFrame({
    'rainfall_24h': np.random.uniform(100, 300, num_events),
    'rainfall_3h': np.random.uniform(30, 100, num_events),
    'soil_moisture': np.random.uniform(70, 99, num_events),
    'river_level': np.random.uniform(5, 12, num_events),
    'slope': np.random.uniform(20, 50, num_events),
    'previous_rainfall': np.random.uniform(150, 400, num_events),
    'landslide': 1
})

# 2. Simulate Safe Days (landslide = 0)
safe_events = pd.DataFrame({
    'rainfall_24h': np.random.uniform(0, 50, num_events),
    'rainfall_3h': np.random.uniform(0, 15, num_events),
    'soil_moisture': np.random.uniform(20, 60, num_events),
    'river_level': np.random.uniform(1, 4, num_events),
    'slope': np.random.uniform(20, 50, num_events), 
    'previous_rainfall': np.random.uniform(0, 50, num_events),
    'landslide': 0
})

# Combine them into one large dataset
final_dataset = pd.concat([real_events, safe_events], ignore_index=True)

# Shuffle the dataset so the model learns properly
final_dataset = final_dataset.sample(frac=1).reset_index(drop=True)

# Save the final file
final_dataset.to_csv("final_training_data.csv", index=False)

print("\n--- Training Dataset Complete ---")
print(f"Total training records generated: {len(final_dataset)}")
print("Saved as: final_training_data.csv")