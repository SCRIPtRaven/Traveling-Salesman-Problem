import csv
import os
import random
import geonamescache


class ModelData:
    MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
    FILE_NAME = os.path.join(MODEL_DIR, "data.csv")

    @staticmethod
    def is_ascii(s):
        return all(ord(c) < 128 for c in s)

    def generate_data(self, rows):
        data_list = []
        used_coordinates = set()

        gc = geonamescache.GeonamesCache()
        cities = gc.get_cities()

        valid_cities = [city for city in cities.values() if
                        'latitude' in city and 'longitude' in city and self.is_ascii(city['name'])]

        for _ in range(rows):
            while True:
                city = random.choice(valid_cities)
                latitude = random.uniform(0, 10000)
                longitude = random.uniform(0, 10000)
                coordinate = (latitude, longitude)
                if coordinate not in used_coordinates:
                    used_coordinates.add(coordinate)
                    break

            location_name = city['name']
            data_list.append((location_name, latitude, longitude))

        return data_list

    def write_to_csv(self, data_list):
        with open(self.FILE_NAME, "w", newline="", encoding="UTF8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Location Name", "X Coordinate", "Y Coordinate"])
            writer.writerows(data_list)

        print(f"Data saved to {self.FILE_NAME}.")

    @staticmethod
    def read_data_from_csv():
        data_list = []
        with open(ModelData.FILE_NAME, 'r') as file:
            next(file)  # Skip the header line
            for line in file:
                line = line.strip().split(',')
                data_list.append([line[0], float(line[1]), float(line[2])])
        return data_list

    def start(self):
        num_rows = 100
        data = self.generate_data(num_rows)
        self.write_to_csv(data)
