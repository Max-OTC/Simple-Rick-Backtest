import numpy as np
import os
from datetime import datetime, timedelta
import vars as vars

# Global cache for loaded CSV data
data_cache = {}

def load_csv_data(file_path):
    try:
        return np.loadtxt(file_path, delimiter=',', skiprows=1, usecols=(0,3,4,5,6,7,8,9), dtype=np.float64)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def get_next_univ3_tick(t0, t1):
    dt0 = datetime.fromtimestamp(t0 / 1000)
    dt1 = datetime.fromtimestamp(t1 / 1000)
    
    data_list = []
    
    current_date = dt0.date()
    while current_date <= dt1.date():
        file_path = f"data/univ3/{vars.univ3_pair}/{current_date.strftime('%Y%m%d')}.csv"
        
        if file_path not in data_cache:
            data = load_csv_data(file_path)
            if data is not None:
                data_cache[file_path] = data
        
        if file_path in data_cache:
            data = data_cache[file_path]
            mask = (data[:, 0] >= t0) & (data[:, 0] <= t1)
            filtered_data = data[mask]
            if filtered_data.size > 0:
                data_list.append(filtered_data)
        
        current_date += timedelta(days=1)
    
    if data_list:
        return np.vstack(data_list)
    else:
        return np.array([])

# Test: Getting data between 3:00 and 4:00 on July 4, 2024
test_date = datetime(2024, 7, 4)
test_date2 = datetime(2024, 8, 4)

t0 = int(test_date.replace(hour=3, minute=0, second=0).timestamp() * 1000)
t1 = int(test_date2.replace(hour=4, minute=0, second=0).timestamp() * 1000)

# Set the Uniswap V3 pair for testing
vars.univ3_pair = "USDCWETH"  # Adjust this to match your actual pair

result = get_lines_between_timestamps(t0, t1)
print(f"Number of rows retrieved: {len(result)}")
if len(result) > 0:
    print("First few rows:")
    print(result[:5])
else:
    print("No data found for the specified time range.")