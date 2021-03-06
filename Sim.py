# test bed for the simulation process

import Package
import Truck
import DataStructures
# Primary class that "runs" the truck delivery simulation. Instantiating and instance of the simulation requires the
# following parameters:
# 1. filename_of_packages: this is a csv file that includes all of the data for the packages to be delivered.
# 2. filename_of_distances: this is a csv file that lists the distances from every location to every other location.
# The file does not include addresses, but the subsequent filename_address_index is used to create a correlation between
# an address and a location code that the program generates. The application creates "location codes" to be used by the
# program. Each code represents the line number on which is exists in this CSV file. For example the hub is on the first
# line, so it is assigned location code 0
# 3. filename_address_index: This is a list of strings representing an address, as a csv file. The ordering of the
# addresses should match the ordering in the filename_of_distances, so that the numbering of location codes is mapped
# correctly.
# 4. num_of_addresses: How many addresses are included in the distance index
# 5. max_num_package_per_truck : This is default of 16, but this could be altered if in the future truck capacity
# changes.
# Other data members which are created as class members include:
# 1. packages_truck1(2) : These are packages that are loaded into the truck specified. They do not have any limitations
# and it's assumed they can be delivered at any time of day.
# 2. self.packages_with_no_restrictions: All packages start here. When the class is created, all packages are loaded
# onto this list. They are moved into other lists as appropriate.
# 3. packages_with_deadline_truck1(2): These packages need to be delivered by a certain time. They are prioritized
# and will be delivered first.
# 4. packages_not_available: Packages are moved to this list if they are not available at the depot, or if they are not
# ready to be loaded on to a truck.
# 5. total_distance_traveled: This is an aggregate of distances traveled by all trucks.
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
        self.total_distance_traveled = 0
        self.max_num_package_per_truck = max_num_package_per_truck


    # Takes a list of packages. Returns the optimal order they should be delivered in, using a
    # greedy algorithm to compute. Returns a list of packages in the best order using a "nearest neighbor" approach.
    # O(n^2)
    def discoverShortestPathList(self, starting_location, package_list):
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

    # Move a package from one list to another list. Package id is used rather than the actual package object, mostly
    # so that it is easy for an employee to potentially adjust where packages go by their number, rather than
    # having to know which package object a package number correlates with. (more extensible if the program functionality
    # is extended down the line)
    def movePackageFromOneListToAnother(self, source_list, dest_list, package_id):
        package = self.new_packages.returnPackageByID(package_id)
        source_list.remove(package)
        dest_list.append(package)

    # if a package has been loaded on a truck, its status is updated. Runs this on all trucks in a ready status,
    # so it only needs to be run after packages have been newly loaded.
    def updateStatusToLoadedOnTruck(self):
        for package in self.truck1.packages:
            package.updateDeliveryStatus('Loaded on truck 1 for delivery')
        for package in self.truck2.packages:
            package.updateDeliveryStatus('Loaded on truck 2 for delivery')
        for package in self.packages_with_deadline_truck1:
            package.updateDeliveryStatus('Loaded on truck 1 for delivery')
        for package in self.packages_with_deadline_truck2:
            package.updateDeliveryStatus('Loaded on truck 2 for delivery')



    # Manages the loading of trucks and their delivery. End_time is the time after which the simulation will
    # end. If no time is entered end of day is assumed (19:00). In this case, packages are loaded in an order
    # that allows the application to meet the requirements as specified. It would be easy to create additional
    # functionality that would allow more flexibility. This implementaiton is offered as a proof of concept.
    def loadAndDeliver(self, end_time='19:00'):
        # Load packages that must be on specific trucks
        # 3, 18,  36, 38 only on truck 2
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_truck2, 3)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_truck2, 18)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_truck2, 36)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_truck2, 38)

        # 13, 14, 15, 16, 19, 20 must be delivered together so they will go on truck 1. 13, 14, 16, 20
        # are early packages)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_truck1, 19)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1, 15)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1, 13)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1, 14)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1, 16)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1, 20)


        # 29, 30, 31, 34, 37, 40 by 10:30 am, split evenly between two trucks. (25 arrives late)Run through
        # optimization first, so that the order is as beneficial as possible.
        # 6 is a unique case, because it needs to delivered by 10:30 but won't be available until 9:05, so it's
        # not included heree
        list_adjacent = [1, 29, 30, 31, 34, 37, 40]
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
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_not_available, 9)
        for package in self.packages_not_available:
            package.updateDeliveryStatus(f"Awaiting package at hub - in Transit")
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

        # Take of list of packages and send them through the optimization algorithm. This serves the purpose of grouping
        # packages more closely to one another - hopefully avoiding the trucks having to cross paths more often than
        # necessary.
        optimized_list = self.discoverShortestPathList(0, to_deliver)

        # Split the optimized list into two lists, of the correct size for each truck
        list_truck1 = optimized_list[:total_num_packages_remaining_truck1]
        list_truck2 = optimized_list[total_num_packages_remaining_truck1:]

        # Load truck 1
        while list_truck1:
            self.movePackageFromOneListToAnother(list_truck1, self.packages_truck1, list_truck1[0].id)


        #  and truck 2
        while list_truck2:
            self.movePackageFromOneListToAnother(list_truck2, self.packages_truck2, list_truck2[0].id)

        # copy lists over to the truck's list
        self.truck1.packages = self.packages_truck1
        self.truck2.packages = self.packages_truck2

        # Now that everything is loaded, update the statuses of the loaded trucks.
        self.updateStatusToLoadedOnTruck()

        # Truck two will report to depot to pick up package 9 (appended last because of a delayed
        # address 10:05). Add 6, 25, 28, 32 available at 9:05. Truck 2 will run the simulation until 9:05
        # or until the given end_time, whichever is earlier.
        self.runIndividualTruckSimulation(self.truck1, self.packages_with_deadline_truck1, end_time)
        if self.determineIfTimeIsAfter('09:05', end_time):
            self.runIndividualTruckSimulation(self.truck2, self.packages_with_deadline_truck2, '09:05')
        else:
            self.runIndividualTruckSimulation(self.truck2, self.packages_with_deadline_truck2, end_time)

        # This stops the simulation from running and subsequently loading truck 2 again if the given end time
        # falls before 9:05
        if self.determineIfTimeIsAfter(end_time, '09:05'):
            return

        # Add the late packages to truck 2
        self.movePackageFromOneListToAnother(self.packages_not_available, self.packages_with_deadline_truck2, 6)
        self.movePackageFromOneListToAnother(self.packages_not_available, self.packages_with_deadline_truck2, 25)
        self.movePackageFromOneListToAnother(self.packages_not_available, self.truck2.packages, 28)
        self.movePackageFromOneListToAnother(self.packages_not_available, self.truck2.packages, 32)
        self.movePackageFromOneListToAnother(self.packages_not_available, self.truck2.packages_to_hold, 9)
        self.truck2.packages_to_hold[0].updateDeliveryStatus('Loaded on truck 2 for delivery')

        # if there is any space remaining, load truck 2 until it's full.
        truck_space = self.max_num_package_per_truck - (len(self.packages_with_deadline_truck2) +
                                                        len(self.truck2.packages) + len(self.truck2.packages_to_hold))
        to_load = self.packages_with_no_restrictions[:truck_space]

        # Optimize the route
        optimize = self.discoverShortestPathList(0, to_load)
        for package in optimize:
            self.truck2.packages.append(package)
            self.packages_with_no_restrictions.remove(package)

        # Update load status
        self.updateStatusToLoadedOnTruck()

        # Deliver until the given end time
        self.runIndividualTruckSimulation(self.truck2, self.packages_with_deadline_truck2, end_time)

    # Run a delivery simulation. Truck is the truck object doing the delivery. Special_handling is a list of
    # packages that must be run first . Time is the spot after which the simulation
    # should stop. So if the time from 8:00 to 8:15 were to be reviewed, this would be looking for times after 8:00
    def runIndividualTruckSimulation(self, truck, special_handling, time):
        # deliver time sensitive packages first
        # Hand deliver the earliest delivery, so that it makes it on time.
        current_location = 0  # At depot
        delivered = []  # tracks delivered packages so they can be removed from the appropriate list.
        # There is a package that needs to be updated so these variables will manage that
        update_address = True
        update_time = '10:20'
        # Delivers all special handling (ie early) packages until there are either no packages on this list remaining,
        # or, the time given has elapsed. The application checks the time at each delivery point, but will not stop while
        # on route
        while special_handling:
            next_destination = self.calculateClosestVertex(current_location, special_handling)
            self.deliverPackage(truck, next_destination, current_location)
            current_location = next_destination.location_code
            special_handling.remove(next_destination)
            if truck.determineIfTimeIsAfter(time):
                self.returnToDepotAddMiles(truck, current_location)
                return
            if truck.determineIfTimeIsAfter(update_time) and update_address:
                address_to_update = self.new_packages.packageHash.findDataInHashTable(9)
                address_to_update.updateAddress('410 S State St', 'Salt Lake City', '84111')
                update_address = False
        for item in delivered:
            if item in special_handling:
                special_handling.remove(item)
        # Deliver the remaining packages using some optimization to reduce overall mileage
        # for packages in truck.packages:
        while truck.packages:
            next_stop = self.calculateClosestVertex(current_location, truck.packages)
            truck_time = self.deliverPackage(truck, next_stop, current_location)
            current_location = next_stop.location_code
            truck.packages.remove(next_stop)
            if truck.determineIfTimeIsAfter(time):
                return
            if truck.determineIfTimeIsAfter(update_time) and update_address == True:
                address_to_update = self.new_packages.packageHash.findDataInHashTable(9)
                address_to_update.updateAddress('410 S State St', 'Salt Lake City', '84111', 20)
                update_address = False

        # Finally deliver packages that needed to be held for later delivery
        for item in truck.packages_to_hold:
            truck_time = self.deliverPackage(truck, item, current_location)
            current_location = item.location_code
            truck.packages_to_hold.remove(item)
            if truck.determineIfTimeIsAfter(time):
                return
            if truck.determineIfTimeIsAfter(update_time) and update_address == True:
                address_to_update = self.new_packages.packageHash.findDataInHashTable(9)
                address_to_update.updateAddress('410 S State St', 'Salt Lake City', '84111', 20)
                update_address = False

        # If we reach the end before time, return to the depot
        self.returnToDepotAddMiles(truck, current_location)

    # Deliver package. Update truck time and distance traveled. Update package status, and return current truck time
    def deliverPackage(self, truck, package, current_location):
        distance_traveled = self.new_packages.address_matrix.lookupDistance(current_location, package.location_code)
        truck_time = truck.deliverPackage(distance_traveled)
        self.updateTotalMiles(distance_traveled)
        package.updateDeliveryStatus(f"Delivered at {truck.truck_time}, On Truck {truck.truck_number}")

        return truck_time

    # adds distance to the total miles traveled for both trucks. Is incremented everytime a delivery is made, or when
    # a truck returns to the depot
    def updateTotalMiles(self, distance):
        self.total_distance_traveled = self.total_distance_traveled + distance

    # Calculates the number of miles needed to get from the current location back to the depot. Increments the mileage
    # of the truck and it's clock. Adds mileage to the total distance traveled during the simulation
    def returnToDepotAddMiles(self, truck, current_location):
        distance_traveled = self.new_packages.address_matrix.lookupDistance(current_location, 0)
        truck_time = truck.deliverPackage(distance_traveled)
        self.updateTotalMiles(distance_traveled)

    # determines if time 2 is later than time 1
    def determineIfTimeIsAfter(self, time1, time2):
        hour_time1, minute_time1 = map(int, time1.split(':'))
        hour_time2, minute_time2 = map(int, time2.split(':'))

        if hour_time2 > hour_time1:
            return True
        else:
            if hour_time2 < hour_time1:  # if given hour is before objects hour
                return False
            else:
                if minute_time2 < minute_time1:  # if given minute is before objects minutes
                    return False
                else:
                    return True


