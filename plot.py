import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import csv
from datetime import datetime

def load_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip the header
        data = np.array(list(reader), dtype=float)
    return header, data

def plot_data(csv_file):
    header, data = load_csv(csv_file)
    
    # Convert timestamp to datetime
    timestamps = [datetime.fromtimestamp(ts/1000) for ts in data[:, 0]]

    # Create the plot
    fig, axs = plt.subplots(5, 1, figsize=(12, 15), sharex=True)
    fig.suptitle('Trading Data Over Time')

    # Plot Long positions
    axs[0].plot(timestamps, data[:, 1], color='blue')
    axs[0].set_ylabel('Long')

    # Plot Short positions
    axs[1].plot(timestamps, data[:, 2], color='red')
    axs[1].set_ylabel('Short')

    # Plot Average Entry Price
    axs[2].plot(timestamps, data[:, 3], color='green')
    axs[2].set_ylabel('Avg Entry Price')

    # Plot USD Balance
    axs[3].plot(timestamps, data[:, 4], color='purple')
    axs[3].set_ylabel('USD Balance')

    # Calculate and plot the total position (Long - Short)
    total_position = data[:, 1] - data[:, 2]
    axs[4].plot(timestamps, total_position, color='orange')
    axs[4].set_ylabel('Total Position')

    # Format x-axis
    for ax in axs:
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))
        ax.grid(True)

    plt.xlabel('Timestamp')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as a PNG file
    plt.savefig('trading_data_plot.png')
    print("Plot saved as trading_data_plot.png")

    # Show the plot
    plt.show()

if __name__ == "__main__":
    plot_data('upnl_log.csv')