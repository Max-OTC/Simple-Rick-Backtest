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

long = 0
short = 0
avg_entry_price = 0
usd_balance = 100000
fee = 0.00075

CSV_FILENAME = "./src/upnl_log.csv"

last_time = 0
last_10_minutes = 0
limit_order_list = {}
last_tick_price = 0
