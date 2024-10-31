from geopy.distance import geodesic
import numpy as np
import polars as pl


import os
import django
import json

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Setup Django
django.setup()

top_left = (38.762673, -97.571776)
top_right = (38.762661, -97.570070)
bottom_left = (38.761811, -97.571767)
bottom_right = (38.761806, -97.570046)

M = 16
N = 37

# M = 10
# N = 15

points = []

def interpolate(start_point, end_point, num_points):
    latitudes = np.linspace(start_point[0], end_point[0], num_points).tolist()
    longitudes = np.linspace(start_point[1], end_point[1], num_points).tolist()

    return latitudes, longitudes

left_lat, left_long = interpolate(top_left, bottom_left, M)
right_lat, right_long = interpolate(top_right, bottom_right, M)

grid = []
for i in range(M):
    row_lat, row_long = interpolate((left_lat[i], left_long[i]), (right_lat[i], right_long[i]), N)
    grid.append(list(zip(row_lat, row_long)))

geojson = {
    "type": "FeatureCollection",
    "features": []
}

for row in range(M-1):
    for col in range(N-1):
        points.append([row, col, grid[row][col][0], grid[row][col][1]])
        tl = [grid[row][col][1], grid[row][col][0]]
        bl = [grid[row+1][col][1], grid[row+1][col][0]]
        br = [grid[row+1][col+1][1], grid[row+1][col+1][0]]
        tr = [grid[row][col+1][1], grid[row][col+1][0]]
        
        feature = {
            "type": "Feature",
            "id": f"{row}_{col}",
            "geometry": {
                "coordinates": [
                    [
                        tl,
                        bl, 
                        br,
                        tr,
                        tl
                    ]
                ],
                "type": "Polygon"
            },
            "properties": {}
        }

        geojson['features'].append(feature)

df = pl.DataFrame(points, schema=['row', 'col', 'lat', 'long'], orient='row')
# print(df)

file_path = os.path.expanduser('~/Desktop/trial.geojson')
with open(file_path, 'w') as f:
    json_data = json.dump(geojson, f)


with open('points.csv', 'w') as f:
    f.write("lat,long\n")
    for row in range(M):
        for col in range(N):
            lat, long = grid[row][col]
            f.writelines(f"{lat},{long}\n")





r, c = 10, 24
tl = df.filter(row=r-1, col=c-1)
tr = df.filter(row=r-1, col=c)
bl = df.filter(row=r, col=c-1)
br = df.filter(row=r, col=c)
# print(tl)
# print(tr)
# print(br)
# print(bl)


import geopandas

gdf = geopandas.read_file(file_path)

print(gdf)
gdf.set_index("id")

print(gdf.area)
print(gdf.crs['units'])