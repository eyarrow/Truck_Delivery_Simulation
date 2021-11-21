# test bed for the simulation process

import Package
import Truck
import DataStructures

class Simulation:
    def __init__(self, filename_of_packages, filename_of_distances, filename_address_index,
                 num_of_addresses, max_num_package_per_truck=16):
        self.new_packages = Package.PackagesToBeDelivered(filename_of_packages, filename_of_distances,
                                                          filename_address_index, num_of_addresses)
        self.truck1 = Truck.Truck(1)
        self.truck2 = Truck.Truck(2)
        self.packages_truck1 = []  # packages on truck 1
        self.packages_truck2 = []  # packages on truck 2
        self.packages_with_deadline_truck1 = []  # packages that have a specific deadline for delivery
        self.packages_with_deadline_truck2 = []
        self.packages_not_available = []  # packages that are not available at the depot
        self.packages_with_no_restrictions = self.new_packages.returnAllPackages()  # packages that have no delivery
                                                    # restrictions. to start, this is loaded with all packages
        self.packages_that_are_delivered = []  # packages that have been delivered
        self.total_distance_traveled = 0
        self.timed_requests = []  # Packages that must be delivered before or after a given time.
        self.max_num_package_per_truck = max_num_package_per_truck


    # Takes a list of packages. Returns the optimal order they should be delivered in, using a
    # greedy algorithm to compute. Returns a list of packages in the best order using a "nearest neighbor" approach.
    # O(n^2)
    def discoverShortestPathList(self, starting_location, package_list):
        # Get the ideal ordering for delivering the given packages. Produces the list of location codes
        # in order.
        nearest_neighbor_list = []
        while package_list:
            nearest_neighbor = self.calculateClosestVertex(starting_location, package_list)
            nearest_neighbor_list.append(nearest_neighbor)
            starting_location = nearest_neighbor.location_code
            package_list.remove(nearest_neighbor)
        return nearest_neighbor_list

    # takes a location code,and a list of potential adjacent vertices. Returns the one that is closest
    def calculateClosestVertex(self, starting_location, potential_adjacent):
        shortest_distance = 0
        closest_vertex = 0
        for i in range(len(potential_adjacent)):
            distance = self.new_packages.address_matrix.lookupDistance(starting_location,
                                                                       potential_adjacent[i].location_code)
            if shortest_distance == 0 and closest_vertex == 0:
                shortest_distance = distance
                closest_vertex = potential_adjacent[i]
            else:
                if shortest_distance > distance:
                    shortest_distance = distance
                    closest_vertex = potential_adjacent[i]
        return closest_vertex

    # Move a package from one list to another list
    def movePackageFromOneListToAnother(self, source_list, dest_list, package_id):
        package = self.new_packages.returnPackageByID(package_id)
        source_list.remove(package)
        dest_list.append(package)

    # if a package has been loaded on a truck, its status is updated. Runs this on all trucks in a ready status,
    # so not necessary to run more than once
    def updateStatusToLoadedOnTruck(self):
        for package in self.packages_truck1:
            package.updateDeliveryStatus('Loaded on truck 1 for delivery')
        for package in self.packages_truck2:
            package.updateDeliveryStatus('Loaded on truck 2 for delivery')
        for package in self.packages_with_deadline_truck1:
            package.updateDeliveryStatus('Loaded on truck 1 for delivery')
        for package in self.packages_with_deadline_truck2:
            package.updateDeliveryStatus('Loaded on truck 1 for delivery')


    # Manages the initial loading of the trucks
    def initialLoad(self):
        # Load packages that must be on specific trucks
        # 3, 18,  36, 38 only on truck 2
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_truck2, 3)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_truck2, 18)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_truck2, 36)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_truck2, 38)

        # Load packages that must be delivered early
        # 15 by 9 AM
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1, 15)

        # 13, 14, 16, 20, 29, 30, 31, 34, 37, 40 by 10:30 am, split evenly between two trucks. (25 arrives late)Run through
        # optimization first, so that the order is as beneficial as possible.
        # 6 is a unique case, because it needs to delivered by 10:30 but won't be available until 9:05
        list_adjacent = [1, 13, 14, 16, 20, 29, 30, 31, 34, 37, 40]
        adjacent_packages = []
        while list_adjacent:
            for i in range(len(self.packages_with_no_restrictions)):
                if self.packages_with_no_restrictions[i].id == list_adjacent[0]:
                    adjacent_packages.append(self.packages_with_no_restrictions[i])
                    list_adjacent.remove(self.packages_with_no_restrictions[i].id)

        ordered_list = self.discoverShortestPathList(0, adjacent_packages)
        # split the list in half, and distribute amongst the two trucks.
        mid = len(ordered_list) // 2
        list1 = ordered_list[mid:]
        list2 = ordered_list[:mid]

        # Load the time sensitive lists onto the trucks
        for item in list1:
            self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1,
                                                 item.id)
        for item in list2:
            self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck2,
                                                 item.id)


        # Remove packages that are not available at first load
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_not_available, 6)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_not_available, 25)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_not_available, 28)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_not_available, 32)

        # See how many openings are left
        # truck 1
        total_num_packages_remaining_truck1 = len(self.packages_truck1 + self.packages_with_deadline_truck1)
        total_num_packages_remaining_truck2 = len(self.packages_truck2 + self.packages_with_deadline_truck2)

        total_num_packages_to_pull = total_num_packages_remaining_truck1 + total_num_packages_remaining_truck2
        # peel of some packages from the remaining ones
        to_deliver = []
        for i in range(total_num_packages_to_pull):
            to_deliver.append(self.packages_with_no_restrictions[i])
        self.packages_with_no_restrictions = self.packages_with_no_restrictions[total_num_packages_to_pull:]

        optimized_list = self.discoverShortestPathList(0, to_deliver)
        list_truck1 = optimized_list[:total_num_packages_remaining_truck1]
        list_truck2 = optimized_list[total_num_packages_remaining_truck1:]

        # Load truck 1
        while list_truck1:
            self.movePackageFromOneListToAnother(list_truck1, self.packages_truck1, list_truck1[0].id)


        #  and truck 2
        while list_truck2:
            self.movePackageFromOneListToAnother(list_truck2, self.packages_truck2, list_truck2[i].id)

        self.truck1.packages = self.packages_truck1
        self.truck2.packages = self.packages_truck2

        self.updateStatusToLoadedOnTruck()

        self.runIndividualTruckSimulation(self.truck1, self.packages_with_deadline_truck1, '19:00')
        self.runIndividualTruckSimulation(self.truck2, self.packages_with_deadline_truck2, '19:00')
        print(f"Total travel miles truck 1: {self.truck1.miles}")
        print(f"Total travel miles truck 2: {self.truck2.miles}")


    # Run a delivery simulation. Truck is the truck object doing the delivery. Special_handling is a list of
    # packages that must be run first (so used outside of optimization. Time is the spot after which the simulation
    # should stop. So if the time from 8:00 to 8:15 were to be reviewed, this would be looking for times after 8:00
    def runIndividualTruckSimulation(self, truck, special_handling, time):
        # deliver time sensitive packages first
        # Hand deliver the earliest delivery, so that it makes it on time. (needs to be reusable for subs delivery
        current_location = 0  # At depot
        delivered = []  # tracks delivered packages so they can be removed from the appropriate list.
        for item in special_handling:
            truck_time = self.deliverPackage(truck, item, current_location)
            current_location = item.location_code
            if truck.determineIfTimeIsAfter(time):
                return
        # Deliver the remaining packages using some optimization to reduce overall mileage
        # for packages in truck.packages:
        while truck.packages:
            next_stop = self.calculateClosestVertex(current_location, truck.packages)
            truck_time = self.deliverPackage(truck, truck.packages[0], current_location)
            current_location = next_stop.location_code
            truck.packages.remove(truck.packages[0])
            if truck.determineIfTimeIsAfter(time):
                return

        # If we reach the end before time, return to the depot
        self.returnToDepotAddMiles(truck, current_location)




    # Deliver package. Update truck time and distance traveled. Update package status, and return current truck time
    def deliverPackage(self, truck, package, current_location):
        distance_traveled = self.new_packages.address_matrix.lookupDistance(current_location, package.location_code)
        truck_time = truck.deliverPackage(distance_traveled)
        self.updateTotalMiles(distance_traveled)
        package.updateDeliveryStatus(f"Delivered at {truck.truck_time}")

        return truck_time

    # adds distance to the total miles traveled for both trucks
    def updateTotalMiles(self, distance):
        self.total_distance_traveled = self.total_distance_traveled + distance

    # Calculates the number of miles needed to get from the current location back to the depot. Increments the mileage of
    # the truck and it's clock. Adds mileage to the total distance
    def returnToDepotAddMiles(self, truck, current_location):
        distance_traveled = self.new_packages.address_matrix.lookupDistance(current_location, 0)
        truck_time = truck.deliverPackage(distance_traveled)
        self.updateTotalMiles(distance_traveled)

