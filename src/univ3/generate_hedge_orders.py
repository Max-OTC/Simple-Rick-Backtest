import numpy as np
from src.univ3.x1_x2_balance import x1_x2_balance, delta_hedge, usdeth_binance_delta_hedge

def generate_hedge_orders(current_price, range_lower, range_upper, pool_amount_usdc, hedge_amount_usdc, order_spacing):
    orders = []
    current_hedge = 0
    
    # Calculate the number of steps
    num_steps = int((range_upper - range_lower) / (range_lower * order_spacing / 100)) + 1
    
    print(f"Number of steps: {num_steps}")
    
    for step in range(num_steps):
        if current_price < range_lower:
            token1_balance, token2_balance = x1_x2_balance(pool_amount_usdc, price, range_lower, range_upper)


        # Calculate price for this step, starting from the lower bound
        price = range_lower * (1 + step * order_spacing / 100)
        price = min(price, range_upper)
        print( f"Price: {price:.2f}")
        
        # Calculate balance at this price
        token1_balance, token2_balance = x1_x2_balance(pool_amount_usdc, price, range_lower, range_upper)
        print(f"Token1: {token1_balance:.2f} USDC, Token2: {token2_balance:.6f} ETH ({token2_balance * price:.2f} USD)")
        
        # Calculate total hedge amount in ETH
        total_hedge_eth = hedge_amount_usdc / current_price
        print(f"Total Hedge Amount in ETH: {total_hedge_eth:.6f}")
        
        # Calculate hedge amount for this step
        hedge_amount = (total_hedge_eth / num_steps)
        print(f"Hedge Amount: {hedge_amount:.6f}")
        
        is_long = price > current_price
        orders.append({
            'price': price,
            'amount': hedge_amount,
            'isLong': is_long
        })
        print(f"Price: {price:.2f}, Token1: {token1_balance:.2f} USDC, Token2: {token2_balance:.6f} ETH ({token2_balance * price:.2f} USD), {order_type} Order: {hedge_amount:.6f} ETH")
    
    return orders

# Example usage
current_price = 1855  # Current ETH price in USDC
range_lower = 1850    # Lower bound of Uniswap V3 range
range_upper = 1860    # Upper bound of Uniswap V3 range
pool_amount_usdc = 10000   # Amount for Uniswap V3 pool
hedge_amount_usdc = 10000  # Amount for hedging
order_spacing = 0.1   # Order spacing in percent

hedge_orders = generate_hedge_orders(current_price, range_lower, range_upper, pool_amount_usdc, hedge_amount_usdc, order_spacing)

print("\nFinal Orders:")
for order in hedge_orders:
    print(f"Price: {order['price']:.2f}, Amount: {order['amount']:.6f}, isLong: {order['isLong']}")