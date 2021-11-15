# Module to manage trucks individually and in aggregate.
import DataStructures


# Class to manage instructions around deliveries that require special timing. "time" is the time on the clock by or
# before the package must be delivered. Application assumes that military time is used, and leading zeroes are included.
# (ex: 09:00 is valid whereas 9:00 is not) "before_after" should be either 0 or 1. 0 means that the package should be
# delivered BEFORE the given time, whereas, 1 means that the package should be delivered after that time.
# "package_number" is the number of the package to be delivered.
class TimedDelivery:
    def __init__(self, time, before_after, package_number):
        self.TimedDelivery = (time, before_after, package_number)

    # check to see whether or not package is eligible for delivery at a given point in time. Returns true if
    # the package is deliverable, false if it is too early for delivery
    def checkDeliveryElligibility(self, current_time):
        if self.TimedDelivery[1] == 0:  # If it is supposed to be delivered before the given time, the answer is always yes
            return True
        else:  # Must be after a certain time, so check the condition
            if self.determineIfTimeIsAfter(current_time) is True:
                return True
            else:
                return False

    def returnPackageID(self):
        return self.TimedDelivery[2]

    # Given a time as a parameter, determines if the time entered as a parameter is after the objects given time.
    # if so returns true, else returns false. Assumes time given is military time, with leading zeroes included
    def determineIfTimeIsAfter(self, time):
        parse_hour = self.TimedDelivery[0][:2]
        parse_minute = self.TimedDelivery[0][3:5]
        parse_given_hour = time.TimedDelivery[0][:2]
        parse_given_minute = time.TimedDelivery[0][3:5]

        if parse_given_hour > parse_hour:
            return True
        else:
            if parse_given_hour < parse_hour:  # if given hour is before objects hour
                return False
            else:
                if parse_given_minute < parse_minute:  # if given minute is before objects minutes
                    return False
                else:
                    return True


# Class to manage each individual truck throughout the delivery process. "packages" represent all packages that are
# loaded on the truck that DO NOT have time constraints. "packages_timed_delivery" is a linked list of packages that
# do have time constraints. These are added as "TimedDelivery" objects which help determine delivery logic. The list
# is always maintained in sorted order of when the package should be delivered.
class Truck:
    def __init__(self, truck_number, miles=0, location='Depot'):
        self.truck_number = truck_number
        self.miles = miles
        self.location = location
        self.packages = []  # List of packages with no special instructions
        self.packages_timed_delivery = DataStructures.LinkedList()  # Packages with instructions around delivery times
        self.num_of_timed_packages = 0
        self.num_of_packages = 0
        self.delivered_packages = []
        self.truck_time = "08:00:00"  # "local time" on the truck

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
        self.num_of_packages = self.num_of_packages+1

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
        new_timed_delivery = TimedDelivery(time, before_after, package_number)
        self.num_of_timed_packages = self.num_of_timed_packages + 1
        # check to see if Linked list has data
        iterate = self.packages_timed_delivery  # linked list object
        trail = None
        temp = None
        # If the list is empty add tne new node
        if self.packages_timed_delivery.head.data is None:
            self.packages_timed_delivery.addToLinkedList(new_timed_delivery)
        # If there are members in the list, there are existing nodes. Check to see if the first node is greater
        # than the incoming one
        else:
            if new_timed_delivery.determineIfTimeIsAfter(self.packages_timed_delivery.head.data):
                temp = self.packages_timed_delivery.head
                new_delivery = DataStructures.Node(new_timed_delivery)
                new_delivery.next = temp
                self.packages_timed_delivery.head = new_delivery
            else:  # iterate until we find a spot
                trail = self.packages_timed_delivery.head
                iterate = self.packages_timed_delivery.head.next
                while iterate:
                    if new_timed_delivery.determineIfTimeIsAfter(iterate.data):
                        new_delivery = DataStructures.Node(new_timed_delivery)
                        trail.next = new_delivery
                        new_delivery.next = iterate
                        return
                    else:
                        trail = iterate
                        iterate = iterate.next
                # add at the end
                self.packages_timed_delivery.addToLinkedList(new_timed_delivery)

    # Move a package for the normal delivery schedule to a requested time delivery. The timed delivery information
    # must be included in parameters, and items will be removed from the regular list once prioritized.
    def moveFromNormalDeliveryToTimedDelivery(self, time, before_after, package_number):
        self.packages.remove(package_number)
        self.addToTimedDeliveryList(time, before_after, package_number)
        self.num_of_packages = self.num_of_packages-1

    # Return a list of time sensitive packages that are eligible for delivery. Makes sure that they
    # have not already been delivered, and that they are currently eligible by time.
    def getTimeSensitivePackagesList(self, packages):
        clock = self.truck_time
        number_of_deliverable_packages = 0
        deliverable_package_list = []
        undeliverable = []
        temp = self.packages_timed_delivery.head
        trail = temp
        delivered_check = False
        while temp.next is not None:
            time = TimedDelivery(clock, 0, 0)
            is_deliverable = temp.data.checkDeliveryElligibility(time)
            if is_deliverable:
                number_of_deliverable_packages = number_of_deliverable_packages+1
                package_id = temp.data.returnPackageID()
                deliverable_package_list.append(package_id)
                self.num_of_timed_packages = self.num_of_timed_packages - 1
                trail.next = temp.next
                temp = None
                temp = trail.next
            else:
                undeliverable.append(temp.data)
                temp = temp.next
                trail = trail.next
        print(f"List to be delivered after run: ")
        temp = self.packages_timed_delivery.head
        while temp.next is not None:
            print(temp.data.returnPackageID())
            temp = temp.next
        return deliverable_package_list

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



    def deliverPackage(self, package_number, distance):
        self.delivered_packages.append(package_number)
        self.miles = self.miles + distance
        time_elapsed = distance / 18
        minutes = time_elapsed * 60
        self.addTimeToClock(minutes)
        return self.truck_time

    # removes packages from the list to be delivered once they are delivered.
    def updatePackageList(self, list_of_delivered_packages):
        for item in self.packages:
            for package in list_of_delivered_packages:
                if item == package:
                    self.packages.remove(package)







