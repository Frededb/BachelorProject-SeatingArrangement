import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
df = pd.read_csv('flattened_fullrun_data.csv')

# Convert score to numeric, handling any DNF or error values
df['score'] = pd.to_numeric(df['score'], errors='coerce')

# Remove rows with NaN scores
df = df.dropna(subset=['score'])

# Define population sizes to analyze
population_sizes = [8, 30, 100, 300]

# Function to process and generate outputs for a specific population size
def process_population(df, n_people):
    # Filter data for this population size
    df_filtered = df[df['n_people'] == n_people]
    
    if df_filtered.empty:
        print(f"No data found for {n_people} people")
        return
    
    # Average scores for each algorithm per dataset (cohesion, iteration)
    df_avg = df_filtered.groupby(['algorithm', 'cohesion', 'iteration'])['score'].mean().reset_index()
    
    # Dictionary to count how many times each algorithm is the best
    best_counts = {}
    tie_count = 0  # Count how many groups have ties
    total_groups = 0  # Total number of (cohesion, iteration) groups

    # Group by dataset (cohesion, iteration) and find the best algorithm(s) for each
    for (cohesion, iteration), group in df_avg.groupby(['cohesion', 'iteration']):
        if len(group) > 0:
            max_score = group['score'].max()
            best_algos = group[group['score'] == max_score]['algorithm'].tolist()
            for best_algo in best_algos:
                best_counts[best_algo] = best_counts.get(best_algo, 0) + 1
            if len(best_algos) > 1:
                tie_count += 1
            total_groups += 1
    
    # Create a DataFrame for the table
    best_df = pd.DataFrame(list(best_counts.items()), columns=['Algorithm', 'Best Count'])
    best_df = best_df.sort_values(by='Best Count', ascending=False)
    
    # Print the data table
    num_datasets = sum(best_counts.values())
    print(f"\n{'='*70}")
    print(f"Data Table for {n_people} people: Number of times each algorithm is the best")
    print(f"Total datasets (including ties): {num_datasets}")
    print(f"Number of (cohesion, iteration) groups: {total_groups}")
    print(f"Number of ties: {tie_count} ({(tie_count/total_groups*100):.1f}% of groups)")
    print(f"{'='*70}")
    print(best_df.to_string(index=False))
    
    # Save the table to CSV
    csv_filename = f'best_algorithm_table_{n_people}p.csv'
    best_df.to_csv(csv_filename, index=False)
    print(f"Table saved to: {csv_filename}")
    
    # Create the pie chart
    plt.figure(figsize=(14, 10))
    
    # Create labels with algorithm names for outside
    algo_names = list(best_counts.keys())
    
    # Create custom autopct function to show only percentage
    def make_autopct(values):
        def my_autopct(pct):
            return f'{pct:.1f}%'
        return my_autopct
    
    # Create the pie chart with percentage labels only
    wedges, texts, autotexts = plt.pie(
        best_counts.values(), 
        labels=algo_names, 
        autopct=make_autopct(best_counts.values()), 
        startangle=90, 
        textprops={'fontsize': 12},
        pctdistance=0.80
    )
    
    # Style the algorithm name labels
    for text in texts:
        text.set_fontsize(11)
        text.set_weight('normal')
        text.set_color('black')
    
    # Style the percentage labels
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')
        autotext.set_fontsize(12)
    
    plt.title(f'Proportion of Datasets Where Each Algorithm is the Best ({n_people} people)', fontsize=14, pad=20, weight='bold')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # Save the pie chart
    chart_filename = f'plots/best_algorithm_piechart_{n_people}p.png'
    plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
    print(f"Pie chart saved to: {chart_filename}")
    
    plt.close()

# Process all population sizes
for pop_size in population_sizes:
    process_population(df, pop_size)
