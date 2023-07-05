import math
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.animation import FuncAnimation


start_location = 0
DATA_LIST = None


def get_start():
    return start_location


def create_plot():
    fig, ax = plt.subplots()
    x_coords = [row[1] for row in DATA_LIST]
    y_coords = [row[2] for row in DATA_LIST]
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
    global start_location, scatter, ax, route_trace, DATA_LIST
    if event.inaxes is None:  # Ignore clicks outside the axes
        return
    min_distance = float('inf')
    for i, location in enumerate(DATA_LIST):
        distance = math.sqrt((event.xdata - location[1]) ** 2 + (event.ydata - location[2]) ** 2)
        if distance < min_distance:
            min_distance = distance
            start_location = i

    # Update the point colors to indicate the new start location
    colors = ['red' if i == start_location else 'black' for i in range(len(DATA_LIST))]
    sizes = [20 if i == start_location else 3 for i in range(len(DATA_LIST))]

    ax.clear()
    ax.set_xticks([])
    ax.set_yticks([])
    scatter = ax.scatter([row[1] for row in DATA_LIST], [row[2] for row in DATA_LIST], s=sizes, color=colors)

    # Add route lines
    route_trace, = ax.plot([], [], color='blue', linewidth=0.75)

    canvas.draw()  # redraw the canvas to show the new start location


def start_animation(contr):
    global fig, ax, route_trace, DATA_LIST, anim, canvas, history_text, history, total_distance
    route = contr.handle_route_request()
    anim = FuncAnimation(fig, update, fargs=(route, DATA_LIST, route_trace, contr), frames=len(route), interval=0.001,
                         repeat=False, blit=False, init_func=init_animation)
    # update history after the animation has finished
    history.append((contr.handle_method_request(), contr.handle_total_distance_request(route)))
    history = history[-10:]  # keep only the last 10 entries
    history_text.set(
        "\n".join(["Method: {}, Distance: {}".format("Greedy" if x[0] == 1 else "Random", x[1]) for x in history]))
    canvas.draw()  # redraw the canvas after starting the animation


def init_animation():
    global route_trace
    route_trace.set_data([], [])
    total_distance.set("Total Distance: 0")


def update(frame, route, data, route_trace, contr):
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
            distance += contr.handle_distance_request(data[route[i]], data[route[i - 1]])
    route_trace.set_data(route_x, route_y)
    total_distance.set("Total Distance: " + str(round(distance, 2)))  # update the distance


def create_gui(contr):
    global fig, ax, route_trace, DATA_LIST, anim, canvas, history_text, history, total_distance

    history = []
    root = tk.Tk()
    root.title("Traveling Salesman Problem")

    root.state('zoomed')

    fig, ax, route_trace = create_plot()

    fig.canvas.mpl_connect('button_press_event', contr.handle_start_selection)

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
    method.set(1)  # set default method to Greedy
    tk.Radiobutton(right_frame, text="Greedy", variable=method, value=1, command=lambda: contr.handle_solution_selection(method.get())).pack(anchor='w')
    tk.Radiobutton(right_frame, text="Random", variable=method, value=2, command=lambda: contr.handle_solution_selection(method.get())).pack(anchor='w')

    # Create a Start button at the bottom of the right frame
    start_button = tk.Button(right_frame, text="Start", command=contr.handle_start_button)
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

    root.mainloop()


def main(contr):
    global DATA_LIST
    DATA_LIST = contr.handle_data_request()
    create_gui(contr)
