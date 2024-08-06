import numpy as np
from univ3_cl import univ3_cl
from get_cl_deltas import get_cl_deltas

def compute_price_levels_optimized(pa: float, pb: float, x: float, px: float, step: float) -> list:
    """
    Compute optimized price levels and corresponding token deltas for a Uniswap V3 liquidity pool.

    This function calculates price levels between two bounds (pa and pb) and computes the
    corresponding token deltas (changes in token quantities) at each price level. It uses
    the Uniswap V3 concentrated liquidity model and optimizes the computation for performance.

    Parameters:
    pa (float): The lower bound of the price range.
    pb (float): The upper bound of the price range.
    x (float): The initial amount of token X.
    px (float): The current price point of interest.
    step (float): The step size for price level generation, as a fraction (e.g., 0.2 for 20%).

    Returns:
    list of tuples: A list where each tuple contains:
        - price (float): The price level.
        - delta_x (float): The change in token X quantity at this price level.
        - delta_y (float): The change in token Y quantity at this price level.
    
    The deltas are calculated as follows:
    - For prices above px: delta_up is used (representing liquidity being added).
    - For prices below px: delta_down is used (representing liquidity being removed).
    - At px: deltas are set to 0.

    Note:
    - This function uses logarithmic spacing for more efficient and accurate price level generation.
    - It relies on external functions `univ3_cl` and `get_cl_deltas` for core calculations.
    - The computation is optimized for large datasets using NumPy operations.

    Example:
    >>> result = compute_price_levels_optimized(1000, 2000, 3, 1450, 0.2)
    >>> print(result[0])  # Example output: (1000.0, -0.000000, 0.000000)
    """
    # Generate price levels using logarithmic spacing
    log_pa, log_pb = np.log(pa), np.log(pb)
    num_steps = int(np.ceil((log_pb - log_pa) / np.log(1 + step)))
    price_levels = np.exp(np.linspace(log_pa, log_pb, num_steps + 1))
    
    # Add px to the price levels if it's within the range
    if pa < px < pb:
        price_levels = np.sort(np.append(price_levels, px))
    
    # Compute results using univ3_cl
    results = univ3_cl(pa, pb, x, price_levels)
    
    # Calculate deltas using get_cl_deltas
    delta_vector = get_cl_deltas(results)
    
    # Convert delta_vector to numpy array for faster processing
    delta_array = np.array(delta_vector)
    
    # Create mask for prices above and below px
    mask_above = delta_array[:, 0] > px
    mask_below = delta_array[:, 0] < px
    
    # Create output array
    output = np.zeros((len(price_levels), 3))
    output[:, 0] = delta_array[:, 0]  # Price
    output[mask_above, 1:] = delta_array[mask_above, 1:3]  # Delta up for prices above px
    output[mask_below, 1:] = delta_array[mask_below, 3:5]  # Delta down for prices below px
    
    # Set deltas to 0 for px
    output[delta_array[:, 0] == px, 1:] = 0
    
    return output.tolist()  # Convert back to list of tuples for consistency
# Test the function
pa = 1000
pb = 2000
x = 3
px = 1450
step = 0.2  # 20% step

result = compute_price_levels_optimized(pa, pb, x, px, step)

# Print the result in a table format
print("\nFinal Result:")
print("Price\t\tDelta X\t\tDelta Y")
print("-" * 40)
for price, delta_x, delta_y in result:
    print(f"{price:.2f}\t\t{delta_x:.6f}\t\t{delta_y:.6f}")