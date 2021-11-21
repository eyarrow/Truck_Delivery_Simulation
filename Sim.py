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
                                                                                    # restrictions
        self.packages_that_are_delivered = []  # packages that have been delivered
        self.total_distance_traveled = 0
        self.timed_requests = []  # Packages that must be delivered before or after a given time.
        self.max_num_package_per_truck = max_num_package_per_truck

    # Move a package from one list to another list
    def movePackageFromOneListToAnother(self, source_list, dest_list, package_id):
        package = self.new_packages.returnPackageByID(package_id)
        source_list.remove(package)
        dest_list.append(package)

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

        # 13, 14, 16, 20, 25, 29, 30, 31, 34, 37, 40 by 10:30 am, split evenly between two trucks. Run through
        # optimization first, so that the order is as beneficial as possible.
        # 6 is a unique case, because it needs to delivered by 10:30 but won't be available until 9:05
        # self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1, 15)
        # self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1, 15)
        # self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1, 15)
        # self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1, 15)
        # self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1, 15)
        # self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1, 15)
        # self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1, 15)
        # self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1, 15)
        # self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1, 15)
        # self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_with_deadline_truck1, 15)

        # Remove packages that are not available at first load
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_not_available, 6)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_not_available, 25)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_not_available, 28)
        self.movePackageFromOneListToAnother(self.packages_with_no_restrictions, self.packages_not_available, 32)

        self.truck1.packages = self.packages_truck1
        self.truck2.packages = self.packages_truck2

        self.runIndividualTruckSimulation(self.truck1, self.packages_with_deadline_truck1, '08:00')

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

