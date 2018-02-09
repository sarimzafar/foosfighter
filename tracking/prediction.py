import numpy as np

# Takes in all the points
# Takes in the number of points to be used to track the ball


def prediction(tracking_points, sampling_count, n):
    if sampling_count > len(tracking_points):
        return None, None, None

    fit_data = tracking_points[-sampling_count:]
    x_array = []
    y_array = []

    for item in fit_data[::-1]:
        if item is None:
            continue

        if n > 0:
            x_array.append(item[0])
            y_array.append(item[1])
            n = n-1
    
    if len(x_array) < 2 or len(y_array) < 2:
        return None, None, None

    m, c = np.polyfit(x_array, y_array, 1)
    
    if x_array[len(x_array)-1] > x_array[len(x_array)-2]:
        direction = 1
    else:
        direction = -1
    
    return m, c, direction
    
