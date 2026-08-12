import pandas as pd

print("Loading cleaned dataset...")
df = pd.read_csv("landslide_inventory_cleaned.csv")

# Clean up column names just in case there are hidden spaces from the PDF
df.columns = df.columns.astype(str).str.strip()

# Find the column that represents the State
state_col = None
for col in df.columns:
    if 'state' in col.lower():
        state_col = col
        break

if state_col:
    print(f"Searching in column: '{state_col}'")
    
    # Filter rows where the state contains 'Kerala'
    kerala_df = df[df[state_col].astype(str).str.contains('Kerala', case=False, na=False)]
    
    print("\n--- Filtering Complete ---")
    print(f"Total Kerala landslides found: {len(kerala_df)}")
    
    # Save to our final target file
    kerala_df.to_csv("kerala_landslides.csv", index=False)
    print("Saved as: kerala_landslides.csv")
else:
    print("Error: Could not find a 'State' column in the dataset.")
    print("Columns available:", df.columns.tolist())