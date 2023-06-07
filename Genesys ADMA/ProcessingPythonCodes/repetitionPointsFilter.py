import pandas as pd
import math
import simplekml

# Read the Excel file
df = pd.read_excel('/home/gokulnath/Downloads/localization/rosoutput.xlsx')

# Filter out repeating points
filtered_points = []
serial_numbers = []
coordinates = []  # List to store combined coordinate values

for index, row in df.iterrows():
    curr_lat = row['fGPSLatAbs']
    curr_lon = row['fGPSLonAbs']

    if index == 0 or (curr_lat != prev_lat or curr_lon != prev_lon):
        filtered_points.append((curr_lat, curr_lon))
        serial_numbers.append(len(filtered_points))
        coordinates.append(f"{curr_lat} {curr_lon}")

    prev_lat = curr_lat
    prev_lon = curr_lon

# Create a new DataFrame with the filtered points, serial numbers, and combined coordinates
new_df = pd.DataFrame({'Serial Number': serial_numbers,
                       'fGPSLatAbs': [point[0] for point in filtered_points],
                       'fGPSLonAbs': [point[1] for point in filtered_points],
                       'Coordinates': coordinates})

# Write the new DataFrame to an Excel file
new_df.to_excel('/home/gokulnath/Downloads/localization/nodesFilter2.xlsx', index=False)

# Create a new KML object
kml = simplekml.Kml()

# Create a KML folder for the points
folder = kml.newfolder(name='Filtered Points')

# Add the filtered points to the KML folder with serial number labels
for i, point in enumerate(filtered_points):
    pnt = folder.newpoint(coords=[(point[1], point[0])])
    pnt.name = str(serial_numbers[i])

# Save the KML file
kml.save('/home/gokulnath/Downloads/localization/nodesFilter2.kml')
