import pandas as pd

# Load the CSV file
final_df = pd.read_csv('Data/merged_output4(final_one).csv')

# Drop rows without a company name
final_df.dropna(subset=['company_name'], inplace=True)

# Dropping records with "outofbusiness_status-2" set to specific statuses
final_df = final_df[~final_df['outofbusiness_status-2'].isin(["Believed to be Out of Business", "Confirmed to be Out of Business"])]

# Selecting and renaming the desired columns
desired_columns = ['firm_id', 'company_name', 'address_1', 'city', 'state', 'zip', 'phone', 'email', 'url']
final_df = final_df[desired_columns]
final_df.rename(columns={'address_1': 'address'}, inplace=True)

# Normalizing Zip Codes to ensure they are properly formatted as a five-digit string
final_df['zip'] = final_df['zip'].apply(lambda x: '{:05}'.format(int(x)) if pd.notnull(x) else None)

# Phone Number Formatting to ensure consistency
final_df['phone'] = final_df['phone'].apply(lambda x: '{:010}'.format(int(float(x))) if pd.notnull(x) else None)

# Dropping Duplicate Entries based on 'company_name' and 'address'
final_df.drop_duplicates(subset=['company_name', 'address'], inplace=True)

# Saving the cleaned and normalized DataFrame to a new CSV file
final_df.to_csv('Data/cleaned_and_normalized_data.csv', index=False)

print(final_df.head())
