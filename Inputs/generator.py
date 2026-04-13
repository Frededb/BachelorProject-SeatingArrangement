import json
import random

def generate_data(people_count, wish_count_dist, avoidance_count_dist, wishback_chance, group_cohesion=80, output_file="generated_data.json"):
    """
    Generate randomized student preference data.
    
    :param people_count: Total number of people to generate.
    :param wish_count_dist: Dictionary mapping number of wishes to their probability (e.g., {0: 0.1, 1: 0.3, 2: 0.6}).
    :param avoidance_count_dist: Dictionary mapping number of avoidances to their probability.
    :param wishback_chance: Probability that if A wishes for B, B will also wish for A.
    :param group_cohesion: Value from 0-100. 0 = one random unstructured blob, 100 = completely isolated small groups, 80 = small groups with a few clear bridges.
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

    # Group people into small communities (Explicit Stochastic Block Model)
    names_shuffled = list(names)
    random.shuffle(names_shuffled)
    
    groups = {}
    current_group = 1
    idx = 0
    while idx < people_count:
        # Community sizes roughly between 4 and 8 people
        size = random.randint(4, min(8, max(4, people_count - idx)))
        if people_count - idx <= 8:
            size = people_count - idx
            
        for _ in range(size):
            groups[names_shuffled[idx]] = current_group
            idx += 1
        current_group += 1

    popularities = {name: random.paretovariate(3) for name in names}
    
    # Base calculations for scaling smoothly: 
    # Use exponential scaling across the 0-100 spectrum because probabilities are experienced logarithmically.
    cohesion_factor = max(0, min(100, group_cohesion)) / 100.0
    p = cohesion_factor
    
    # At 0: intra = 1.0. At 100: intra = 10,000.0
    intra_weight = 10.0 ** (4.0 * p)
    
    # At 0: dist = 1.0. At 100: dist = 0.0001
    dist_weight = 10.0 ** (-4.0 * p)
    
    # Adjacent peaks slightly in the middle (at 50) to create bridges, then scales down to 1.0 at extremes.
    # At p=0.5: 10^(0.5 * 3 * 0.5) = 10^0.75 ≈ 5.62
    adj_weight = 10.0 ** (p * 3.0 * (1.0 - p))

    # To ensure massive populations don't mathematically drown out the cliques (since 10,000 distant people * 0.001 weight = 10.0 > 1 inner group),
    # we precalculate the size of the tiers relative to each group to distribute the probability mass evenly
    from collections import Counter
    group_sizes = Counter(groups.values())
    tier_counts = {}
    
    for g in range(1, current_group):
        intra_count = group_sizes[g] - 1
        adj_count = 0
        for other_g, size in group_sizes.items():
            if other_g != g and (abs(g - other_g) == 1 or abs(g - other_g) == current_group - 2):
                adj_count += size
        dist_count = people_count - 1 - intra_count - adj_count
        tier_counts[g] = (max(1, intra_count), max(1, adj_count), max(1, dist_count))

    def get_affinity(a, b, is_avoidance=False):
        if is_avoidance:
            return 1.0 
            
        group_a = groups[a]
        group_b = groups[b]
        intra_c, adj_c, dist_c = tier_counts[group_a]
        
        # Stochastic Block Model tier mass scaled by the size of the tier
        if group_a == group_b:
            base_weight = intra_weight / intra_c
        elif abs(group_a - group_b) == 1 or abs(group_a - group_b) == current_group - 2:
            base_weight = adj_weight / adj_c
        else:
            base_weight = dist_weight / dist_c
        
        # Boost if already reciprocal 
        if a in preferences[b]:
            base_weight *= (1.0 + wishback_chance * 20)
            
        return base_weight * popularities[b]

    # Helper function to pick a target using weighted probabilities
    def pick_target(chooser, available_targets, is_avoidance=False):
        weights = [get_affinity(chooser, t, is_avoidance) for t in available_targets]
        
        # If all weights effectively round down to 0, fallback to pure structural random so they at least meet their input distributions safely
        if sum(weights) <= 0.0001:
            return random.choice(available_targets)
            
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
        # Allow people in tiny isolated groups to just use 0 if they don't have valid targets inside to avoid hanging loops
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
        people_count=100,
        wish_count_dist=wish_dist,
        avoidance_count_dist=avoid_dist,
        wishback_chance=0.6073,
        group_cohesion=30, # Try 0 (blob) through 100 (isolated islands)
        output_file="generated100.json"
    )
