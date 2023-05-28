const { getCipherInfo, randomBytes } = require('node:crypto');
const https = require('node:https');
const fs = require('node:fs')

var api_key = '';
try {
    api_key = fs.readFileSync('../api_key.txt', 'utf-8');
} catch (e) {
    console.log(`Failed to load api_key: ${e}.`);
    process.exit(1);
}

function get_city_info(city) {
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
            weather_data(short_city_data.lon, short_city_data.lat, short_city_data.name);
        });
    });
    req.end();

}

// gets the temperature, humidity, weather description of a chosen city
function weather_data(lon, lat, city) {
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
            console.log(`${short_weather_data.name},${short_weather_data.temp},${short_weather_data.humidity},${short_weather_data.description}`);
        });
    });
    req.end();
}

function user_input() {
    console.log("Please enter a city and its country code, separated by coma, no spaces (ex:Paris,fr): ");
    process.stdin.once('data', (data) => {
        data = data.toString().replace('\n', '');
        if (!/^[a-z]+\,[a-z]{2}$/i.test(data)) {
            user_input();
        } else {
            get_city_info(data);
        }
    });
}

user_input();

