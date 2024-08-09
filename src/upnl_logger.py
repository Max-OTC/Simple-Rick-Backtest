# trading_functions.py

import csv
from datetime import datetime
import src.vars as vars

def reset_log_file():
    with open(vars.CSV_FILENAME, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Timestamp', 'Price', 'Binance Pnl', 'Uniswap Pnl', 'Binance Rebalance', 'Univ3 Rebalance', 'Binance Volume', 'Univ3 Volume'])


# print upnl each 10 minutes of the simulation
def upnl_logger(time):
    if time % 600000 == 0:        
        # Log to CSV file
        with open(vars.CSV_FILENAME, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([
                int(time/1000),
                int(vars.current_px),
                round(vars.binance_pnl, 2),
                round(vars.uniswap_pnl, 2),
                int(vars.binance_rebalance_number),
                int(vars.uni_rebalance_number),
                int(vars.binance_rebalance_volume),
                int(vars.uni_rebalance_volume),
            ])
    vars.last_time = int(time)