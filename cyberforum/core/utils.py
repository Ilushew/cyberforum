import requests

from django.conf import settings


def geocode_address(address: str):
    api_key = getattr(settings, "YANDEX_GEOCODER_API_KEY", None)
    if not api_key:
        url = "https://geocode-maps.yandex.ru/1.x/"
    else:
        url = f"https://geocode-maps.yandex.ru/1.x/?apikey={api_key}"

    params = {"geocode": address, "format": "json", "results": 1}

    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            geo_object = (
                data.get("response", {})
                .get("GeoObjectCollection", {})
                .get("featureMember")
            )
            if geo_object:
                coords = geo_object[0]["GeoObject"]["Point"]["pos"]  # "lon lat"
                lon, lat = map(float, coords.split())
                lon, lat = str(lon).replace(",", "."), str(lat).replace(",", ".")
                return lat, lon
    except Exception as e:
        print(f"Ошибка геокодинга для '{address}': {e}")

    return None, None
