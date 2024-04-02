from datetime import datetime, timedelta, time
import csv

class PackageHashTable:
    def __init__(self, size=40, csv_file_path='resources/packages_CSV.csv'): # hardcoded filepath
        self.size = size
        self.table = [None] * size
        self.csv_file_path = csv_file_path
        self.read_packages_from_csv()

    def read_packages_from_csv(self):
        with open(self.csv_file_path) as file:
            next(file)  # skip header
            # read each line and parse for package attributes
            for line in file:
                package_data = line.strip().split(',')
                package_id, address, city, zip_code, deadline, weight, arrival = package_data
                self.insert_package(int(package_id), address, city, zip_code, deadline, int(weight), arrival_time=arrival)

    def hash_function(self, package_id):
        return package_id % self.size

    def insert_package(self, package_id, address, city, zip_code, deadline, weight, arrival_time=None, delivery_status=None):
        # insert package into table, pre-populating certain fields based on given logic
        index = self.hash_function(package_id)
        if self.table[index] is None:
            self.table[index] = [] # no two package should have the same slot in the table
        if arrival_time is None or not arrival_time.strip():
            arrival_time = self.default_arrival_time() # default arrival time when empty is 8:00 AM
        if delivery_status is None:
            delivery_status = self.default_delivery_status(arrival_time) # packages that do not arrive late arrive at 8:00 AM
        self.table[index].append({
            'package_id': package_id,
            'address': address,
            'city': city,
            'zip_code': zip_code,
            'deadline': self.default_deadline(deadline), # default deadline is 11:59 PM (eod)
            'weight': weight,
            'arrival_time': arrival_time,
            'delivery_status': delivery_status,
            'delivered_time': None
        })

    def default_deadline(self, deadline):
        # if deadline in CSV is eod, return 11:59 PM
        if deadline.lower() == 'eod':
            return datetime.strptime('11:59 PM', "%I:%M %p").time()
        else:
            return datetime.strptime(deadline, "%I:%M %p").time()

    def default_arrival_time(self):
        return datetime.strptime('8:00 AM', "%I:%M %p").time()

    def default_delivery_status(self, arrival_time):
        # a package that is not late is assumed to be at the hub at 8:00 AM ready for departure
        hub_arrival_time = time(8, 0)
        
        if arrival_time == hub_arrival_time:
            return 'At Hub'
        else:
            return 'En Route to Hub'

    def lookup_package(self, package_id):
        # lookup a package by going to the table's index corresponding directly to package ID
        index = self.hash_function(package_id)
        if self.table[index] is not None:
            for package in self.table[index]:
                if package['package_id'] == package_id:
                    return package
        return None

    def format_package_details(self, package):
        # default package lookup print (when no time is given 11:59 PM aka eod is used)
        print()
        formatted_details = f"Package {package['package_id']}\n" \
                            f"Address: {package['address']}\n" \
                            f"City: {package['city']}\n" \
                            f"Zip Code: {package['zip_code']}\n" \
                            f"Weight: {package['weight']} kilo(s)\n" \
                            f"Deadline: {package['deadline'].strftime('%I:%M %p')}\n"

        if package['delivery_status'].lower() == 'delivered':
            delivered_time = package['delivered_time']
            formatted_time = package['delivered_time'].strftime("%I:%M %p")
            formatted_details += f"Delivery Status: {package['delivery_status']} at {formatted_time}\n"
        else:
            formatted_details += f"Delivery Status: {package['delivery_status']}\n"

        return formatted_details

    def package_status_in_time(self, package, requested_time):
        # when time is given, logic is required to view package state at specific time
        print()
        formatted_details = f"Package {package['package_id']}\n" \
                            f"Address: {package['address']}\n" \
                            f"City: {package['city']}\n" \
                            f"Zip Code: {package['zip_code']}\n" \
                            f"Weight: {package['weight']} kilo(s)\n" \
                            f"Deadline: {package['deadline'].strftime('%I:%M %p')}\n"

        print()
        print(formatted_details, end="")

        arrival_time = package.get("arrival_time")
        loaded_time = package.get("loaded_time")
        delivered_time = package.get("delivered_time")

        print("Status at " + requested_time.strftime("%I:%M %p") + ": ", end="")
        # logic to ensure accurate package state return based on time comparisons
        if requested_time < arrival_time:
            print("en route to hub")
        elif requested_time < loaded_time:
            print("at hub")
        elif requested_time < delivered_time:
            print("en route")
        elif delivered_time <= requested_time:
            print("delivered at", delivered_time.strftime('%I:%M %p'))
        else:
            print("error: status could not be found")

