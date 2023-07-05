from model import model_data, model_calculations
from view import view_gui


class Controller:
    def __init__(self):
        self.m_data = model_data
        self.m_calculations = model_calculations
        self.view = view_gui

    def generate_data(self):
        self.m_data.main()

    def handle_data_request(self):
        return self.m_data.read_data_from_csv()

    def start(self):
        self.view.main(self)

    def handle_solution_selection(self, selected: int):
        self.m_calculations.set_method(selected)

    def handle_start_selection(self, event):
        self.view.on_plot_click(event)

    def handle_start_button(self):
        self.view.start_animation(self)

    def handle_route_request(self):
        return self.m_calculations.calculate_route(self)

    def handle_total_distance_request(self, route):
        return self.m_calculations.calculate_total_distance(route)

    def handle_method_request(self):
        return self.m_calculations.get_method()

    def handle_distance_request(self, p1, p2):
        return self.m_calculations.calculate_distance(p1, p2)

    def handle_position_selection(self):
        return self.view.get_start()
