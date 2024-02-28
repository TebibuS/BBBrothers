import pandas as pd
from tqdm import tqdm  # Import tqdm

def merge_specific_columns_from_multiple_csv(file_info, common_column, output_file):
    """
    Merges specific columns from multiple CSV files into a single file, with a progress bar.

    Parameters:
    file_info (dict): A dictionary where each key is the path to a CSV file and its value is a list of columns to be selected from that file.
    common_column (str): The name of the column common to all files, used to merge them.
    output_file (str): Path to save the merged CSV file.
    """
    merged_df = None

    # Wrap the iteration with tqdm for a progress bar
    for file_path, columns in tqdm(file_info.items(), desc="Merging files"):
        # Ensure the common column is included in columns to read
        columns_to_read = list(set(columns + [common_column]))
        df = pd.read_csv(file_path, usecols=columns_to_read, nrows=20)

        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on=common_column, how='outer')

    # Save the merged dataframe to a new CSV file
    merged_df.to_csv(output_file, index=False)
    print(f"Merged file saved as {output_file}")


COMPANY_NAMES_COLUMS = ['ID', 'firm_id', 'company_name', 'condensed_name', 'main', 'legal']
ADDRESS_COLUMS = ['ID', 'address_1', 'address_2', 'city', 'state', 'zip', 'zip_4']
PHONE_COLUMS = ['ID', 'phone']
EMAIL_COLUMS = ['ID', 'email']
URL_COLUMS = ['ID', 'url']
    


file_info = {
    'Data/tblfirms_firm_companyname.csv': COMPANY_NAMES_COLUMS,
    'Data/tblfirms_firm_address.csv': ADDRESS_COLUMS,
    'Data/tblfirms_firm_phone.csv': PHONE_COLUMS,
    'Data/tblfirms_firm_email.csv': EMAIL_COLUMS,
    'Data/tblfirms_firm_url.csv': URL_COLUMS
}
merge_specific_columns_from_multiple_csv(file_info, 'ID', 'Data/sample_file1.csv')
