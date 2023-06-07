import rosbag
import pandas as pd
import simplekml

# Specify the path to the ROS bag file
bag_path = '/home/gokulnath/Downloads/localization/roundabout2_2023-06-02-14-29-59.bag'
excel_path = '/home/gokulnath/Downloads/localization/rosoutput.xlsx'
kml_path = '/home/gokulnath/Downloads/localization/rosoutput.kml'

def extract_adma_data(bag_path, excel_path):
    # Open the ROS bag
    bag = rosbag.Bag(bag_path)

    # Create lists to store the desired values
    fGPSLatAbs_list = []
    fGPSLonAbs_list = []

    # Extract messages from the adma_data topic
    topic_name = '/adma_connect/adma_data'
    for topic, msg, t in bag.read_messages(topics=[topic_name]):
        # Extract the desired values and append them to the respective lists
        fGPSLatAbs_list.append(msg.fGPSLatAbs)
        fGPSLonAbs_list.append(msg.fGPSLonAbs)

    # Create a DataFrame from the lists
    df = pd.DataFrame({
        'fGPSLatAbs': fGPSLatAbs_list,
        'fGPSLonAbs': fGPSLonAbs_list
    })

    # Save the DataFrame to an Excel file
    df.to_excel(excel_path, index=False)

    # Close the bag file
    bag.close()

def convert_excel_to_kml(excel_path, kml_path):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_path)

    # Create a KML object
    kml = simplekml.Kml()

    # Iterate over the rows in the DataFrame
    for index, row in df.iterrows():
        # Extract the latitude and longitude values
        lat = row['fGPSLatAbs']
        lon = row['fGPSLonAbs']

        # Create a KML point at the latitude and longitude
        point = kml.newpoint(name=f'Point {index+1}', coords=[(lon, lat)])

    # Save the KML file
    kml.save(kml_path)

# Call the function to extract adma_data messages and save the desired values to an Excel file
extract_adma_data(bag_path, excel_path)

# Call the function to convert the Excel file to KML
convert_excel_to_kml(excel_path, kml_path)
