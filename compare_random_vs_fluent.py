import pandas as pd
import argparse
from pathlib import Path

def compare_random_vs_fluent(csv_file):
    """
    Compare Random and Fluent versions of each algorithm.
    Calculates the average score difference for each algorithm pair.
    """
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Convert score and time to numeric
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df['time'] = pd.to_numeric(df['time'], errors='coerce')

    # Get unique algorithms
    algorithms = df['algorithm'].unique()

    # Extract base algorithm names (e.g., "annealing" from "annealingFromRandom")
    algorithm_pairs = {}
    for algo in algorithms:
        if 'FromRandom' in algo:
            base_name = algo.replace('FromRandom', '')
            if base_name not in algorithm_pairs:
                algorithm_pairs[base_name] = {}
            algorithm_pairs[base_name]['random'] = algo
        elif 'FromFluent' in algo:
            base_name = algo.replace('FromFluent', '')
            if base_name not in algorithm_pairs:
                algorithm_pairs[base_name] = {}
            algorithm_pairs[base_name]['fluent'] = algo

    # Calculate differences
    results = []

    for base_name, versions in algorithm_pairs.items():
        if 'random' not in versions or 'fluent' not in versions:
            print(f"Skipping {base_name}: missing Random or Fluent version")
            continue

        random_algo = versions['random']
        fluent_algo = versions['fluent']

        # Get data for both versions
        random_data = df[df['algorithm'] == random_algo]['score']
        fluent_data = df[df['algorithm'] == fluent_algo]['score']

        # Calculate statistics
        random_avg = random_data.mean()
        fluent_avg = fluent_data.mean()
        difference = random_avg - fluent_avg
        percent_diff = (difference / fluent_avg * 100) if fluent_avg != 0 else 0
        # Calculate percent Fluent is better/worse than Random (based on Random as baseline)
        percent_fluent_better = ((fluent_avg - random_avg) / random_avg * 100) if random_avg != 0 else 0
        
        # Calculate percentage of times Fluent performs better than Random
        if len(random_data) == len(fluent_data):
            fluent_better_count = (fluent_data.values > random_data.values).sum()
            percent_times_better = (fluent_better_count / len(fluent_data) * 100) if len(fluent_data) > 0 else 0
        else:
            percent_times_better = None

        results.append({
            'algorithm': base_name,
            'random_avg_score': random_avg,
            'fluent_avg_score': fluent_avg,
            'difference': difference,
            'percent_difference': percent_diff,
            'percent_fluent_vs_random': percent_fluent_better,
            'percent_times_fluent_better': percent_times_better,
            'random_samples': len(random_data),
            'fluent_samples': len(fluent_data)
        })

    # Create results dataframe
    results_df = pd.DataFrame(results)

    # Sort by difference
    results_df = results_df.sort_values('difference', ascending=False)

    # Print results
    print("\n" + "="*140)
    print("RANDOM vs FLUENT COMPARISON")
    print("="*140)
    print(f"\n{'Algorithm':<20} {'Random Avg':<15} {'Fluent Avg':<15} {'Difference':<15} {'Fluent Better %':<18} {'% Times Better':<16}")
    print("-"*140)

    for _, row in results_df.iterrows():
        times_better_str = f"{row['percent_times_fluent_better']:.2f}%" if row['percent_times_fluent_better'] is not None else "N/A"
        print(f"{row['algorithm']:<20} {row['random_avg_score']:<15.2f} {row['fluent_avg_score']:<15.2f} {row['difference']:<15.2f} {row['percent_fluent_vs_random']:<18.2f}% {times_better_str:<16}")

    # Add totals row
    total_row = {
        'random_avg_score': results_df['random_avg_score'].mean(),
        'fluent_avg_score': results_df['fluent_avg_score'].mean(),
        'difference': results_df['difference'].mean(),
        'percent_fluent_vs_random': results_df['percent_fluent_vs_random'].mean(),
        'percent_times_fluent_better': results_df['percent_times_fluent_better'].mean()
    }
    
    print("-"*140)
    times_better_str = f"{total_row['percent_times_fluent_better']:.2f}%" if total_row['percent_times_fluent_better'] is not None else "N/A"
    print(f"{'TOTAL/AVERAGE':<20} {total_row['random_avg_score']:<15.2f} {total_row['fluent_avg_score']:<15.2f} {total_row['difference']:<15.2f} {total_row['percent_fluent_vs_random']:<18.2f}% {times_better_str:<16}")
    print("="*140)
    
    print(f"\nNote: 'Fluent Better %' shows how much Fluent differs from Random (baseline 100%)")
    print(f"      Positive % = Fluent is BETTER (higher scores)")
    print(f"      Negative % = Fluent is WORSE (lower scores)")
    print(f"      '% Times Better' shows in what percentage of individual runs Fluent scored higher than Random")
    print(f"      'Difference' column: Positive = Random has higher scores (better), Negative = Fluent has higher scores (better)")
    print("\n")

    return results_df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare Random vs Fluent versions of algorithms')
    parser.add_argument('csv_file', help='Path to the flattened CSV file')
    parser.add_argument('--output', help='Optional: save results to CSV file')
    args = parser.parse_args()

    results_df = compare_random_vs_fluent(args.csv_file)

    if args.output:
        results_df.to_csv(args.output, index=False)
        print(f"Results saved to {args.output}")





