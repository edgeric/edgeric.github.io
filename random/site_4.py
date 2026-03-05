from itertools import permutations
import math
import time

def optimal_allocate_rbs(total_rbs, sites_info):
    # Extract site information and prepare for allocation
    site_keys = list(sites_info.keys())
    weights = [sites_info[key]['weight'] for key in site_keys]
    total_weights = sum(weights)
    adjusted_rbs = [round((weight / total_weights) * total_rbs) for weight in weights]

    # Adjust the total RBs to match exactly the total_rbs if there's any rounding issue
    while sum(adjusted_rbs) != total_rbs:
        if sum(adjusted_rbs) > total_rbs:
            adjusted_rbs[adjusted_rbs.index(max(adjusted_rbs))] -= 1
        else:
            adjusted_rbs[adjusted_rbs.index(min(adjusted_rbs))] += 1

    # Store the calculated RBs in the sites_info for easy access
    for key, rbs in zip(site_keys, adjusted_rbs):
        sites_info[key]['rbs'] = rbs

    allocations = list(permutations(site_keys))
    min_affected = float('inf')
    best_allocation = None

    # Evaluate each combination
    for allocation in allocations:
        alloc_ranges = get_rb_ranges(allocation, sites_info)
        affected = calculate_affected_prbs(alloc_ranges, sites_info)
        if affected < min_affected:
            min_affected = affected
            best_allocation = {key: sites_info[key]['alloc_range'] for key in allocation}

    return best_allocation

def get_rb_ranges(allocation, sites_info):
    # Generate RB ranges for the given allocation and store them in sites_info
    start = 0
    for site_key in allocation:
        rb = sites_info[site_key]['rbs']
        end = start + rb
        sites_info[site_key]['alloc_range'] = (start, end - 1)
        start = end
    return sites_info

def calculate_affected_prbs(sites_info_with_ranges, sites_info):
    # Calculate total affected PRBs based on allocation ranges and bad RB indices
    total_affected = 0
    for site_key, info in sites_info_with_ranges.items():
        start, end = info['alloc_range']
        bad_rbs = info['bad_rbs']
        affected = len([rb for rb in range(start, end + 1) if rb in bad_rbs])
        total_affected += affected
    return total_affected

# Example usage
sites_info = {
    1: {'weight': 0.7, 'bad_rbs': [1, 2]},
    2: {'weight': 0.1, 'bad_rbs': [3, 4, 5]}
    #3: {'weight': 0.2, 'bad_rbs': [6, 7, 8, 9]}
}
total_rbs = 10
time_start = time.time()
best_allocation = optimal_allocate_rbs(total_rbs, sites_info)
time_end = time.time() - time_start
print("Best Allocation:", best_allocation)
print("time taken: ", time_end*1000000)
