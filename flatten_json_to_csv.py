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
            for first_key, first_val in algo_data.items():
                # Detect the structure: check if first_key is a number (n_people) or float string (cohesion)
                try:
                    # Try to parse as float to detect cohesion structure
                    cohesion_test = float(first_key)
                    is_cohesion_first = True
                except ValueError:
                    is_cohesion_first = False
                
                if is_cohesion_first:
                    # Structure: results[algorithm][n_people][cohesion][iteration_id] or results[algorithm][n_people][cohesion] with scores/times
                    # NOTE: The first level keys that look like floats are actually n_people, and the nested keys are cohesion
                    for n_people_str, pc_data in algo_data.items():
                        n_people = int(float(n_people_str))  # Parse as float then convert to int
                        for cohesion_str, cohesion_data in pc_data.items():
                            cohesion = int(cohesion_str)
                            # Check if cohesion_data has 'scores' and 'times' keys (old format)
                            if isinstance(cohesion_data, dict) and 'scores' in cohesion_data:
                                for iteration, score in enumerate(cohesion_data['scores']):
                                    time_val = cohesion_data['times'][iteration]
                                    rows.append({
                                        'algorithm': algorithm,
                                        'n_people': n_people,
                                        'cohesion': cohesion,
                                        'iteration': iteration,
                                        'score': score,
                                        'time': time_val
                                    })
                            else:
                                # Structure with iteration_id keys
                                for iteration_id, iter_data in cohesion_data.items():
                                    if isinstance(iter_data, dict) and 'scores' in iter_data:
                                        for idx, score in enumerate(iter_data['scores']):
                                            time_val = iter_data['times'][idx]
                                            rows.append({
                                                'algorithm': algorithm,
                                                'n_people': n_people,
                                                'cohesion': cohesion,
                                                'iteration': idx,
                                                'iteration_id': int(iteration_id),
                                                'score': score,
                                                'time': time_val
                                            })
                else:
                    # Structure: results[algorithm][cohesion_str][n_people_str]
                    # NOTE: In this case, first level keys that don't parse as float are cohesion
                    for cohesion_str, cs_data in algo_data.items():
                        cohesion = int(cohesion_str)
                        for n_people_str, pc_data in cs_data.items():
                            n_people = int(n_people_str)
                            # Check if pc_data has 'scores' and 'times' keys
                            if isinstance(pc_data, dict) and 'scores' in pc_data:
                                for iteration, score in enumerate(pc_data['scores']):
                                    time_val = pc_data['times'][iteration]
                                    rows.append({
                                        'algorithm': algorithm,
                                        'n_people': n_people,
                                        'cohesion': cohesion,
                                        'iteration': iteration,
                                        'score': score,
                                        'time': time_val
                                    })
                            else:
                                # Structure with iteration_id keys
                                for iteration_id, iter_data in pc_data.items():
                                    if isinstance(iter_data, dict) and 'scores' in iter_data:
                                        for idx, score in enumerate(iter_data['scores']):
                                            time_val = iter_data['times'][idx]
                                            rows.append({
                                                'algorithm': algorithm,
                                                'n_people': n_people,
                                                'cohesion': cohesion,
                                                'iteration': idx,
                                                'iteration_id': int(iteration_id),
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
