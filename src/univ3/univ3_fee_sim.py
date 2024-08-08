import numpy as np
from decimal import Decimal
import src.binance.vars as vars

def univ3_fee_sim(data):
    fees = univ3_fee_compute(data, vars.pa, vars.pb, vars.px, vars.x, vars.y)
    vars.total_fees += fees

def univ3_fee_compute(univ3_data, pa, pb, px, x, y):
    # Convert the data to a numpy array if it's not already
    if not isinstance(univ3_data, np.ndarray):
        data = np.array(univ3_data)
    else:
        data = univ3_data
    
    # Extract relevant columns
    amount_usd = np.array([Decimal(str(val['AMOUNT_USD'])) for val in data])
    price = np.array([Decimal(str(val['PRICE'])) for val in data])
    fee_tier = np.array([Decimal(str(val['FEE_TIER'])) for val in data])
    liquidity = np.array([Decimal(str(val['LIQUIDITY'])) * Decimal('1e-12') for val in data])  # Adjust liquidity
    
    # Calculate user's liquidity (simplified version)
    user_liquidity = Decimal(str(x)) * Decimal(str(y)).sqrt()
    
    # Create a mask for trades within the price range
    in_range_mask = (price >= Decimal(str(pa))) & (price <= Decimal(str(pb)))
    
    # Calculate fees for trades within the range
    fee_tier_decimal = fee_tier[in_range_mask] / Decimal('1000000')  # Convert basis points to decimal
    trade_volume = amount_usd[in_range_mask]
    existing_liquidity = liquidity[in_range_mask]
    
    fees = fee_tier_decimal * trade_volume * (user_liquidity / (existing_liquidity + user_liquidity))
    
    total_fees = sum(fees)
    
    return total_fees

# Example usage
univ3_data = [
    [1640995220000, 'USDC', 'WETH', 47523.200755, -12.8884296186484981, 47506.98531290466244825164826599057, 3687.28, 194197, 500, 1966685670725897590],
    [1640995220000, 'USDC', 'WETH', 368451.893403, -100.049472154053881679, 368555.0930115048721847536637824242, 3682.70, 194200, 500, 1966685670725897590],
    [1640995220000, 'USDC', 'WETH', 7348.892457, -1.993353935934415093, 7346.96164905827763056597386097239, 3686.70, 194199, 500, 1966685670725897590],
    [1640995265000, 'USDC', 'WETH', -54685.215206, 14.845936081607570259, 54694.4632917732771886980550686387, 3683.51, 194200, 500, 1966685670725897590],
    [1640995283000, 'USDC', 'WETH', -4928.390319, 1.3381875, 4929.64504311265435005161115835641, 3682.88, 194200, 500, 1966685670725897590]
]

# Example position parameters
pa = 3680  # Lower price bound
pb = 3690  # Upper price bound
px = 3685  # Current price
x = 1000   # Amount of token 0
y = 0.271  # Amount of token 1

#total_fees = univ3_fee_sim(univ3_data, pa, pb, px, x, y)
#print(f"Total fees generated: {total_fees}")