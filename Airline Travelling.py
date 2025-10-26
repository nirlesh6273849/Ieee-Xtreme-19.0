import sys

def solve():
    """
    Uses dynamic programming to solve the Airline Traveling problem.
    """
    # Use fast I/O
    input = sys.stdin.readline
    output = sys.stdout.write

    try:
        n_str, k_str = input().split()
        n, k = int(n_str), int(k_str)
    except (IOError, ValueError):
        return

    # city_costs[0] is unused
    city_costs = [0] * n
    distinct_costs = set()
    
    costs_line = input().split()
    for i in range(1, n):
        city_costs[i] = int(costs_line[i - 1])
        distinct_costs.add(city_costs[i])

    # --- DP Preprocessing ---
    
    # reachable_round_trip_cost[x] is true if cost x is possible
    # using only round trips (0 -> i -> 0)
    reachable_round_trip_cost = [False] * (k + 1)
    # Base case: cost 0 is possible (no flights)
    reachable_round_trip_cost[0] = True
    
    # Unbounded knapsack-style DP
    for cost in distinct_costs:
        round_trip_cost = 2 * cost
        
        # Only consider valid, useful costs
        if round_trip_cost > 0 and round_trip_cost <= k:
            for x in range(round_trip_cost, k + 1):
                if reachable_round_trip_cost[x - round_trip_cost]:
                    reachable_round_trip_cost[x] = True

    # --- Answer Queries ---
    try:
        q = int(input())
    except (IOError, ValueError):
        return
        
    query_answers = []
    for _ in range(q):
        a_str, b_str = input().split()
        a, b = int(a_str), int(b_str)
        
        is_possible = False
        
        if a == 0 and b == 0:
            # Case 1: 0 -> 0. Must be a sum of round trips.
            is_possible = reachable_round_trip_cost[k]
            
        elif a == 0 and b != 0:
            # Case 2: 0 -> b. Path: (Round trips) + (0 -> b)
            cost_b = city_costs[b]
            if k >= cost_b:
                is_possible = reachable_round_trip_cost[k - cost_b]
                
        elif a != 0 and b == 0:
            # Case 3: a -> 0. Path: (a -> 0) + (Round trips)
            cost_a = city_costs[a]
            if k >= cost_a:
                is_possible = reachable_round_trip_cost[k - cost_a]
                
        else:
            # Case 4: a -> b. Path: (a -> 0) + (Round trips) + (0 -> b)
            cost_a = city_costs[a]
            cost_b = city_costs[b]
            required_legs_cost = cost_a + cost_b
            if k >= required_legs_cost:
                is_possible = reachable_round_trip_cost[k - required_legs_cost]

        query_answers.append("Yes" if is_possible else "No")

    output("\n".join(query_answers) + "\n")

if __name__ == "__main__":
    solve()