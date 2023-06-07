import rosbag
import pandas as pd
import simplekml
import glob

# Specify the path to the folder containing the ROS bag files
bag_folder = '/home/gokulnath/Downloads/localization/rosbagFiles/'
excel_path = '/home/gokulnath/Downloads/localization/rosoutput.xlsx'
kml_path = '/home/gokulnath/Downloads/localization/rosoutput.kml'

def extract_adma_data(bag_path):
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

    # Close the bag file
    bag.close()

    return df

def convert_excel_to_kml(df, kml):
    # Iterate over the rows in the DataFrame
    for index, row in df.iterrows():
        # Extract the latitude and longitude values
        lat = row['fGPSLatAbs']
        lon = row['fGPSLonAbs']

        # Create a KML point at the latitude and longitude
        point = kml.newpoint(name=f'Point {index+1}', coords=[(lon, lat)])

def process_bag_files(bag_folder, excel_path, kml_path):
    # Get a list of bag files in the folder
    bag_files = glob.glob(bag_folder + '*.bag')

    # Create an empty list to store the DataFrames
    df_list = []

    # Create a KML object
    kml = simplekml.Kml()

    # Process each bag file
    for bag_file in bag_files:
        print(f"Processing bag file: {bag_file}")

        # Extract data from the bag file
        df = extract_adma_data(bag_file)

        # Append the DataFrame to the list
        df_list.append(df)

        # Convert the current dataframe to KML
        convert_excel_to_kml(df, kml)

    # Concatenate the DataFrames
    combined_df = pd.concat(df_list, ignore_index=True)

    # Save the combined DataFrame to an Excel file
    combined_df.to_excel(excel_path, index=False)

    # Save the KML file
    kml.save(kml_path)

# Call the function to process the bag files and generate the combined Excel and KML files
process_bag_files(bag_folder, excel_path, kml_path)
