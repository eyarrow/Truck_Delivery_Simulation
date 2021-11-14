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
        self.clock = '08:00'
        self.specific_truck_requests = []  # Packages that must be delivered on a specific truck
        self.timed_requests = []  # Packages that must be delivered before or after a given time.
        self.max_num_package_per_truck = max_num_package_per_truck
        self.packages_to_be_delivered = self.new_packages.returnPackageIndices()

    # initializes a set of trucks to be used for the day. Uses the truck numbers as assigned by the calling application
    def initializeTrucks(self, list_of_trucks):
        truck_list = []
        for truck in list_of_trucks:
            new_truck = Truck.Truck(truck)
            truck_list.append(new_truck)
        return truck_list

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
        least_loaded_truck = 0
        max = 0
        index = 0
        loaded_deliveries = []
        while self.timed_requests:
            for trucks in self.truck_list:
                num = trucks.num_of_timed_packages
                if max == 0:
                    max = num
                    least_loaded_truck = trucks.truck_number
                else:
                    if num < max:
                        least_loaded_truck = trucks.truck_number
                    else:  # num is greater than max, num is the new max
                        max = num
        # Add the package to the least loaded truck
            time = self.timed_requests[index][0]
            before_after = self.timed_requests[index][1]
            package_number = self.timed_requests[index][2]
            self.loadTimedPackagedByTruckNumber(least_loaded_truck, time, before_after, package_number)
            package_tuple = (time, before_after, package_number)
            self.timed_requests.remove(package_tuple)
            loaded_deliveries.append(package_number)
            for item in self.packages_to_be_delivered:
                if item == package_number:
                    self.packages_to_be_delivered.remove(package_number)


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

    # Loads trucks with packages up to their capacity
    def loadTrucksToMaxCapacity(self):
        for truck in self.truck_list:
            current_load = truck.num_of_timed_packages + truck.num_of_packages
            while current_load < self.max_num_package_per_truck:
                self.loadPackageByTruckNumber(truck.truck_number, self.packages_to_be_delivered[0])
                current_load = current_load + 1

    # Run a singular truck simulation **test**
    def runTruckSimulation(self):






