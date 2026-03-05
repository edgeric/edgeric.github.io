from itertools import permutations
import math
import time

def optimal_allocate_rbs(total_rbs, sites_info):
    # Generate all valid combinations of RB allocations
    weights = [site['weight'] for site in sites_info]
    scaled_weights = [weight * total_rbs for weight in weights]
    allocations = generate_all_combinations(scaled_weights, total_rbs)
    
    min_affected = float('inf')
    best_allocation = None

    # Evaluate each combination
    for allocation in allocations:
        affected = calculate_affected_prbs(allocation, sites_info)
        if affected < min_affected:
            min_affected = affected
            best_allocation = allocation
    
    return best_allocation

def generate_all_combinations(scaled_weights, total_rbs):
    # Generate all permutations of scaled weights
    basic_allocations = [math.floor(weight) for weight in scaled_weights]
    remainder = total_rbs - sum(basic_allocations)
    # Handling the remainder by distributing one extra RB to the sites with the highest decimal residuals
    residuals = sorted([(index, weight % 1) for index, weight in enumerate(scaled_weights)], key=lambda x: x[1], reverse=True)
    for i in range(remainder):
        basic_allocations[residuals[i][0]] += 1
    
    return list(permutations(basic_allocations))

def calculate_affected_prbs(allocation, sites_info):
    # Calculate total affected PRBs based on current allocation and bad RB indices
    total_affected = 0
    for alloc, site in zip(allocation, sites_info):
        bad_rbs = site['bad_rbs']
        affected = len([rb for rb in range(alloc) if rb in bad_rbs])
        total_affected += affected
    
    return total_affected

# Example usage
sites_info = [
    {'weight': 0.2, 'bad_rbs': [1, 2]},
    {'weight': 0.4, 'bad_rbs': [3, 4, 5]},
    {'weight': 0.5, 'bad_rbs': [6, 7, 8, 9]}
]
total_rbs = 10
time_start = time.time()
best_allocation = optimal_allocate_rbs(total_rbs, sites_info)
time_end = time.time() 
time_exec = time_end - time_start
print("Best Allocation:", best_allocation)
print("time taken: ", time_exec*1000000)
