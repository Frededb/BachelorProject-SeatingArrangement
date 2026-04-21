import json
from pathlib import Path
import generateData
import analyzeData

def calc_dist_error(real_dist, sim_dist):
    keys = set(real_dist.keys()).union(set(sim_dist.keys()))
    err = 0.0
    for k in keys:
        v1 = real_dist.get(str(k), real_dist.get(k, 0.0))
        v2 = sim_dist.get(str(k), sim_dist.get(k, 0.0))
        err += abs(v1 - v2)
    # Total variation distance is half of the sum of abs differences
    return err / 2.0

def main():
    real_path = Path("Inputs/realData/inputReal.json")
    if not real_path.exists():
        print(f"Cannot find {real_path}")
        return
        
    real_res = analyzeData.run_all_analyses_from_file(real_path)
    real_cond = real_res["conditional_probabilities"]
    real_dists = {
        "out_pref": real_res["outgoing_distributions"]["prefers_distribution"]["percentages"],
        "out_avoid": real_res["outgoing_distributions"]["avoids_distribution"]["percentages"],
        "in_pref": real_res["incoming_distributions"]["preferred_by_x_people_distribution"]["percentages"],
        "in_avoid": real_res["incoming_distributions"]["avoided_by_x_people_distribution"]["percentages"]
    }
    
    print(f"{'Cohesion':<9}| {'Cond. Probs Error (Avg/Max)':<28} | {'Out-Pref Err':<12} | {'Out-Avoid Err':<13} | {'In-Pref Err':<11} | {'In-Avoid Err':<12}")
    print("-" * 105)
    
    for cohesion in range(0, 101, 10):
        # Generate data for 100 people using seed for reproducibility
        people_raw = generateData.generateData(100, cohesion, seed=42+cohesion)
        # Transform generated people to match what analyzeData expects
        mapped_people = []
        for p in people_raw:
            mapped_people.append({
                "name": p["id"],
                "preferences": p["attributes"][2],
                "avoidances": p["attributes"][3]
            })
            
        people_links = analyzeData.load_people_from_data(mapped_people)
        sim_res = analyzeData.run_all_analyses(people_links)
        
        sim_cond = sim_res["conditional_probabilities"]
        sim_dists = {
            "out_pref": sim_res["outgoing_distributions"]["prefers_distribution"]["percentages"],
            "out_avoid": sim_res["outgoing_distributions"]["avoids_distribution"]["percentages"],
            "in_pref": sim_res["incoming_distributions"]["preferred_by_x_people_distribution"]["percentages"],
            "in_avoid": sim_res["incoming_distributions"]["avoided_by_x_people_distribution"]["percentages"]
        }
        
        cond_errs = []
        for k, v in real_cond.items():
            r_pct = v.get("percentage") or 0.0
            s_pct = sim_cond[k].get("percentage") or 0.0
            cond_errs.append(abs(r_pct - s_pct))
            
        avg_cond = sum(cond_errs)/len(cond_errs)
        max_cond = max(cond_errs)
        
        o_p_err = calc_dist_error(real_dists["out_pref"], sim_dists["out_pref"])
        o_a_err = calc_dist_error(real_dists["out_avoid"], sim_dists["out_avoid"])
        i_p_err = calc_dist_error(real_dists["in_pref"], sim_dists["in_pref"])
        i_a_err = calc_dist_error(real_dists["in_avoid"], sim_dists["in_avoid"])
        
        cond_str = f"{avg_cond:.1f}% avg, {max_cond:.1f}% max"
        print(f"{cohesion:<9}| {cond_str:<28} | {o_p_err:<11.1f}% | {o_a_err:<12.1f}% | {i_p_err:<10.1f}% | {i_a_err:<11.1f}%")

if __name__ == '__main__':
    main()