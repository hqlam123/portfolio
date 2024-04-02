import csv
import os

class DistanceMatrix:
    def __init__(self):
        # hardcoded file path
        current_dir = os.getcwd()
        file_path = current_dir + '/truck-routing-algorithm/resources/distances_CSV.csv'

        self.buildings = []
        self.distances = []

        self.read_distance_csv(file_path)

    def read_distance_csv(self, file_path):
        with open(file_path, newline='') as file:
            reader = csv.reader(file)
            data = list(reader)

        # get building names from the first row and first column
        self.buildings = data[0][1:]

        # create the distances matrix by reading the CSV file
        self.distances = [[0.0] * len(self.buildings) for _ in range(len(self.buildings))]

        for i in range(1, len(data)):
            for j in range(1, len(data[i])):
                distance = float(data[i][j]) if data[i][j] else float(data[j][i])
                self.distances[i - 1][j - 1] = distance

    def get_distance(self, from_building, to_building):
        # return distance by referencing the matrix
        try:
            from_index = self.buildings.index(from_building)
            to_index = self.buildings.index(to_building)
            return self.distances[from_index][to_index]
        except ValueError:
            print(f"One or both of the buildings not found: {from_building}, {to_building}")
            return None
