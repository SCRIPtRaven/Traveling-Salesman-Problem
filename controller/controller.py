from model import model_data, model_logic
from view import view_gui


class Controller:
    def __init__(self):
        self.model_data = model_data.ModelData()
        self.model_calculations = model_logic.ModelCalculations()
        self.view = view_gui.ViewGUI(self)

    def generate_data(self):
        self.model_data.start()

    def handle_data_request(self):
        return self.model_data.read_data_from_csv()

    def start(self):
        self.view.create_gui()

    def handle_solution_selection(self, selected: int):
        self.model_calculations.METHOD = selected

    def handle_start_selection(self, event):
        self.view.on_plot_click(event)

    def handle_start_button(self):
        self.view.start_animation()

    def handle_route_request(self):
        return self.model_calculations.calculate_route(self)

    def handle_total_distance_request(self, route):
        return self.model_calculations.calculate_total_distance(route)

    def handle_method_request(self):
        return self.model_calculations.METHOD

    def handle_distance_request(self, p1, p2):
        return self.model_calculations.calculate_distance(p1, p2)

    def handle_position_selection(self):
        return self.view.get_start()
