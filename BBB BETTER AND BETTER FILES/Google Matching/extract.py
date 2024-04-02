import os
import pandas as pd

# Set the directory where your CSV files are located
directory = "/Users/pedro/Desktop/BBB_data"

# Loop through every file in the directory
for filename in os.listdir(directory):
    # Check if the file is a CSV
    if filename.endswith(".csv"):
        # Construct the full file path
        file_path = os.path.join(directory, filename)
        # Read the first 100 rows of the CSV file
        df = pd.read_csv(file_path, nrows=100)
        # Construct the output filename
        output_filename = filename.replace(".csv", "_first100.csv")
        output_path = os.path.join(directory, output_filename)
        # Write the first 100 rows to the new file
        df.to_csv(output_path, index=False)
        print(f"Processed {filename} and saved first 100 rows to {output_filename}")
