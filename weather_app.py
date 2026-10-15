import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_city_coordinates(city):
    """Find a city's latitude and longitude."""
    response = requests.get(
        GEOCODING_URL,
        params={"name": city, "count": 1, "language": "en", "format": "json"},
        timeout=15
    )
    response.raise_for_status()

    data = response.json()
    results = data.get("results", [])

    if not results:
        return None

    place = results[0]
    return {
        "name": place["name"],
        "country": place.get("country", "Unknown"),
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "timezone": place.get("timezone", "auto")
    }


def get_weather(place):
    """Fetch current weather conditions."""
    params = {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "is_day",
            "precipitation",
            "weather_code",
            "wind_speed_10m"
        ],
        "timezone": place["timezone"]
    }

    response = requests.get(
        WEATHER_URL,
        params=params,
        timeout=15
    )
    response.raise_for_status()
    return response.json()


def display_weather(place, data):
    """Display the weather report."""
    current = data.get("current")

    if not current:
        print("Weather data is currently unavailable.")
        return

    code = current.get("weather_code")
    condition = WEATHER_CODES.get(code, "Unknown conditions")

    print("\n" + "=" * 40)
    print(f" WEATHER REPORT: {place['name']}, {place['country']}")
    print("=" * 40)
    print(f" Date and time      : {current.get('time', 'N/A')}")
    print(f" Conditions         : {condition}")
    print(f" Temperature        : {current.get('temperature_2m', 'N/A')} °C")
    print(f" Feels like         : {current.get('apparent_temperature', 'N/A')} °C")
    print(f" Humidity           : {current.get('relative_humidity_2m', 'N/A')}%")
    print(f" Wind speed         : {current.get('wind_speed_10m', 'N/A')} km/h")
    print(f" Precipitation      : {current.get('precipitation', 'N/A')} mm")
    print(f" Daytime            : {'Yes' if current.get('is_day') == 1 else 'No'}")
    print("=" * 40)


def main():
    print("\nWelcome to the Python Weather App!")

    while True:
        city = input(
            "\nEnter a city name (or type 'exit' to quit): "
        ).strip()

        if city.lower() == "exit":
            print("Thank you for using the Weather App!")
            break

        if not city:
            print("Please enter a valid city name.")
            continue

        try:
            print(f"\nFetching weather for {city}...")

            place = get_city_coordinates(city)

            if place is None:
                print("City not found. Please check the spelling.")
                continue

            weather_data = get_weather(place)
            display_weather(place, weather_data)

        except requests.exceptions.Timeout:
            print("Request timed out. Please try again.")

        except requests.exceptions.ConnectionError:
            print("Could not connect to the internet. Check your connection.")

        except requests.exceptions.HTTPError as error:
            print(f"Weather API returned an error: {error}")

        except requests.exceptions.RequestException as error:
            print(f"An error occurred while fetching weather: {error}")

        except (KeyError, TypeError, ValueError) as error:
            print(f"Could not process the weather data: {error}")


if __name__ == "__main__":
    print("Starting the Weather App...")
    main()
