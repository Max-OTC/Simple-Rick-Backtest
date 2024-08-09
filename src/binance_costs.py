import numpy as np
#from univ3_cl import rebalance_cl
import src.vars as vars

def get_next_trigger_prices(current_price, limit_orders):
    """
    Returns the next higher and lower prices that will trigger calculate_crossings.
    """
    higher_prices = limit_orders[limit_orders[:, 0] > current_price, 0]
    lower_prices = limit_orders[limit_orders[:, 0] < current_price, 0]
    
    next_higher = np.min(higher_prices) if higher_prices.size > 0 else None
    next_lower = np.max(lower_prices) if lower_prices.size > 0 else None
    
    return next_lower, next_higher

def calculate_crossings(price1, price2, limit_orders):
    """
    Based on the limit_orders, compute if a price crossing occurs between price1 and price2,
    and calculate the impact if crossing occurs.
    """
    # Ensure price1 < price2
    price1, price2 = min(price1, price2), max(price1, price2)

    # Find indices of crossed prices
    crossed_indices = np.where((limit_orders[:, 0] > price1) & (limit_orders[:, 0] <= price2))[0]

    if len(crossed_indices) == 0:
        return 0  # No crossings

    cumulative_pnl = 0
    for i in crossed_indices:
        if i > 0:  # Skip the first crossed price if it's the origin
            x = limit_orders[i, 1] - limit_orders[i-1, 1]
            prev_price = limit_orders[i-1, 0]
            current_price = limit_orders[i, 0]
            cumulative_pnl += binance_rebalance_loss(x, prev_price, current_price)

    return cumulative_pnl

def binance_rebalance_loss(x, price1, price2):
    """
    Calculates the PnL for the price movement from price1 to price2 given the initial x value.
    """
    pnl = x * (price2 - price1) 
    fee = pnl * ( 1 + vars.binance_fee )
    return fee

# Example usage
#def test_rebalance_cl():
    balance_price = 1500
    range_percent = 40
    total_value = 10000
    step_percent = 5

    #limit_orders = rebalance_cl(balance_price, range_percent, total_value, step_percent)

    #print("\nLimit orders:")
    #np.set_printoptions(precision=2, suppress=True)
    #print(limit_orders)

    #current_price = 1550
    #next_lower, next_higher = get_next_trigger_prices(current_price, limit_orders)
    #print(f"\nCurrent price: {current_price}")
    #print(f"Next lower trigger price: {next_lower}")
    #print(f"Next higher trigger price: {next_higher}")

    # Only calculate crossings if the price has moved to a trigger price
    #if next_higher is not None and current_price >= next_higher:
        #result = calculate_crossings(balance_price, next_higher, limit_orders)
        #print(f"\nCumulative PnL for price movement from {balance_price} to {next_higher}: {result:.2f}")
    #elif next_lower is not None and current_price <= next_lower:
        #result = calculate_crossings(balance_price, next_lower, limit_orders)
    #    print(f"\nCumulative PnL for price movement from {balance_price} to {next_lower}: {result:.2f}")
    #else:
        #print("\nNo crossing occurred. No need to calculate PnL.")

#test_rebalance_cl()
