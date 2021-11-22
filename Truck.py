# Module to manage trucks individually and in aggregate.
import DataStructures

# Class to manage each individual truck throughout the delivery process. "packages" represent all packages that are
# loaded on the truck that DO NOT have time constraints. packages_to_hold are packages that need to be held for delivery
# The simulation algorithm will leave those deliveries for end of day.
class Truck:
    def __init__(self, truck_number=-1, miles=0, location='Depot'):
        self.truck_number = truck_number  # a truck number
        self.miles = miles  # aggregate of miles driven. Starts at zero
        self.packages = []  # List of packages with no special instructions
        self.packages_to_hold = []
        self.truck_time = "08:00:00"  # "local time" on the truck

    # Given a time as a parameter, determines if the time entered as a parameter is after the trucks clock time.
    # if so returns true, else returns false. Assumes time given is military time, with leading zeroes included
    def determineIfTimeIsAfter(self, delivery_time):
        hour, minute = map(int, delivery_time.split(':'))

        given_time = self.truck_time[:5]
        given_hour, given_minute = map(int, given_time.split(':'))

        if given_hour > hour:
            return True
        else:
            if given_hour < hour:  # if given hour is before objects hour
                return False
            else:
                if given_minute < minute:  # if given minute is before objects minutes
                    return False
                else:
                    return True

    # # check to see whether or not package is eligible for delivery at a given point in time. Returns true if
    # # the package is deliverable, false if it is too early for delivery
    # def checkDeliveryElligibility(self, delivery_time, before_after_flag):
    #     if before_after_flag == 0:  # If it is supposed to be delivered before the given time, the answer is always yes
    #         return True
    #     else:  # Must be after a certain time, so check the condition
    #         if self.determineIfTimeIsAfter(delivery_time) is True:
    #             return True
    #         else:
    #             return False

    # Returns the list of packages to be delivered
    def returnPackages(self):
        return self.packages

    # Returns the list of packages that have timed delivery requirements
    def returnPackagesTimedDeivery(self):
        return self.packages_timed_delivery

    # Returns the number of miles driven by the truck in a given work day
    def returnMiles(self):
        return self.miles

    # Returns the truck's current location
    def returnLocation(self):
        return self.location

    # Add a package to the package list
    def addToPackageList(self, package_number):
        self.packages.append(package_number)
        self.num_of_packages = self.num_of_packages + 1

    # Checks to see if package number provided already exists on list. If it does returns true
    def checkIfPackageOnPackageList(self, package_number):
        flag = False
        for package in self.packages:
            if package == package_number:
                flag = True
        return flag

    # Add a package to the time delivery list. These are packages that need to be delivered before or after a given
    # time
    def addToTimedDeliveryList(self, time, before_after, package_number):
        def sortOrder(myList):
            time = myList[0]
            hour, minute = map(int, time.split(':'))
            return (hour * 60) + minute

        new_timed_delivery = (time, before_after, package_number)
        self.packages_timed_delivery.append(new_timed_delivery)
        self.num_of_timed_packages = self.num_of_timed_packages + 1
        self.packages_timed_delivery.sort(key=sortOrder)

    # Move a package for the normal delivery schedule to a requested time delivery. The timed delivery information
    # must be included in parameters, and items will be removed from the regular list once prioritized.
    def moveFromNormalDeliveryToTimedDelivery(self, time, before_after, package_number):
        self.packages.remove(package_number)
        self.addToTimedDeliveryList(time, before_after, package_number)
        self.num_of_packages = self.num_of_packages - 1

    # Return a list of time sensitive packages that are eligible for delivery. Makes sure that they
    # have not already been delivered, and that they are currently eligible by time.
    def getTimeSensitivePackagesList(self, packages):
        hold_list = []
        ready_list = []
        delivery_values = self.packages_timed_delivery
        for item in delivery_values:
            is_eligible = self.checkDeliveryElligibility(item[0], item[1])
            if is_eligible:
                package_id = item[2]
                ready_list.append(package_id)
            else:
                hold_list.append(item)
        self.packages_timed_delivery = hold_list
        return ready_list

    # Increments the truck clock
    def addTimeToClock(self, minutes):
        hour = 0
        minute = 0
        seconds = 0
        if minutes > 60:
            hour = int(minutes / 60)
        minute = int(minutes % 60)
        left_over = minutes - ((hour * 60) + minute)
        seconds = int(left_over * 60)
        existing_hour = int(self.truck_time[:2])
        existing_minute = int(self.truck_time[3:5])
        existing_second = int(self.truck_time[7:9])

        new_hour = hour + existing_hour
        new_minute = minute + existing_minute
        new_second = seconds + existing_second

        if new_second > 60:
            num = new_second % 60
            new_second = num
            new_minute = new_minute + 1

        if new_minute > 60:
            num = new_minute % 60
            new_minute = num
            new_hour = new_hour + 1

        # Convert back to string
        if new_second < 10:
            string_second = "0" + str(new_second)
        else:
            string_second = str(new_second)

        if new_minute < 10:
            string_minute = "0" + str(new_minute)
        else:
            string_minute = str(new_minute)

        if new_hour < 10:
            string_hour = "0" + str(new_hour)
        else:
            string_hour = str(new_hour)

        combined_time_string = string_hour + ":" + string_minute + ":" + string_second
        self.truck_time = combined_time_string

    # Updates distance traveled and clock time for a truck. Takes the distance traveled as a parameter
    def deliverPackage(self, distance):
        self.miles = self.miles + distance
        time_elapsed = distance / 18
        minutes = time_elapsed * 60
        if distance > 0:
            self.addTimeToClock(minutes)
        return self.truck_time

    # removes packages from the list to be delivered once they are delivered.
    def updatePackageList(self):
        for item in self.delivered_packages:
            for package in self.packages:
                if item == package:
                    self.packages.remove(item)
