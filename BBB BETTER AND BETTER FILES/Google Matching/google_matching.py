from dotenv import load_dotenv
import os
import pandas as pd
import requests
from fuzzywuzzy import fuzz

load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')
#API_KEY = ""
print(API_KEY)

# Function to call Google Places API with error handling
def get_place_details(query):
    search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={API_KEY}"
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    try:
        search_response = requests.get(search_url)
        search_response.raise_for_status()
        search_data = search_response.json()
        if search_data["status"] == "OK":
            # Assume the first result is the most relevant
            place_id = search_data["results"][0]["place_id"]
            
            # Get detailed information, including phone number
            details_params = {
                "place_id": place_id,
                "fields": "name,formatted_address,formatted_phone_number,website",
                "key": API_KEY
            }
            details_response = requests.get(details_url, params=details_params)
            details_response.raise_for_status()
            details_data = details_response.json()
            
            if details_data["status"] == "OK":
                result = details_data["result"]
                result ['place_id'] = place_id
                return result
            else:
                print(f"Details API returned status: {details_data['status']}")
                return None
        else:
            print(f"Search API returned status: {search_data['status']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for query '{query}': {e}")
        return None

# Function to calculate confidence score with weights
def calculate_confidence(company_name, address, phone, api_data):

    company_name_str = str(company_name)
    address_str = str(address)
    api_name_str = str(api_data.get("name", ""))
    api_address_str = str(api_data.get("formatted_address", "").replace(", USA", ""))
    api_phone_str = str(api_data.get("formatted_phone_number", "")).replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    phone_str = str(phone).replace(" ", "").replace("-", "") if phone else ""

    print("Comparing:")
    print(company_name_str)
    print(api_name_str)
    print(address_str)
    print(api_address_str)
    print(phone_str)
    print(api_phone_str)
    
    address_score = fuzz.ratio(address_str, api_address_str)
    phone_score = 100 if str(phone_str) == api_phone_str else 0  # Adjusted to give a full score on match

    address_weight = 0.5
    phone_weight = 0.5

    # Calculate weighted confidence score
    confidence_score = (address_score * address_weight) + (phone_score * phone_weight)
    return confidence_score

# Function to determine outdated reason and update DataFrame
def update_outdated_info(updated_row, confidence_score, api_data, formatted_address):
    outdated_reason = ""
    company_name = str(updated_row["company_name"])
    api_name = str(api_data.get("name", ""))
    address = formatted_address
    api_address = str(api_data.get("formatted_address", "").replace(", USA", ""))
    phone = str(updated_row["phone"]).replace(" ", "").replace("-", "") if updated_row["phone"] else ""
    api_phone = str(api_data.get("formatted_phone_number", "")).replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    api_url = api_data.get("website", "")

    if confidence_score < 80:
        # Check individual discrepancies, now safely converting all comparisons to strings
        if fuzz.ratio(company_name, api_name) < 70:
            outdated_reason += "Name mismatch, "
        if fuzz.ratio(address, api_address) < 80:
            outdated_reason += "Address mismatch, "
        if phone != api_phone:
            outdated_reason += "Phone mismatch, "

        # Remove trailing comma if present
        outdated_reason = outdated_reason.rstrip(", ")

        updated_row["outdated"] = True
        updated_row["outdated_reason"] = outdated_reason
    else:
        # Explicitly mark as not outdated if the conditions are not met
        updated_row["outdated"] = False
        updated_row["outdated_reason"] = "Information current" 

    updated_row["google_name"] = api_name
    updated_row["google_address"] = api_address
    updated_row["google_phone"] = api_phone
    updated_row["google_url"] = api_url
    updated_row["google_place_id"] = api_data.get("place_id", "")

def format_address(address, city, state, zip_code):
    """
    Formats the address by concatenating address, city, state, and zip code.
    Example: '123 Main St, Anytown, CA, 12345'
    """
    return f"{address}, {city}, {state} {zip_code}"

def format_phone_number(phone_str):
    """
    Formats a phone number to remove trailing '.0' and ensures it is a string.
    Args:
        phone_str (str): The phone number as a string.
    Returns:
        str: The formatted phone number.
    """
    # Check if the phone_str is not None and is a string
    if phone_str and isinstance(phone_str, str):
        # If there's a '.0' at the end of the string, remove it
        if phone_str.endswith('.0'):
            return phone_str[:-2]
    return phone_str

def format_zip(zip_str): 
    if zip_str and isinstance(zip_str, str):
        # If there's a '.0' at the end of the string, remove it
        if zip_str.endswith('.0'):
            return zip_str[:-2]
    return zip_str


def check_name_similarity(company_name, api_data):
    api_name_str = str(api_data.get("name", ""))
    name_similarity_score = fuzz.ratio(company_name, api_name_str)
    return name_similarity_score >= 70  # Returns True if names are close enough

# Load business data from CSV
df = pd.read_csv("Data/cleaned_and_normalized_data_first23.csv", dtype={'phone': str, 'zip': str})

df['phone'] = df['phone'].apply(format_phone_number)
df['zip'] = df['zip'].apply(format_zip)
# Create a list to store updated rows
updated_rows = []

# Iterate through each business entry and verify
for index, row in df.iterrows():
    company_name = row["company_name"]
    city = row["city"]
    state = row["state"]
    address = row["address"]
    zip_code = row["zip"]
    phone = row["phone"]
    address = format_address(address, city, state, zip_code)
    print(address)

    # Construct query for Google Places API
    query = f"{company_name} {city}, {state}"

    # Retrieve business information from API
    api_data = get_place_details(query)
    print(api_data)

    # Update row and add to list
    updated_row = row.copy()
    if api_data:
        if check_name_similarity(company_name, api_data):
            confidence_score = calculate_confidence(company_name, address, phone, api_data)
            updated_row["confidence_score"] = confidence_score
            update_outdated_info(updated_row, confidence_score, api_data, address)
        else:
            # Names aren't close enough, consider the business not found
            updated_row["outdated"] = True
            updated_row["outdated_reason"] = "No mactch found in Google Places"
    else:
        updated_row["outdated"] = True
        updated_row["outdated_reason"] = "No match found in Google Places"

    updated_rows.append(updated_row)

# Instead of concatenating the original and updated data, directly create the updated DataFrame from updated_rows list
updated_df = pd.DataFrame(updated_rows)

# Export updated data to CSV
updated_df.to_csv("Data/updated_business_data.csv", index=False)

print("Business information verification complete. Updated data saved to 'Data/updated_business_data.csv'")
