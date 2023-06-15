import requests
import random

api_key = "e66bdef54de4e4b80c94c1571cac6d4c"


url = "https://openweathermap.org/"

cities = [
    "Praia,cv",
    "Helsinki,fi,",
    "Dublin,ie",
    "Bucharest,ro",
    "Madrid,es",
    "Stockholm,se",
    "Tunis,tn",
    "Ankara,tr",
    "Toshloq,uz",
    "Cardiff,gb",
    "Mustaba,ye",
    "Valletta,mt",
    "Porto Novo,pt",
    "Chicago,il,us",
    "Rome,it",
    "Kairo,eg",
    "Sofia,bg",
    "Kyoto,jp",
]


# function that gets the city info from openweathermap.org
def get_city_info(city):
    searched_city = city.replace(" ", "%20")
    original_url = f"https://api.openweathermap.org/geo/1.0/direct?q={searched_city}&limit=5&appid=e66bdef54de4e4b80c94c1571cac6d4c"
    url = original_url.replace("{searched_city}", city)
    response = requests.get(url)
    data_array = []

    if response.status_code == 200:
        data = response.json()
        data_array.append(data)
        for i in data_array:
            city_data = i[0]
        short_city_data = {
            "name": city_data["name"],
            "lat": city_data["lat"],
            "lon": city_data["lon"],
            "country": city_data["country"],
        }
        get_weather_data(
            short_city_data["lat"], short_city_data["lon"], short_city_data["name"]
        )
    else:
        print("Error: ", response.status_code)


# end of get_city_info


# gets the weather info for any given city
def get_weather_data(lat, lon, city):
    weather_url = f"https://api.openweathermap.org//data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid=e66bdef54de4e4b80c94c1571cac6d4c"
    response = requests.get(weather_url)

    weather_data_array = []
    if response.status_code == 200:
        data = response.json()
        weather_data_array.append(data)

        for weather_city_data in weather_data_array:
            short_weather_data = {
                "name": city,
                "temp": weather_city_data["main"]["temp"],
                "humidity": weather_city_data["main"]["humidity"],
                "description": weather_city_data["weather"][0]["description"],
            }
            print(
                f'City: {short_weather_data["name"]}\nTemperature: {short_weather_data["temp"]} C\nHumidity: {short_weather_data["humidity"]} %\nThe weather in {short_weather_data["name"]} is {short_weather_data["description"]}.\n'
            )


# choose either 5 random cities or one selected by user
usr_choice = input(
    "Do you want to choose the city?(y/n) If no, then weather information for 5 random cities will be generated."
)
acceptable_answers = ["y", "n", "yes", "no"]

if usr_choice.lower() not in acceptable_answers:
    usr_choice = input("Please enter a valid response - y/n")
should_generate_cities = False
if "y" in usr_choice.lower():
    usr_city = input(
        "Please enter a valid city name and country code, separated by coma, no spaces {city_name,st}: "
    )
    res = get_city_info(usr_city)
else:
    should_generate_cities = True
    rand_cities = []
    rand_cities_weather_data = []
    while len(rand_cities) < 5:
        random_num = random.randint(1, len(cities))
        if not cities[random_num] in rand_cities:
            rand_cities.append(cities[random_num])
    for rand_city in rand_cities:
        get_city_info(rand_city)
# end of logic for user choice
