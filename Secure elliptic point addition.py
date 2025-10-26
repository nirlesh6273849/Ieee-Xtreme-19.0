import sys

# Use fast I/O
input = sys.stdin.readline
output = sys.stdout.write

def inverse_mod_p(k, p):
    """
    Computes the modular multiplicative inverse of k mod p
    using Fermat's Little Theorem, k^(p-2) mod p.
    """
    # pow(base, exponent, modulus) is efficient
    return pow(k, p - 2, p)

def solve():
    """
    Reads curve parameters and points, computes P1 + P2.
    """
    try:
        # Read a, b, p, x1, y1, x2, y2
        params = list(map(int, input().split()))
        if len(params) != 7:
            return None # Stop processing
        a, b, p, x1, y1, x2, y2 = params
    except (IOError, ValueError):
        return None # Stop processing

    # --- Elliptic Curve Point Addition Logic ---

    slope = 0
    
    # Case 1: P1 + P2 = O (Point at Infinity)
    # This happens if x1 = x2 and y1 = -y2 mod p
    if x1 == x2 and y1 != y2:
        if y2 == (p - y1) % p:
            return "POINT_AT_INFINITY"

    # Case 2: Point Doubling (P1 = P2)
    if x1 == x2 and y1 == y2:
        # Sub-case: 2*P1 = O if y1 = 0 (vertical tangent)
        if y1 == 0:
            return "POINT_AT_INFINITY"
            
        # General Doubling: slope = (3*x1^2 + a) * (2*y1)^-1 mod p
        numerator = (3 * x1 * x1 + a) % p
        denominator = (2 * y1) % p

    # Case 3: General Addition (P1 != P2 and P1 != -P2)
    else:
        # General Addition: slope = (y2 - y1) * (x2 - x1)^-1 mod p
        numerator = (y2 - y1) % p
        denominator = (x2 - x1) % p

    # --- Calculate slope and new coordinates ---

    # Handle negative numerators/denominators before inverse
    numerator = (numerator + p) % p
    denominator = (denominator + p) % p

    # This check is crucial for Case 3, where denominator might be 0
    # if x1 = x2. But Case 1 and 2 should have already caught this.
    if denominator == 0:
        # This implies x1 = x2, which should be caught by Case 1 or 2
        # If it's Case 1 but y1 != -y2, it's an invalid state (two points
        # on a vertical line that aren't inverses).
        # We can treat this as infinity.
        return "POINT_AT_INFINITY"

    inv_denominator = inverse_mod_p(denominator, p)
    slope = (numerator * inv_denominator) % p

    # Calculate coordinates of P3 = (x3, y3)
    # x3 = slope^2 - x1 - x2 mod p
    x3 = (slope * slope - x1 - x2) % p
      
    # y3 = slope * (x1 - x3) - y1 mod p
    y3 = (slope * (x1 - x3) - y1) % p

    # Ensure coordinates are positive (0 to p-1)
    x3 = (x3 + p) % p
    y3 = (y3 + p) % p
        
    return f"{x3} {y3}"

def main():
    try:
        T = int(input())
    except (IOError, ValueError):
        return

    output_lines = []
    for _ in range(T):
        result = solve()
        if result is None:
            break
        output_lines.append(result)

    # Print all results at once
    output('\n'.join(output_lines) + '\n')

if __name__ == "__main__":
    main()