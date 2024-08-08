import numpy as np

def get_cl_deltas(results):
    """
    Calculates the delta between successive token balances for each price level,
    including deltas going up and down for both tokens.
    Returns a NumPy array containing the price and deltas.
    """
    results_array = np.array(results)
    n = len(results_array)
    
    prices = results_array[:, 0]
    x = results_array[:, 1]
    y = results_array[:, 2]
    
    delta_up_x = np.zeros(n)
    delta_up_y = np.zeros(n)
    delta_down_x = np.zeros(n)
    delta_down_y = np.zeros(n)
    
    delta_up_x[1:] = x[1:] - x[:-1]
    delta_up_y[1:] = y[1:] - y[:-1]
    delta_down_x[:-1] = -(x[1:] - x[:-1])
    delta_down_y[:-1] = -(y[1:] - y[:-1])
    
    return np.column_stack((prices, delta_up_x, delta_up_y, delta_down_x, delta_down_y))

