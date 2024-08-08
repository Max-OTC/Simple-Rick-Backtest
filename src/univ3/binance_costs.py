
import numpy as np
from univ3_cl import rebalance_cl

def calculate_crossings(price1, price2):
    """
    Based on the limit_orders, compute if a price crossing occurs between price1 and price2,
    and calculate the impact if crossing occurs.
    """
    global limit_orders
    if limit_orders is None:
        raise ValueError("No limit orders stored. Please run store_limit_orders first.")
    
    # Identify if we crossed any prices
    crossed = limit_orders[(limit_orders[:, 0] > price1) & (limit_orders[:, 0] <= price2)]
    
    if crossed.size == 0:
        print("No crossings.")
        return None
    
    results = []
    current_price = price1

    for i in range(len(crossed)):
        next_price = crossed[i, 0]
        if i == 0:
            results.append((current_price, next_price, crossed[i]))
        else:
            results.append((results[-1][1], next_price, crossed[i]))
    
    # Add final crossing from last limit order to price2
    results.append((results[-1][1], price2, crossed[-1]))
    
    total_pnl = 0

    print("Crossed Price Ranges and Binance PnL:")
    for r in results:
        total_pnl += binance_rebalance_loss(r[2][1], r[0], r[1])
    print(f"From {r[0]:.6f} to {r[1]:.6f}, Binance PnL: {total_pnl:.6f}")
    
    
    return results

def binance_rebalance_loss(x, price1, price2):
    """
    Calculates the PnL for the price movement from price1 to price2 given the initial x value.
    """
    return - x * (price2 - price1) / price1

# Example usage
balance_price = 1500
range_percent = 40
total_value = 10000
step_percent = 5

limit_orders = rebalance_cl(balance_price, range_percent, total_value, step_percent)

print("\nLimit orders:")
np.set_printoptions(precision=2, suppress=True)
print(limit_orders)

calculate_crossings(balance_price, 1600)
