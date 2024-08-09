import src.vars as vars
from univ3_cl import rebalance_cl
import time

last_rebalance_time = 0

def strategy_manager():
    if last_rebalance_time == 0:
        rebalance_cl()
    elif vars.last_tick_time - last_rebalance_time > 3600:
        if vars.current_px > vars.current_pb and vars.current_pa > vars.current_pb:
            rebalance_cl()




