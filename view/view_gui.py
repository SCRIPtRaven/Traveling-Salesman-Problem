import math
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.animation import FuncAnimation


class ViewGUI:
    def __init__(self, controller):
        self.controller = controller
        self.start_location = 0
        self.data_list = None
        self.fig = None
        self.ax = None
        self.scatter = None
        self.route_trace = None
        self.anim = None
        self.canvas = None
        self.history_text = None
        self.history = []

    def get_start(self):
        return self.start_location

    def create_plot(self):
        self.fig, self.ax = plt.subplots()
        x_coords = [row[1] for row in self.data_list]
        y_coords = [row[2] for row in self.data_list]
        self.scatter = self.ax.scatter(x_coords, y_coords, s=3, color='black')

        # Add route lines
        self.route_trace, = self.ax.plot([], [], color='blue', linewidth=0.75)

        # Remove white space around the graph
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
        self.ax.set_xticks([])
        self.ax.set_yticks([])

    def on_plot_click(self, event):
        if event.inaxes is None:  # Ignore clicks outside the axes
            return
        min_distance = float('inf')
        for i, location in enumerate(self.data_list):
            distance = math.sqrt((event.xdata - location[1]) ** 2 + (event.ydata - location[2]) ** 2)
            if distance < min_distance:
                min_distance = distance
                self.start_location = i

        # Update the point colors to indicate the new start location
        colors = ['red' if i == self.start_location else 'black' for i in range(len(self.data_list))]
        sizes = [20 if i == self.start_location else 3 for i in range(len(self.data_list))]

        self.ax.clear()
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.scatter = self.ax.scatter([row[1] for row in self.data_list], [row[2] for row in self.data_list],
                                       s=sizes, color=colors)

        # Add route lines
        self.route_trace, = self.ax.plot([], [], color='blue', linewidth=0.75)

        self.canvas.draw()  # redraw the canvas to show the new start location

    def start_animation(self):
        route = self.controller.handle_route_request()
        self.anim = FuncAnimation(self.fig, self.update, fargs=(route, self.data_list, self.route_trace),
                                  frames=len(route), interval=0.001, repeat=False, blit=False,
                                  init_func=self.init_animation)
        # update history after the animation has finished
        self.history.append((self.controller.handle_method_request(), self.controller.handle_total_distance_request(route)))
        self.history = self.history[-10:]  # keep only the last 10 entries
        self.history_text.set(
            "\n".join(["Method: {}, Distance: {}".format("Greedy" if x[0] == 1 else "Random", x[1]) for x in self.history]))
        self.canvas.draw()  # redraw the canvas after starting the animation

    def init_animation(self):
        self.route_trace.set_data([], [])
        self.total_distance.set("Total Distance: 0")

    def update(self, frame, route, data, route_trace):
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
                distance += self.controller.handle_distance_request(data[route[i]], data[route[i - 1]])
        route_trace.set_data(route_x, route_y)
        self.total_distance.set("Total Distance: " + str(round(distance, 2)))  # update the distance

    def create_gui(self):
        self.data_list = self.controller.handle_data_request()

        root = tk.Tk()
        root.title("Traveling Salesman Problem")

        root.state('zoomed')

        self.fig, self.ax = plt.subplots()
        self.create_plot()

        self.fig.canvas.mpl_connect('button_press_event', self.controller.handle_start_selection)

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
        self.canvas = tkagg.FigureCanvasTkAgg(self.fig, master=left_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        middle_frame = tk.Frame(paned_window)
        paned_window.add(middle_frame)

        # Create a frame on the right side of the PanedWindow for other content
        right_frame = tk.Frame(paned_window)
        paned_window.add(right_frame)

        # Create a radio button for method selection
        method = tk.IntVar()
        method.set(1)  # set default method to Greedy
        tk.Radiobutton(right_frame, text="Greedy", variable=method, value=1,
                       command=lambda: self.controller.handle_solution_selection(method.get())).pack(anchor='w')
        tk.Radiobutton(right_frame, text="Random", variable=method, value=2,
                       command=lambda: self.controller.handle_solution_selection(method.get())).pack(anchor='w')

        # Create a Start button at the bottom of the right frame
        start_button = tk.Button(right_frame, text="Start", command=self.controller.handle_start_button)
        start_button.pack(side=tk.BOTTOM, fill=tk.X)

        # Create a field for the total distance
        self.total_distance = tk.StringVar()
        total_distance_label = tk.Label(right_frame, textvariable=self.total_distance)
        self.total_distance.set("Total Distance: 0")
        total_distance_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Create a field for the history
        self.history_text = tk.StringVar()
        history_label = tk.Label(right_frame, textvariable=self.history_text, justify='left')
        history_label.pack(side=tk.BOTTOM, fill=tk.X)

        root.mainloop()
