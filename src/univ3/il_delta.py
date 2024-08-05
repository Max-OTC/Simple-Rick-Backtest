import numpy as np
from x1_x2_balance import calculate_amounts, calculate_liquidity
from x1_x2_optimizer import optimizer_x1_x2

def il_delta(x, y, px0, px1, pa, pb):
    l0 = calculate_liquidity(x, y, px0, pa, pb)
    print("l0:", l0)

    x0, y0 = calculate_amounts(l0, px0, pa, pb)
    print(x0, y0)

    l1 = calculate_liquidity(x, y, px1, pa, pb)
    print("l1:", l1)

    x1, y1 = calculate_amounts(l1, px1, pa, pb)
    print(x1, y1)

    dx = x0 - x1
    dy = y0 - y1

    print(f"Price: {px0:.2f} -> {px1:.2f}")
    print(f"Token1: {x0:.4f} -> {x1:.4f}, Delta: {dx:.4f}")
    print(f"Token2: {y0:.4f} -> {y1:.4f}, Delta: {dy:.4f}")

    return dx, dy


z = 10000
px = 2000
pa = 1800
pb = 2200
pzx = 1
pzy = 2000

x, y = optimizer_x1_x2(z, px, pa, pb, pzx, pzy)
print("x,y :", x, y)
px0 = px
step = 0.1
px1 = px0 * (1 + step)
il_delta(x, y, 1/px0, 1/px1, pa, pb)