import httpx
import certifi

CITY_COORDS = {
    "kuala lumpur": (3.1390, 101.6869),
    "putrajaya": (2.9264, 101.6964),
    "penang": (5.4141, 100.3288),
    "langkawi": (6.3500, 99.8000),
    "johor bahru": (1.4927, 103.7414),
    "kota kinabalu": (5.9804, 116.0735),
    "kuching": (1.5533, 110.3592),
}

def get_weather(city: str = "Kuala Lumpur") -> str:
    city_key = city.lower()
    if city_key not in CITY_COORDS:
        return f"City '{city}' not in database. Available: {', '.join(CITY_COORDS.keys())}"
    lat, lon = CITY_COORDS[city_key]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
    try:
        # Try with certifi first
        with httpx.Client(timeout=10, verify=certifi.where()) as client:
            resp = client.get(url)
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        # Fallback for corporate proxy / self-signed chain
        try:
            with httpx.Client(timeout=10, verify=False) as client:
                resp = client.get(url)
                resp.raise_for_status()
                data = resp.json()
        except Exception as e:
            return f"Error fetching weather: {str(e)}"
    
    current = data.get("current", {})
    temp = current.get("temperature_2m", "N/A")
    humidity = current.get("relative_humidity_2m", "N/A")
    wind = current.get("wind_speed_10m", "N/A")
    return f"Weather in {city.title()}:\nTemperature: {temp}°C\nHumidity: {humidity}%\nWind: {wind} km/h"
