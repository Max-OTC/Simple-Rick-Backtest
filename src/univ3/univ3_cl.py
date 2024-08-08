import numpy as np

def univ3_cl(pa, pb, total_value, balance_price, prices):
    """
    Calculates the balances of token X and token Y at different price levels 
    in a Uniswap v3 liquidity pool considering concentrated liquidity.

    Parameters:
    pa (float): The lower bound of the price range.
    pb (float): The upper bound of the price range.
    total_value (float): The total value in USD of both tokens combined.
    balance_price (float): The price at which x * price = y initially.
    prices (np.array): The price levels to compute balances for.

    Returns:
    tuple: (results, geometric_mean)
        results (np.array): An array where each row contains [price, token_X_balance, token_Y_balance, total_value, il_percentage].
        geometric_mean (float): The geometric mean of pa and pb.
    """
    sqrt_pa, sqrt_pb, sqrt_balance_price = np.sqrt([pa, pb, balance_price])
    initial_y = total_value / 2
    initial_x = initial_y / balance_price
    L = initial_x * sqrt_balance_price * sqrt_pb / (sqrt_pb - sqrt_balance_price)
    sqrt_prices = np.sqrt(prices)
    
    X = np.zeros_like(prices)
    Y = np.zeros_like(prices)
    mask = (prices >= pa) & (prices <= pb)
    X[mask] = L * (sqrt_pb - sqrt_prices[mask]) / (sqrt_prices[mask] * sqrt_pb)
    Y[mask] = L * (sqrt_prices[mask] - sqrt_pa)
    X[prices < pa] = L * (sqrt_pb - sqrt_pa) / (sqrt_pa * sqrt_pb)
    Y[prices > pb] = L * (sqrt_pb - sqrt_pa)
    
    total_values = X * prices + Y
    hodl_value = initial_x * prices + initial_y
    il_percentage = (total_values - hodl_value) / hodl_value * 100
    
    return np.column_stack((prices, X, Y, total_values, il_percentage)), np.sqrt(pa * pb)

def generate_prices_array(pa, pb, balance_price, step_percent=1):
    step_factor = 1 + step_percent / 100
    prices = [pa]
    while prices[-1] * step_factor < pb:
        next_price = prices[-1] * step_factor
        if prices[-1] < balance_price < next_price:
            prices.append(balance_price)
        prices.append(next_price)
    return np.sort(np.unique(np.append(prices, [balance_price, pb])))

def calculate_pool_ranges(balance_price, range_percent):
    factor = np.sqrt(1 + range_percent / 100)
    return balance_price / factor, balance_price * factor



def rebalance_cl(balance_price, range_percent, total_value, step_percent):
    pa, pb = calculate_pool_ranges(balance_price, range_percent)
    prices = generate_prices_array(pa, pb, balance_price, step_percent)
    limit_orders, geometric_mean = univ3_cl(pa, pb, total_value, balance_price, prices)
    return limit_orders