import sys

# Use sys.stdin.readline for faster I/O
input = sys.stdin.readline

def add_to_xor_basis(xor_basis, value):
    """
    Inserts a value into a fully reduced (bidirectional) XOR basis.
    """
    for b in xor_basis:
        value = min(value, value ^ b)
    if not value:
        return
    for i in range(len(xor_basis)):
        xor_basis[i] = min(xor_basis[i], xor_basis[i] ^ value)
    xor_basis.append(value)
    xor_basis.sort(reverse=True) # Keep basis sorted

def solve():
    """
    Main function to read input, compute expectation, and print.
    """
    line = input().split()
    if not line:
        return False
        
    N, K = int(line[0]), int(line[1])
    
    values = list(map(int, input().split()))
    
    xor_basis = []
    for val in values:
        add_to_xor_basis(xor_basis, val)

    dim = len(xor_basis)
    if dim == 0:
        # Only reachable value is 0. 0^K is 0 (except 0^0=1)
        if K == 0:
            print("1.00")
        else:
            print("0.00")
        return True

    # Generate all 2^dim reachable XOR sums
    all_xor_sums = [0]
    for b in xor_basis:
        # Add (r ^ b) for every r already in the list
        all_xor_sums.extend([r ^ b for r in all_xor_sums])

    # Sum v^K using Python's arbitrary-precision integers
    total_pow_sum = 0
    for v in all_xor_sums:
        total_pow_sum += pow(v, K)
        
    # Denominator is 2^dim
    denominator = 1 << dim
    
    # --- Fixed-point arithmetic for rounding ---
    # We want (total_pow_sum / denominator) * 100, rounded
    
    # Calculate scaled = (total_pow_sum * 100)
    scaled_numerator = total_pow_sum * 100
    
    # Get quotient and remainder
    q = scaled_numerator // denominator
    r = scaled_numerator % denominator
    
    # Standard rounding (ties round half up)
    if r * 2 >= denominator:
        q += 1
        
    # q now holds the value * 100, rounded.
    int_part = q // 100
    frac_part = q % 100
    
    # Print in the format "INT.FRAC" with leading zero for fraction
    # The f-string ":02d" handles the leading zero (e.g., 5 -> "05")
    print(f"{int_part}.{frac_part:02d}")
    
    return True

if __name__ == "__main__":
    while solve():
        pass