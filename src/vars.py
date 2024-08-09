

binance_pair = 'ETHUSDT'
univ3_pair = 'USDCWETH'

simulation_start_day = "20240101"  # YYYYMMDD format
simulation_end_day = "20240802"    # YYYYMMDD format
simulation_current_day = simulation_start_day

CSV_FILENAME = "./src/upnl_log.csv"

######## prices var

last_px = 0
current_px = 0
limit_orders = []

######## fees
binance_fee = 0
uniswap_fee = 0.003

######## cumulative pnl
uniswap_pnl = 0
uni_rebalance_number = 0
uni_rebalance_volume = 0
cl_total_fees = 0

binance_pnl = 0
binance_rebalance_number = 0
binance_rebalance_volume = 0


######## univ3 vars
range_percent = 10
total_value = 100000
step_percent = 0.5

current_pa = 0
current_pb = 0
current_total_value = 0
current_balance_price = 0


############ time vars
last_time = 0
last_10_minutes = 0


