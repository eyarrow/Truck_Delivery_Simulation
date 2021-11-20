# Module to manage Classes and functionality that are used to run the delivery simulation
import Package
import Truck

# Parameters:
# list_of_trucks - a list of integers representing individual trucks. The integer given should correspond with the truck
# number
# filename_of_packages - filename of csv file that lists packages to be delivered
# filename_of_distances - filename of csv file that includes distances between addresses for the day's deliveries
# filename_address_index - filename of csv file that is used to map a numerical value to an address
# num_of_addresses - Number of addresses included in days delivery
class Simulation:
    def __init__(self, list_of_trucks, filename_of_packages, filename_of_distances, filename_address_index,
                 num_of_addresses, max_num_package_per_truck=16):
        self.new_packages = Package.PackagesToBeDelivered(filename_of_packages, filename_of_distances,
                                                          filename_address_index, num_of_addresses)
        self.truck_list = self.initializeTrucks(list_of_trucks)
        self.num_of_trucks = len(self.truck_list)
        self.total_distance_traveled = 0
        self.clock = '08:00'
        self.specific_truck_requests = []  # Packages that must be delivered on a specific truck
        self.timed_requests = []  # Packages that must be delivered before or after a given time.
        self.max_num_package_per_truck = max_num_package_per_truck
        self.packages_to_be_delivered = self.new_packages.returnPackageIndices()

    # Takes a list of package numbers. Returns the optimal order they should be delivered in, using a
    # greedy algorithm to compute. Returns a list of package numbers. Emulates a "nearest neighbor" approach
    def discoverShortestPath(self, starting_location_code, package_list):
        vertex_list = []  # Holds the list of location codes
        package_with_code = {}
        nearest_neighbor_list = []
        sorted_return_list = []
        # Create a list of tuples that pairs the package number and location_code in the format:
        # (package_number, location_code). This provides a list that can be returned to the calling
        # function.
        for item in package_list:
            package = self.new_packages.packageHash.findDataInHashTable(item)
            location_code = package.returnLocationCode()
            vertex_list.append(location_code)
            package_with_code[package.id] = location_code

        # Get the ideal ordering for delivering the given packages. Produces the list of location codes
        # in order.
        while vertex_list:
            nearest_neighbor = self.calculateClosestVertex(starting_location_code, vertex_list)
            nearest_neighbor_list.append(nearest_neighbor)
            starting_location_code = nearest_neighbor
            vertex_list.remove(nearest_neighbor)

        # sort tuples in the correct order
        list_of_packages_to_return = []
        for i in range(len(nearest_neighbor_list)):
            for key, value in package_with_code.items():
                if nearest_neighbor_list[i] == value and key not in sorted_return_list:
                    sorted_return_list.append(key)

        return sorted_return_list




    # takes a location code,and a list of potential adjacent vertices. Returns the one that is closest
    def calculateClosestVertex(self, starting_vertex, potential_adjacent):
        shortest_distance = 0
        closest_vertex = 0
        for i in range(len(potential_adjacent)):
            distance = self.new_packages.address_matrix.lookupDistance(starting_vertex, potential_adjacent[i])
            if shortest_distance == 0 and closest_vertex == 0:
                shortest_distance = distance
                closest_vertex = potential_adjacent[i]
            else:
                if shortest_distance > distance:
                    shortest_distance = distance
                    closest_vertex = potential_adjacent[i]
        return closest_vertex





    # initializes a set of trucks to be used for the day. Uses the truck numbers as assigned by the calling application
    def initializeTrucks(self, list_of_trucks):
        truck_list = []
        for truck in list_of_trucks:
            new_truck = Truck.Truck(truck)
            truck_list.append(new_truck)
        return truck_list

    # used for adding packages that have recently arrived at the depo
    def newPackagesAtDepot(self, list_of_packages):
        for item in list_of_packages:
            self.packages_to_be_delivered.append(item)
            package_to_update = self.new_packages.packageHash.findDataInHashTable(item)
            package_to_update.updateDeliveryStatus('at the hub')

    # Used to enter packages that need to be on a specific truck. This might be a route requirement, or can be used
    # to keep specific packages delivered together. The value of "truck" is an integer that is the truck number.
    # list_of_packages are the packages that must be delivered on the given truck.
    def truckSpecificDelivery(self, truck, list_of_packages):
        for item in list_of_packages:
            truck_specific_tuple = (truck, item)
            self.specific_truck_requests.append(truck_specific_tuple)
        # Load onto the appropriate truck
        for i in range(len(self.specific_truck_requests)):
            truck = self.specific_truck_requests[i][0]
            package = self.specific_truck_requests[i][1]
            for i in range(len(self.truck_list)):
                if self.truck_list[i].truck_number == truck:
                    self.truck_list[i].addToPackageList(package)
                    self.packages_to_be_delivered.remove(package)
                    status_string = f"Loaded on Truck {self.truck_list[i].truck_number} - out for delivery"
                    self.new_packages.updateStatusByPackageID(package, status_string)
        self.specific_truck_requests = []

    # Checks to see if a priority (timed) package is already loaded on a particular truck. If it is, it's moved
    # to the correct list for delivery
    def addTimedRequests(self, time, before_after, package_number):
        # Check if the package is already loaded. If it is, move from regular package list to priority
        check_if_on_truck = False
        for truck in self.truck_list:
            exists_already = truck.checkIfPackageOnPackageList(package_number)
            if exists_already:
                truck.moveFromNormalDeliveryToTimedDelivery(time, before_after, package_number)
                check_if_on_truck = True
        return check_if_on_truck

    # Used to enter packages that have a time restriction to their delivery parameters. Parameters are: time, which
    # represents the time constraint. before_after is an integer, where 0 means the package needs to be delivered
    # before the given time, and 1 means after. list_of_packages are a list of packages that need to meet the said
    # requirement. It creates a list of tuples which are used to determine delivery logic. If the package is already
    # loaded on a truck, that truck is updated to move the package to the priority list.
    def setTimeSensitiveDeliveryTimes(self, time, before_after, list_of_packages):
        for item in list_of_packages:
            delivery_requirements_tuple = (time, before_after, item)
            check_if_on_truck = self.addTimedRequests(time, before_after, item)
            if check_if_on_truck is False:
                self.timed_requests.append(delivery_requirements_tuple)

    # Loads the remaining timed deliveries and attempts to distribute them evenly across trucks.
    def loadRemainingTimedDeliveries(self):
        # Determine the least loaded truck
        greatest_truck = Truck.Truck()
        least_truck = Truck.Truck()
        offset = 0
        truck1_packages = self.truck_list[0].num_of_packages + self.truck_list[0].num_of_timed_packages
        truck2_packages = self.truck_list[1].num_of_packages + self.truck_list[1].num_of_timed_packages
        # if truck1_packages == truck2_packages: Special case offset can stay one
        if truck1_packages > truck2_packages:
            greatest_truck = self.truck_list[0]
            least_truck = self.truck_list[1]
            offset = truck1_packages - truck2_packages
        if truck2_packages > truck1_packages:
            greatest_truck = self.truck_list[1]
            least_truck = self.truck_list[0]
            offset = truck2_packages - truck1_packages

        # Split the packages between two trucks
        deliver_list = []
        for i in range(len(self.timed_requests)):
            delivery = self.timed_requests[i][2]
            deliver_list.append(delivery)
        deliver_list = self.discoverShortestPath(0, deliver_list)
        length = len(deliver_list)
        mid = length // 2
        mid = mid + offset
        list1 = deliver_list[:mid] # presumably could be larger list, so needs to go to bigger truck
        list2 = deliver_list[mid:]

        # least_loaded_truck = 0
        # max = 0
        # index = 0
        # loaded_deliveries = []
        # while self.timed_requests:
        #     for trucks in self.truck_list:
        #         num = trucks.num_of_timed_packages
        #         if max == 0:
        #             max = num
        #             least_loaded_truck = trucks.truck_number
        #         else:
        #             if num < max:
        #                 least_loaded_truck = trucks.truck_number
        #             else:  # num is greater than max, num is the new max
        #                 max = num
        # Add the package to the least loaded truck
        if offset == 0:   # list is evenly divided
            self.truck_list[0].packages.append(list1)
            self.truck_list[1].packages.append(list2)
        else:
            greatest_truck.packages.append(list1)
            least_truck.packages.append(list2)
            # time = self.timed_requests[index][0]
            # before_after = self.timed_requests[index][1]
            # package_number = self.timed_requests[index][2]
            # self.loadTimedPackagedByTruckNumber(least_loaded_truck, time, before_after, package_number)
            # package_tuple = (time, before_after, package_number)
            self.timed_requests = []
           # self.loaded_deliveries.append(list1_delivery_order)

            # for item in self.packages_to_be_delivered:
            #     if item == package_number:
            #         self.packages_to_be_delivered.remove(package_number)


    # Load specific package to specific truck
    def loadPackageByTruckNumber(self, truck_number, package_number):
        for truck in self.truck_list:
            if truck.truck_number == truck_number:
                truck.addToPackageList(package_number)
                self.packages_to_be_delivered.remove(package_number)
                status_string = f"Loaded on Truck {truck.truck_number} - out for delivery"
                self.new_packages.updateStatusByPackageID(package_number, status_string)

    # load a package with time constraints to a given truck
    def loadTimedPackagedByTruckNumber(self, truck_number, time, before_after, package_number):
        for truck in self.truck_list:
            if truck.truck_number == truck_number:
                truck.addToTimedDeliveryList(time, before_after, package_number)
                status_string = f"Loaded on Truck {truck.truck_number} - out for delivery"
                self.new_packages.updateStatusByPackageID(package_number, status_string)

    # print the package list with current status
    def printPackagesCurrentStatus(self):
        self.new_packages.printAllPackages()

    # Removes packages from the self.packages_to_be_delivered list. These may be packages
    # that are not ready to be delivered for whatever reason.
    def removePackagesThatAreNotReadyAtDepo(self, list_of_package_numbers):
        for item in list_of_package_numbers:
            self.packages_to_be_delivered.remove(item)
            package_to_update = self.new_packages.packageHash.findDataInHashTable(item)
            package_to_update.updateDeliveryStatus('Delayed, Depot is awaiting arrival')

    # Loads trucks with packages up to their capacity
    def loadTrucksToMaxCapacity(self):
        for truck in self.truck_list:
            current_load = truck.num_of_timed_packages + truck.num_of_packages
            while current_load < self.max_num_package_per_truck:
                self.loadPackageByTruckNumber(truck.truck_number, self.packages_to_be_delivered[0])
                current_load = current_load + 1

    # "delivers" packages, calculates miles traveled and time expended.
    def updateDelivery(self, truck, location_code1, location_code2, list_of_packages_to_deliver):
        # determine distance
        distance = self.new_packages.address_matrix.lookupDistance(location_code1, location_code2)
        # deliver package
        time = truck.deliverPackage(list_of_packages_to_deliver[0], distance)
        self.total_distance_traveled = self.total_distance_traveled + distance
        self.new_packages.updateStatusByPackageID(list_of_packages_to_deliver[0], f"Delivered at {time}")

    # Returns true if time to check falls within the timerange
    def determineIfDeliveryFallsInTimeRange(self, start_time, end_time, time_to_check):
        time_to_check = time_to_check[:5]
        start_hour, start_minute = map(int, start_time.split(':'))
        end_hour, end_minute = map(int, end_time.split(':'))
        time_to_check_hour, time_to_check_minute = map(int, time_to_check.split(':'))
        if start_hour < time_to_check_hour < end_hour:
            return True
        if start_hour > time_to_check_hour > end_hour:
            return False
        else:
            if start_hour == time_to_check_hour and time_to_check_hour < end_hour:
                return True
            elif start_hour == time_to_check_hour and time_to_check_hour == end_hour:
                if start_minute < time_to_check_minute < end_minute:
                    return True
                else:
                    return False
            else:
                return False



    # Load the trucks for this simulation. Based on the parameters of this scenario, this assumes 2 trucks,
    # but the program could easily be modified to accomodate more, and most functions are written to be used
    # with any number of trucks.
    def loadTrucks(self):
        # Load packages that need to be on specific trucks, including those that need to be delivered early
        list1 = (15, 13, 14, 16, 20, 19)
        for item in list1:
            self.truck_list[0].packages.append(item)
        self.truck_list[0].num_of_packages = self.truck_list[0].num_of_packages + len(list1)
        status_string = f"Loaded on Truck 1 - out for delivery"
        for item in list1:
            self.new_packages.updateStatusByPackageID(item, status_string)
        list2 = (29, 30, 31, 34, 37, 40, 3, 18, 36, 38)
        for item in list2:
            self.truck_list[1].packages.append(item)
        self.truck_list[1].num_of_packages = self.truck_list[1].num_of_packages + len(list2)
        status_string = f"Loaded on Truck 2 - out for delivery"
        for item in list2:
            self.new_packages.updateStatusByPackageID(item, status_string)
        remove_list = list1 + list2
        for item in self.packages_to_be_delivered:  # remove assigned packages
            for package in remove_list:
                if item == package:
                    self.packages_to_be_delivered.remove(item)
        self.packages_to_be_delivered.remove(9)
        self.removePackagesThatAreNotReadyAtDepo([6, 25, 28, 32])
        remove_list = []
        for truck in self.truck_list:
            while truck.num_of_packages < 16 and len(self.packages_to_be_delivered) > 0:
                item = self.packages_to_be_delivered[0]
                truck.packages.append(item)
                truck.num_of_packages = truck.num_of_packages + 1
                self.packages_to_be_delivered.remove(item)

        # run delivery of first set of packages
        self.runTruckSimulation()

        # re-load trucks, now at the depo
        self.newPackagesAtDepot([25, 28, 32])
        self.packages_to_be_delivered.append(9)
        self.packages_to_be_delivered.sort()

        # Update address on package 9, this needs to happen after 10:05
        address_to_update = self.new_packages.packageHash.findDataInHashTable(9)
        address_to_update.updateAddress('410 S State St', 'Salt Lake City', '84111')

        # Deliver package 6:
        # self.truck_list[0].packages = [6]
        # self.runTruckSimulation()
        # sort remaining packages into the most advantageous order ahead of time to consolidate packages
        sorted_order = self.discoverShortestPath(0, self.packages_to_be_delivered)
        self.packages_to_be_delivered = [6]
        for item in sorted_order:
            self.packages_to_be_delivered.append(item)

        # Split the list between the trucks
        mid = len(self.packages_to_be_delivered) // 2
        list1 = self.packages_to_be_delivered[:mid]
        list2 = self.packages_to_be_delivered[mid:]

        # Load truck 1
        for item in list1:
            self.truck_list[0].num_of_packages = self.truck_list[0].num_of_packages + 1
            self.truck_list[0].packages.append(item)
            self.packages_to_be_delivered.remove(item)

        # Load truck 2
        for item in list2:
            self.truck_list[1].num_of_packages = self.truck_list[1].num_of_packages + 1
            self.truck_list[1].packages.append(item)
            self.packages_to_be_delivered.remove(item)

        self.runTruckSimulation()

        print("harry")
        self.total_distance_traveled = self.truck_list[0].miles + self.truck_list[1].miles



    # Used to manage time specific events - makes sure that the trucks perform needed tasks at the right time.
    def checkTime(self, truck):
        print("loverly")


    # Run a singular truck simulation. Will run the simulation until the time specified. (falling between
    # time_start, and time_end
    def runTruckSimulation(self):
        # start with timed packages
        list_to_deliver = []
        num_of_packages_delivered = 0
        current_location = 0
        move_to_regular_packages = []

        # Now regular packages, until there are no packages
        for truck in self.truck_list:
            to_deliver = truck.packages
            to_deliver = self.discoverShortestPath(current_location, to_deliver)
            total_miles = 0
            while len(to_deliver) > 0:
                location_code2 = self.new_packages.returnLocationCode(to_deliver[0])
                self.updateDelivery(truck, current_location, location_code2, to_deliver)
                current_location = location_code2
                item = to_deliver[0]
                to_deliver.remove(item)
               # if self.determineIfDeliveryFallsInTimeRange(time_start, time_end, truck.truck_time):
                   # return True
            truck.updatePackageList()
            # now drive back to the depot
             # add miles
            distance_to_depot = self.new_packages.address_matrix.lookupDistance(current_location, 0)
            truck.miles = truck.miles + distance_to_depot
            # add time
            time_elapsed = distance_to_depot / 18
            minutes = time_elapsed * 60
            truck.addTimeToClock(minutes)
            print(f"Truck {truck.truck_number} added {minutes} minutes")



        # Update address package 9
        # address_to_update = self.new_packages.packageHash.findDataInHashTable(9)
        # address_to_update.updateAddress('410 S State St', 'Salt Lake City', '84111')
        # # check back on timed delivery packages
        # for truck in self.truck_list:
        #     list_to_deliver = truck.getTimeSensitivePackagesList(self.new_packages)
        #     list_to_deliver = self.discoverShortestPath(current_location, list_to_deliver)
        #     while len(list_to_deliver) > 0:
        #         location_code2 = self.new_packages.returnLocationCode(list_to_deliver[0])
        #         self.updateDelivery(truck, current_location, location_code2, list_to_deliver)
        #         current_location = location_code2
        #         item = list_to_deliver[0]
        #         list_to_deliver.remove(item)
        #         if self.determineIfDeliveryFallsInTimeRange(time_start, time_end, truck.truck_time):
        #             return True

    # reload the trucks after first run. Used for subsequent runs.
    def reloadTrucks(self):
        for truck in self.truck_list:
            truck.num_of_timed_packages = 0
            truck.num_of_packages = 0
            truck.packages = []
            truck.packages_timed_delivery = []
        self.loadRemainingTimedDeliveries()
        #split remaining load between the trucks.
        least_loaded_truck = 0
        max = 0
        index = 0
        loaded_deliveries = []
        while self.packages_to_be_delivered:
            for trucks in self.truck_list:
                num = trucks.num_of_packages
                if max == 0:
                    max = num
                    least_loaded_truck = trucks.truck_number
                else:
                    if num < max:
                        least_loaded_truck = trucks.truck_number
                    else:  # num is greater than max, num is the new max
                        max = num
            package = self.packages_to_be_delivered[0]
            self.loadPackageByTruckNumber(least_loaded_truck, self.packages_to_be_delivered[0])
            loaded_deliveries.append(package)







    # Used to deliver subsequent loads of trucks
    def deliverSubsequentRounds(self):
        current_location = 0
        for truck in self.truck_list:
            list_to_deliver = truck.getTimeSensitivePackagesList(self.new_packages)
            list_to_deliver = self.discoverShortestPath(current_location, list_to_deliver)
            while len(list_to_deliver) > 0:
                location_code2 = self.new_packages.returnLocationCode(list_to_deliver[0])
                self.updateDelivery(truck, current_location, location_code2, list_to_deliver)
                current_location = location_code2
                item = list_to_deliver[0]
                list_to_deliver.remove(item)

                # Now regular packages, until there are no packages
                for truck in self.truck_list:
                    delivered = []
                    to_deliver = truck.packages
                    to_deliver = self.discoverShortestPath(current_location, to_deliver)
                    total_miles = 0
                    while len(to_deliver) > 0:
                        location_code2 = self.new_packages.returnLocationCode(to_deliver[0])
                        self.updateDelivery(truck, current_location, location_code2, to_deliver)
                        current_location = location_code2
                        item = to_deliver[0]
                        to_deliver.remove(item)
                truck.updatePackageList(to_deliver)
                for item in delivered:
                    self.packages_to_be_delivered.remove(item)

        for truck in self.truck_list:
            print(f"Truck {truck.truck_number} drove {truck.miles} miles")


    def runTimeSensitiveDelivery(self, time_start, time_end):
        # Load packages that need to be on specific trucks
        self.truckSpecificDelivery(2, [3, 18, 36, 38])  # requirement: loaded on truck 2
        self.truckSpecificDelivery(1, [13, 14, 15, 16, 19, 20])  # req: must be delivered together

        # Load parameters for time sensitive deliveries
        self.setTimeSensitiveDeliveryTimes('10:30', 0, [13, 14, 16, 20, 29, 30, 31, 34, 37, 40])
        self.setTimeSensitiveDeliveryTimes('09:00', 0, [15])
        self.setTimeSensitiveDeliveryTimes('10:20', 1, [9])  # needs delivery address updated

        # Load any time sensitive packages onto trucks that have not been loaded already
        self.loadRemainingTimedDeliveries()
        self.removePackagesThatAreNotReadyAtDepo([6, 25, 28, 32])

        # Load the rest of the packages until the trucks are full
        self.loadTrucksToMaxCapacity()
        run_result = self.runTruckSimulation(time_start, time_end)
        if run_result:
            return



















