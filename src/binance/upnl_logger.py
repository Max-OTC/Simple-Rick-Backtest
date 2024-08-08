# trading_functions.py

import csv
from datetime import datetime
import src.binance.vars as vars

def reset_log_file():
    with open(vars.CSV_FILENAME, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Timestamp', 'Long', 'Short', 'Avg Entry Price', 'USD Balance', 'Price', 'Onchain Pnl', 'Total Fees'])


# print upnl each 10 minutes of the simulation
def upnl_logger(time):
    if time % 600000 == 0:        
        # Log to CSV file
        with open(vars.CSV_FILENAME, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([
                int(time/1000),
                round(vars.long, 2),
                round(vars.short, 2),
                int(vars.avg_entry_price),
                int(vars.usd_balance),
                int(vars.last_tick_price),
                int(vars.onchain_pnl),
                int(vars.total_fees)
            ])
    vars.last_time = int(time)