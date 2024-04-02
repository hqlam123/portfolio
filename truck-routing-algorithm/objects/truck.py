from datetime import datetime, timedelta, time
from typing import List
from helpers.package_hash_table import PackageHashTable
from helpers.address_reader import AddressReader
from helpers.distance_reader import DistanceMatrix

class Truck:
    def __init__(self, truck_id, start_time: time, package_hash_table):
        self.package_hash_table = package_hash_table
        self.address_reader = AddressReader()
        self.distance_reader = DistanceMatrix()

        self.id = truck_id
        self.time = start_time
        self.packages_held: List[int] = []  # list of package IDs (held as ints for referencing against hash table)
        
        self.location = "Western Governors University" # all trucks begin at the hub
        self.destination = ""
        
        self.miles_traveled = 0
        self.packages_delivered = 0

    def next_package(self):
        """
        THIS IS THE SORTING ALGORITHM
        It uses nearest neighbor principles.
        The algorithm parses ALL packages and determines the next closest location, prioritizing deadlines.
        This allows a simple yet effective method for package delivery.
        """

        # parse packages held to get earliest deadline
        earliest_deadline = time(23, 59)

        for package_id in self.packages_held:
            the_package = self.package_hash_table.lookup_package(package_id)
            package_deadline = the_package.get("deadline")

            if package_deadline < earliest_deadline:
                earliest_deadline = package_deadline

        # parse packages held again, adding those that match current deadline
        deadline_sublist = []

        for package_id in self.packages_held:
            the_package = self.package_hash_table.lookup_package(package_id)
            package_deadline = the_package.get("deadline")
            
            if package_deadline == earliest_deadline:
                deadline_sublist.append(package_id)

        # return nearest package destination within deadline_sublist
        closest_package = None
        closest_distance = float('inf')

        for package_id in deadline_sublist:
            the_package = self.package_hash_table.lookup_package(package_id)
            current_distance = self.distance_to_destination(the_package.get("address"))

            if (closest_package == None or current_distance < closest_distance):
                closest_package = the_package
                closest_distance = current_distance

        return closest_package.get("package_id")

    def distance_to_destination(self, destination):
        # use AddressReader to get the name from the destination address
        destination_name = self.address_reader.get_place_name(destination)

        # calculate the distance using the updated destination name
        return self.distance_reader.get_distance(self.location, destination_name)

    def load_packages(self, package_ids):
        # this method takes an array of IDs as ints
        for package_id in package_ids:
            # add the package to the truck's held packages
            self.packages_held.append(package_id)

            # retrieve package details based on package ID
            package_details = self.package_hash_table.lookup_package(package_id)

            # set package details
            package_details["truck_id"] = self.id
            package_details["status"] = f"at hub on truck {self.id}"
            package_details["loaded_time"] = self.time

    def remove_package(self, package_id: int):
        # return package details based on ID
        package_details = self.package_hash_table.lookup_package(package_id)

        # update the package details
        package_details["delivery_status"] = "delivered"
        package_details["delivered_time"] = self.time

        self.packages_held.remove(package_id)
            
    def add_time(self, time_to_add: int):
        # adds time to the truck's current "clock"
        self.time += timedelta(minutes=time_to_add)
