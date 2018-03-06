import numpy as np
import warnings
# Takes in all the points
# Takes in the number of points to be used to track the ball
warnings.simplefilter('ignore', np.RankWarning)

def prediction(tracking_points, n):
	if len(tracking_points) < n :
		return None, None, None
    
	x_array = []
	y_array = []

	for item in tracking_points:
		x_array.append(item[0])
		y_array.append(item[1])
               
	m, c = np.polyfit(x_array, y_array, 1)
    
	if x_array[-1:] > x_array[-2:-1]:
		direction = 1
	else:
		direction = -1
    
	return m, c, direction
    
