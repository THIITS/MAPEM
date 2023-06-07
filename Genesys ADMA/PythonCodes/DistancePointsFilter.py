import pandas as pd
import math
import simplekml

# Read the Excel file
df = pd.read_excel('/home/gokulnath/Downloads/localization/rosoutput.xlsx')

# Calculate the distance between two coordinate points using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Radius of the Earth in meters

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

# Sort alternative points at approximately 20 meters
sorted_points = []
serial_numbers = []
coordinates = []  # List to store combined coordinate values
prev_lat = df.iloc[0]['fGPSLatAbs']
prev_lon = df.iloc[0]['fGPSLonAbs']
sorted_points.append((prev_lat, prev_lon))
serial_numbers.append(1)
coordinates.append(f"{prev_lat} {prev_lon}")

for index, row in df.iterrows():
    curr_lat = row['fGPSLatAbs']
    curr_lon = row['fGPSLonAbs']
    distance = calculate_distance(prev_lat, prev_lon, curr_lat, curr_lon)

    if distance >= 20:  # Adjust the threshold as needed
        sorted_points.append((curr_lat, curr_lon))
        prev_lat = curr_lat
        prev_lon = curr_lon
        serial_numbers.append(len(sorted_points))
        coordinates.append(f"{curr_lat} {curr_lon}")

# Create a new DataFrame with the sorted points, serial numbers, and combined coordinates
new_df = pd.DataFrame({'Serial Number': serial_numbers,
                       'fGPSLatAbs': [point[0] for point in sorted_points],
                       'fGPSLonAbs': [point[1] for point in sorted_points],
                       'Coordinates': coordinates})

# Write the new DataFrame to an Excel file
new_df.to_excel('/home/gokulnath/Downloads/localization/nodes.xlsx', index=False)

# Create a new KML object
kml = simplekml.Kml()

# Create a KML folder for the points
folder = kml.newfolder(name='Sorted Points')

# Add the sorted points to the KML folder with serial number labels
for i, point in enumerate(sorted_points):
    pnt = folder.newpoint(coords=[(point[1], point[0])])
    pnt.name = str(serial_numbers[i])

# Save the KML file
kml.save('/home/gokulnath/Downloads/localization/nodes.kml')
