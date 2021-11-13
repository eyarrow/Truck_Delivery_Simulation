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
        if self.before_after == 0:  # If it is supposed to be delivered before the given time, the answer is always yes
            return True
        else:  # Must be after a certain time, so check the condition
            if self.determineIfTimeIsAfter(current_time) is True:
                return True
            else:
                return False

    # Given a time as a parameter, determines if the time entered as a parameter is after the objects given time.
    # if so returns true, else returns false. Assumes time given is military time, with leading zeroes included
    def determineIfTimeIsAfter(self, time):
        parse_hour = self.TimedDelivery[0][:2]
        print(parse_hour)
        parse_minute = self.TimedDelivery[0][3:5]
        print(parse_minute)
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

    def returnPackages(self):
        return self.packages

    def returnPackagesTimedDeivery(self):
        return self.packages_timed_delivery

    def returnMiles(self):
        return self.miles

    def returnLocation(self):
        return self.location

    def addToPackageList(self, package_number):
        self.packages.append(package_number)

    def addToTimedDeliveryList(self, time, before_after, package_number):
        new_timed_delivery = TimedDelivery(time, before_after, package_number)
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




