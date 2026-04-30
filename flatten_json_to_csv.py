import json
import pandas as pd
import os
import sys
import argparse
from pathlib import Path

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Flatten JSON files from a directory to CSV')
parser.add_argument('json_dir', help='Path to the directory containing JSON files')
parser.add_argument('output_file', help='Path for the output CSV file')
args = parser.parse_args()

# Initialize a list to hold the flattened rows
rows = []

# Path to the JSON directory
json_dir = Path(args.json_dir)

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
df.to_csv(args.output_file, index=False)

print(f"\nData flattened and saved to {args.output_file}")
print(f"Total rows: {len(df)}")
