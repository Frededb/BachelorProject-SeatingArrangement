import json
import random

def generate_data(people_count, wish_count_dist, avoidance_count_dist, wishback_chance, double_wish_chance, output_file="generated_data.json"):
    """
    Generate randomized student preference data.
    
    :param people_count: Total number of people to generate.
    :param wish_count_dist: Dictionary mapping number of wishes to their probability (e.g., {0: 0.1, 1: 0.3, 2: 0.6}).
    :param avoidance_count_dist: Dictionary mapping number of avoidances to their probability.
    :param wishback_chance: Probability that if A wishes for B, B will also wish for A.
    :param double_wish_chance: Probability that if A wishes for B, and B wishes for C, A will also wish for C.
    :param output_file: Output path for the JSON file.
    """
    people = []
    names = [f"P{i}" for i in range(1, people_count + 1)]
    
    # Initialize basic info
    for name in names:
        people.append({
            "name": name,
            "studyprogram": random.choices(["cs", "swu"], weights=[0.037, 0.963], k=1)[0],
            "year": random.choices(["2021", "2022", "2023", "2025"], weights=[0.0185, 0.0185, 0.8148, 0.1481], k=1)[0],
            "preferences": [],
            "avoidances": []
        })
        
    def get_count(dist):
        counts = list(dist.keys())
        probs = list(dist.values())
        return random.choices(counts, weights=probs, k=1)[0]
        
    preferences = {name: set() for name in names}
    avoidances = {name: set() for name in names}
    
    # Pre-calculate target out-degrees based on distributions
    target_wish_counts = {name: get_count(wish_count_dist) for name in names}
    target_avoid_counts = {name: get_count(avoidance_count_dist) for name in names}

    # Group people into clusters to mimic real-life friend groups
    group_count = max(1, people_count // 5) # average group size of 5
    groups = {name: random.randint(1, group_count) for name in names}
    popularities = {name: random.paretovariate(3) for name in names}

    def get_affinity(a, b, is_avoidance=False):
        if is_avoidance:
            return 1.0 
            
        # Massive affinity for same-group members to create cliques
        same_group = (groups[a] == groups[b])
        base_weight = 1000.0 if same_group else 1.0
        
        # Boost if already reciprocal 
        if a in preferences[b]:
            base_weight *= (1.0 + wishback_chance * 10)
            
        return base_weight * popularities[b]

    # Helper function to pick a target using weighted probabilities
    def pick_target(chooser, available_targets, is_avoidance=False):
        weights = [get_affinity(chooser, t, is_avoidance) for t in available_targets]
        return random.choices(available_targets, weights=weights, k=1)[0]

    # Generate preferences
    for name in names:
        count = target_wish_counts[name]
        available_targets = [n for n in names if n != name]
        
        while len(preferences[name]) < count and available_targets:
            target = pick_target(name, available_targets, is_avoidance=False)
            preferences[name].add(target)
            available_targets.remove(target)

    # Generate avoidances (no complex triadic closure needed, keep simple)
    for name in names:
        count = target_avoid_counts[name]
        available_targets = [n for n in names if n != name and n not in preferences[name]]
        
        while len(avoidances[name]) < count and available_targets:
            target = pick_target(name, available_targets, is_avoidance=True)
            avoidances[name].add(target)
            available_targets.remove(target)

    # Convert sets to lists and format output
    for person in people:
        person["preferences"] = list(preferences[person["name"]])
        person["avoidances"] = list(avoidances[person["name"]])

    with open(output_file, 'w') as f:
        json.dump(people, f, indent=4)
        
    return people

if __name__ == "__main__":
    # Example usage
    wish_dist = {
        0: 0.0926, 1: 0.2037, 2: 0.0556, 3: 0.1667, 4: 0.1111, 
        5: 0.2222, 6: 0.0185, 7: 0.0556, 8: 0.0185, 9: 0.0370, 10: 0.0185
    }
    avoid_dist = {
        0: 0.8148, 1: 0.1667, 3: 0.0185
    }
    
    generate_data(
        people_count=54,
        wish_count_dist=wish_dist,
        avoidance_count_dist=avoid_dist,
        wishback_chance=0.6073,
        double_wish_chance=0.5071,
        output_file="generated100.json"
    )
