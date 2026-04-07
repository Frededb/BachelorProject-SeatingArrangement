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
            "studyprogram": random.choice(["SWU", "ds", "CS", "Math"]),
            "year": random.choice(["2022", "2023", "2024"]),
            "preferences": [],
            "avoidances": []
        })
        
    def get_count(dist):
        counts = list(dist.keys())
        probs = list(dist.values())
        return random.choices(counts, weights=probs, k=1)[0]
        
    preferences = {name: set() for name in names}
    avoidances = {name: set() for name in names}
    
    # 1. Generate base wishes based on wish_count_dist
    for name in names:
        target_wish_count = get_count(wish_count_dist)
        available_targets = [n for n in names if n != name and n not in preferences[name]]
        
        while len(preferences[name]) < target_wish_count and available_targets:
            target = random.choice(available_targets)
            preferences[name].add(target)
            available_targets.remove(target)
            
            # Apply wishback chance
            if random.random() < wishback_chance:
                # Target wishes back for 'name'
                target_wish_count_for_target = get_count(wish_count_dist) 
                # Give target at least one wish if they didn't have one, or just add it anyway
                preferences[target].add(name)
                
    # 2. Apply double wish chance (Triadic closure: A -> B, B -> C  => A -> C)
    for name in names:
        friends = list(preferences[name])
        for friend in friends:
            friends_of_friend = list(preferences[friend])
            for fof in friends_of_friend:
                if fof != name and fof not in preferences[name]:
                    if random.random() < double_wish_chance:
                        preferences[name].add(fof)

    # 3. Generate avoidances based on avoidance_count_dist
    for name in names:
        target_avoid_count = get_count(avoidance_count_dist)
        # Cannot avoid self and cannot avoid someone already preferred
        available_targets = [n for n in names if n != name and n not in preferences[name] and n not in avoidances[name]]
        
        while len(avoidances[name]) < target_avoid_count and available_targets:
            target = random.choice(available_targets)
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
    wish_dist = {0: 0.1, 1: 0.3, 2: 0.4, 3: 0.2}
    avoid_dist = {0: 0.6, 1: 0.3, 2: 0.1}
    
    generate_data(
        people_count=100,
        wish_count_dist=wish_dist,
        avoidance_count_dist=avoid_dist,
        wishback_chance=0.4,
        double_wish_chance=0.2,
        output_file="Inputs/generated100.json"
    )
