import numpy as np
import src.vars as vars
from src.upnl_logger import upnl_logger
from src.strategy_manager import strategy_manager
from src.get_next_binance_tick import get_next_binance_tick
from src.get_next_univ3_tick import get_next_univ3_tick
from src.univ3_fee_sim import univ3_fee_sim
from src.binance_costs import calculate_crossings, get_next_trigger_prices

def process_next_tick():
    if vars.current_px != 0:
        next_lower, next_higher = get_next_trigger_prices(vars.current_px, vars.limit_order_list)
    binance_tick_price, binance_tick_time = get_next_binance_tick(vars.last_time)
    univ3_ticks = get_next_univ3_tick(vars.last_time, binance_tick_time)
    vars.last_px = vars.current_px
    vars.last_px = binance_tick_price
    vars.last_tick_time = binance_tick_time
    if binance_tick_price is None:
        return False
    
    upnl_logger(binance_tick_time)
    calculate_crossings(vars.last_px, vars.current_px, vars.limit_orders)
    univ3_fee_sim(univ3_ticks)
    strategy_manager()
    
    vars.last_time = binance_tick_time 
    vars.last_tick_price = binance_tick_price

    return True