import numpy as np

def x1_x2_balance(usd_notional, current_price, range_lower, range_upper, buffer=0.0001):
    """
    Calculate the balance of token1 (USDC) and token2 (ETH) based on concentrated liquidity in Uniswap V3.
    
    :param usd_notional: Total value of the position in USD
    :param current_price: Current price of ETH in USDC
    :param range_lower: Lower price range in USDC
    :param range_upper: Upper price range in USDC
    :param buffer: Small buffer to handle edge cases
    :return: Tuple of (usdc_balance, eth_balance)
    """
    if current_price < range_lower * (1 + buffer):
        # All liquidity is in USDC
        return usd_notional, 0
    
    elif current_price > range_upper * (1 - buffer):
        # All liquidity is in ETH
        return 0, usd_notional / current_price
    
    else:
        # Liquidity is distributed between USDC and ETH
        sqrt_price = np.sqrt(current_price)
        sqrt_lower = np.sqrt(range_lower)
        sqrt_upper = np.sqrt(range_upper)
        
        L = usd_notional / (2 * (sqrt_upper - sqrt_lower) * sqrt_price)
        
        usdc_balance = L * (sqrt_upper - sqrt_price) * sqrt_price
        eth_balance = L * (sqrt_price - sqrt_lower) / sqrt_price
        
        return usdc_balance, eth_balance

def delta_hedge(usd_notional, current_price, step, range_lower, range_upper):
    prev_balance_token1, prev_balance_token2 = x1_x2_balance(usd_notional, current_price, range_lower, range_upper)
    new_price = current_price * (1 + step)
    balance_token1, balance_token2 = x1_x2_balance(usd_notional, new_price, range_lower, range_upper)
    
    delta_token1 = balance_token1 - prev_balance_token1
    delta_token2 = balance_token2 - prev_balance_token2
    
    print(f"Price: {current_price:.2f} -> {new_price:.2f}")
    print(f"USDC: {prev_balance_token1:.4f} -> {balance_token1:.4f}, Delta: {delta_token1:.4f}")
    print(f"ETH: {prev_balance_token2:.4f} -> {balance_token2:.4f}, Delta: {delta_token2:.4f}")
    
    return delta_token1, delta_token2

# Test the function
usd_notional = 10000   
current_price = 2200  # USDC per ETH
range_lower = 1800    
range_upper = 2200  

step = -0.001  # -0.1% price change

delta1, delta2 = delta_hedge(usd_notional, current_price, step, range_lower, range_upper)
print(f"\nFinal Delta USDC: {delta1:.4f}")
print(f"Final Delta ETH: {delta2:.4f}")