# global_vars.py

class LimitOrder:
    def __init__(self, amount, isLong):
        self.amount = amount
        self.isLong = isLong

binance_pair = 'ETHUSDT'
univ3_pair = 'USDCWETH'

simulation_start_day = "20240101"  # YYYYMMDD format
simulation_end_day = "20240802"    # YYYYMMDD format
simulation_current_day = simulation_start_day

CSV_FILENAME = "./src/upnl_log.csv"

############ Binance FUtures
long = 0
short = 0
avg_entry_price = 0
usd_balance = 100000
fee = 0.00075

############ UniV3
px = 0
py = 1
x = 0
y = 0
tn = 0
pa = 0
pb = 0
step = 0.001
cl_range = 0.05
onchain_balance_usd = 100000
borrow_haircut = 0.8
onchain_pnl = 0
total_fees = 0


############ Do not modify
last_time = 0
last_10_minutes = 0
limit_order_list = {}
last_tick_price = 0
