#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <deque>

using namespace std;

// Use 64-bit integers
typedef long long ll;
// Use a very large negative number for "infinity" in a max-DP
const ll kNegativeInf = -1e18; 

// Represents a line y = m*x + c
struct LinearFunction {
    ll m, c; 
    
    // Calculates y for a given x
    ll get_value(ll x) const { 
        return m * x + c;
    }
    // Calculates the x-coordinate of the intersection with another line
    double get_intersection_x(const LinearFunction& other) const {
        // (c2 - c1) / (m1 - m2)
        return (double)(other.c - c) / (m - other.m);
    }
};

/**
 * @brief Convex Hull Trick structure for Max Queries.
 * Assumes slopes are added in increasing order (m).
 * Assumes query points (x) are increasing.
 */
struct MaxQueryCHT {
    deque<LinearFunction> hull_lines;

    void insert_line(ll m, ll c) {
        LinearFunction new_line = {m, c};
        
        // Remove lines from the back that are made obsolete
        while (hull_lines.size() >= 2) {
            LinearFunction& l1 = hull_lines[hull_lines.size() - 2];
            LinearFunction& l2 = hull_lines[hull_lines.size() - 1];
            // If new_line intersects l1 before l1 intersects l2,
            // then l2 is obsolete.
            if (l1.get_intersection_x(new_line) <= l1.get_intersection_x(l2)) {
                hull_lines.pop_back();
            } else {
                break;
            }
        }
        hull_lines.push_back(new_line);
    }

    ll query(ll x) {
        if (hull_lines.empty()) {
            return kNegativeInf;
        }
        // Remove lines from the front that are no longer optimal
        // (since query points x are increasing)
        while (hull_lines.size() >= 2) {
            LinearFunction& l1 = hull_lines[0];
            LinearFunction& l2 = hull_lines[1];
            if (l1.get_value(x) <= l2.get_value(x)) {
                hull_lines.pop_front();
            } else {
                break;
            }
        }
        return hull_lines[0].get_value(x);
    }
};

// Helper function for 1D array indexing
inline size_t get_flat_index(int i, int j, int M_cols) {
    return (size_t)i * (M_cols + 1) + j;
}

int main() {
    // Fast I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    string a, b;
    ll match_score, mismatch_score, gap_penalty;

    cin >> n >> a >> m >> b >> match_score >> mismatch_score >> gap_penalty;

    // --- Initialize DP Tables ---
    size_t table_size = (size_t)(n + 1) * (m + 1);
    // match_dp[i][j] = score ending with a[i] vs b[j]
    vector<ll> match_dp(table_size, kNegativeInf);
    // gap_a_dp[i][j] = score ending with a[i] vs '-'
    vector<ll> gap_a_dp(table_size, kNegativeInf);
    // gap_b_dp[i][j] = score ending with '-' vs b[j]
    vector<ll> gap_b_dp(table_size, kNegativeInf);

    // One CHT for each column (for gap_a)
    vector<MaxQueryCHT> col_chtrees(m + 1);
    
    // Base case
    match_dp[get_flat_index(0, 0, m)] = 0;
    
    // Add the 0-th line (Source(0,j) + g*0*0) to all column CHTs
    for (int j = 0; j <= m; ++j) {
        ll g = gap_penalty;
        ll i = 0;
        ll source_val = (j == 0) ? 0 : kNegativeInf;
        col_chtrees[j].insert_line(-2 * g * i, source_val + g * i * i);
    }

    // --- Fill DP Tables ---
    for (int i = 0; i <= n; ++i) {
        // Reusable CHT for the current row i (for gap_b)
        MaxQueryCHT row_chtree;
        
        // Add the 0-th line (Source(i,0) + g*0*0) for this row
        ll g = gap_penalty;
        ll j = 0;
        ll source_val = (i == 0) ? 0 : kNegativeInf;
        row_chtree.insert_line(-2 * g * j, source_val + g * j * j);

        for (int j = 0; j <= m; ++j) {
            if (i == 0 && j == 0) continue;

            size_t curr_idx = get_flat_index(i, j, m);
            
            // --- A. Calculate match_dp[i][j] ---
            if (i > 0 && j > 0) {
                ll score = (a[i - 1] == b[j - 1]) ? match_score : mismatch_score;
                size_t prev_idx = get_flat_index(i - 1, j - 1, m);
                
                ll prev_max = max({match_dp[prev_idx], 
                                   gap_a_dp[prev_idx], 
                                   gap_b_dp[prev_idx]});
                if (prev_max != kNegativeInf) {
                    match_dp[curr_idx] = prev_max + score;
                }
            }

            // --- B. Calculate gap_a_dp[i][j] (gap in b) ---
            if (i > 0) {
                // Query: x = i
                ll max_val = col_chtrees[j].query(i);
                if (max_val != kNegativeInf) {
                    gap_a_dp[curr_idx] = g * i * i + max_val;
                }
            }

            // --- C. Calculate gap_b_dp[i][j] (gap in a) ---
            if (j > 0) {
                // Query: x = j
                ll max_val = row_chtree.query(j);
                if (max_val != kNegativeInf) {
                    gap_b_dp[curr_idx] = g * j * j + max_val;
                }
            }
            
            // --- D. Update CHTs for next iterations ---
            
            // Update col_chtrees[j] for (i+1, j)
            ll prev_state_max_X = max(match_dp[curr_idx], gap_b_dp[curr_idx]);
            if (prev_state_max_X != kNegativeInf) {
                // Add line: m = -2*g*i, c = Source(i,j) + g*i*i
                col_chtrees[j].insert_line(-2 * g * i, prev_state_max_X + g * i * i);
            }

            // Update row_chtree for (i, j+1)
            ll prev_state_max_Y = max(match_dp[curr_idx], gap_a_dp[curr_idx]);
            if (prev_state_max_Y != kNegativeInf) {
                // Add line: m = -2*g*j, c = Source(i,j) + g*j*j
                row_chtree.insert_line(-2 * g * j, prev_state_max_Y + g * j * j);
            }
        }
    }

    // --- Final Answer ---
    size_t final_idx = get_flat_index(n, m, m);
    ll final_M = match_dp[final_idx];
    ll final_X = gap_a_dp[final_idx];
    ll final_Y = gap_b_dp[final_idx];

    cout << max({final_M, final_X, final_Y}) << "\n";
    return 0;
}