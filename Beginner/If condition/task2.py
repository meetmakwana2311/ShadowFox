cities_per_country = {
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth"],
    "UAE": ["Dubai", "Abu Dhabi", "Sharjah", "Ajman"],
    "India": ["Mumbai", "Bangalore", "Chennai", "Delhi"]
}

def find_country_by_city():
    city_name = input("Enter a city name: ").strip()
    
    country_found = None
    
    for country, cities in cities_per_country.items():
        if city_name in cities:
            country_found = country
            break
    
    if country_found:
        print(f"{city_name} is in {country_found}")
    else:
        print(f"{city_name} is not found in the list of cities.")

find_country_by_city()
