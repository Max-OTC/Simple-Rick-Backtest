from src.binance.add_limit_order import add_limit_order
import src.binance.vars as vars
import numpy as np

first_price = 0
grid_interval = 0.0001  # 0.5%
num_grids = 10  # Number of grids above and below the initial price

def round_to_nearest_half_percent(price):
    return round(price / (price * grid_interval)) * (price * grid_interval)

def setup_grid(base_price):
    vars.limit_order_list.clear()
    
    # Generate grid prices in a vectorized manner
    grid_multipliers = np.arange(1, num_grids + 1) * grid_interval
    long_prices = base_price * (1 + grid_multipliers)
    short_prices = base_price * (1 - grid_multipliers)
    
    # Add long orders
    for price in long_prices:
        add_limit_order(0.01, price, True)
    
    # Add short orders
    for price in short_prices:
        add_limit_order(0.01, price, False)

def strategy_manager(next_tick_price, next_tick_time):
    global first_price
    
    if first_price == 0:
        first_price = next_tick_price
        base_price = round_to_nearest_half_percent(first_price)
        setup_grid(base_price)
    
    # Reset the grid every hour
    if next_tick_time % 3600 == 0:
        base_price = round_to_nearest_half_percent(next_tick_price)
        setup_grid(base_price)