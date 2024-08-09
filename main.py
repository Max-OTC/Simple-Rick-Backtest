from src.orders import process_next_tick
import src.vars as vars
from src.upnl_logger import reset_log_file

def run_simulation():
    reset_log_file()
    vars.last_time = 0

    while True:
        if not process_next_tick():
            break

    print("Simulation complete")

if __name__ == "__main__":
    run_simulation()