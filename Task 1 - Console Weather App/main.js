const { getCipherInfo, randomBytes } = require('node:crypto');
const https = require('node:https');
const prompt = require('prompt-sync')();
const fs = require('node:fs')

var api_key = '';
try {
    api_key = fs.readFileSync('../api_key.txt', 'utf-8');
} catch (e) {
    console.log(`Failed to load api_key: ${e}.`);
    process.exit(1);
}

// 19 randomly chosen cities
let cities = ['Praia,cv', 'Helsinki,fi,', 'Dublin,ie',
    'Bucharest,ro', 'Madrid,es', 'Stockholm,se',
    'Tunis,tn', 'Ankara,tr', 'Toshloq,uz',
    'Cardiff,gb', 'Mustaba,ye', 'Valletta,mt',
    'Porto Novo,pt', 'Chicago,il,us',
    'Rome,it', 'Kairo,eg', 'Sofia,bg', 'Kyoto,jp'];

// generates a random number from 0 to max
function getRandomInt(max) {
    return Math.round(Math.random() * max);
}

// gets the name, lattitude, longtitude, state and country of the chosen city
function get_city_info(city, fn) {
    city = city.replace(' ', '%20');
    const options = {
        protocol: 'https:',
        host: 'api.openweathermap.org',
        path: `/geo/1.0/direct?q=${city}&limit=5&appid=${api_key}`
    };
    const req = https.request(options, function (res) {
        let data_array = []
        res.on('data', chunk => {
            data_array.push(chunk);
        });

        res.on('end', () => {
            const city_data = JSON.parse(data_array.join(''));
            const short_city_data = {};
            short_city_data.name = city_data[0].name;
            short_city_data.lat = city_data[0].lat;
            short_city_data.lon = city_data[0].lon;
            short_city_data.state = city_data[0].state;
            short_city_data.country = city_data[0].country;
            weather_data(short_city_data.lon, short_city_data.lat, short_city_data.name, fn);
        });
    });
    req.end();

}

// gets the temperature, humidity, weather description of a chosen city
function weather_data(lon, lat, city, fn) {
    const options = {
        protocol: 'https:',
        host: 'api.openweathermap.org',
        path: `/data/2.5/weather?lat=${lat}&lon=${lon}&units=metric&appid=${api_key}`
    };
    const req = https.request(options, function (res) {
        let weather_data_array = []
        res.on('data', chunk => {
            weather_data_array.push(chunk);
        });

        res.on('end', () => {
            const weather_data = JSON.parse(weather_data_array.join(''));
            const short_weather_data = {};
            short_weather_data.name = city;
            short_weather_data.temp = weather_data.main.temp;
            short_weather_data.humidity = weather_data.main.humidity;
            short_weather_data.description = weather_data.weather[0].description;
            console.log(`City: ${short_weather_data.name}\nTemperature: ${short_weather_data.temp} C\nHumidity: ${short_weather_data.humidity} %\nThe weather in ${short_weather_data.name} is ${short_weather_data.description}.\n`);
            if (typeof fn == 'function') {
                fn(short_weather_data)
            }
        });
    });
    req.end();
}

//  user's choice to enter cities or not
let should_generate_cities = prompt("Do you want to choose the city?(y/n) If no, then weather information for 5 random cities will be generated. ")
while (should_generate_cities != 'y' && should_generate_cities != 'n') {
    should_generate_cities = prompt("Please enter a valid response - y/n")
}

// if yes info for a single city will be displayed, otherwise for 5 random cities
if (should_generate_cities == 'y') {
    let user_city = prompt("Please enter a city and its country code, separated by coma, no spaces (ex:Paris,fr): ");
    while (!/^[a-z]+\,[a-z]{2}$/i.test(user_city)) {
        user_city = prompt("Please enter a valid city name and country code, separated by coma, no spaces: ")
    }

    get_city_info(user_city);

} else {
    let rand_cities = []
    let rand_cities_weather_data = []
    // generates 5 random cities
    while (rand_cities.length < 5) {
        let rand_num = getRandomInt(cities.length - 1);
        if (!rand_cities.includes(cities[rand_num])) {
            rand_cities.push(cities[rand_num]);
        }
    }
    for (let city of rand_cities) {
        get_city_info(city, (short_weather_data) => {
            rand_cities_weather_data.push(short_weather_data);

            // calculates average temperature and coldest city
            if (rand_cities_weather_data.length == rand_cities.length) {
                let min_temp = 50000;
                let avg_temp = 0;
                let coldest_city = ''
                for (let city of rand_cities_weather_data) {
                    if (city.temp < min_temp) {
                        min_temp = city.temp;
                        coldest_city = city.name;
                    }
                    avg_temp += city.temp;
                }
                console.log(`The coldest city of the random cities is ${coldest_city} (${min_temp} C).`);
                console.log(`Average temperature between the random cities is ${(avg_temp / rand_cities_weather_data.length).toFixed(2)} C.`);
            }
        });
    }
}


