import numpy as np
from x1_x2_balance import calculate_amounts, calculate_liquidity

def optimizer_x1_x2(z, px, pa, pb, pzx, pzy):
    """
    Optimize the position for a given total value z and price range.

    :param z: Total value to allocate
    :param px: Current price of X in terms of Y
    :param pa: Lower price bound
    :param pb: Upper price bound
    :param pzx: Price of X in terms of z
    :param pzy: Price of Y in terms of z
    :return: Tuple (amount of X, amount of Y)
    """
    # Step 1: Calculate the ratio of x to y using calculate_amounts
    x_amount = z / 2 / pzx
    y_amount = z / 2 / pzy

    l = calculate_liquidity(x_amount, y_amount, px, pa, pb)
    x_ratio, y_ratio = calculate_amounts(l, px, pa, pb)
    
    if x_ratio == 0:
        return 0, z / pzy
    elif y_ratio == 0:
        return z / pzx, 0
    else:
        print( x_amount, y_amount,  x_ratio  * px, x_ratio, y_ratio, px)
        ratio = ( x_ratio  * px )/ ( y_ratio )
        print("ratio", ratio)
        x_amount = x_amount * ratio
        y_amount = y_amount * ratio


        return x_amount, y_amount
    
    return x_amount, y_amount

def test_optimizer_x1_x2():
    """
    Test the optimizer_x1_x2 function for various scenarios.
    """
    z = 10000  # Total value to allocate
    pzx = 2000  # Price of X in terms of z
    pzy = 1     # Price of Y in terms of z

    # Test case 1: Price within the range
    pa, pb, px = 1800, 2200, 2000
    print("\nTest 1 (Price within range):")
    x, y = optimizer_x1_x2(z, px, pa, pb, pzx, pzy)
    print(f"Optimal X: {x:.6f}, Optimal Y: {y:.6f}")

    # Test case 2: Price at lower boundary
    px = pa
    print("\nTest 2 (Price at lower boundary):")
    x, y = optimizer_x1_x2(z, px, pa, pb, pzx, pzy)
    print(f"Optimal X: {x:.6f}, Optimal Y: {y:.6f}")

    # Test case 3: Price at upper boundary
    px = pb
    print("\nTest 3 (Price at upper boundary):")
    x, y = optimizer_x1_x2(z, px, pa, pb, pzx, pzy)
    print(f"Optimal X: {x:.6f}, Optimal Y: {y:.6f}")

# Run the test
test_optimizer_x1_x2()