import numpy as np

def univ3_cl(pa, pb, x, n):
    # Calculate initial y using the formula for invariant
    y = (x * pa * pb) / (pa * pb - x * (pb - pa))
    
    # Calculate initial liquidity L
    L = np.sqrt(x * y * pa * pb)
    
    # Generate price levels
    price_levels = np.linspace(pa, pb, n)
    
    # Calculate token balances at each price level
    results = []
    for p in price_levels:
        X = L * (np.sqrt(pb) - np.sqrt(p)) / (np.sqrt(p * pb))
        Y = L * (np.sqrt(p) - np.sqrt(pa))
        results.append((p, X, Y))
    
    return results

# Example usage
pa = 1000
pb = 2000
x = 3
n = 3

result = univ3_cl(pa, pb, x, n)

# Improved print format
print("Price\t\tToken X\t\tToken Y")
print("-" * 40)
for price, x, y in result:
    print(f"{price:.2f}\t\t{x:.2f}\t\t{y:.2f}")
