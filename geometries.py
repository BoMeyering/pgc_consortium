from geopy.distance import geodesic
import numpy as np

top_left = (38.762673, -97.571776)
top_right = (38.762661, -97.570070)
bottom_left = (38.761811, -97.571767)
bottom_right = (38.761806, -97.570046)

M = 17
N = 37

def interpolate(start_point, end_point, num_points):
    latitudes = np.linspace(start_point[0], end_point[0], num_points).tolist()
    longitudes = np.linspace(start_point[1], end_point[1], num_points).tolist()

    return latitudes, longitudes

left_lat, left_long = interpolate(top_left, bottom_left, M)
right_lat, right_long = interpolate(top_right, bottom_right, M)

grid = []
for i in range(M):
    # print((left_lat[i], left_long[i]))
    # print((right_lat[i], right_long[i]))
    row_lat, row_long = interpolate((left_lat[i], left_long[i]), (right_lat[i], right_long[i]), N)

    grid.append(list(zip(row_lat, row_long)))

print(grid)
with open('points.csv', 'w') as f:
    f.write("lat,long\n")
    for row in range(M):
        for col in range(N):
            print(grid[row][col])
            lat, long = grid[row][col]
            f.writelines(f"{lat},{long}\n")

