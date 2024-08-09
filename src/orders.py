import numpy as np
import src.vars as vars
from src.upnl_logger import upnl_logger
from src.strategy_manager import strategy_manager
from src.get_next_tick import get_next_tick
from collections import defaultdict
from src.univ3_fee_sim import univ3_fee_sim
from binance_costs import calculate_crossings, get_next_trigger_prices

def process_next_tick():
    if vars.current_px != 0:
        next_lower, next_higher = get_next_trigger_prices(vars.current_px, vars.limit_order_list)
    next_tick_price, next_tick_time = get_next_tick(vars.last_time)
    vars.last_px = vars.current_px
    vars.last_px = next_tick_price
    vars.tn = next_tick_time
    if next_tick_price is None:
        return False
    
    upnl_logger()
    calculate_crossings(vars.last_px, vars.current_px, vars.limit_orders)

    #univ3_fee_sim(univ3_data)
    #
    strategy_manager()
    
    vars.last_time = next_tick_time 
    vars.last_tick_price = next_tick_price

    return True

def fill_limit_orders(next_tick_price):
    if not vars.limit_order_list:
        return

    prices = np.array(list(vars.limit_order_list.keys()))
    long_mask = (next_tick_price >= prices) & np.array([orders[0].isLong for orders in vars.limit_order_list.values()])
    short_mask = (next_tick_price <= prices) & np.array([not orders[0].isLong for orders in vars.limit_order_list.values()])
    fill_mask = long_mask | short_mask

    new_limit_order_list = defaultdict(list)

    for price, should_fill in zip(prices, fill_mask):
        orders = vars.limit_order_list[price]
        if should_fill:
            for order in orders:
                fill_long_short(order.amount, price, order.isLong)
        else:
            new_limit_order_list[price] = orders

    vars.limit_order_list = dict(new_limit_order_list)