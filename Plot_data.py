import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
import tkinter as tk
import matplotlib.backends.backend_tkagg as tkagg
import sys
import random
import heapq


def read_data_from_csv(file):
    data = []
    with open(file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            location_name, x_coord, y_coord = row
            x_coord = float(x_coord)
            y_coord = float(y_coord)
            data.append((location_name, x_coord, y_coord))
    return data


def calculate_distance(location1, location2):
    x1, y1 = location1[1], location1[2]
    x2, y2 = location2[1], location2[2]
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


def create_plot(data):
    fig, ax = plt.subplots()
    x_coords = [row[1] for row in data]
    y_coords = [row[2] for row in data]
    global scatter
    scatter = ax.scatter(x_coords, y_coords, s=3, color='black')

    # Add route lines
    route_trace, = ax.plot([], [], color='blue', linewidth=0.75)

    # Remove white space around the graph
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    ax.set_xticks([])
    ax.set_yticks([])

    return fig, ax, route_trace


def on_plot_click(event):
    global start_location, scatter, ax, route_trace
    if event.inaxes is None:  # Ignore clicks outside the axes
        return
    min_distance = float('inf')
    for i, location in enumerate(data_list):
        distance = math.sqrt((event.xdata - location[1]) ** 2 + (event.ydata - location[2]) ** 2)
        if distance < min_distance:
            min_distance = distance
            start_location = i

    # Update the point colors to indicate the new start location
    colors = ['red' if i == start_location else 'black' for i in range(len(data_list))]
    sizes = [20 if i == start_location else 3 for i in range(len(data_list))]

    ax.clear()
    ax.set_xticks([])
    ax.set_yticks([])
    scatter = ax.scatter([row[1] for row in data_list], [row[2] for row in data_list], s=sizes, color=colors)

    # Add route lines
    route_trace, = ax.plot([], [], color='blue', linewidth=0.75)

    canvas.draw()  # redraw the canvas to show the new start location


def calculate_route_greedy(data):
    num_locations = len(data)
    distances = [[0.0] * num_locations for _ in range(num_locations)]
    for i in range(num_locations):
        for j in range(num_locations):
            distances[i][j] = calculate_distance(data[i], data[j])

    remaining_locations = set(range(num_locations)) - {start_location}
    current_location = start_location
    route = [current_location]

    while remaining_locations:
        nearest_location = min(remaining_locations, key=lambda x: distances[current_location][x])
        route.append(nearest_location)
        remaining_locations.remove(nearest_location)
        current_location = nearest_location

    return route


def calculate_route_simplest(data):
    num_locations = len(data)
    distances = [[0.0] * num_locations for _ in range(num_locations)]
    for i in range(num_locations):
        for j in range(num_locations):
            distances[i][j] = calculate_distance(data[i], data[j])

    remaining_locations = set(range(num_locations)) - {start_location}
    current_location = start_location
    route = [current_location]

    while remaining_locations:
        # Get 10 closest locations from remaining locations.
        closest_locations = heapq.nsmallest(10, remaining_locations, key=lambda x: distances[current_location][x])
        # random.choice selects a random element from the closest_locations list
        next_location = random.choice(closest_locations)
        route.append(next_location)
        remaining_locations.remove(next_location)
        current_location = next_location

    return route


def calculate_route(data):
    # use the appropriate method based on the checkbox value
    if method.get() == 1:
        return calculate_route_greedy(data)
    else:
        return calculate_route_simplest(data)


def update(frame, route, data, route_trace):
    route_x = []
    route_y = []
    distance = 0
    for i in range(frame + 1):
        location_index = route[i]
        location = data[location_index]
        route_x.append(location[1])
        route_y.append(location[2])
        if i > 0:
            # update the total distance as the animation progresses
            distance += calculate_distance(data[route[i]], data[route[i - 1]])
    route_trace.set_data(route_x, route_y)
    total_distance.set("Total Distance: " + str(round(distance, 2)))  # update the distance


def on_closing(root):
    # Exit the script when closing the window
    root.destroy()
    sys.exit()


def start_animation():
    global fig, ax, route_trace, data_list, anim, canvas, history_text, history, total_distance
    route = calculate_route(data_list)
    anim = FuncAnimation(fig, update, fargs=(route, data_list, route_trace), frames=len(route), interval=0.001,
                         repeat=False, blit=False, init_func=init_animation)
    # update history after the animation has finished
    history.append((method.get(), calculate_total_distance(route, data_list)))
    history = history[-10:]  # keep only the last 10 entries
    history_text.set("\n".join(["Method: {}, Distance: {}".format("Greedy" if x[0] == 1 else "Random", x[1]) for x in history]))
    canvas.draw()  # redraw the canvas after starting the animation


def calculate_total_distance(route, data):
    distance = 0
    for i in range(len(route) - 1):
        distance += calculate_distance(data[route[i]], data[route[i + 1]])
    return round(distance, 2)


def init_animation():
    global route_trace
    route_trace.set_data([], [])
    total_distance.set("Total Distance: 0")


def create_gui(data):
    global fig, ax, route_trace, data_list, anim, canvas, method, history_text, history, total_distance
    data_list = data
    history = []
    root = tk.Tk()
    root.title("Traveling Salesman Problem")

    root.state('zoomed')

    fig, ax, route_trace = create_plot(data)

    fig.canvas.mpl_connect('button_press_event', on_plot_click)

    # Create a PanedWindow to divide the GUI into two resizable parts
    paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=1)

    # Create a frame on the left side of the PanedWindow to hold the graph
    left_frame = tk.Frame(paned_window)
    paned_window.add(left_frame)

    # Set the initial width and minimum width of the left frame
    left_frame_width = 1600
    left_frame.config(width=left_frame_width)
    paned_window.paneconfigure(left_frame, minsize=left_frame_width)

    # Add the graph to the left_frame
    canvas = tkagg.FigureCanvasTkAgg(fig, master=left_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    middle_frame = tk.Frame(paned_window)
    paned_window.add(middle_frame)

    # Create a frame on the right side of the PanedWindow for other content
    right_frame = tk.Frame(paned_window)
    paned_window.add(right_frame)

    # Create a radio button for method selection
    method = tk.IntVar()
    tk.Radiobutton(right_frame, text="Greedy", variable=method, value=1).pack(anchor='w')
    tk.Radiobutton(right_frame, text="Random", variable=method, value=2).pack(anchor='w')
    method.set(1)  # set default method to Greedy

    # Create a Start button at the bottom of the right frame
    start_button = tk.Button(right_frame, text="Start", command=start_animation)
    start_button.pack(side=tk.BOTTOM, fill=tk.X)

    # Create a field for the total distance
    total_distance = tk.StringVar()
    total_distance_label = tk.Label(right_frame, textvariable=total_distance)
    total_distance.set("Total Distance: 0")
    total_distance_label.pack(side=tk.BOTTOM, fill=tk.X)

    # Create a field for the history
    history_text = tk.StringVar()
    history_label = tk.Label(right_frame, textvariable=history_text, justify='left')
    history_label.pack(side=tk.BOTTOM, fill=tk.X)

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    tk.mainloop()


if __name__ == "__main__":
    start_location = 0
    file_name = "model/data.csv"
    data_list = read_data_from_csv(file_name)
    create_gui(data_list)
