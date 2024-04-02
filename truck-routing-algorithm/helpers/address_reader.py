import csv

class AddressReader:
    def __init__(self):
        # hard coded filepath
        file_path = 'resources/addresses_CSV.csv'  # Hardcoded file path
        self.addresses = self.read_address_csv(file_path)

    def read_address_csv(self, file_path):
        # initiate addresses array, populate with name-address tuples
        addresses = []

        with open(file_path, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    place_name, address = row[0].strip(), row[1].strip()
                    addresses.append((place_name, address))

        return addresses

    def get_place_name(self, input_address):
        # take address and return name by referencing array's name-address tuples
        for place_name, address in self.addresses:
            if address == input_address:
                return place_name
        return None
