#include <iostream>
#include <vector>
#include <queue>
#include <algorithm> // For min, swap
#include <cmath> // For log2

using namespace std;

// Constraints
const int kMaxNodes = 1000005;
const int kMaxLogN = 21; // ~log2(kMaxNodes) + 1
const int kInfinity = 1e9;

int g_num_nodes, g_num_queries;
// g_node_color[i] = 1 for white, 0 for black
int g_node_color[kMaxNodes];
vector<int> g_graph[kMaxNodes];

// --- Step 1: Multi-Source BFS ---
// g_dist_to_white[i] = shortest distance from node i to *any* white node
int g_dist_to_white[kMaxNodes];

/**
 * @brief Performs a multi-source BFS from all white nodes.
 * Populates the g_dist_to_white[] array.
 */
void compute_white_distances() {
    queue<int> q;
    for (int i = 1; i <= g_num_nodes; ++i) {
        if (g_node_color[i] == 1) {
            g_dist_to_white[i] = 0;
            q.push(i);
        } else {
            g_dist_to_white[i] = kInfinity;
        }
    }

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        for (int v : g_graph[u]) {
            if (g_dist_to_white[v] == kInfinity) {
                g_dist_to_white[v] = g_dist_to_white[u] + 1;
                q.push(v);
            }
        }
    }
}

// --- Step 2: Binary Lifting & Path Min ---
int g_depth[kMaxNodes];
// g_ancestor[u][i] = 2^i-th ancestor of u
int g_ancestor[kMaxNodes][kMaxLogN];
// g_path_min_dist[u][i] = min(g_dist_to_white[p]) for all p on the
//                         path from u to its 2^i-th ancestor
int g_path_min_dist[kMaxNodes][kMaxLogN];

/**
 * @brief DFS to compute depth, 0th-ancestor, and 0th-path-min.
 */
void tree_dfs(int u, int p, int d) {
    g_depth[u] = d;
    g_ancestor[u][0] = p;
    // The path of length 2^0 (1 node) from u is just u itself.
    g_path_min_dist[u][0] = g_dist_to_white[u];

    for (int v : g_graph[u]) {
        if (v != p) {
            tree_dfs(v, u, d + 1);
        }
    }
}

/**
 * @brief Builds the binary lifting tables.
 */
void precompute_lifting() {
    // Run DFS from root (node 1)
    tree_dfs(1, 0, 0);
    
    // Initialize virtual root (node 0)
    for (int i = 0; i < kMaxLogN; ++i) {
        g_ancestor[0][i] = 0;
        g_path_min_dist[0][i] = kInfinity;
    }

    // Build the DP tables
    for (int i = 1; i < kMaxLogN; ++i) {
        for (int u = 1; u <= g_num_nodes; ++u) {
            int half_ancestor = g_ancestor[u][i - 1];
            g_ancestor[u][i] = g_ancestor[half_ancestor][i - 1];
            
            // The min on the 2^i path is the min of the
            // first 2^(i-1) path and the second 2^(i-1) path
            g_path_min_dist[u][i] = min(
                g_path_min_dist[u][i - 1], 
                g_path_min_dist[half_ancestor][i - 1]
            );
        }
    }
}

// --- Step 3: Answering Queries ---

/**
 * @brief Finds the Lowest Common Ancestor of u and v.
 */
int find_lca(int u, int v) {
    if (g_depth[u] < g_depth[v]) {
        swap(u, v);
    }

    // 1. Bring u to the same depth as v
    for (int i = kMaxLogN - 1; i >= 0; --i) {
        if (g_depth[u] - (1 << i) >= g_depth[v]) {
            u = g_ancestor[u][i];
        }
    }

    if (u == v) {
        return u;
    }

    // 2. Jump u and v up together
    for (int i = kMaxLogN - 1; i >= 0; --i) {
        if (g_ancestor[u][i] != g_ancestor[v][i]) {
            u = g_ancestor[u][i];
            v = g_ancestor[v][i];
        }
    }
    return g_ancestor[u][0];
}

/**
 * @brief Queries the minimum g_dist_to_white[] value on the path
 * from node u up to (but *not* including) the ancestor_node.
 */
int get_path_min_to_ancestor(int u, int ancestor_node) {
    int min_val = kInfinity;
    
    for (int i = kMaxLogN - 1; i >= 0; --i) {
        // Check if the 2^i-th ancestor is valid AND is *strictly above*
        // the target ancestor_node.
        if (g_ancestor[u][i] != 0 && g_depth[g_ancestor[u][i]] > g_depth[ancestor_node]) {
            // This entire 2^i path segment is valid
            min_val = min(min_val, g_path_min_dist[u][i]);
            // Jump up
            u = g_ancestor[u][i];
        }
    }
    
    // After the loop, 'u' is the child of ancestor_node
    // We still need to include its value
    if (u != ancestor_node) {
         min_val = min(min_val, g_path_min_dist[u][0]); // g_dist_to_white[u]
    }
    
    return min_val;
}

int main() {
    // Fast I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cin >> g_num_nodes >> g_num_queries;
    for (int i = 1; i <= g_num_nodes; ++i) {
        cin >> g_node_color[i];
    }
    for (int i = 0; i < g_num_nodes - 1; ++i) {
        int u, v;
        cin >> u >> v;
        g_graph[u].push_back(v);
        g_graph[v].push_back(u);
    }

    // Step 1: Precompute distances to nearest white node
    compute_white_distances();
    
    // Step 2: Precompute LCA and path-min structures
    precompute_lifting();
    
    // Step 3: Process queries
    for (int i = 0; i < g_num_queries; ++i) {
        int u, v;
        cin >> u >> v;

        int lca = find_lca(u, v);
        
        // The final answer is the minimum of:
        // 1. The distance at the LCA itself
        int min_path_dist = g_dist_to_white[lca];
        
        // 2. The minimum on the path from u up to (but not incl.) the LCA
        min_path_dist = min(min_path_dist, get_path_min_to_ancestor(u, lca));
        
        // 3. The minimum on the path from v up to (but not incl.) the LCA
        min_path_dist = min(min_path_dist, get_path_min_to_ancestor(v, lca));
        
        cout << min_path_dist << "\n";
    }

    return 0;
}