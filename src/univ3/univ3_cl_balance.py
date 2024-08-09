import numpy as np

def univ3_cl_balance(pa, pb, total_value, balance_price, px):
    """
    Calculates the number of token 1 and token 2 at a specific price level
    in a Uniswap v3 liquidity pool considering concentrated liquidity.

    Parameters:
    pa (float): The lower bound of the price range.
    pb (float): The upper bound of the price range.
    total_value (float): The total value in USD of both tokens combined.
    balance_price (float): The price at which x * price = y initially.
    px (float): The specific price level to compute token amounts for.

    Returns:
    tuple: (token_1, token_2)
        token_1 (float): The amount of token 1 (X) at the given price level.
        token_2 (float): The amount of token 2 (Y) at the given price level.
    """
    sqrt_pa, sqrt_pb, sqrt_balance_price = np.sqrt([pa, pb, balance_price])
    initial_y = total_value / 2
    initial_x = initial_y / balance_price
    L = initial_x * sqrt_balance_price * sqrt_pb / (sqrt_pb - sqrt_balance_price)
    
    sqrt_px = np.sqrt(px)
    
    if px < pa:
        token_1 = L * (sqrt_pb - sqrt_pa) / (sqrt_pa * sqrt_pb)
        token_2 = 0
    elif px > pb:
        token_1 = 0
        token_2 = L * (sqrt_pb - sqrt_pa)
    else:
        token_1 = L * (sqrt_pb - sqrt_px) / (sqrt_px * sqrt_pb)
        token_2 = L * (sqrt_px - sqrt_pa)
    
    return token_1, token_2
def test_univ3_cl_balance():
    # Test case 1: Price at the lower bound
    pa, pb = 1267, 1774
    total_value = 10000
    balance_price = 1500
    px = 1000
    token_1, token_2 = univ3_cl_balance(pa, pb, total_value, balance_price, px)
    print(f"Test 1 - Price at lower bound: Token 1 = {token_1:.2f}, Token 2 = {token_2:.2f}")

    # Test case 2: Price at the upper bound
    px = 2000
    token_1, token_2 = univ3_cl_balance(pa, pb, total_value, balance_price, px)
    print(f"Test 2 - Price at upper bound: Token 1 = {token_1:.2f}, Token 2 = {token_2:.2f}")

    # Test case 3: Price at the balance price
    px = 1500
    token_1, token_2 = univ3_cl_balance(pa, pb, total_value, balance_price, px)
    print(f"Test 3 - Price at balance price: Token 1 = {token_1:.2f}, Token 2 = {token_2:.2f}")

    # Test case 4: Price below the lower bound
    px = 800
    token_1, token_2 = univ3_cl_balance(pa, pb, total_value, balance_price, px)
    print(f"Test 4 - Price below lower bound: Token 1 = {token_1:.2f}, Token 2 = {token_2:.2f}")

    # Test case 5: Price above the upper bound
    px = 2200
    token_1, token_2 = univ3_cl_balance(pa, pb, total_value, balance_price, px)
    print(f"Test 5 - Price above upper bound: Token 1 = {token_1:.2f}, Token 2 = {token_2:.2f}")

#test_univ3_cl_balance()