import csv
from datetime import datetime, timedelta
import src.binance.vars as vars
import src.univ3.univ3_fee_sim


# Compute cumluative fees and set into a csv each hours
def compute_and_log_fees():
    start_time = datetime.fromtimestamp(vars.simulation_start_time / 1000)
    end_time = datetime.fromtimestamp(vars.simulation_end_time / 1000)
    current_time = start_time
    next_log_time = current_time + timedelta(hours=1)
    cumulative_fees = 0

    with open('fee_log.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Timestamp', 'Cumulative Fees'])

        last_time = vars.simulation_start_time
        while current_time < end_time:
            price = 0
            new_time = 0

            # Compute fees here (placeholder)
            fees = 0  # Replace with actual fee computation

            cumulative_fees += fees
            current_time = datetime.fromtimestamp(new_time / 1000)

            if current_time >= next_log_time:
                csvwriter.writerow([next_log_time.strftime('%Y-%m-%d %H:%M:%S'), cumulative_fees])
                next_log_time += timedelta(hours=1)

            last_time = new_time

    print("Fee computation and logging completed.")

if __name__ == "__main__":
    compute_and_log_fees()