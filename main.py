import requests
import folium
import math

#Hämtar magnetisk variation från NOAA
def get_mag_variation(lat, lon):
    url = "https://www.ngdc.noaa.gov/geomag-web/calculators/calculateDeclination"
    params = {
        "lat1": lat,
        "lon1": lon,
        "key": "zNEw7",
        "resultFormat": "json"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data["result"][0]["declination"]
    except:
        print("Kunde inte hämta magnetisk variation.")
        return 0

# Beräknar kurs mellan två koordinater
def bearing(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1

    x = math.sin(dlon) * math.cos(lat2)
    y = (math.cos(lat1) * math.sin(lat2) -
         math.sin(lat1) * math.cos(lat2) * math.cos(dlon))

    return (math.degrees(math.atan2(x, y)) + 360) % 360


# =========================

val_av = input("Har du en målkoordinat? (ja/nej) ")

# =========================
# JA: räkna kurs mellan två punkter
# =========================
if val_av.lower() == "ja":

    try:
        lat = float(input("Ange din latitud ").replace(",", "."))
        lon = float(input("Ange din longitud ").replace(",", "."))
        target_lat = float(input("Ange mållatitud ").replace(",", "."))
        target_lon = float(input("Ange mållongitud ").replace(",", "."))
    except ValueError:
        print("Felaktig inmatning.")
        exit()

    kurs = bearing(lat, lon, target_lat, target_lon)
    variation = get_mag_variation(lat, lon)
    magnetisk_kurs = kurs - variation

    print(f"\nGeografisk kurs: {kurs:.2f}°")
    print(f"Magnetisk variation: {variation:.2f}°")
    print(f"Styr kurs (kompass): {magnetisk_kurs:.2f}°")

    # karta
    k = folium.Map(location=[lat, lon], zoom_start=6)
    folium.Marker([lat, lon], popup="Start").add_to(k)
    folium.Marker([target_lat, target_lon], popup="Mål").add_to(k)
    folium.PolyLine([[lat, lon], [target_lat, target_lon]]).add_to(k)
    k.save("map.html")


# =========================
# NEJ: konvertera kurs från kompass till geografisk eller tvärtom
# =========================
elif val_av.lower() == "nej":

    try:
        lat = float(input("Ange din latitud ").replace(",", "."))
        lon = float(input("Ange din longitud ").replace(",", "."))
    except ValueError:
        print("Felaktig inmatning.")
        exit()

    variation = get_mag_variation(lat, lon)

    print("\nVad vill du konvertera?")
    print("1 = Kompass → Geografisk")
    print("2 = Geografisk → Kompass")

    val = input("Val (1/2): ")

    try:
        kurs = float(input("Ange kurs (grader): ").replace(",", "."))
    except ValueError:
        print("Felaktig kurs.")
        exit()

    if val == "1":
        # magnetisk -> true
        geografisk = kurs + variation
        print(f"\nGeografisk kurs: {geografisk:.2f}°")
        print(f"Variation: {variation:.2f}°")

    elif val == "2":
        # true -> magnetisk
        magnetisk = kurs - variation
        print(f"\nStyrkurs (kompass): {magnetisk:.2f}°")
        print(f"Variation: {variation:.2f}°")

    else:
        print("Ogiltigt val.")


else:
    print("Svara ja eller nej.")