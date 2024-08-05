import numpy as np

def univ3_cl(pa, pb, x, prices):
    """
    Calculates the balances of token X and token Y at different price levels 
    in a Uniswap v3 liquidity pool considering concentrated liquidity.

    Parameters:
    pa (float): The lower bound of the price range.
    pb (float): The upper bound of the price range.
    x (float): The initial amount of token X.
    prices (list or array): The price levels to compute balances for.

    Returns:
    list of tuples: A list of tuples, each containing the price level, 
                    the balance of token X, and the balance of token Y 
                    at that price level in the form (price, token_X_balance, token_Y_balance).
    """
    
    # Calculate initial liquidity L
    L = x * np.sqrt(pa * pb) / (np.sqrt(pb) - np.sqrt(pa))
    
    # Calculate token balances at each price level
    results = []
    for p in prices:
        if p < pa:
            X = L / np.sqrt(pa)
            Y = 0
        elif pa <= p <= pb:
            X = L * (np.sqrt(pb) - np.sqrt(p)) / (np.sqrt(p) * np.sqrt(pb))
            Y = L * (np.sqrt(p) - np.sqrt(pa))
        else:
            X = 0
            Y = L * (np.sqrt(pb) - np.sqrt(pa))
        
        results.append((p, X, Y))
    
    return results

def print_deltas(results):
    """
    Prints the delta between successive token balances for each price level.

    Parameters:
    results (list of tuples): The result from univ3_cl function.
    """
    print("Price\t\tDelta X\t\tDelta Y")
    print("-" * 40)
    
    for i in range(1, len(results)):
        price_prev, x_prev, y_prev = results[i - 1]
        price_curr, x_curr, y_curr = results[i]
        
        delta_x = x_curr - x_prev
        delta_y = y_curr - y_prev
        
        print(f"{price_curr:.2f}\t\t{delta_x:.6f}\t\t{delta_y:.6f}")

# Example usage
pa = 1000
pb = 2000
x = 3
prices = [1000, 1500, 2000]  

result = univ3_cl(pa, pb, x, prices)

# Improved print format
print("Price\t\tToken X\t\tToken Y")
print("-" * 40)
for price, x, y in result:
    print(f"{price:.2f}\t\t{x:.6f}\t\t{y:.6f}")

# Print deltas
print("\nDeltas between successive price levels:")
print_deltas(result)
