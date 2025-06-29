cities_per_country = {
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth"],
    "UAE": ["Dubai", "Abu Dhabi", "Sharjah", "Ajman"],
    "India": ["Mumbai", "Bangalore", "Chennai", "Delhi"]
}

def check_cities_same_country():
    city1 = input("Enter the first city: ").strip()
    city2 = input("Enter the second city: ").strip()
    
    country1 = None
    country2 = None
    
    for country, cities in cities_per_country.items():
        if city1 in cities:
            country1 = country
        if city2 in cities:
            country2 = country
    
    if country1 and country2:
        if country1 == country2:
            print(f"Both cities are in {country1}")
        else:
            print("They don't belong to the same country")
    else:
        print("One or both cities are not found in the list of cities.")

check_cities_same_country()
