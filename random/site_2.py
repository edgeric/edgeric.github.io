def allocate_rbs(total_rbs, sites_info):
    """
    Allocate RBs to sites based on weight, attempting to minimize bad RBs, ensuring continuous segments,
    with sites sorted by demand from highest to lowest.

    :param total_rbs: Total number of RBs available.
    :param sites_info: List of dicts, each containing 'weight' and 'bad_rbs' (indices of bad RBs).
    :return: Allocation map where key is site index and value is list of allocated RBs.
    """
    # Calculate total weight and sort sites by demand (high to low)
    total_weight = sum(site['weight'] for site in sites_info)
    sites_info_sorted = sorted(sites_info, key=lambda site: site['weight'], reverse=True)
    
    available_rbs = set(range(total_rbs))
    allocations = {}

    for i, site in enumerate(sites_info_sorted):
        required_rbs = round(site['weight'] / total_weight * total_rbs)
        
        best_segment = None
        min_bad_rbs = float('inf')

        for start in range(total_rbs - required_rbs + 1):
            segment = set(range(start, start + required_rbs))
            if segment.issubset(available_rbs):
                bad_rbs_count = len(segment.intersection(site['bad_rbs']))
                if bad_rbs_count < min_bad_rbs:
                    min_bad_rbs = bad_rbs_count
                    best_segment = segment
                    if bad_rbs_count == 0:  # optimal segment found, no need to search further
                        break

        if best_segment is not None:
            allocations[i] = list(best_segment)
            available_rbs.difference_update(best_segment)
        else:
            # Fallback: allow allocation with bad RBs if necessary
            for start in range(total_rbs - required_rbs + 1):
                segment = set(range(start, start + required_rbs))
                if segment.issubset(available_rbs):  # Less ideal segment but necessary
                    allocations[i] = list(segment)
                    available_rbs.difference_update(segment)
                    break

    # Mapping back to original site indices (if needed)
    original_index_allocations = {sites_info.index(site): alloc for site, alloc in zip(sites_info_sorted, allocations.values())}
    return original_index_allocations

# Example usage
sites_info = [
    {'weight': 5, 'bad_rbs': [1, 2, 3]},
    {'weight': 3, 'bad_rbs': [4, 5, 6]},
    {'weight': 2, 'bad_rbs': [10, 11, 12]}
]

allocations = allocate_rbs(25, sites_info)
for site, rbs in allocations.items():
    print(f"Site {site} allocated RBs: {rbs}")
