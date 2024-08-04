import numpy as np

def token1_token2_balance(amount_token1, amount_token2, current_price, range_lower, range_upper, buffer=0.0001):
    """
    Calculate the balance of token1 and token2 based on concentrated liquidity in Uniswap V3.
    
    :param amount_token1: Initial amount of token1
    :param amount_token2: Initial amount of token2
    :param current_price: Current price of token2 in terms of token1
    :param range_lower: Lower price range
    :param range_upper: Upper price range
    :param buffer: Small buffer to handle edge cases
    :return: Tuple of (token1_balance, token2_balance)
    """
    total_value = amount_token1 + amount_token2 * current_price

    if current_price < range_lower * (1 + buffer):
        # All liquidity is in token1
        return total_value, 0
    
    elif current_price > range_upper * (1 - buffer):
        # All liquidity is in token2
        return 0, total_value / current_price
    
    else:
        # Liquidity is distributed between token1 and token2
        sqrt_price = np.sqrt(current_price)
        sqrt_lower = np.sqrt(range_lower)
        sqrt_upper = np.sqrt(range_upper)
        
        L = total_value / (sqrt_upper - sqrt_lower)
        
        token1_balance = L * (sqrt_upper - sqrt_price)
        token2_balance = L * (1/sqrt_price - 1/sqrt_upper)
        
        return token1_balance, token2_balance

# Example usage:
# amount_token1 = 1000  # e.g., 1000 USDC
# amount_token2 = 0.5   # e.g., 0.5 WETH
# current_price = 2200  # Current price of WETH in USDC
# range_lower = 1800    # Lower price range
# range_upper = 2200    # Upper price range

# alance_token1, balance_token2 = token1_token2_balance(amount_token1, amount_token2, current_price, range_lower, range_upper)
# print(f"price: {current_price}")
# print(f"Token1 balance: {balance_token1}")
# print(f"Token2 balance: {balance_token2}")