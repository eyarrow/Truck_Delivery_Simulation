# Module to manage trucks individually and in aggregate.
import DataStructures


# Class to manage instructions around deliveries that require special timing. "time" is the time on the clock by or
# before the package must be delivered. Application assumes that military time is used, and leading zeroes are included.
# (ex: 09:00 is valid whereas 9:00 is not) "before_after" should be either 0 or 1. 0 means that the package should be
# delivered BEFORE the given time, whereas, 1 means that the package should be delivered after that time.
# "package_number" is the number of the package to be delivered.
class TimedDelivery:
    def __init__(self, time, before_after, package_number):
        self.time = time
        self.before_after = before_after
        self.package_number = package_number

    # check to see whether or not package is eligible for delivery at a given point in time. Returns true if
    # the package is deliverable, false if it is too early for delivery
    def checkDeliveryElligibility(self, current_time):
        parse_hour_current = current_time[:2]
        parse_minute_current = current_time[3:5]
        parse_hour = self.time[:2]
        parse_minute = self.time[3:5]
        if self.before_after is 0:  # If it is supposed to be delivered before the given time, the answer is always yes
            return True
        else:  # Must be after a certain time, so check the condition
            if parse_hour > parse_hour_current:
                return False
            else:
                if parse_hour < parse_hour_current:
                    return True
                else:  # hours are equal check minutes
                    if parse_minute < parse_minute_current:
                        return True
                    else:
                        return False




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
