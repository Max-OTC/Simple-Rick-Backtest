import src.binance.vars as vars
from src.binance.fill_long_short import fill_long_short
from src.univ3.compute_price_levels import compute_price_levels
from src.binance.add_limit_order import add_limit_order
import time

open_cl_balance = 0

def rebalance_range(px):
    fill_long_short(vars.long, px, False)
    fill_long_short(vars.long, px, True)
    vars.limit_order_list.clear()
    px = vars.avg_entry_price
    vars.pa = px * (1 - vars.cl_range / 2)
    vars.pb = px * (1 + vars.cl_range / 2)
    
    price_levels = compute_price_levels(vars.pa, vars.pb, vars.balance * vars.borrow_haircut, px, vars.step)
    for price, delta_x, delta_y in price_levels:
        if delta_x >= 0:
            add_limit_order(delta_x, price, False)
        else:
            add_limit_order(delta_x, price, True)
    global open_cl_balance
    open_cl_balance = vars.balance

def range_rebalance(px):
    current_time = time.time()
    if current_time - last_rebalance_time >= 3600:  # 1 hour in seconds
        if px < vars.pa or px > vars.pb:
            rebalance_range(px)
            last_rebalance_time = current_time

def cl_token_delta(px, py=1):
    global avg_entry_x, avg_entry_y, x_amount_bought, y_amount_bought
    if avg_entry_x == 0 or avg_entry_y == 0 or x_amount_bought == 0 or y_amount_bought == 0:
        return 0
    
    # Calculate token delta between entry and exit of range
    x_value_entry = x_amount_bought * avg_entry_x
    y_value_entry = y_amount_bought * avg_entry_y
    
    x_value_current = x_amount_bought * px
    y_value_current = y_amount_bought / py
    
    return (x_value_current + y_value_current) - (x_value_entry + y_value_entry)

def strategy(next_tick_price, next_tick_time):
    if vars.pa == 0 and vars.pb == 0:
        rebalance_range(next_tick_price)
    
    range_rebalance(next_tick_price)
    
    # Rebalance each tick the orders, but don't change pa and pb, just change px
    price_levels = compute_price_levels(vars.pa, vars.pb, open_cl_balance * vars.borrow_haircut, next_tick_price, vars.step)
    for price, delta_x, delta_y in price_levels:
        if delta_x >= 0:
            add_limit_order(delta_x, price, False)
        else:
            add_limit_order(delta_x, price, True)
    
        # Exit range
        #close_last_cl(next_tick_price)
        # Sell token2 for token1 at vars.univ3_swap_fee
        # Close market binance futures hedge position (short here)
        # These operations would need to be implemented based on your specific requirements

def close_last_cl(px):
    global open_cl_balance
    price_levels = compute_price_levels(vars.pa, vars.pb, open_cl_balance * vars.borrow_haircut, px, vars.step)
    for price, delta_x, delta_y in price_levels:
        if price == px:
            # Implement the logic to close the position at this price
            # This might involve selling/buying tokens and updating balances
            pass
    open_cl_balance = 0

# Initialize global variables
avg_entry_x = 0
avg_entry_y = 0
x_amount_bought = 0
y_amount_bought = 0
last_rebalance_time = time.time()
