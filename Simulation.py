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
                 num_of_addresses):
        self.new_packages = Package.PackagesToBeDelivered(filename_of_packages, filename_of_distances,
                                                          filename_address_index, num_of_addresses)
        self.truck_list = self.initializeTrucks(list_of_trucks)
        self.num_of_trucks = len(self.truck_list)
        self.clock = '08:00'
        self.specific_truck_requests = []  # Packages that must be delivered on a specific truck
        self.timed_requests = []  # Packages that must be delivered before or after a given time.

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
        self.specific_truck_requests = []






