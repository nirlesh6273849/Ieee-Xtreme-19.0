import sys

# Use fast I/O
input = sys.stdin.readline
output = sys.stdout.write

def find_triplet(N):
    """
    Attempts to construct a triplet (A, B, C) for a given N.
    Returns (A, B, C) on success or None on failure.
    """
    
    # Condition 1: N must be even
    if N % 2 != 0:
        return None
    
    # Condition 2: N must not be a power of two
    # (N & (N - 1) == 0) is true if N is a power of two
    if N & (N - 1) == 0:
        return None

    # Try iterating through powers of two
    exponent = 0
    while True:
        power_of_two = 1 << exponent
        
        # Stop if 2^k >= N
        if power_of_two >= N:
            break
            
        remainder = N - power_of_two
        
        # We need (remainder - power_of_two) to be non-negative and even
        if remainder >= power_of_two and (remainder - power_of_two) % 2 == 0:
            
            common_bits = (remainder - power_of_two) // 2
            
            # The 'and' part (common_bits) must not overlap with the 'xor' part (power_of_two)
            if (common_bits & power_of_two) == 0:
                
                # We found a valid construction.
                # Reconstruct x and y from their AND and XOR
                # x = common_bits | power_of_two
                # y = common_bits
                x = common_bits | power_of_two
                y = common_bits
                
                # Reconstruct A, B, C
                A = N + power_of_two
                B = x
                C = y
                
                # Final safety checks (must be positive and distinct)
                if A > 0 and B > 0 and C > 0 and A != B and B != C and A != C:
                    # (Verification, not strictly needed)
                    # if (A + B + C == 2 * N) and (A ^ B ^ C == N):
                    return (A, B, C)
                        
        exponent += 1
        # 63 bits is sufficient for 2^63 range
        if exponent > 62:
            break
            
    # No solution found
    return None

def main():
    """
    Reads the number of test cases and runs find_triplet for each.
    """
    try:
        t = int(input())
    except (IOError, ValueError):
        t = 0
        
    output_lines = []
    for _ in range(t):
        try:
            N = int(input())
        except (IOError, ValueError):
            continue
            
        result = find_triplet(N)
        
        if result is None:
            output_lines.append("-1")
        else:
            output_lines.append(f"{result[0]} {result[1]} {result[2]}")
            
    output("\n".join(output_lines) + "\n")

if __name__ == "__main__":
    main()