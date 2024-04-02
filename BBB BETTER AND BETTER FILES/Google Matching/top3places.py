import pandas as pd
import requests

# Replace 'YOUR_API_KEY_HERE' with your actual Google Places API key
API_KEY = "AIzaSyAsXrm-NU0zZE_BKhgpEVVMrw4VoBdHXWA"

def get_top_3_places(query):
    search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={API_KEY}"
    try:
        search_response = requests.get(search_url)
        search_response.raise_for_status()
        search_data = search_response.json()

        if search_data["status"] == "OK":
            top_places = []
            for place in search_data["results"][:3]:
                place_details = {
                    "name": place.get("name"),
                    "address": place.get("formatted_address"),
                    "place_id": place.get("place_id")
                }
                top_places.append(place_details)
            return top_places
        else:
            print(f"Search API returned status: {search_data['status']}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for query '{query}': {e}")
        return []

# Load business data from CSV
df = pd.read_csv("Data/cleaned_and_normalized_data_first10.csv", dtype={"phone": str})

# Iterate through each business entry and search
for index, row in df.iterrows():
    company_name = row["company_name"]
    city = row.get("city", "")
    state = row.get("state", "")
    query = f"{company_name} {city}, {state}"

    top_places = get_top_3_places(query)
    print(f"\nTop 3 places for '{company_name}':")
    if top_places:
        for idx, place in enumerate(top_places, start=1):
            print(f"{idx}. Name: {place['name']}, Address: {place['address']}, Place ID: {place['place_id']}")
    else:
        print("No places found or an error occurred.")

