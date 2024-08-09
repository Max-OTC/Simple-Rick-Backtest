import numpy as np
import os
from datetime import datetime, timedelta
import src.vars as vars

def load_binance_csv_data(csv_path):
    try:
        return np.loadtxt(csv_path, delimiter=',', dtype=np.float64)
    except Exception as e:
        print(f"Error reading Binance file {csv_path}: {e}")
        return None

data_cache = {}
date_list = None
current_date_index = 0
current_data = None

def initialize_date_range():
    global date_list
    start = datetime.strptime(vars.simulation_start_day, "%Y%m%d")
    end = datetime.strptime(vars.simulation_end_day, "%Y%m%d")
    date_list = [(start + timedelta(days=i)).strftime("%Y%m%d") for i in range((end - start).days + 1)]

def get_next_binance_tick(last_time):
    global data_cache, date_list, current_date_index, current_data

    if date_list is None:
        initialize_date_range()

    while current_date_index < len(date_list):
        current_day = date_list[current_date_index]
        csv_path = f"data/binance/{vars.binance_pair}/{current_day}.csv"

        if current_data is None:
            if csv_path not in data_cache:
                data = load_binance_csv_data(csv_path)
                if data is None:
                    current_date_index += 1
                    continue
                data_cache[csv_path] = data
            current_data = data_cache[csv_path]

        binance_mask = current_data[:, 0] > last_time
        if np.any(binance_mask):
            binance_idx = np.argmax(binance_mask)
            new_time = current_data[binance_idx, 0]
            return current_data[binance_idx, 4], new_time

        current_date_index += 1
        current_data = None

    print("Simulation end")
    return None, None