import requests
import json
import os
from datetime import datetime

CITIES = {
    "Uttar Pradesh": ["Agra", "Lucknow", "Kanpur", "Varanasi", "Noida", "Meerut", "Prayagraj", "Bareilly", "Aligarh", "Moradabad"],
    "Punjab": ["Amritsar", "Ludhiana", "Jalandhar", "Patiala", "Bathinda", "Mohali", "Pathankot", "Hoshiarpur", "Batala", "Moga"],
    "Haryana": ["Gurgaon", "Faridabad", "Panipat", "Ambala", "Yamunanagar", "Rohtak", "Hisar", "Karnal", "Sonipat", "Panchkula"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Ajmer", "Bikaner", "Kota", "Alwar", "Bhilwara", "Sikar", "Bharatpur"],
    "Himachal": ["Shimla", "Manali", "Dharamshala", "Solan", "Mandi", "Kullu", "Hamirpur", "Bilaspur", "Chamba", "Una"],
    "Uttarakhand": ["Dehradun", "Rishikesh", "Haridwar", "Nainital", "Mussoorie", "Haldwani", "Roorkee", "Rudrapur", "Kashipur", "Pauri"]
}

API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def ingest_weather():
    if not os.path.exists("bronze"):
        os.makedirs("bronze")
        
    all_data = []
    flat_city_list = [city for state in CITIES.values() for city in state]
    
    print(f"Fetching data for {len(flat_city_list)} cities...")

    for city in flat_city_list:
        try:
            params = {"q": city, "appid": API_KEY, "units": "metric"}
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                for state, cities in CITIES.items():
                    if city in cities:
                        data['state'] = state
                all_data.append(data)
                print(f"Success: {city}")
            else:
                print(f"Failed: {city}")
        except Exception as e:
            print(f"Error: {e}")

    filename = f"bronze/weather_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(all_data, f)
    
    print(f"Saved: {filename}")

if __name__ == "__main__":
    ingest_weather()