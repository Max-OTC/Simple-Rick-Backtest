from src.strategy.grid import strategy


def strategy_manager(next_tick_price, next_tick_time):
    strategy(next_tick_price, next_tick_time)