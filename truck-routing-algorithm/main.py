from datetime import time, timedelta, datetime
from helpers.package_hash_table import PackageHashTable
from helpers.address_reader import AddressReader
from helpers.distance_reader import DistanceMatrix
from objects.truck import Truck

global to_print
to_print = True

def main():
    # load helper classes
    address_reader = AddressReader()
    package_hash_table = PackageHashTable()
    distance_matrix = DistanceMatrix()

    # create trucks with start times
    # truck1 runs immediately, truck2 waits for the late packages, truck3 leaves at 10:20 to account for package #9
    truck1 = Truck(1, time(8, 0), package_hash_table)
    truck2 = Truck(2, time(9, 5), package_hash_table)
    truck3 = Truck(3, time(10, 20), package_hash_table)

    # load trucks and begin delivery routes
    load_trucks(truck1, truck2, truck3)
    start_delivery_route(truck1, address_reader, distance_matrix)
    start_delivery_route(truck2, address_reader, distance_matrix)
    start_delivery_route(truck3, address_reader, distance_matrix)

    # display interface for viewing info at eod
    display_info(truck1, truck2, truck3)

    # display package status at given time ranges per requirement D
    print_time_range(package_hash_table)

    # display interface for displaying package status at a given time
    package_lookup(package_hash_table)

def load_trucks(truck1, truck2, truck3):
    # truck1 is loaded with deadline packages already at hub, 19 due to grouping, then until full
    # truck2 is loaded with 9:05 arrival packages, packages needing to be on truck2, then until full
    # truck 3 gets the corrected package, then until full

    truck1.load_packages([15, 1, 13, 14, 16, 20, 29, 30, 31, 34, 37, 40, 19, 2, 4, 5])
    truck2.load_packages([6, 25, 3, 18, 28, 32, 36, 38, 7, 8 , 10, 11, 12, 17, 21, 22])
    truck3.load_packages([9, 23, 24, 26, 27, 33, 35, 39])

def start_delivery_route(truck, address_reader, distance_reader):
    # packages get delivered until truck is empty
    while len(truck.packages_held) != 0:
        # identiy the next package to be delivered
        closest_package_id = truck.next_package()
        package = truck.package_hash_table.lookup_package(closest_package_id)
        
        # set truck destination to that package
        destination = address_reader.get_place_name(package["address"])
        truck.destination = destination
        location_to_print = truck.location # helps to group all print lines together

        # calculate distance to destination, add to truck mileage
        distance = distance_reader.get_distance(truck.location, truck.destination)
        truck.miles_traveled += distance

        # calculate time traveled, convert to datetime, add to truck's "clock"
        minutes_traveled = int(distance / 18.0 * 60)
        truck_datetime = datetime.combine(datetime.today(), truck.time)
        new_datetime = truck_datetime + timedelta(minutes=minutes_traveled)
        new_time = new_datetime.time()
        truck.time = new_time

        # "deliver" the package
        truck.remove_package(closest_package_id)
        truck.packages_delivered += 1

        # set truck location to where it "physically" is at end of delivery
        truck.location = destination

        # print details
        if to_print:
            print(f"Truck{truck.id} location: {location_to_print}")
            print(f"Truck{truck.id} destination: {truck.destination}")
            print(f"Distance to next destination: {distance} miles")
            print(f"Minutes traveled: {minutes_traveled}")
            print(f"Package deadline: {package['deadline']}")
            delivered_time = package['delivered_time']
            formatted_time = package['delivered_time'].strftime("%I:%M %p")
            print(f"Package {package['package_id']} delivered time: {formatted_time}")
            if truck.time < package.get("deadline"):
                print("ON TIME!")
            else:
                print("LATE!")
            print()

    # check if it's truck1 returning to hub
    if truck.id == 1:
        
        truck.destination = "Western Governors University"

        # calculate distance to hub
        distance_to_hub = distance_reader.get_distance(truck.location, truck.destination)
        truck.miles_traveled += distance_to_hub

        # calculate time traveled
        minutes_traveled_to_hub = int(distance_to_hub / 18.0 * 60)
        truck_datetime = datetime.combine(datetime.today(), truck.time)
        new_datetime = truck_datetime + timedelta(minutes=minutes_traveled_to_hub)
        new_time = new_datetime.time()
        truck.time = new_time
        
        if to_print:
            print("Truck1 returning to hub")
            print(f"Truck{truck.id} location: {truck.location}")
            print(f"Truck{truck.id} destination: {truck.destination}")
            print(f"Distance to next destination: {distance_to_hub} miles")
            print(f"Minutes traveled: {minutes_traveled_to_hub}")
            print(f"Truck{truck.id} arrives back at hub: {truck.time.strftime('%I:%M %p')}")
            print()
        
def display_info(truck1, truck2, truck3):
    # displays total packages delivered and all truck information
    if to_print:
        total_packages_delivered = truck1.packages_delivered + truck2.packages_delivered + truck3.packages_delivered
        total_distance = round(truck1.miles_traveled + truck2.miles_traveled + truck3.miles_traveled, 1)

        print("Total Packages Delivered:", total_packages_delivered)

        print("Truck1 total distance:", round(truck1.miles_traveled, 1), "miles", "packages delivered:",
            truck1.packages_delivered)
        print("Truck2 total distance:", round(truck2.miles_traveled, 1), "miles", "packages delivered:",
            truck2.packages_delivered)
        print("Truck3 total distance:", round(truck3.miles_traveled, 1), "miles", "packages delivered:",
            truck3.packages_delivered)

        print("Total distance:", total_distance, "miles")

def print_time_range(package_hash_table):
    # prints time ranges per requirement D
    if to_print:
        print()
        print("STATUS OF PACKAGES FROM 8:35 AM - 9:25 AM")
        time_range_printout(time(8, 35), time(9, 25), package_hash_table)
        print("STATUS OF PACKAGES FROM 9:35 AM - 10:25 AM")
        time_range_printout(time(9, 35), time(10, 25), package_hash_table)
        print("STATUS OF PACKAGES FROM 12:03 PM - 1:12 PM")
        time_range_printout(time(12, 3), time(13, 12), package_hash_table)

def time_range_printout(time_range_l, time_range_r, package_hash_table):
    # iterate through packages to check for their status against given time
    # methods are different for each truck due to their individual departure time
    for package_id in range(1, 41):
        package = package_hash_table.lookup_package(package_id)
        print("Package " + str(package_id) + ": ", end="")

        if package.get("truck_id") == 1:
            if package.get("delivered_time") < time_range_r:
                delivered_time = package['delivered_time']
                formatted_time = package['delivered_time'].strftime("%I:%M %p")
                print("delivered at", formatted_time)
            else:
                print("en route")

        if package.get("truck_id") == 2:
            if package.get("delivered_time") < time_range_r:
                delivered_time = package['delivered_time']
                formatted_time = package['delivered_time'].strftime("%I:%M %p")
                print("delivered at", formatted_time)
            elif time_range_r < time(9, 5):
                print("at hub on truck 2")
            else: print("en route")

        if package.get("truck_id") == 3:
            if package.get("delivered_time") < time_range_r:
                delivered_time = package['delivered_time']
                formatted_time = package['delivered_time'].strftime("%I:%M %p")
                print("delivered at", formatted_time)
            elif time_range_r < time(10, 20):
                print("at hub on truck 3")
            else: print("en route")

    print()

def package_lookup(package_hash_table):
    # attempt to get valid package id from user
    try:
        package_id_to_lookup = int(input("Enter the Package ID to look up: "))
    except ValueError:
        print("Invalid input. Please enter a valid package ID (a positive integer).")
        return

    found_package = package_hash_table.lookup_package(package_id_to_lookup)

    # if package exists, prompt for time and then print details
    if not found_package:
        print(f"Package {package_id_to_lookup} not found.")
    else:
        requested_time_str = input("Enter time (hh:mm) (blank for EOD): ")

        if not requested_time_str.strip():
            print(package_hash_table.format_package_details(found_package))
        else:
            try:
                requested_time = datetime.strptime(requested_time_str, "%H:%M").time()
                package_hash_table.package_status_in_time(found_package, requested_time)
            except ValueError:
                print("Invalid time format. Please enter in the format hh:mm.")

if __name__ == "__main__":
    main()

def debug_code():
    pass
    # code used during development that helped with debugging

    # # get place name from address
    # input_address = '2530 S 500 E'  # Replace with the desired address
    # place_name = address_reader.get_place_name(input_address)
    # if place_name:
    #     print(f"The place name for the address '{input_address}' is '{place_name}'.")
    # else:
    #     print(f"No matching place name found for the address '{input_address}'.")

    # # Get distance from 'Western Governors University' to 'Sugar House Park'
    # distance = distance_matrix.get_distance('Western Governors University', 'Sugar House Park')
    # print(f"Distance: {distance} miles")