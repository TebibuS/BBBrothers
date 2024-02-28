import pandas as pd

# Load the CSV file
file_path = 'Data/sample_file1.csv'
data = pd.read_csv(file_path)

# 1. Handling Missing Values
data['address_2'].fillna('', inplace=True)

# 3. Invalid or Inconsistent Zip Codes
data['zip'] = data['zip'].apply(lambda x: f"{int(x):05}" if pd.notnull(x) else None)

# 4. Phone Number Formatting
data['phone'] = data['phone'].apply(lambda x: f"{x:010.0f}" if pd.notnull(x) else None)

# 6. Duplicate Entries
data.drop_duplicates(subset=['company_name', 'address_1'], inplace=True)

# 7. Address Cleaning (Merge 'address_1' and 'address_2')
data['full_address'] = data['address_1'].str.strip() + " " + data['address_2'].str.strip()
data.drop(['address_1', 'address_2'], axis=1, inplace=True)

# 10. Handling PO Boxes in Addresses
data['full_address'] = data['full_address'].str.replace(r'(?i)\bP\.?O\.? Box\b', 'PO Box', regex=True)

# Display the first few rows of the cleaned dataframe to verify changes
column_order = ['ID', 'firm_id', 'company_name', 'condensed_name', 'main', 'legal', 'full_address',
                'city', 'state', 'zip', 'zip_4', 'phone', 'email', 'url']

# Reorder the dataframe columns
data = data[column_order]
print(data.head())
cleaned_file_path = 'Data/cleaned_sample_file1.csv'

# Save the cleaned dataframe to a new CSV file
data.to_csv(cleaned_file_path, index=False)
