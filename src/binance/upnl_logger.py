# trading_functions.py

import csv
from datetime import datetime
import src.binance.vars as vars

def reset_log_file():
    with open(vars.CSV_FILENAME, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Timestamp', 'Long', 'Short', 'Avg Entry Price', 'USD Balance', 'Price'])

# print upnl each 10 minutes of the simulation
def upnl_logger(time):
    if time % 600000 == 0:        
        # Log to CSV file
        with open(vars.CSV_FILENAME, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([time, vars.long, vars.short, vars.avg_entry_price, vars.usd_balance, vars.last_tick_price])
    vars.last_time = time
