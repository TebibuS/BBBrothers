from dotenv import load_dotenv
import os
import pandas as pd
import requests
from datetime import datetime

ENV_PATH = str('C:\BBBrothers\BBB BETTER AND BETTER FILES\.env')
load_dotenv(dotenv_path=ENV_PATH)

def get_business_details(api_key, business_name,location="Minnesota"):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={business_name}+in+{location}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    business_details_list = []

    if 'results' in data:
        for result in data['results']:
            place_id = result['place_id']
            details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_phone_number,formatted_address,website,reviews,rating&key={api_key}"
            details_response = requests.get(details_url)
            details_data = details_response.json()
            
            if 'result' in details_data:
                last_reviewed = max([review.get('time', 0) for review in details_data['result'].get('reviews', [{'time': 0}])])
                last_reviewed_date = datetime.utcfromtimestamp(last_reviewed).strftime('%Y-%m-%d %H:%M:%S')
                
                business_info = {
                    'Name': details_data['result'].get('name', ''),
                    'Phone Number': details_data['result'].get('formatted_phone_number', ''),
                    'Address': details_data['result'].get('formatted_address', ''),
                    'Website': details_data['result'].get('website', ''),
                    'Last Reviewed': last_reviewed_date,
                    'Rating' : details_data['result'].get('rating','')
                }
                business_details_list.append(business_info)
    if business_details_list:
        df = pd.DataFrame(business_details_list)
        return df
    else:
        return pd.DataFrame({'Error': ['No businesses found.']})
    
# Example usage
api_key = os.getenv("GOOGLE_PLACES_TOKEN")
business_name = "Starbucks"
business_details_df = get_business_details(api_key, business_name)
business_details_df.to_csv('pedro_is_so_cool.csv')

