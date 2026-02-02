import requests

BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

def fetch_irradiance(lat, lon, date):
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN",
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "start": date,
        "end": date,
        "format": "JSON"
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()
    irradiance = list(
        data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"].values()
    )[0]

    return irradiance  # kWh/m²/day
