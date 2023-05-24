import tkinter as tk
import subprocess
import time


def get_weather_data_js(city_name):
    city_name = city_name + '\n'
    proc = subprocess.Popen(['node', r".\main.js"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    # print(proc.stdout.readline())
    #     time.sleep(0.1)
    #     proc.stdin.write(b'y\n')
    #     proc.stdin.flush()
    print(city_name)
    print(city_name.encode('ASCII'))
    # time.sleep(0.1)
    proc.stdin.write(city_name.encode('ASCII'))
    proc.stdin.flush()
    # time.sleep(1)
    # try:
    proc.stdout.readline()
    # except NameError:
    #     print(NameError, '\nsomething went wrong here')

    # time.sleep(1)
    inp = proc.stdout.readline().decode().split(',')
    city_text.insert(0, inp[0])
    temp_text.insert(0, inp[1] + ' C')
    humidity_text.insert(0, inp[2] + '%')


def print_user_input():
    input_text = f'{city_input.get()},{city_state.get()}'
    # print("User Input:", input_text)
    get_weather_data_js(input_text)


def on_entry_click_city(event):
    if city_input.get() == "Enter city name...":
        city_input.delete(0, tk.END)  # Remove the default text
        city_input.config(fg="black")  # Change the text color to black


def on_entry_click_state(event):
    if city_state.get() == "Enter city state/country...":
        city_state.delete(0, tk.END)  # Remove the default text
        city_state.config(fg="black")  # Change the text color to black


# Create the main window
root = tk.Tk()
root.title("Data Display")

# Create the entry field and button in the first row
city_input = tk.Entry(root, fg="gray")
city_input.insert(0, "Enter city name...")
city_input.bind("<FocusIn>", on_entry_click_city)
city_input.grid(row=0, column=0, padx=5, pady=5)

# enter_button = tk.Button(root, text="Enter", command=print_user_input)
# enter_button.grid(row=0, column=1, padx=5, pady=5)


# Create the state field and button in the first row
city_state = tk.Entry(root, fg="gray")
city_state.insert(0, "Enter city state/country...")
city_state.bind("<FocusIn>", on_entry_click_state)
city_state.grid(row=1, column=0, padx=5, pady=5)

enter_button = tk.Button(root, text="Enter", command=print_user_input)
enter_button.grid(row=1, column=1, padx=5, pady=5)

# Create the label and text field in the third row for City name
city_label = tk.Label(root, text="City name:")
city_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)

city_text = tk.Entry(root)
city_text.grid(row=2, column=1, padx=5, pady=5)

# Create the labels and text fields in the fourth and fifth rows for Temperature and Humidity
temp_label = tk.Label(root, text="Temperature:")
temp_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

temp_text = tk.Entry(root)
temp_text.grid(row=3, column=1, padx=5, pady=5)

humidity_label = tk.Label(root, text="Humidity:")
humidity_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)

humidity_text = tk.Entry(root)
humidity_text.grid(row=4, column=1, padx=5, pady=5)

# Create the label and text field for Previous cities
# prev_cities_label = tk.Label(root, text="Previous cities:")
# prev_cities_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
#
# prev_cities_text = tk.Entry(root)
# prev_cities_text.grid(row=6, column=1, padx=5, pady=5)

# Create the label for Average temperature
# avg_temp_label = tk.Label(root, text="Average temperature:")
# avg_temp_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.E)
#
# avg_temp_text = tk.Entry(root)
# avg_temp_text.grid(row=8, column=1, padx=5, pady=5)

# Create the label for Coldest city
# coldest_city_label = tk.Label(root, text="Coldest city:")
# coldest_city_label.grid(row=9, column=0, padx=5, pady=5, sticky=tk.E)
#
# coldest_city_text = tk.Entry(root)
# coldest_city_text.grid(row=9, column=1, padx=5, pady=5)

# Create the Quit button in the last row
quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.grid(row=11, column=1, padx=5, pady=5, sticky=tk.E)

# Start the main loop
root.mainloop()
