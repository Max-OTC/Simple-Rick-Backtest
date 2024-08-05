import numpy as np
def calculate_liquidity(x, y, px, pa, pb):
    """
    Calculate the liquidity for a given position in a Uniswap V3-style liquidity pool.

    :param x: Amount of asset X
    :param y: Amount of asset Y
    :param px: Current price of X in terms of Y
    :param pa: Lower price bound
    :param pb: Upper price bound
    :return: Calculated liquidity
    """
    sqrt_px = np.sqrt(px)
    sqrt_pa = np.sqrt(pa)
    sqrt_pb = np.sqrt(pb)
    
    if px >= pb:
        return y / (sqrt_pb - sqrt_pa)
    elif px <= pa:
        return x * sqrt_pa * sqrt_pb / (sqrt_pb - sqrt_pa)
    else:
        lx = x * ((sqrt_px * sqrt_pb) / (sqrt_pb - sqrt_px))
        ly = y / (sqrt_px - sqrt_pa)
        return min(lx, ly)

def calculate_amounts(l, px, pa, pb):
    """
    Calculate the amounts of X and Y for a given liquidity and price range.

    :param l: Liquidity
    :param px: Current price of X in terms of Y
    :param pa: Lower price bound
    :param pb: Upper price bound
    :return: Tuple (amount of X, amount of Y)
    """
    sqrt_px = np.sqrt(px)
    sqrt_pa = np.sqrt(pa)
    sqrt_pb = np.sqrt(pb)
    
    if px >= pb:
        return 0, l * (sqrt_pb - sqrt_pa)
    elif px <= pa:
        return l * (sqrt_pb - sqrt_pa) / (sqrt_pa * sqrt_pb), 0
    else:
        x = l * ((sqrt_pb - sqrt_px) / (sqrt_px * sqrt_pb))
        y = l * (sqrt_px - sqrt_pa)
        return x, y