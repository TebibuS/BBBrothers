import pandas as pd
import requests
import time
from urllib.parse import quote_plus
from fuzzywuzzy import fuzz  # Fuzzy matching of strings
from dotenv import load_dotenv
import os

# Helper functions for normalization
def normalize_phone_number(phone):
    """Strip non-numeric characters and country code if present."""
    return ''.join(filter(str.isdigit, phone))

def fuzzy_name_match(name1, name2, threshold=90):
    """Check if two names are similar using fuzzy matching."""
    return fuzz.partial_ratio(name1.lower(), name2.lower()) >= threshold

# Constants
ENV_PATH = ".env"
load_dotenv(dotenv_path=ENV_PATH)
API_KEY = os.getenv("GOOFLE_PLACES_TOKEN")  # Replace with your actual API key
BATCH_SIZE = 10  # Adjust based on your quota and rate limits

# Function to safely make API requests
def safe_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error making request: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception during request: {e}")
    return None

# Function to rate limit requests
def rate_limited_request(url):
    time.sleep(1)  # Simple fixed delay between requests
    return safe_request(url)

# Load CSV
df = pd.read_csv('/mnt/data/cleaned_sample_file1.csv')

# Prepare DataFrame for updated information
columns = ['ID', 'company_name', 'needs_update', 'google_name', 'google_phone', 'google_address']
updated_df = pd.DataFrame(columns=columns)

# Process in batches
for start in range(0, len(df), BATCH_SIZE):
    end = start + BATCH_SIZE
    batch = df[start:end]

    for index, row in batch.iterrows():
        business_name = quote_plus(row['company_name'] + ' ' + row['city'] + ', ' + row['state'])
        search_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={business_name}&inputtype=textquery&fields=place_id&key={API_KEY}"
        
        search_response = rate_limited_request(search_url)
        if search_response and search_response['candidates']:
            place_id = search_response['candidates'][0]['place_id']
            details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_phone_number,formatted_address&key={API_KEY}"
            
            details_response = rate_limited_request(details_url)
            if details_response and 'result' in details_response:
                details = details_response['result']
                
                # Enhanced comparison logic
                name_match = fuzzy_name_match(row['company_name'], details.get('name', ''))
                phone_match = normalize_phone_number(str(row['phone'])) == normalize_phone_number(details.get('formatted_phone_number', ''))
                # Assuming address normalization function exists
                # address_match = normalize_address(row['full_address']) == normalize_address(details.get('formatted_address', ''))
                
                needs_update = not (name_match and phone_match)  # Expand logic for address_match etc.
                
                updated_info = {
                    'ID': row['ID'],
                    'company_name': row['company_name'],
                    'needs_update': needs_update,
                    'google_name': details.get('name', ''),
                    'google_phone': details.get('formatted_phone_number', ''),
                    'google_address': details.get('formatted_address', '')
                }
                updated_df = pd.concat([updated_df, pd.DataFrame([updated_info])], ignore_index=True)

# Optimize DataFrame memory usage before saving
updated_df = updated_df.convert_dtypes()

# Save updated information to a new CSV file
output_file_path = '/mnt/data/updated_business_info_enhanced.csv'
updated_df.to_csv(output_file_path, index=False)
print(f"Output file saved to {output_file_path}")
