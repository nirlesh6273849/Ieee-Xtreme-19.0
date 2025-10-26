import sys
import heapq

# Set higher recursion depth for DSU
sys.setrecursionlimit(400000)

class DisjointSetUnion:
    """Standard DSU implementation with path compression and union-by-size."""
    def __init__(self, n):
        self.parents = list(range(n))
        self.sizes = [1] * n

    def get_root(self, i):
        """Find the root of i with path compression."""
        if self.parents[i] == i:
            return i
        self.parents[i] = self.get_root(self.parents[i])
        return self.parents[i]

    def merge_sets(self, i, j):
        """Merge the sets containing i and j. Return True if merged."""
        root_i = self.get_root(i)
        root_j = self.get_root(j)
        
        if root_i != root_j:
            # Union by size
            if self.sizes[root_i] < self.sizes[root_j]:
                root_i, root_j = root_j, root_i
            self.parents[root_j] = root_i
            self.sizes[root_i] += self.sizes[root_j]
            return True
        return False

def find_shortest_time(start_node, end_node, num_nodes, graph):
    """
    Standard Dijkstra's algorithm to find shortest time.
    """
    min_times = [float('inf')] * (num_nodes + 1)
    min_times[start_node] = 0
    # Priority queue stores (time, node)
    priority_queue = [(0, start_node)]

    while priority_queue:
        time, u = heapq.heappop(priority_queue)

        if time > min_times[u]:
            continue
        
        if u == end_node:
            # Found the shortest path to the end
            return min_times[end_node]

        for v, w in graph[u]:
            if min_times[u] + w < min_times[v]:
                min_times[v] = min_times[u] + w
                heapq.heappush(priority_queue, (min_times[v], v))
    
    return min_times[end_node]

def run_test_case():
    """
    Solves a single test case for the Stable Power Network.
    """
    input = sys.stdin.readline
    
    try:
        N, M = map(int, input().split())
        all_edges = []
        for _ in range(M):
            # u, v, time, risk
            all_edges.append(list(map(int, input().split())))
    except (IOError, ValueError):
        return

    # 1. Sort all edges by risk
    all_edges.sort(key=lambda edge: edge[3])

    dsu = DisjointSetUnion(N + 1)
    bottleneck_risk = -1

    # 2. Find the minimum bottleneck risk using a Kruskal-like approach
    for u, v, time, risk in all_edges:
        dsu.merge_sets(u, v)
        # As soon as 1 and N are connected, the current edge's
        # risk is the minimum maximum risk for *some* path.
        if dsu.get_root(1) == dsu.get_root(N):
            bottleneck_risk = risk
            break

    # 3. Handle the case where 1 and N are never connected
    if bottleneck_risk == -1:
        print("-1")
        return

    # 4. Build the time-based graph
    # Include only edges with risk <= our bottleneck_risk
    time_graph = [[] for _ in range(N + 1)]
    for u, v, time, risk in all_edges:
        if risk <= bottleneck_risk:
            time_graph[u].append((v, time))
            time_graph[v].append((u, time))
            
    # 5. Run Dijkstra on the time_graph to find the shortest time
    final_time = find_shortest_time(1, N, N, time_graph)
    
    print(f"{bottleneck_risk} {final_time}")

# --- Main execution ---
try:
    T = int(sys.stdin.readline())
except (IOError, ValueError):
    T = 0
    
for _ in range(T):
    run_test_case()