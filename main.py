# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import Package
import Truck

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Load the package data for the simulation, including packages to be delivered, addresses, and their distance
    # information
    new_packages = Package.PackagesToBeDelivered('packages.csv', 'distances.csv', 'addresslist.csv', 27)
    new_packages.printAllPackages()

    truck1 = Truck.Truck(1)
    truck1.addToTimedDeliveryList('09:00', 0, 15)
    truck1.addToTimedDeliveryList('08:00', 0, 21)
    truck1.addToTimedDeliveryList('10:00', 0, 5)
    truck1.addToTimedDeliveryList('10:30', 1, 7)
    truck1.addToTimedDeliveryList('10:00', 0, 8)
    truck1.addToTimedDeliveryList('08:00', 0, 2)
    truck1.addToTimedDeliveryList('12:00', 0, 9)

    print("There is something about Mary")
