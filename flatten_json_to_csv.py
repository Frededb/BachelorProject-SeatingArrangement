import json
import pandas as pd

# Load the JSON data
with open('Data/ExperimentsData.json', 'r') as f:
    data = json.load(f)

# Initialize a list to hold the flattened rows
rows = []

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

# Create a DataFrame
df = pd.DataFrame(rows)

# Save to CSV in Data folder
df.to_csv('Data/flattened_experiments_data.csv', index=False)

print("Data flattened and saved to Data/flattened_experiments_data.csv")
