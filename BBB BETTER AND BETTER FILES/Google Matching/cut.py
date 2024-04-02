import os
import pandas as pd

# Set files to be cut
files = ['cleaned_and_normalized_data2.csv']
directory = "/Users/pedro/Desktop/BBB/Data"
# Loop through every file in the directory
for file in files:
    file_path = os.path.join(directory, file)
    # Read the first 100 rows of the CSV file
    df = pd.read_csv(file_path, nrows=3)
    # Construct the output filename
    output_filename = file.replace(".csv", "_first3.csv")
    output_path = os.path.join(directory, output_filename)
    # Write the first 100 rows to the new file
    df.to_csv(output_path, index=False)
    print(f"Processed {file} and saved first 3 rows to {output_filename}")
