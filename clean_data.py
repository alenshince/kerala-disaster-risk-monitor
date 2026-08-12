import pandas as pd

print("Loading raw extracted data...")

# Read the CSV, telling Pandas not to guess the headers yet
df = pd.read_csv("landslide_inventory_extracted.csv", header=None)

# Set the 2nd row (index 1) as the actual column names
df.columns = df.iloc[1]

# Drop the first two rows (the title and the old header row)
df = df[2:].reset_index(drop=True)

print("\n--- Cleaning Successful ---")
print(f"Total clean rows: {len(df)}")
print("\nColumns detected:")
print(df.columns.tolist())

# Save it as a new file so we don't overwrite the original raw data
df.to_csv("landslide_inventory_cleaned.csv", index=False)
print("\nSaved as: landslide_inventory_cleaned.csv")