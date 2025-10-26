import sys
import threading

# Increase recursion depth for DSU operations
sys.setrecursionlimit(2 * 10**5) 

class DisjointSetUnion:
    """A DSU implementation using a dictionary for sparse grids."""
    def __init__(self):
        self.parent_map = {}
        self.component_values = {}

    def add_cell(self, cell_id, initial_value):
        """Adds a new cell to the DSU as its own component."""
        if cell_id not in self.parent_map:
            self.parent_map[cell_id] = cell_id
            self.component_values[cell_id] = [initial_value]

    def find_root(self, cell_id):
        """Finds the root of the component for cell_id with path compression."""
        if self.parent_map[cell_id] == cell_id:
            return cell_id
        
        root = self.find_root(self.parent_map[cell_id])
        self.parent_map[cell_id] = root
        return root

    def merge_sets(self, cell_id_a, cell_id_b):
        """Merges the sets containing cell_id_a and cell_id_b."""
        root_a = self.find_root(cell_id_a)
        root_b = self.find_root(cell_id_b)
        
        if root_a != root_b:
            # Merge smaller component into larger (by convention, b into a)
            self.parent_map[root_b] = root_a
            # Move component values
            self.component_values[root_a].extend(self.component_values[root_b])
            del self.component_values[root_b]

def coords_to_id(r, c, M):
    """Encodes (row, col) coordinates into a unique integer ID."""
    return r * M + c

def link_symmetric_cells(cells, dsu, M):
    """
    Given a list of (r, c) coords for a word,
    merges the sets of symmetric cells.
    """
    n = len(cells)
    for i in range(n // 2):
        r1, c1 = cells[i]
        r2, c2 = cells[n - 1 - i]
        dsu.merge_sets(coords_to_id(r1, c1, M), coords_to_id(r2, c2, M))

def solve():
    """
    Main logic for the Palindrome Matrix problem.
    """
    N, M = map(int, sys.stdin.readline().split())
    grid = [list(sys.stdin.readline().strip()) for _ in range(N)]

    dsu = DisjointSetUnion()

    # 1. Initialize DSU with all non-empty cells
    for r in range(N):
        for c in range(M):
            if grid[r][c] != '.':
                dsu.add_cell(coords_to_id(r, c, M), int(grid[r][c]))

    # 2. Link symmetric cells in row-words
    for r in range(N):
        current_word_coords = []
        for c in range(M):
            if grid[r][c] != '.':
                current_word_coords.append((r, c))
            else:
                if current_word_coords:
                    # End of a word, process it
                    link_symmetric_cells(current_word_coords, dsu, M)
                    current_word_coords = []
        # Process the last word in the row
        if current_word_coords:
            link_symmetric_cells(current_word_coords, dsu, M)

    # 3. Link symmetric cells in column-words
    for c in range(M):
        current_word_coords = []
        for r in range(N):
            if grid[r][c] != '.':
                current_word_coords.append((r, c))
            else:
                if current_word_coords:
                    link_symmetric_cells(current_word_coords, dsu, M)
                    current_word_coords = []
        # Process the last word in the column
        if current_word_coords:
            link_symmetric_cells(current_word_coords, dsu, M)

    # 4. Create the result grid
    result_grid = [row[:] for row in grid]
    
    # 5. Fill in the optimal digit for each component
    # We only need the component values from the roots
    for root_id, component_digits in dsu.component_values.items():
        
        # Find the digit (0-9) that minimizes the cost
        # Key is a tuple: (total_cost, digit)
        # This tie-breaks by choosing the smallest digit
        best_digit = min(
            range(10), 
            key=lambda d: (sum(abs(d - x) for x in component_digits), d)
        )
        
        # Get the (r, c) coords from the root_id
        # (This is a bit of a hack, we just need one cell from the component)
        r, c = divmod(root_id, M)
        root_cell = (r, c) 
        
        # We need to fill all cells in this component
        # We must re-iterate the grid to find all cells
        # This is inefficient, but the original did this too (via groups)
        
    # Re-build the groups to fill the grid
    # (The original did this, so we will too)
    groups = {}
    for r in range(N):
        for c in range(M):
            if grid[r][c] != '.':
                cell_id = coords_to_id(r,c,M)
                root = dsu.find_root(cell_id)
                if root not in groups:
                    groups[root] = {'coords': [], 'digits': []}
                groups[root]['coords'].append((r,c))
                groups[root]['digits'].append(int(grid[r][c]))

    for root_id, data in groups.items():
        component_digits = data['digits']
        best_digit = min(
            range(10), 
            key=lambda d: (sum(abs(d - x) for x in component_digits), d)
        )
        
        for (r, c) in data['coords']:
            result_grid[r][c] = str(best_digit)

    # 6. Output the result
    for row in result_grid:
        print("".join(row))

# Run the main function in a new thread to avoid stack overflow
threading.Thread(target=solve).start()