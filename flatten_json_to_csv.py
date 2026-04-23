import json
import pandas as pd
import os
from pathlib import Path

# Initialize a list to hold the flattened rows
rows = []

# Path to the jsonDataComposite directory
json_dir = Path('Data/jsonDataComposite')

# Iterate through all JSON files in the directory
for json_file in sorted(json_dir.glob('*.json')):
    print(f"Processing {json_file.name}...")
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Iterate through the results
        for algorithm, algo_data in data['results'].items():
            for n_people_str, pc_data in algo_data.items():
                n_people = int(n_people_str)
                for cohesion_str, cs_data in pc_data.items():
                    cohesion = int(cohesion_str)
                    for iteration, score in enumerate(cs_data['scores']):
                        time_val = cs_data['times'][iteration]
                        rows.append({
                            'algorithm': algorithm,
                            'n_people': n_people,
                            'cohesion': cohesion,
                            'iteration': iteration,
                            'score': score,
                            'time': time_val
                        })
    except Exception as e:
        print(f"Error processing {json_file.name}: {e}")

# Create a DataFrame
df = pd.DataFrame(rows)

# Save to CSV in Data folder
df.to_csv('Data/flattened_composite_experiments_data.csv', index=False)

print(f"\nData flattened and saved to Data/flattened_experiments_data.csv")
print(f"Total rows: {len(df)}")
