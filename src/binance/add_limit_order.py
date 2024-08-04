import src.binance.vars as vars


def add_limit_order(amount, price, isLong):
    if price not in vars.limit_order_list:
        vars.limit_order_list[price] = []
    vars.limit_order_list[price].append(vars.LimitOrder(amount, isLong))