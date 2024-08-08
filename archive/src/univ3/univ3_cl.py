import numpy as np

def univ3_cl(pa, pb, x, prices):
    """
    Calculates the balances of token X and token Y at different price levels 
    in a Uniswap v3 liquidity pool considering concentrated liquidity.

    Parameters:
    pa (float): The lower bound of the price range.
    pb (float): The upper bound of the price range.
    x (float): The initial amount of token X.
    prices (np.array): The price levels to compute balances for.

    Returns:
    np.array: An array where each row contains the price level, 
              the balance of token X, and the balance of token Y 
              at that price level in the form [price, token_X_balance, token_Y_balance].
    """
    
    # Ensure prices is a NumPy array
    prices = np.asarray(prices)
    
    # Calculate initial liquidity L
    sqrt_pa = np.sqrt(pa)
    sqrt_pb = np.sqrt(pb)
    L = x * np.sqrt(pa * pb) / (sqrt_pb - sqrt_pa)
    
    # Precompute common terms
    sqrt_prices = np.sqrt(prices)
    
    # Create masks for different price ranges
    mask_below = prices < pa
    mask_between = (pa <= prices) & (prices <= pb)
    mask_above = prices > pb
    
    # Initialize X and Y arrays
    X = np.zeros_like(prices)
    Y = np.zeros_like(prices)
    
    # Calculate token balances for each price range
    X[mask_below] = L / sqrt_pa
    X[mask_between] = L * (sqrt_pb - sqrt_prices[mask_between]) / (sqrt_prices[mask_between] * sqrt_pb)
    Y[mask_between] = L * (sqrt_prices[mask_between] - sqrt_pa)
    Y[mask_above] = L * (sqrt_pb - sqrt_pa)
    
    # Combine results
    results = np.column_stack((prices, X, Y))
    
    return results