from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)
fd_r = open('./city_history', 'r')
fd_w = open('./city_history', 'w')
row_cities = fd_r.read()
fd_r.close()
#
# l = [1, 2, 3]
# a = [['1', 'a'], ['2', 'b'], ['3', 'c']]

if len(row_cities) > 0:
    curr_cities = []
    array1 = row_cities.split('\n')
    for i in range(len(array1)):
        curr_cities.append(array1[i].split(';'))
else:
    curr_cities = []


# glues the array back together
def array_glue(arr):
    tmp_arr = []
    for i in range(len(arr)):
        tmp_arr.append(';'.join(arr[i]))
    fd_w.write('\n'.join(tmp_arr) + '\n')


# checks if a city was added to the final list
def city_check(array, item):
    is_added = False
    for i in array:
        if item == i[0]:
            is_added = True
    return is_added


# calculates the average temperature
def avg_temp(arr):
    total_temp = 0
    for i in range(len(arr)):
        total_temp += float(arr[i][1])
    return total_temp / len(arr)


# determines coldest city
def coldest_city(arr):
    min_temp = 50000
    city = ''
    for i in range(len(arr)):
        curr_temp = float(arr[i][1])
        if curr_temp < min_temp:
            min_temp = curr_temp
            city = str(arr[i][0])
    return [city, min_temp]


def get_weather_data_js(city_name):
    city_name = city_name + '\n'
    proc = subprocess.Popen(['node', r".\main.js"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    proc.stdin.write(city_name.encode('ASCII'))
    proc.stdin.flush()
    proc.stdout.readline()
    inp = proc.stdout.readline().decode().split(',')

    data_dict = {
        "city_name": inp[0],
        "temp": inp[1],
        "humidity": inp[2],
        "weather": inp[3]
    }
    return data_dict


@app.route("/")
def hello_world():
    # fd = open("./templates/base.html")
    return render_template("template_empty.html")


@app.route('/get_weather_data', methods=['POST'])
def data():
    form_data = request.form
    user_input = form_data['city_input']
    user_data = get_weather_data_js(user_input)

    if not city_check(curr_cities, user_data['city_name']):
        curr_cities.append([user_data['city_name'], user_data['temp']])

    if len(curr_cities) > 5:
        curr_cities.pop(0)

    array_glue(curr_cities)
    average_temp = avg_temp(curr_cities)
    coldest_city_res = coldest_city(curr_cities)
    coldest_city_name = coldest_city_res[0]
    coldest_city_temp = str(coldest_city_res[1])
    prev_cities = []
    for item in curr_cities:
        prev_cities.append(item[0])

    return render_template('template_with_data.html', city_name=user_data['city_name'], temper=user_data['temp'],
                           humidity=user_data['humidity'], weather_cond=user_data["weather"],
                           avg_temp=f'{average_temp:.2f}',
                           coldest_city_name=coldest_city_name, coldest_city_temp=coldest_city_temp,
                           prev_cities=", ".join(prev_cities))
