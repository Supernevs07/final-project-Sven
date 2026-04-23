import datetime
import requests 
def get_mag_variation(lat,lon):
     url = "https://www.ngdc.noaa.gov/geomag-web/calculators/calculateDeclination"
     params = {
        "lat1": lat,
        "lon1": lon,
        "key": "zNEw7",
        "resultFormat": "json"
    }
   
     response = requests.get(url, params=params)
    
     data = response.json()
    
    # Plocka ut declination (magnetisk variation)
     variation = data["result"][0]["declination"]
    
     return variation

# Test
lat = input("Ange din latitud ")   
lon = input("Ange din longitud ")

variation = get_mag_variation(lat, lon)
print(f"Magnetisk variation: {variation}°")


