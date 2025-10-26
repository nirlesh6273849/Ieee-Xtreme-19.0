import sys

# Use fast I/O
input = sys.stdin.readline
output = sys.stdout.write

def calculate_min_flips(N, K, S):
    """
    Solves a single test case for the Magic Wands problem.
    """
    
    # 1. Initialize state
    # is_sad[i] = 1 if 'S', 0 if 'H'
    is_sad = [0] * N
    for i in range(N):
        if S[i] == 'S':
            is_sad[i] = 1
            
    # flip_events[i] = 1 if a flip operation *ends* just before i
    flip_events = [0] * (N + 1)
    
    total_operations = 0
    active_flips = 0 # How many active flips cover the current index

    # 2. Greedy pass: Fix elements from 0 to N-K
    # This loop is correct even if N < K (range is empty)
    for i in range(N - K + 1):
        
        # Update active_flips: add effect of flips starting/ending at i
        # (In this model, we only track end events)
        active_flips ^= flip_events[i]
        
        # Get the actual current state
        # 0 (H) or 1 (S)
        current_state = is_sad[i] ^ active_flips
        
        if current_state == 1:
            # This student is 'S', so we MUST flip
            total_operations += 1
            
            # This new flip starts at i
            active_flips ^= 1
            
            # This new flip ends at i+K
            # We mark the end event
            if i + K <= N:
                flip_events[i + K] ^= 1

    # 3. Check pass: Check elements from N-K+1 to N
    # These elements could not be the *start* of a flip
    
    # Ensure we don't start checking from a negative index
    check_start_index = max(0, N - K + 1)
    
    for i in range(check_start_index, N):
        active_flips ^= flip_events[i]
        current_state = is_sad[i] ^ active_flips
        
        if current_state == 1:
            # This student is 'S' and we can't fix it
            return "-1"

    # If we get here, all students are 'H'
    return str(total_operations)

def main():
    try:
        T = int(input())
    except (IOError, ValueError):
        return

    results = []
    for _ in range(T):
        try:
            line = input().split()
            if not line:
                break
            N = int(line[0])
            K = int(line[1])
            S = line[2]
        except (IOError, IndexError, ValueError):
            break
            
        results.append(calculate_min_flips(N, K, S))
        
    output("\n".join(results) + "\n")

if __name__ == "__main__":
    main()