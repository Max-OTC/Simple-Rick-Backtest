import numpy as np
import src.binance.vars as vars
from src.binance.upnl_logger import upnl_logger
from src.binance.fill_long_short import fill_long_short
from src.binance.strategy_manager import strategy_manager
from src.binance.get_next_tick import get_next_tick
from src.binance.add_limit_order import add_limit_order
from collections import defaultdict

def process_next_tick():
    next_tick_price, next_tick_time = get_next_tick(vars.last_time)
    if next_tick_price is None:
        return False
    
    upnl_logger(next_tick_time)
    fill_limit_orders(next_tick_price)
    strategy_manager(next_tick_price, next_tick_time)
    
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